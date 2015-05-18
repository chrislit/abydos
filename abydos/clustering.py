# -*- coding: utf-8 -*-

# Copyright 2014-2015 by Christopher C. Little.
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

"""abydos.clustering

The clustering module implements clustering algorithms such as:
    - string fingerprinting
"""

from __future__ import unicode_literals
from __future__ import division
import unicodedata
from ._compat import _unicode
from .phonetic import double_metaphone
from .qgram import QGrams
from .distance import sim
from .stats import hmean


def fingerprint(phrase):
    """String fingerprint

    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening spaces

    :param phrase: the string from which to calculate the fingerprint
    :returns: the fingerprint of the phrase
    :rtype: str
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
    phrase = ' '.join(sorted(list(set(phrase.split()))))
    return phrase


def qgram_fingerprint(phrase, qval=2, start_stop=''):
    """Q-Gram fingerprint

    A q-gram fingerprint is a string consisting of all of the unique q-grams
    in a string, alphabetized & concatenated.

    :param phrase: the string from which to calculate the q-gram fingerprint
    :param qval: the length of each q-gram (by default 2)
    :param start_stop: the start & stop symbol(s) to concatenate on either end
        of the phrase, as defined in abydos.util.qgram()
    :returns: the q-gram fingerprint of the phrase
    :rtype: str
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum()])
    phrase = QGrams(phrase, qval, start_stop)
    phrase = ''.join(sorted(list(phrase)))
    return phrase


def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone, *args):
    """Return the phonetic fingerprint of a phrase

    A phonetic fingerprint is identical to a standard string fingerprint, as
    implemented in abydos.clustering.fingerprint(), but performs the
    fingerprinting function after converting the string to its phonetic form,
    as determined by some phonetic algorithm.

    :param phrase: the string from which to calculate the phonetic fingerprint
    :param phonetic_algorithm: a phonetic algorithm that takes a string and
        returns a string (presumably a phonetic representation of the original
        string) By default, this function uses
        abydos.phonetic.double_metaphone()
    :param *args: additional arguments to pass to the phonetic algorithm,
        along with the phrase itself
    :returns: the phonetic fingerprint of the phrase
    :rtype: str
    """
    phonetic = ''
    for word in phrase.split():
        word = phonetic_algorithm(word, *args)
        if not isinstance(word, _unicode) and hasattr(word, '__iter__'):
            word = word[0]
        phonetic += word + ' '
    phonetic = phonetic[:-1]
    return fingerprint(phonetic)


def skeleton_key(word):
    """Skeleton key

    The skeleton key of a word is defined in:
    Pollock, Joseph J. and Antonio Zamora. 1984. "Automatic Spelling Correction
    in Scientific and Scholarly Text." Communications of the ACM, 27(4).
    358--368. <http://dl.acm.org/citation.cfm?id=358048>

    :param word: the word to transform into its skeleton key
    :returns: the skeleton key
    :rtype: str
    """
    _vowels = frozenset('AEIOU')

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in
                    frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

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
    """Omission key

    The omission key of a word is defined in:
    Pollock, Joseph J. and Antonio Zamora. 1984. "Automatic Spelling Correction
    in Scientific and Scholarly Text." Communications of the ACM, 27(4).
    358--368. <http://dl.acm.org/citation.cfm?id=358048>

    :param word: the word to transform into its omission key
    :returns: the omission key
    :rtype: str
    """
    _consonants = tuple('JKQXZVWYBFMGPDHCLNTSR')

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in
                    frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

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
                             meanfunc=hmean, symmetric=False):
    """Mean pairwise similarity of a collection of strings

    Takes the mean of the pairwise similarity between each member of a
    collection, optionally in both directions (for asymmetric similarity
    metrics.

    :param collection: a collection of terms or a string that can be split
    :param metric: a similarity metric function
    :param mean: a mean function that takes a list of values and returns a
        float
    :param symmetric: set to True if all pairwise similarities should be
        calculated in both directions
    :returns: the mean pairwise similarity of a collection of strings
    :rtype: str
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

    if not hasattr(meanfunc, '__call__'):
        raise ValueError('meanfunc must be a function')
    return meanfunc(pairwise_values)
