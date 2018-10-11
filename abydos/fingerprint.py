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

"""abydos.fingerprint.

The fingerprint module implements string fingerprints such as:
    - string fingerprint
    - q-gram fingerprint
    - phonetic fingerprint
    - Pollock & Zomora's skeleton key
    - Pollock & Zomora's omission key
    - Cisłak & Grabowski's occurrence fingerprint
    - Cisłak & Grabowski's occurrence halved fingerprint
    - Cisłak & Grabowski's count fingerprint
    - Cisłak & Grabowski's position fingerprint
    - Synoname Toolcode
"""

from __future__ import division, unicode_literals

from collections import Counter
from unicodedata import normalize as unicode_normalize

from six import text_type

from .phonetic import double_metaphone
from .qgram import QGrams

__all__ = ['MOST_COMMON_LETTERS', 'MOST_COMMON_LETTERS_CG',
           'MOST_COMMON_LETTERS_DE', 'MOST_COMMON_LETTERS_DE_LC',
           'MOST_COMMON_LETTERS_EN_LC', 'count_fingerprint',
           'occurrence_fingerprint', 'occurrence_halved_fingerprint',
           'omission_key', 'phonetic_fingerprint', 'position_fingerprint',
           'qgram_fingerprint', 'skeleton_key', 'str_fingerprint',
           'synoname_toolcode']


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


def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone,
                         joiner=' ', *args):
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
    phonetic = phonetic[:-len(joiner)]
    return str_fingerprint(phonetic)


def skeleton_key(word):
    """Return the skeleton key.

    The skeleton key of a word is defined in :cite:`Pollock:1984`.

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
    _vowels = {'A', 'E', 'I', 'O', 'U'}

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})
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
    """Return the omission key.

    The omission key of a word is defined in :cite:`Pollock:1984`.

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
    _consonants = ('J', 'K', 'Q', 'X', 'Z', 'V', 'W', 'Y', 'B', 'F', 'M', 'G',
                   'P', 'D', 'H', 'C', 'L', 'N', 'T', 'S', 'R')

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

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


# most common letters, as defined in Cisłak & Grabowski
MOST_COMMON_LETTERS_CG = ('e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd',
                          'l', 'c', 'u', 'm', 'w', 'f')

# most common letters (case-folded to lowercase), as shown in Google Books
# English n-grams, among letters a-z & digits 0-9
MOST_COMMON_LETTERS_EN_LC = ('e', 't', 'a', 'i', 'o', 'n', 's', 'r', 'h', 'l',
                             'd', 'c', 'u', 'm', 'f', 'p', 'g', 'y', 'w', 'b',
                             'v', 'k', 'x', 'j', 'q', 'z', '1', '2', '0', '9',
                             '3', '4', '8', '5', '6', '7')

# most common letters, as shown in Google Books English n-grams, among letters
# A-Z, a-z & digits 0-9
MOST_COMMON_LETTERS = ('e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd',
                       'c', 'u', 'm', 'f', 'p', 'g', 'y', 'w', 'b', 'v', 'k',
                       'T', 'I', 'A', 'S', 'C', 'x', 'M', 'P', 'E', 'B', 'H',
                       'R', 'N', 'D', 'L', 'F', 'W', 'O', 'q', 'G', 'z', 'j',
                       'J', 'U', 'V', 'K', 'Y', '1', '2', '0', 'X', '9', 'Q',
                       '3', 'Z', '4', '8', '5', '6', '7',)

# most common letters (case-folded to lowercase), as shown in Google Books
# German n-grams, among letters (a-z and umlauted vowels & eszett) & digits 0-9
MOST_COMMON_LETTERS_DE = ('e', 'n', 'i', 'r', 's', 't', 'a', 'd', 'h', 'u',
                          'l', 'g', 'c', 'o', 'm', 'b', 'f', 'w', 'k', 'z',
                          'v', 'p', 'ü', 'ä', 'ß', 'ö', 'j', 'y', 'x', 'q',
                          '1', '2', '3', '4', '0', '5', '6', '9', '8', '7')

