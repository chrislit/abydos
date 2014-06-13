# -*- coding: utf-8 -*-
"""abydos.clustering

The clustering module implements clustering algorithms such as string
fingerprinting, k-nearest neighbors, and ...


Copyright 2014 by Christopher C. Little.
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
import unicodedata
import numpy as np
from ._compat import _unicode
from .phonetic import double_metaphone
from .qgram import QGrams
from .distance import sim


def fingerprint(phrase):
    """Return the fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the fingerprint of

    Description:
    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening spaces
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
    phrase = ' '.join(sorted(list(set(phrase.split()))))
    return phrase


def qgram_fingerprint(phrase, qval=2, start_stop=''):
    """Return the q-gram fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the q-gram fingerprint of
    qval -- the length of each q-gram (by default 2)
    start_stop -- the start & stop symbol(s) to concatenate on either end of
        the phrase, as defined in abydos.util.qgram()

    Description:
    A q-gram fingerprint is a string consisting of all of the unique q-grams
    in a string, alphabetized & concatenated.
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum()])
    phrase = QGrams(phrase, qval, start_stop)
    phrase = ''.join(sorted(list(phrase)))
    return phrase


def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone, *args):
    """Return the phonetic fingerprint of a phrase

    Arguments:
    phrase -- a string to calculate the phonetic fingerprint of
    phonetic_algorithm -- a phonetic algorithm that takes a string and returns
        a string (presumably a phonetic representation of the original string)
        By default, this function uses double_metaphone() from abydos.phonetic.
    *args -- additional arguments to pass to the phonetic algorithm, along with
        the phrase itself

    Description:
    A phonetic fingerprint is identical to a standard string fingerprint, as
    implemented in abydos.clustering.fingerprint(), but performs the
    fingerprinting function after converting the string to its phonetic form,
    as determined by some phonetic algorithm.
    """
    phrase = phonetic_algorithm(phrase, *args)
    if hasattr(phrase, '__iter__'):
        phrase = phrase[0]
    return fingerprint(phrase)


def skeleton_key(word):
    """Return the skeleton key of a word

    Arguments:
    word -- the word to transform into its skeleton key

    Description:
    The skeleton key of a word is defined in:
    Pollock, Joseph J. and Antonio Zamora. 1984. "Automatic Spelling Correction
    in Scientific and Scholarly Text." Communications of the ACM, 27(4).
    358--368. <http://dl.acm.org/citation.cfm?id=358048>
    """
    _vowels = 'AEIOU'

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    start = word[0:1]
    consonant_part = ''
    vowel_part = ''

    # add consonants & vowels to to separate strings
    # (omitting the first char & duplicates)
    for char in word[1:]:
        if char != start:
            if char in _vowels:
                if char not in vowel_part:
                    vowel_part += char
            elif char not in consonant_part:
                consonant_part += char
    # return the first char followed by consonants followed by vowels
    return start + consonant_part + vowel_part


def omission_key(word):
    """Return the omission key of a word

    Arguments:
    word -- the word to transform into its omission key

    Description:
    The omission key of a word is defined in:
    Pollock, Joseph J. and Antonio Zamora. 1984. "Automatic Spelling Correction
    in Scientific and Scholarly Text." Communications of the ACM, 27(4).
    358--368. <http://dl.acm.org/citation.cfm?id=358048>
    """
    _consonants = 'JKQXZVWYBFMGPDHCLNTSR'

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    key = ''

    # add consonants in order supplied by _consonants (no duplicates)
    for char in _consonants:
        if char in word:
            key += char

    # add vowels in order they appeared in the word (no duplicates)
    for char in word:
        if char not in _consonants and char not in key:
            key += char

    return key


def mean_pairwise_similarity(collection, metric=sim,
                             mean='harmonic', symmetric=False):
    """Return the mean pairwise similarity of a collection of strings

    Arguments:
    collection -- a tuple, list, or set of terms or a string that can be split
    metric -- a similarity metric function
    mean -- 'harmonic', 'geometric', or 'arithmetic': the mean type
    symmetric -- set to True if all pairwise similarities should be calculated
                    in both directions
    """
    if hasattr(collection, 'split'):
        collection = collection.split()
    if not hasattr(collection, '__iter__'):
        raise ValueError('collection is neither a string nor iterable type')
    elif len(collection) < 2:
        raise ValueError('collection has fewer than two members')

    pairwise_values = []

    for i, word1 in list(enumerate(collection)):
        for j, word2 in list(enumerate(collection)):
            if i != j:
                pairwise_values.append(metric(word1, word2))
                if symmetric:
                    pairwise_values.append(metric(word2, word1))

    if mean == 'harmonic':
        return len(pairwise_values)/sum([1/x for x in pairwise_values])
    elif mean == 'geometric':
        return (np.prod(pairwise_values)**(1/len(pairwise_values)))
    elif mean == 'arithmetic':
        return sum(pairwise_values)/len(pairwise_values)
    else:
        raise ValueError('Unknown mean type')
