# -*- coding: utf-8 -*-
"""abydos.phonetic

The phonetic module implements phonetic algorithms including:
    Robert C. Russell's Index
    American Soundex
    Daitch-Mokotoff Soundex
    Kölner Phonetik
    NYSIIS
    Match Rating Algorithm
    Metaphone
    Double Metaphone
    Caverphone
    Alpha Search Inquiry System
    Fuzzy Soundex
    Phonex
    Phonem
    Phonix
    SfinxBis
    phonet
    Standardized Phonetic Frequency Code
    Beider-Morse Phonetic Matching


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
from ._compat import _unicode, _range
from itertools import groupby
from collections import Counter
import re
import unicodedata
from ._bm import _bmpm


def _delete_consecutive_repeats(word):
    """Return word with all contiguous repeating characters collapsed to
    a single instance
    """
    return ''.join(char for char, _ in groupby(word))


def russell_index(word):
    """Return the Russell Index of a word as an int

    Arguments:
    word -- the word to translate to a Russell Index value

    Description:
    This follows Robert C. Russell's Index algorithm, as described in
    US Patent 1,261,167 (1917)
    """
    _russell_translation = dict(zip([ord(_) for _ in
                                           u'ABCDEFGIKLMNOPQRSTUVXYZ'],
                                          u'12341231356712383412313'))

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = word.replace('ß', 'SS')
    word = word.replace('GH', '')  # discard gh (rule 3)
    word = word.rstrip('SZ') # discard /[sz]$/ (rule 3)

    # translate according to Russell's mapping
    word = ''.join([c for c in word if c in tuple('ABCDEFGIKLMNOPQRSTUVXYZ')])
    sdx = word.translate(_russell_translation)

    # remove any 1s after the first occurrence
    one = sdx.find('1')+1
    if one:
        sdx = sdx[:one] + ''.join([c for c in sdx[one:] if  c != '1'])

    # remove repeating characters
    sdx = _delete_consecutive_repeats(sdx)

    # return as an int
    return int(sdx) if sdx else None


def russell_index_num_to_alpha(num):
    """Return the Russell Index alphabetic string of a Index number

    Arguments:
    num -- an integer representing a Russell Index

    Description:
    This follows Robert C. Russell's Index algorithm, as described in
    US Patent 1,261,167 (1917)
    """
    _russell_num_translation = dict(zip([ord(_) for _ in u'12345678'],
                                        u'ABCDLMNR'))
    num = ''.join([c for c in _unicode(num) if c in tuple('12345678')])
    if num:
        return num.translate(_russell_num_translation)


def russell_index_alpha(word):
    """Return the Russell Index of a word as an alphabetic string

    Arguments:
    word -- the word to translate to a Russell Index value

    Description:
    This follows Robert C. Russell's Index algorithm, as described in
    US Patent 1,261,167 (1917)
    """
    if word:
        return russell_index_num_to_alpha(russell_index(word))


def soundex(word, maxlength=4, var='American', reverse=False):
    """Return the Soundex value of a word

    Arguments:
    word -- the word to translate to Soundex
    maxlength -- the length of the code returned (defaults to 4)
    var -- the variant of the algorithm to employ (defaults to 'American'):
        'American' follows the American Soundex algorithm, as described at
        http://www.archives.gov/publications/general-info-leaflets/55-census.html
        and in Knuth(1998:394); this is also called Miracode
        'special' follows the rules from the 1880-1910 US Census, in which
        h & w are not treated as blocking consonants but as vowels
        'dm' computes the Daitch-Mokotoff Soundex
    reverse -- reverse the word before computing the selected Soundex
        (defaults to False); This results in "Reverse Soundex"
    """
    _soundex_translation = dict(zip([ord(_) for _ in
                                     u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
                                    u'01230129022455012623019202'))

    # Call the D-M Soundex function itself if requested
    if var == 'dm':
        return dm_soundex(word, maxlength, reverse)

    # Require a maxlength of at least 4
    maxlength = max(4, maxlength)

    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    # Nothing to convert, return base case
    if not word:
        return '0'*maxlength

    # Reverse word if computing Reverse Soundex
    if reverse:
        word = word[::-1]

    # apply the Soundex algorithm
    sdx = word.translate(_soundex_translation)

    if var == 'special':
        sdx = sdx.replace('9', '0') # special rule for 1880-1910 census
    else:
        sdx = sdx.replace('9', '') # rule 1
    sdx = _delete_consecutive_repeats(sdx) # rule 3

    if word[0] in 'HW':
        sdx = word[0] + sdx
    else:
        sdx = word[0] + sdx[1:]
    sdx = sdx.replace('0', '') # rule 1

    sdx += ('0'*maxlength) # rule 4

    return sdx[:maxlength]


def dm_soundex(word, maxlength=6, reverse=False):
    """Return the Daitch-Mokotoff Soundex values of a word as a set
        A collection is necessary since there can be multiple values for a
        single word.

    Arguments:
    word -- the word to translate to D-M Soundex
    maxlength -- the length of the code returned (defaults to 4)
    reverse -- reverse the word before computing the selected Soundex (defaults
        to False); This results in "Reverse Soundex"
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
                  'CH':((5, 4), (5, 4), (5, 4)),
                  'CK':((5, 45), (5, 45), (5, 45)),
                  'C':((5, 4), (5, 4), (5, 4)),
                  'J':((1, 4), ('_', 4), ('_', 4)),
                  'RZ':((94, 4), (94, 4), (94, 4)),
                  'RS':((94, 4), (94, 4), (94, 4))}

    _dms_order = {'A':('AI', 'AJ', 'AU', 'AY', 'A'), 'B':('B'),
                 'C':('CHS', 'CSZ', 'CZS', 'CH', 'CK', 'CS', 'CZ', 'C'),
                 'D':('DRS', 'DRZ', 'DSH', 'DSZ', 'DZH', 'DZS', 'DS', 'DT',
                      'DZ', 'D'), 'E':('EI', 'EJ', 'EU', 'EY', 'E'),
                  'F':('FB', 'F'), 'G':('G'), 'H':('H'),
                  'I':('IA', 'IE', 'IO', 'IU', 'I'), 'J':('J'),
                  'K':('KH', 'KS', 'K'), 'L':('L'), 'M':('MN', 'M'),
                  'N':('NM', 'N'), 'O':('OI', 'OJ', 'OY', 'O'),
                  'P':('PF', 'PH', 'P'), 'Q':('Q'), 'R':('RS', 'RZ', 'R'),
                  'S':('SCHTSCH', 'SCHTCH', 'SCHTSH', 'SHTCH', 'SHTSH', 'STSCH',
                       'SCHD', 'SCHT', 'SHCH', 'STCH', 'STRS', 'STRZ', 'STSH',
                       'SZCS', 'SZCZ', 'SCH', 'SHD', 'SHT', 'SZD', 'SZT', 'SC',
                       'SD', 'SH', 'ST', 'SZ', 'S'),
                  'T':('TTSCH', 'TSCH', 'TTCH', 'TTSZ', 'TCH', 'THS', 'TRS',
                       'TRZ', 'TSH', 'TSZ', 'TTS', 'TTZ', 'TZS', 'TC', 'TH',
                       'TS', 'TZ', 'T'), 'U':('UE', 'UI', 'UJ', 'UY', 'U'),
                  'V':('V'), 'W':('W'), 'X':('X'), 'Y':('Y'),
                  'Z':('ZHDZH', 'ZDZH', 'ZSCH', 'ZDZ', 'ZHD', 'ZSH', 'ZD', 'ZH',
                       'ZS', 'Z')}

    _vowels = tuple('AEIJOUY')
    dms = [''] # initialize empty code list

    # Require a maxlength of at least 6
    maxlength = max(6, maxlength)

    # uppercase, normalize, decompose, and filter non-A-Z
    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    # Nothing to convert, return base case
    if not word:
        return set(['0'*maxlength])

    # Reverse word if computing Reverse Soundex
    if reverse:
        word = word[::-1]

    pos = 0
    while pos < len(word):
        # Iterate through _dms_order, which specifies the possible substrings
        # for which codes exist in the Daitch-Mokotoff coding
        for sstr in _dms_order[word[pos]]:
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
                    dms = [_ + _unicode(dm_val[0]) for _ in dms] \
                            + [_ + _unicode(dm_val[1]) for _ in dms]
                else:
                    dms = [_ + _unicode(dm_val) for _ in dms]
                pos += len(sstr)
                break

    # Filter out double letters and _ placeholders
    dms = [''.join([c for c in _delete_consecutive_repeats(_) if c != '_'])
          for _ in dms]

    # Trim codes and return set
    dms = [(_ + ('0'*maxlength))[:maxlength] for _ in dms]
    return set(dms)


def koelner_phonetik(word):
    """Return the Kölner Phonetik code for a word

    Arguments:
    word -- the word to translate to a Kölner Phonetik code

    Description:
    Based on the algorithm described at
    https://de.wikipedia.org/wiki/Kölner_Phonetik
    """
    def _after(word, i, letters):
        """Return True if word[i] follows one of the supplied letters
        """
        if i > 0 and word[i-1] in tuple(letters):
            return True
        return False

    def _before(word, i, letters):
        """Return True if word[i] precedes one of the supplied letters
        """
        if i+1 < len(word) and word[i+1] in tuple(letters):
            return True
        return False

    _vowels = tuple('AEIJYOU')

    sdx = ''

    word = word.replace('ß', 'SS')
    word = unicodedata.normalize('NFKD', _unicode(word.upper()))

    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    # Nothing to convert, return base case
    if not word:
        return sdx

    for i in _range(len(word)):
        if word[i] in _vowels:
            sdx += '0'
        elif word[i] in 'B':
            sdx += '1'
        elif word[i] in 'P':
            if _before(word, i, 'H'):
                sdx += '3'
            else:
                sdx += '1'
        elif word[i] in 'DT':
            if _before(word, i, 'CSZ'):
                sdx += '8'
            else:
                sdx += '2'
        elif word[i] in 'FVW':
            sdx += '3'
        elif word[i] in 'GKQ':
            sdx += '4'
        elif word[i] in 'C':
            if _after(word, i, 'SZ'):
                sdx += '8'
            elif i == 0:
                if _before(word, i, 'AHKLOQRUX'):
                    sdx += '4'
                else:
                    sdx += '8'
            elif _before(word, i, 'AHKOQUX'):
                sdx += '4'
            else:
                sdx += '8'
        elif word[i] in 'X':
            if _after(word, i, 'CKQ'):
                sdx += '8'
            else:
                sdx += '48'
        elif word[i] in 'L':
            sdx += '5'
        elif word[i] in 'MN':
            sdx += '6'
        elif word[i] in 'R':
            sdx += '7'
        elif word[i] in 'SZ':
            sdx += '8'

    sdx = _delete_consecutive_repeats(sdx)

    sdx = sdx[0] + sdx[1:].replace('0', '')

    return sdx


