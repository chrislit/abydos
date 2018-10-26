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

"""abydos.fingerprint._basic.

The fingerprint.basic module implements string fingerprints described at
:cite:`OpenRefine:2012`:

    - string fingerprint
    - q-gram fingerprint
    - phonetic fingerprint
"""

from __future__ import unicode_literals

from unicodedata import normalize as unicode_normalize

from six import text_type

from ..phonetic import double_metaphone
from ..tokenizer import QGrams

__all__ = ['phonetic_fingerprint', 'qgram_fingerprint', 'str_fingerprint']


def str_fingerprint(phrase, joiner=' '):
    """Return string fingerprint.

    The fingerprint of a string is a string consisting of all of the unique
    words in a string, alphabetized & concatenated with intervening joiners.
    This fingerprint is described at :cite:`OpenRefine:2012`.

    :param str phrase: the string from which to calculate the fingerprint
    :param str joiner: the string that will be placed between each word
    :returns: the fingerprint of the phrase
    :rtype: str

    >>> str_fingerprint('The quick brown fox jumped over the lazy dog.')
    'brown dog fox jumped lazy over quick the'
    """
    phrase = unicode_normalize('NFKD', text_type(phrase.strip().lower()))
    phrase = ''.join([c for c in phrase if c.isalnum() or c.isspace()])
    phrase = joiner.join(sorted(list(set(phrase.split()))))
    return phrase


def qgram_fingerprint(phrase, qval=2, start_stop='', joiner=''):
    """Return Q-Gram fingerprint.

    A q-gram fingerprint is a string consisting of all of the unique q-grams
    in a string, alphabetized & concatenated. This fingerprint is described at
    :cite:`OpenRefine:2012`.

    :param str phrase: the string from which to calculate the q-gram
        fingerprint
    :param int qval: the length of each q-gram (by default 2)
    :param str start_stop: the start & stop symbol(s) to concatenate on either
        end of the phrase, as defined in abydos.util.qgram()
    :param str joiner: the string that will be placed between each word
    :returns: the q-gram fingerprint of the phrase
    :rtype: str

    >>> qgram_fingerprint('The quick brown fox jumped over the lazy dog.')
    'azbrckdoedeleqerfoheicjukblampnfogovowoxpequrortthuiumvewnxjydzy'
    >>> qgram_fingerprint('Christopher')
    'cherhehrisopphristto'
    >>> qgram_fingerprint('Niall')
    'aliallni'
    """
    phrase = unicode_normalize('NFKD', text_type(phrase.strip().lower()))
    phrase = ''.join(c for c in phrase if c.isalnum())
    phrase = QGrams(phrase, qval, start_stop)
    phrase = joiner.join(sorted(phrase))
    return phrase


def phonetic_fingerprint(
    phrase, phonetic_algorithm=double_metaphone, joiner=' ', *args
):
    """Return the phonetic fingerprint of a phrase.

    A phonetic fingerprint is identical to a standard string fingerprint, as
    implemented in abydos.clustering.fingerprint(), but performs the
    fingerprinting function after converting the string to its phonetic form,
    as determined by some phonetic algorithm. This fingerprint is described at
    :cite:`OpenRefine:2012`.

    :param str phrase: the string from which to calculate the phonetic
        fingerprint
    :param function phonetic_algorithm: a phonetic algorithm that takes a
        string and returns a string (presumably a phonetic representation of
        the original string) By default, this function uses
        abydos.phonetic.double_metaphone()
    :param str joiner: the string that will be placed between each word
    :param args: additional arguments to pass to the phonetic algorithm,
        along with the phrase itself
    :returns: the phonetic fingerprint of the phrase
    :rtype: str

    >>> phonetic_fingerprint('The quick brown fox jumped over the lazy dog.')
    '0 afr fks jmpt kk ls prn tk'
    >>> from abydos.phonetic import soundex
    >>> phonetic_fingerprint('The quick brown fox jumped over the lazy dog.',
    ... phonetic_algorithm=soundex)
    'b650 d200 f200 j513 l200 o160 q200 t000'
    """
    phonetic = ''
    for word in phrase.split():
        word = phonetic_algorithm(word, *args)
        if not isinstance(word, text_type) and hasattr(word, '__iter__'):
            word = word[0]
        phonetic += word + joiner
    phonetic = phonetic[: -len(joiner)]
    return str_fingerprint(phonetic)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
