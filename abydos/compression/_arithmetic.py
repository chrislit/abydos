# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.compression._arithmetic.

Arithmetic coder/decoder
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter
from fractions import Fraction

from six import PY3, text_type


if PY3:
    long = int

__all__ = ['Arithmetic', 'ac_decode', 'ac_encode', 'ac_train']


class Arithmetic(object):
    """Arithmetic Coder.

    This is based on Andrew Dalke's public domain implementation
    :cite:`Dalke:2005`. It has been ported to use the fractions.Fraction class.
    """

    _probs = {}

    def __init__(self, text=None):
        """Initialize arithmetic coder object.

        Parameters
        ----------
        text : str
            The training text

        """
        if text is not None:
            self.train(text)

    def get_probs(self):
        """Return the probs dictionary.

        Returns
        -------
        dict
            The dictionary of probabilities

        """
        return self._probs

    def set_probs(self, probs):
        """Set the probs dictionary.

        Parameters
        ----------
        probs : dict
            The dictionary of probabilities

        """
        self._probs = probs

    def train(self, text):
        r"""Generate a probability dict from the provided text.

        Text to 0-order probability statistics as a dict

        Parameters
        ----------
        text : str
            The text data over which to calculate probability statistics. This
            must not contain the NUL (0x00) character because that is used to
            indicate the end of data.

        Example
        -------
        >>> ac = Arithmetic()
        >>> ac.train('the quick brown fox jumped over the lazy dog')
        >>> ac.get_probs()
        {' ': (Fraction(0, 1), Fraction(8, 45)),
         'o': (Fraction(8, 45), Fraction(4, 15)),
         'e': (Fraction(4, 15), Fraction(16, 45)),
         'u': (Fraction(16, 45), Fraction(2, 5)),
         't': (Fraction(2, 5), Fraction(4, 9)),
         'r': (Fraction(4, 9), Fraction(22, 45)),
         'h': (Fraction(22, 45), Fraction(8, 15)),
         'd': (Fraction(8, 15), Fraction(26, 45)),
         'z': (Fraction(26, 45), Fraction(3, 5)),
         'y': (Fraction(3, 5), Fraction(28, 45)),
         'x': (Fraction(28, 45), Fraction(29, 45)),
         'w': (Fraction(29, 45), Fraction(2, 3)),
         'v': (Fraction(2, 3), Fraction(31, 45)),
         'q': (Fraction(31, 45), Fraction(32, 45)),
         'p': (Fraction(32, 45), Fraction(11, 15)),
         'n': (Fraction(11, 15), Fraction(34, 45)),
         'm': (Fraction(34, 45), Fraction(7, 9)),
         'l': (Fraction(7, 9), Fraction(4, 5)),
         'k': (Fraction(4, 5), Fraction(37, 45)),
         'j': (Fraction(37, 45), Fraction(38, 45)),
         'i': (Fraction(38, 45), Fraction(13, 15)),
         'g': (Fraction(13, 15), Fraction(8, 9)),
         'f': (Fraction(8, 9), Fraction(41, 45)),
         'c': (Fraction(41, 45), Fraction(14, 15)),
         'b': (Fraction(14, 15), Fraction(43, 45)),
         'a': (Fraction(43, 45), Fraction(44, 45)),
         '\x00': (Fraction(44, 45), Fraction(1, 1))}

        """
        text = text_type(text)
        if '\x00' in text:
            text = text.replace('\x00', ' ')
        counts = Counter(text)
        counts['\x00'] = 1
        tot_letters = sum(counts.values())

        tot = 0
        self._probs = {}
        prev = Fraction(0)
        for char, count in sorted(
            counts.items(), key=lambda x: (x[1], x[0]), reverse=True
        ):
            follow = Fraction(tot + count, tot_letters)
            self._probs[char] = (prev, follow)
            prev = follow
            tot = tot + count

    def encode(self, text):
        """Encode a text using arithmetic coding.

        Text and the 0-order probability statistics -> longval, nbits

        The encoded number is Fraction(longval, 2**nbits)

        Parameters
        ----------
        text : str
            A string to encode

        Returns
        -------
        tuple
            The arithmetically coded text

        Example
        -------
        >>> ac = Arithmetic('the quick brown fox jumped over the lazy dog')
        >>> ac.encode('align')
        (16720586181, 34)

        """
        text = text_type(text)
        if '\x00' in text:
            text = text.replace('\x00', ' ')
        minval = Fraction(0)
        maxval = Fraction(1)

        for char in text + '\x00':
            prob_range = self._probs[char]
            delta = maxval - minval
            maxval = minval + prob_range[1] * delta
            minval = minval + prob_range[0] * delta

        # I tried without the /2 just to check.  Doesn't work.
        # Keep scaling up until the error range is >= 1.  That
        # gives me the minimum number of bits needed to resolve
        # down to the end-of-data character.
        delta = (maxval - minval) / 2
        nbits = long(0)
        while delta < 1:
            nbits += 1
            delta *= 2
        # The below condition shouldn't ever be false
        if nbits == 0:  # pragma: no cover
            return 0, 0
        # using -1 instead of /2
        avg = (maxval + minval) * 2 ** (nbits - 1)
        # Could return a rational instead ...
        # the division truncation is deliberate
        return avg.numerator // avg.denominator, nbits

    def decode(self, longval, nbits):
        """Decode the number to a string using the given statistics.

        Parameters
        ----------
        longval : int
            The first part of an encoded tuple from encode
        nbits : int
            The second part of an encoded tuple from encode

        Returns
        -------
        str
            The arithmetically decoded text

        Example
        -------
        >>> ac = Arithmetic('the quick brown fox jumped over the lazy dog')
        >>> ac.decode(16720586181, 34)
        'align'

        """
        val = Fraction(longval, long(1) << nbits)
        letters = []

        probs_items = [
            (char, minval, maxval)
            for (char, (minval, maxval)) in self._probs.items()
        ]

        char = '\x00'
        while True:
            for (char, minval, maxval) in probs_items:  # noqa: B007
                if minval <= val < maxval:
                    break

            if char == '\x00':
                break
            letters.append(char)
            delta = maxval - minval
            val = (val - minval) / delta
        return ''.join(letters)


