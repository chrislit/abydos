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
from ._compat import _unicode, _range
from .phonetic import double_metaphone
from .qgram import QGrams
from .distance import sim
from .stats import hmean


def fingerprint(phrase):
    """String fingerprint

    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening spaces

    :param str phrase: the string from which to calculate the fingerprint
    :returns: the fingerprint of the phrase
    :rtype: str

    >>> fingerprint('The quick brown fox jumped over the lazy dog.')
    'brown dog fox jumped lazy over quick the'
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
    phrase = ' '.join(sorted(list(set(phrase.split()))))
    return phrase


def qgram_fingerprint(phrase, qval=2, start_stop=''):
    """Q-Gram fingerprint

    A q-gram fingerprint is a string consisting of all of the unique q-grams
    in a string, alphabetized & concatenated.

    :param str phrase: the string from which to calculate the q-gram
        fingerprint
    :param int qval: the length of each q-gram (by default 2)
    :param str start_stop: the start & stop symbol(s) to concatenate on either
        end of the phrase, as defined in abydos.util.qgram()
    :returns: the q-gram fingerprint of the phrase
    :rtype: str

    >>> qgram_fingerprint('The quick brown fox jumped over the lazy dog.')
    'azbrckdoedeleqerfoheicjukblampnfogovowoxpequrortthuiumvewnxjydzy'
    >>> qgram_fingerprint('Christopher')
    'cherhehrisopphristto'
    >>> qgram_fingerprint('Niall')
    'aliallni'
    """
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join(c for c in phrase if c.isalnum())
    phrase = QGrams(phrase, qval, start_stop)
    phrase = ''.join(sorted(phrase))
    return phrase


def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone, *args):
    """Return the phonetic fingerprint of a phrase

    A phonetic fingerprint is identical to a standard string fingerprint, as
    implemented in abydos.clustering.fingerprint(), but performs the
    fingerprinting function after converting the string to its phonetic form,
    as determined by some phonetic algorithm.

    :param str phrase: the string from which to calculate the phonetic
        fingerprint
    :param function phonetic_algorithm: a phonetic algorithm that takes a
        string and returns a string (presumably a phonetic representation of
        the original string) By default, this function uses
        abydos.phonetic.double_metaphone()
    :param args: additional arguments to pass to the phonetic algorithm,
        along with the phrase itself
    :returns: the phonetic fingerprint of the phrase
    :rtype: str

    >>> phonetic_fingerprint('The quick brown fox jumped over the lazy dog.')
    '0 afr fks jmpt kk ls prn tk'
    >>> phonetic_fingerprint('The quick brown fox jumped over the lazy dog.',
    ... phonetic_algorithm=soundex)
    'b650 d200 f200 j513 l200 o160 q200 t000'
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

    :param str word: the word to transform into its skeleton key
    :returns: the skeleton key
    :rtype: str

    >>> skeleton_key('The quick brown fox jumped over the lazy dog.')
    'THQCKBRWNFXJMPDVLZYGEUIOA'
    >>> skeleton_key('Christopher')
    'CHRSTPIOE'
    >>> skeleton_key('Niall')
    'NLIA'
    """
    _vowels = frozenset('AEIOU')

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join(c for c in word if c in
                   frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

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

    :param str word: the word to transform into its omission key
    :returns: the omission key
    :rtype: str

    >>> omission_key('The quick brown fox jumped over the lazy dog.')
    'JKQXZVWYBFMGPDHCLNTREUIOA'
    >>> omission_key('Christopher')
    'PHCTSRIOE'
    >>> omission_key('Niall')
    'LNIA'
    """
    _consonants = tuple('JKQXZVWYBFMGPDHCLNTSR')

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join(c for c in word if c in
                   frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

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

    :param list collection: a collection of terms or a string that can be split
    :param function metric: a similarity metric function
    :param function mean: a mean function that takes a list of values and
        returns a float
    :param bool symmetric: set to True if all pairwise similarities should be
        calculated in both directions
    :returns: the mean pairwise similarity of a collection of strings
    :rtype: str

    >>> mean_pairwise_similarity(['Christopher', 'Kristof', 'Christobal'])
    0.51980198019801982
    >>> mean_pairwise_similarity(['Niall', 'Neal', 'Neil'])
    0.54545454545454541
    """
    if hasattr(collection, 'split'):
        collection = collection.split()
    if not hasattr(collection, '__iter__'):
        raise ValueError('collection is neither a string nor iterable type')
    elif len(collection) < 2:
        raise ValueError('collection has fewer than two members')

    collection = list(collection)

    pairwise_values = []

    for i in _range(len(collection)):
        for j in _range(i+1, len(collection)):
            pairwise_values.append(metric(collection[i], collection[j]))
            if symmetric:
                pairwise_values.append(metric(collection[j], collection[i]))

    if not hasattr(meanfunc, '__call__'):
        raise ValueError('meanfunc must be a function')
    return meanfunc(pairwise_values)
