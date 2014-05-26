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
    Phonex
    Phonem
    Phonix


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

# pylint: disable=C0302

from __future__ import unicode_literals
from __future__ import division
from ._compat import _unicode, _range
from itertools import groupby
import re
import unicodedata


def russell_index(word):
    """Return the Russell Index of a word as an int

    Arguments:
    word -- the word to translate to a Russell Index value

    Description:
    This follows Robert C. Russell's Index algorithm, as described in
    US Patent 1,261,167 (1917)
    """
    _russell_translation_table = dict(zip([ord(_) for _ in
                                           u'ABCDEFGIKLMNOPQRSTUVXYZ'],
                                          u'12341231356712383412313'))

    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = word.replace('GH', '')  # discard gh (rule 3)
    word = word.rstrip('SZ') # discard /[sz]$/ (rule 3)

    # translate according to Russell's mapping
    word = ''.join([c for c in word if c in list('ABCDEFGIKLMNOPQRSTUVXYZ')])
    sdx = word.translate(_russell_translation_table)

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
    _russell_num_translation_table = dict(zip([ord(_) for _ in u'12345678'],
                                              u'ABCDLMNR'))
    num = ''.join([c for c in _unicode(num) if c in list('12345678')])
    if num:
        return num.translate(_russell_num_translation_table)


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
    _soundex_translation_table = dict(zip([ord(_) for _ in
                                           u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
                                          u'01230129022455012623019202'))

    # Call the D-M Soundex function itself if requested
    if var == 'dm':
        return dm_soundex(word, maxlength, reverse)

    # Require a maxlength of at least 4
    maxlength = max(4, maxlength)

    # uppercase, normalize, decompose, and filter non-A-Z
    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    # Nothing to convert, return base case
    if not word:
        return '0'*maxlength

    # Reverse word if computing Reverse Soundex
    if reverse:
        word = word[::-1]

    # apply the Soundex algorithm
    sdx = word.translate(_soundex_translation_table)

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

    _vowels = list('AEIJOUY')
    dms = [''] # initialize empty code list

    # Require a maxlength of at least 6
    maxlength = max(6, maxlength)

    # uppercase, normalize, decompose, and filter non-A-Z
    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = ''.join([c for c in word if c in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

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
        if i > 0 and word[i-1] in list(letters):
            return True
        return False

    def _before(word, i, letters):
        """Return True if word[i] precedes one of the supplied letters
        """
        if i+1 < len(word) and word[i+1] in list(letters):
            return True
        return False

    _vowels = list('AEIJYOU')

    sdx = ''

    word = word.replace('ß', 'SS')
    word = unicodedata.normalize('NFKD', _unicode(word.upper()))

    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')
    word = ''.join([c for c in word if c in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

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
    _koelner_num_translation_table = dict(zip([ord(_) for _ in u'012345678'],
                                              u'APTFKLNRS'))
    num = ''.join([c for c in _unicode(num) if c in list('012345678')])
    return num.translate(_koelner_num_translation_table)


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

    _vowels = list('AEIOU')

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

        if word[i] != key[-1]:
            key += word[i]

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
    word = word[0]+''.join([c for c in word[1:] if c not in list('AEIOU')])
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
    _vowels = list('AEIOU')
    _frontv = list('EIY')
    _varson = list('CSPTG')

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
            if (i > 0 and i+2 < elen and ename[i+1] == 'I' and
                ename[i+2] in 'OA'):
                metaph += 'X'
            elif ename[i+1:i+2] == 'H':
                metaph += 'X'
            else:
                metaph += 'S'

        elif ename[i] == 'T':
            if (i > 0 and i+2 < elen and ename[i+1] == 'I' and
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
        return word[pos] in list('AEIOUY')

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

        if _get_at(current) in list('AEIOUY'):
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
    _vowels = list('aeiou')

    word = word.lower()
    word = ''.join([c for c in word if c in list('abcdefghijklmnopqrstuvwxyz')])

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
    word = ''.join([c for c in word if c in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

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


def fuzzy_soundex(word, maxlength=4):
    """Return the Phonex encoding of a word

    Arguments:
    word -- the word to translate to a Phonex encoding
    maxlength -- the length of the code returned (defaults to 4)

    Description:
    Phonex is an algorithm derived from Soundex, defined in:
    Holmes, David and M. Catherine McCabe. "Improving Precision and Recall for
    Soundex Retrieval."
    http://wayback.archive.org/web/20100629121128/http://www.ir.iit.edu/publications/downloads/IEEESoundexV5.pdf
    """
    pass


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
            if name[i+1:i+2] in list('AEIOUY') or i+1 == len(name):
                code = '4'
        elif name[i] in 'MN':
            if name[i+1:i+2] in list('DG'):
                name = name[:i+1] + name[i] + name[i+2:]
            code = '5'
        elif name[i] == 'R':
            if name[i+1:i+2] in list('AEIOUY') or i+1 == len(name):
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

    """
    pass


def phonix(word):
    """Return the Phonix encoding of a word

    Arguments:
    word -- the word to translate to a Phonix encoding

    Description:
    Phonix is a Soundex-like algorithm defined in:
    T.N. Gadd: PHONIX --- The Algorithm, Program 24/4, 1990, p.363-366.

    This implementation is based on http://cpansearch.perl.org/src/ULPFR/WAIT-1.800/soundex.c
    """
    pass


def _delete_consecutive_repeats(word):
    """Return word with all contiguous repeating characters collapsed to
    a single instance
    """
    return ''.join(char for char, _ in groupby(word))