# most common letters (case-folded to lowercase), as shown in Google Books
# German n-grams, among letters (A-Z, a-z, umlauted vowels & eszett) & digits
# 0-9
MOST_COMMON_LETTERS_DE_LC = ('e', 'n', 'i', 'r', 's', 't', 'a', 'd', 'h', 'u',
                             'l', 'c', 'g', 'o', 'm', 'b', 'f', 'w', 'k', 'z',
                             'v', 'p', 'ü', 'ä', 'S', 'A', 'D', 'B', 'E', 'G',
                             'M', 'ß', 'V', 'K', 'ö', 'W', 'F', 'P', 'R', 'I',
                             'H', 'L', 'T', 'N', 'Z', 'y', 'U', 'j', 'J', 'O',
                             'C', 'x', 'q', 'Ü', 'Q', 'X', 'Ä', 'Ö', '1', '2',
                             'Y', '3', '4', '0', '5', '6', '9', '8', '7')


def occurrence_fingerprint(word, n_bits=16,
                           most_common=MOST_COMMON_LETTERS_CG):
    """Return the occurrence fingerprint.

    Based on the occurrence fingerprint from :cite:`Cislak:2017`.

    :param str word: the word to fingerprint
    :param int n_bits: number of bits in the fingerprint returned
    :param list most_common: the most common tokens in the target language,
        ordered by frequency
    :returns: the occurrence fingerprint
    :rtype: int

    >>> bin(occurrence_fingerprint('hat'))
    '0b110000100000000'
    >>> bin(occurrence_fingerprint('niall'))
    '0b10110000100000'
    >>> bin(occurrence_fingerprint('colin'))
    '0b1110000110000'
    >>> bin(occurrence_fingerprint('atcg'))
    '0b110000000010000'
    >>> bin(occurrence_fingerprint('entreatment'))
    '0b1110010010000100'
    """
    word = set(word)
    fingerprint = 0

    for letter in most_common:
        if letter in word:
            fingerprint += 1
        n_bits -= 1
        if n_bits:
            fingerprint <<= 1
        else:
            break

    n_bits -= 1
    if n_bits > 0:
        fingerprint <<= n_bits

    return fingerprint


def occurrence_halved_fingerprint(word, n_bits=16,
                                  most_common=MOST_COMMON_LETTERS_CG):
    """Return the occurrence halved fingerprint.

    Based on the occurrence halved fingerprint from :cite:`Cislak:2017`.

    :param str word: the word to fingerprint
    :param int n_bits: number of bits in the fingerprint returned
    :param list most_common: the most common tokens in the target language,
        ordered by frequency
    :returns: the occurrence halved fingerprint
    :rtype: int

    >>> bin(occurrence_halved_fingerprint('hat'))
    '0b1010000000010'
    >>> bin(occurrence_halved_fingerprint('niall'))
    '0b10010100000'
    >>> bin(occurrence_halved_fingerprint('colin'))
    '0b1001010000'
    >>> bin(occurrence_halved_fingerprint('atcg'))
    '0b10100000000000'
    >>> bin(occurrence_halved_fingerprint('entreatment'))
    '0b1111010000110000'
    """
    if n_bits % 2:
        n_bits += 1

    w_len = len(word)//2
    w_1 = set(word[:w_len])
    w_2 = set(word[w_len:])
    fingerprint = 0

    for letter in most_common:
        if n_bits:
            fingerprint <<= 1
            if letter in w_1:
                fingerprint += 1
            fingerprint <<= 1
            if letter in w_2:
                fingerprint += 1
            n_bits -= 2
        else:
            break

    if n_bits > 0:
        fingerprint <<= n_bits

    return fingerprint