def koelner_phonetik_num_to_alpha(num):
    """Given the numeric form of a Kölner Phonetik value, returns an
    alphabetic form
    """
    _koelner_num_translation = dict(zip([ord(_) for _ in u'012345678'],
                                        u'APTFKLNRS'))
    num = ''.join([c for c in _unicode(num) if c in tuple('012345678')])
    return num.translate(_koelner_num_translation)


def koelner_phonetik_alpha(word):
    """Given a string 'word', returns an alphabetic value representing
    its Kölner Phonetik value
    """
    return koelner_phonetik_num_to_alpha(koelner_phonetik(word))


def nysiis(word, maxlength=6):
    """Return the New York State Identification and Intelligence System
        (NYSIIS) coding of a string

    Arguments:
    word -- the word to apply the match rating approach to
    maxlength -- the maximum length (default 6) of the code to return

    Description:
    A description of the algorithm can be found at
    https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System
    """
    # Require a maxlength of at least 6
    maxlength = max(6, maxlength)

    _vowels = tuple('AEIOU')

    word = ''.join([c for c in word.upper() if c.isalpha()])

    if word.startswith('MAC'):
        word = 'MCC'+word[3:]
    if word.startswith('KN'):
        word = 'NN'+word[2:]
    if word.startswith('K'):
        word = 'C'+word[1:]
    if word.startswith('PH') or word.startswith('PF'):
        word = 'FF'+word[2:]
    if word.startswith('SCH'):
        word = 'SSS'+word[3:]

    if word.endswith('EE') or word.endswith('IE'):
        word = word[:-2]+'Y'
    if (word.endswith('DT') or word.endswith('RT') or word.endswith('RD') or
        word.endswith('NT') or word.endswith('ND')):
        word = word[:-2]+'D'

    key = word[0]

    skip = 0
    for i in _range(1, len(word)):
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
        elif word[i:i+3] == 'SCH':
            word = word[:i] + 'SSS' + word[i+3:]
            skip = 2
        elif word[i:i+2] == 'PH':
            word = word[:i] + 'FF' + word[i+2:]
            skip = 1
        elif word[i] == 'H' and (word[i-1] not in _vowels or
                                 word[i+1:i+2] not in _vowels):
            word = word[:i] + word[i-1] + word[i+1:]
        elif word[i] == 'W' and word[i-1] in _vowels:
            word = word[:i] + word[i-1] + word[i+1:]

        if word[i:i+skip+1] != key[-1:]:
            key += word[i:i+skip+1]

    key = _delete_consecutive_repeats(key)

    if key[-1] == 'S':
        key = key[:-1]
    if key[-2:] == 'AY':
        key = key[:-2] + 'Y'
    if key[-1:] == 'A':
        key = key[:-1]

    return key[:maxlength]


def mra(word):
    """Return the personal numeric identifier (PNI) for a word, derived by the
        Western Airlines Surname Match Rating Algorithm

    Arguments:
    word -- the word to apply the match rating approach to

    Description:
    A description of the algorithm can be found on page 18 of
    https://archive.org/details/accessingindivid00moor
    """
    word = word.upper()
    word = word[0]+''.join([c for c in word[1:] if c not in tuple('AEIOU')])
    word = _delete_consecutive_repeats(word)
    if len(word) > 6:
        word = word[:3]+word[-3:]
    return word


def metaphone(word, maxlength=float('inf')):
    """Return the Metaphone encoding of a word

    Arguments:
    word -- the word to apply the Metaphone algorithm to
    maxlength -- the maximum length of the returned Metaphone code
        (defaults to unlimited, but in Philips' original implementation
        this was 4)

    Description:
    Based on Lawrence Philips' BASIC code from 1990:
    http://aspell.net/metaphone/metaphone.basic
    This incorporates some corrections to the above code, particularly
    some of those suggested by Michael Kuhn in:
    http://aspell.net/metaphone/metaphone-kuhn.txt
    """
    # pylint: disable=too-many-branches
    _vowels = tuple('AEIOU')
    _frontv = tuple('EIY')
    _varson = tuple('CSPTG')

    # Require a maxlength of at least 4
    maxlength = max(4, maxlength)

    # As in variable sound--those modified by adding an "h"
    ename = ''.join([c for c in word.upper() if c.isalnum()])

    # Delete nonalphanumeric characters and make all caps
    if ename == '':
        return ''
    if ename[0:2] in ['PN', 'AE', 'KN', 'GN', 'WR']:
        ename = ename[1:]
    elif ename[0] == 'X':
        ename = 'S' + ename[1:]
    elif ename[0:2] == 'WH':
        ename = 'W' + ename[2:]

    # Convert to metaph
    elen = len(ename)-1
    metaph = ''
    for i in _range(len(ename)):
        if len(metaph) >= maxlength:
            break
        if ename[i] not in 'GT' and i > 0 and ename[i-1] == ename[i]:
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
            if (i > 0 and ename[i-1] in _vowels and
                ename[i+1:i+2] not in _vowels):
                continue
            elif i > 0 and ename[i-1] in _varson:
                continue
            else:
                metaph += 'H'

        elif ename[i] in 'FJLMNR':
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
            if (i > 0 and i+2 <= elen and ename[i+1] == 'I' and
                ename[i+2] in 'OA'):
                metaph += 'X'
            elif ename[i+1:i+2] == 'H':
                metaph += 'X'
            else:
                metaph += 'S'

        elif ename[i] == 'T':
            if (i > 0 and i+2 <= elen and ename[i+1] == 'I' and
                ename[i+2] in 'OA'):
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