def ac_train(text):
    r"""Generate a probability dict from the provided text.

    This is a wrapper for :py:meth:`Arithmetic.train`.

    Parameters
    ----------
    text : str
        The text data over which to calculate probability statistics. This must
        not contain the NUL (0x00) character because that's used to indicate
        the end of data.

    Returns
    -------
    dict
        A probability dict

    Example
    -------
    >>> ac_train('the quick brown fox jumped over the lazy dog')
    {' ': (Fraction(0, 1), Fraction(8, 45)),
     'o': (Fraction(8, 45), Fraction(4, 15)),
     'e': (Fraction(4, 15), Fraction(16, 45)),
     'u': (Fraction(16, 45), Fraction(2, 5)),
     't': (Fraction(2, 5), Fraction(4, 9)),
     'r': (Fraction(4, 9), Fraction(22, 45)),
     'h': (Fraction(22, 45), Fraction(8, 15)),
     'd': (Fraction(8, 15), Fraction(26, 45)),
     'z': (Fraction(26, 45), Fraction(3, 5)),
     'y': (Fraction(3, 5), Fraction(28, 45)),
     'x': (Fraction(28, 45), Fraction(29, 45)),
     'w': (Fraction(29, 45), Fraction(2, 3)),
     'v': (Fraction(2, 3), Fraction(31, 45)),
     'q': (Fraction(31, 45), Fraction(32, 45)),
     'p': (Fraction(32, 45), Fraction(11, 15)),
     'n': (Fraction(11, 15), Fraction(34, 45)),
     'm': (Fraction(34, 45), Fraction(7, 9)),
     'l': (Fraction(7, 9), Fraction(4, 5)),
     'k': (Fraction(4, 5), Fraction(37, 45)),
     'j': (Fraction(37, 45), Fraction(38, 45)),
     'i': (Fraction(38, 45), Fraction(13, 15)),
     'g': (Fraction(13, 15), Fraction(8, 9)),
     'f': (Fraction(8, 9), Fraction(41, 45)),
     'c': (Fraction(41, 45), Fraction(14, 15)),
     'b': (Fraction(14, 15), Fraction(43, 45)),
     'a': (Fraction(43, 45), Fraction(44, 45)),
     '\x00': (Fraction(44, 45), Fraction(1, 1))}

    """
    return Arithmetic(text).get_probs()


def ac_encode(text, probs):
    """Encode a text using arithmetic coding with the provided probabilities.

    This is a wrapper for :py:meth:`Arithmetic.encode`.

    Parameters
    ----------
    text : str
        A string to encode
    probs : dict
        A probability statistics dictionary generated by
        :py:meth:`Arithmetic.train`

    Returns
    -------
    tuple
        The arithmetically coded text

    Example
    -------
    >>> pr = ac_train('the quick brown fox jumped over the lazy dog')
    >>> ac_encode('align', pr)
    (16720586181, 34)

    """
    coder = Arithmetic()
    coder.set_probs(probs)
    return coder.encode(text)


def ac_decode(longval, nbits, probs):
    """Decode the number to a string using the given statistics.

    This is a wrapper for :py:meth:`Arithmetic.decode`.

    Parameters
    ----------
    longval : int
        The first part of an encoded tuple from ac_encode
    nbits : int
        The second part of an encoded tuple from ac_encode
    probs : dict
        A probability statistics dictionary generated by
        :py:meth:`Arithmetic.train`

    Returns
    -------
    str
        The arithmetically decoded text

    Example
    -------
    >>> pr = ac_train('the quick brown fox jumped over the lazy dog')
    >>> ac_decode(16720586181, 34, pr)
    'align'

    """
    coder = Arithmetic()
    coder.set_probs(probs)
    return coder.decode(longval, nbits)


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
