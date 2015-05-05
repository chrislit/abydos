# -*- coding: utf-8 -*-
"""abydos.compression

The compression module defines compression functions for use within Abydos,
including:
    ac_train, ac_encode, & ac_decode -- arithmetic coding functions
    bwt_encode & bwt_decode -- Burrows-Wheeler transform encoder/decoder
    rle_encode & rle_decode -- Run-Length Encoding encoder/decoder


Copyright 2014-2015 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
from __future__ import division
from collections import Counter
from itertools import groupby
from .util import Rational
from ._compat import _unicode, _long, _range

def ac_train(text):
    """Generate a probability dict from the provided text

    Text -> 0-order probability statistics as a dict

    Text must not contain the NUL (0x00) character because that's used to
    indicate the end of data.

    This is based on Andrew Dalke's public domain implementation:
    http://code.activestate.com/recipes/306626/
    It has been ported to use the custom Rational class above.
    """
    text = _unicode(text)
    if '\x00' in text:
        text = text.replace('\x00', ' ')
    counts = Counter(text)
    counts['\x00'] = 1
    tot_letters = sum(counts.values())

    tot = 0
    prob_range = {}
    prev = Rational(0)
    for char, count in sorted(counts.items(), key=lambda x: (x[1], x[0]),
                           reverse=True):
        follow = Rational(tot + count, tot_letters)
        prob_range[char] = (prev, follow)
        prev = follow
        tot = tot + count
    assert tot == tot_letters

    return prob_range


def ac_encode(text, probs):
    """Encode a text using arithmetic coding with the provided probabilities

    Text and the 0-order probability statistics -> longval, nbits

    The encoded number is rational(longval, 2**nbits)

    This is based on Andrew Dalke's public domain implementation:
    http://code.activestate.com/recipes/306626/
    It has been ported to use the custom Rational class above.
    """
    text = _unicode(text)
    if '\x00' in text:
        text = text.replace('\x00', ' ')
    minval = Rational(0)
    maxval = Rational(1)
    for char in text + '\x00':
        prob_range = probs[char]
        delta = maxval - minval
        maxval = minval + prob_range[1] * delta
        minval = minval + prob_range[0] * delta

    # I tried without the /2 just to check.  Doesn't work.
    # Keep scaling up until the error range is >= 1.  That
    # gives me the minimum number of bits needed to resolve
    # down to the end-of-data character.
    delta = (maxval - minval) / 2
    nbits = _long(0)
    while delta < 1:
        nbits = nbits + 1
        delta <<= 1
    if nbits == 0: # pragma: no cover
        return 0, 0
    else:
        # using -1 instead of /2
        avg = (maxval + minval)<<(nbits-1)
    # Could return a rational instead ...
    return avg.p//avg.q, nbits  # the division truncation is deliberate

def ac_decode(longval, nbits, probs):
    """Decode the number to a string using the given statistics

    This is based on Andrew Dalke's public domain implementation:
    http://code.activestate.com/recipes/306626/
    It has been ported to use the custom Rational class above.
    """
    val = Rational(longval, _long(1)<<nbits)
    letters = []
    probs_items = [(char, minval, maxval) for (char, (minval, maxval))
                   in probs.items()]

    char = '\x00'
    while True:
        for (char, minval, maxval) in probs_items:
            if minval <= val < maxval:
                break

        if char == '\x00':
            break
        letters.append(char)
        delta = maxval - minval
        val = (val - minval)/delta
    return ''.join(letters)


def bwt_encode(word, terminator='\0'):
    """Return the Burrows-Wheeler transformed form of a word

    Arguments:
    word -- the word to transform using BWT
    terminator -- a character to add to word to signal the end of the string

    Description:
    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression.
    Cf. https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform
    """
    if word:
        assert terminator not in word, ('Specified terminator, '+
                                        (terminator if terminator else '\\0')+
                                        ', already in word.')
        word += terminator
        wordlist = sorted([word[i:]+word[:i] for i in _range(len(word))])
        return ''.join([w[-1] for w in wordlist])
    return terminator


def bwt_decode(code, terminator='\0'):
    """Return a word decoded from BWT form

    Arguments:
    code -- the word to transform from BWT form
    terminator -- a character added to word to signal the end of the string

    Description:
    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression. This function reverses the transform.
    Cf. https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform
    """
    if code:
        assert terminator in code, ('Specified terminator, '+
                                    (terminator if terminator else '\\0')+
                                    ', absent from word.')
        wordlist = [''] * len(code)
        for i in _range(len(code)):
            wordlist = sorted([code[i]+wordlist[i] for i in _range(len(code))])
        s = [w for w in wordlist if w[-1] == terminator][0]
        return s.rstrip(terminator)
    return ''


def rle_encode(text, use_bwt=True):
    """Simple, crude run-length-encoding (RLE) encoder
    http://rosettacode.org/wiki/Run-length_encoding#Python

    Arguments:
    text -- a text string to encode
    use_bwt -- boolean indicating whether to perform BWT encoding before RLE

    Description:
    Based on http://rosettacode.org/wiki/Run-length_encoding#Python

    Digits 0-9 cannot be in text.
    """
    if use_bwt:
        text = bwt_encode(text)
    text = [(len(list(g)),k) for k,g in groupby(text)]
    text = [(str(n)+k if n>2 else (k if n==1 else 2*k)) for n,k in text]
    return ''.join(text)

def rle_decode(text, use_bwt=True):
    """Simple, crude run-length-encoding (RLE) decoder

    Arguments:
    text -- a text string to decode
    use_bwt -- boolean indicating whether to perform BWT decoding after RLE
        decoding

    Description:
    Based on http://rosettacode.org/wiki/Run-length_encoding#Python

    Digits 0-9 cannot have been in the original text.
    """
    mult = ''
    decoded = []
    for l in list(text):
        if not l.isdigit():
            if mult:
                decoded.append(int(mult)*l)
                mult = ''
            else:
                decoded.append(l)
        else:
            mult += l

    text = ''.join(decoded)
    if use_bwt:
        text = bwt_decode(text)
    return text