def double_metaphone(word, maxlength=float('inf')):
    """Return the Double Metaphone encodings of a word as a tuple

    Arguments:
    word -- the word to apply the Double Metaphone algorithm to
    maxlength -- the maximum length of the returned Double Metaphone codes
        (defaults to unlimited, but in Philips' original implementation this
        was 4)

    Description:
    Based on Lawrence Philips' (Visual) C++ code from 1999:
    http://aspell.net/metaphone/dmetaph.cpp
    """
    # pylint: disable=too-many-branches
    # Require a maxlength of at least 4
    maxlength = max(4, maxlength)

    primary = ''
    secondary = ''

    def _slavo_germanic():
        """Return True if the word appears to be Slavic or Germanic
        """
        if 'W' in word or 'K' in word or 'CZ' in word:
            return True
        return False

    def _metaph_add(pri, sec=''):
        """Return a new metaphone tuple with the supplied additional elements
        """
        newpri = primary
        newsec = secondary
        if pri:
            newpri += pri
        if sec:
            if sec != ' ':
                newsec += sec
        else:
            if pri and (pri != ' '):
                newsec += pri
        return (newpri, newsec)

    def _is_vowel(pos):
        """Return true if the character at word[pos] is a vowel
        """
        if pos < 0:
            return False
        return word[pos] in tuple('AEIOUY')

    def _get_at(pos):
        """Return the character at word[pos]
        """
        if not pos < 0:
            return word[pos]

    def _string_at(pos, slen, substrings):
        """Return True if word[pos:pos+slen] is in substrings
        """
        if pos < 0:
            return False
        return word[pos:pos+slen] in substrings

    current = 0
    length = len(word)
    if length < 0:
        return ''
    last = length - 1

    word = word.upper()

    # Pad the original string so that we can index beyond the edge of the world
    word += '     '

    # Skip these when at start of word
    if word[0:2] in ['GN', 'KN', 'PN', 'WR', 'PS']:
        current += 1

    # Initial 'X' is pronounced 'Z' e.g. 'Xavier'
    if _get_at(0) == 'X':
        (primary, secondary) = _metaph_add('S') # 'Z' maps to 'S'
        current += 1

    # Main loop
    while True:
        if current >= length:
            break

        if _get_at(current) in tuple('AEIOUY'):
            if current == 0:
                # All init vowels now map to 'A'
                (primary, secondary) = _metaph_add('A')
            current += 1
            continue

        elif _get_at(current) == 'B':
            # "-mb", e.g", "dumb", already skipped over...
            (primary, secondary) = _metaph_add('P')
            if _get_at(current + 1) == 'B':
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'Ç':
            (primary, secondary) = _metaph_add('S')
            current += 1
            continue

        elif _get_at(current) == 'C':
            # Various Germanic
            if (current > 1 and not _is_vowel(current - 2) and
                _string_at((current - 1), 3, ["ACH"]) and
                ((_get_at(current + 2) != 'I') and
                 ((_get_at(current + 2) != 'E') or
                  _string_at((current - 2), 6, ["BACHER", "MACHER"])))):
                (primary, secondary) = _metaph_add("K")
                current += 2
                continue

            # Special case 'caesar'
            elif current == 0 and _string_at(current, 6, ["CAESAR"]):
                (primary, secondary) = _metaph_add("S")
                current += 2
                continue

            # Italian 'chianti'
            elif _string_at(current, 4, ["CHIA"]):
                (primary, secondary) = _metaph_add("K")
                current += 2
                continue

            elif _string_at(current, 2, ["CH"]):
                # Find 'Michael'
                if  current > 0 and _string_at(current, 4, ["CHAE"]):
                    (primary, secondary) = _metaph_add("K", "X")
                    current += 2
                    continue

                # Greek roots e.g. 'chemistry', 'chorus'
                elif (current == 0 and
                      (_string_at((current + 1), 5, ["HARAC", "HARIS"]) or
                       _string_at((current + 1), 3, ["HOR", "HYM",
                                                     "HIA", "HEM"]))
                      and not _string_at(0, 5, ["CHORE"])):
                    (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

                # Germanic, Greek, or otherwise 'ch' for 'kh' sound
                elif ((_string_at(0, 4, ["VAN ", "VON "]) or
                       _string_at(0, 3, ["SCH"]))
                      # 'architect but not 'arch', 'orchestra', 'orchid'
                      or _string_at((current - 2), 6,
                                    ["ORCHES", "ARCHIT", "ORCHID"])
                      or _string_at((current + 2), 1, ["T", "S"])
                      or ((_string_at((current - 1), 1,
                                      ["A", "O", "U", "E"]) or (current == 0))
                          # e.g., 'wachtler', 'wechsler', but not 'tichner'
                          and _string_at((current + 2), 1,
                                         ["L", "R", "N", "M", "B", "H", "F",
                                          "V", "W", " "]))):
                    (primary, secondary) = _metaph_add("K")

                else:
                    if current > 0:
                        if _string_at(0, 2, ["MC"]):
                            # e.g., "McHugh"
                            (primary, secondary) = _metaph_add("K")
                        else:
                            (primary, secondary) = _metaph_add("X", "K")
                    else:
                        (primary, secondary) = _metaph_add("X")

                current += 2
                continue

            # e.g, 'czerny'
            elif (_string_at(current, 2, ["CZ"]) and
                  not _string_at((current - 2), 4, ["WICZ"])):
                (primary, secondary) = _metaph_add("S", "X")
                current += 2
                continue

            # e.g., 'focaccia'
            elif _string_at((current + 1), 3, ["CIA"]):
                (primary, secondary) = _metaph_add("X")
                current += 3

            # double 'C', but not if e.g. 'McClellan'
            elif (_string_at(current, 2, ["CC"]) and
                  not ((current == 1) and (_get_at(0) == 'M'))):
                # 'bellocchio' but not 'bacchus'
                if (_string_at((current + 2), 1, ["I", "E", "H"]) and
                    not _string_at((current + 2), 2, ["HU"])):
                    # 'accident', 'accede' 'succeed'
                    if (((current == 1) and _get_at(current - 1) == 'A')
                        or _string_at((current - 1), 5, ["UCCEE", "UCCES"])):
                        (primary, secondary) = _metaph_add("KS")
                    # 'bacci', 'bertucci', other italian
                    else:
                        (primary, secondary) = _metaph_add("X")
                    current += 3
                    continue
                else: # Pierce's rule
                    (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

            elif _string_at(current, 2, ["CK", "CG", "CQ"]):
                (primary, secondary) = _metaph_add("K")
                current += 2
                continue

            elif _string_at(current, 2, ["CI", "CE", "CY"]):
                # Italian vs. English
                if _string_at(current, 3, ["CIO", "CIE", "CIA"]):
                    (primary, secondary) = _metaph_add("S", "X")
                else:
                    (primary, secondary) = _metaph_add("S")
                current += 2
                continue

            # else
            else:
                (primary, secondary) = _metaph_add("K")

                # name sent in 'mac caffrey', 'mac gregor
                if _string_at((current + 1), 2, [" C", " Q", " G"]):
                    current += 3
                elif (_string_at((current + 1), 1, ["C", "K", "Q"])
                      and not _string_at((current + 1), 2, ["CE", "CI"])):
                    current += 2
                else:
                    current += 1
                continue

        elif _get_at(current) == 'D':
            if _string_at(current, 2, ["DG"]):
                if _string_at((current + 2), 1, ["I", "E", "Y"]):
                    # e.g. 'edge'
                    (primary, secondary) = _metaph_add("J")
                    current += 3
                    continue
                else:
                    # e.g. 'edgar'
                    (primary, secondary) = _metaph_add("TK")
                    current += 2
                    continue

            elif _string_at(current, 2, ["DT", "DD"]):
                (primary, secondary) = _metaph_add("T")
                current += 2
                continue

            # else
            else:
                (primary, secondary) = _metaph_add("T")
                current += 1
                continue

        elif _get_at(current) == 'F':
            if _get_at(current + 1) == 'F':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("F")
            continue

        elif _get_at(current) == 'G':
            if _get_at(current + 1) == 'H':
                if (current > 0) and not _is_vowel(current - 1):
                    (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

                # 'ghislane', ghiradelli
                elif current == 0:
                    if _get_at(current + 2) == 'I':
                        (primary, secondary) = _metaph_add("J")
                    else:
                        (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

                # Parker's rule (with some further refinements) - e.g., 'hugh'
                elif (((current > 1) and
                       _string_at((current - 2), 1, ["B", "H", "D"]))
                    # e.g., 'bough'
                    or ((current > 2) and
                        _string_at((current - 3), 1, ["B", "H", "D"]))
                    # e.g., 'broughton'
                    or ((current > 3) and
                        _string_at((current - 4), 1, ["B", "H"]))):
                    current += 2
                    continue
                else:
                    # e.g. 'laugh', 'McLaughlin', 'cough',
                    #      'gough', 'rough', 'tough'
                    if ((current > 2)
                         and (_get_at(current - 1) == 'U')
                         and (_string_at((current - 3), 1,
                                         ["C", "G", "L", "R", "T"]))):
                        (primary, secondary) = _metaph_add("F")
                    elif (current > 0) and _get_at(current - 1) != 'I':
                        (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

            elif _get_at(current + 1) == 'N':
                if (current == 1) and _is_vowel(0) and not _slavo_germanic():
                    (primary, secondary) = _metaph_add("KN", "N")
                # not e.g. 'cagney'
                elif (not _string_at((current + 2), 2, ["EY"]) and
                      (_get_at(current + 1) != 'Y') and
                      not _slavo_germanic()):
                    (primary, secondary) = _metaph_add("N", "KN")
                else:
                    (primary, secondary) = _metaph_add("KN")
                current += 2
                continue

            # 'tagliaro'
            elif _string_at((current + 1), 2, ["LI"]) and not _slavo_germanic():
                (primary, secondary) = _metaph_add("KL", "L")
                current += 2
                continue

            # -ges-, -gep-, -gel-, -gie- at beginning
            elif ((current == 0)
                  and ((_get_at(current + 1) == 'Y')
                       or _string_at((current + 1), 2,
                                     ["ES", "EP", "EB", "EL", "EY", "IB", "IL",
                                      "IN", "IE", "EI", "ER"]))):
                (primary, secondary) = _metaph_add("K", "J")
                current += 2
                continue

            #  -ger-,  -gy-
            elif ((_string_at((current + 1), 2, ["ER"]) or
                   (_get_at(current + 1) == 'Y'))
                  and not _string_at(0, 6, ["DANGER", "RANGER", "MANGER"])
                  and not _string_at((current - 1), 1, ["E", "I"])
                  and not _string_at((current - 1), 3, ["RGY", "OGY"])):
                (primary, secondary) = _metaph_add("K", "J")
                current += 2
                continue

            #  italian e.g, 'biaggi'
            elif (_string_at((current + 1), 1, ["E", "I", "Y"])
                  or _string_at((current - 1), 4, ["AGGI", "OGGI"])):
                # obvious germanic
                if ((_string_at(0, 4, ["VAN ", "VON "]) or
                     _string_at(0, 3, ["SCH"]))
                    or _string_at((current + 1), 2, ["ET"])):
                    (primary, secondary) = _metaph_add("K")
                elif _string_at((current + 1), 4, ["IER "]):
                    (primary, secondary) = _metaph_add("J")
                else:
                    (primary, secondary) = _metaph_add("J", "K")
                current += 2
                continue

            else:
                if _get_at(current + 1) == 'G':
                    current += 2
                else:
                    current += 1
                (primary, secondary) = _metaph_add("K")
                continue

        elif _get_at(current) == 'H':
            # only keep if first & before vowel or btw. 2 vowels
            if (((current == 0) or _is_vowel(current - 1))
                and _is_vowel(current + 1)):
                (primary, secondary) = _metaph_add("H")
                current += 2
            else: # also takes care of 'HH'
                current += 1
            continue

        elif _get_at(current) == 'J':
            # obvious spanish, 'jose', 'san jacinto'
            if _string_at(current, 4, ["JOSE"]) or _string_at(0, 4, ["SAN "]):
                if (((current == 0) and (_get_at(current + 4) == ' ')) or
                    _string_at(0, 4, ["SAN "])):
                    (primary, secondary) = _metaph_add("H")
                else:
                    (primary, secondary) = _metaph_add("J", "H")
                current += 1
                continue

            elif (current == 0) and not _string_at(current, 4, ["JOSE"]):
                # Yankelovich/Jankelowicz
                (primary, secondary) = _metaph_add("J", "A")
            # Spanish pron. of e.g. 'bajador'
            elif (_is_vowel(current - 1)
                  and not _slavo_germanic()
                  and ((_get_at(current + 1) == 'A') or
                       (_get_at(current + 1) == 'O'))):
                (primary, secondary) = _metaph_add("J", "H")
            elif current == last:
                (primary, secondary) = _metaph_add("J", " ")
            elif (not _string_at((current + 1), 1,
                                 ["L", "T", "K", "S", "N", "M", "B", "Z"])
                  and not _string_at((current - 1), 1, ["S", "K", "L"])):
                (primary, secondary) = _metaph_add("J")

            if _get_at(current + 1) == 'J': # it could happen!
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'K':
            if _get_at(current + 1) == 'K':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("K")
            continue

        elif _get_at(current) == 'L':
            if _get_at(current + 1) == 'L':
                # Spanish e.g. 'cabrillo', 'gallegos'
                if (((current == (length - 3))
                     and _string_at((current - 1), 4, ["ILLO", "ILLA", "ALLE"]))
                    or ((_string_at((last - 1), 2, ["AS", "OS"]) or
                         _string_at(last, 1, ["A", "O"]))
                        and _string_at((current - 1), 4, ["ALLE"]))):
                    (primary, secondary) = _metaph_add("L", " ")
                    current += 2
                    continue
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("L")
            continue

        elif _get_at(current) == 'M':
            if((_string_at((current - 1), 3, ["UMB"])
                and (((current + 1) == last) or
                     _string_at((current + 2), 2, ["ER"])))
               # 'dumb', 'thumb'
               or  (_get_at(current + 1) == 'M')):
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("M")
            continue

        elif _get_at(current) == 'N':
            if _get_at(current + 1) == 'N':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("N")
            continue

        elif _get_at(current) == 'Ñ':
            current += 1
            (primary, secondary) = _metaph_add("N")
            continue

        elif _get_at(current) == 'P':
            if _get_at(current + 1) == 'H':
                (primary, secondary) = _metaph_add("F")
                current += 2
                continue

            # also account for "campbell", "raspberry"
            elif _string_at((current + 1), 1, ["P", "B"]):
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("P")
            continue

        elif _get_at(current) == 'Q':
            if _get_at(current + 1) == 'Q':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("K")
            continue

        elif _get_at(current) == 'R':
            # french e.g. 'rogier', but exclude 'hochmeier'
            if ((current == last)
                and not _slavo_germanic()
                and _string_at((current - 2), 2, ["IE"])
                and not _string_at((current - 4), 2, ["ME", "MA"])):
                (primary, secondary) = _metaph_add("", "R")
            else:
                (primary, secondary) = _metaph_add("R")

            if _get_at(current + 1) == 'R':
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'S':
            # special cases 'island', 'isle', 'carlisle', 'carlysle'
            if _string_at((current - 1), 3, ["ISL", "YSL"]):
                current += 1
                continue

            # special case 'sugar-'
            elif (current == 0) and _string_at(current, 5, ["SUGAR"]):
                (primary, secondary) = _metaph_add("X", "S")
                current += 1
                continue

            elif _string_at(current, 2, ["SH"]):
                # Germanic
                if _string_at((current + 1), 4,
                              ["HEIM", "HOEK", "HOLM", "HOLZ"]):
                    (primary, secondary) = _metaph_add("S")
                else:
                    (primary, secondary) = _metaph_add("X")
                current += 2
                continue

            # Italian & Armenian
            elif (_string_at(current, 3, ["SIO", "SIA"]) or
                  _string_at(current, 4, ["SIAN"])):
                if not _slavo_germanic():
                    (primary, secondary) = _metaph_add("S", "X")
                else:
                    (primary, secondary) = _metaph_add("S")
                current += 3
                continue

            # German & anglicisations, e.g. 'smith' match 'schmidt',
            #                               'snider' match 'schneider'
            # also, -sz- in Slavic language although in Hungarian it is
            #       pronounced 's'
            elif (((current == 0)
                   and _string_at((current + 1), 1, ["M", "N", "L", "W"]))
                  or _string_at((current + 1), 1, ["Z"])):
                (primary, secondary) = _metaph_add("S", "X")
                if _string_at((current + 1), 1, ["Z"]):
                    current += 2
                else:
                    current += 1
                continue

            elif _string_at(current, 2, ["SC"]):
                # Schlesinger's rule
                if _get_at(current + 2) == 'H':
                    # dutch origin, e.g. 'school', 'schooner'
                    if _string_at((current + 3), 2,
                                  ["OO", "ER", "EN", "UY", "ED", "EM"]):
                        # 'schermerhorn', 'schenker'
                        if _string_at((current + 3), 2, ["ER", "EN"]):
                            (primary, secondary) = _metaph_add("X", "SK")
                        else:
                            (primary, secondary) = _metaph_add("SK")
                        current += 3
                        continue
                    else:
                        if ((current == 0) and not _is_vowel(3) and
                            (_get_at(3) != 'W')):
                            (primary, secondary) = _metaph_add("X", "S")
                        else:
                            (primary, secondary) = _metaph_add("X")
                        current += 3
                        continue

                elif _string_at((current + 2), 1, ["I", "E", "Y"]):
                    (primary, secondary) = _metaph_add("S")
                    current += 3
                    continue

                # else
                else:
                    (primary, secondary) = _metaph_add("SK")
                    current += 3
                    continue

            else:
                # french e.g. 'resnais', 'artois'
                if (current == last) and _string_at((current - 2), 2,
                                                    ["AI", "OI"]):
                    (primary, secondary) = _metaph_add("", "S")
                else:
                    (primary, secondary) = _metaph_add("S")

                if _string_at((current + 1), 1, ["S", "Z"]):
                    current += 2
                else:
                    current += 1
                continue

        elif _get_at(current) == 'T':
            if _string_at(current, 4, ["TION"]):
                (primary, secondary) = _metaph_add("X")
                current += 3
                continue

            elif _string_at(current, 3, ["TIA", "TCH"]):
                (primary, secondary) = _metaph_add("X")
                current += 3
                continue

            elif (_string_at(current, 2, ["TH"])
                  or _string_at(current, 3, ["TTH"])):
                # special case 'thomas', 'thames' or germanic
                if (_string_at((current + 2), 2, ["OM", "AM"])
                    or _string_at(0, 4, ["VAN ", "VON "])
                    or _string_at(0, 3, ["SCH"])):
                    (primary, secondary) = _metaph_add("T")
                else:
                    (primary, secondary) = _metaph_add("0", "T")
                current += 2
                continue

            elif _string_at((current + 1), 1, ["T", "D"]):
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("T")
            continue

        elif _get_at(current) == 'V':
            if _get_at(current + 1) == 'V':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("F")
            continue

        elif _get_at(current) == 'W':
            # can also be in middle of word
            if _string_at(current, 2, ["WR"]):
                (primary, secondary) = _metaph_add("R")
                current += 2
                continue
            elif ((current == 0)
                  and (_is_vowel(current + 1) or _string_at(current, 2,
                                                            ["WH"]))):
                # Wasserman should match Vasserman
                if _is_vowel(current + 1):
                    (primary, secondary) = _metaph_add("A", "F")
                else:
                    # need Uomo to match Womo
                    (primary, secondary) = _metaph_add("A")

            # Arnow should match Arnoff
            if (((current == last) and _is_vowel(current - 1))
                or _string_at((current - 1), 5,
                              ["EWSKI", "EWSKY", "OWSKI", "OWSKY"])
                or _string_at(0, 3, ["SCH"])):
                (primary, secondary) = _metaph_add("", "F")
                current += 1
                continue
            # Polish e.g. 'filipowicz'
            elif _string_at(current, 4, ["WICZ", "WITZ"]):
                (primary, secondary) = _metaph_add("TS", "FX")
                current += 4
                continue
            # else skip it
            else:
                current += 1
                continue

        elif _get_at(current) == 'X':
            # French e.g. breaux
            if (not ((current == last)
                     and (_string_at((current - 3), 3, ["IAU", "EAU"])
                          or _string_at((current - 2), 2, ["AU", "OU"])))):
                (primary, secondary) = _metaph_add("KS")

            if _string_at((current + 1), 1, ["C", "X"]):
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'Z':
            # Chinese Pinyin e.g. 'zhao'
            if _get_at(current + 1) == 'H':
                (primary, secondary) = _metaph_add("J")
                current += 2
                continue
            elif (_string_at((current + 1), 2, ["ZO", "ZI", "ZA"])
                  or (_slavo_germanic() and ((current > 0) and
                                             _get_at(current - 1) != 'T'))):
                (primary, secondary) = _metaph_add("S", "TS")
            else:
                (primary, secondary) = _metaph_add("S")

            if _get_at(current + 1) == 'Z':
                current += 2
            else:
                current += 1
            continue

        else:
            current += 1

    if maxlength < float('inf'):
        primary = primary[:maxlength]
        secondary = secondary[:maxlength]
    if primary == secondary:
        secondary = ''

    return (primary, secondary)


def caverphone(word, version=2):
    """Return the Caverphone encoding of a word

    Arguments:
    word -- the word to apply the Caverphone algorithm to
    version -- the version of Caverphone to employ for encoding (defaults to 2)

    Description:
    A description of version 1 of the algorithm can be found at:
    http://caversham.otago.ac.nz/files/working/ctp060902.pdf
    A description of version 2 of the algorithm can be found at:
    http://caversham.otago.ac.nz/files/working/ctp150804.pdf
    """
    _vowels = tuple('aeiou')

    word = word.lower()
    word = ''.join([c for c in word if c in
                    tuple('abcdefghijklmnopqrstuvwxyz')])

    # the main replacemet algorithm
    if version != 1 and word.endswith('e'):
        word = word[:-1]
    if word:
        if word.startswith('cough'):
            word = 'cou2f'+word[5:]
        if word.startswith('rough'):
            word = 'rou2f'+word[5:]
        if word.startswith('tough'):
            word = 'tou2f'+word[5:]
        if word.startswith('enough'):
            word = 'enou2f'+word[6:]
        if version != 1 and word.startswith('trough'):
            word = 'trou2f'+word[6:]
        if word.startswith('gn'):
            word = '2n'+word[2:]
        if word.endswith('mb'):
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
            if word.startswith('y3'):
                word = 'Y3'+word[2:]
            if word.startswith('y'):
                word = 'A'+word[1:]
            word = word.replace('y', '3')
        word = word.replace('3gh3', '3kh3')
        word = word.replace('gh', '22')
        word = word.replace('g', 'k')
        word = re.sub(r's+', r'S', word)
        word = re.sub(r't+', r'T', word)
        word = re.sub(r'p+', r'P', word)
        word = re.sub(r'k+', r'K', word)
        word = re.sub(r'f+', r'F', word)
        word = re.sub(r'm+', r'M', word)
        word = re.sub(r'n+', r'N', word)
        word = word.replace('w3', 'W3')
        if version == 1:
            word = word.replace('wy', 'Wy')
        word = word.replace('wh3', 'Wh3')
        if version == 1:
            word = word.replace('why', 'Why')
        if version != 1 and word.endswith('w'):
            word = word[:-1]+'3'
        word = word.replace('w', '2')
        if word.startswith('h'):
            word = 'A'+word[1:]
        word = word.replace('h', '2')
        word = word.replace('r3', 'R3')
        if version == 1:
            word = word.replace('ry', 'Ry')
        if version != 1 and word.endswith('r'):
            word = word[:-1]+'3'
        word = word.replace('r', '2')
        word = word.replace('l3', 'L3')
        if version == 1:
            word = word.replace('ly', 'Ly')
        if version != 1 and word.endswith('l'):
            word = word[:-1]+'3'
        word = word.replace('l', '2')
        if version == 1:
            word = word.replace('j', 'y')
            word = word.replace('y3', 'Y3')
            word = word.replace('y', '2')
        word = word.replace('2', '')
        if version != 1 and word.endswith('3'):
            word = word[:-1]+'A'
        word = word.replace('3', '')

    # pad with 1s, then extract the necessary length of code
    word = word+'1'*10
    if version != 1:
        word = word[:10]
    else:
        word = word[:6]

    return word


def alpha_sis(word, maxlength=14):
    """Return the IBM Alpha Search Inquiry System key of a word as a tuple
        A collection is necessary since there can be multiple values for a
        single word. But the collection must be ordered since the first value
        is the primary coding.

    Arguments:
    word -- the word to apply the Alpha SIS algorithm to
    maxlength -- the length of the code returned (defaults to 14)

    Description:
    Based on the algorithm described in "Accessing individual records from
    personal data files using non-unique identifiers" / Gwendolyn B. Moore,
    et al.; prepared for the Institute for Computer Sciences and Technology,
    National Bureau of Standards, Washington, D.C (1977):
    https://archive.org/stream/accessingindivid00moor#page/15/mode/1up
    """
    _alpha_sis_initials = {'GF':'08', 'GM':'03', 'GN':'02', 'KN':'02',
                           'PF':'08', 'PN':'02', 'PS':'00', 'WR':'04', 'A':'1',
                           'E':'1', 'H':'2', 'I':'1', 'J':'3', 'O':'1', 'U':'1',
                           'W':'4', 'Y':'5'}
    _alpha_sis_initials_order = ('GF', 'GM', 'GN', 'KN', 'PF', 'PN', 'PS', 'WR',
                                 'A', 'E', 'H', 'I', 'J', 'O', 'U', 'W', 'Y')
    _alpha_sis_basic = {'SCH':'6', 'CZ':('70', '6', '0'), 'CH':('6', '70', '0'),
                        'CK':('7', '6'), 'DS':('0', '10'), 'DZ':('0', '10'),
                        'TS':('0', '10'), 'TZ':('0', '10'), 'CI':'0', 'CY':'0',
                        'CE':'0', 'SH':'6', 'DG':'7', 'PH':'8', 'C':('7', '6'),
                        'K':('7', '6'), 'Z':'0', 'S':'0', 'D':'1', 'T':'1',
                        'N':'2', 'M':'3', 'R':'4', 'L':'5', 'J':'6', 'G':'7',
                        'Q':'7', 'X':'7', 'F':'8', 'V':'8', 'B':'9', 'P':'9'}
    _alpha_sis_basic_order = ('SCH', 'CZ', 'CH', 'CK', 'DS', 'DZ', 'TS', 'TZ',
                              'CI', 'CY', 'CE', 'SH', 'DG', 'PH', 'C', 'K', 'Z',
                              'S', 'D', 'T', 'N', 'M', 'R', 'L', 'J', 'C', 'G',
                              'K', 'Q', 'X', 'F', 'V', 'B', 'P')

    alpha = ['']
    pos = 0
    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    # Do special processing for initial substrings
    for k in _alpha_sis_initials_order:
        if word.startswith(k):
            alpha[0] += _alpha_sis_initials[k]
            pos += len(k)
            break

    # Add a '0' if alpha is still empty
    if len(alpha[0]) == 0:
        alpha[0] += '0'

    # Whether or not any special initial codes were encoded, iterate
    # through the length of the word in the main encoding loop
    while pos < len(word):
        origpos = pos
        for k in _alpha_sis_basic_order:
            if word[pos:].startswith(k):
                if isinstance(_alpha_sis_basic[k], tuple):
                    newalpha = []
                    for i in _range(len(_alpha_sis_basic[k])):
                        newalpha += [_ + _alpha_sis_basic[k][i] for _ in alpha]
                    alpha = newalpha
                else:
                    alpha = [_ + _alpha_sis_basic[k] for _ in alpha]
                pos += len(k)
                break
        if pos == origpos:
            alpha = [_ + '_' for _ in alpha]
            pos += 1

    # Trim doublets and placeholders
    for i in _range(len(alpha)):
        pos = 1
        while pos < len(alpha[i]):
            if alpha[i][pos] == alpha[i][pos-1]:
                alpha[i] = alpha[i][:pos]+alpha[i][pos+1:]
            pos += 1
    alpha = [_.replace('_', '') for _ in alpha]

    # Trim codes and return tuple
    alpha = [(_ + ('0'*maxlength))[:maxlength] for _ in alpha]
    return tuple(alpha)


def fuzzy_soundex(word, maxlength=5):
    """Return the Fuzzy Soundex encoding of a word

    Arguments:
    word -- the word to translate to a Phonex encoding
    maxlength -- the length of the code returned (defaults to 4)

    Description:
    Fuzzy Soundex is an algorithm derived from Soundex, defined in:
    Holmes, David and M. Catherine McCabe. "Improving Precision and Recall for
    Soundex Retrieval."
    http://wayback.archive.org/web/20100629121128/http://www.ir.iit.edu/publications/downloads/IEEESoundexV5.pdf
    """
    _fuzzy_soundex_translation = dict(zip([ord(_) for _ in
                                           u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
                                          u'0193017-07745501769301-7-9'))

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))

    if not word:
        return '0' * maxlength

    if word[:2] in ('CS', 'CZ', 'TS', 'TZ'):
        word = 'SS' + word[2:]
    elif word[:2] == 'GN':
        word = 'NN' + word[2:]
    elif word[:2] in ('HR', 'WR'):
        word = 'RR' + word[2:]
    elif word[:2] == 'HW':
        word = 'WW' + word[2:]
    elif word[:2] in ('KN', 'NG'):
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

    if word[0] in 'HWY':
        sdx = word[0] + sdx
    else:
        sdx = word[0] + sdx[1:]

    sdx = sdx.replace('0', '')

    sdx += ('0'*maxlength)

    return sdx[:maxlength]


def phonex(word, maxlength=4):
    """Return the Phonex encoding of a word

    Arguments:
    word -- the word to translate to a Phonex encoding
    maxlength -- the length of the code returned (defaults to 4)

    Description:
    Phonex is an algorithm derived from Soundex, defined in:
    Lait, A. J. and B. Randell. "An Assessment of Name Matching Algorithms".
    http://homepages.cs.ncl.ac.uk/brian.randell/Genealogy/NameMatching.pdf
    """
    name = unicodedata.normalize('NFKD', _unicode(word.upper()))

    name_code = last = ''

    # Deletions effected by replacing with next letter which
    # will be ignored due to duplicate handling of Soundex code.
    # This is faster than 'moving' all subsequent letters.

    # Remove any trailing Ss
    while name.endswith('S'):
        name = name[:-1]

    # Phonetic equivalents of first 2 characters
    # Works since duplicate letters are ignored
    if name.startswith('KN'):
        name = 'N' + name[2:] # KN.. == N..
    elif name.startswith('PH'):
        name = 'F' + name[2:] # PH.. == F.. (H ignored anyway)
    elif name.startswith('WR'):
        name = 'R' + name[2:] # WR.. == R..

    if name:
        # Special case, ignore H first letter (subsequent Hs ignored anyway)
        # Works since duplicate letters are ignored
        if name[0] == 'H':
            name = name[1:]

        # Phonetic equivalents of first character
        if name[0] in 'AEIOUY':
            name = 'A' + name[1:]
        elif name[0] in 'BP':
            name = 'B' + name[1:]
        elif name[0] in 'VF':
            name = 'F' + name[1:]
        elif name[0] in 'KQC':
            name = 'C' + name[1:]
        elif name[0] in 'JG':
            name = 'G' + name[1:]
        elif name[0] in 'ZS':
            name = 'S' + name[1:]

        name_code = last = name[0]

    # MODIFIED SOUNDEX CODE
    for i in _range(1, len(name)):
        if name[i] in 'BPFV':
            code = '1'
        elif name[i] in 'CSKGJQXZ':
            code = '2'
        elif name[i] in 'DT':
            if name[i+1:i+2] != 'C':
                code = '3'
        elif name[i] == 'L':
            if name[i+1:i+2] in tuple('AEIOUY') or i+1 == len(name):
                code = '4'
        elif name[i] in 'MN':
            if name[i+1:i+2] in tuple('DG'):
                name = name[:i+1] + name[i] + name[i+2:]
            code = '5'
        elif name[i] == 'R':
            if name[i+1:i+2] in tuple('AEIOUY') or i+1 == len(name):
                code = '6'
        else:
            code = '0'

        if code != last and code != '0' and i != 0:
            name_code += code

        if len(name_code) == 0:
            last = code
        else:
            last = name_code[-1]

    name_code += '0' * maxlength
    return name_code[:maxlength]


def phonem(word):
    """Return the Phonem encoding of a word

    Arguments:
    word -- the word to translate to a Phonem encoding

    Description:
    Phonem is defined in Wilde, Georg and Carsten Meyer. 1999. "Doppelgaenger
    gesucht - Ein Programm fuer kontextsensitive phonetische Textumwandlung."
    ct Magazin fuer Computer & Technik 25/1999.

    This version is based on the Perl implementation documented at:
    http://phonetik.phil-fak.uni-koeln.de/fileadmin/home/ritters/Allgemeine_Dateien/Martin_Wilz.pdf
    It includes some enhancements presented in the Java port at:
    https://github.com/dcm4che/dcm4che/blob/master/dcm4che-soundex/src/main/java/org/dcm4che3/soundex/Phonem.java

    Phonem is intended chiefly for German names/words.
    """
    _phonem_substitutions = (('SC', 'C'), ('SZ', 'C'), ('CZ', 'C'), ('TZ', 'C'),
                             ('TS', 'C'), ('KS', 'X'), ('PF', 'V'),
                             ('QU', 'KW'), ('PH', 'V'), ('UE', 'Y'),
                             ('AE', 'E'), ('OE', 'Ö'), ('EI', 'AY'),
                             ('EY', 'AY'), ('EU', 'OY'), ('AU', 'A§'),
                             ('OU', '§'))
    _phonem_translation = dict(zip([ord(_) for _ in
                                    u'ZKGQÇÑßFWPTÁÀÂÃÅÄÆÉÈÊËIJÌÍÎÏÜÝ§ÚÙÛÔÒÓÕØ'],
                                   u'CCCCCNSVVBDAAAAAEEEEEEYYYYYYYYUUUUOOOOÖ'))

    word = unicodedata.normalize('NFC', _unicode(word.upper()))
    for i, j in _phonem_substitutions:
        word = word.replace(i, j)
    word = word.translate(_phonem_translation)

    return ''.join([c for c in _delete_consecutive_repeats(word)
                    if c in tuple('ABCDLMNORSUVWXYÖ')])


def phonix(word, maxlength=4):
    """Return the Phonix encoding of a word

    Arguments:
    word -- the word to translate to a Phonix encoding
    maxlength -- the length of the code returned (defaults to 4)

    Description:
    Phonix is a Soundex-like algorithm defined in:
    T.N. Gadd: PHONIX --- The Algorithm, Program 24/4, 1990, p.363-366.

    This implementation is based on
    http://cpansearch.perl.org/src/ULPFR/WAIT-1.800/soundex.c
    http://cs.anu.edu.au/people/Peter.Christen/Febrl/febrl-0.4.01/encode.py
    and
    https://metacpan.org/pod/Text::Phonetic::Phonix
    """
    def _start_repl(word, src, tar, post=None):
        """replace src with tar at the start of word
        in the environment pre__post
        """
        if post:
            for i in tuple(post):
                if word.startswith(src+i):
                    return tar + word[len(src):]
        elif word.startswith(src):
            return tar + word[len(src):]
        return word

    def _end_repl(word, src, tar, pre=None):
        """replace src with tar at the end of word
        in the environment pre__post
        """
        if pre:
            for i in tuple(pre):
                if word.endswith(i+src):
                    return word[:-len(src)] + tar
        elif word.endswith(src):
            return word[:-len(src)] + tar
        return word

    def _mid_repl(word, src, tar, pre=None, post=None):
        """replace src with tar in the middle of word
        in the environment pre__post
        """
        if pre or post:
            if not pre:
                return word[0] + _all_repl(word[1:], src, tar, pre, post)
            elif not post:
                return _all_repl(word[:-1], src, tar, pre, post) + word[-1]
            else:
                return _all_repl(word, src, tar, pre, post)
        else:
            return (word[0] + _all_repl(word[1:-1], src, tar, pre, post)
                    + word[-1])

    def _all_repl(word, src, tar, pre=None, post=None):
        """replace src with tar anywhere in word
        in the environment pre__post
        """
        if pre or post:
            if post:
                post = tuple(post)
            else:
                post = tuple(('',))
            if pre:
                pre = tuple(pre)
            else:
                pre = tuple(('',))

            for i, j in tuple((i, j) for i in pre for j in post):
                word = word.replace(i+src+j, i+tar+j)
            return word
        else:
            return word.replace(src, tar)

    _vow = 'AEIOU'
    _con = 'BCDFGHJKLMNPQRSTVWXYZ'

    _phonix_substitutions = [(_all_repl, 'DG', 'G'),
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
                             (_start_repl, 'CZ', _con),
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
                             (_all_repl, 'MPT', 'MT')]

    _phonix_translation = dict(zip([ord(_) for _ in
                                    u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
                                   u'01230720022455012683070808'))

    sdx = ''

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])
    if word:
        for trans in _phonix_substitutions:
            word = trans[0](word, *trans[1:])
        if word[0] in tuple('AEIOUY'):
            sdx = 'v' + word[1:].translate(_phonix_translation)
        else:
            sdx = word[0] + word[1:].translate(_phonix_translation)
        sdx = _delete_consecutive_repeats(sdx)
        sdx = sdx.replace('0', '')

    sdx += '0' * maxlength
    return sdx[:maxlength]


def sfinxbis(word, maxlength=None):
    """Return the SfinxBis encoding of a word

    Arguments:
    word -- the word to translate to a SfinxBis encoding
    maxlength -- the length of the code returned (defaults to unlimited)

    Description:
    SfinxBis is a Soundex-like algorithm defined in:
    http://www.swami.se/download/18.248ad5af12aa8136533800091/SfinxBis.pdf

    This implementation follows the reference implementation:
    http://www.swami.se/download/18.248ad5af12aa8136533800093/swamiSfinxBis.java.txt

    SfinxBis is intended chiefly for Swedish names.
    """
    adelstitler = (' DE LA ', ' DE LAS ', ' DE LOS ', ' VAN DE ', ' VAN DEN ',
                   ' VAN DER ', ' VON DEM ', ' VON DER ',
                   ' AF ', ' AV ', ' DA ', ' DE ', ' DEL ', ' DEN ', ' DES ',
                   ' DI ', ' DO ', ' DON ', ' DOS ', ' DU ', ' E ', ' IN ',
                   ' LA ', ' LE ', ' MAC ', ' MC ', ' VAN ', ' VON ', ' Y ',
                   ' S:T ')

    _harde_vokaler = tuple('AOUÅ')
    _mjuka_vokaler = tuple('EIYÄÖ')
    _konsonanter = tuple('BCDFGHJKLMNPQRSTVWXZ')
    _alfabet = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ')

    _sfinxbis_translation = dict(zip([ord(_) for _ in
                                      u'BCDFGHJKLMNPQRSTVZAOUÅEIYÄÖ'],
                                      u'123729224551268378999999999'))

    _sfinxbis_substitutions = dict(zip([ord(_) for _ in
                                        u'WZÀÁÂÃÆÇÈÉÊËÌÍÎÏÑÒÓÔÕØÙÚÛÜÝ'],
                                       u'VSAAAAÄCEEEEIIIINOOOOÖUUUYY'))

    def _foersvensker(ordet):
        """Return Swedish-ized form of the word
        """
        ordet = ordet.replace('STIERN', 'STJÄRN')
        ordet = ordet.replace('HIE', 'HJ')
        ordet = ordet.replace('SIÖ', 'SJÖ')
        ordet = ordet.replace('SCH', 'SH')
        ordet = ordet.replace('QU', 'KV')
        ordet = ordet.replace('IO', 'JO')
        ordet = ordet.replace('PH', 'F')

        for i in _harde_vokaler:
            ordet = ordet.replace(i+'Ü', i+'J')
            ordet = ordet.replace(i+'Y', i+'J')
            ordet = ordet.replace(i+'I', i+'J')
        for i in _mjuka_vokaler:
            ordet = ordet.replace(i+'Ü', i+'J')
            ordet = ordet.replace(i+'Y', i+'J')
            ordet = ordet.replace(i+'I', i+'J')

        if 'H' in ordet:
            for i in _konsonanter:
                ordet = ordet.replace('H'+i, i)

        ordet = ordet.translate(_sfinxbis_substitutions)

        ordet = ordet.replace('Ð', 'ETH')
        ordet = ordet.replace('Þ', 'TH')
        ordet = ordet.replace('ß', 'SS')

        return ordet


    def _koda_foersta_ljudet(ordet):
        """Return word with the first sound coded
        """
        if ordet[0:1] in _mjuka_vokaler or ordet[0:1] in _harde_vokaler:
            ordet = '$' + ordet[1:]
        elif ordet[0:2] in ('DJ', 'GJ', 'HJ', 'LJ'):
            ordet = 'J' + ordet[2:]
        elif ordet[0:1] == 'G' and ordet[1:2] in _mjuka_vokaler:
            ordet = 'J' + ordet[1:]
        elif ordet[0:1] == 'Q':
            ordet = 'K' + ordet[1:]
        elif (ordet[0:2] == 'CH' and
              ordet[2:3] in _mjuka_vokaler + _harde_vokaler):
            ordet = '#' + ordet[2:]
        elif ordet[0:1] == 'C' and ordet[1:2] in _harde_vokaler:
            ordet = 'K' + ordet[1:]
        elif ordet[0:1] == 'C' and ordet[1:2] in _konsonanter:
            ordet = 'K' + ordet[1:]
        elif ordet[0:1] == 'X':
            ordet = 'S' + ordet[1:]
        elif ordet[0:1] == 'C' and ordet[1:2] in _mjuka_vokaler:
            ordet = 'S' + ordet[1:]
        elif ordet[0:3] in ('SKJ', 'STJ', 'SCH'):
            ordet = '#' + ordet[3:]
        elif ordet[0:2] in ('SH', 'KJ', 'TJ', 'SJ'):
            ordet = '#' + ordet[2:]
        elif ordet[0:2] == 'SK' and ordet[2:3] in _mjuka_vokaler:
            ordet = '#' + ordet[2:]
        elif ordet[0:1] == 'K' and ordet[1:2] in _mjuka_vokaler:
            ordet = '#' + ordet[1:]
        return ordet


    # Steg 1, Versaler
    word = unicodedata.normalize('NFC', _unicode(word.upper()))
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
        return ('',)

    # Steg 4, Försvenskning
    ordlista = [_foersvensker(ordet) for ordet in ordlista]

    # Steg 5, Ta bort alla tecken som inte är A-Ö (65-90,196,197,214)
    ordlista = [''.join([c for c in ordet if c in _alfabet])
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
                zip([_[0:1] for _ in ordlista], rest)]

    # truncate, if maxlength is set
    if maxlength:
        ordlista = [ordet[:maxlength] for ordet in ordlista]

    return tuple(ordlista)


def phonet(word, mode=1, lang='de', trace=False):
    """Return the phonet encoding of a word

    Arguments:
    word -- the word to translate to a phonet encoding
    mode -- the ponet variant to employ (1 or 2)
    lang -- 'de' (default) for German
            'none' for no language
    trace -- prints debugging info if True

    Description:
    phonet was developed by Jörg Michael and documented in c't magazine
    vol. 25/1999, p. 252. It is a phonetic algorithm designed primarily for
    German.
    Cf. http://www.heise.de/ct/ftp/99/25/252/

    This is a port of Jesper Zedlitz's code, which is licensed LGPL:
    https://code.google.com/p/phonet4java/source/browse/trunk/src/main/java/com/googlecode/phonet4java/Phonet.java
    That is, in turn, based on Michael's C code, which is also licensed LGPL:
    ftp://ftp.heise.de/pub/ct/listings/phonet.zip
    """
    # pylint: disable=too-many-branches

    _phonet_rules_no_lang = (# separator chars
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
                             'VAN DEN ^', 'VANDEN', 'VANDEN')

    _phonet_rules_german = (# separator chars
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
                            'ALOI^', 'ALOI', 'ALUI', # Do NOT merge these rules
                            'ALOY^', 'ALOI', 'ALUI', # (needed by 'check_rules')
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
                            'CHEM-^', 'KE', 'KE', # or: 'CHE', 'KE'
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
                            'CH^', 'K', 'K', # or: 'CH', 'K'
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
                            'K(SßXZ)7', 'X', 'X', # implies 'KST' -> 'XT'
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
                            'O(FV)$', 'AU', 'AU', # due to 'OW$' -> 'AU'
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

    _phonet_upper_translation = dict(zip([ord(_) for _ in
            u'abcdefghijklmnopqrstuvwxyzàáâãåäæçðèéêëìíîïñòóôõöøœšßþùúûüýÿ'],
            u'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÅÄÆÇÐÈÉÊËÌÍÎÏÑÒÓÔÕÖØŒŠßÞÙÚÛÜÝŸ'))

    def _trinfo(text, rule, err_text, lang):
        """Output debug information
        """
        if lang == 'none':
            _phonet_rules = _phonet_rules_no_lang
        else:
            _phonet_rules = _phonet_rules_german

        from_rule = ('(NULL)' if _phonet_rules[rule] == None else
                     _phonet_rules[rule])
        to_rule1 = ('(NULL)' if (_phonet_rules[rule + 1] == None) else
                    _phonet_rules[rule + 1])
        to_rule2 = ('(NULL)' if (_phonet_rules[rule + 2] == None) else
                    _phonet_rules[rule + 2])
        print('"{} {}:  "{}"{}"{}" {}'.format(text, ((rule / 3) + 1), from_rule,
                                              to_rule1, to_rule2, err_text))

    def _initialize_phonet(lang):
        """Initialize phonet variables
        """
        if lang == 'none':
            _phonet_rules = _phonet_rules_no_lang
        else:
            _phonet_rules = _phonet_rules_german

        phonet_hash[''] = -1

        # German and international umlauts
        for j in 'ÀÁÂÃÅÄÆÇÐÈÉÊËÌÍÎÏÑÒÓÔÕÖØŒŠßÞÙÚÛÜÝŸ':
            alpha_pos[j] = 1
            phonet_hash[j] = -1

        # "normal" letters ('A'-'Z')
        for i, j in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            alpha_pos[j] = i + 2
            phonet_hash[j] = -1

        for i in _range(26):
            for j in _range(28):
                phonet_hash_1[i, j] = -1
                phonet_hash_2[i, j] = -1

        # for each phonetc rule
        for i in _range(len(_phonet_rules)):
            rule = _phonet_rules[i]

            if rule and i % 3 == 0:
                # calculate first hash value
                k = _phonet_rules[i][0]

                if phonet_hash[k] < 0 and (_phonet_rules[i+1] or
                                           _phonet_rules[i+2]):
                    phonet_hash[k] = i

                # calculate second hash values
                if k != '' and alpha_pos[k] >= 2:
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


    def _phonet(term, mode, lang, trace):
        """Return the phonet coded form of a term
        """
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

            if trace:
                print('\ncheck position {}:  src = "{}",  dest = "{}"'.format
                      (j, src[i:], dest[:j]))

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

                    if ((_phonet_rules[pos] is None) or
                        (_phonet_rules[pos + mode] is None)):
                        # no conversion rule available
                        pos += 3
                        continue

                    if trace:
                        _trinfo('> rule no.', pos, 'is being checked', lang)

                    # check whole string
                    matches = 1 # number of matching letters
                    priority = 5 # default priority
                    rule = _phonet_rules[pos]
                    rule = rule[1:]

                    while (rule and (len(rule) > 0) and
                           (len(src) > (i + matches)) and
                           (src[i + matches] == rule[0]) and
                           not rule[0].isdigit() and
                           (rule not in '(-<^$')):
                        matches += 1
                        rule = rule[1:]

                    if rule and (rule[0] == '('):
                        # check an array of letters
                        if ((len(src) > (i + matches)) and
                            src[i + matches].isalpha() and
                            (src[i + matches] in rule[1:])):
                            matches += 1

                            while rule and rule[0] != ')':
                                rule = rule[1:]

                            if rule[0] == ')':
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

                    if ((not rule or rule[0] == '') or
                        ((rule[0] == '^') and
                         ((i == 0) or not src[i-1].isalpha()) and
                         ((rule[1:2] != '$') or
                          (not (src[i+matches0:i+matches0+1].isalpha()) and
                           (src[i+matches0:i+matches0+1] != '.')))) or
                        ((rule[0] == '$') and (i > 0) and src[i-1].isalpha() and
                         ((not src[i+matches0:i+matches0+1].isalpha()) and
                          (src[i+matches0:i+matches0+1] != '.')))):
                        # look for continuation, if:
                        # matches > 1 und NO '-' in first string */
                        pos0 = -1

                        start3 = 0
                        start4 = 0
                        end3 = 0
                        end4 = 0

                        if ((matches > 1) and (src[i+matches:i+matches+1] != '')
                            and (priority0 != ord('-'))):
                            char0 = src[i+matches-1]
                            pos0 = alpha_pos[char0]

                            if (pos0 >= 2) and (src[i+matches] != ''):
                                xpos = pos0 - 2
                                pos0 = alpha_pos[src[i+matches]]
                                start3 = phonet_hash_1[xpos, pos0]
                                start4 = phonet_hash_1[xpos, 0]
                                end3 = phonet_hash_2[xpos, pos0]
                                end4 = phonet_hash_2[xpos, 0]

                                # preserve rule priorities
                                if ((start4 >= 0) and
                                    ((start3 < 0) or (start4 < start3))):
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
                            while ((_phonet_rules[pos0] == None) or
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

                                if ((_phonet_rules[pos0] == None) or
                                    (_phonet_rules[pos0 + mode] == None)):
                                    # no conversion rule available
                                    pos0 += 3
                                    continue

                                if trace:
                                    _trinfo('> > continuation rule no.', pos0,
                                               'is being checked', lang)

                                # check whole string
                                matches0 = matches
                                priority0 = 5
                                rule = _phonet_rules[pos0]
                                rule = rule[1:]

                                while (rule and len(rule) > 0 and
                                       (src[i+matches0:i+matches0+1] == rule[0])
                                       and (not rule[0].isdigit() or
                                            (rule in '(-<^$'))):
                                    matches0 += 1
                                    rule = rule[1:]

                                if rule and rule[0] == '(':
                                    # check an array of letters
                                    if (src[i+matches0:i+matches0+1].isalpha()
                                        and (src[i+matches0] in rule[1:])):
                                        matches0 += 1

                                        while rule and (rule[0] != ')'):
                                            rule = rule[1:]

                                        if rule[0] == ')':
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
                                     src[i+matches0:i+matches0+1].isalpha() and
                                     (src[i+matches0:i+matches0+1] != '.'))):
                                    if matches0 == matches:
                                        # this is only a partial string
                                        if trace:
                                            _trinfo('> > continuation rule no.',
                                                    pos0,
                                                    'not used (too short)',
                                                    lang)

                                        pos0 += 3
                                        continue

                                    if priority0 < priority:
                                        # priority is too low
                                        if trace:
                                            _trinfo('> > continuation rule no.',
                                                    pos0, 'not used (priority)',
                                                    lang)

                                        pos0 += 3
                                        continue

                                    # continuation rule found
                                    break

                                if trace:
                                    _trinfo('> > continuation rule no.', pos0,
                                        'not used', lang)

                                pos0 += 3

                            # end of "while"
                            if ((priority0 >= priority) and
                                ((_phonet_rules[pos0] != None) and
                                 (_phonet_rules[pos0][0] == char0))):
                                pos += 3

                                if trace:
                                    _trinfo('> rule no.', pos, '', lang)
                                    _trinfo('> not used because of continuation'
                                            , pos0, '', lang)
                                continue

                        # replace string
                        if trace:
                            _trinfo('Rule no.', pos, 'is applied', lang)

                        if (_phonet_rules[pos] and
                            ('<' in _phonet_rules[pos][1:])):
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

                            while rule and (src[i+matches0] != ''):
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

                            if (_phonet_rules[pos] and
                                '^^' in _phonet_rules[pos][1:]):
                                if char != '':
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
                if (char != '') and ((j == 0) or (dest[j-1] != char)):
                    # delete multiple letters only
                    dest = dest[0:j] + char + dest[min(j+1, term_length):]
                    j += 1

                i += 1
                zeta = 0

        dest = dest[0:j]

        return dest


    _initialize_phonet(lang)

    word = unicodedata.normalize('NFKC', _unicode(word))
    return _phonet(word, mode, lang, trace)


def spfc(word):
    """Return the Standardized Phonetic Frequency Code of a word

    Arguments:
    word -- the word to translate to a Standardized Phonetic Frequency Code

    Description:
    Standardized Phonetic Frequency Code is roughly Soundex-like.
    This implementation is based on page 19-21 of
    https://archive.org/stream/accessingindivid00moor#page/19/mode/1up
    """

    _pf1 = dict(zip([ord(_) for _ in u'SZCKQVFPUWABLORDHIEMNXGJT'],
                   u'0011112222334445556666777'))
    _pf2 = dict(zip([ord(_) for _ in
                    u'SZCKQFPXABORDHIMNGJTUVWEL'],
                    u'0011122233445556677788899'))
    _pf3 = dict(zip([ord(_) for _ in
                    u'BCKQVDTFLPGJXMNRSZAEHIOUWY'],
                    u'00000112223334456677777777'))

    _substitutions = (('DK', 'K'), ('DT', 'T'), ('SC', 'S'), ('KN', 'N'),
                      ('MN', 'N'))

    def _raise_word_ex():
        """Raise an AttributeError
        """
        raise AttributeError('word attribute must be a string with a space or' +
                             ' period dividing the first and last names or a ' +
                             'tuple/list consisting of the first and last ' +
                             'names')

    if not word:
        return ''

    if isinstance(word, _unicode):
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

    names = [unicodedata.normalize('NFKD', _unicode(_.strip().upper()))
             for _ in names]
    code = ''

    def steps_one_to_three(name):
        """Performs the first three steps of SPFC
        """
        # filter out non A-Z
        name = ''.join([_ for _ in name if _ in
                        tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

        # 1. In the field, convert DK to K, DT to T, SC to S, KN to N,
        # and MN to N
        for subst in _substitutions:
            name = name.replace(subst[0], subst[1])

        # 2. In the name field, replace multiple letters with a single letter
        name = _delete_consecutive_repeats(name)

        # 3. Remove vowels, W, H, and Y, but keep the first letter in the name
        # field.
        name = name[0] + ''.join([_ for _ in name[1:] if _ not in
                                  tuple('AEIOUWHY')])
        return name

    names = [steps_one_to_three(_) for _ in names]

    # 4. The first digit of the code is obtained using PF1 and the first letter
    # of the name field. Remove this letter after coding.
    code += names[1][0].translate(_pf1)
    names[1] = names[1][1:]

    # 5. Using the last letters of the name, use Table PF3 to obtain the
    # second digit of the code. Use as many letters as possible and remove
    # after coding.
    if names[1].endswith('STN') or names[1].endswith('PRS'):
        code += '8'
        names[1] = names[1][:-3]
    elif names[1].endswith('SN'):
        code += '8'
        names[1] = names[1][:-2]
    elif names[1].endswith('STR'):
        code += '9'
        names[1] = names[1][:-3]
    elif (names[1].endswith('SR') or names[1].endswith('TN') or
          names[1].endswith('TD')):
        code += '9'
        names[1] = names[1][:-2]
    elif names[1].endswith('DRS'):
        code += '7'
        names[1] = names[1][:-3]
    elif names[1].endswith('TR') or names[1].endswith('MN'):
        code += '7'
        names[1] = names[1][:-2]
    else:
        code += names[1][-1].translate(_pf3)
        names[1] = names[1][:-1]

    # 6. The third digit is found using Table PF2 and the first character of
    # the first name. Remove after coding.
    code += names[0][0].translate(_pf2)
    names[0] = names[0][1:]

    # 7. The fourth digit is found using Table PF2 and the first character of
    # the name field. If no letters remain use zero. After coding remove the
    # letter.
    # 8. The fifth digit is found in the same manner as the fourth using the
    # remaining characters of the name field if any.
    for _ in _range(2):
        if names[1]:
            code += names[1][0].translate(_pf2)
            names[1] = names[1][1:]
        else:
            code += '0'

    return code

def german_ipa(word):
    """Return the IPA transcription of a German word

    Arguments:
    word -- the German word to transcribe to IPA

    Description:
    This is based largely on the orthographic mapping described at:
    https://en.wikipedia.org/wiki/German_orthography

    No significant attempt is made to accomodate loanwords.
    """
    # pylint: disable=too-many-branches
    _vowels = tuple('AEIOUYÄÖÜ')

    word = unicodedata.normalize('NFKC', _unicode(word.upper()))
    word = word.replace('ß', 'SS')

    #word = ''.join([c for c in word if c in tuple('ABCDEFGIKLMNOPQRSTUVXYZ')])

    ipa = ''
    last = len(word)-1
    skip = 0
    for i in _range(len(word)):
        if skip:
            skip -= 1
            continue

        # Consonants
        if word[i] in 'BFJKLMR':
            ipa += word[i].lower()
        elif word[i] == 'C':
            if word[i:i+2] == 'CH':
                if word[i:i+3] == 'CHS':
                    ipa += 'ks'
                    skip = 2
                elif word[i:i+4] == 'CHEN':
                    ipa += 'ç'
                    skip = 1
                elif i-1 >= 0 and word[i-1] in tuple('AOU'):
                    ipa += 'x'
                    skip = 1
                else:
                    ipa += 'ç'
                    skip = 1
            elif word[i:i+2] == 'CK':
                ipa += 'k'
                skip = 1
            elif i != last and word[i+1] in tuple('ÄEI'):
                ipa += 'ts'
            else:
                ipa += 'k'
        elif word[i] == 'D':
            if word[i:i+4] == 'DSCH':
                ipa += 'dʒ'
                skip = 3
            elif word[i:i+2] == 'DT':
                ipa += 't'
                skip = 1
            else:
                ipa += 'd'
        elif word[i] == 'G':
            if i-1 >= 0 and word[i-1] == 'I':
                ipa += 'ç'
            else:
                ipa += 'g'
        elif word[i] == 'H':
            if i != last and word[i+1] in _vowels:
                ipa += 'h'
            # else ignore
        elif word[i] == 'N':
            if word[i:i+2] == 'NG':
                ipa += 'ŋ'
                skip = 1
            elif word[i:i+2] == 'NK':
                ipa += 'ŋk'
                skip = 1
            else:
                ipa += 'n'
        elif word[i] == 'P':
            if word[i:i+2] == 'PH':
                ipa += 'f'
                skip = 1
            else:
                ipa += 'p'
        elif word[i] == 'Q':
            if word[i:i+2] == 'QU' and i+1 != last and word[i+2] in _vowels:
                ipa += 'kv'
                skip = 1
            else:
                ipa += 'k'
        elif word[i] == 'S':
            if word[i:i+2] == 'SS':
                ipa += 's'
                skip = 1
            elif word[i:i+3] == 'SCH':
                ipa += 'ʃ'
                skip = 2
            elif i == 0 and i != last and word[i+1] in tuple('PT'):
                ipa += 'ʃ'
            elif i != last and word[i+1] in _vowels:
                ipa += 'z'
            else:
                ipa += 's'
        elif word[i] == 'T':
            if word[i:i+4] == 'TSCH':
                ipa += 'tʃ'
                skip = 3
            elif word[i:i+5] == 'TZSCH':
                ipa += 'tʃ'
                skip = 4
            elif (word[i:i+4] == 'TION' or word[i:i+4] == 'TIÄR' or
                  word[i:i+4] == 'TIAL' or word[i:i+5] == 'TIELL'):
                ipa += 'tsi'
                skip = 1
            elif word[i:i+2] == 'TZ':
                ipa += 'ts'
                skip = 1
            elif word[i:i+2] == 'TH':
                ipa += 't'
                skip = 1
            else:
                ipa += 't'
        elif word[i] == 'V':
            ipa += 'f'
        elif word[i] == 'W':
            ipa += 'v'
        elif word[i] == 'X':
            ipa += 'ks'
        elif word[i] == 'Z':
            if word[i:i+4] == 'ZSCH':
                ipa += 'tʃ'
                skip = 3
            else:
                ipa += 'ts'

        # Vowels -- little attention is paid to length or tenseness
        # -Diphthongs first
        elif word[i:i+2] in tuple(('EI', 'AI', 'EY', 'AY')):
            ipa += 'ai'
            skip = 1
        elif word[i:i+2] in tuple(('EU', 'ÄU')):
            ipa += 'oy'
            skip = 1
        elif word[i:i+2] == 'AU':
            ipa += 'au'
            skip = 1

        # -Monophthongs following
        elif word[i] == 'A':
            if word[i:i+2] in tuple(('AA', 'AH')):
                skip = 1
            ipa += 'a'
        elif word[i] == 'E':
            if word[i:i+2] in tuple(('EE', 'EH')):
                skip = 1
            ipa += 'e'
        elif word[i] == 'I':
            if word[i:i+2] in tuple(('IE', 'IH')):
                skip = 1
            if word[i:i+3] == 'IEH':
                skip = 2
            ipa += 'i'
        elif word[i] == 'O':
            if word[i:i+2] in tuple(('OO', 'OH')):
                skip = 1
            ipa += 'o'
        elif word[i] == 'U':
            if word[i:i+2] == 'UH':
                skip = 1
            ipa += 'u'
        elif word[i] == 'Y':
            ipa += 'y'
        elif word[i] == 'Ä':
            if word[i:i+2] == 'ÄH':
                skip = 1
            ipa += 'e'
        elif word[i] == 'Ö':
            if word[i:i+2] == 'ÖH':
                skip = 1
            ipa += 'ø'
        elif word[i] == 'Ü':
            if word[i:i+2] == 'ÜH':
                skip = 1
            ipa += 'y'

    return ipa


def bmpm(word, language_arg=0, name_mode='gen', match_mode='approx',
         concat=False, filter_langs=False):
    """Return the Beider-Morse Phonetic Matching algorithm encoding(s) of a
    term

    Arguments:
    word -- the term to which to apply the Beider-Morse Phonetic Matching
                algorithm
    language_arg -- the language of the term; supported values include:
                "any", "arabic", "cyrillic", "czech", "dutch", "english",
                "french", "german", "greek", "greeklatin", "hebrew",
                "hungarian", "italian", "polish", "portuguese","romanian",
                "russian", "spanish", "turkish"
    name_mode -- the name mode of the algorithm: 'gen' (default),
                'ash' (Ashkenazi), or 'sep' (Sephardic)
    match_mode -- matching mode: 'approx' or 'exact'
    concat -- concatenation mode
    filter_langs -- filter out incompatible languages

    Description:
    The Beider-Morse Phonetic Matching algorithm is described at:
    http://stevemorse.org/phonetics/bmpm.htm
    The reference implementation is licensed under GPLv3 and available at:
    http://stevemorse.org/phoneticinfo.htm
    """
    return _bmpm(word, language_arg, name_mode, match_mode,
                 concat, filter_langs)
