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

"""abydos.phonetic.

The phonetic module implements phonetic algorithms including:

    - Robert C. Russell's Index
    - American Soundex
    - Refined Soundex
    - Daitch-Mokotoff Soundex
    - Kölner Phonetik
    - NYSIIS
    - Match Rating Algorithm
    - Metaphone
    - Double Metaphone
    - Caverphone
    - Alpha Search Inquiry System
    - Fuzzy Soundex
    - Phonex
    - Phonem
    - Phonix
    - SfinxBis
    - phonet
    - Standardized Phonetic Frequency Code
    - Statistics Canada
    - Lein
    - Roger Root
    - Oxford Name Compression Algorithm (ONCA)
    - Eudex phonetic hash
    - Haase Phonetik
    - Reth-Schek Phonetik
    - FONEM
    - Parmar-Kumbharana
    - Davidson's Consonant Code
    - SoundD
    - PSHP Soundex/Viewex Coding
    - an early version of Henry Code
    - Norphone
    - Dolby Code
    - Phonetic Spanish
    - Spanish Metaphone
    - MetaSoundex
    - SoundexBR
    - NRL English-to-phoneme
    - Beider-Morse Phonetic Matching
"""

from __future__ import division, unicode_literals

from collections import Counter
from itertools import groupby, product
from re import compile as re_compile
from re import match as re_match
from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

from ._bm import _bmpm

__all__ = ['alpha_sis', 'bmpm', 'caverphone', 'davidson', 'dm_soundex',
           'dolby', 'double_metaphone', 'eudex', 'fonem', 'fuzzy_soundex',
           'haase_phonetik', 'henry_early', 'koelner_phonetik',
           'koelner_phonetik_alpha', 'koelner_phonetik_num_to_alpha', 'lein',
           'metaphone', 'metasoundex', 'mra', 'norphone', 'nrl', 'nysiis',
           'onca', 'parmar_kumbharana', 'phonem', 'phonet', 'phonetic_spanish',
           'phonex', 'phonix', 'pshp_soundex_first', 'pshp_soundex_last',
           'refined_soundex', 'reth_schek_phonetik', 'roger_root',
           'russell_index', 'russell_index_alpha',
           'russell_index_num_to_alpha', 'sfinxbis', 'sound_d', 'soundex',
           'soundex_br', 'spanish_metaphone', 'spfc', 'statistics_canada']


def _delete_consecutive_repeats(word):
    """Delete consecutive repeated characters in a word.

    :param str word: the word to transform
    :returns: word with consecutive repeating characters collapsed to
        a single instance
    :rtype: str

    >>> _delete_consecutive_repeats('REDDEE')
    'REDE'
    >>> _delete_consecutive_repeats('AEIOU')
    'AEIOU'
    >>> _delete_consecutive_repeats('AAACCCTTTGGG')
    'ACTG'
    """
    return ''.join(char for char, _ in groupby(word))


def russell_index(word):
    """Return the Russell Index (integer output) of a word.

    This follows Robert C. Russell's Index algorithm, as described in
    :cite:`Russell:1917`.

    :param str word: the word to transform
    :returns: the Russell Index value
    :rtype: int

    >>> russell_index('Christopher')
    3813428
    >>> russell_index('Niall')
    715
    >>> russell_index('Smith')
    3614
    >>> russell_index('Schmidt')
    3614
    """
    _russell_translation = dict(zip((ord(_) for _ in
                                     'ABCDEFGIKLMNOPQRSTUVXYZ'),
                                    '12341231356712383412313'))

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = word.replace('GH', '')  # discard gh (rule 3)
    word = word.rstrip('SZ')  # discard /[sz]$/ (rule 3)

    # translate according to Russell's mapping
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z'})
    sdx = word.translate(_russell_translation)

    # remove any 1s after the first occurrence
    one = sdx.find('1')+1
    if one:
        sdx = sdx[:one] + ''.join(c for c in sdx[one:] if c != '1')

    # remove repeating characters
    sdx = _delete_consecutive_repeats(sdx)

    # return as an int
    return int(sdx) if sdx else float('NaN')


def russell_index_num_to_alpha(num):
    """Convert the Russell Index integer to an alphabetic string.

    This follows Robert C. Russell's Index algorithm, as described in
    :cite:`Russell:1917`.

    :param int num: a Russell Index integer value
    :returns: the Russell Index as an alphabetic string
    :rtype: str

    >>> russell_index_num_to_alpha(3813428)
    'CRACDBR'
    >>> russell_index_num_to_alpha(715)
    'NAL'
    >>> russell_index_num_to_alpha(3614)
    'CMAD'
    """
    _russell_num_translation = dict(zip((ord(_) for _ in '12345678'),
                                        'ABCDLMNR'))
    num = ''.join(c for c in text_type(num) if c in {'1', '2', '3', '4', '5',
                                                     '6', '7', '8'})
    if num:
        return num.translate(_russell_num_translation)
    return ''


def russell_index_alpha(word):
    """Return the Russell Index (alphabetic output) for the word.

    This follows Robert C. Russell's Index algorithm, as described in
    :cite:`Russell:1917`.

    :param str word: the word to transform
    :returns: the Russell Index value as an alphabetic string
    :rtype: str

    >>> russell_index_alpha('Christopher')
    'CRACDBR'
    >>> russell_index_alpha('Niall')
    'NAL'
    >>> russell_index_alpha('Smith')
    'CMAD'
    >>> russell_index_alpha('Schmidt')
    'CMAD'
    """
    if word:
        return russell_index_num_to_alpha(russell_index(word))
    return ''