def count_fingerprint(word, n_bits=16,
                      most_common=MOST_COMMON_LETTERS_CG):
    """Return the count fingerprint.

    Based on the count fingerprint from :cite:`Cislak:2017`.

    :param str word: the word to fingerprint
    :param int n_bits: number of bits in the fingerprint returned
    :param list most_common: the most common tokens in the target language,
        ordered by frequency
    :returns: the count fingerprint
    :rtype: int

    >>> bin(count_fingerprint('hat'))
    '0b1010000000001'
    >>> bin(count_fingerprint('niall'))
    '0b10001010000'
    >>> bin(count_fingerprint('colin'))
    '0b101010000'
    >>> bin(count_fingerprint('atcg'))
    '0b1010000000000'
    >>> bin(count_fingerprint('entreatment'))
    '0b1111010000100000'
    """
    if n_bits % 2:
        n_bits += 1

    word = Counter(word)
    fingerprint = 0

    for letter in most_common:
        if n_bits:
            fingerprint <<= 2
            fingerprint += (word[letter] & 3)
            n_bits -= 2
        else:
            break

    if n_bits:
        fingerprint <<= n_bits

    return fingerprint


def position_fingerprint(word, n_bits=16,
                         most_common=MOST_COMMON_LETTERS_CG,
                         bits_per_letter=3):
    """Return the position fingerprint.

    Based on the position fingerprint from :cite:`Cislak:2017`.

    :param str word: the word to fingerprint
    :param int n_bits: number of bits in the fingerprint returned
    :param list most_common: the most common tokens in the target language,
        ordered by frequency
    :param int bits_per_letter: the bits to assign for letter position
    :returns: the position fingerprint
    :rtype: int

    >>> bin(position_fingerprint('hat'))
    '0b1110100011111111'
    >>> bin(position_fingerprint('niall'))
    '0b1111110101110010'
    >>> bin(position_fingerprint('colin'))
    '0b1111111110010111'
    >>> bin(position_fingerprint('atcg'))
    '0b1110010001111111'
    >>> bin(position_fingerprint('entreatment'))
    '0b101011111111'
    """
    position = {}
    for pos, letter in enumerate(word):
        if letter not in position and letter in most_common:
            position[letter] = min(pos, 2**bits_per_letter-1)

    fingerprint = 0

    for letter in most_common:
        if n_bits:
            fingerprint <<= min(bits_per_letter, n_bits)
            if letter in position:
                fingerprint += min(position[letter], 2**n_bits-1)
            else:
                fingerprint += min(2**bits_per_letter-1, 2**n_bits-1)
            n_bits -= min(bits_per_letter, n_bits)
        else:
            break

    for _ in range(n_bits):
        fingerprint <<= 1
        fingerprint += 1

    return fingerprint


_synoname_special_table = (
    # Roman, match, extra, method
    (False, 'NONE', '', 0),
    (False, 'aine', '', 3),
    (False, 'also erroneously', '', 4),
    (False, 'also identified with the', '', 2),
    (False, 'also identified with', '', 2),
    (False, 'archbishop', '', 7),
    (False, 'atelier', '', 7),
    (False, 'baron', '', 7),
    (False, 'cadet', '', 3),
    (False, 'cardinal', '', 7),
    (False, 'circle of', '', 5),
    (False, 'circle', '', 5),
    (False, 'class of', '', 5),
    (False, 'conde de', '', 7),
    (False, 'countess', '', 7),
    (False, 'count', '', 7),
    (False, "d'", " d'", 15),
    (False, 'dai', '', 15),
    (False, "dall'", " dall'", 15),
    (False, 'dalla', '', 15),
    (False, 'dalle', '', 15),
    (False, 'dal', '', 15),
    (False, 'da', '', 15),
    (False, 'degli', '', 15),
    (False, 'della', '', 15),
    (False, 'del', '', 15),
    (False, 'den', '', 15),
    (False, 'der altere', '', 3),
    (False, 'der jungere', '', 3),
    (False, 'der', '', 15),
    (False, 'de la', '', 15),
    (False, 'des', '', 15),
    (False, "de'", " de'", 15),
    (False, 'de', '', 15),
    (False, 'di ser', '', 7),
    (False, 'di', '', 15),
    (False, 'dos', '', 15),
    (False, 'du', '', 15),
    (False, 'duke of', '', 7),
    (False, 'earl of', '', 7),
    (False, 'el', '', 15),
    (False, 'fils', '', 3),
    (False, 'florentine follower of', '', 5),
    (False, 'follower of', '', 5),
    (False, 'fra', '', 7),
    (False, 'freiherr von', '', 7),
    (False, 'giovane', '', 7),
    (False, 'group', '', 5),
    (True, 'iii', '', 3),
    (True, 'ii', '', 3),
    (False, 'il giovane', '', 7),
    (False, 'il vecchio', '', 7),
    (False, 'il', '', 15),
    (False, "in't", '', 7),
    (False, 'in het', '', 7),
    (True, 'iv', '', 3),
    (True, 'ix', '', 3),
    (True, 'i', '', 3),
    (False, 'jr.', '', 3),
    (False, 'jr', '', 3),
    (False, 'juniore', '', 3),
    (False, 'junior', '', 3),
    (False, 'king of', '', 7),
    (False, "l'", " l'", 15),
    (False, "l'aine", '', 3),
    (False, 'la', '', 15),
    (False, 'le jeune', '', 3),
    (False, 'le', '', 15),
    (False, 'lo', '', 15),
    (False, 'maestro', '', 7),
    (False, 'maitre', '', 7),
    (False, 'marchioness', '', 7),
    (False, 'markgrafin von', '', 7),
    (False, 'marquess', '', 7),
    (False, 'marquis', '', 7),
    (False, 'master of the', '', 7),
    (False, 'master of', '', 7),
    (False, 'master known as the', '', 7),
    (False, 'master with the', '', 7),
    (False, 'master with', '', 7),
    (False, 'masters', '', 7),
    (False, 'master', '', 7),
    (False, 'meister', '', 7),
    (False, 'met de', '', 7),
    (False, 'met', '', 7),
    (False, 'mlle.', '', 7),
    (False, 'mlle', '', 7),
    (False, 'monogrammist', '', 7),
    (False, 'monsu', '', 7),
    (False, 'nee', '', 2),
    (False, 'of', '', 3),
    (False, 'oncle', '', 3),
    (False, 'op den', '', 15),
    (False, 'op de', '', 15),
    (False, 'or', '', 2),
    (False, 'over den', '', 15),
    (False, 'over de', '', 15),
    (False, 'over', '', 7),
    (False, 'p.re', '', 7),
    (False, 'p.r.a.', '', 1),
    (False, 'padre', '', 7),
    (False, 'painter', '', 7),
    (False, 'pere', '', 3),
    (False, 'possibly identified with', '', 6),
    (False, 'possibly', '', 6),
    (False, 'pseudo', '', 15),
    (False, 'r.a.', '', 1),
    (False, 'reichsgraf von', '', 7),
    (False, 'ritter von', '', 7),
    (False, 'sainte-', ' sainte-', 8),
    (False, 'sainte', '', 7),
    (False, 'saint-', ' saint-', 8),
    (False, 'saint', '', 7),
    (False, 'santa', '', 15),
    (False, "sant'", " sant'", 15),
    (False, 'san', '', 15),
    (False, 'ser', '', 7),
    (False, 'seniore', '', 3),
    (False, 'senior', '', 3),
    (False, 'sir', '', 5),
    (False, 'sr.', '', 3),
    (False, 'sr', '', 3),
    (False, 'ss.', ' ss.', 14),
    (False, 'ss', '', 6),
    (False, 'st-', ' st-', 8),
    (False, 'st.', ' st.', 15),
    (False, 'ste-', ' ste-', 8),
    (False, 'ste.', ' ste.', 15),
    (False, 'studio', '', 7),
    (False, 'sub-group', '', 5),
    (False, 'sultan of', '', 7),
    (False, 'ten', '', 15),
    (False, 'ter', '', 15),
    (False, 'the elder', '', 3),
    (False, 'the younger', '', 3),
    (False, 'the', '', 7),
    (False, 'tot', '', 15),
    (False, 'unidentified', '', 1),
    (False, 'van den', '', 15),
    (False, 'van der', '', 15),
    (False, 'van de', '', 15),
    (False, 'vanden', '', 15),
    (False, 'vander', '', 15),
    (False, 'van', '', 15),
    (False, 'vecchia', '', 7),
    (False, 'vecchio', '', 7),
    (True, 'viii', '', 3),
    (True, 'vii', '', 3),
    (True, 'vi', '', 3),
    (True, 'v', '', 3),
    (False, 'vom', '', 7),
    (False, 'von', '', 15),
    (False, 'workshop', '', 7),
    (True, 'xiii', '', 3),
    (True, 'xii', '', 3),
    (True, 'xiv', '', 3),
    (True, 'xix', '', 3),
    (True, 'xi', '', 3),
    (True, 'xviii', '', 3),
    (True, 'xvii', '', 3),
    (True, 'xvi', '', 3),
    (True, 'xv', '', 3),
    (True, 'xx', '', 3),
    (True, 'x', '', 3),
    (False, 'y', '', 7)
)