def soundex(word, max_length=4, var='American', reverse=False, zero_pad=True):
    """Return the Soundex code for a word.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param str var: the variant of the algorithm to employ (defaults to
        'American'):

        - 'American' follows the American Soundex algorithm, as described at
          :cite:`US:2007` and in :cite:`Knuth:1998`; this is also called
          Miracode
        - 'special' follows the rules from the 1880-1910 US Census
          retrospective re-analysis, in which h & w are not treated as blocking
          consonants but as vowels. Cf. :cite:`Repici:2013`.
        - 'Census' follows the rules laid out in GIL 55 :cite:`US:1997` by the
          US Census, including coding prefixed and unprefixed versions of some
          names

    :param bool reverse: reverse the word before computing the selected Soundex
        (defaults to False); This results in "Reverse Soundex", which is useful
        for blocking in cases where the initial elements may be in error.
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the Soundex value
    :rtype: str

    >>> soundex("Christopher")
    'C623'
    >>> soundex("Niall")
    'N400'
    >>> soundex('Smith')
    'S530'
    >>> soundex('Schmidt')
    'S530'

    >>> soundex('Christopher', max_length=-1)
    'C623160000000000000000000000000000000000000000000000000000000000'
    >>> soundex('Christopher', max_length=-1, zero_pad=False)
    'C62316'

    >>> soundex('Christopher', reverse=True)
    'R132'

    >>> soundex('Ashcroft')
    'A261'
    >>> soundex('Asicroft')
    'A226'
    >>> soundex('Ashcroft', var='special')
    'A226'
    >>> soundex('Asicroft', var='special')
    'A226'
    """
    _soundex_translation = dict(zip((ord(_) for _ in
                                     'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                    '01230129022455012623019202'))

    # Require a max_length of at least 4 and not more than 64
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')

    if var == 'Census':
        # TODO: Should these prefixes be supplemented? (VANDE, DELA, VON)
        if word[:3] in {'VAN', 'CON'} and len(word) > 4:
            return (soundex(word, max_length, 'American', reverse, zero_pad),
                    soundex(word[3:], max_length, 'American', reverse,
                            zero_pad))
        if word[:2] in {'DE', 'DI', 'LA', 'LE'} and len(word) > 3:
            return (soundex(word, max_length, 'American', reverse, zero_pad),
                    soundex(word[2:], max_length, 'American', reverse,
                            zero_pad))
        # Otherwise, proceed as usual (var='American' mode, ostensibly)

    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    # Nothing to convert, return base case
    if not word:
        if zero_pad:
            return '0'*max_length
        return '0'

    # Reverse word if computing Reverse Soundex
    if reverse:
        word = word[::-1]

    # apply the Soundex algorithm
    sdx = word.translate(_soundex_translation)

    if var == 'special':
        sdx = sdx.replace('9', '0')  # special rule for 1880-1910 census
    else:
        sdx = sdx.replace('9', '')  # rule 1
    sdx = _delete_consecutive_repeats(sdx)  # rule 3

    if word[0] in 'HW':
        sdx = word[0] + sdx
    else:
        sdx = word[0] + sdx[1:]
    sdx = sdx.replace('0', '')  # rule 1

    if zero_pad:
        sdx += ('0'*max_length)  # rule 4

    return sdx[:max_length]


def refined_soundex(word, max_length=-1, zero_pad=False,
                    retain_vowels=False):
    """Return the Refined Soundex code for a word.

    This is Soundex, but with more character classes. It was defined at
    :cite:`Boyce:1998`.

    :param word: the word to transform
    :param max_length: the length of the code returned (defaults to unlimited)
    :param zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :param retain_vowels: retain vowels (as 0) in the resulting code
    :returns: the Refined Soundex value
    :rtype: str

    >>> refined_soundex('Christopher')
    'C393619'
    >>> refined_soundex('Niall')
    'N87'
    >>> refined_soundex('Smith')
    'S386'
    >>> refined_soundex('Schmidt')
    'S386'
    """
    _ref_soundex_translation = dict(zip((ord(_) for _ in
                                         'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                        '01360240043788015936020505'))

    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    # apply the Soundex algorithm
    sdx = word[:1] + word.translate(_ref_soundex_translation)
    sdx = _delete_consecutive_repeats(sdx)
    if not retain_vowels:
        sdx = sdx.replace('0', '')  # Delete vowels, H, W, Y

    if max_length > 0:
        if zero_pad:
            sdx += ('0' * max_length)
        sdx = sdx[:max_length]

    return sdx


def dm_soundex(word, max_length=6, zero_pad=True):
    """Return the Daitch-Mokotoff Soundex code for a word.

    Based on Daitch-Mokotoff Soundex :cite:`Mokotoff:1997`, this returns values
    of a word as a set. A collection is necessary since there can be multiple
    values for a single word.

    :param word: the word to transform
    :param max_length: the length of the code returned (defaults to 6; must be
        between 6 and 64)
    :param zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the Daitch-Mokotoff Soundex value
    :rtype: str

    >>> sorted(dm_soundex('Christopher'))
    ['494379', '594379']
    >>> dm_soundex('Niall')
    {'680000'}
    >>> dm_soundex('Smith')
    {'463000'}
    >>> dm_soundex('Schmidt')
    {'463000'}

    >>> sorted(dm_soundex('The quick brown fox', max_length=20,
    ... zero_pad=False))
    ['35457976754', '3557976754']
    """
    _dms_table = {'STCH': (2, 4, 4), 'DRZ': (4, 4, 4), 'ZH': (4, 4, 4),
                  'ZHDZH': (2, 4, 4), 'DZH': (4, 4, 4), 'DRS': (4, 4, 4),
                  'DZS': (4, 4, 4), 'SCHTCH': (2, 4, 4), 'SHTSH': (2, 4, 4),
                  'SZCZ': (2, 4, 4), 'TZS': (4, 4, 4), 'SZCS': (2, 4, 4),
                  'STSH': (2, 4, 4), 'SHCH': (2, 4, 4), 'D': (3, 3, 3),
                  'H': (5, 5, '_'), 'TTSCH': (4, 4, 4), 'THS': (4, 4, 4),
                  'L': (8, 8, 8), 'P': (7, 7, 7), 'CHS': (5, 54, 54),
                  'T': (3, 3, 3), 'X': (5, 54, 54), 'OJ': (0, 1, '_'),
                  'OI': (0, 1, '_'), 'SCHTSH': (2, 4, 4), 'OY': (0, 1, '_'),
                  'Y': (1, '_', '_'), 'TSH': (4, 4, 4), 'ZDZ': (2, 4, 4),
                  'TSZ': (4, 4, 4), 'SHT': (2, 43, 43), 'SCHTSCH': (2, 4, 4),
                  'TTSZ': (4, 4, 4), 'TTZ': (4, 4, 4), 'SCH': (4, 4, 4),
                  'TTS': (4, 4, 4), 'SZD': (2, 43, 43), 'AI': (0, 1, '_'),
                  'PF': (7, 7, 7), 'TCH': (4, 4, 4), 'PH': (7, 7, 7),
                  'TTCH': (4, 4, 4), 'SZT': (2, 43, 43), 'ZDZH': (2, 4, 4),
                  'EI': (0, 1, '_'), 'G': (5, 5, 5), 'EJ': (0, 1, '_'),
                  'ZD': (2, 43, 43), 'IU': (1, '_', '_'), 'K': (5, 5, 5),
                  'O': (0, '_', '_'), 'SHTCH': (2, 4, 4), 'S': (4, 4, 4),
                  'TRZ': (4, 4, 4), 'SHD': (2, 43, 43), 'DSH': (4, 4, 4),
                  'CSZ': (4, 4, 4), 'EU': (1, 1, '_'), 'TRS': (4, 4, 4),
                  'ZS': (4, 4, 4), 'STRZ': (2, 4, 4), 'UY': (0, 1, '_'),
                  'STRS': (2, 4, 4), 'CZS': (4, 4, 4),
                  'MN': ('6_6', '6_6', '6_6'), 'UI': (0, 1, '_'),
                  'UJ': (0, 1, '_'), 'UE': (0, '_', '_'), 'EY': (0, 1, '_'),
                  'W': (7, 7, 7), 'IA': (1, '_', '_'), 'FB': (7, 7, 7),
                  'STSCH': (2, 4, 4), 'SCHT': (2, 43, 43),
                  'NM': ('6_6', '6_6', '6_6'), 'SCHD': (2, 43, 43),
                  'B': (7, 7, 7), 'DSZ': (4, 4, 4), 'F': (7, 7, 7),
                  'N': (6, 6, 6), 'CZ': (4, 4, 4), 'R': (9, 9, 9),
                  'U': (0, '_', '_'), 'V': (7, 7, 7), 'CS': (4, 4, 4),
                  'Z': (4, 4, 4), 'SZ': (4, 4, 4), 'TSCH': (4, 4, 4),
                  'KH': (5, 5, 5), 'ST': (2, 43, 43), 'KS': (5, 54, 54),
                  'SH': (4, 4, 4), 'SC': (2, 4, 4), 'SD': (2, 43, 43),
                  'DZ': (4, 4, 4), 'ZHD': (2, 43, 43), 'DT': (3, 3, 3),
                  'ZSH': (4, 4, 4), 'DS': (4, 4, 4), 'TZ': (4, 4, 4),
                  'TS': (4, 4, 4), 'TH': (3, 3, 3), 'TC': (4, 4, 4),
                  'A': (0, '_', '_'), 'E': (0, '_', '_'), 'I': (0, '_', '_'),
                  'AJ': (0, 1, '_'), 'M': (6, 6, 6), 'Q': (5, 5, 5),
                  'AU': (0, 7, '_'), 'IO': (1, '_', '_'), 'AY': (0, 1, '_'),
                  'IE': (1, '_', '_'), 'ZSCH': (4, 4, 4),
                  'CH': ((5, 4), (5, 4), (5, 4)),
                  'CK': ((5, 45), (5, 45), (5, 45)),
                  'C': ((5, 4), (5, 4), (5, 4)),
                  'J': ((1, 4), ('_', 4), ('_', 4)),
                  'RZ': ((94, 4), (94, 4), (94, 4)),
                  'RS': ((94, 4), (94, 4), (94, 4))}

    _dms_order = {'A': ('AI', 'AJ', 'AU', 'AY', 'A'),
                  'B': ('B',),
                  'C': ('CHS', 'CSZ', 'CZS', 'CH', 'CK', 'CS', 'CZ', 'C'),
                  'D': ('DRS', 'DRZ', 'DSH', 'DSZ', 'DZH', 'DZS', 'DS', 'DT',
                        'DZ', 'D'),
                  'E': ('EI', 'EJ', 'EU', 'EY', 'E'),
                  'F': ('FB', 'F'),
                  'G': ('G',),
                  'H': ('H',),
                  'I': ('IA', 'IE', 'IO', 'IU', 'I'),
                  'J': ('J',),
                  'K': ('KH', 'KS', 'K'),
                  'L': ('L',),
                  'M': ('MN', 'M'),
                  'N': ('NM', 'N'),
                  'O': ('OI', 'OJ', 'OY', 'O'),
                  'P': ('PF', 'PH', 'P'),
                  'Q': ('Q',),
                  'R': ('RS', 'RZ', 'R'),
                  'S': ('SCHTSCH', 'SCHTCH', 'SCHTSH', 'SHTCH', 'SHTSH',
                        'STSCH', 'SCHD', 'SCHT', 'SHCH', 'STCH', 'STRS',
                        'STRZ', 'STSH', 'SZCS', 'SZCZ', 'SCH', 'SHD', 'SHT',
                        'SZD', 'SZT', 'SC', 'SD', 'SH', 'ST', 'SZ', 'S'),
                  'T': ('TTSCH', 'TSCH', 'TTCH', 'TTSZ', 'TCH', 'THS', 'TRS',
                        'TRZ', 'TSH', 'TSZ', 'TTS', 'TTZ', 'TZS', 'TC', 'TH',
                        'TS', 'TZ', 'T'),
                  'U': ('UE', 'UI', 'UJ', 'UY', 'U'),
                  'V': ('V',),
                  'W': ('W',),
                  'X': ('X',),
                  'Y': ('Y',),
                  'Z': ('ZHDZH', 'ZDZH', 'ZSCH', 'ZDZ', 'ZHD', 'ZSH', 'ZD',
                        'ZH', 'ZS', 'Z')}

    _vowels = {'A', 'E', 'I', 'J', 'O', 'U', 'Y'}
    dms = ['']  # initialize empty code list

    # Require a max_length of at least 6 and not more than 64
    if max_length != -1:
        max_length = min(max(6, max_length), 64)
    else:
        max_length = 64

    # uppercase, normalize, decompose, and filter non-A-Z
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    # Nothing to convert, return base case
    if not word:
        if zero_pad:
            return {'0'*max_length}
        return {'0'}

    pos = 0
    while pos < len(word):
        # Iterate through _dms_order, which specifies the possible substrings
        # for which codes exist in the Daitch-Mokotoff coding
        for sstr in _dms_order[word[pos]]:  # pragma: no branch
            if word[pos:].startswith(sstr):
                # Having determined a valid substring start, retrieve the code
                dm_val = _dms_table[sstr]

                # Having retried the code (triple), determine the correct
                # positional variant (first, pre-vocalic, elsewhere)
                if pos == 0:
                    dm_val = dm_val[0]
                elif (pos+len(sstr) < len(word) and
                      word[pos+len(sstr)] in _vowels):
                    dm_val = dm_val[1]
                else:
                    dm_val = dm_val[2]

                # Build the code strings
                if isinstance(dm_val, tuple):
                    dms = [_ + text_type(dm_val[0]) for _ in dms] \
                            + [_ + text_type(dm_val[1]) for _ in dms]
                else:
                    dms = [_ + text_type(dm_val) for _ in dms]
                pos += len(sstr)
                break

    # Filter out double letters and _ placeholders
    dms = (''.join(c for c in _delete_consecutive_repeats(_) if c != '_')
           for _ in dms)

    # Trim codes and return set
    if zero_pad:
        dms = ((_ + ('0'*max_length))[:max_length] for _ in dms)
    else:
        dms = (_[:max_length] for _ in dms)
    return set(dms)


def koelner_phonetik(word):
    """Return the Kölner Phonetik (numeric output) code for a word.

    Based on the algorithm defined by :cite:`Postel:1969`.

    While the output code is numeric, it is still a str because 0s can lead
    the code.

    :param str word: the word to transform
    :returns: the Kölner Phonetik value as a numeric string
    :rtype: str

    >>> koelner_phonetik('Christopher')
    '478237'
    >>> koelner_phonetik('Niall')
    '65'
    >>> koelner_phonetik('Smith')
    '862'
    >>> koelner_phonetik('Schmidt')
    '862'
    >>> koelner_phonetik('Müller')
    '657'
    >>> koelner_phonetik('Zimmermann')
    '86766'
    """
    def _after(word, pos, letters):
        """Return True if word[i] follows one of the supplied letters."""
        return pos > 0 and word[pos-1] in letters

    def _before(word, pos, letters):
        """Return True if word[i] precedes one of the supplied letters."""
        return pos+1 < len(word) and word[pos+1] in letters

    _vowels = {'A', 'E', 'I', 'J', 'O', 'U', 'Y'}

    sdx = ''

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')

    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    # Nothing to convert, return base case
    if not word:
        return sdx

    for i in range(len(word)):
        if word[i] in _vowels:
            sdx += '0'
        elif word[i] == 'B':
            sdx += '1'
        elif word[i] == 'P':
            if _before(word, i, {'H'}):
                sdx += '3'
            else:
                sdx += '1'
        elif word[i] in {'D', 'T'}:
            if _before(word, i, {'C', 'S', 'Z'}):
                sdx += '8'
            else:
                sdx += '2'
        elif word[i] in {'F', 'V', 'W'}:
            sdx += '3'
        elif word[i] in {'G', 'K', 'Q'}:
            sdx += '4'
        elif word[i] == 'C':
            if _after(word, i, {'S', 'Z'}):
                sdx += '8'
            elif i == 0:
                if _before(word, i, {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U',
                                     'X'}):
                    sdx += '4'
                else:
                    sdx += '8'
            elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                sdx += '4'
            else:
                sdx += '8'
        elif word[i] == 'X':
            if _after(word, i, {'C', 'K', 'Q'}):
                sdx += '8'
            else:
                sdx += '48'
        elif word[i] == 'L':
            sdx += '5'
        elif word[i] in {'M', 'N'}:
            sdx += '6'
        elif word[i] == 'R':
            sdx += '7'
        elif word[i] in {'S', 'Z'}:
            sdx += '8'

    sdx = _delete_consecutive_repeats(sdx)

    if sdx:
        sdx = sdx[:1] + sdx[1:].replace('0', '')

    return sdx


def koelner_phonetik_num_to_alpha(num):
    """Convert a Kölner Phonetik code from numeric to alphabetic.

    :param str num: a numeric Kölner Phonetik representation (can be a str or
        an int)
    :returns: an alphabetic representation of the same word
    :rtype: str

    >>> koelner_phonetik_num_to_alpha('862')
    'SNT'
    >>> koelner_phonetik_num_to_alpha('657')
    'NLR'
    >>> koelner_phonetik_num_to_alpha('86766')
    'SNRNN'
    """
    _koelner_num_translation = dict(zip((ord(_) for _ in '012345678'),
                                        'APTFKLNRS'))
    num = ''.join(c for c in text_type(num) if c in {'0', '1', '2', '3', '4',
                                                     '5', '6', '7', '8'})
    return num.translate(_koelner_num_translation)


def koelner_phonetik_alpha(word):
    """Return the Kölner Phonetik (alphabetic output) code for a word.

    :param str word: the word to transform
    :returns: the Kölner Phonetik value as an alphabetic string
    :rtype: str

    >>> koelner_phonetik_alpha('Smith')
    'SNT'
    >>> koelner_phonetik_alpha('Schmidt')
    'SNT'
    >>> koelner_phonetik_alpha('Müller')
    'NLR'
    >>> koelner_phonetik_alpha('Zimmermann')
    'SNRNN'
    """
    return koelner_phonetik_num_to_alpha(koelner_phonetik(word))


def nysiis(word, max_length=6, modified=False):
    """Return the NYSIIS code for a word.

    The New York State Identification and Intelligence System algorithm is
    defined in :cite:`Taft:1970`.

    The modified version of this algorithm is described in Appendix B of
    :cite:`Lynch:1977`.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 6) of the code to return
    :param bool modified: indicates whether to use USDA modified NYSIIS
    :returns: the NYSIIS value
    :rtype: str

    >>> nysiis('Christopher')
    'CRASTA'
    >>> nysiis('Niall')
    'NAL'
    >>> nysiis('Smith')
    'SNAT'
    >>> nysiis('Schmidt')
    'SNAD'

    >>> nysiis('Christopher', max_length=-1)
    'CRASTAFAR'

    >>> nysiis('Christopher', max_length=8, modified=True)
    'CRASTAFA'
    >>> nysiis('Niall', max_length=8, modified=True)
    'NAL'
    >>> nysiis('Smith', max_length=8, modified=True)
    'SNAT'
    >>> nysiis('Schmidt', max_length=8, modified=True)
    'SNAD'
    """
    # Require a max_length of at least 6
    if max_length > -1:
        max_length = max(6, max_length)

    _vowels = {'A', 'E', 'I', 'O', 'U'}

    word = ''.join(c for c in word.upper() if c.isalpha())
    word = word.replace('ß', 'SS')

    # exit early if there are no alphas
    if not word:
        return ''

    original_first_char = word[0]

    if word[:3] == 'MAC':
        word = 'MCC'+word[3:]
    elif word[:2] == 'KN':
        word = 'NN'+word[2:]
    elif word[:1] == 'K':
        word = 'C'+word[1:]
    elif word[:2] in {'PH', 'PF'}:
        word = 'FF'+word[2:]
    elif word[:3] == 'SCH':
        word = 'SSS'+word[3:]
    elif modified:
        if word[:2] == 'WR':
            word = 'RR'+word[2:]
        elif word[:2] == 'RH':
            word = 'RR'+word[2:]
        elif word[:2] == 'DG':
            word = 'GG'+word[2:]
        elif word[:1] in _vowels:
            word = 'A'+word[1:]

    if modified and word[-1:] in {'S', 'Z'}:
        word = word[:-1]

    if word[-2:] == 'EE' or word[-2:] == 'IE' or (modified and
                                                  word[-2:] == 'YE'):
        word = word[:-2]+'Y'
    elif word[-2:] in {'DT', 'RT', 'RD'}:
        word = word[:-2]+'D'
    elif word[-2:] in {'NT', 'ND'}:
        word = word[:-2]+('N' if modified else 'D')
    elif modified:
        if word[-2:] == 'IX':
            word = word[:-2]+'ICK'
        elif word[-2:] == 'EX':
            word = word[:-2]+'ECK'
        elif word[-2:] in {'JR', 'SR'}:
            return 'ERROR'

    key = word[:1]

    skip = 0
    for i in range(1, len(word)):
        if i >= len(word):
            continue
        elif skip:
            skip -= 1
            continue
        elif word[i:i+2] == 'EV':
            word = word[:i] + 'AF' + word[i+2:]
            skip = 1
        elif word[i] in _vowels:
            word = word[:i] + 'A' + word[i+1:]
        elif modified and i != len(word)-1 and word[i] == 'Y':
            word = word[:i] + 'A' + word[i+1:]
        elif word[i] == 'Q':
            word = word[:i] + 'G' + word[i+1:]
        elif word[i] == 'Z':
            word = word[:i] + 'S' + word[i+1:]
        elif word[i] == 'M':
            word = word[:i] + 'N' + word[i+1:]
        elif word[i:i+2] == 'KN':
            word = word[:i] + 'N' + word[i+2:]
        elif word[i] == 'K':
            word = word[:i] + 'C' + word[i+1:]
        elif modified and i == len(word)-3 and word[i:i+3] == 'SCH':
            word = word[:i] + 'SSA'
            skip = 2
        elif word[i:i+3] == 'SCH':
            word = word[:i] + 'SSS' + word[i+3:]
            skip = 2
        elif modified and i == len(word)-2 and word[i:i+2] == 'SH':
            word = word[:i] + 'SA'
            skip = 1
        elif word[i:i+2] == 'SH':
            word = word[:i] + 'SS' + word[i+2:]
            skip = 1
        elif word[i:i+2] == 'PH':
            word = word[:i] + 'FF' + word[i+2:]
            skip = 1
        elif modified and word[i:i+3] == 'GHT':
            word = word[:i] + 'TTT' + word[i+3:]
            skip = 2
        elif modified and word[i:i+2] == 'DG':
            word = word[:i] + 'GG' + word[i+2:]
            skip = 1
        elif modified and word[i:i+2] == 'WR':
            word = word[:i] + 'RR' + word[i+2:]
            skip = 1
        elif word[i] == 'H' and (word[i-1] not in _vowels or
                                 word[i+1:i+2] not in _vowels):
            word = word[:i] + word[i-1] + word[i+1:]
        elif word[i] == 'W' and word[i-1] in _vowels:
            word = word[:i] + word[i-1] + word[i+1:]

        if word[i:i+skip+1] != key[-1:]:
            key += word[i:i+skip+1]

    key = _delete_consecutive_repeats(key)

    if key[-1:] == 'S':
        key = key[:-1]
    if key[-2:] == 'AY':
        key = key[:-2] + 'Y'
    if key[-1:] == 'A':
        key = key[:-1]
    if modified and key[:1] == 'A':
        key = original_first_char + key[1:]

    if max_length > 0:
        key = key[:max_length]

    return key


def mra(word):
    """Return the MRA personal numeric identifier (PNI) for a word.

    A description of the Western Airlines Surname Match Rating Algorithm can
    be found on page 18 of :cite:`Moore:1977`.

    :param str word: the word to transform
    :returns: the MRA PNI
    :rtype: str

    >>> mra('Christopher')
    'CHRPHR'
    >>> mra('Niall')
    'NL'
    >>> mra('Smith')
    'SMTH'
    >>> mra('Schmidt')
    'SCHMDT'
    """
    if not word:
        return word
    word = word.upper()
    word = word.replace('ß', 'SS')
    word = word[0]+''.join(c for c in word[1:] if
                           c not in {'A', 'E', 'I', 'O', 'U'})
    word = _delete_consecutive_repeats(word)
    if len(word) > 6:
        word = word[:3]+word[-3:]
    return word


def metaphone(word, max_length=-1):
    """Return the Metaphone code for a word.

    Based on Lawrence Philips' Pick BASIC code from 1990 :cite:`Philips:1990`,
    as described in :cite:`Philips:1990b`.
    This incorporates some corrections to the above code, particularly
    some of those suggested by Michael Kuhn in :cite:`Kuhn:1995`.

    :param str word: the word to transform
    :param int max_length: the maximum length of the returned Metaphone code
        (defaults to 64, but in Philips' original implementation this was 4)
    :returns: the Metaphone value
    :rtype: str


    >>> metaphone('Christopher')
    'KRSTFR'
    >>> metaphone('Niall')
    'NL'
    >>> metaphone('Smith')
    'SM0'
    >>> metaphone('Schmidt')
    'SKMTT'
    """
    _vowels = {'A', 'E', 'I', 'O', 'U'}
    _frontv = {'E', 'I', 'Y'}
    _varson = {'C', 'G', 'P', 'S', 'T'}

    # Require a max_length of at least 4
    if max_length != -1:
        max_length = max(4, max_length)
    else:
        max_length = 64

    # As in variable sound--those modified by adding an "h"
    ename = ''.join(c for c in word.upper() if c.isalnum())
    ename = ename.replace('ß', 'SS')

    # Delete non-alphanumeric characters and make all caps
    if not ename:
        return ''
    if ename[0:2] in {'PN', 'AE', 'KN', 'GN', 'WR'}:
        ename = ename[1:]
    elif ename[0] == 'X':
        ename = 'S' + ename[1:]
    elif ename[0:2] == 'WH':
        ename = 'W' + ename[2:]

    # Convert to metaphone
    elen = len(ename)-1
    metaph = ''
    for i in range(len(ename)):
        if len(metaph) >= max_length:
            break
        if ((ename[i] not in {'G', 'T'} and
             i > 0 and ename[i-1] == ename[i])):
            continue

        if ename[i] in _vowels and i == 0:
            metaph = ename[i]

        elif ename[i] == 'B':
            if i != elen or ename[i-1] != 'M':
                metaph += ename[i]

        elif ename[i] == 'C':
            if not (i > 0 and ename[i-1] == 'S' and ename[i+1:i+2] in _frontv):
                if ename[i+1:i+3] == 'IA':
                    metaph += 'X'
                elif ename[i+1:i+2] in _frontv:
                    metaph += 'S'
                elif i > 0 and ename[i-1:i+2] == 'SCH':
                    metaph += 'K'
                elif ename[i+1:i+2] == 'H':
                    if i == 0 and i+1 < elen and ename[i+2:i+3] not in _vowels:
                        metaph += 'K'
                    else:
                        metaph += 'X'
                else:
                    metaph += 'K'

        elif ename[i] == 'D':
            if ename[i+1:i+2] == 'G' and ename[i+2:i+3] in _frontv:
                metaph += 'J'
            else:
                metaph += 'T'

        elif ename[i] == 'G':
            if ename[i+1:i+2] == 'H' and not (i+1 == elen or
                                              ename[i+2:i+3] not in _vowels):
                continue
            elif i > 0 and ((i+1 == elen and ename[i+1] == 'N') or
                            (i+3 == elen and ename[i+1:i+4] == 'NED')):
                continue
            elif (i-1 > 0 and i+1 <= elen and ename[i-1] == 'D' and
                  ename[i+1] in _frontv):
                continue
            elif ename[i+1:i+2] == 'G':
                continue
            elif ename[i+1:i+2] in _frontv:
                if i == 0 or ename[i-1] != 'G':
                    metaph += 'J'
                else:
                    metaph += 'K'
            else:
                metaph += 'K'

        elif ename[i] == 'H':
            if ((i > 0 and ename[i-1] in _vowels and
                 ename[i+1:i+2] not in _vowels)):
                continue
            elif i > 0 and ename[i-1] in _varson:
                continue
            else:
                metaph += 'H'

        elif ename[i] in {'F', 'J', 'L', 'M', 'N', 'R'}:
            metaph += ename[i]

        elif ename[i] == 'K':
            if i > 0 and ename[i-1] == 'C':
                continue
            else:
                metaph += 'K'

        elif ename[i] == 'P':
            if ename[i+1:i+2] == 'H':
                metaph += 'F'
            else:
                metaph += 'P'

        elif ename[i] == 'Q':
            metaph += 'K'

        elif ename[i] == 'S':
            if ((i > 0 and i+2 <= elen and ename[i+1] == 'I' and
                 ename[i+2] in 'OA')):
                metaph += 'X'
            elif ename[i+1:i+2] == 'H':
                metaph += 'X'
            else:
                metaph += 'S'

        elif ename[i] == 'T':
            if ((i > 0 and i+2 <= elen and ename[i+1] == 'I' and
                 ename[i+2] in {'A', 'O'})):
                metaph += 'X'
            elif ename[i+1:i+2] == 'H':
                metaph += '0'
            elif ename[i+1:i+3] != 'CH':
                if ename[i-1:i] != 'T':
                    metaph += 'T'

        elif ename[i] == 'V':
            metaph += 'F'

        elif ename[i] in 'WY':
            if ename[i+1:i+2] in _vowels:
                metaph += ename[i]

        elif ename[i] == 'X':
            metaph += 'KS'

        elif ename[i] == 'Z':
            metaph += 'S'

    return metaph


def double_metaphone(word, max_length=-1):
    """Return the Double Metaphone code for a word.

    Based on Lawrence Philips' (Visual) C++ code from 1999
    :cite:`Philips:2000`.

    :param word: the word to transform
    :param max_length: the maximum length of the returned Double Metaphone
        codes (defaults to 64, but in Philips' original implementation this
        was 4)
    :returns: the Double Metaphone value(s)
    :rtype: tuple

    >>> double_metaphone('Christopher')
    ('KRSTFR', '')
    >>> double_metaphone('Niall')
    ('NL', '')
    >>> double_metaphone('Smith')
    ('SM0', 'XMT')
    >>> double_metaphone('Schmidt')
    ('XMT', 'SMT')
    """
    # Require a max_length of at least 4
    if max_length != -1:
        max_length = max(4, max_length)
    else:
        max_length = 64

    primary = ''
    secondary = ''

    def _slavo_germanic():
        """Return True if the word appears to be Slavic or Germanic."""
        if 'W' in word or 'K' in word or 'CZ' in word:
            return True
        return False

    def _metaph_add(pri, sec=''):
        """Return a new metaphone tuple with the supplied elements."""
        newpri = primary
        newsec = secondary
        if pri:
            newpri += pri
        if sec:
            if sec != ' ':
                newsec += sec
        else:
            newsec += pri
        return newpri, newsec

    def _is_vowel(pos):
        """Return True if the character at word[pos] is a vowel."""
        if pos >= 0 and word[pos] in {'A', 'E', 'I', 'O', 'U', 'Y'}:
            return True
        return False

    def _get_at(pos):
        """Return the character at word[pos]."""
        return word[pos]

    def _string_at(pos, slen, substrings):
        """Return True if word[pos:pos+slen] is in substrings."""
        if pos < 0:
            return False
        return word[pos:pos+slen] in substrings

    current = 0
    length = len(word)
    if length < 1:
        return '', ''
    last = length - 1

    word = word.upper()
    word = word.replace('ß', 'SS')

    # Pad the original string so that we can index beyond the edge of the world
    word += '     '

    # Skip these when at start of word
    if word[0:2] in {'GN', 'KN', 'PN', 'WR', 'PS'}:
        current += 1

    # Initial 'X' is pronounced 'Z' e.g. 'Xavier'
    if _get_at(0) == 'X':
        primary, secondary = _metaph_add('S')  # 'Z' maps to 'S'
        current += 1

    # Main loop
    while True:
        if current >= length:
            break

        if _get_at(current) in {'A', 'E', 'I', 'O', 'U', 'Y'}:
            if current == 0:
                # All init vowels now map to 'A'
                primary, secondary = _metaph_add('A')
            current += 1
            continue

        elif _get_at(current) == 'B':
            # "-mb", e.g", "dumb", already skipped over...
            primary, secondary = _metaph_add('P')
            if _get_at(current + 1) == 'B':
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'Ç':
            primary, secondary = _metaph_add('S')
            current += 1
            continue

        elif _get_at(current) == 'C':
            # Various Germanic
            if (current > 1 and not _is_vowel(current - 2) and
                    _string_at((current - 1), 3, {'ACH'}) and
                    ((_get_at(current + 2) != 'I') and
                     ((_get_at(current + 2) != 'E') or
                      _string_at((current - 2), 6,
                                 {'BACHER', 'MACHER'})))):
                primary, secondary = _metaph_add('K')
                current += 2
                continue

            # Special case 'caesar'
            elif current == 0 and _string_at(current, 6, {'CAESAR'}):
                primary, secondary = _metaph_add('S')
                current += 2
                continue

            # Italian 'chianti'
            elif _string_at(current, 4, {'CHIA'}):
                primary, secondary = _metaph_add('K')
                current += 2
                continue

            elif _string_at(current, 2, {'CH'}):
                # Find 'Michael'
                if current > 0 and _string_at(current, 4, {'CHAE'}):
                    primary, secondary = _metaph_add('K', 'X')
                    current += 2
                    continue

                # Greek roots e.g. 'chemistry', 'chorus'
                elif (current == 0 and
                      (_string_at((current + 1), 5,
                                  {'HARAC', 'HARIS'}) or
                       _string_at((current + 1), 3,
                                  {'HOR', 'HYM', 'HIA', 'HEM'})) and
                      not _string_at(0, 5, {'CHORE'})):
                    primary, secondary = _metaph_add('K')
                    current += 2
                    continue

                # Germanic, Greek, or otherwise 'ch' for 'kh' sound
                elif ((_string_at(0, 4, {'VAN ', 'VON '}) or
                       _string_at(0, 3, {'SCH'})) or
                      # 'architect but not 'arch', 'orchestra', 'orchid'
                      _string_at((current - 2), 6,
                                 {'ORCHES', 'ARCHIT', 'ORCHID'}) or
                      _string_at((current + 2), 1, {'T', 'S'}) or
                      ((_string_at((current - 1), 1,
                                   {'A', 'O', 'U', 'E'}) or
                        (current == 0)) and
                       # e.g., 'wachtler', 'wechsler', but not 'tichner'
                       _string_at((current + 2), 1,
                                  {'L', 'R', 'N', 'M', 'B', 'H', 'F', 'V', 'W',
                                   ' '}))):
                    primary, secondary = _metaph_add('K')

                else:
                    if current > 0:
                        if _string_at(0, 2, {'MC'}):
                            # e.g., "McHugh"
                            primary, secondary = _metaph_add('K')
                        else:
                            primary, secondary = _metaph_add('X', 'K')
                    else:
                        primary, secondary = _metaph_add('X')

                current += 2
                continue

            # e.g, 'czerny'
            elif (_string_at(current, 2, {'CZ'}) and
                  not _string_at((current - 2), 4, {'WICZ'})):
                primary, secondary = _metaph_add('S', 'X')
                current += 2
                continue

            # e.g., 'focaccia'
            elif _string_at((current + 1), 3, {'CIA'}):
                primary, secondary = _metaph_add('X')
                current += 3

            # double 'C', but not if e.g. 'McClellan'
            elif (_string_at(current, 2, {'CC'}) and
                  not ((current == 1) and (_get_at(0) == 'M'))):
                # 'bellocchio' but not 'bacchus'
                if ((_string_at((current + 2), 1,
                                {'I', 'E', 'H'}) and
                     not _string_at((current + 2), 2, ['HU']))):
                    # 'accident', 'accede' 'succeed'
                    if ((((current == 1) and _get_at(current - 1) == 'A') or
                         _string_at((current - 1), 5,
                                    {'UCCEE', 'UCCES'}))):
                        primary, secondary = _metaph_add('KS')
                    # 'bacci', 'bertucci', other italian
                    else:
                        primary, secondary = _metaph_add('X')
                    current += 3
                    continue
                else:  # Pierce's rule
                    primary, secondary = _metaph_add('K')
                    current += 2
                    continue

            elif _string_at(current, 2, {'CK', 'CG', 'CQ'}):
                primary, secondary = _metaph_add('K')
                current += 2
                continue

            elif _string_at(current, 2, {'CI', 'CE', 'CY'}):
                # Italian vs. English
                if _string_at(current, 3, {'CIO', 'CIE', 'CIA'}):
                    primary, secondary = _metaph_add('S', 'X')
                else:
                    primary, secondary = _metaph_add('S')
                current += 2
                continue

            # else
            else:
                primary, secondary = _metaph_add('K')

                # name sent in 'mac caffrey', 'mac gregor
                if _string_at((current + 1), 2, {' C', ' Q', ' G'}):
                    current += 3
                elif (_string_at((current + 1), 1,
                                 {'C', 'K', 'Q'}) and
                      not _string_at((current + 1), 2, {'CE', 'CI'})):
                    current += 2
                else:
                    current += 1
                continue

        elif _get_at(current) == 'D':
            if _string_at(current, 2, {'DG'}):
                if _string_at((current + 2), 1, {'I', 'E', 'Y'}):
                    # e.g. 'edge'
                    primary, secondary = _metaph_add('J')
                    current += 3
                    continue
                else:
                    # e.g. 'edgar'
                    primary, secondary = _metaph_add('TK')
                    current += 2
                    continue

            elif _string_at(current, 2, {'DT', 'DD'}):
                primary, secondary = _metaph_add('T')
                current += 2
                continue

            # else
            else:
                primary, secondary = _metaph_add('T')
                current += 1
                continue

        elif _get_at(current) == 'F':
            if _get_at(current + 1) == 'F':
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('F')
            continue

        elif _get_at(current) == 'G':
            if _get_at(current + 1) == 'H':
                if (current > 0) and not _is_vowel(current - 1):
                    primary, secondary = _metaph_add('K')
                    current += 2
                    continue

                # 'ghislane', ghiradelli
                elif current == 0:
                    if _get_at(current + 2) == 'I':
                        primary, secondary = _metaph_add('J')
                    else:
                        primary, secondary = _metaph_add('K')
                    current += 2
                    continue

                # Parker's rule (with some further refinements) - e.g., 'hugh'
                elif (((current > 1) and
                       _string_at((current - 2), 1, {'B', 'H', 'D'})) or
                      # e.g., 'bough'
                      ((current > 2) and
                       _string_at((current - 3), 1, {'B', 'H', 'D'})) or
                      # e.g., 'broughton'
                      ((current > 3) and
                       _string_at((current - 4), 1, {'B', 'H'}))):
                    current += 2
                    continue
                else:
                    # e.g. 'laugh', 'McLaughlin', 'cough',
                    #      'gough', 'rough', 'tough'
                    if ((current > 2) and
                            (_get_at(current - 1) == 'U') and
                            (_string_at((current - 3), 1,
                                        {'C', 'G', 'L', 'R', 'T'}))):
                        primary, secondary = _metaph_add('F')
                    elif (current > 0) and _get_at(current - 1) != 'I':
                        primary, secondary = _metaph_add('K')
                    current += 2
                    continue

            elif _get_at(current + 1) == 'N':
                if (current == 1) and _is_vowel(0) and not _slavo_germanic():
                    primary, secondary = _metaph_add('KN', 'N')
                # not e.g. 'cagney'
                elif (not _string_at((current + 2), 2, {'EY'}) and
                      (_get_at(current + 1) != 'Y') and
                      not _slavo_germanic()):
                    primary, secondary = _metaph_add('N', 'KN')
                else:
                    primary, secondary = _metaph_add('KN')
                current += 2
                continue

            # 'tagliaro'
            elif (_string_at((current + 1), 2, {'LI'}) and
                  not _slavo_germanic()):
                primary, secondary = _metaph_add('KL', 'L')
                current += 2
                continue

            # -ges-, -gep-, -gel-, -gie- at beginning
            elif ((current == 0) and
                  ((_get_at(current + 1) == 'Y') or
                   _string_at((current + 1), 2, {'ES', 'EP', 'EB', 'EL', 'EY',
                                                 'IB', 'IL', 'IN', 'IE', 'EI',
                                                 'ER'}))):
                primary, secondary = _metaph_add('K', 'J')
                current += 2
                continue

            #  -ger-,  -gy-
            elif ((_string_at((current + 1), 2, {'ER'}) or
                   (_get_at(current + 1) == 'Y')) and not
                  _string_at(0, 6, {'DANGER', 'RANGER', 'MANGER'}) and not
                  _string_at((current - 1), 1, {'E', 'I'}) and not
                  _string_at((current - 1), 3, {'RGY', 'OGY'})):
                primary, secondary = _metaph_add('K', 'J')
                current += 2
                continue

            #  italian e.g, 'biaggi'
            elif (_string_at((current + 1), 1, {'E', 'I', 'Y'}) or
                  _string_at((current - 1), 4, {'AGGI', 'OGGI'})):
                # obvious germanic
                if (((_string_at(0, 4, {'VAN ', 'VON '}) or
                      _string_at(0, 3, {'SCH'})) or
                     _string_at((current + 1), 2, {'ET'}))):
                    primary, secondary = _metaph_add('K')
                elif _string_at((current + 1), 4, {'IER '}):
                    primary, secondary = _metaph_add('J')
                else:
                    primary, secondary = _metaph_add('J', 'K')
                current += 2
                continue

            else:
                if _get_at(current + 1) == 'G':
                    current += 2
                else:
                    current += 1
                primary, secondary = _metaph_add('K')
                continue

        elif _get_at(current) == 'H':
            # only keep if first & before vowel or btw. 2 vowels
            if ((((current == 0) or _is_vowel(current - 1)) and
                 _is_vowel(current + 1))):
                primary, secondary = _metaph_add('H')
                current += 2
            else:  # also takes care of 'HH'
                current += 1
            continue

        elif _get_at(current) == 'J':
            # obvious spanish, 'jose', 'san jacinto'
            if _string_at(current, 4, ['JOSE']) or _string_at(0, 4, {'SAN '}):
                if ((((current == 0) and (_get_at(current + 4) == ' ')) or
                     _string_at(0, 4, ['SAN ']))):
                    primary, secondary = _metaph_add('H')
                else:
                    primary, secondary = _metaph_add('J', 'H')
                current += 1
                continue

            elif (current == 0) and not _string_at(current, 4, {'JOSE'}):
                # Yankelovich/Jankelowicz
                primary, secondary = _metaph_add('J', 'A')
            # Spanish pron. of e.g. 'bajador'
            elif (_is_vowel(current - 1) and
                  not _slavo_germanic() and
                  ((_get_at(current + 1) == 'A') or
                   (_get_at(current + 1) == 'O'))):
                primary, secondary = _metaph_add('J', 'H')
            elif current == last:
                primary, secondary = _metaph_add('J', ' ')
            elif (not _string_at((current + 1), 1,
                                 {'L', 'T', 'K', 'S', 'N', 'M', 'B', 'Z'}) and
                  not _string_at((current - 1), 1, {'S', 'K', 'L'})):
                primary, secondary = _metaph_add('J')

            if _get_at(current + 1) == 'J':  # it could happen!
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'K':
            if _get_at(current + 1) == 'K':
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('K')
            continue

        elif _get_at(current) == 'L':
            if _get_at(current + 1) == 'L':
                # Spanish e.g. 'cabrillo', 'gallegos'
                if (((current == (length - 3)) and
                     _string_at((current - 1), 4, {'ILLO', 'ILLA', 'ALLE'})) or
                        ((_string_at((last - 1), 2, {'AS', 'OS'}) or
                          _string_at(last, 1, {'A', 'O'})) and
                         _string_at((current - 1), 4, {'ALLE'}))):
                    primary, secondary = _metaph_add('L', ' ')
                    current += 2
                    continue
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('L')
            continue

        elif _get_at(current) == 'M':
            if (((_string_at((current - 1), 3, {'UMB'}) and
                  (((current + 1) == last) or
                   _string_at((current + 2), 2, {'ER'}))) or
                 # 'dumb', 'thumb'
                 (_get_at(current + 1) == 'M'))):
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('M')
            continue

        elif _get_at(current) == 'N':
            if _get_at(current + 1) == 'N':
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('N')
            continue

        elif _get_at(current) == 'Ñ':
            current += 1
            primary, secondary = _metaph_add('N')
            continue

        elif _get_at(current) == 'P':
            if _get_at(current + 1) == 'H':
                primary, secondary = _metaph_add('F')
                current += 2
                continue

            # also account for "campbell", "raspberry"
            elif _string_at((current + 1), 1, {'P', 'B'}):
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('P')
            continue

        elif _get_at(current) == 'Q':
            if _get_at(current + 1) == 'Q':
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('K')
            continue

        elif _get_at(current) == 'R':
            # french e.g. 'rogier', but exclude 'hochmeier'
            if (((current == last) and
                 not _slavo_germanic() and
                 _string_at((current - 2), 2, {'IE'}) and
                 not _string_at((current - 4), 2, {'ME', 'MA'}))):
                primary, secondary = _metaph_add('', 'R')
            else:
                primary, secondary = _metaph_add('R')

            if _get_at(current + 1) == 'R':
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'S':
            # special cases 'island', 'isle', 'carlisle', 'carlysle'
            if _string_at((current - 1), 3, {'ISL', 'YSL'}):
                current += 1
                continue

            # special case 'sugar-'
            elif (current == 0) and _string_at(current, 5, {'SUGAR'}):
                primary, secondary = _metaph_add('X', 'S')
                current += 1
                continue

            elif _string_at(current, 2, {'SH'}):
                # Germanic
                if _string_at((current + 1), 4,
                              {'HEIM', 'HOEK', 'HOLM', 'HOLZ'}):
                    primary, secondary = _metaph_add('S')
                else:
                    primary, secondary = _metaph_add('X')
                current += 2
                continue

            # Italian & Armenian
            elif (_string_at(current, 3, {'SIO', 'SIA'}) or
                  _string_at(current, 4, {'SIAN'})):
                if not _slavo_germanic():
                    primary, secondary = _metaph_add('S', 'X')
                else:
                    primary, secondary = _metaph_add('S')
                current += 3
                continue

            # German & anglicisations, e.g. 'smith' match 'schmidt',
            #                               'snider' match 'schneider'
            # also, -sz- in Slavic language although in Hungarian it is
            #       pronounced 's'
            elif (((current == 0) and
                   _string_at((current + 1), 1, {'M', 'N', 'L', 'W'})) or
                  _string_at((current + 1), 1, {'Z'})):
                primary, secondary = _metaph_add('S', 'X')
                if _string_at((current + 1), 1, {'Z'}):
                    current += 2
                else:
                    current += 1
                continue

            elif _string_at(current, 2, {'SC'}):
                # Schlesinger's rule
                if _get_at(current + 2) == 'H':
                    # dutch origin, e.g. 'school', 'schooner'
                    if _string_at((current + 3), 2,
                                  {'OO', 'ER', 'EN', 'UY', 'ED', 'EM'}):
                        # 'schermerhorn', 'schenker'
                        if _string_at((current + 3), 2, {'ER', 'EN'}):
                            primary, secondary = _metaph_add('X', 'SK')
                        else:
                            primary, secondary = _metaph_add('SK')
                        current += 3
                        continue
                    else:
                        if (((current == 0) and not _is_vowel(3) and
                             (_get_at(3) != 'W'))):
                            primary, secondary = _metaph_add('X', 'S')
                        else:
                            primary, secondary = _metaph_add('X')
                        current += 3
                        continue

                elif _string_at((current + 2), 1, {'I', 'E', 'Y'}):
                    primary, secondary = _metaph_add('S')
                    current += 3
                    continue

                # else
                else:
                    primary, secondary = _metaph_add('SK')
                    current += 3
                    continue

            else:
                # french e.g. 'resnais', 'artois'
                if (current == last) and _string_at((current - 2), 2,
                                                    {'AI', 'OI'}):
                    primary, secondary = _metaph_add('', 'S')
                else:
                    primary, secondary = _metaph_add('S')

                if _string_at((current + 1), 1, {'S', 'Z'}):
                    current += 2
                else:
                    current += 1
                continue

        elif _get_at(current) == 'T':
            if _string_at(current, 4, {'TION'}):
                primary, secondary = _metaph_add('X')
                current += 3
                continue

            elif _string_at(current, 3, {'TIA', 'TCH'}):
                primary, secondary = _metaph_add('X')
                current += 3
                continue

            elif (_string_at(current, 2, {'TH'}) or
                  _string_at(current, 3, {'TTH'})):
                # special case 'thomas', 'thames' or germanic
                if ((_string_at((current + 2), 2, {'OM', 'AM'}) or
                     _string_at(0, 4, {'VAN ', 'VON '}) or
                     _string_at(0, 3, {'SCH'}))):
                    primary, secondary = _metaph_add('T')
                else:
                    primary, secondary = _metaph_add('0', 'T')
                current += 2
                continue

            elif _string_at((current + 1), 1, {'T', 'D'}):
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('T')
            continue

        elif _get_at(current) == 'V':
            if _get_at(current + 1) == 'V':
                current += 2
            else:
                current += 1
            primary, secondary = _metaph_add('F')
            continue

        elif _get_at(current) == 'W':
            # can also be in middle of word
            if _string_at(current, 2, {'WR'}):
                primary, secondary = _metaph_add('R')
                current += 2
                continue
            elif ((current == 0) and
                  (_is_vowel(current + 1) or _string_at(current, 2, {'WH'}))):
                # Wasserman should match Vasserman
                if _is_vowel(current + 1):
                    primary, secondary = _metaph_add('A', 'F')
                else:
                    # need Uomo to match Womo
                    primary, secondary = _metaph_add('A')

            # Arnow should match Arnoff
            if ((((current == last) and _is_vowel(current - 1)) or
                 _string_at((current - 1), 5,
                            {'EWSKI', 'EWSKY', 'OWSKI', 'OWSKY'}) or
                 _string_at(0, 3, ['SCH']))):
                primary, secondary = _metaph_add('', 'F')
                current += 1
                continue
            # Polish e.g. 'filipowicz'
            elif _string_at(current, 4, {'WICZ', 'WITZ'}):
                primary, secondary = _metaph_add('TS', 'FX')
                current += 4
                continue
            # else skip it
            else:
                current += 1
                continue

        elif _get_at(current) == 'X':
            # French e.g. breaux
            if (not ((current == last) and
                     (_string_at((current - 3), 3, {'IAU', 'EAU'}) or
                      _string_at((current - 2), 2, {'AU', 'OU'})))):
                primary, secondary = _metaph_add('KS')

            if _string_at((current + 1), 1, {'C', 'X'}):
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'Z':
            # Chinese Pinyin e.g. 'zhao'
            if _get_at(current + 1) == 'H':
                primary, secondary = _metaph_add('J')
                current += 2
                continue
            elif (_string_at((current + 1), 2, {'ZO', 'ZI', 'ZA'}) or
                  (_slavo_germanic() and ((current > 0) and
                                          _get_at(current - 1) != 'T'))):
                primary, secondary = _metaph_add('S', 'TS')
            else:
                primary, secondary = _metaph_add('S')

            if _get_at(current + 1) == 'Z':
                current += 2
            else:
                current += 1
            continue

        else:
            current += 1

    if max_length > 0:
        primary = primary[:max_length]
        secondary = secondary[:max_length]
    if primary == secondary:
        secondary = ''

    return primary, secondary


def caverphone(word, version=2):
    """Return the Caverphone code for a word.

    A description of version 1 of the algorithm can be found in
    :cite:`Hood:2002`.

    A description of version 2 of the algorithm can be found in
    :cite:`Hood:2004`.

    :param str word: the word to transform
    :param int version: the version of Caverphone to employ for encoding
        (defaults to 2)
    :returns: the Caverphone value
    :rtype: str

    >>> caverphone('Christopher')
    'KRSTFA1111'
    >>> caverphone('Niall')
    'NA11111111'
    >>> caverphone('Smith')
    'SMT1111111'
    >>> caverphone('Schmidt')
    'SKMT111111'

    >>> caverphone('Christopher', 1)
    'KRSTF1'
    >>> caverphone('Niall', 1)
    'N11111'
    >>> caverphone('Smith', 1)
    'SMT111'
    >>> caverphone('Schmidt', 1)
    'SKMT11'
    """
    _vowels = {'a', 'e', 'i', 'o', 'u'}

    word = word.lower()
    word = ''.join(c for c in word if c in
                   {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                    'y', 'z'})

    def _squeeze_replace(word, char, new_char):
        """Convert strings of char in word to one instance of new_char."""
        while char * 2 in word:
            word = word.replace(char * 2, char)
        return word.replace(char, new_char)

    # the main replacement algorithm
    if version != 1 and word[-1:] == 'e':
        word = word[:-1]
    if word:
        if word[:5] == 'cough':
            word = 'cou2f'+word[5:]
        if word[:5] == 'rough':
            word = 'rou2f'+word[5:]
        if word[:5] == 'tough':
            word = 'tou2f'+word[5:]
        if word[:6] == 'enough':
            word = 'enou2f'+word[6:]
        if version != 1 and word[:6] == 'trough':
            word = 'trou2f'+word[6:]
        if word[:2] == 'gn':
            word = '2n'+word[2:]
        if word[-2:] == 'mb':
            word = word[:-1]+'2'
        word = word.replace('cq', '2q')
        word = word.replace('ci', 'si')
        word = word.replace('ce', 'se')
        word = word.replace('cy', 'sy')
        word = word.replace('tch', '2ch')
        word = word.replace('c', 'k')
        word = word.replace('q', 'k')
        word = word.replace('x', 'k')
        word = word.replace('v', 'f')
        word = word.replace('dg', '2g')
        word = word.replace('tio', 'sio')
        word = word.replace('tia', 'sia')
        word = word.replace('d', 't')
        word = word.replace('ph', 'fh')
        word = word.replace('b', 'p')
        word = word.replace('sh', 's2')
        word = word.replace('z', 's')
        if word[0] in _vowels:
            word = 'A'+word[1:]
        word = word.replace('a', '3')
        word = word.replace('e', '3')
        word = word.replace('i', '3')
        word = word.replace('o', '3')
        word = word.replace('u', '3')
        if version != 1:
            word = word.replace('j', 'y')
            if word[:2] == 'y3':
                word = 'Y3'+word[2:]
            if word[:1] == 'y':
                word = 'A'+word[1:]
            word = word.replace('y', '3')
        word = word.replace('3gh3', '3kh3')
        word = word.replace('gh', '22')
        word = word.replace('g', 'k')

        word = _squeeze_replace(word, 's', 'S')
        word = _squeeze_replace(word, 't', 'T')
        word = _squeeze_replace(word, 'p', 'P')
        word = _squeeze_replace(word, 'k', 'K')
        word = _squeeze_replace(word, 'f', 'F')
        word = _squeeze_replace(word, 'm', 'M')
        word = _squeeze_replace(word, 'n', 'N')

        word = word.replace('w3', 'W3')
        if version == 1:
            word = word.replace('wy', 'Wy')
        word = word.replace('wh3', 'Wh3')
        if version == 1:
            word = word.replace('why', 'Why')
        if version != 1 and word[-1:] == 'w':
            word = word[:-1]+'3'
        word = word.replace('w', '2')
        if word[:1] == 'h':
            word = 'A'+word[1:]
        word = word.replace('h', '2')
        word = word.replace('r3', 'R3')
        if version == 1:
            word = word.replace('ry', 'Ry')
        if version != 1 and word[-1:] == 'r':
            word = word[:-1]+'3'
        word = word.replace('r', '2')
        word = word.replace('l3', 'L3')
        if version == 1:
            word = word.replace('ly', 'Ly')
        if version != 1 and word[-1:] == 'l':
            word = word[:-1]+'3'
        word = word.replace('l', '2')
        if version == 1:
            word = word.replace('j', 'y')
            word = word.replace('y3', 'Y3')
            word = word.replace('y', '2')
        word = word.replace('2', '')
        if version != 1 and word[-1:] == '3':
            word = word[:-1]+'A'
        word = word.replace('3', '')

    # pad with 1s, then extract the necessary length of code
    word += '1'*10
    if version != 1:
        word = word[:10]
    else:
        word = word[:6]

    return word


def alpha_sis(word, max_length=14):
    """Return the IBM Alpha Search Inquiry System code for a word.

    The Alpha Search Inquiry System code is defined in :cite:`IBM:1973`.
    This implementation is based on the description in :cite:`Moore:1977`.

    A collection is necessary since there can be multiple values for a
    single word. But the collection must be ordered since the first value
    is the primary coding.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 14)
    :returns: the Alpha SIS value
    :rtype: tuple

    >>> alpha_sis('Christopher')
    ('06401840000000', '07040184000000', '04018400000000')
    >>> alpha_sis('Niall')
    ('02500000000000',)
    >>> alpha_sis('Smith')
    ('03100000000000',)
    >>> alpha_sis('Schmidt')
    ('06310000000000',)
    """
    _alpha_sis_initials = {'GF': '08', 'GM': '03', 'GN': '02', 'KN': '02',
                           'PF': '08', 'PN': '02', 'PS': '00', 'WR': '04',
                           'A': '1', 'E': '1', 'H': '2', 'I': '1', 'J': '3',
                           'O': '1', 'U': '1', 'W': '4', 'Y': '5'}
    _alpha_sis_initials_order = ('GF', 'GM', 'GN', 'KN', 'PF', 'PN', 'PS',
                                 'WR', 'A', 'E', 'H', 'I', 'J', 'O', 'U', 'W',
                                 'Y')
    _alpha_sis_basic = {'SCH': '6', 'CZ': ('70', '6', '0'),
                        'CH': ('6', '70', '0'), 'CK': ('7', '6'),
                        'DS': ('0', '10'), 'DZ': ('0', '10'),
                        'TS': ('0', '10'), 'TZ': ('0', '10'), 'CI': '0',
                        'CY': '0', 'CE': '0', 'SH': '6', 'DG': '7', 'PH': '8',
                        'C': ('7', '6'), 'K': ('7', '6'), 'Z': '0', 'S': '0',
                        'D': '1', 'T': '1', 'N': '2', 'M': '3', 'R': '4',
                        'L': '5', 'J': '6', 'G': '7', 'Q': '7', 'X': '7',
                        'F': '8', 'V': '8', 'B': '9', 'P': '9'}
    _alpha_sis_basic_order = ('SCH', 'CZ', 'CH', 'CK', 'DS', 'DZ', 'TS', 'TZ',
                              'CI', 'CY', 'CE', 'SH', 'DG', 'PH', 'C', 'K',
                              'Z', 'S', 'D', 'T', 'N', 'M', 'R', 'L', 'J', 'C',
                              'G', 'K', 'Q', 'X', 'F', 'V', 'B', 'P')

    alpha = ['']
    pos = 0
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    # Clamp max_length to [4, 64]
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    # Do special processing for initial substrings
    for k in _alpha_sis_initials_order:
        if word.startswith(k):
            alpha[0] += _alpha_sis_initials[k]
            pos += len(k)
            break

    # Add a '0' if alpha is still empty
    if not alpha[0]:
        alpha[0] += '0'

    # Whether or not any special initial codes were encoded, iterate
    # through the length of the word in the main encoding loop
    while pos < len(word):
        orig_pos = pos
        for k in _alpha_sis_basic_order:
            if word[pos:].startswith(k):
                if isinstance(_alpha_sis_basic[k], tuple):
                    newalpha = []
                    for i in range(len(_alpha_sis_basic[k])):
                        newalpha += [_ + _alpha_sis_basic[k][i] for _ in alpha]
                    alpha = newalpha
                else:
                    alpha = [_ + _alpha_sis_basic[k] for _ in alpha]
                pos += len(k)
                break
        if pos == orig_pos:
            alpha = [_ + '_' for _ in alpha]
            pos += 1

    # Trim doublets and placeholders
    for i in range(len(alpha)):
        pos = 1
        while pos < len(alpha[i]):
            if alpha[i][pos] == alpha[i][pos-1]:
                alpha[i] = alpha[i][:pos]+alpha[i][pos+1:]
            pos += 1
    alpha = (_.replace('_', '') for _ in alpha)

    # Trim codes and return tuple
    alpha = ((_ + ('0'*max_length))[:max_length] for _ in alpha)
    return tuple(alpha)


def fuzzy_soundex(word, max_length=5, zero_pad=True):
    """Return the Fuzzy Soundex code for a word.

    Fuzzy Soundex is an algorithm derived from Soundex, defined in
    :cite:`Holmes:2002`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool zero_pad: pad the end of the return value with 0s to achieve
        a max_length string
    :returns: the Fuzzy Soundex value
    :rtype: str

    >>> fuzzy_soundex('Christopher')
    'K6931'
    >>> fuzzy_soundex('Niall')
    'N4000'
    >>> fuzzy_soundex('Smith')
    'S5300'
    >>> fuzzy_soundex('Smith')
    'S5300'
    """
    _fuzzy_soundex_translation = dict(zip((ord(_) for _ in
                                           'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                          '0193017-07745501769301-7-9'))

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')

    # Clamp max_length to [4, 64]
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    if not word:
        if zero_pad:
            return '0' * max_length
        return '0'

    if word[:2] in {'CS', 'CZ', 'TS', 'TZ'}:
        word = 'SS' + word[2:]
    elif word[:2] == 'GN':
        word = 'NN' + word[2:]
    elif word[:2] in {'HR', 'WR'}:
        word = 'RR' + word[2:]
    elif word[:2] == 'HW':
        word = 'WW' + word[2:]
    elif word[:2] in {'KN', 'NG'}:
        word = 'NN' + word[2:]

    if word[-2:] == 'CH':
        word = word[:-2] + 'KK'
    elif word[-2:] == 'NT':
        word = word[:-2] + 'TT'
    elif word[-2:] == 'RT':
        word = word[:-2] + 'RR'
    elif word[-3:] == 'RDT':
        word = word[:-3] + 'RR'

    word = word.replace('CA', 'KA')
    word = word.replace('CC', 'KK')
    word = word.replace('CK', 'KK')
    word = word.replace('CE', 'SE')
    word = word.replace('CHL', 'KL')
    word = word.replace('CL', 'KL')
    word = word.replace('CHR', 'KR')
    word = word.replace('CR', 'KR')
    word = word.replace('CI', 'SI')
    word = word.replace('CO', 'KO')
    word = word.replace('CU', 'KU')
    word = word.replace('CY', 'SY')
    word = word.replace('DG', 'GG')
    word = word.replace('GH', 'HH')
    word = word.replace('MAC', 'MK')
    word = word.replace('MC', 'MK')
    word = word.replace('NST', 'NSS')
    word = word.replace('PF', 'FF')
    word = word.replace('PH', 'FF')
    word = word.replace('SCH', 'SSS')
    word = word.replace('TIO', 'SIO')
    word = word.replace('TIA', 'SIO')
    word = word.replace('TCH', 'CHH')

    sdx = word.translate(_fuzzy_soundex_translation)
    sdx = sdx.replace('-', '')

    # remove repeating characters
    sdx = _delete_consecutive_repeats(sdx)

    if word[0] in {'H', 'W', 'Y'}:
        sdx = word[0] + sdx
    else:
        sdx = word[0] + sdx[1:]

    sdx = sdx.replace('0', '')

    if zero_pad:
        sdx += ('0'*max_length)

    return sdx[:max_length]


def phonex(word, max_length=4, zero_pad=True):
    """Return the Phonex code for a word.

    Phonex is an algorithm derived from Soundex, defined in :cite:`Lait:1996`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool zero_pad: pad the end of the return value with 0s to achieve
        a max_length string
    :returns: the Phonex value
    :rtype: str

    >>> phonex('Christopher')
    'C623'
    >>> phonex('Niall')
    'N400'
    >>> phonex('Schmidt')
    'S253'
    >>> phonex('Smith')
    'S530'
    """
    name = unicode_normalize('NFKD', text_type(word.upper()))
    name = name.replace('ß', 'SS')

    # Clamp max_length to [4, 64]
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    name_code = last = ''

    # Deletions effected by replacing with next letter which
    # will be ignored due to duplicate handling of Soundex code.
    # This is faster than 'moving' all subsequent letters.

    # Remove any trailing Ss
    while name[-1:] == 'S':
        name = name[:-1]

    # Phonetic equivalents of first 2 characters
    # Works since duplicate letters are ignored
    if name[:2] == 'KN':
        name = 'N' + name[2:]  # KN.. == N..
    elif name[:2] == 'PH':
        name = 'F' + name[2:]  # PH.. == F.. (H ignored anyway)
    elif name[:2] == 'WR':
        name = 'R' + name[2:]  # WR.. == R..

    if name:
        # Special case, ignore H first letter (subsequent Hs ignored anyway)
        # Works since duplicate letters are ignored
        if name[0] == 'H':
            name = name[1:]

    if name:
        # Phonetic equivalents of first character
        if name[0] in {'A', 'E', 'I', 'O', 'U', 'Y'}:
            name = 'A' + name[1:]
        elif name[0] in {'B', 'P'}:
            name = 'B' + name[1:]
        elif name[0] in {'V', 'F'}:
            name = 'F' + name[1:]
        elif name[0] in {'C', 'K', 'Q'}:
            name = 'C' + name[1:]
        elif name[0] in {'G', 'J'}:
            name = 'G' + name[1:]
        elif name[0] in {'S', 'Z'}:
            name = 'S' + name[1:]

        name_code = last = name[0]

    # Modified Soundex code
    for i in range(1, len(name)):
        code = '0'
        if name[i] in {'B', 'F', 'P', 'V'}:
            code = '1'
        elif name[i] in {'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z'}:
            code = '2'
        elif name[i] in {'D', 'T'}:
            if name[i+1:i+2] != 'C':
                code = '3'
        elif name[i] == 'L':
            if (name[i+1:i+2] in {'A', 'E', 'I', 'O', 'U', 'Y'} or
                    i+1 == len(name)):
                code = '4'
        elif name[i] in {'M', 'N'}:
            if name[i+1:i+2] in {'D', 'G'}:
                name = name[:i+1] + name[i] + name[i+2:]
            code = '5'
        elif name[i] == 'R':
            if (name[i+1:i+2] in {'A', 'E', 'I', 'O', 'U', 'Y'} or
                    i+1 == len(name)):
                code = '6'

        if code != last and code != '0' and i != 0:
            name_code += code

        last = name_code[-1]

    if zero_pad:
        name_code += '0' * max_length
    if not name_code:
        name_code = '0'
    return name_code[:max_length]


def phonem(word):
    """Return the Phonem code for a word.

    Phonem is defined in :cite:`Wilde:1988`.

    This version is based on the Perl implementation documented at
    :cite:`Wilz:2005`.
    It includes some enhancements presented in the Java port at
    :cite:`dcm4che:2011`.

    Phonem is intended chiefly for German names/words.

    :param str word: the word to transform
    :returns: the Phonem value
    :rtype: str

    >>> phonem('Christopher')
    'CRYSDOVR'
    >>> phonem('Niall')
    'NYAL'
    >>> phonem('Smith')
    'SMYD'
    >>> phonem('Schmidt')
    'CMYD'
    """
    _phonem_substitutions = (('SC', 'C'), ('SZ', 'C'), ('CZ', 'C'),
                             ('TZ', 'C'), ('TS', 'C'), ('KS', 'X'),
                             ('PF', 'V'), ('QU', 'KW'), ('PH', 'V'),
                             ('UE', 'Y'), ('AE', 'E'), ('OE', 'Ö'),
                             ('EI', 'AY'), ('EY', 'AY'), ('EU', 'OY'),
                             ('AU', 'A§'), ('OU', '§'))
    _phonem_translation = dict(zip((ord(_) for _ in
                                    'ZKGQÇÑßFWPTÁÀÂÃÅÄÆÉÈÊËIJÌÍÎÏÜÝ§ÚÙÛÔÒÓÕØ'),
                                   'CCCCCNSVVBDAAAAAEEEEEEYYYYYYYYUUUUOOOOÖ'))

    word = unicode_normalize('NFC', text_type(word.upper()))
    for i, j in _phonem_substitutions:
        word = word.replace(i, j)
    word = word.translate(_phonem_translation)

    return ''.join(c for c in _delete_consecutive_repeats(word)
                   if c in {'A', 'B', 'C', 'D', 'L', 'M', 'N', 'O', 'R', 'S',
                            'U', 'V', 'W', 'X', 'Y', 'Ö'})


def phonix(word, max_length=4, zero_pad=True):
    """Return the Phonix code for a word.

    Phonix is a Soundex-like algorithm defined in :cite:`Gadd:1990`.

    This implementation is based on:
    - :cite:`Pfeifer:2000`
    - :cite:`Christen:2011`
    - :cite:`Kollar:2007`

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool zero_pad: pad the end of the return value with 0s to achieve
        a max_length string
    :returns: the Phonix value
    :rtype: str

    >>> phonix('Christopher')
    'K683'
    >>> phonix('Niall')
    'N400'
    >>> phonix('Smith')
    'S530'
    >>> phonix('Schmidt')
    'S530'
    """
    def _start_repl(word, src, tar, post=None):
        r"""Replace src with tar at the start of word."""
        if post:
            for i in post:
                if word.startswith(src+i):
                    return tar + word[len(src):]
        elif word.startswith(src):
            return tar + word[len(src):]
        return word

    def _end_repl(word, src, tar, pre=None):
        r"""Replace src with tar at the end of word."""
        if pre:
            for i in pre:
                if word.endswith(i+src):
                    return word[:-len(src)] + tar
        elif word.endswith(src):
            return word[:-len(src)] + tar
        return word

    def _mid_repl(word, src, tar, pre=None, post=None):
        r"""Replace src with tar in the middle of word."""
        if pre or post:
            if not pre:
                return word[0] + _all_repl(word[1:], src, tar, pre, post)
            elif not post:
                return (_all_repl(word[:-1], src, tar, pre, post) +
                        word[-1])
            return _all_repl(word, src, tar, pre, post)
        return (word[0] +
                _all_repl(word[1:-1], src, tar, pre, post) +
                word[-1])

    def _all_repl(word, src, tar, pre=None, post=None):
        r"""Replace src with tar anywhere in word."""
        if pre or post:
            if post:
                post = post
            else:
                post = frozenset(('',))
            if pre:
                pre = pre
            else:
                pre = frozenset(('',))

            for i, j in ((i, j) for i in pre for j in post):
                word = word.replace(i+src+j, i+tar+j)
            return word
        else:
            return word.replace(src, tar)

    _vow = {'A', 'E', 'I', 'O', 'U'}
    _con = {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q',
            'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}

    _phonix_substitutions = ((_all_repl, 'DG', 'G'),
                             (_all_repl, 'CO', 'KO'),
                             (_all_repl, 'CA', 'KA'),
                             (_all_repl, 'CU', 'KU'),
                             (_all_repl, 'CY', 'SI'),
                             (_all_repl, 'CI', 'SI'),
                             (_all_repl, 'CE', 'SE'),
                             (_start_repl, 'CL', 'KL', _vow),
                             (_all_repl, 'CK', 'K'),
                             (_end_repl, 'GC', 'K'),
                             (_end_repl, 'JC', 'K'),
                             (_start_repl, 'CHR', 'KR', _vow),
                             (_start_repl, 'CR', 'KR', _vow),
                             (_start_repl, 'WR', 'R'),
                             (_all_repl, 'NC', 'NK'),
                             (_all_repl, 'CT', 'KT'),
                             (_all_repl, 'PH', 'F'),
                             (_all_repl, 'AA', 'AR'),
                             (_all_repl, 'SCH', 'SH'),
                             (_all_repl, 'BTL', 'TL'),
                             (_all_repl, 'GHT', 'T'),
                             (_all_repl, 'AUGH', 'ARF'),
                             (_mid_repl, 'LJ', 'LD', _vow, _vow),
                             (_all_repl, 'LOUGH', 'LOW'),
                             (_start_repl, 'Q', 'KW'),
                             (_start_repl, 'KN', 'N'),
                             (_end_repl, 'GN', 'N'),
                             (_all_repl, 'GHN', 'N'),
                             (_end_repl, 'GNE', 'N'),
                             (_all_repl, 'GHNE', 'NE'),
                             (_end_repl, 'GNES', 'NS'),
                             (_start_repl, 'GN', 'N'),
                             (_mid_repl, 'GN', 'N', None, _con),
                             (_end_repl, 'GN', 'N'),
                             (_start_repl, 'PS', 'S'),
                             (_start_repl, 'PT', 'T'),
                             (_start_repl, 'CZ', 'C'),
                             (_mid_repl, 'WZ', 'Z', _vow),
                             (_mid_repl, 'CZ', 'CH'),
                             (_all_repl, 'LZ', 'LSH'),
                             (_all_repl, 'RZ', 'RSH'),
                             (_mid_repl, 'Z', 'S', None, _vow),
                             (_all_repl, 'ZZ', 'TS'),
                             (_mid_repl, 'Z', 'TS', _con),
                             (_all_repl, 'HROUG', 'REW'),
                             (_all_repl, 'OUGH', 'OF'),
                             (_mid_repl, 'Q', 'KW', _vow, _vow),
                             (_mid_repl, 'J', 'Y', _vow, _vow),
                             (_start_repl, 'YJ', 'Y', _vow),
                             (_start_repl, 'GH', 'G'),
                             (_end_repl, 'GH', 'E', _vow),
                             (_start_repl, 'CY', 'S'),
                             (_all_repl, 'NX', 'NKS'),
                             (_start_repl, 'PF', 'F'),
                             (_end_repl, 'DT', 'T'),
                             (_end_repl, 'TL', 'TIL'),
                             (_end_repl, 'DL', 'DIL'),
                             (_all_repl, 'YTH', 'ITH'),
                             (_start_repl, 'TJ', 'CH', _vow),
                             (_start_repl, 'TSJ', 'CH', _vow),
                             (_start_repl, 'TS', 'T', _vow),
                             (_all_repl, 'TCH', 'CH'),
                             (_mid_repl, 'WSK', 'VSKIE', _vow),
                             (_end_repl, 'WSK', 'VSKIE', _vow),
                             (_start_repl, 'MN', 'N', _vow),
                             (_start_repl, 'PN', 'N', _vow),
                             (_mid_repl, 'STL', 'SL', _vow),
                             (_end_repl, 'STL', 'SL', _vow),
                             (_end_repl, 'TNT', 'ENT'),
                             (_end_repl, 'EAUX', 'OH'),
                             (_all_repl, 'EXCI', 'ECS'),
                             (_all_repl, 'X', 'ECS'),
                             (_end_repl, 'NED', 'ND'),
                             (_all_repl, 'JR', 'DR'),
                             (_end_repl, 'EE', 'EA'),
                             (_all_repl, 'ZS', 'S'),
                             (_mid_repl, 'R', 'AH', _vow, _con),
                             (_end_repl, 'R', 'AH', _vow),
                             (_mid_repl, 'HR', 'AH', _vow, _con),
                             (_end_repl, 'HR', 'AH', _vow),
                             (_end_repl, 'HR', 'AH', _vow),
                             (_end_repl, 'RE', 'AR'),
                             (_end_repl, 'R', 'AH', _vow),
                             (_all_repl, 'LLE', 'LE'),
                             (_end_repl, 'LE', 'ILE', _con),
                             (_end_repl, 'LES', 'ILES', _con),
                             (_end_repl, 'E', ''),
                             (_end_repl, 'ES', 'S'),
                             (_end_repl, 'SS', 'AS', _vow),
                             (_end_repl, 'MB', 'M', _vow),
                             (_all_repl, 'MPTS', 'MPS'),
                             (_all_repl, 'MPS', 'MS'),
                             (_all_repl, 'MPT', 'MT'))

    _phonix_translation = dict(zip((ord(_) for _ in
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                   '01230720022455012683070808'))

    sdx = ''

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})
    if word:
        for trans in _phonix_substitutions:
            word = trans[0](word, *trans[1:])
        if word[0] in {'A', 'E', 'I', 'O', 'U', 'Y'}:
            sdx = 'v' + word[1:].translate(_phonix_translation)
        else:
            sdx = word[0] + word[1:].translate(_phonix_translation)
        sdx = _delete_consecutive_repeats(sdx)
        sdx = sdx.replace('0', '')

    # Clamp max_length to [4, 64]
    if max_length != -1:
        max_length = min(max(4, max_length), 64)
    else:
        max_length = 64

    if zero_pad:
        sdx += '0' * max_length
    if not sdx:
        sdx = '0'
    return sdx[:max_length]


def sfinxbis(word, max_length=-1):
    """Return the SfinxBis code for a word.

    SfinxBis is a Soundex-like algorithm defined in :cite:`Axelsson:2009`.

    This implementation follows the reference implementation:
    :cite:`Sjoo:2009`.

    SfinxBis is intended chiefly for Swedish names.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to
        unlimited)
    :returns: the SfinxBis value
    :rtype: tuple

    >>> sfinxbis('Christopher')
    ('K68376',)
    >>> sfinxbis('Niall')
    ('N4',)
    >>> sfinxbis('Smith')
    ('S53',)
    >>> sfinxbis('Schmidt')
    ('S53',)

    >>> sfinxbis('Johansson')
    ('J585',)
    >>> sfinxbis('Sjöberg')
    ('#162',)
    """
    adelstitler = (' DE LA ', ' DE LAS ', ' DE LOS ', ' VAN DE ', ' VAN DEN ',
                   ' VAN DER ', ' VON DEM ', ' VON DER ',
                   ' AF ', ' AV ', ' DA ', ' DE ', ' DEL ', ' DEN ', ' DES ',
                   ' DI ', ' DO ', ' DON ', ' DOS ', ' DU ', ' E ', ' IN ',
                   ' LA ', ' LE ', ' MAC ', ' MC ', ' VAN ', ' VON ', ' Y ',
                   ' S:T ')

    _harde_vokaler = {'A', 'O', 'U', 'Å'}
    _mjuka_vokaler = {'E', 'I', 'Y', 'Ä', 'Ö'}
    _konsonanter = {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
                    'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z'}
    _alfabet = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z', 'Ä', 'Å', 'Ö'}

    _sfinxbis_translation = dict(zip((ord(_) for _ in
                                      'BCDFGHJKLMNPQRSTVZAOUÅEIYÄÖ'),
                                     '123729224551268378999999999'))

    _sfinxbis_substitutions = dict(zip((ord(_) for _ in
                                        'WZÀÁÂÃÆÇÈÉÊËÌÍÎÏÑÒÓÔÕØÙÚÛÜÝ'),
                                       'VSAAAAÄCEEEEIIIINOOOOÖUUUYY'))

    def _foersvensker(lokal_ordet):
        """Return the Swedish-ized form of the word."""
        lokal_ordet = lokal_ordet.replace('STIERN', 'STJÄRN')
        lokal_ordet = lokal_ordet.replace('HIE', 'HJ')
        lokal_ordet = lokal_ordet.replace('SIÖ', 'SJÖ')
        lokal_ordet = lokal_ordet.replace('SCH', 'SH')
        lokal_ordet = lokal_ordet.replace('QU', 'KV')
        lokal_ordet = lokal_ordet.replace('IO', 'JO')
        lokal_ordet = lokal_ordet.replace('PH', 'F')

        for i in _harde_vokaler:
            lokal_ordet = lokal_ordet.replace(i+'Ü', i+'J')
            lokal_ordet = lokal_ordet.replace(i+'Y', i+'J')
            lokal_ordet = lokal_ordet.replace(i+'I', i+'J')
        for i in _mjuka_vokaler:
            lokal_ordet = lokal_ordet.replace(i+'Ü', i+'J')
            lokal_ordet = lokal_ordet.replace(i+'Y', i+'J')
            lokal_ordet = lokal_ordet.replace(i+'I', i+'J')

        if 'H' in lokal_ordet:
            for i in _konsonanter:
                lokal_ordet = lokal_ordet.replace('H'+i, i)

        lokal_ordet = lokal_ordet.translate(_sfinxbis_substitutions)

        lokal_ordet = lokal_ordet.replace('Ð', 'ETH')
        lokal_ordet = lokal_ordet.replace('Þ', 'TH')
        lokal_ordet = lokal_ordet.replace('ß', 'SS')

        return lokal_ordet

    def _koda_foersta_ljudet(lokal_ordet):
        """Return the word with the first sound coded."""
        if (lokal_ordet[0:1] in _mjuka_vokaler or
                lokal_ordet[0:1] in _harde_vokaler):
            lokal_ordet = '$' + lokal_ordet[1:]
        elif lokal_ordet[0:2] in ('DJ', 'GJ', 'HJ', 'LJ'):
            lokal_ordet = 'J' + lokal_ordet[2:]
        elif lokal_ordet[0:1] == 'G' and lokal_ordet[1:2] in _mjuka_vokaler:
            lokal_ordet = 'J' + lokal_ordet[1:]
        elif lokal_ordet[0:1] == 'Q':
            lokal_ordet = 'K' + lokal_ordet[1:]
        elif (lokal_ordet[0:2] == 'CH' and
              lokal_ordet[2:3] in frozenset(_mjuka_vokaler | _harde_vokaler)):
            lokal_ordet = '#' + lokal_ordet[2:]
        elif lokal_ordet[0:1] == 'C' and lokal_ordet[1:2] in _harde_vokaler:
            lokal_ordet = 'K' + lokal_ordet[1:]
        elif lokal_ordet[0:1] == 'C' and lokal_ordet[1:2] in _konsonanter:
            lokal_ordet = 'K' + lokal_ordet[1:]
        elif lokal_ordet[0:1] == 'X':
            lokal_ordet = 'S' + lokal_ordet[1:]
        elif lokal_ordet[0:1] == 'C' and lokal_ordet[1:2] in _mjuka_vokaler:
            lokal_ordet = 'S' + lokal_ordet[1:]
        elif lokal_ordet[0:3] in ('SKJ', 'STJ', 'SCH'):
            lokal_ordet = '#' + lokal_ordet[3:]
        elif lokal_ordet[0:2] in ('SH', 'KJ', 'TJ', 'SJ'):
            lokal_ordet = '#' + lokal_ordet[2:]
        elif lokal_ordet[0:2] == 'SK' and lokal_ordet[2:3] in _mjuka_vokaler:
            lokal_ordet = '#' + lokal_ordet[2:]
        elif lokal_ordet[0:1] == 'K' and lokal_ordet[1:2] in _mjuka_vokaler:
            lokal_ordet = '#' + lokal_ordet[1:]
        return lokal_ordet

    # Steg 1, Versaler
    word = unicode_normalize('NFC', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = word.replace('-', ' ')

    # Steg 2, Ta bort adelsprefix
    for adelstitel in adelstitler:
        while adelstitel in word:
            word = word.replace(adelstitel, ' ')
        if word.startswith(adelstitel[1:]):
            word = word[len(adelstitel)-1:]

    # Split word into tokens
    ordlista = word.split()

    # Steg 3, Ta bort dubbelteckning i början på namnet
    ordlista = [_delete_consecutive_repeats(ordet) for ordet in ordlista]
    if not ordlista:
        # noinspection PyRedundantParentheses
        return ('',)

    # Steg 4, Försvenskning
    ordlista = [_foersvensker(ordet) for ordet in ordlista]

    # Steg 5, Ta bort alla tecken som inte är A-Ö (65-90,196,197,214)
    ordlista = [''.join(c for c in ordet if c in _alfabet)
                for ordet in ordlista]

    # Steg 6, Koda första ljudet
    ordlista = [_koda_foersta_ljudet(ordet) for ordet in ordlista]

    # Steg 7, Dela upp namnet i två delar
    rest = [ordet[1:] for ordet in ordlista]

    # Steg 8, Utför fonetisk transformation i resten
    rest = [ordet.replace('DT', 'T') for ordet in rest]
    rest = [ordet.replace('X', 'KS') for ordet in rest]

    # Steg 9, Koda resten till en sifferkod
    for vokal in _mjuka_vokaler:
        rest = [ordet.replace('C'+vokal, '8'+vokal) for ordet in rest]
    rest = [ordet.translate(_sfinxbis_translation) for ordet in rest]

    # Steg 10, Ta bort intilliggande dubbletter
    rest = [_delete_consecutive_repeats(ordet) for ordet in rest]

    # Steg 11, Ta bort alla "9"
    rest = [ordet.replace('9', '') for ordet in rest]

    # Steg 12, Sätt ihop delarna igen
    ordlista = [''.join(ordet) for ordet in
                zip((_[0:1] for _ in ordlista), rest)]

    # truncate, if max_length is set
    if max_length > 0:
        ordlista = [ordet[:max_length] for ordet in ordlista]

    return tuple(ordlista)


def phonet(word, mode=1, lang='de'):
    """Return the phonet code for a word.

    phonet ("Hannoveraner Phonetik") was developed by Jörg Michael and
    documented in :cite:`Michael:1999`.

    This is a port of Jesper Zedlitz's code, which is licensed LGPL
    :cite:`Zedlitz:2015`.

    That is, in turn, based on Michael's C code, which is also licensed LGPL
    :cite:`Michael:2007`.

    :param str word: the word to transform
    :param int mode: the ponet variant to employ (1 or 2)
    :param str lang: 'de' (default) for German
            'none' for no language
    :returns: the phonet value
    :rtype: str

    >>> phonet('Christopher')
    'KRISTOFA'
    >>> phonet('Niall')
    'NIAL'
    >>> phonet('Smith')
    'SMIT'
    >>> phonet('Schmidt')
    'SHMIT'

    >>> phonet('Christopher', mode=2)
    'KRIZTUFA'
    >>> phonet('Niall', mode=2)
    'NIAL'
    >>> phonet('Smith', mode=2)
    'ZNIT'
    >>> phonet('Schmidt', mode=2)
    'ZNIT'

    >>> phonet('Christopher', lang='none')
    'CHRISTOPHER'
    >>> phonet('Niall', lang='none')
    'NIAL'
    >>> phonet('Smith', lang='none')
    'SMITH'
    >>> phonet('Schmidt', lang='none')
    'SCHMIDT'
    """
    _phonet_rules_no_lang = (  # separator chars
        '´', ' ', ' ',
        '"', ' ', ' ',
        '`$', '', '',
        '\'', ' ', ' ',
        ',', ',', ',',
        ';', ',', ',',
        '-', ' ', ' ',
        ' ', ' ', ' ',
        '.', '.', '.',
        ':', '.', '.',
        # German umlauts
        'Ä', 'AE', 'AE',
        'Ö', 'OE', 'OE',
        'Ü', 'UE', 'UE',
        'ß', 'S', 'S',
        # international umlauts
        'À', 'A', 'A',
        'Á', 'A', 'A',
        'Â', 'A', 'A',
        'Ã', 'A', 'A',
        'Å', 'A', 'A',
        'Æ', 'AE', 'AE',
        'Ç', 'C', 'C',
        'Ð', 'DJ', 'DJ',
        'È', 'E', 'E',
        'É', 'E', 'E',
        'Ê', 'E', 'E',
        'Ë', 'E', 'E',
        'Ì', 'I', 'I',
        'Í', 'I', 'I',
        'Î', 'I', 'I',
        'Ï', 'I', 'I',
        'Ñ', 'NH', 'NH',
        'Ò', 'O', 'O',
        'Ó', 'O', 'O',
        'Ô', 'O', 'O',
        'Õ', 'O', 'O',
        'Œ', 'OE', 'OE',
        'Ø', 'OE', 'OE',
        'Š', 'SH', 'SH',
        'Þ', 'TH', 'TH',
        'Ù', 'U', 'U',
        'Ú', 'U', 'U',
        'Û', 'U', 'U',
        'Ý', 'Y', 'Y',
        'Ÿ', 'Y', 'Y',
        # 'normal' letters (A-Z)
        'MC^', 'MAC', 'MAC',
        'MC^', 'MAC', 'MAC',
        'M´^', 'MAC', 'MAC',
        'M\'^', 'MAC', 'MAC',
        'O´^', 'O', 'O',
        'O\'^', 'O', 'O',
        'VAN DEN ^', 'VANDEN', 'VANDEN',
        None, None, None)

    _phonet_rules_german = (  # separator chars
        '´', ' ', ' ',
        '"', ' ', ' ',
        '`$', '', '',
        '\'', ' ', ' ',
        ',', ' ', ' ',
        ';', ' ', ' ',
        '-', ' ', ' ',
        ' ', ' ', ' ',
        '.', '.', '.',
        ':', '.', '.',
        # German umlauts
        'ÄE', 'E', 'E',
        'ÄU<', 'EU', 'EU',
        'ÄV(AEOU)-<', 'EW', None,
        'Ä$', 'Ä', None,
        'Ä<', None, 'E',
        'Ä', 'E', None,
        'ÖE', 'Ö', 'Ö',
        'ÖU', 'Ö', 'Ö',
        'ÖVER--<', 'ÖW', None,
        'ÖV(AOU)-', 'ÖW', None,
        'ÜBEL(GNRW)-^^', 'ÜBL ', 'IBL ',
        'ÜBER^^', 'ÜBA', 'IBA',
        'ÜE', 'Ü', 'I',
        'ÜVER--<', 'ÜW', None,
        'ÜV(AOU)-', 'ÜW', None,
        'Ü', None, 'I',
        'ßCH<', None, 'Z',
        'ß<', 'S', 'Z',
        # international umlauts
        'À<', 'A', 'A',
        'Á<', 'A', 'A',
        'Â<', 'A', 'A',
        'Ã<', 'A', 'A',
        'Å<', 'A', 'A',
        'ÆER-', 'E', 'E',
        'ÆU<', 'EU', 'EU',
        'ÆV(AEOU)-<', 'EW', None,
        'Æ$', 'Ä', None,
        'Æ<', None, 'E',
        'Æ', 'E', None,
        'Ç', 'Z', 'Z',
        'ÐÐ-', '', '',
        'Ð', 'DI', 'TI',
        'È<', 'E', 'E',
        'É<', 'E', 'E',
        'Ê<', 'E', 'E',
        'Ë', 'E', 'E',
        'Ì<', 'I', 'I',
        'Í<', 'I', 'I',
        'Î<', 'I', 'I',
        'Ï', 'I', 'I',
        'ÑÑ-', '', '',
        'Ñ', 'NI', 'NI',
        'Ò<', 'O', 'U',
        'Ó<', 'O', 'U',
        'Ô<', 'O', 'U',
        'Õ<', 'O', 'U',
        'Œ<', 'Ö', 'Ö',
        'Ø(IJY)-<', 'E', 'E',
        'Ø<', 'Ö', 'Ö',
        'Š', 'SH', 'Z',
        'Þ', 'T', 'T',
        'Ù<', 'U', 'U',
        'Ú<', 'U', 'U',
        'Û<', 'U', 'U',
        'Ý<', 'I', 'I',
        'Ÿ<', 'I', 'I',
        # 'normal' letters (A-Z)
        'ABELLE$', 'ABL', 'ABL',
        'ABELL$', 'ABL', 'ABL',
        'ABIENNE$', 'ABIN', 'ABIN',
        'ACHME---^', 'ACH', 'AK',
        'ACEY$', 'AZI', 'AZI',
        'ADV', 'ATW', None,
        'AEGL-', 'EK', None,
        'AEU<', 'EU', 'EU',
        'AE2', 'E', 'E',
        'AFTRAUBEN------', 'AFT ', 'AFT ',
        'AGL-1', 'AK', None,
        'AGNI-^', 'AKN', 'AKN',
        'AGNIE-', 'ANI', 'ANI',
        'AGN(AEOU)-$', 'ANI', 'ANI',
        'AH(AIOÖUÜY)-', 'AH', None,
        'AIA2', 'AIA', 'AIA',
        'AIE$', 'E', 'E',
        'AILL(EOU)-', 'ALI', 'ALI',
        'AINE$', 'EN', 'EN',
        'AIRE$', 'ER', 'ER',
        'AIR-', 'E', 'E',
        'AISE$', 'ES', 'EZ',
        'AISSANCE$', 'ESANS', 'EZANZ',
        'AISSE$', 'ES', 'EZ',
        'AIX$', 'EX', 'EX',
        'AJ(AÄEÈÉÊIOÖUÜ)--', 'A', 'A',
        'AKTIE', 'AXIE', 'AXIE',
        'AKTUEL', 'AKTUEL', None,
        'ALOI^', 'ALOI', 'ALUI',  # Don't merge these rules
        'ALOY^', 'ALOI', 'ALUI',  # needed by 'check_rules'
        'AMATEU(RS)-', 'AMATÖ', 'ANATÖ',
        'ANCH(OEI)-', 'ANSH', 'ANZ',
        'ANDERGEGANG----', 'ANDA GE', 'ANTA KE',
        'ANDERGEHE----', 'ANDA ', 'ANTA ',
        'ANDERGESETZ----', 'ANDA GE', 'ANTA KE',
        'ANDERGING----', 'ANDA ', 'ANTA ',
        'ANDERSETZ(ET)-----', 'ANDA ', 'ANTA ',
        'ANDERZUGEHE----', 'ANDA ZU ', 'ANTA ZU ',
        'ANDERZUSETZE-----', 'ANDA ZU ', 'ANTA ZU ',
        'ANER(BKO)---^^', 'AN', None,
        'ANHAND---^$', 'AN H', 'AN ',
        'ANH(AÄEIOÖUÜY)--^^', 'AN', None,
        'ANIELLE$', 'ANIEL', 'ANIL',
        'ANIEL', 'ANIEL', None,
        'ANSTELLE----^$', 'AN ST', 'AN ZT',
        'ANTI^^', 'ANTI', 'ANTI',
        'ANVER^^', 'ANFA', 'ANFA',
        'ATIA$', 'ATIA', 'ATIA',
        'ATIA(NS)--', 'ATI', 'ATI',
        'ATI(AÄOÖUÜ)-', 'AZI', 'AZI',
        'AUAU--', '', '',
        'AUERE$', 'AUERE', None,
        'AUERE(NS)-$', 'AUERE', None,
        'AUERE(AIOUY)--', 'AUER', None,
        'AUER(AÄIOÖUÜY)-', 'AUER', None,
        'AUER<', 'AUA', 'AUA',
        'AUF^^', 'AUF', 'AUF',
        'AULT$', 'O', 'U',
        'AUR(BCDFGKLMNQSTVWZ)-', 'AUA', 'AUA',
        'AUR$', 'AUA', 'AUA',
        'AUSSE$', 'OS', 'UZ',
        'AUS(ST)-^', 'AUS', 'AUS',
        'AUS^^', 'AUS', 'AUS',
        'AUTOFAHR----', 'AUTO ', 'AUTU ',
        'AUTO^^', 'AUTO', 'AUTU',
        'AUX(IY)-', 'AUX', 'AUX',
        'AUX', 'O', 'U',
        'AU', 'AU', 'AU',
        'AVER--<', 'AW', None,
        'AVIER$', 'AWIE', 'AFIE',
        'AV(EÈÉÊI)-^', 'AW', None,
        'AV(AOU)-', 'AW', None,
        'AYRE$', 'EIRE', 'EIRE',
        'AYRE(NS)-$', 'EIRE', 'EIRE',
        'AYRE(AIOUY)--', 'EIR', 'EIR',
        'AYR(AÄIOÖUÜY)-', 'EIR', 'EIR',
        'AYR<', 'EIA', 'EIA',
        'AYER--<', 'EI', 'EI',
        'AY(AÄEIOÖUÜY)--', 'A', 'A',
        'AË', 'E', 'E',
        'A(IJY)<', 'EI', 'EI',
        'BABY^$', 'BEBI', 'BEBI',
        'BAB(IY)^', 'BEBI', 'BEBI',
        'BEAU^$', 'BO', None,
        'BEA(BCMNRU)-^', 'BEA', 'BEA',
        'BEAT(AEIMORU)-^', 'BEAT', 'BEAT',
        'BEE$', 'BI', 'BI',
        'BEIGE^$', 'BESH', 'BEZ',
        'BENOIT--', 'BENO', 'BENU',
        'BER(DT)-', 'BER', None,
        'BERN(DT)-', 'BERN', None,
        'BE(LMNRST)-^', 'BE', 'BE',
        'BETTE$', 'BET', 'BET',
        'BEVOR^$', 'BEFOR', None,
        'BIC$', 'BIZ', 'BIZ',
        'BOWL(EI)-', 'BOL', 'BUL',
        'BP(AÄEÈÉÊIÌÍÎOÖRUÜY)-', 'B', 'B',
        'BRINGEND-----^', 'BRI', 'BRI',
        'BRINGEND-----', ' BRI', ' BRI',
        'BROW(NS)-', 'BRAU', 'BRAU',
        'BUDGET7', 'BÜGE', 'BIKE',
        'BUFFET7', 'BÜFE', 'BIFE',
        'BYLLE$', 'BILE', 'BILE',
        'BYLL$', 'BIL', 'BIL',
        'BYPA--^', 'BEI', 'BEI',
        'BYTE<', 'BEIT', 'BEIT',
        'BY9^', 'BÜ', None,
        'B(SßZ)$', 'BS', None,
        'CACH(EI)-^', 'KESH', 'KEZ',
        'CAE--', 'Z', 'Z',
        'CA(IY)$', 'ZEI', 'ZEI',
        'CE(EIJUY)--', 'Z', 'Z',
        'CENT<', 'ZENT', 'ZENT',
        'CERST(EI)----^', 'KE', 'KE',
        'CER$', 'ZA', 'ZA',
        'CE3', 'ZE', 'ZE',
        'CH\'S$', 'X', 'X',
        'CH´S$', 'X', 'X',
        'CHAO(ST)-', 'KAO', 'KAU',
        'CHAMPIO-^', 'SHEMPI', 'ZENBI',
        'CHAR(AI)-^', 'KAR', 'KAR',
        'CHAU(CDFSVWXZ)-', 'SHO', 'ZU',
        'CHÄ(CF)-', 'SHE', 'ZE',
        'CHE(CF)-', 'SHE', 'ZE',
        'CHEM-^', 'KE', 'KE',  # or: 'CHE', 'KE'
        'CHEQUE<', 'SHEK', 'ZEK',
        'CHI(CFGPVW)-', 'SHI', 'ZI',
        'CH(AEUY)-<^', 'SH', 'Z',
        'CHK-', '', '',
        'CHO(CKPS)-^', 'SHO', 'ZU',
        'CHRIS-', 'KRI', None,
        'CHRO-', 'KR', None,
        'CH(LOR)-<^', 'K', 'K',
        'CHST-', 'X', 'X',
        'CH(SßXZ)3', 'X', 'X',
        'CHTNI-3', 'CHN', 'KN',
        'CH^', 'K', 'K',  # or: 'CH', 'K'
        'CH', 'CH', 'K',
        'CIC$', 'ZIZ', 'ZIZ',
        'CIENCEFICT----', 'EIENS ', 'EIENZ ',
        'CIENCE$', 'EIENS', 'EIENZ',
        'CIER$', 'ZIE', 'ZIE',
        'CYB-^', 'ZEI', 'ZEI',
        'CY9^', 'ZÜ', 'ZI',
        'C(IJY)-<3', 'Z', 'Z',
        'CLOWN-', 'KLAU', 'KLAU',
        'CCH', 'Z', 'Z',
        'CCE-', 'X', 'X',
        'C(CK)-', '', '',
        'CLAUDET---', 'KLO', 'KLU',
        'CLAUDINE^$', 'KLODIN', 'KLUTIN',
        'COACH', 'KOSH', 'KUZ',
        'COLE$', 'KOL', 'KUL',
        'COUCH', 'KAUSH', 'KAUZ',
        'COW', 'KAU', 'KAU',
        'CQUES$', 'K', 'K',
        'CQUE', 'K', 'K',
        'CRASH--9', 'KRE', 'KRE',
        'CREAT-^', 'KREA', 'KREA',
        'CST', 'XT', 'XT',
        'CS<^', 'Z', 'Z',
        'C(SßX)', 'X', 'X',
        'CT\'S$', 'X', 'X',
        'CT(SßXZ)', 'X', 'X',
        'CZ<', 'Z', 'Z',
        'C(ÈÉÊÌÍÎÝ)3', 'Z', 'Z',
        'C.^', 'C.', 'C.',
        'CÄ-', 'Z', 'Z',
        'CÜ$', 'ZÜ', 'ZI',
        'C\'S$', 'X', 'X',
        'C<', 'K', 'K',
        'DAHER^$', 'DAHER', None,
        'DARAUFFOLGE-----', 'DARAUF ', 'TARAUF ',
        'DAVO(NR)-^$', 'DAFO', 'TAFU',
        'DD(SZ)--<', '', '',
        'DD9', 'D', None,
        'DEPOT7', 'DEPO', 'TEBU',
        'DESIGN', 'DISEIN', 'TIZEIN',
        'DE(LMNRST)-3^', 'DE', 'TE',
        'DETTE$', 'DET', 'TET',
        'DH$', 'T', None,
        'DIC$', 'DIZ', 'TIZ',
        'DIDR-^', 'DIT', None,
        'DIEDR-^', 'DIT', None,
        'DJ(AEIOU)-^', 'I', 'I',
        'DMITR-^', 'DIMIT', 'TINIT',
        'DRY9^', 'DRÜ', None,
        'DT-', '', '',
        'DUIS-^', 'DÜ', 'TI',
        'DURCH^^', 'DURCH', 'TURK',
        'DVA$', 'TWA', None,
        'DY9^', 'DÜ', None,
        'DYS$', 'DIS', None,
        'DS(CH)--<', 'T', 'T',
        'DST', 'ZT', 'ZT',
        'DZS(CH)--', 'T', 'T',
        'D(SßZ)', 'Z', 'Z',
        'D(AÄEIOÖRUÜY)-', 'D', None,
        'D(ÀÁÂÃÅÈÉÊÌÍÎÙÚÛ)-', 'D', None,
        'D\'H^', 'D', 'T',
        'D´H^', 'D', 'T',
        'D`H^', 'D', 'T',
        'D\'S3$', 'Z', 'Z',
        'D´S3$', 'Z', 'Z',
        'D^', 'D', None,
        'D', 'T', 'T',
        'EAULT$', 'O', 'U',
        'EAUX$', 'O', 'U',
        'EAU', 'O', 'U',
        'EAV', 'IW', 'IF',
        'EAS3$', 'EAS', None,
        'EA(AÄEIOÖÜY)-3', 'EA', 'EA',
        'EA3$', 'EA', 'EA',
        'EA3', 'I', 'I',
        'EBENSO^$', 'EBNSO', 'EBNZU',
        'EBENSO^^', 'EBNSO ', 'EBNZU ',
        'EBEN^^', 'EBN', 'EBN',
        'EE9', 'E', 'E',
        'EGL-1', 'EK', None,
        'EHE(IUY)--1', 'EH', None,
        'EHUNG---1', 'E', None,
        'EH(AÄIOÖUÜY)-1', 'EH', None,
        'EIEI--', '', '',
        'EIERE^$', 'EIERE', None,
        'EIERE$', 'EIERE', None,
        'EIERE(NS)-$', 'EIERE', None,
        'EIERE(AIOUY)--', 'EIER', None,
        'EIER(AÄIOÖUÜY)-', 'EIER', None,
        'EIER<', 'EIA', None,
        'EIGL-1', 'EIK', None,
        'EIGH$', 'EI', 'EI',
        'EIH--', 'E', 'E',
        'EILLE$', 'EI', 'EI',
        'EIR(BCDFGKLMNQSTVWZ)-', 'EIA', 'EIA',
        'EIR$', 'EIA', 'EIA',
        'EITRAUBEN------', 'EIT ', 'EIT ',
        'EI', 'EI', 'EI',
        'EJ$', 'EI', 'EI',
        'ELIZ^', 'ELIS', None,
        'ELZ^', 'ELS', None,
        'EL-^', 'E', 'E',
        'ELANG----1', 'E', 'E',
        'EL(DKL)--1', 'E', 'E',
        'EL(MNT)--1$', 'E', 'E',
        'ELYNE$', 'ELINE', 'ELINE',
        'ELYN$', 'ELIN', 'ELIN',
        'EL(AÄEÈÉÊIÌÍÎOÖUÜY)-1', 'EL', 'EL',
        'EL-1', 'L', 'L',
        'EM-^', None, 'E',
        'EM(DFKMPQT)--1', None, 'E',
        'EM(AÄEÈÉÊIÌÍÎOÖUÜY)--1', None, 'E',
        'EM-1', None, 'N',
        'ENGAG-^', 'ANGA', 'ANKA',
        'EN-^', 'E', 'E',
        'ENTUEL', 'ENTUEL', None,
        'EN(CDGKQSTZ)--1', 'E', 'E',
        'EN(AÄEÈÉÊIÌÍÎNOÖUÜY)-1', 'EN', 'EN',
        'EN-1', '', '',
        'ERH(AÄEIOÖUÜ)-^', 'ERH', 'ER',
        'ER-^', 'E', 'E',
        'ERREGEND-----', ' ER', ' ER',
        'ERT1$', 'AT', None,
        'ER(DGLKMNRQTZß)-1', 'ER', None,
        'ER(AÄEÈÉÊIÌÍÎOÖUÜY)-1', 'ER', 'A',
        'ER1$', 'A', 'A',
        'ER<1', 'A', 'A',
        'ETAT7', 'ETA', 'ETA',
        'ETI(AÄOÖÜU)-', 'EZI', 'EZI',
        'EUERE$', 'EUERE', None,
        'EUERE(NS)-$', 'EUERE', None,
        'EUERE(AIOUY)--', 'EUER', None,
        'EUER(AÄIOÖUÜY)-', 'EUER', None,
        'EUER<', 'EUA', None,
        'EUEU--', '', '',
        'EUILLE$', 'Ö', 'Ö',
        'EUR$', 'ÖR', 'ÖR',
        'EUX', 'Ö', 'Ö',
        'EUSZ$', 'EUS', None,
        'EUTZ$', 'EUS', None,
        'EUYS$', 'EUS', 'EUZ',
        'EUZ$', 'EUS', None,
        'EU', 'EU', 'EU',
        'EVER--<1', 'EW', None,
        'EV(ÄOÖUÜ)-1', 'EW', None,
        'EYER<', 'EIA', 'EIA',
        'EY<', 'EI', 'EI',
        'FACETTE', 'FASET', 'FAZET',
        'FANS--^$', 'FE', 'FE',
        'FAN-^$', 'FE', 'FE',
        'FAULT-', 'FOL', 'FUL',
        'FEE(DL)-', 'FI', 'FI',
        'FEHLER', 'FELA', 'FELA',
        'FE(LMNRST)-3^', 'FE', 'FE',
        'FOERDERN---^', 'FÖRD', 'FÖRT',
        'FOERDERN---', ' FÖRD', ' FÖRT',
        'FOND7', 'FON', 'FUN',
        'FRAIN$', 'FRA', 'FRA',
        'FRISEU(RS)-', 'FRISÖ', 'FRIZÖ',
        'FY9^', 'FÜ', None,
        'FÖRDERN---^', 'FÖRD', 'FÖRT',
        'FÖRDERN---', ' FÖRD', ' FÖRT',
        'GAGS^$', 'GEX', 'KEX',
        'GAG^$', 'GEK', 'KEK',
        'GD', 'KT', 'KT',
        'GEGEN^^', 'GEGN', 'KEKN',
        'GEGENGEKOM-----', 'GEGN ', 'KEKN ',
        'GEGENGESET-----', 'GEGN ', 'KEKN ',
        'GEGENKOMME-----', 'GEGN ', 'KEKN ',
        'GEGENZUKOM---', 'GEGN ZU ', 'KEKN ZU ',
        'GENDETWAS-----$', 'GENT ', 'KENT ',
        'GENRE', 'IORE', 'IURE',
        'GE(LMNRST)-3^', 'GE', 'KE',
        'GER(DKT)-', 'GER', None,
        'GETTE$', 'GET', 'KET',
        'GGF.', 'GF.', None,
        'GG-', '', '',
        'GH', 'G', None,
        'GI(AOU)-^', 'I', 'I',
        'GION-3', 'KIO', 'KIU',
        'G(CK)-', '', '',
        'GJ(AEIOU)-^', 'I', 'I',
        'GMBH^$', 'GMBH', 'GMBH',
        'GNAC$', 'NIAK', 'NIAK',
        'GNON$', 'NION', 'NIUN',
        'GN$', 'N', 'N',
        'GONCAL-^', 'GONZA', 'KUNZA',
        'GRY9^', 'GRÜ', None,
        'G(SßXZ)-<', 'K', 'K',
        'GUCK-', 'KU', 'KU',
        'GUISEP-^', 'IUSE', 'IUZE',
        'GUI-^', 'G', 'K',
        'GUTAUSSEH------^', 'GUT ', 'KUT ',
        'GUTGEHEND------^', 'GUT ', 'KUT ',
        'GY9^', 'GÜ', None,
        'G(AÄEILOÖRUÜY)-', 'G', None,
        'G(ÀÁÂÃÅÈÉÊÌÍÎÙÚÛ)-', 'G', None,
        'G\'S$', 'X', 'X',
        'G´S$', 'X', 'X',
        'G^', 'G', None,
        'G', 'K', 'K',
        'HA(HIUY)--1', 'H', None,
        'HANDVOL---^', 'HANT ', 'ANT ',
        'HANNOVE-^', 'HANOF', None,
        'HAVEN7$', 'HAFN', None,
        'HEAD-', 'HE', 'E',
        'HELIEGEN------', 'E ', 'E ',
        'HESTEHEN------', 'E ', 'E ',
        'HE(LMNRST)-3^', 'HE', 'E',
        'HE(LMN)-1', 'E', 'E',
        'HEUR1$', 'ÖR', 'ÖR',
        'HE(HIUY)--1', 'H', None,
        'HIH(AÄEIOÖUÜY)-1', 'IH', None,
        'HLH(AÄEIOÖUÜY)-1', 'LH', None,
        'HMH(AÄEIOÖUÜY)-1', 'MH', None,
        'HNH(AÄEIOÖUÜY)-1', 'NH', None,
        'HOBBY9^', 'HOBI', None,
        'HOCHBEGAB-----^', 'HOCH ', 'UK ',
        'HOCHTALEN-----^', 'HOCH ', 'UK ',
        'HOCHZUFRI-----^', 'HOCH ', 'UK ',
        'HO(HIY)--1', 'H', None,
        'HRH(AÄEIOÖUÜY)-1', 'RH', None,
        'HUH(AÄEIOÖUÜY)-1', 'UH', None,
        'HUIS^^', 'HÜS', 'IZ',
        'HUIS$', 'ÜS', 'IZ',
        'HUI--1', 'H', None,
        'HYGIEN^', 'HÜKIEN', None,
        'HY9^', 'HÜ', None,
        'HY(BDGMNPST)-', 'Ü', None,
        'H.^', None, 'H.',
        'HÄU--1', 'H', None,
        'H^', 'H', '',
        'H', '', '',
        'ICHELL---', 'ISH', 'IZ',
        'ICHI$', 'ISHI', 'IZI',
        'IEC$', 'IZ', 'IZ',
        'IEDENSTELLE------', 'IDN ', 'ITN ',
        'IEI-3', '', '',
        'IELL3', 'IEL', 'IEL',
        'IENNE$', 'IN', 'IN',
        'IERRE$', 'IER', 'IER',
        'IERZULAN---', 'IR ZU ', 'IR ZU ',
        'IETTE$', 'IT', 'IT',
        'IEU', 'IÖ', 'IÖ',
        'IE<4', 'I', 'I',
        'IGL-1', 'IK', None,
        'IGHT3$', 'EIT', 'EIT',
        'IGNI(EO)-', 'INI', 'INI',
        'IGN(AEOU)-$', 'INI', 'INI',
        'IHER(DGLKRT)--1', 'IHE', None,
        'IHE(IUY)--', 'IH', None,
        'IH(AIOÖUÜY)-', 'IH', None,
        'IJ(AOU)-', 'I', 'I',
        'IJ$', 'I', 'I',
        'IJ<', 'EI', 'EI',
        'IKOLE$', 'IKOL', 'IKUL',
        'ILLAN(STZ)--4', 'ILIA', 'ILIA',
        'ILLAR(DT)--4', 'ILIA', 'ILIA',
        'IMSTAN----^', 'IM ', 'IN ',
        'INDELERREGE------', 'INDL ', 'INTL ',
        'INFRAGE-----^$', 'IN ', 'IN ',
        'INTERN(AOU)-^', 'INTAN', 'INTAN',
        'INVER-', 'INWE', 'INFE',
        'ITI(AÄIOÖUÜ)-', 'IZI', 'IZI',
        'IUSZ$', 'IUS', None,
        'IUTZ$', 'IUS', None,
        'IUZ$', 'IUS', None,
        'IVER--<', 'IW', None,
        'IVIER$', 'IWIE', 'IFIE',
        'IV(ÄOÖUÜ)-', 'IW', None,
        'IV<3', 'IW', None,
        'IY2', 'I', None,
        'I(ÈÉÊ)<4', 'I', 'I',
        'JAVIE---<^', 'ZA', 'ZA',
        'JEANS^$', 'JINS', 'INZ',
        'JEANNE^$', 'IAN', 'IAN',
        'JEAN-^', 'IA', 'IA',
        'JER-^', 'IE', 'IE',
        'JE(LMNST)-', 'IE', 'IE',
        'JI^', 'JI', None,
        'JOR(GK)^$', 'IÖRK', 'IÖRK',
        'J', 'I', 'I',
        'KC(ÄEIJ)-', 'X', 'X',
        'KD', 'KT', None,
        'KE(LMNRST)-3^', 'KE', 'KE',
        'KG(AÄEILOÖRUÜY)-', 'K', None,
        'KH<^', 'K', 'K',
        'KIC$', 'KIZ', 'KIZ',
        'KLE(LMNRST)-3^', 'KLE', 'KLE',
        'KOTELE-^', 'KOTL', 'KUTL',
        'KREAT-^', 'KREA', 'KREA',
        'KRÜS(TZ)--^', 'KRI', None,
        'KRYS(TZ)--^', 'KRI', None,
        'KRY9^', 'KRÜ', None,
        'KSCH---', 'K', 'K',
        'KSH--', 'K', 'K',
        'K(SßXZ)7', 'X', 'X',  # implies 'KST' -> 'XT'
        'KT\'S$', 'X', 'X',
        'KTI(AIOU)-3', 'XI', 'XI',
        'KT(SßXZ)', 'X', 'X',
        'KY9^', 'KÜ', None,
        'K\'S$', 'X', 'X',
        'K´S$', 'X', 'X',
        'LANGES$', ' LANGES', ' LANKEZ',
        'LANGE$', ' LANGE', ' LANKE',
        'LANG$', ' LANK', ' LANK',
        'LARVE-', 'LARF', 'LARF',
        'LD(SßZ)$', 'LS', 'LZ',
        'LD\'S$', 'LS', 'LZ',
        'LD´S$', 'LS', 'LZ',
        'LEAND-^', 'LEAN', 'LEAN',
        'LEERSTEHE-----^', 'LER ', 'LER ',
        'LEICHBLEIB-----', 'LEICH ', 'LEIK ',
        'LEICHLAUTE-----', 'LEICH ', 'LEIK ',
        'LEIDERREGE------', 'LEIT ', 'LEIT ',
        'LEIDGEPR----^', 'LEIT ', 'LEIT ',
        'LEINSTEHE-----', 'LEIN ', 'LEIN ',
        'LEL-', 'LE', 'LE',
        'LE(MNRST)-3^', 'LE', 'LE',
        'LETTE$', 'LET', 'LET',
        'LFGNAG-', 'LFGAN', 'LFKAN',
        'LICHERWEIS----', 'LICHA ', 'LIKA ',
        'LIC$', 'LIZ', 'LIZ',
        'LIVE^$', 'LEIF', 'LEIF',
        'LT(SßZ)$', 'LS', 'LZ',
        'LT\'S$', 'LS', 'LZ',
        'LT´S$', 'LS', 'LZ',
        'LUI(GS)--', 'LU', 'LU',
        'LV(AIO)-', 'LW', None,
        'LY9^', 'LÜ', None,
        'LSTS$', 'LS', 'LZ',
        'LZ(BDFGKLMNPQRSTVWX)-', 'LS', None,
        'L(SßZ)$', 'LS', None,
        'MAIR-<', 'MEI', 'NEI',
        'MANAG-', 'MENE', 'NENE',
        'MANUEL', 'MANUEL', None,
        'MASSEU(RS)-', 'MASÖ', 'NAZÖ',
        'MATCH', 'MESH', 'NEZ',
        'MAURICE', 'MORIS', 'NURIZ',
        'MBH^$', 'MBH', 'MBH',
        'MB(ßZ)$', 'MS', None,
        'MB(SßTZ)-', 'M', 'N',
        'MCG9^', 'MAK', 'NAK',
        'MC9^', 'MAK', 'NAK',
        'MEMOIR-^', 'MEMOA', 'NENUA',
        'MERHAVEN$', 'MAHAFN', None,
        'ME(LMNRST)-3^', 'ME', 'NE',
        'MEN(STZ)--3', 'ME', None,
        'MEN$', 'MEN', None,
        'MIGUEL-', 'MIGE', 'NIKE',
        'MIKE^$', 'MEIK', 'NEIK',
        'MITHILFE----^$', 'MIT H', 'NIT ',
        'MN$', 'M', None,
        'MN', 'N', 'N',
        'MPJUTE-', 'MPUT', 'NBUT',
        'MP(ßZ)$', 'MS', None,
        'MP(SßTZ)-', 'M', 'N',
        'MP(BDJLMNPQVW)-', 'MB', 'NB',
        'MY9^', 'MÜ', None,
        'M(ßZ)$', 'MS', None,
        'M´G7^', 'MAK', 'NAK',
        'M\'G7^', 'MAK', 'NAK',
        'M´^', 'MAK', 'NAK',
        'M\'^', 'MAK', 'NAK',
        'M', None, 'N',
        'NACH^^', 'NACH', 'NAK',
        'NADINE', 'NADIN', 'NATIN',
        'NAIV--', 'NA', 'NA',
        'NAISE$', 'NESE', 'NEZE',
        'NAUGENOMM------', 'NAU ', 'NAU ',
        'NAUSOGUT$', 'NAUSO GUT', 'NAUZU KUT',
        'NCH$', 'NSH', 'NZ',
        'NCOISE$', 'SOA', 'ZUA',
        'NCOIS$', 'SOA', 'ZUA',
        'NDAR$', 'NDA', 'NTA',
        'NDERINGEN------', 'NDE ', 'NTE ',
        'NDRO(CDKTZ)-', 'NTRO', None,
        'ND(BFGJLMNPQVW)-', 'NT', None,
        'ND(SßZ)$', 'NS', 'NZ',
        'ND\'S$', 'NS', 'NZ',
        'ND´S$', 'NS', 'NZ',
        'NEBEN^^', 'NEBN', 'NEBN',
        'NENGELERN------', 'NEN ', 'NEN ',
        'NENLERN(ET)---', 'NEN LE', 'NEN LE',
        'NENZULERNE---', 'NEN ZU LE', 'NEN ZU LE',
        'NE(LMNRST)-3^', 'NE', 'NE',
        'NEN-3', 'NE', 'NE',
        'NETTE$', 'NET', 'NET',
        'NGU^^', 'NU', 'NU',
        'NG(BDFJLMNPQRTVW)-', 'NK', 'NK',
        'NH(AUO)-$', 'NI', 'NI',
        'NICHTSAHNEN-----', 'NIX ', 'NIX ',
        'NICHTSSAGE----', 'NIX ', 'NIX ',
        'NICHTS^^', 'NIX', 'NIX',
        'NICHT^^', 'NICHT', 'NIKT',
        'NINE$', 'NIN', 'NIN',
        'NON^^', 'NON', 'NUN',
        'NOTLEIDE-----^', 'NOT ', 'NUT ',
        'NOT^^', 'NOT', 'NUT',
        'NTI(AIOU)-3', 'NZI', 'NZI',
        'NTIEL--3', 'NZI', 'NZI',
        'NT(SßZ)$', 'NS', 'NZ',
        'NT\'S$', 'NS', 'NZ',
        'NT´S$', 'NS', 'NZ',
        'NYLON', 'NEILON', 'NEILUN',
        'NY9^', 'NÜ', None,
        'NSTZUNEH---', 'NST ZU ', 'NZT ZU ',
        'NSZ-', 'NS', None,
        'NSTS$', 'NS', 'NZ',
        'NZ(BDFGKLMNPQRSTVWX)-', 'NS', None,
        'N(SßZ)$', 'NS', None,
        'OBERE-', 'OBER', None,
        'OBER^^', 'OBA', 'UBA',
        'OEU2', 'Ö', 'Ö',
        'OE<2', 'Ö', 'Ö',
        'OGL-', 'OK', None,
        'OGNIE-', 'ONI', 'UNI',
        'OGN(AEOU)-$', 'ONI', 'UNI',
        'OH(AIOÖUÜY)-', 'OH', None,
        'OIE$', 'Ö', 'Ö',
        'OIRE$', 'OA', 'UA',
        'OIR$', 'OA', 'UA',
        'OIX', 'OA', 'UA',
        'OI<3', 'EU', 'EU',
        'OKAY^$', 'OKE', 'UKE',
        'OLYN$', 'OLIN', 'ULIN',
        'OO(DLMZ)-', 'U', None,
        'OO$', 'U', None,
        'OO-', '', '',
        'ORGINAL-----', 'ORI', 'URI',
        'OTI(AÄOÖUÜ)-', 'OZI', 'UZI',
        'OUI^', 'WI', 'FI',
        'OUILLE$', 'ULIE', 'ULIE',
        'OU(DT)-^', 'AU', 'AU',
        'OUSE$', 'AUS', 'AUZ',
        'OUT-', 'AU', 'AU',
        'OU', 'U', 'U',
        'O(FV)$', 'AU', 'AU',  # due to 'OW$' -> 'AU'
        'OVER--<', 'OW', None,
        'OV(AOU)-', 'OW', None,
        'OW$', 'AU', 'AU',
        'OWS$', 'OS', 'UZ',
        'OJ(AÄEIOÖUÜ)--', 'O', 'U',
        'OYER', 'OIA', None,
        'OY(AÄEIOÖUÜ)--', 'O', 'U',
        'O(JY)<', 'EU', 'EU',
        'OZ$', 'OS', None,
        'O´^', 'O', 'U',
        'O\'^', 'O', 'U',
        'O', None, 'U',
        'PATIEN--^', 'PAZI', 'PAZI',
        'PENSIO-^', 'PANSI', 'PANZI',
        'PE(LMNRST)-3^', 'PE', 'PE',
        'PFER-^', 'FE', 'FE',
        'P(FH)<', 'F', 'F',
        'PIC^$', 'PIK', 'PIK',
        'PIC$', 'PIZ', 'PIZ',
        'PIPELINE', 'PEIBLEIN', 'PEIBLEIN',
        'POLYP-', 'POLÜ', None,
        'POLY^^', 'POLI', 'PULI',
        'PORTRAIT7', 'PORTRE', 'PURTRE',
        'POWER7', 'PAUA', 'PAUA',
        'PP(FH)--<', 'B', 'B',
        'PP-', '', '',
        'PRODUZ-^', 'PRODU', 'BRUTU',
        'PRODUZI--', ' PRODU', ' BRUTU',
        'PRIX^$', 'PRI', 'PRI',
        'PS-^^', 'P', None,
        'P(SßZ)^', None, 'Z',
        'P(SßZ)$', 'BS', None,
        'PT-^', '', '',
        'PTI(AÄOÖUÜ)-3', 'BZI', 'BZI',
        'PY9^', 'PÜ', None,
        'P(AÄEIOÖRUÜY)-', 'P', 'P',
        'P(ÀÁÂÃÅÈÉÊÌÍÎÙÚÛ)-', 'P', None,
        'P.^', None, 'P.',
        'P^', 'P', None,
        'P', 'B', 'B',
        'QI-', 'Z', 'Z',
        'QUARANT--', 'KARA', 'KARA',
        'QUE(LMNRST)-3', 'KWE', 'KFE',
        'QUE$', 'K', 'K',
        'QUI(NS)$', 'KI', 'KI',
        'QUIZ7', 'KWIS', None,
        'Q(UV)7', 'KW', 'KF',
        'Q<', 'K', 'K',
        'RADFAHR----', 'RAT ', 'RAT ',
        'RAEFTEZEHRE-----', 'REFTE ', 'REFTE ',
        'RCH', 'RCH', 'RK',
        'REA(DU)---3^', 'R', None,
        'REBSERZEUG------', 'REBS ', 'REBZ ',
        'RECHERCH^', 'RESHASH', 'REZAZ',
        'RECYCL--', 'RIZEI', 'RIZEI',
        'RE(ALST)-3^', 'RE', None,
        'REE$', 'RI', 'RI',
        'RER$', 'RA', 'RA',
        'RE(MNR)-4', 'RE', 'RE',
        'RETTE$', 'RET', 'RET',
        'REUZ$', 'REUZ', None,
        'REW$', 'RU', 'RU',
        'RH<^', 'R', 'R',
        'RJA(MN)--', 'RI', 'RI',
        'ROWD-^', 'RAU', 'RAU',
        'RTEMONNAIE-', 'RTMON', 'RTNUN',
        'RTI(AÄOÖUÜ)-3', 'RZI', 'RZI',
        'RTIEL--3', 'RZI', 'RZI',
        'RV(AEOU)-3', 'RW', None,
        'RY(KN)-$', 'RI', 'RI',
        'RY9^', 'RÜ', None,
        'RÄFTEZEHRE-----', 'REFTE ', 'REFTE ',
        'SAISO-^', 'SES', 'ZEZ',
        'SAFE^$', 'SEIF', 'ZEIF',
        'SAUCE-^', 'SOS', 'ZUZ',
        'SCHLAGGEBEN-----<', 'SHLAK ', 'ZLAK ',
        'SCHSCH---7', '', '',
        'SCHTSCH', 'SH', 'Z',
        'SC(HZ)<', 'SH', 'Z',
        'SC', 'SK', 'ZK',
        'SELBSTST--7^^', 'SELB', 'ZELB',
        'SELBST7^^', 'SELBST', 'ZELBZT',
        'SERVICE7^', 'SÖRWIS', 'ZÖRFIZ',
        'SERVI-^', 'SERW', None,
        'SE(LMNRST)-3^', 'SE', 'ZE',
        'SETTE$', 'SET', 'ZET',
        'SHP-^', 'S', 'Z',
        'SHST', 'SHT', 'ZT',
        'SHTSH', 'SH', 'Z',
        'SHT', 'ST', 'Z',
        'SHY9^', 'SHÜ', None,
        'SH^^', 'SH', None,
        'SH3', 'SH', 'Z',
        'SICHERGEGAN-----^', 'SICHA ', 'ZIKA ',
        'SICHERGEHE----^', 'SICHA ', 'ZIKA ',
        'SICHERGESTEL------^', 'SICHA ', 'ZIKA ',
        'SICHERSTELL-----^', 'SICHA ', 'ZIKA ',
        'SICHERZU(GS)--^', 'SICHA ZU ', 'ZIKA ZU ',
        'SIEGLI-^', 'SIKL', 'ZIKL',
        'SIGLI-^', 'SIKL', 'ZIKL',
        'SIGHT', 'SEIT', 'ZEIT',
        'SIGN', 'SEIN', 'ZEIN',
        'SKI(NPZ)-', 'SKI', 'ZKI',
        'SKI<^', 'SHI', 'ZI',
        'SODASS^$', 'SO DAS', 'ZU TAZ',
        'SODAß^$', 'SO DAS', 'ZU TAZ',
        'SOGENAN--^', 'SO GEN', 'ZU KEN',
        'SOUND-', 'SAUN', 'ZAUN',
        'STAATS^^', 'STAZ', 'ZTAZ',
        'STADT^^', 'STAT', 'ZTAT',
        'STANDE$', ' STANDE', ' ZTANTE',
        'START^^', 'START', 'ZTART',
        'STAURANT7', 'STORAN', 'ZTURAN',
        'STEAK-', 'STE', 'ZTE',
        'STEPHEN-^$', 'STEW', None,
        'STERN', 'STERN', None,
        'STRAF^^', 'STRAF', 'ZTRAF',
        'ST\'S$', 'Z', 'Z',
        'ST´S$', 'Z', 'Z',
        'STST--', '', '',
        'STS(ACEÈÉÊHIÌÍÎOUÄÜÖ)--', 'ST', 'ZT',
        'ST(SZ)', 'Z', 'Z',
        'SPAREN---^', 'SPA', 'ZPA',
        'SPAREND----', ' SPA', ' ZPA',
        'S(PTW)-^^', 'S', None,
        'SP', 'SP', None,
        'STYN(AE)-$', 'STIN', 'ZTIN',
        'ST', 'ST', 'ZT',
        'SUITE<', 'SIUT', 'ZIUT',
        'SUKE--$', 'S', 'Z',
        'SURF(EI)-', 'SÖRF', 'ZÖRF',
        'SV(AEÈÉÊIÌÍÎOU)-<^', 'SW', None,
        'SYB(IY)--^', 'SIB', None,
        'SYL(KVW)--^', 'SI', None,
        'SY9^', 'SÜ', None,
        'SZE(NPT)-^', 'ZE', 'ZE',
        'SZI(ELN)-^', 'ZI', 'ZI',
        'SZCZ<', 'SH', 'Z',
        'SZT<', 'ST', 'ZT',
        'SZ<3', 'SH', 'Z',
        'SÜL(KVW)--^', 'SI', None,
        'S', None, 'Z',
        'TCH', 'SH', 'Z',
        'TD(AÄEIOÖRUÜY)-', 'T', None,
        'TD(ÀÁÂÃÅÈÉÊËÌÍÎÏÒÓÔÕØÙÚÛÝŸ)-', 'T', None,
        'TEAT-^', 'TEA', 'TEA',
        'TERRAI7^', 'TERA', 'TERA',
        'TE(LMNRST)-3^', 'TE', 'TE',
        'TH<', 'T', 'T',
        'TICHT-', 'TIK', 'TIK',
        'TICH$', 'TIK', 'TIK',
        'TIC$', 'TIZ', 'TIZ',
        'TIGGESTELL-------', 'TIK ', 'TIK ',
        'TIGSTELL-----', 'TIK ', 'TIK ',
        'TOAS-^', 'TO', 'TU',
        'TOILET-', 'TOLE', 'TULE',
        'TOIN-', 'TOA', 'TUA',
        'TRAECHTI-^', 'TRECHT', 'TREKT',
        'TRAECHTIG--', ' TRECHT', ' TREKT',
        'TRAINI-', 'TREN', 'TREN',
        'TRÄCHTI-^', 'TRECHT', 'TREKT',
        'TRÄCHTIG--', ' TRECHT', ' TREKT',
        'TSCH', 'SH', 'Z',
        'TSH', 'SH', 'Z',
        'TST', 'ZT', 'ZT',
        'T(Sß)', 'Z', 'Z',
        'TT(SZ)--<', '', '',
        'TT9', 'T', 'T',
        'TV^$', 'TV', 'TV',
        'TX(AEIOU)-3', 'SH', 'Z',
        'TY9^', 'TÜ', None,
        'TZ-', '', '',
        'T\'S3$', 'Z', 'Z',
        'T´S3$', 'Z', 'Z',
        'UEBEL(GNRW)-^^', 'ÜBL ', 'IBL ',
        'UEBER^^', 'ÜBA', 'IBA',
        'UE2', 'Ü', 'I',
        'UGL-', 'UK', None,
        'UH(AOÖUÜY)-', 'UH', None,
        'UIE$', 'Ü', 'I',
        'UM^^', 'UM', 'UN',
        'UNTERE--3', 'UNTE', 'UNTE',
        'UNTER^^', 'UNTA', 'UNTA',
        'UNVER^^', 'UNFA', 'UNFA',
        'UN^^', 'UN', 'UN',
        'UTI(AÄOÖUÜ)-', 'UZI', 'UZI',
        'UVE-4', 'UW', None,
        'UY2', 'UI', None,
        'UZZ', 'AS', 'AZ',
        'VACL-^', 'WAZ', 'FAZ',
        'VAC$', 'WAZ', 'FAZ',
        'VAN DEN ^', 'FANDN', 'FANTN',
        'VANES-^', 'WANE', None,
        'VATRO-', 'WATR', None,
        'VA(DHJNT)--^', 'F', None,
        'VEDD-^', 'FE', 'FE',
        'VE(BEHIU)--^', 'F', None,
        'VEL(BDLMNT)-^', 'FEL', None,
        'VENTZ-^', 'FEN', None,
        'VEN(NRSZ)-^', 'FEN', None,
        'VER(AB)-^$', 'WER', None,
        'VERBAL^$', 'WERBAL', None,
        'VERBAL(EINS)-^', 'WERBAL', None,
        'VERTEBR--', 'WERTE', None,
        'VEREIN-----', 'F', None,
        'VEREN(AEIOU)-^', 'WEREN', None,
        'VERIFI', 'WERIFI', None,
        'VERON(AEIOU)-^', 'WERON', None,
        'VERSEN^', 'FERSN', 'FAZN',
        'VERSIERT--^', 'WERSI', None,
        'VERSIO--^', 'WERS', None,
        'VERSUS', 'WERSUS', None,
        'VERTI(GK)-', 'WERTI', None,
        'VER^^', 'FER', 'FA',
        'VERSPRECHE-------', ' FER', ' FA',
        'VER$', 'WA', None,
        'VER', 'FA', 'FA',
        'VET(HT)-^', 'FET', 'FET',
        'VETTE$', 'WET', 'FET',
        'VE^', 'WE', None,
        'VIC$', 'WIZ', 'FIZ',
        'VIELSAGE----', 'FIL ', 'FIL ',
        'VIEL', 'FIL', 'FIL',
        'VIEW', 'WIU', 'FIU',
        'VILL(AE)-', 'WIL', None,
        'VIS(ACEIKUVWZ)-<^', 'WIS', None,
        'VI(ELS)--^', 'F', None,
        'VILLON--', 'WILI', 'FILI',
        'VIZE^^', 'FIZE', 'FIZE',
        'VLIE--^', 'FL', None,
        'VL(AEIOU)--', 'W', None,
        'VOKA-^', 'WOK', None,
        'VOL(ATUVW)--^', 'WO', None,
        'VOR^^', 'FOR', 'FUR',
        'VR(AEIOU)--', 'W', None,
        'VV9', 'W', None,
        'VY9^', 'WÜ', 'FI',
        'V(ÜY)-', 'W', None,
        'V(ÀÁÂÃÅÈÉÊÌÍÎÙÚÛ)-', 'W', None,
        'V(AEIJLRU)-<', 'W', None,
        'V.^', 'V.', None,
        'V<', 'F', 'F',
        'WEITERENTWI-----^', 'WEITA ', 'FEITA ',
        'WEITREICH-----^', 'WEIT ', 'FEIT ',
        'WEITVER^', 'WEIT FER', 'FEIT FA',
        'WE(LMNRST)-3^', 'WE', 'FE',
        'WER(DST)-', 'WER', None,
        'WIC$', 'WIZ', 'FIZ',
        'WIEDERU--', 'WIDE', 'FITE',
        'WIEDER^$', 'WIDA', 'FITA',
        'WIEDER^^', 'WIDA ', 'FITA ',
        'WIEVIEL', 'WI FIL', 'FI FIL',
        'WISUEL', 'WISUEL', None,
        'WR-^', 'W', None,
        'WY9^', 'WÜ', 'FI',
        'W(BDFGJKLMNPQRSTZ)-', 'F', None,
        'W$', 'F', None,
        'W', None, 'F',
        'X<^', 'Z', 'Z',
        'XHAVEN$', 'XAFN', None,
        'X(CSZ)', 'X', 'X',
        'XTS(CH)--', 'XT', 'XT',
        'XT(SZ)', 'Z', 'Z',
        'YE(LMNRST)-3^', 'IE', 'IE',
        'YE-3', 'I', 'I',
        'YOR(GK)^$', 'IÖRK', 'IÖRK',
        'Y(AOU)-<7', 'I', 'I',
        'Y(BKLMNPRSTX)-1', 'Ü', None,
        'YVES^$', 'IF', 'IF',
        'YVONNE^$', 'IWON', 'IFUN',
        'Y.^', 'Y.', None,
        'Y', 'I', 'I',
        'ZC(AOU)-', 'SK', 'ZK',
        'ZE(LMNRST)-3^', 'ZE', 'ZE',
        'ZIEJ$', 'ZI', 'ZI',
        'ZIGERJA(HR)-3', 'ZIGA IA', 'ZIKA IA',
        'ZL(AEIOU)-', 'SL', None,
        'ZS(CHT)--', '', '',
        'ZS', 'SH', 'Z',
        'ZUERST', 'ZUERST', 'ZUERST',
        'ZUGRUNDE^$', 'ZU GRUNDE', 'ZU KRUNTE',
        'ZUGRUNDE', 'ZU GRUNDE ', 'ZU KRUNTE ',
        'ZUGUNSTEN', 'ZU GUNSTN', 'ZU KUNZTN',
        'ZUHAUSE-', 'ZU HAUS', 'ZU AUZ',
        'ZULASTEN^$', 'ZU LASTN', 'ZU LAZTN',
        'ZURUECK^^', 'ZURÜK', 'ZURIK',
        'ZURZEIT', 'ZUR ZEIT', 'ZUR ZEIT',
        'ZURÜCK^^', 'ZURÜK', 'ZURIK',
        'ZUSTANDE', 'ZU STANDE', 'ZU ZTANTE',
        'ZUTAGE', 'ZU TAGE', 'ZU TAKE',
        'ZUVER^^', 'ZUFA', 'ZUFA',
        'ZUVIEL', 'ZU FIL', 'ZU FIL',
        'ZUWENIG', 'ZU WENIK', 'ZU FENIK',
        'ZY9^', 'ZÜ', None,
        'ZYK3$', 'ZIK', None,
        'Z(VW)7^', 'SW', None,
        None, None, None)

    phonet_hash = Counter()
    alpha_pos = Counter()

    phonet_hash_1 = Counter()
    phonet_hash_2 = Counter()

    _phonet_upper_translation = dict(zip((ord(_) for _ in
                                          'abcdefghijklmnopqrstuvwxyzàáâãåäæ' +
                                          'çðèéêëìíîïñòóôõöøœšßþùúûüýÿ'),
                                         'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÅÄÆ' +
                                         'ÇÐÈÉÊËÌÍÎÏÑÒÓÔÕÖØŒŠßÞÙÚÛÜÝŸ'))

    def _initialize_phonet(lang):
        """Initialize phonet variables."""
        if lang == 'none':
            _phonet_rules = _phonet_rules_no_lang
        else:
            _phonet_rules = _phonet_rules_german

        phonet_hash[''] = -1

        # German and international umlauts
        for j in {'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë',
                  'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', 'Ø',
                  'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'Œ', 'Š', 'Ÿ'}:
            alpha_pos[j] = 1
            phonet_hash[j] = -1

        # "normal" letters ('A'-'Z')
        for i, j in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            alpha_pos[j] = i + 2
            phonet_hash[j] = -1

        for i in range(26):
            for j in range(28):
                phonet_hash_1[i, j] = -1
                phonet_hash_2[i, j] = -1

        # for each phonetc rule
        for i in range(len(_phonet_rules)):
            rule = _phonet_rules[i]

            if rule and i % 3 == 0:
                # calculate first hash value
                k = _phonet_rules[i][0]

                if phonet_hash[k] < 0 and (_phonet_rules[i+1] or
                                           _phonet_rules[i+2]):
                    phonet_hash[k] = i

                # calculate second hash values
                if k and alpha_pos[k] >= 2:
                    k = alpha_pos[k]

                    j = k-2
                    rule = rule[1:]

                    if not rule:
                        rule = ' '
                    elif rule[0] == '(':
                        rule = rule[1:]
                    else:
                        rule = rule[0]

                    while rule and (rule[0] != ')'):
                        k = alpha_pos[rule[0]]

                        if k > 0:
                            # add hash value for this letter
                            if phonet_hash_1[j, k] < 0:
                                phonet_hash_1[j, k] = i
                                phonet_hash_2[j, k] = i

                            if phonet_hash_2[j, k] >= (i-30):
                                phonet_hash_2[j, k] = i
                            else:
                                k = -1

                        if k <= 0:
                            # add hash value for all letters
                            if phonet_hash_1[j, 0] < 0:
                                phonet_hash_1[j, 0] = i

                            phonet_hash_2[j, 0] = i

                        rule = rule[1:]

    def _phonet(term, mode, lang):
        """Return the phonet coded form of a term."""
        if lang == 'none':
            _phonet_rules = _phonet_rules_no_lang
        else:
            _phonet_rules = _phonet_rules_german

        char0 = ''
        dest = term

        if not term:
            return ''

        term_length = len(term)

        # convert input string to upper-case
        src = term.translate(_phonet_upper_translation)

        # check "src"
        i = 0
        j = 0
        zeta = 0

        while i < len(src):
            char = src[i]

            pos = alpha_pos[char]

            if pos >= 2:
                xpos = pos-2

                if i+1 == len(src):
                    pos = alpha_pos['']
                else:
                    pos = alpha_pos[src[i+1]]

                start1 = phonet_hash_1[xpos, pos]
                start2 = phonet_hash_1[xpos, 0]
                end1 = phonet_hash_2[xpos, pos]
                end2 = phonet_hash_2[xpos, 0]

                # preserve rule priorities
                if (start2 >= 0) and ((start1 < 0) or (start2 < start1)):
                    pos = start1
                    start1 = start2
                    start2 = pos
                    pos = end1
                    end1 = end2
                    end2 = pos

                if (end1 >= start2) and (start2 >= 0):
                    if end2 > end1:
                        end1 = end2

                    start2 = -1
                    end2 = -1
            else:
                pos = phonet_hash[char]
                start1 = pos
                end1 = 10000
                start2 = -1
                end2 = -1

            pos = start1
            zeta0 = 0

            if pos >= 0:
                # check rules for this char
                while ((_phonet_rules[pos] is None) or
                       (_phonet_rules[pos][0] == char)):
                    if pos > end1:
                        if start2 > 0:
                            pos = start2
                            start1 = start2
                            start2 = -1
                            end1 = end2
                            end2 = -1
                            continue

                        break

                    if (((_phonet_rules[pos] is None) or
                         (_phonet_rules[pos + mode] is None))):
                        # no conversion rule available
                        pos += 3
                        continue

                    # check whole string
                    matches = 1  # number of matching letters
                    priority = 5  # default priority
                    rule = _phonet_rules[pos]
                    rule = rule[1:]

                    while (rule and
                           (len(src) > (i + matches)) and
                           (src[i + matches] == rule[0]) and
                           not rule[0].isdigit() and
                           (rule not in '(-<^$')):
                        matches += 1
                        rule = rule[1:]

                    if rule and (rule[0] == '('):
                        # check an array of letters
                        if (((len(src) > (i + matches)) and
                             src[i + matches].isalpha() and
                             (src[i + matches] in rule[1:]))):
                            matches += 1

                            while rule and rule[0] != ')':
                                rule = rule[1:]

                            # if rule[0] == ')':
                            rule = rule[1:]

                    if rule:
                        priority0 = ord(rule[0])
                    else:
                        priority0 = 0

                    matches0 = matches

                    while rule and rule[0] == '-' and matches > 1:
                        matches -= 1
                        rule = rule[1:]

                    if rule and rule[0] == '<':
                        rule = rule[1:]

                    if rule and rule[0].isdigit():
                        # read priority
                        priority = int(rule[0])
                        rule = rule[1:]

                    if rule and rule[0:2] == '^^':
                        rule = rule[1:]

                    if (not rule or
                            ((rule[0] == '^') and
                             ((i == 0) or not src[i-1].isalpha()) and
                             ((rule[1:2] != '$') or
                              (not (src[i+matches0:i+matches0+1].isalpha()) and
                               (src[i+matches0:i+matches0+1] != '.')))) or
                            ((rule[0] == '$') and (i > 0) and
                             src[i-1].isalpha() and
                             ((not src[i+matches0:i+matches0+1].isalpha()) and
                              (src[i+matches0:i+matches0+1] != '.')))):
                        # look for continuation, if:
                        # matches > 1 und NO '-' in first string */
                        pos0 = -1

                        start3 = 0
                        start4 = 0
                        end3 = 0
                        end4 = 0

                        if (((matches > 1) and
                             src[i+matches:i+matches+1] and
                             (priority0 != ord('-')))):
                            char0 = src[i+matches-1]
                            pos0 = alpha_pos[char0]

                            if pos0 >= 2 and src[i+matches]:
                                xpos = pos0 - 2
                                pos0 = alpha_pos[src[i+matches]]
                                start3 = phonet_hash_1[xpos, pos0]
                                start4 = phonet_hash_1[xpos, 0]
                                end3 = phonet_hash_2[xpos, pos0]
                                end4 = phonet_hash_2[xpos, 0]

                                # preserve rule priorities
                                if (((start4 >= 0) and
                                     ((start3 < 0) or (start4 < start3)))):
                                    pos0 = start3
                                    start3 = start4
                                    start4 = pos0
                                    pos0 = end3
                                    end3 = end4
                                    end4 = pos0

                                if (end3 >= start4) and (start4 >= 0):
                                    if end4 > end3:
                                        end3 = end4

                                    start4 = -1
                                    end4 = -1
                            else:
                                pos0 = phonet_hash[char0]
                                start3 = pos0
                                end3 = 10000
                                start4 = -1
                                end4 = -1

                            pos0 = start3

                        # check continuation rules for src[i+matches]
                        if pos0 >= 0:
                            while ((_phonet_rules[pos0] is None) or
                                   (_phonet_rules[pos0][0] == char0)):
                                if pos0 > end3:
                                    if start4 > 0:
                                        pos0 = start4
                                        start3 = start4
                                        start4 = -1
                                        end3 = end4
                                        end4 = -1
                                        continue

                                    priority0 = -1

                                    # important
                                    break

                                if (((_phonet_rules[pos0] is None) or
                                     (_phonet_rules[pos0 + mode]
                                      is None))):
                                    # no conversion rule available
                                    pos0 += 3
                                    continue

                                # check whole string
                                matches0 = matches
                                priority0 = 5
                                rule = _phonet_rules[pos0]
                                rule = rule[1:]

                                while (rule and
                                       (src[i+matches0:i+matches0+1] ==
                                        rule[0]) and
                                       (not rule[0].isdigit() or
                                        (rule in '(-<^$'))):
                                    matches0 += 1
                                    rule = rule[1:]

                                if rule and rule[0] == '(':
                                    # check an array of letters
                                    if ((src[i+matches0:i+matches0+1]
                                         .isalpha() and
                                         (src[i+matches0] in rule[1:]))):
                                        matches0 += 1

                                        while rule and rule[0] != ')':
                                            rule = rule[1:]

                                        # if rule[0] == ')':
                                        rule = rule[1:]

                                while rule and rule[0] == '-':
                                    # "matches0" is NOT decremented
                                    # because of  "if (matches0 == matches)"
                                    rule = rule[1:]

                                if rule and rule[0] == '<':
                                    rule = rule[1:]

                                if rule and rule[0].isdigit():
                                    priority0 = int(rule[0])
                                    rule = rule[1:]

                                if (not rule or
                                        # rule == '^' is not possible here
                                        ((rule[0] == '$') and not
                                         src[i+matches0:i+matches0+1]
                                         .isalpha() and
                                         (src[i+matches0:i+matches0+1]
                                          != '.'))):
                                    if matches0 == matches:
                                        # this is only a partial string
                                        pos0 += 3
                                        continue

                                    if priority0 < priority:
                                        # priority is too low
                                        pos0 += 3
                                        continue

                                    # continuation rule found
                                    break

                                pos0 += 3

                            # end of "while"
                            if ((priority0 >= priority) and
                                    ((_phonet_rules[pos0] is not None) and
                                     (_phonet_rules[pos0][0] == char0))):

                                pos += 3
                                continue

                        # replace string
                        if ((_phonet_rules[pos] and
                             ('<' in _phonet_rules[pos][1:]))):
                            priority0 = 1
                        else:
                            priority0 = 0

                        rule = _phonet_rules[pos + mode]

                        if (priority0 == 1) and (zeta == 0):
                            # rule with '<' is applied
                            if ((j > 0) and rule and
                                    ((dest[j-1] == char) or
                                     (dest[j-1] == rule[0]))):
                                j -= 1

                            zeta0 = 1
                            zeta += 1
                            matches0 = 0

                            while rule and src[i+matches0]:
                                src = (src[0:i+matches0] + rule[0] +
                                       src[i+matches0+1:])
                                matches0 += 1
                                rule = rule[1:]

                            if matches0 < matches:
                                src = (src[0:i+matches0] +
                                       src[i+matches:])

                            char = src[i]
                        else:
                            i = i + matches - 1
                            zeta = 0

                            while len(rule) > 1:
                                if (j == 0) or (dest[j - 1] != rule[0]):
                                    dest = (dest[0:j] + rule[0] +
                                            dest[min(len(dest), j+1):])
                                    j += 1

                                rule = rule[1:]

                            # new "current char"
                            if not rule:
                                rule = ''
                                char = ''
                            else:
                                char = rule[0]

                            if ((_phonet_rules[pos] and
                                 '^^' in _phonet_rules[pos][1:])):
                                if char:
                                    dest = (dest[0:j] + char +
                                            dest[min(len(dest), j + 1):])
                                    j += 1

                                src = src[i + 1:]
                                i = 0
                                zeta0 = 1

                        break

                    pos += 3

                    if pos > end1 and start2 > 0:
                        pos = start2
                        start1 = start2
                        end1 = end2
                        start2 = -1
                        end2 = -1

            if zeta0 == 0:
                if char and ((j == 0) or (dest[j-1] != char)):
                    # delete multiple letters only
                    dest = dest[0:j] + char + dest[min(j+1, term_length):]
                    j += 1

                i += 1
                zeta = 0

        dest = dest[0:j]

        return dest

    _initialize_phonet(lang)

    word = unicode_normalize('NFKC', text_type(word))
    return _phonet(word, mode, lang)


def spfc(word):
    """Return the Standardized Phonetic Frequency Code (SPFC) of a word.

    Standardized Phonetic Frequency Code is roughly Soundex-like.
    This implementation is based on page 19-21 of :cite:`Moore:1977`.

    :param str word: the word to transform
    :returns: the SPFC value
    :rtype: str

    >>> spfc('Christopher Smith')
    '01160'
    >>> spfc('Christopher Schmidt')
    '01160'
    >>> spfc('Niall Smith')
    '01660'
    >>> spfc('Niall Schmidt')
    '01660'

    >>> spfc('L.Smith')
    '01960'
    >>> spfc('R.Miller')
    '65490'

    >>> spfc(('L', 'Smith'))
    '01960'
    >>> spfc(('R', 'Miller'))
    '65490'
    """
    _pf1 = dict(zip((ord(_) for _ in 'SZCKQVFPUWABLORDHIEMNXGJT'),
                    '0011112222334445556666777'))
    _pf2 = dict(zip((ord(_) for _ in
                     'SZCKQFPXABORDHIMNGJTUVWEL'),
                    '0011122233445556677788899'))
    _pf3 = dict(zip((ord(_) for _ in
                     'BCKQVDTFLPGJXMNRSZAEHIOUWY'),
                    '00000112223334456677777777'))

    _substitutions = (('DK', 'K'), ('DT', 'T'), ('SC', 'S'), ('KN', 'N'),
                      ('MN', 'N'))

    def _raise_word_ex():
        """Raise an AttributeError."""
        raise AttributeError('word attribute must be a string with a space ' +
                             'or period dividing the first and last names ' +
                             'or a tuple/list consisting of the first and ' +
                             'last names')

    if not word:
        return ''

    names = []
    if isinstance(word, (str, text_type)):
        names = word.split('.', 1)
        if len(names) != 2:
            names = word.split(' ', 1)
            if len(names) != 2:
                _raise_word_ex()
    elif hasattr(word, '__iter__'):
        if len(word) != 2:
            _raise_word_ex()
        names = word
    else:
        _raise_word_ex()

    names = [unicode_normalize('NFKD', text_type(_.strip()
                                                 .replace('ß', 'SS')
                                                 .upper()))
             for _ in names]
    code = ''

    def steps_one_to_three(name):
        """Perform the first three steps of SPFC."""
        # filter out non A-Z
        name = ''.join(_ for _ in name if _ in
                       {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                        'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                        'W', 'X', 'Y', 'Z'})

        # 1. In the field, convert DK to K, DT to T, SC to S, KN to N,
        # and MN to N
        for subst in _substitutions:
            name = name.replace(subst[0], subst[1])

        # 2. In the name field, replace multiple letters with a single letter
        name = _delete_consecutive_repeats(name)

        # 3. Remove vowels, W, H, and Y, but keep the first letter in the name
        # field.
        if name:
            name = name[0] + ''.join(_ for _ in name[1:] if _ not in
                                     {'A', 'E', 'H', 'I', 'O', 'U', 'W', 'Y'})
        return name

    names = [steps_one_to_three(_) for _ in names]

    # 4. The first digit of the code is obtained using PF1 and the first letter
    # of the name field. Remove this letter after coding.
    if names[1]:
        code += names[1][0].translate(_pf1)
        names[1] = names[1][1:]

    # 5. Using the last letters of the name, use Table PF3 to obtain the
    # second digit of the code. Use as many letters as possible and remove
    # after coding.
    if names[1]:
        if names[1][-3:] == 'STN' or names[1][-3:] == 'PRS':
            code += '8'
            names[1] = names[1][:-3]
        elif names[1][-2:] == 'SN':
            code += '8'
            names[1] = names[1][:-2]
        elif names[1][-3:] == 'STR':
            code += '9'
            names[1] = names[1][:-3]
        elif names[1][-2:] in {'SR', 'TN', 'TD'}:
            code += '9'
            names[1] = names[1][:-2]
        elif names[1][-3:] == 'DRS':
            code += '7'
            names[1] = names[1][:-3]
        elif names[1][-2:] in {'TR', 'MN'}:
            code += '7'
            names[1] = names[1][:-2]
        else:
            code += names[1][-1].translate(_pf3)
            names[1] = names[1][:-1]

    # 6. The third digit is found using Table PF2 and the first character of
    # the first name. Remove after coding.
    if names[0]:
        code += names[0][0].translate(_pf2)
        names[0] = names[0][1:]

    # 7. The fourth digit is found using Table PF2 and the first character of
    # the name field. If no letters remain use zero. After coding remove the
    # letter.
    # 8. The fifth digit is found in the same manner as the fourth using the
    # remaining characters of the name field if any.
    for _ in range(2):
        if names[1]:
            code += names[1][0].translate(_pf2)
            names[1] = names[1][1:]
        else:
            code += '0'

    return code


def statistics_canada(word, max_length=4):
    """Return the Statistics Canada code for a word.

    The original description of this algorithm could not be located, and
    may only have been specified in an unpublished TR. The coding does not
    appear to be in use by Statistics Canada any longer. In its place, this is
    an implementation of the "Census modified Statistics Canada name coding
    procedure".

    The modified version of this algorithm is described in Appendix B of
     :cite:`Moore:1977`.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 4) of the code to return
    :returns: the Statistics Canada name code value
    :rtype: str

    >>> statistics_canada('Christopher')
    'CHRS'
    >>> statistics_canada('Niall')
    'NL'
    >>> statistics_canada('Smith')
    'SMTH'
    >>> statistics_canada('Schmidt')
    'SCHM'
    """
    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})
    if not word:
        return ''

    code = word[1:]
    for vowel in {'A', 'E', 'I', 'O', 'U', 'Y'}:
        code = code.replace(vowel, '')
    code = word[0]+code
    code = _delete_consecutive_repeats(code)
    code = code.replace(' ', '')

    return code[:max_length]


def lein(word, max_length=4, zero_pad=True):
    """Return the Lein code for a word.

    This is Lein name coding, described in :cite:`Moore:1977`.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 4) of the code to return
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the Lein code
    :rtype: str

    >>> lein('Christopher')
    'C351'
    >>> lein('Niall')
    'N300'
    >>> lein('Smith')
    'S210'
    >>> lein('Schmidt')
    'S521'
    """
    _lein_translation = dict(zip((ord(_) for _ in
                                  'BCDFGJKLMNPQRSTVXZ'),
                                 '451455532245351455'))

    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    code = word[:1]  # Rule 1
    word = word[1:].translate({32: None, 65: None, 69: None, 72: None,
                               73: None, 79: None, 85: None, 87: None,
                               89: None})  # Rule 2
    word = _delete_consecutive_repeats(word)  # Rule 3
    code += word.translate(_lein_translation)  # Rule 4

    if zero_pad:
        code += ('0'*max_length)  # Rule 4

    return code[:max_length]


def roger_root(word, max_length=5, zero_pad=True):
    """Return the Roger Root code for a word.

    This is Roger Root name coding, described in :cite:`Moore:1977`.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 5) of the code to return
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the Roger Root code
    :rtype: str

    >>> roger_root('Christopher')
    '06401'
    >>> roger_root('Niall')
    '02500'
    >>> roger_root('Smith')
    '00310'
    >>> roger_root('Schmidt')
    '06310'
    """
    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    # '*' is used to prevent combining by _delete_consecutive_repeats()
    _init_patterns = {4: {'TSCH': '06'},
                      3: {'TSH': '06', 'SCH': '06'},
                      2: {'CE': '0*0', 'CH': '06', 'CI': '0*0', 'CY': '0*0',
                          'DG': '07', 'GF': '08', 'GM': '03', 'GN': '02',
                          'KN': '02', 'PF': '08', 'PH': '08', 'PN': '02',
                          'SH': '06', 'TS': '0*0', 'WR': '04'},
                      1: {'A': '1', 'B': '09', 'C': '07', 'D': '01', 'E': '1',
                          'F': '08', 'G': '07', 'H': '2', 'I': '1', 'J': '3',
                          'K': '07', 'L': '05', 'M': '03', 'N': '02', 'O': '1',
                          'P': '09', 'Q': '07', 'R': '04', 'S': '0*0',
                          'T': '01', 'U': '1', 'V': '08', 'W': '4', 'X': '07',
                          'Y': '5', 'Z': '0*0'}}

    _med_patterns = {4: {'TSCH': '6'},
                     3: {'TSH': '6', 'SCH': '6'},
                     2: {'CE': '0', 'CH': '6', 'CI': '0', 'CY': '0', 'DG': '7',
                         'PH': '8', 'SH': '6', 'TS': '0'},
                     1: {'B': '9', 'C': '7', 'D': '1', 'F': '8', 'G': '7',
                         'J': '6', 'K': '7', 'L': '5', 'M': '3', 'N': '2',
                         'P': '9', 'Q': '7', 'R': '4', 'S': '0', 'T': '1',
                         'V': '8', 'X': '7', 'Z': '0',
                         'A': '*', 'E': '*', 'H': '*', 'I': '*', 'O': '*',
                         'U': '*', 'W': '*', 'Y': '*'}}

    code = ''
    pos = 0

    # Do first digit(s) first
    for num in range(4, 0, -1):
        if word[:num] in _init_patterns[num]:
            code = _init_patterns[num][word[:num]]
            pos += num
            break

    # Then code subsequent digits
    while pos < len(word):
        for num in range(4, 0, -1):  # pragma: no branch
            if word[pos:pos+num] in _med_patterns[num]:
                code += _med_patterns[num][word[pos:pos+num]]
                pos += num
                break

    code = _delete_consecutive_repeats(code)
    code = code.replace('*', '')

    if zero_pad:
        code += '0'*max_length

    return code[:max_length]


def onca(word, max_length=4, zero_pad=True):
    """Return the Oxford Name Compression Algorithm (ONCA) code for a word.

    This is the Oxford Name Compression Algorithm, based on :cite:`Gill:1997`.

    I can find no complete description of the "anglicised version of the NYSIIS
    method" identified as the first step in this algorithm, so this is likely
    not a precisely correct implementation, in that it employs the standard
    NYSIIS algorithm.

    :param str word: the word to transform
    :param int max_length: the maximum length (default 5) of the code to return
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the ONCA code
    :rtype: str

    >>> onca('Christopher')
    'C623'
    >>> onca('Niall')
    'N400'
    >>> onca('Smith')
    'S530'
    >>> onca('Schmidt')
    'S530'
    """
    # In the most extreme case, 3 characters of NYSIIS input can be compressed
    # to one character of output, so give it triple the max_length.
    return soundex(nysiis(word, max_length=max_length*3), max_length,
                   zero_pad=zero_pad)


def eudex(word, max_length=8):
    """Return the eudex phonetic hash of a word.

    This implementation of eudex phonetic hashing is based on the specification
    (not the reference implementation) at :cite:`Ticki:2016`.

    Further details can be found at :cite:`Ticki:2016b`.

    :param str word: the word to transform
    :param int max_length: the length in bits of the code returned (default 8)
    :returns: the eudex hash
    :rtype: int

    >>> eudex('Colin')
    432345564238053650
    >>> eudex('Christopher')
    433648490138894409
    >>> eudex('Niall')
    648518346341351840
    >>> eudex('Smith')
    720575940412906756
    >>> eudex('Schmidt')
    720589151732307997
    """
    _trailing_phones = {
        'a': 0,  # a
        'b': 0b01001000,  # b
        'c': 0b00001100,  # c
        'd': 0b00011000,  # d
        'e': 0,  # e
        'f': 0b01000100,  # f
        'g': 0b00001000,  # g
        'h': 0b00000100,  # h
        'i': 1,  # i
        'j': 0b00000101,  # j
        'k': 0b00001001,  # k
        'l': 0b10100000,  # l
        'm': 0b00000010,  # m
        'n': 0b00010010,  # n
        'o': 0,  # o
        'p': 0b01001001,  # p
        'q': 0b10101000,  # q
        'r': 0b10100001,  # r
        's': 0b00010100,  # s
        't': 0b00011101,  # t
        'u': 1,  # u
        'v': 0b01000101,  # v
        'w': 0b00000000,  # w
        'x': 0b10000100,  # x
        'y': 1,  # y
        'z': 0b10010100,  # z

        'ß': 0b00010101,  # ß
        'à': 0,  # à
        'á': 0,  # á
        'â': 0,  # â
        'ã': 0,  # ã
        'ä': 0,  # ä[æ]
        'å': 1,  # å[oː]
        'æ': 0,  # æ[æ]
        'ç': 0b10010101,  # ç[t͡ʃ]
        'è': 1,  # è
        'é': 1,  # é
        'ê': 1,  # ê
        'ë': 1,  # ë
        'ì': 1,  # ì
        'í': 1,  # í
        'î': 1,  # î
        'ï': 1,  # ï
        'ð': 0b00010101,  # ð[ð̠](represented as a non-plosive T)
        'ñ': 0b00010111,  # ñ[nj](represented as a combination of n and j)
        'ò': 0,  # ò
        'ó': 0,  # ó
        'ô': 0,  # ô
        'õ': 0,  # õ
        'ö': 1,  # ö[ø]
        '÷': 0b11111111,  # ÷
        'ø': 1,  # ø[ø]
        'ù': 1,  # ù
        'ú': 1,  # ú
        'û': 1,  # û
        'ü': 1,  # ü
        'ý': 1,  # ý
        'þ': 0b00010101,  # þ[ð̠](represented as a non-plosive T)
        'ÿ': 1,  # ÿ
    }

    _initial_phones = {
        'a': 0b10000100,  # a*
        'b': 0b00100100,  # b
        'c': 0b00000110,  # c
        'd': 0b00001100,  # d
        'e': 0b11011000,  # e*
        'f': 0b00100010,  # f
        'g': 0b00000100,  # g
        'h': 0b00000010,  # h
        'i': 0b11111000,  # i*
        'j': 0b00000011,  # j
        'k': 0b00000101,  # k
        'l': 0b01010000,  # l
        'm': 0b00000001,  # m
        'n': 0b00001001,  # n
        'o': 0b10010100,  # o*
        'p': 0b00100101,  # p
        'q': 0b01010100,  # q
        'r': 0b01010001,  # r
        's': 0b00001010,  # s
        't': 0b00001110,  # t
        'u': 0b11100000,  # u*
        'v': 0b00100011,  # v
        'w': 0b00000000,  # w
        'x': 0b01000010,  # x
        'y': 0b11100100,  # y*
        'z': 0b01001010,  # z

        'ß': 0b00001011,  # ß
        'à': 0b10000101,  # à
        'á': 0b10000101,  # á
        'â': 0b10000000,  # â
        'ã': 0b10000110,  # ã
        'ä': 0b10100110,  # ä [æ]
        'å': 0b11000010,  # å [oː]
        'æ': 0b10100111,  # æ [æ]
        'ç': 0b01010100,  # ç [t͡ʃ]
        'è': 0b11011001,  # è
        'é': 0b11011001,  # é
        'ê': 0b11011001,  # ê
        'ë': 0b11000110,  # ë [ə] or [œ]
        'ì': 0b11111001,  # ì
        'í': 0b11111001,  # í
        'î': 0b11111001,  # î
        'ï': 0b11111001,  # ï
        'ð': 0b00001011,  # ð [ð̠] (represented as a non-plosive T)
        'ñ': 0b00001011,  # ñ [nj] (represented as a combination of n and j)
        'ò': 0b10010101,  # ò
        'ó': 0b10010101,  # ó
        'ô': 0b10010101,  # ô
        'õ': 0b10010101,  # õ
        'ö': 0b11011100,  # ö [œ] or [ø]
        '÷': 0b11111111,  # ÷
        'ø': 0b11011101,  # ø [œ] or [ø]
        'ù': 0b11100001,  # ù
        'ú': 0b11100001,  # ú
        'û': 0b11100001,  # û
        'ü': 0b11100101,  # ü
        'ý': 0b11100101,  # ý
        'þ': 0b00001011,  # þ [ð̠] (represented as a non-plosive T)
        'ÿ': 0b11100101,  # ÿ
    }
    # Lowercase input & filter unknown characters
    word = ''.join(char for char in word.lower() if char in _initial_phones)

    if not word:
        word = '÷'

    # Perform initial eudex coding of each character
    values = [_initial_phones[word[0]]]
    values += [_trailing_phones[char] for char in word[1:]]

    # Right-shift by one to determine if second instance should be skipped
    shifted_values = [_ >> 1 for _ in values]
    condensed_values = [values[0]]
    for n in range(1, len(shifted_values)):
        if shifted_values[n] != shifted_values[n-1]:
            condensed_values.append(values[n])

    # Add padding after first character & trim beyond max_length
    values = ([condensed_values[0]] +
              [0]*max(0, max_length - len(condensed_values)) +
              condensed_values[1:max_length])

    # Combine individual character values into eudex hash
    hash_value = 0
    for val in values:
        hash_value = (hash_value << 8) | val

    return hash_value


def haase_phonetik(word, primary_only=False):
    """Return the Haase Phonetik (numeric output) code for a word.

    Based on the algorithm described at :cite:`Prante:2015`.

    Based on the original :cite:`Haase:2000`.

    While the output code is numeric, it is nevertheless a str.

    :param str word: the word to transform
    :param bool primary_only: if True, only the primary code is returned
    :returns: the Haase Phonetik value as a numeric string
    :rtype: tuple

    >>> haase_phonetik('Joachim')
    ('9496',)
    >>> haase_phonetik('Christoph')
    ('4798293', '8798293')
    >>> haase_phonetik('Jörg')
    ('974',)
    >>> haase_phonetik('Smith')
    ('8692',)
    >>> haase_phonetik('Schmidt')
    ('8692', '4692')
    """
    def _after(word, i, letters):
        """Return True if word[i] follows one of the supplied letters."""
        if i > 0 and word[i-1] in letters:
            return True
        return False

    def _before(word, i, letters):
        """Return True if word[i] precedes one of the supplied letters."""
        if i+1 < len(word) and word[i+1] in letters:
            return True
        return False

    _vowels = {'A', 'E', 'I', 'J', 'O', 'U', 'Y'}

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')

    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    variants = []
    if primary_only:
        variants = [word]
    else:
        pos = 0
        if word[:2] == 'CH':
            variants.append(('CH', 'SCH'))
            pos += 2
        len_3_vars = {'OWN': 'AUN', 'WSK': 'RSK', 'SCH': 'CH', 'GLI': 'LI',
                      'AUX': 'O', 'EUX': 'O'}
        while pos < len(word):
            if word[pos:pos+4] == 'ILLE':
                variants.append(('ILLE', 'I'))
                pos += 4
            elif word[pos:pos+3] in len_3_vars:
                variants.append((word[pos:pos+3], len_3_vars[word[pos:pos+3]]))
                pos += 3
            elif word[pos:pos+2] == 'RB':
                variants.append(('RB', 'RW'))
                pos += 2
            elif len(word[pos:]) == 3 and word[pos:] == 'EAU':
                variants.append(('EAU', 'O'))
                pos += 3
            elif len(word[pos:]) == 1 and word[pos:] in {'A', 'O'}:
                if word[pos:] == 'O':
                    variants.append(('O', 'OW'))
                else:
                    variants.append(('A', 'AR'))
                pos += 1
            else:
                variants.append((word[pos],))
                pos += 1

        variants = [''.join(letters) for letters in product(*variants)]

    def _haase_code(word):
        sdx = ''
        for i in range(len(word)):
            if word[i] in _vowels:
                sdx += '9'
            elif word[i] == 'B':
                sdx += '1'
            elif word[i] == 'P':
                if _before(word, i, {'H'}):
                    sdx += '3'
                else:
                    sdx += '1'
            elif word[i] in {'D', 'T'}:
                if _before(word, i, {'C', 'S', 'Z'}):
                    sdx += '8'
                else:
                    sdx += '2'
            elif word[i] in {'F', 'V', 'W'}:
                sdx += '3'
            elif word[i] in {'G', 'K', 'Q'}:
                sdx += '4'
            elif word[i] == 'C':
                if _after(word, i, {'S', 'Z'}):
                    sdx += '8'
                elif i == 0:
                    if _before(word, i, {'A', 'H', 'K', 'L', 'O', 'Q', 'R',
                                         'U', 'X'}):
                        sdx += '4'
                    else:
                        sdx += '8'
                elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                    sdx += '4'
                else:
                    sdx += '8'
            elif word[i] == 'X':
                if _after(word, i, {'C', 'K', 'Q'}):
                    sdx += '8'
                else:
                    sdx += '48'
            elif word[i] == 'L':
                sdx += '5'
            elif word[i] in {'M', 'N'}:
                sdx += '6'
            elif word[i] == 'R':
                sdx += '7'
            elif word[i] in {'S', 'Z'}:
                sdx += '8'

        sdx = _delete_consecutive_repeats(sdx)

        return sdx

    encoded = tuple(_haase_code(word) for word in variants)
    if len(encoded) > 1:
        encoded_set = set()
        encoded_single = []
        for code in encoded:
            if code not in encoded_set:
                encoded_set.add(code)
                encoded_single.append(code)
        return tuple(encoded_single)

    return encoded


def reth_schek_phonetik(word):
    """Return Reth-Schek Phonetik code for a word.

    This algorithm is proposed in :cite:`Reth:1977`.

    Since I couldn't secure a copy of that document (maybe I'll look for it
    next time I'm in Germany), this implementation is based on what I could
    glean from the implementations published by German Record Linkage
    Center (www.record-linkage.de):

    - Privacy-preserving Record Linkage (PPRL) (in R) :cite:`Rukasz:2018`
    - Merge ToolBox (in Java) :cite:`Schnell:2004`

    Rules that are unclear:

    - Should 'C' become 'G' or 'Z'? (PPRL has both, 'Z' rule blocked)
    - Should 'CC' become 'G'? (PPRL has blocked 'CK' that may be typo)
    - Should 'TUI' -> 'ZUI' rule exist? (PPRL has rule, but I can't
      think of a German word with '-tui-' in it.)
    - Should we really change 'SCH' -> 'CH' and then 'CH' -> 'SCH'?

    :param str word: the word to transform
    :returns: the Reth-Schek Phonetik code
    :rtype: str

    >>> reth_schek_phonetik('Joachim')
    'JOAGHIM'
    >>> reth_schek_phonetik('Christoph')
    'GHRISDOF'
    >>> reth_schek_phonetik('Jörg')
    'JOERG'
    >>> reth_schek_phonetik('Smith')
    'SMID'
    >>> reth_schek_phonetik('Schmidt')
    'SCHMID'
    """
    replacements = {3: {'AEH': 'E', 'IEH': 'I', 'OEH': 'OE', 'UEH': 'UE',
                        'SCH': 'CH', 'ZIO': 'TIO', 'TIU': 'TIO', 'ZIU': 'TIO',
                        'CHS': 'X', 'CKS': 'X', 'AEU': 'OI'},
                    2: {'LL': 'L', 'AA': 'A', 'AH': 'A', 'BB': 'B', 'PP': 'B',
                        'BP': 'B', 'PB': 'B', 'DD': 'D', 'DT': 'D', 'TT': 'D',
                        'TH': 'D', 'EE': 'E', 'EH': 'E', 'AE': 'E', 'FF': 'F',
                        'PH': 'F', 'KK': 'K', 'GG': 'G', 'GK': 'G', 'KG': 'G',
                        'CK': 'G', 'CC': 'C', 'IE': 'I', 'IH': 'I', 'MM': 'M',
                        'NN': 'N', 'OO': 'O', 'OH': 'O', 'SZ': 'S', 'UH': 'U',
                        'GS': 'X', 'KS': 'X', 'TZ': 'Z', 'AY': 'AI',
                        'EI': 'AI', 'EY': 'AI', 'EU': 'OI', 'RR': 'R',
                        'SS': 'S', 'KW': 'QU'},
                    1: {'P': 'B', 'T': 'D', 'V': 'F', 'W': 'F', 'C': 'G',
                        'K': 'G', 'Y': 'I'}}

    # Uppercase
    word = word.upper()

    # Replace umlauts/eszett
    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')
    word = word.replace('ß', 'SS')

    # Main loop, using above replacements table
    pos = 0
    while pos < len(word):
        for num in range(3, 0, -1):
            if word[pos:pos+num] in replacements[num]:
                word = (word[:pos] + replacements[num][word[pos:pos+num]]
                        + word[pos+num:])
                pos += 1
                break
        else:
            pos += 1  # Advance if nothing is recognized

    # Change 'CH' back(?) to 'SCH'
    word = word.replace('CH', 'SCH')

    # Replace final sequences
    if word[-2:] == 'ER':
        word = word[:-2]+'R'
    elif word[-2:] == 'EL':
        word = word[:-2]+'L'
    elif word[-1:] == 'H':
        word = word[:-1]

    return word


def fonem(word):
    """Return the FONEM code of a word.

    FONEM is a phonetic algorithm designed for French (particularly surnames in
    Saguenay, Canada), defined in :cite:`Bouchard:1981`.

    Guillaume Plique's Javascript implementation :cite:`Plique:2018` at
    https://github.com/Yomguithereal/talisman/blob/master/src/phonetics/french/fonem.js
    was also consulted for this implementation.

    :param str word: the word to transform
    :returns: the FONEM code
    :rtype: str

    >>> fonem('Marchand')
    'MARCHEN'
    >>> fonem('Beaulieu')
    'BOLIEU'
    >>> fonem('Beaumont')
    'BOMON'
    >>> fonem('Legrand')
    'LEGREN'
    >>> fonem('Pelletier')
    'PELETIER'
    """
    # I don't see a sane way of doing this without regexps :(
    rule_table = {
        # Vowels & groups of vowels
        'V-1':     (re_compile('E?AU'), 'O'),
        'V-2,5':   (re_compile('(E?AU|O)L[TX]$'), 'O'),
        'V-3,4':   (re_compile('E?AU[TX]$'), 'O'),
        'V-6':     (re_compile('E?AUL?D$'), 'O'),
        'V-7':     (re_compile(r'(?<!G)AY$'), 'E'),
        'V-8':     (re_compile('EUX$'), 'EU'),
        'V-9':     (re_compile('EY(?=$|[BCDFGHJKLMNPQRSTVWXZ])'), 'E'),
        'V-10':    ('Y', 'I'),
        'V-11':    (re_compile('(?<=[AEIOUY])I(?=[AEIOUY])'), 'Y'),
        'V-12':    (re_compile('(?<=[AEIOUY])ILL'), 'Y'),
        'V-13':    (re_compile('OU(?=[AEOU]|I(?!LL))'), 'W'),
        'V-14':    (re_compile(r'([AEIOUY])(?=\1)'), ''),
        # Nasal vowels
        'V-15':    (re_compile('[AE]M(?=[BCDFGHJKLMPQRSTVWXZ])(?!$)'), 'EN'),
        'V-16':    (re_compile('OM(?=[BCDFGHJKLMPQRSTVWXZ])'), 'ON'),
        'V-17':    (re_compile('AN(?=[BCDFGHJKLMNPQRSTVWXZ])'), 'EN'),
        'V-18':    (re_compile('(AI[MN]|EIN)(?=[BCDFGHJKLMNPQRSTVWXZ]|$)'),
                    'IN'),
        'V-19':    (re_compile('B(O|U|OU)RNE?$'), 'BURN'),
        'V-20':    (re_compile('(^IM|(?<=[BCDFGHJKLMNPQRSTVWXZ])' +
                               'IM(?=[BCDFGHJKLMPQRSTVWXZ]))'), 'IN'),
        # Consonants and groups of consonants
        'C-1':     ('BV', 'V'),
        'C-2':     (re_compile('(?<=[AEIOUY])C(?=[EIY])'), 'SS'),
        'C-3':     (re_compile('(?<=[BDFGHJKLMNPQRSTVWZ])C(?=[EIY])'), 'S'),
        'C-4':     (re_compile('^C(?=[EIY])'), 'S'),
        'C-5':     (re_compile('^C(?=[OUA])'), 'K'),
        'C-6':     (re_compile('(?<=[AEIOUY])C$'), 'K'),
        'C-7':     (re_compile('C(?=[BDFGJKLMNPQRSTVWXZ])'), 'K'),
        'C-8':     (re_compile('CC(?=[AOU])'), 'K'),
        'C-9':     (re_compile('CC(?=[EIY])'), 'X'),
        'C-10':    (re_compile('G(?=[EIY])'), 'J'),
        'C-11':    (re_compile('GA(?=I?[MN])'), 'G#'),
        'C-12':    (re_compile('GE(O|AU)'), 'JO'),
        'C-13':    (re_compile('GNI(?=[AEIOUY])'), 'GN'),
        'C-14':    (re_compile('(?<![PCS])H'), ''),
        'C-15':    ('JEA', 'JA'),
        'C-16':    (re_compile('^MAC(?=[BCDFGHJKLMNPQRSTVWXZ])'), 'MA#'),
        'C-17':    (re_compile('^MC'), 'MA#'),
        'C-18':    ('PH', 'F'),
        'C-19':    ('QU', 'K'),
        'C-20':    (re_compile('^SC(?=[EIY])'), 'S'),
        'C-21':    (re_compile('(?<=.)SC(?=[EIY])'), 'SS'),
        'C-22':    (re_compile('(?<=.)SC(?=[AOU])'), 'SK'),
        'C-23':    ('SH', 'CH'),
        'C-24':    (re_compile('TIA$'), 'SSIA'),
        'C-25':    (re_compile('(?<=[AIOUY])W'), ''),
        'C-26':    (re_compile('X[CSZ]'), 'X'),
        'C-27':    (re_compile('(?<=[AEIOUY])Z|(?<=[BCDFGHJKLMNPQRSTVWXZ])' +
                               'Z(?=[BCDFGHJKLMNPQRSTVWXZ])'), 'S'),
        'C-28':    (re_compile(r'([BDFGHJKMNPQRTVWXZ])\1'), r'\1'),
        'C-28a':   (re_compile('CC(?=[BCDFGHJKLMNPQRSTVWXZ]|$)'), 'C'),
        'C-28b':   (re_compile('((?<=[BCDFGHJKLMNPQRSTVWXZ])|^)SS'), 'S'),
        'C-28bb':  (re_compile('SS(?=[BCDFGHJKLMNPQRSTVWXZ]|$)'), 'S'),
        'C-28c':   (re_compile('((?<=[^I])|^)LL'), 'L'),
        'C-28d':   (re_compile('ILE$'), 'ILLE'),
        'C-29':    (re_compile('(ILS|[CS]H|[MN]P|R[CFKLNSX])$|([BCDFGHJKL' +
                               'MNPQRSTVWXZ])[BCDFGHJKLMNPQRSTVWXZ]$'),
                    lambda m: (m.group(1) or '') + (m.group(2) or '')),
        'C-30,32': (re_compile('^(SA?INT?|SEI[NM]|CINQ?|ST)(?!E)-?'), 'ST-'),
        'C-31,33': (re_compile('^(SAINTE|STE)-?'), 'STE-'),
        # Rules to undo rule bleeding prevention in C-11, C-16, C-17
        'C-34':    ('G#', 'GA'),
        'C-35':    ('MA#', 'MAC')
    }
    rule_order = [
        'V-14', 'C-28', 'C-28a', 'C-28b', 'C-28bb', 'C-28c', 'C-28d',
        'C-12',
        'C-8', 'C-9', 'C-10',
        'C-16', 'C-17', 'C-2', 'C-3', 'C-7',
        'V-2,5', 'V-3,4', 'V-6',
        'V-1', 'C-14',
        'C-31,33', 'C-30,32',
        'C-11', 'V-15', 'V-17', 'V-18',
        'V-7', 'V-8', 'V-9', 'V-10', 'V-11', 'V-12', 'V-13', 'V-16',
        'V-19', 'V-20',
        'C-1', 'C-4', 'C-5', 'C-6', 'C-13', 'C-15',
        'C-18', 'C-19', 'C-20', 'C-21', 'C-22', 'C-23', 'C-24',
        'C-25', 'C-26', 'C-27',
        'C-29',
        'V-14', 'C-28', 'C-28a', 'C-28b', 'C-28bb', 'C-28c', 'C-28d',
        'C-34', 'C-35'
    ]

    # normalize, upper-case, and filter non-French letters
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.translate({198: 'AE', 338: 'OE'})
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z', '-'})

    for rule in rule_order:
        regex, repl = rule_table[rule]
        if isinstance(regex, text_type):
            word = word.replace(regex, repl)
        else:
            word = regex.sub(repl, word)

    return word


def parmar_kumbharana(word):
    """Return the Parmar-Kumbharana encoding of a word.

    This is based on the phonetic algorithm proposed in :cite:`Parmar:2014`.

    :param str word: the word to transform
    :returns: the Parmar-Kumbharana encoding
    :rtype: str

    >>> parmar_kumbharana('Gough')
    'GF'
    >>> parmar_kumbharana('pneuma')
    'NM'
    >>> parmar_kumbharana('knight')
    'NT'
    >>> parmar_kumbharana('trice')
    'TRS'
    >>> parmar_kumbharana('judge')
    'JJ'
    """
    rule_table = {4: {'OUGH': 'F'},
                  3: {'DGE': 'J',
                      'OUL': 'U',
                      'GHT': 'T'},
                  2: {'CE': 'S', 'CI': 'S', 'CY': 'S',
                      'GE': 'J', 'GI': 'J', 'GY': 'J',
                      'WR': 'R',
                      'GN': 'N', 'KN': 'N', 'PN': 'N',
                      'CK': 'K',
                      'SH': 'S'}}
    vowel_trans = {65: '', 69: '', 73: '', 79: '', 85: '', 89: ''}

    word = word.upper()  # Rule 3
    word = _delete_consecutive_repeats(word)  # Rule 4

    # Rule 5
    i = 0
    while i < len(word):
        for match_len in range(4, 1, -1):
            if word[i:i+match_len] in rule_table[match_len]:
                repl = rule_table[match_len][word[i:i+match_len]]
                word = (word[:i] + repl + word[i+match_len:])
                i += len(repl)
                break
        else:
            i += 1

    word = word[0]+word[1:].translate(vowel_trans)  # Rule 6
    return word


def davidson(lname, fname='.', omit_fname=False):
    """Return Davidson's Consonant Code.

    This is based on the name compression system described in
    :cite:`Davidson:1962`.

    :cite:`Dolby:1970` identifies this as having been the name compression
    algorithm used by SABRE.

    :param str lname: Last name (or word) to be encoded
    :param str fname: First name (optional), of which the first character is
        included in the code.
    :param bool omit_fname: Set to True to completely omit the first character
        of the first name
    :returns: Davidson's Consonant Code
    :rtype: str

    >>> davidson('Gough')
    'G   .'
    >>> davidson('pneuma')
    'PNM .'
    >>> davidson('knight')
    'KNGT.'
    >>> davidson('trice')
    'TRC .'
    >>> davidson('judge')
    'JDG .'
    >>> davidson('Smith', 'James')
    'SMT J'
    >>> davidson('Wasserman', 'Tabitha')
    'WSRMT'
    """
    trans = {65: '', 69: '', 73: '', 79: '', 85: '', 72: '', 87: '', 89: ''}

    lname = text_type(lname.upper())
    code = _delete_consecutive_repeats(lname[:1] + lname[1:].translate(trans))
    code = code[:4] + (4-len(code))*' '

    if not omit_fname:
        code += fname[:1].upper()

    return code


def sound_d(word, max_length=4):
    """Return the SoundD code.

    SoundD is defined in :cite:`Varol:2012`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :returns: the SoundD code
    :rtype: str

    >>> sound_d('Gough')
    '2000'
    >>> sound_d('pneuma')
    '5500'
    >>> sound_d('knight')
    '5300'
    >>> sound_d('trice')
    '3620'
    >>> sound_d('judge')
    '2200'
    """
    _ref_soundd_translation = dict(zip((ord(_) for _ in
                                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                       '01230120022455012623010202'))

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    if word[:2] in {'KN', 'GN', 'PN', 'AC', 'WR'}:
        word = word[1:]
    elif word[:1] == 'X':
        word = 'S'+word[1:]
    elif word[:2] == 'WH':
        word = 'W'+word[2:]

    word = word.replace('DGE', '20').replace('DGI', '20').replace('GH', '0')

    word = word.translate(_ref_soundd_translation)
    word = _delete_consecutive_repeats(word)
    word = word.replace('0', '')

    if max_length != -1:
        if len(word) < max_length:
            word += '0' * (max_length-len(word))
        else:
            word = word[:max_length]

    return word


def pshp_soundex_last(lname, max_length=4, german=False):
    """Calculate the PSHP Soundex/Viewex Coding of a last name.

    This coding is based on :cite:`Hershberg:1976`.

    Reference was also made to the German version of the same:
    :cite:`Hershberg:1979`.

    A separate function, pshp_soundex_first() is used for first names.

    :param str lname: the last name to encode
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool german: set to True if the name is German (different rules
        apply)
    :returns: the PSHP Soundex/Viewex Coding
    :rtype: str

    >>> pshp_soundex_last('Smith')
    'S530'
    >>> pshp_soundex_last('Waters')
    'W350'
    >>> pshp_soundex_last('James')
    'J500'
    >>> pshp_soundex_last('Schmidt')
    'S530'
    >>> pshp_soundex_last('Ashcroft')
    'A225'
    """
    lname = unicode_normalize('NFKD', text_type(lname.upper()))
    lname = lname.replace('ß', 'SS')
    lname = ''.join(c for c in lname if c in
                    {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                     'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                     'W', 'X', 'Y', 'Z'})

    # A. Prefix treatment
    if lname[:3] == 'VON' or lname[:3] == 'VAN':
        lname = lname[3:].strip()

    # The rule implemented below says "MC, MAC become 1". I believe it meant to
    # say they become M except in German data (where superscripted 1 indicates
    # "except in German data"). It doesn't make sense for them to become 1
    # (BPFV -> 1) or to apply outside German. Unfortunately, both articles have
    # this error(?).
    if not german:
        if lname[:3] == 'MAC':
            lname = 'M'+lname[3:]
        elif lname[:2] == 'MC':
            lname = 'M'+lname[2:]

    # The non-German-only rule to strip ' is unnecessary due to filtering

    if lname[:1] in {'E', 'I', 'O', 'U'}:
        lname = 'A' + lname[1:]
    elif lname[:2] in {'GE', 'GI', 'GY'}:
        lname = 'J' + lname[1:]
    elif lname[:2] in {'CE', 'CI', 'CY'}:
        lname = 'S' + lname[1:]
    elif lname[:3] == 'CHR':
        lname = 'K' + lname[1:]
    elif lname[:1] == 'C' and lname[:2] != 'CH':
        lname = 'K' + lname[1:]

    if lname[:2] == 'KN':
        lname = 'N' + lname[1:]
    elif lname[:2] == 'PH':
        lname = 'F' + lname[1:]
    elif lname[:3] in {'WIE', 'WEI'}:
        lname = 'V' + lname[1:]

    if german and lname[:1] in {'W', 'M', 'Y', 'Z'}:
        lname = {'W': 'V', 'M': 'N', 'Y': 'J', 'Z': 'S'}[lname[0]]+lname[1:]

    code = lname[:1]

    # B. Postfix treatment
    if german:  # moved from end of postfix treatment due to blocking
        if lname[-3:] == 'TES':
            lname = lname[:-3]
        elif lname[-2:] == 'TS':
            lname = lname[:-2]
        if lname[-3:] == 'TZE':
            lname = lname[:-3]
        elif lname[-2:] == 'ZE':
            lname = lname[:-2]
        if lname[-1:] == 'Z':
            lname = lname[:-1]
        elif lname[-2:] == 'TE':
            lname = lname[:-2]

    if lname[-1:] == 'R':
        lname = lname[:-1] + 'N'
    elif lname[-2:] in {'SE', 'CE'}:
        lname = lname[:-2]
    if lname[-2:] == 'SS':
        lname = lname[:-2]
    elif lname[-1:] == 'S':
        lname = lname[:-1]

    if not german:
        l5_repl = {'STOWN': 'SAWON', 'MPSON': 'MASON'}
        l4_repl = {'NSEN': 'ASEN', 'MSON': 'ASON', 'STEN': 'SAEN',
                   'STON': 'SAON'}
        if lname[-5:] in l5_repl:
            lname = lname[:-5] + l5_repl[lname[-5:]]
        elif lname[-4:] in l4_repl:
            lname = lname[:-4] + l4_repl[lname[-4:]]

    if lname[-2:] in {'NG', 'ND'}:
        lname = lname[:-1]
    if not german and lname[-3:] in {'GAN', 'GEN'}:
        lname = lname[:-3]+'A'+lname[-2:]

    # C. Infix Treatment
    lname = lname.replace('CK', 'C')
    lname = lname.replace('SCH', 'S')
    lname = lname.replace('DT', 'T')
    lname = lname.replace('ND', 'N')
    lname = lname.replace('NG', 'N')
    lname = lname.replace('LM', 'M')
    lname = lname.replace('MN', 'M')
    lname = lname.replace('WIE', 'VIE')
    lname = lname.replace('WEI', 'VEI')

    # D. Soundexing
    # code for X & Y are unspecified, but presumably are 2 & 0
    _pshp_translation = dict(zip((ord(_) for _ in
                                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                 '01230120022455012523010202'))

    lname = lname.translate(_pshp_translation)
    lname = _delete_consecutive_repeats(lname)

    code += lname[1:]
    code = code.replace('0', '')  # rule 1

    if max_length != -1:
        if len(code) < max_length:
            code += '0' * (max_length-len(code))
        else:
            code = code[:max_length]

    return code


def pshp_soundex_first(fname, max_length=4, german=False):
    """Calculate the PSHP Soundex/Viewex Coding of a first name.

    This coding is based on :cite:`Hershberg:1976`.

    Reference was also made to the German version of the same:
    :cite:`Hershberg:1979`.

    A separate function, pshp_soundex_last() is used for last names.

    :param str fname: the first name to encode
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool german: set to True if the name is German (different rules
        apply)
    :returns: the PSHP Soundex/Viewex Coding
    :rtype: str

    >>> pshp_soundex_first('Smith')
    'S530'
    >>> pshp_soundex_first('Waters')
    'W352'
    >>> pshp_soundex_first('James')
    'J700'
    >>> pshp_soundex_first('Schmidt')
    'S500'
    >>> pshp_soundex_first('Ashcroft')
    'A220'
    >>> pshp_soundex_first('John')
    'J500'
    >>> pshp_soundex_first('Colin')
    'K400'
    >>> pshp_soundex_first('Niall')
    'N400'
    >>> pshp_soundex_first('Sally')
    'S400'
    >>> pshp_soundex_first('Jane')
    'J500'
    """
    fname = unicode_normalize('NFKD', text_type(fname.upper()))
    fname = fname.replace('ß', 'SS')
    fname = ''.join(c for c in fname if c in
                    {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                     'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                     'W', 'X', 'Y', 'Z'})

    # special rules
    if fname == 'JAMES':
        code = 'J7'
    elif fname == 'PAT':
        code = 'P7'

    else:
        # A. Prefix treatment
        if fname[:2] in {'GE', 'GI', 'GY'}:
            fname = 'J' + fname[1:]
        elif fname[:2] in {'CE', 'CI', 'CY'}:
            fname = 'S' + fname[1:]
        elif fname[:3] == 'CHR':
            fname = 'K' + fname[1:]
        elif fname[:1] == 'C' and fname[:2] != 'CH':
            fname = 'K' + fname[1:]

        if fname[:2] == 'KN':
            fname = 'N' + fname[1:]
        elif fname[:2] == 'PH':
            fname = 'F' + fname[1:]
        elif fname[:3] in {'WIE', 'WEI'}:
            fname = 'V' + fname[1:]

        if german and fname[:1] in {'W', 'M', 'Y', 'Z'}:
            fname = ({'W': 'V', 'M': 'N', 'Y': 'J', 'Z': 'S'}[fname[0]] +
                     fname[1:])

        code = fname[:1]

        # B. Soundex coding
        # code for Y unspecified, but presumably is 0
        _pshp_translation = dict(zip((ord(_) for _ in
                                      'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                     '01230120022455012523010202'))

        fname = fname.translate(_pshp_translation)
        fname = _delete_consecutive_repeats(fname)

        code += fname[1:]
        syl_ptr = code.find('0')
        syl2_ptr = code[syl_ptr + 1:].find('0')
        if syl_ptr != -1 and syl2_ptr != -1 and syl2_ptr - syl_ptr > -1:
            code = code[:syl_ptr + 2]

        code = code.replace('0', '')  # rule 1

    if max_length != -1:
        if len(code) < max_length:
            code += '0' * (max_length-len(code))
        else:
            code = code[:max_length]

    return code


def henry_early(word, max_length=3):
    """Calculate the early version of the Henry code for a word.

    The early version of Henry coding is given in :cite:`Legare:1972`. This is
    different from the later version defined in :cite:`Henry:1976`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 3)
    :returns: the early Henry code
    :rtype: str

    >>> henry_early('Marchand')
    'MRC'
    >>> henry_early('Beaulieu')
    'BL'
    >>> henry_early('Beaumont')
    'BM'
    >>> henry_early('Legrand')
    'LGR'
    >>> henry_early('Pelletier')
    'PLT'
    """
    _cons = {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q',
             'R', 'S', 'T', 'V', 'W', 'X', 'Z'}
    _vows = {'A', 'E', 'I', 'O', 'U', 'Y'}
    _diph = {'AI': 'E', 'AY': 'E', 'EI': 'E', 'AU': 'O', 'OI': 'O', 'OU': 'O',
             'EU': 'U'}
    # _unaltered = {'B', 'D', 'F', 'J', 'K', 'L', 'M', 'N', 'R', 'T', 'V'}
    _simple = {'W': 'V', 'X': 'S', 'Z': 'S'}

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    if not word:
        return ''

    # Rule Ia seems to be covered entirely in II

    # Rule Ib
    if word[0] in _vows:
        # Ib1
        if (((word[1:2] in _cons-{'M', 'N'} and word[2:3] in _cons) or
             (word[1:2] in _cons and word[2:3] not in _cons))):
            if word[0] == 'Y':
                word = 'I'+word[1:]
        # Ib2
        elif word[1:2] in {'M', 'N'} and word[2:3] in _cons:
            if word[0] == 'E':
                word = 'A'+word[1:]
            elif word[0] in {'I', 'U', 'Y'}:
                word = 'E'+word[1:]
        # Ib3
        elif word[:2] in _diph:
            word = _diph[word[:2]]+word[2:]
        # Ib4
        elif word[1:2] in _vows and word[0] == 'Y':
            word = 'I' + word[1:]

    code = ''
    skip = 0

    # Rule II
    for pos, char in enumerate(word):
        nxch = word[pos+1:pos+2]
        prev = word[pos-1:pos]

        if skip:
            skip -= 1
        elif char in _vows:
            code += char
        # IIc
        elif char == nxch:
            skip = 1
            code += char
        elif word[pos:pos+2] in {'CQ', 'DT', 'SC'}:
            continue
        # IIb
        elif char in _simple:
            code += _simple[char]
        elif char in {'C', 'G', 'P', 'Q', 'S'}:
            if char == 'C':
                if nxch in {'A', 'O', 'U', 'L', 'R'}:
                    code += 'K'
                elif nxch in {'E', 'I', 'Y'}:
                    code += 'S'
                elif nxch == 'H':
                    if word[pos+2:pos+3] in _vows:
                        code += 'C'
                    else:  # CHR, CHL, etc.
                        code += 'K'
                else:
                    code += 'C'
            elif char == 'G':
                if nxch in {'A', 'O', 'U', 'L', 'R'}:
                    code += 'G'
                elif nxch in {'E', 'I', 'Y'}:
                    code += 'J'
                elif nxch == 'N':
                    code += 'N'
            elif char == 'P':
                if nxch != 'H':
                    code += 'P'
                else:
                    code += 'F'
            elif char == 'Q':
                if word[pos+1:pos+3] in {'UE', 'UI', 'UY'}:
                    code += 'G'
                else:  # QUA, QUO, etc.
                    code += 'K'
            else:  # S...
                if word[pos:pos+6] == 'SAINTE':
                    code += 'X'
                    skip = 5
                elif word[pos:pos+5] == 'SAINT':
                    code += 'X'
                    skip = 4
                elif word[pos:pos+3] == 'STE':
                    code += 'X'
                    skip = 2
                elif word[pos:pos+2] == 'ST':
                    code += 'X'
                    skip = 1
                elif nxch in _cons:
                    continue
                else:
                    code += 'S'
        # IId
        elif char == 'H' and prev in _cons:
            continue
        elif char in _cons-{'L', 'R'} and nxch in _cons-{'L', 'R'}:
            continue
        elif char == 'L' and nxch in {'M', 'N'}:
            continue
        elif char in {'M', 'N'} and prev in _vows and nxch in _cons:
            continue
        # IIa
        else:
            code += char

    # IIe1
    if code[-4:] in {'AULT', 'EULT', 'OULT'}:
        code = code[:-2]
    # The following are blocked by rules above
    # elif code[-4:-3] in _vows and code[-3:] == 'MPS':
    #    code = code[:-3]
    # elif code[-3:-2] in _vows and code[-2:] in {'MB', 'MP', 'ND',
    #                                             'NS', 'NT'}:
    #    code = code[:-2]
    elif code[-2:-1] == 'R' and code[-1:] in _cons:
        code = code[:-1]
    # IIe2
    elif code[-2:-1] in _vows and code[-1:] in {'D', 'M', 'N', 'S', 'T'}:
        code = code[:-1]
    elif code[-2:] == 'ER':
        code = code[:-1]

    # Drop non-initial vowels
    code = code[:1]+code[1:].translate({65: '', 69: '', 73: '', 79: '', 85: '',
                                        89: ''})

    if max_length != -1:
            code = code[:max_length]

    return code


def norphone(word):
    """Return the Norphone code.

    The reference implementation by Lars Marius Garshol is available in
    :cite:`Garshol:2015`.

    Norphone was designed for Norwegian, but this implementation has been
    extended to support Swedish vowels as well. This function incorporates
    the "not implemented" rules from the above file's rule set.

    :param str word: the word to transform
    :returns: the Norphone code
    :rtype: str

    >>> norphone('Hansen')
    'HNSN'
    >>> norphone('Larsen')
    'LRSN'
    >>> norphone('Aagaard')
    'ÅKRT'
    >>> norphone('Braaten')
    'BRTN'
    >>> norphone('Sandvik')
    'SNVK'
    """
    _vowels = {'A', 'E', 'I', 'O', 'U', 'Y', 'Å', 'Æ', 'Ø', 'Ä', 'Ö'}

    replacements = {4: {'SKEI': 'X'},
                    3: {'SKJ': 'X', 'KEI': 'X'},
                    2: {'CH': 'K', 'CK': 'K', 'GJ': 'J', 'GH': 'K', 'HG': 'K',
                        'HJ': 'J', 'HL': 'L', 'HR': 'R', 'KJ': 'X', 'KI': 'X',
                        'LD': 'L', 'ND': 'N', 'PH': 'F', 'TH': 'T', 'SJ': 'X'},
                    1: {'W': 'V', 'X': 'KS', 'Z': 'S', 'D': 'T', 'G': 'K'}}

    word = word.upper()

    code = ''
    skip = 0

    if word[0:2] == 'AA':
        code = 'Å'
        skip = 2
    elif word[0:2] == 'GI':
        code = 'J'
        skip = 2
    elif word[0:3] == 'SKY':
        code = 'X'
        skip = 3
    elif word[0:2] == 'EI':
        code = 'Æ'
        skip = 2
    elif word[0:2] == 'KY':
        code = 'X'
        skip = 2
    elif word[:1] == 'C':
        code = 'K'
        skip = 1
    elif word[:1] == 'Ä':
        code = 'Æ'
        skip = 1
    elif word[:1] == 'Ö':
        code = 'Ø'
        skip = 1

    if word[-2:] == 'DT':
        word = word[:-2]+'T'
    # Though the rules indicate this rule applies in all positions, the
    # reference implementation indicates it applies only in final position.
    elif word[-2:-1] in _vowels and word[-1:] == 'D':
        word = word[:-2]

    for pos, char in enumerate(word):
        if skip:
            skip -= 1
        else:
            for length in sorted(replacements, reverse=True):
                if word[pos:pos+length] in replacements[length]:
                    code += replacements[length][word[pos:pos+length]]
                    skip = length-1
                    break
            else:
                if not pos or char not in _vowels:
                    code += char

    code = _delete_consecutive_repeats(code)

    return code


def dolby(word, max_length=-1, keep_vowels=False, vowel_char='*'):
    r"""Return the Dolby Code of a name.

    This follows "A Spelling Equivalent Abbreviation Algorithm For Personal
    Names" from :cite:`Dolby:1970` and :cite:`Cunningham:1969`.

    :param word: the word to encode
    :param max_length: maximum length of the returned Dolby code -- this also
        activates the fixed-length code mode if it is greater than 0
    :param keep_vowels: if True, retains all vowel markers
    :param vowel_char: the vowel marker character (default to \*)
    :returns: the Dolby Code
    :rtype: str

    >>> dolby('Hansen')
    'H*NSN'
    >>> dolby('Larsen')
    'L*RSN'
    >>> dolby('Aagaard')
    '*GR'
    >>> dolby('Braaten')
    'BR*DN'
    >>> dolby('Sandvik')
    'S*NVK'
    >>> dolby('Hansen', max_length=6)
    'H*NS*N'
    >>> dolby('Larsen', max_length=6)
    'L*RS*N'
    >>> dolby('Aagaard', max_length=6)
    '*G*R  '
    >>> dolby('Braaten', max_length=6)
    'BR*D*N'
    >>> dolby('Sandvik', max_length=6)
    'S*NF*K'

    >>> dolby('Smith')
    'SM*D'
    >>> dolby('Waters')
    'W*DRS'
    >>> dolby('James')
    'J*MS'
    >>> dolby('Schmidt')
    'SM*D'
    >>> dolby('Ashcroft')
    '*SKRFD'
    >>> dolby('Smith', max_length=6)
    'SM*D  '
    >>> dolby('Waters', max_length=6)
    'W*D*RS'
    >>> dolby('James', max_length=6)
    'J*M*S '
    >>> dolby('Schmidt', max_length=6)
    'SM*D  '
    >>> dolby('Ashcroft', max_length=6)
    '*SKRFD'
    """
    _vowels = {'A', 'E', 'I', 'O', 'U', 'Y'}

    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    # Rule 1 (FL2)
    if word[:3] in {'MCG', 'MAG', 'MAC'}:
        word = 'MK'+word[3:]
    elif word[:2] == 'MC':
        word = 'MK'+word[2:]

    # Rule 2 (FL3)
    pos = len(word)-2
    while pos > -1:
        if word[pos:pos+2] in {'DT', 'LD', 'ND', 'NT', 'RC', 'RD', 'RT', 'SC',
                               'SK', 'ST'}:
            word = word[:pos+1]+word[pos+2:]
            pos += 1
        pos -= 1

    # Rule 3 (FL4)
    # Although the rule indicates "after the first letter", the test cases make
    # it clear that these apply to the first letter also.
    word = word.replace('X', 'KS')
    word = word.replace('CE', 'SE')
    word = word.replace('CI', 'SI')
    word = word.replace('CY', 'SI')

    # not in the rule set, but they seem to have intended it
    word = word.replace('TCH', 'CH')

    pos = word.find('CH', 1)
    while pos != -1:
        if word[pos-1:pos] not in _vowels:
            word = word[:pos]+'S'+word[pos+1:]
        pos = word.find('CH', pos+1)

    word = word.replace('C', 'K')
    word = word.replace('Z', 'S')

    word = word.replace('WR', 'R')
    word = word.replace('DG', 'G')
    word = word.replace('QU', 'K')
    word = word.replace('T', 'D')
    word = word.replace('PH', 'F')

    # Rule 4 (FL5)
    # Although the rule indicates "after the first letter", the test cases make
    # it clear that these apply to the first letter also.
    pos = word.find('K', 0)
    while pos != -1:
        if pos > 1 and word[pos-1:pos] not in _vowels | {'L', 'N', 'R'}:
            word = word[:pos-1]+word[pos:]
            pos -= 1
        pos = word.find('K', pos+1)

    # Rule FL6
    if max_length > 0 and word[-1:] == 'E':
        word = word[:-1]

    # Rule 5 (FL7)
    word = _delete_consecutive_repeats(word)

    # Rule 6 (FL8)
    if word[:2] == 'PF':
        word = word[1:]
    if word[-2:] == 'PF':
        word = word[:-1]
    elif word[-2:] == 'GH':
        if word[-3:-2] in _vowels:
            word = word[:-2]+'F'
        else:
            word = word[:-2]+'G'
    word = word.replace('GH', '')

    # Rule FL9
    if max_length > 0:
        word = word.replace('V', 'F')

    # Rules 7-9 (FL10-FL12)
    first = 1 + (1 if max_length > 0 else 0)
    code = ''
    for pos, char in enumerate(word):
        if char in _vowels:
            if first or keep_vowels:
                code += vowel_char
                first -= 1
        elif pos > 0 and char in {'W', 'H'}:
            continue
        else:
            code += char

    if max_length > 0:
        # Rule FL13
        if len(code) > max_length and code[-1:] == 'S':
            code = code[:-1]
        if keep_vowels:
            code = code[:max_length]
        else:
            # Rule FL14
            code = code[:max_length + 2]
            # Rule FL15
            while len(code) > max_length:
                vowels = len(code) - max_length
                excess = vowels - 1
                word = code
                code = ''
                for char in word:
                    if char == vowel_char:
                        if vowels:
                            code += char
                            vowels -= 1
                    else:
                        code += char
                code = code[:max_length + excess]

        # Rule FL16
        code += ' ' * (max_length - len(code))

    return code


def phonetic_spanish(word, max_length=-1):
    """Return the PhoneticSpanish coding of word.

    This follows the coding described in :cite:`Amon:2012` and
    :cite:`delPilarAngeles:2015`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to
        unlimited)
    :returns: the PhoneticSpanish code
    :rtype: str

    >>> phonetic_spanish('Perez')
    '094'
    >>> phonetic_spanish('Martinez')
    '69364'
    >>> phonetic_spanish('Gutierrez')
    '83994'
    >>> phonetic_spanish('Santiago')
    '4638'
    >>> phonetic_spanish('Nicolás')
    '6454'
    """
    _es_soundex_translation = dict(zip((ord(_) for _ in
                                        'BCDFGHJKLMNPQRSTVXYZ'),
                                       '14328287566079431454'))

    # uppercase, normalize, and decompose, filter to A-Z minus vowels & W
    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = ''.join(c for c in word if c in
                   {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
                    'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z'})

    # merge repeated Ls & Rs
    word = word.replace('LL', 'L')
    word = word.replace('R', 'R')

    # apply the Soundex algorithm
    sdx = word.translate(_es_soundex_translation)

    if max_length > 0:
        sdx = (sdx+('0'*max_length))[:max_length]

    return sdx


def spanish_metaphone(word, max_length=6, modified=False):
    """Return the Spanish Metaphone of a word.

    This is a quick rewrite of the Spanish Metaphone Algorithm, as presented at
    https://github.com/amsqr/Spanish-Metaphone and discussed in
    :cite:`Mosquera:2012`.

    Modified version based on :cite:`delPilarAngeles:2016`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 6)
    :param bool modified: Set to True to use del Pilar Angeles &
        Bailón-Miguel's modified version of the algorithm
    :returns: the Spanish Metaphone code
    :rtype: str

    >>> spanish_metaphone('Perez')
    'PRZ'
    >>> spanish_metaphone('Martinez')
    'MRTNZ'
    >>> spanish_metaphone('Gutierrez')
    'GTRRZ'
    >>> spanish_metaphone('Santiago')
    'SNTG'
    >>> spanish_metaphone('Nicolás')
    'NKLS'
    """
    def _is_vowel(pos):
        """Return True if the character at word[pos] is a vowel."""
        return (pos < len(word) and
                word[pos] in {'A', 'E', 'I', 'O', 'U'})

    word = unicode_normalize('NFC', text_type(word.upper()))

    meta_key = ''
    pos = 0

    # do some replacements for the modified version
    if modified:
        word = word.replace('MB', 'NB')
        word = word.replace('MP', 'NP')
        word = word.replace('BS', 'S')
        if word[:2] == 'PS':
            word = word[1:]

    # simple replacements
    word = word.replace('Á', 'A')
    word = word.replace('CH', 'X')
    word = word.replace('Ç', 'S')
    word = word.replace('É', 'E')
    word = word.replace('Í', 'I')
    word = word.replace('Ó', 'O')
    word = word.replace('Ú', 'U')
    word = word.replace('Ñ', 'NY')
    word = word.replace('GÜ', 'W')
    word = word.replace('Ü', 'U')
    word = word.replace('B', 'V')
    word = word.replace('LL', 'Y')

    while len(meta_key) < max_length:
        if pos >= len(word):
            break

        # get the next character
        current_char = word[pos]

        # if a vowel in pos 0, add to key
        if _is_vowel(pos) and pos == 0:
            meta_key += current_char
            pos += 1
        # otherwise, do consonant rules
        else:
            # simple consonants (unmutated)
            if current_char in {'D', 'F', 'J', 'K', 'M', 'N', 'P', 'T', 'V',
                                'L', 'Y'}:
                meta_key += current_char
                # skip doubled consonants
                if word[pos+1:pos+2] == current_char:
                    pos += 2
                else:
                    pos += 1
            else:
                if current_char == 'C':
                    # special case 'acción', 'reacción',etc.
                    if word[pos+1:pos+2] == 'C':
                        meta_key += 'X'
                        pos += 2
                    # special case 'cesar', 'cien', 'cid', 'conciencia'
                    elif word[pos+1:pos+2] in {'E', 'I'}:
                        meta_key += 'Z'
                        pos += 2
                    # base case
                    else:
                        meta_key += 'K'
                        pos += 1
                elif current_char == 'G':
                    # special case 'gente', 'ecologia',etc
                    if word[pos + 1:pos + 2] in {'E', 'I'}:
                        meta_key += 'J'
                        pos += 2
                    # base case
                    else:
                        meta_key += 'G'
                        pos += 1
                elif current_char == 'H':
                    # since the letter 'H' is silent in Spanish,
                    # set the meta key to the vowel after the letter 'H'
                    if _is_vowel(pos+1):
                        meta_key += word[pos+1]
                        pos += 2
                    else:
                        meta_key += 'H'
                        pos += 1
                elif current_char == 'Q':
                    if word[pos+1:pos+2] == 'U':
                        pos += 2
                    else:
                        pos += 1
                    meta_key += 'K'
                elif current_char == 'W':
                    meta_key += 'U'
                    pos += 1
                elif current_char == 'R':
                    meta_key += 'R'
                    pos += 1
                elif current_char == 'S':
                    if not _is_vowel(pos+1) and pos == 0:
                        meta_key += 'ES'
                        pos += 1
                    else:
                        meta_key += 'S'
                        pos += 1
                elif current_char == 'Z':
                    meta_key += 'Z'
                    pos += 1
                elif current_char == 'X':
                    if len(word) > 1 and pos == 0 and not _is_vowel(pos+1):
                        meta_key += 'EX'
                        pos += 1
                    else:
                        meta_key += 'X'
                        pos += 1
                else:
                    pos += 1

    # Final change from S to Z in modified version
    if modified:
        meta_key = meta_key.replace('S', 'Z')

    return meta_key


def metasoundex(word, lang='en'):
    """Return the MetaSoundex code for a word.

    This is based on :cite:`Koneru:2017`. Only English ('en') and Spanish
    ('es') languages are supported, as in the original.

    :param str word: the word to transform
    :param str lang: either 'en' for English or 'es' for Spanish
    :returns: the MetaSoundex code
    :rtype: str

    >>> metasoundex('Smith')
    '4500'
    >>> metasoundex('Waters')
    '7362'
    >>> metasoundex('James')
    '1520'
    >>> metasoundex('Schmidt')
    '4530'
    >>> metasoundex('Ashcroft')
    '0261'
    >>> metasoundex('Perez', lang='es')
    '094'
    >>> metasoundex('Martinez', lang='es')
    '69364'
    >>> metasoundex('Gutierrez', lang='es')
    '83994'
    >>> metasoundex('Santiago', lang='es')
    '4638'
    >>> metasoundex('Nicolás', lang='es')
    '6754'
    """
    _metasoundex_translation = dict(zip((ord(_) for _ in
                                         'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                        '07430755015866075943077514'))

    if lang == 'es':
        return phonetic_spanish(spanish_metaphone(word))

    word = soundex(metaphone(word))
    word = word[0].translate(_metasoundex_translation)+word[1:]

    return word


def soundex_br(word, max_length=4, zero_pad=True):
    """Return the SoundexBR encoding of a word.

    This is based on :cite:`Marcelino:2015`.

    :param str word: the word to transform
    :param int max_length: the length of the code returned (defaults to 4)
    :param bool zero_pad: pad the end of the return value with 0s to achieve a
        max_length string
    :returns: the SoundexBR code
    :rtype: str

    >>> soundex_br('Oliveira')
    'O416'
    >>> soundex_br('Almeida')
    'A453'
    >>> soundex_br('Barbosa')
    'B612'
    >>> soundex_br('Araújo')
    'A620'
    >>> soundex_br('Gonçalves')
    'G524'
    >>> soundex_br('Goncalves')
    'G524'
    """
    _soundex_br_translation = dict(zip((ord(_) for _ in
                                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                                       '01230120022455012623010202'))

    word = unicode_normalize('NFKD', text_type(word.upper()))
    word = ''.join(c for c in word if c in
                   {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'})

    if word[:2] == 'WA':
        first = 'V'
    elif word[:1] == 'K' and word[1:2] in {'A', 'O', 'U'}:
        first = 'C'
    elif word[:1] == 'C' and word[1:2] in {'I', 'E'}:
        first = 'S'
    elif word[:1] == 'G' and word[1:2] in {'E', 'I'}:
        first = 'J'
    elif word[:1] == 'Y':
        first = 'I'
    elif word[:1] == 'H':
        first = word[1:2]
        word = word[1:]
    else:
        first = word[:1]

    sdx = first + word[1:].translate(_soundex_br_translation)
    sdx = _delete_consecutive_repeats(sdx)
    sdx = sdx.replace('0', '')

    if zero_pad:
        sdx += ('0'*max_length)

    return sdx[:max_length]


def nrl(word):
    """Return the Naval Research Laboratory phonetic encoding of a word.

    This is defined by :cite:`Elovitz:1976`.

    :param str word: the word to transform
    :returns: the NRL phonetic encoding
    :rtype: str

    >>> nrl('the')
    'DHAX'
    >>> nrl('round')
    'rAWnd'
    >>> nrl('quick')
    'kwIHk'
    >>> nrl('eaten')
    'IYtEHn'
    >>> nrl('Smith')
    'smIHTH'
    >>> nrl('Larsen')
    'lAArsEHn'
    """
    def _to_regex(pattern, left_match=True):
        new_pattern = ''
        replacements = {'#': '[AEIOU]+',
                        ':': '[BCDFGHJKLMNPQRSTVWXYZ]*',
                        '^': '[BCDFGHJKLMNPQRSTVWXYZ]',
                        '.': '[BDVGJLMNTWZ]',
                        '%': '(ER|E|ES|ED|ING|ELY)',
                        '+': '[EIY]',
                        ' ': '^'}
        for char in pattern:
            new_pattern += (replacements[char] if char in replacements
                            else char)

        if left_match:
            new_pattern += '$'
            if '^' not in pattern:
                new_pattern = '^.*' + new_pattern
        else:
            new_pattern = '^' + new_pattern.replace('^', '$')
            if '$' not in new_pattern:
                new_pattern += '.*$'

        return new_pattern

    rules = {' ': (('', ' ', '', ' '),
                   ('', '-', '', ''),
                   ('.', '\'S', '', 'z'),
                   ('#:.E', '\'S', '', 'z'),
                   ('#', '\'S', '', 'z'),
                   ('', '\'', '', ''),
                   ('', ',', '', ' '),
                   ('', '.', '', ' '),
                   ('', '?', '', ' '),
                   ('', '!', '', ' ')),
             'A': (('', 'A', ' ', 'AX'),
                   (' ', 'ARE', ' ', 'AAr'),
                   (' ', 'AR', 'O', 'AXr'),
                   ('', 'AR', '#', 'EHr'),
                   ('^', 'AS', '#', 'EYs'),
                   ('', 'A', 'WA', 'AX'),
                   ('', 'AW', '', 'AO'),
                   (' :', 'ANY', '', 'EHnIY'),
                   ('', 'A', '^+#', 'EY'),
                   ('#:', 'ALLY', '', 'AXlIY'),
                   (' ', 'AL', '#', 'AXl'),
                   ('', 'AGAIN', '', 'AXgEHn'),
                   ('#:', 'AG', 'E', 'IHj'),
                   ('', 'A', '^+:#', 'AE'),
                   (' :', 'A', '^+ ', 'EY'),
                   ('', 'A', '^%', 'EY'),
                   (' ', 'ARR', '', 'AXr'),
                   ('', 'ARR', '', 'AEr'),
                   (' :', 'AR', ' ', 'AAr'),
                   ('', 'AR', ' ', 'ER'),
                   ('', 'AR', '', 'AAr'),
                   ('', 'AIR', '', 'EHr'),
                   ('', 'AI', '', 'EY'),
                   ('', 'AY', '', 'EY'),
                   ('', 'AU', '', 'AO'),
                   ('#:', 'AL', ' ', 'AXl'),
                   ('#:', 'ALS', ' ', 'AXlz'),
                   ('', 'ALK', '', 'AOk'),
                   ('', 'AL', '^', 'AOl'),
                   (' :', 'ABLE', '', 'EYbAXl'),
                   ('', 'ABLE', '', 'AXbAXl'),
                   ('', 'ANG', '+', 'EYnj'),
                   ('', 'A', '', 'AE')),
             'B': ((' ', 'BE', '^#', 'bIH'),
                   ('', 'BEING', '', 'bIYIHNG'),
                   (' ', 'BOTH', ' ', 'bOWTH'),
                   (' ', 'BUS', '#', 'bIHz'),
                   ('', 'BUIL', '', 'bIHl'),
                   ('', 'B', '', 'b')),
             'C': ((' ', 'CH', '^', 'k'),
                   ('^E', 'CH', '', 'k'),
                   ('', 'CH', '', 'CH'),
                   (' S', 'CI', '#', 'sAY'),
                   ('', 'CI', 'A', 'SH'),
                   ('', 'CI', 'O', 'SH'),
                   ('', 'CI', 'EN', 'SH'),
                   ('', 'C', '+', 's'),
                   ('', 'CK', '', 'k'),
                   ('', 'COM', '%', 'kAHm'),
                   ('', 'C', '', 'k')),
             'D': (('#:', 'DED', ' ', 'dIHd'),
                   ('.E', 'D', ' ', 'd'),
                   ('#:^E', 'D', ' ', 't'),
                   (' ', 'DE', '^#', 'dIH'),
                   (' ', 'DO', ' ', 'dUW'),
                   (' ', 'DOES', '', 'dAHz'),
                   (' ', 'DOING', '', 'dUWIHNG'),
                   (' ', 'DOW', '', 'dAW'),
                   ('', 'DU', 'A', 'jUW'),
                   ('', 'D', '', 'd')),
             'E': (('#:', 'E', ' ', ''),
                   ('\':^', 'E', ' ', ''),
                   (' :', 'E', ' ', 'IY'),
                   ('#', 'ED', ' ', 'd'),
                   ('#:', 'E', 'D ', ''),
                   ('', 'EV', 'ER', 'EHv'),
                   ('', 'E', '^%', 'IY'),
                   ('', 'ERI', '#', 'IYrIY'),
                   ('', 'ERI', '', 'EHrIH'),
                   ('#:', 'ER', '#', 'ER'),
                   ('', 'ER', '#', 'EHr'),
                   ('', 'ER', '', 'ER'),
                   (' ', 'EVEN', '', 'IYvEHn'),
                   ('#:', 'E', 'W', ''),
                   ('T', 'EW', '', 'UW'),
                   ('S', 'EW', '', 'UW'),
                   ('R', 'EW', '', 'UW'),
                   ('D', 'EW', '', 'UW'),
                   ('L', 'EW', '', 'UW'),
                   ('Z', 'EW', '', 'UW'),
                   ('N', 'EW', '', 'UW'),
                   ('J', 'EW', '', 'UW'),
                   ('TH', 'EW', '', 'UW'),
                   ('CH', 'EW', '', 'UW'),
                   ('SH', 'EW', '', 'UW'),
                   ('', 'EW', '', 'yUW'),
                   ('', 'E', 'O', 'IY'),
                   ('#:S', 'ES', ' ', 'IHz'),
                   ('#:C', 'ES', ' ', 'IHz'),
                   ('#:G', 'ES', ' ', 'IHz'),
                   ('#:Z', 'ES', ' ', 'IHz'),
                   ('#:X', 'ES', ' ', 'IHz'),
                   ('#:J', 'ES', ' ', 'IHz'),
                   ('#:CH', 'ES', ' ', 'IHz'),
                   ('#:SH', 'ES', ' ', 'IHz'),
                   ('#:', 'E', 'S ', ''),
                   ('#:', 'ELY', ' ', 'lIY'),
                   ('#:', 'EMENT', '', 'mEHnt'),
                   ('', 'EFUL', '', 'fUHl'),
                   ('', 'EE', '', 'IY'),
                   ('', 'EARN', '', 'ERn'),
                   (' ', 'EAR', '^', 'ER'),
                   ('', 'EAD', '', 'EHd'),
                   ('#:', 'EA', ' ', 'IYAX'),
                   ('', 'EA', 'SU', 'EH'),
                   ('', 'EA', '', 'IY'),
                   ('', 'EIGH', '', 'EY'),
                   ('', 'EI', '', 'IY'),
                   (' ', 'EYE', '', 'AY'),
                   ('', 'EY', '', 'IY'),
                   ('', 'EU', '', 'yUW'),
                   ('', 'E', '', 'EH')),
             'F': (('', 'FUL', '', 'fUHl'),
                   ('', 'F', '', 'f')),
             'G': (('', 'GIV', '', 'gIHv'),
                   (' ', 'G', 'I^', 'g'),
                   ('', 'GE', 'T', 'gEH'),
                   ('SU', 'GGES', '', 'gjEHs'),
                   ('', 'GG', '', 'g'),
                   (' B#', 'G', '', 'g'),
                   ('', 'G', '+', 'j'),
                   ('', 'GREAT', '', 'grEYt'),
                   ('#', 'GH', '', ''),
                   ('', 'G', '', 'g')),
             'H': ((' ', 'HAV', '', 'hAEv'),
                   (' ', 'HERE', '', 'hIYr'),
                   (' ', 'HOUR', '', 'AWER'),
                   ('', 'HOW', '', 'hAW'),
                   ('', 'H', '#', 'h'),
                   ('', 'H', '', '')),
             'I': ((' ', 'IN', '', 'IHn'),
                   (' ', 'I', ' ', 'AY'),
                   ('', 'IN', 'D', 'AYn'),
                   ('', 'IER', '', 'IYER'),
                   ('#:R', 'IED', '', 'IYd'),
                   ('', 'IED', ' ', 'AYd'),
                   ('', 'IEN', '', 'IYEHn'),
                   ('', 'IE', 'T', 'AYEH'),
                   (' :', 'I', '%', 'AY'),
                   ('', 'I', '%', 'IY'),
                   ('', 'IE', '', 'IY'),
                   ('', 'I', '^+:#', 'IH'),
                   ('', 'IR', '#', 'AYr'),
                   ('', 'IZ', '%', 'AYz'),
                   ('', 'IS', '%', 'AYz'),
                   ('', 'I', 'D%', 'AY'),
                   ('+^', 'I', '^+', 'IH'),
                   ('', 'I', 'T%', 'AY'),
                   ('#:^', 'I', '^+', 'IH'),
                   ('', 'I', '^+', 'AY'),
                   ('', 'IR', '', 'ER'),
                   ('', 'IGH', '', 'AY'),
                   ('', 'ILD', '', 'AYld'),
                   ('', 'IGN', ' ', 'AYn'),
                   ('', 'IGN', '^', 'AYn'),
                   ('', 'IGN', '%', 'AYn'),
                   ('', 'IQUE', '', 'IYk'),
                   ('', 'I', '', 'IH')),
             'J': (('', 'J', '', 'j'),),
             'K': ((' ', 'K', 'N', ''),
                   ('', 'K', '', 'k')),
             'L': (('', 'LO', 'C#', 'lOW'),
                   ('L', 'L', '', ''),
                   ('#:^', 'L', '%', 'AXl'),
                   ('', 'LEAD', '', 'lIYd'),
                   ('', 'L', '', 'l')),
             'M': (('', 'MOV', '', 'mUWv'),
                   ('', 'M', '', 'm')),
             'N': (('E', 'NG', '+', 'nj'),
                   ('', 'NG', 'R', 'NGg'),
                   ('', 'NG', '#', 'NGg'),
                   ('', 'NGL', '%', 'NGgAXl'),
                   ('', 'NG', '', 'NG'),
                   ('', 'NK', '', 'NGk'),
                   (' ', 'NOW', ' ', 'nAW'),
                   ('', 'N', '', 'n')),
             'O': (('', 'OF', ' ', 'AXv'),
                   ('', 'OROUGH', '', 'EROW'),
                   ('#:', 'OR', ' ', 'ER'),
                   ('#:', 'ORS', ' ', 'ERz'),
                   ('', 'OR', '', 'AOr'),
                   (' ', 'ONE', '', 'wAHn'),
                   ('', 'OW', '', 'OW'),
                   (' ', 'OVER', '', 'OWvER'),
                   ('', 'OV', '', 'AHv'),
                   ('', 'O', '^%', 'OW'),
                   ('', 'O', '^EN', 'OW'),
                   ('', 'O', '^I#', 'OW'),
                   ('', 'OL', 'D', 'OWl'),
                   ('', 'OUGHT', '', 'AOt'),
                   ('', 'OUGH', '', 'AHf'),
                   (' ', 'OU', '', 'AW'),
                   ('H', 'OU', 'S#', 'AW'),
                   ('', 'OUS', '', 'AXs'),
                   ('', 'OUR', '', 'AOr'),
                   ('', 'OULD', '', 'UHd'),
                   ('^', 'OU', '^L', 'AH'),
                   ('', 'OUP', '', 'UWp'),
                   ('', 'OU', '', 'AW'),
                   ('', 'OY', '', 'OY'),
                   ('', 'OING', '', 'OWIHNG'),
                   ('', 'OI', '', 'OY'),
                   ('', 'OOR', '', 'AOr'),
                   ('', 'OOK', '', 'UHk'),
                   ('', 'OOD', '', 'UHd'),
                   ('', 'OO', '', 'UW'),
                   ('', 'O', 'E', 'OW'),
                   ('', 'O', ' ', 'OW'),
                   ('', 'OA', '', 'OW'),
                   (' ', 'ONLY', '', 'OWnlIY'),
                   (' ', 'ONCE', '', 'wAHns'),
                   ('', 'ON\'T', '', 'OWnt'),
                   ('C', 'O', 'N', 'AA'),
                   ('', 'O', 'NG', 'AO'),
                   (' :^', 'O', 'N', 'AH'),
                   ('I', 'ON', '', 'AXn'),
                   ('#:', 'ON', ' ', 'AXn'),
                   ('#^', 'ON', '', 'AXn'),
                   ('', 'O', 'ST ', 'OW'),
                   ('', 'OF', '^', 'AOf'),
                   ('', 'OTHER', '', 'AHDHER'),
                   ('', 'OSS', ' ', 'AOs'),
                   ('#:^', 'OM', '', 'AHm'),
                   ('', 'O', '', 'AA')),
             'P': (('', 'PH', '', 'f'),
                   ('', 'PEOP', '', 'pIYp'),
                   ('', 'POW', '', 'pAW'),
                   ('', 'PUT', ' ', 'pUHt'),
                   ('', 'P', '', 'p')),
             'Q': (('', 'QUAR', '', 'kwAOr'),
                   ('', 'QU', '', 'kw'),
                   ('', 'Q', '', 'k')),
             'R': ((' ', 'RE', '^#', 'rIY'),
                   ('', 'R', '', 'r')),
             'S': (('', 'SH', '', 'SH'),
                   ('#', 'SION', '', 'ZHAXn'),
                   ('', 'SOME', '', 'sAHm'),
                   ('#', 'SUR', '#', 'ZHER'),
                   ('', 'SUR', '#', 'SHER'),
                   ('#', 'SU', '#', 'ZHUW'),
                   ('#', 'SSU', '#', 'SHUW'),
                   ('#', 'SED', ' ', 'zd'),
                   ('#', 'S', '#', 'z'),
                   ('', 'SAID', '', 'sEHd'),
                   ('^', 'SION', '', 'SHAXn'),
                   ('', 'S', 'S', ''),
                   ('.', 'S', ' ', 'z'),
                   ('#:.E', 'S', ' ', 'z'),
                   ('#:^##', 'S', ' ', 'z'),
                   ('#:^#', 'S', ' ', 's'),
                   ('U', 'S', ' ', 's'),
                   (' :#', 'S', ' ', 'z'),
                   (' ', 'SCH', '', 'sk'),
                   ('', 'S', 'C+', ''),
                   ('#', 'SM', '', 'zm'),
                   ('#', 'SN', '\'', 'zAXn'),
                   ('', 'S', '', 's')),
             'T': ((' ', 'THE', ' ', 'DHAX'),
                   ('', 'TO', ' ', 'tUW'),
                   ('', 'THAT', ' ', 'DHAEt'),
                   (' ', 'THIS', ' ', 'DHIHs'),
                   (' ', 'THEY', '', 'DHEY'),
                   (' ', 'THERE', '', 'DHEHr'),
                   ('', 'THER', '', 'DHER'),
                   ('', 'THEIR', '', 'DHEHr'),
                   (' ', 'THAN', ' ', 'DHAEn'),
                   (' ', 'THEM', ' ', 'DHEHm'),
                   ('', 'THESE', ' ', 'DHIYz'),
                   (' ', 'THEN', '', 'DHEHn'),
                   ('', 'THROUGH', '', 'THrUW'),
                   ('', 'THOSE', '', 'DHOWz'),
                   ('', 'THOUGH', ' ', 'DHOW'),
                   (' ', 'THUS', '', 'DHAHs'),
                   ('', 'TH', '', 'TH'),
                   ('#:', 'TED', ' ', 'tIHd'),
                   ('S', 'TI', '#N', 'CH'),
                   ('', 'TI', 'O', 'SH'),
                   ('', 'TI', 'A', 'SH'),
                   ('', 'TIEN', '', 'SHAXn'),
                   ('', 'TUR', '#', 'CHER'),
                   ('', 'TU', 'A', 'CHUW'),
                   (' ', 'TWO', '', 'tUW'),
                   ('', 'T', '', 't')),
             'U': ((' ', 'UN', 'I', 'yUWn'),
                   (' ', 'UN', '', 'AHn'),
                   (' ', 'UPON', '', 'AXpAOn'),
                   ('T', 'UR', '#', 'UHr'),
                   ('S', 'UR', '#', 'UHr'),
                   ('R', 'UR', '#', 'UHr'),
                   ('D', 'UR', '#', 'UHr'),
                   ('L', 'UR', '#', 'UHr'),
                   ('Z', 'UR', '#', 'UHr'),
                   ('N', 'UR', '#', 'UHr'),
                   ('J', 'UR', '#', 'UHr'),
                   ('TH', 'UR', '#', 'UHr'),
                   ('CH', 'UR', '#', 'UHr'),
                   ('SH', 'UR', '#', 'UHr'),
                   ('', 'UR', '#', 'yUHr'),
                   ('', 'UR', '', 'ER'),
                   ('', 'U', '^ ', 'AH'),
                   ('', 'U', '^^', 'AH'),
                   ('', 'UY', '', 'AY'),
                   (' G', 'U', '#', ''),
                   ('G', 'U', '%', ''),
                   ('G', 'U', '#', 'w'),
                   ('#N', 'U', '', 'yUW'),
                   ('T', 'U', '', 'UW'),
                   ('S', 'U', '', 'UW'),
                   ('R', 'U', '', 'UW'),
                   ('D', 'U', '', 'UW'),
                   ('L', 'U', '', 'UW'),
                   ('Z', 'U', '', 'UW'),
                   ('N', 'U', '', 'UW'),
                   ('J', 'U', '', 'UW'),
                   ('TH', 'U', '', 'UW'),
                   ('CH', 'U', '', 'UW'),
                   ('SH', 'U', '', 'UW'),
                   ('', 'U', '', 'yUW')),
             'V': (('', 'VIEW', '', 'vyUW'),
                   ('', 'V', '', 'v')),
             'W': ((' ', 'WERE', '', 'wER'),
                   ('', 'WA', 'S', 'wAA'),
                   ('', 'WA', 'T', 'wAA'),
                   ('', 'WHERE', '', 'WHEHr'),
                   ('', 'WHAT', '', 'WHAAt'),
                   ('', 'WHOL', '', 'hOWl'),
                   ('', 'WHO', '', 'hUW'),
                   ('', 'WH', '', 'WH'),
                   ('', 'WAR', '', 'wAOr'),
                   ('', 'WOR', '^', 'wER'),
                   ('', 'WR', '', 'r'),
                   ('', 'W', '', 'w')),
             'X': (('', 'X', '', 'ks'),),
             'Y': (('', 'YOUNG', '', 'yAHNG'),
                   (' ', 'YOU', '', 'yUW'),
                   (' ', 'YES', '', 'yEHs'),
                   (' ', 'Y', '', 'y'),
                   ('#:^', 'Y', ' ', 'IY'),
                   ('#:^', 'Y', 'I', 'IY'),
                   (' :', 'Y', ' ', 'AY'),
                   (' :', 'Y', '#', 'AY'),
                   (' :', 'Y', '^+:#', 'IH'),
                   (' :', 'Y', '^#', 'AY'),
                   ('', 'Y', '', 'IH')),
             'Z': (('', 'Z', '', 'z'),)}

    word = word.upper()

    pron = ''
    pos = 0
    while pos < len(word):
        left_orig = word[:pos]
        right_orig = word[pos:]
        first = word[pos] if word[pos] in rules else ' '
        for rule in rules[first]:
            left, match, right, out = rule
            if right_orig.startswith(match):
                if left:
                    l_pattern = _to_regex(left, left_match=True)
                if right:
                    r_pattern = _to_regex(right, left_match=False)
                if ((not left or re_match(l_pattern, left_orig)) and
                        (not right or
                         re_match(r_pattern, right_orig[len(match):]))):
                    pron += out
                    pos += len(match)
                    break
        else:
            pron += word[pos]
            pos += 1

    return pron


def bmpm(word, language_arg=0, name_mode='gen', match_mode='approx',
         concat=False, filter_langs=False):
    """Return the Beider-Morse Phonetic Matching algorithm code for a word.

    The Beider-Morse Phonetic Matching algorithm is described in
    :cite:`Beider:2008`.
    The reference implementation is licensed under GPLv3.

    :param str word: the word to transform
    :param str language_arg: the language of the term; supported values
        include:

            - 'any'
            - 'arabic'
            - 'cyrillic'
            - 'czech'
            - 'dutch'
            - 'english'
            - 'french'
            - 'german'
            - 'greek'
            - 'greeklatin'
            - 'hebrew'
            - 'hungarian'
            - 'italian'
            - 'latvian'
            - 'polish'
            - 'portuguese'
            - 'romanian'
            - 'russian'
            - 'spanish'
            - 'turkish'

    :param str name_mode: the name mode of the algorithm:

            - 'gen' -- general (default)
            - 'ash' -- Ashkenazi
            - 'sep' -- Sephardic

    :param str match_mode: matching mode: 'approx' or 'exact'
    :param bool concat: concatenation mode
    :param bool filter_langs: filter out incompatible languages
    :returns: the BMPM value(s)
    :rtype: tuple

    >>> bmpm('Christopher')
    'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir xristofir
    xristYfir xristopi xritopir xritopi xristofi xritofir xritofi tzristopir
    tzristofir zristopir zristopi zritopir zritopi zristofir zristofi zritofir
    zritofi'
    >>> bmpm('Niall')
    'nial niol'
    >>> bmpm('Smith')
    'zmit'
    >>> bmpm('Schmidt')
    'zmit stzmit'

    >>> bmpm('Christopher', language_arg='German')
    'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir xristofir
    xristYfir'
    >>> bmpm('Christopher', language_arg='English')
    'tzristofir tzrQstofir tzristafir tzrQstafir xristofir xrQstofir xristafir
    xrQstafir'
    >>> bmpm('Christopher', language_arg='German', name_mode='ash')
    'xrQstopir xrQstYpir xristopir xristYpir xrQstofir xrQstYfir xristofir
    xristYfir'

    >>> bmpm('Christopher', language_arg='German', match_mode='exact')
    'xriStopher xriStofer xristopher xristofer'
    """
    return _bmpm(word, language_arg, name_mode, match_mode,
                 concat, filter_langs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