def synoname_toolcode(lname, fname='', qual='', normalize=0):
    """Build the Synoname toolcode.

    Cf. :cite:`Getty:1991,Gross:1991`.

    :param str lname: last name
    :param str fname: first name (can be blank)
    :param str qual: qualifier
    :param int normalize: normalization mode (0, 1, or 2)
    :returns: the transformed last and first names and the synoname toolcode
    :rtype: tuple

    >>> synoname_toolcode('hat')
    ('hat', '', '0000000003$$h')
    >>> synoname_toolcode('niall')
    ('niall', '', '0000000005$$n')
    >>> synoname_toolcode('colin')
    ('colin', '', '0000000005$$c')
    >>> synoname_toolcode('atcg')
    ('atcg', '', '0000000004$$a')
    >>> synoname_toolcode('entreatment')
    ('entreatment', '', '0000000011$$e')

    >>> synoname_toolcode('Ste.-Marie', 'Count John II', normalize=2)
    ('ste.-marie ii', 'count john', '0200491310$015b049a127c$smcji')
    >>> synoname_toolcode('Michelangelo IV', '', 'Workshop of')
    ('michelangelo iv', '', '3000550015$055b$mi')
    """
    method_dict = {'end': 1, 'middle': 2, 'beginning': 4,
                             'beginning_no_space': 8}

    lname = lname.lower()
    fname = fname.lower()
    qual = qual.lower()

    # Start with the basic code
    toolcode = ['0', '0', '0', '000', '00', '00', '$', '', '$', '']

    full_name = ' '.join((lname, fname))

    # Fill field 0 (qualifier)
    qual_3 = {'adaptation after', 'after', 'assistant of', 'assistants of',
              'circle of', 'follower of', 'imitator of', 'in the style of',
              'manner of', 'pupil of', 'school of', 'studio of',
              'style of', 'workshop of'}
    qual_2 = {'copy after', 'copy after?', 'copy of'}
    qual_1 = {'ascribed to', 'attributed to or copy after',
              'attributed to', 'possibly'}

    if qual in qual_3:
        toolcode[0] = '3'
    elif qual in qual_2:
        toolcode[0] = '2'
    elif qual in qual_1:
        toolcode[0] = '1'

    # Fill field 1 (punctuation)
    if '.' in full_name:
        toolcode[1] = '2'
    else:
        for punct in ',-/:;"&\'()!{|}?$%*+<=>[\\]^_`~':
            if punct in full_name:
                toolcode[1] = '1'
                break

    # Fill field 2 (generation)
    gen_1 = ('the elder', ' sr.', ' sr', 'senior', 'der altere', 'il vecchio',
             "l'aine", 'p.re', 'padre', 'seniore', 'vecchia', 'vecchio')
    gen_2 = (' jr.', ' jr', 'der jungere', 'il giovane', 'giovane', 'juniore',
             'junior', 'le jeune', 'the younger')

    elderyounger = ''  # save elder/younger for possible movement later
    for gen in gen_1:
        if gen in full_name:
            toolcode[2] = '1'
            elderyounger = gen
            break
    else:
        for gen in gen_2:
            if gen in full_name:
                toolcode[2] = '2'
                elderyounger = gen
                break

    # do comma flip
    if normalize:
        comma = lname.find(',')
        if comma != -1:
            lname_end = lname[comma + 1:]
            while lname_end[0] in {' ', ','}:
                lname_end = lname_end[1:]
            fname = lname_end + ' ' + fname
            lname = lname[:comma].strip()

    # do elder/younger move
    if normalize == 2 and elderyounger:
        elderyounger_loc = fname.find(elderyounger)
        if elderyounger_loc != -1:
            lname = ' '.join((lname, elderyounger.strip()))
            fname = ' '.join((fname[:elderyounger_loc].strip(),
                              fname[elderyounger_loc +
                                    len(elderyounger):])).strip()

    toolcode[4] = '{:02d}'.format(len(fname))
    toolcode[5] = '{:02d}'.format(len(lname))

    # strip punctuation
    for char in ',/:;"&()!{|}?$%*+<=>[\\]^_`~':
        full_name = full_name.replace(char, '')
    for pos, char in enumerate(full_name):
        if char == '-' and full_name[pos - 1:pos + 2] != 'b-g':
            full_name = full_name[:pos] + ' ' + full_name[pos + 1:]

    # Fill field 9 (search range)
    for letter in [_[0] for _ in full_name.split()]:
        if letter not in toolcode[9]:
            toolcode[9] += letter
        if len(toolcode[9]) == 15:
            break

    def roman_check(numeral, fname, lname):
        """Move Roman numerals from first name to last."""
        loc = fname.find(numeral)
        if fname and (loc != -1 and
                      (len(fname[loc:]) == len(numeral)) or
                      fname[loc+len(numeral)] in {' ', ','}):
            lname = ' '.join((lname, numeral))
            fname = ' '.join((fname[:loc].strip(),
                              fname[loc + len(numeral):].lstrip(' ,')))
        return fname.strip(), lname.strip()

    # Fill fields 7 (specials) and 3 (roman numerals)
    for num, special in enumerate(_synoname_special_table):
        roman, match, extra, method = special
        if method & method_dict['end']:
            match_context = ' ' + match
            loc = full_name.find(match_context)
            if ((len(full_name) > len(match_context)) and
                    (loc == len(full_name) - len(match_context))):
                if roman:
                    if not any(abbr in fname for abbr in ('i.', 'v.', 'x.')):
                        full_name = full_name[:loc]
                        toolcode[7] += '{:03d}'.format(num) + 'a'
                        if toolcode[3] == '000':
                            toolcode[3] = '{:03d}'.format(num)
                        if normalize == 2:
                            fname, lname = roman_check(match, fname, lname)
                else:
                    full_name = full_name[:loc]
                    toolcode[7] += '{:03d}'.format(num) + 'a'
        if method & method_dict['middle']:
            match_context = ' ' + match + ' '
            loc = 0
            while loc != -1:
                loc = full_name.find(match_context, loc+1)
                if loc > 0:
                    if roman:
                        if not any(abbr in fname for abbr in
                                   ('i.', 'v.', 'x.')):
                            full_name = (full_name[:loc] +
                                         full_name[loc + len(match) + 1:])
                            toolcode[7] += '{:03d}'.format(num) + 'b'
                            if toolcode[3] == '000':
                                toolcode[3] = '{:03d}'.format(num)
                            if normalize == 2:
                                fname, lname = roman_check(match, fname, lname)
                    else:
                        full_name = (full_name[:loc] +
                                     full_name[loc + len(match) + 1:])
                        toolcode[7] += '{:03d}'.format(num) + 'b'
        if method & method_dict['beginning']:
            match_context = match + ' '
            loc = full_name.find(match_context)
            if loc == 0:
                full_name = full_name[len(match) + 1:]
                toolcode[7] += '{:03d}'.format(num) + 'c'
        if method & method_dict['beginning_no_space']:
            loc = full_name.find(match)
            if loc == 0:
                toolcode[7] += '{:03d}'.format(num) + 'd'
                if full_name[:len(match)] not in toolcode[9]:
                    toolcode[9] += full_name[:len(match)]

        if extra:
            loc = full_name.find(extra)
            if loc != -1:
                toolcode[7] += '{:03d}'.format(num) + 'X'
                # Since extras are unique, we only look for each of them
                # once, and they include otherwise impossible characters for
                # this field, it's not possible for the following line to have
                # ever been false.
                # if full_name[loc:loc+len(extra)] not in toolcode[9]:
                toolcode[9] += full_name[loc:loc+len(match)]

    return lname, fname, ''.join(toolcode)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
