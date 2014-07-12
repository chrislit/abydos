# -*- coding: utf-8 -*-
"""abydos.stemmer

The stemmer module defines word stemmers including:
    the Porter stemmer


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
import unicodedata
from ._compat import _range, _unicode


_vowels = set('AEIOUy')

def _m_degree(term):
    """Return the m-degree as defined in the Porter stemmer definition

    Arguments:
    term -- the word for which to calculate the m-degree

    Description:
    m-degree is equal to the number of V to C transitions
    """
    mdeg = 0
    last_was_vowel = False
    for letter in term:
        if letter in _vowels:
            last_was_vowel = True
        else:
            if last_was_vowel:
                mdeg += 1
            last_was_vowel = False
    return mdeg

def _has_vowel(term):
    """Return true iff a vowel exists in the term (as defined in the Porter
    stemmer definition)

    Arguments:
    term -- the word to scan for vowels
    """
    for letter in term:
        if letter in _vowels:
            return True
    return False

def _ends_in_doubled_cons(term):
    """Return true iff the stem ends in a doubled consonant (as defined in the
    Porter stemmer definition)

    Arguments:
    term -- the word to scan for vowels
    """
    if len(term) > 1 and term[-1] not in _vowels and term[-2] == term[-1]:
        return True
    return False

def _ends_in_cvc(term):
    """Return true iff the stem ends in cvc (as defined in the Porter stemmer
    definition)

    Arguments:
    term -- the word to scan for cvc
    """
    if len(term) > 2 and (term[-1] not in _vowels and
                          term[-2] in _vowels and
                          term[-3] not in _vowels and
                          term[-1] not in tuple('WXY')):
        return True
    return False

def porter(word):
    """Implementation of Porter stemmer -- ideally returns the word stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The Porter stemmer is defined at
    http://snowball.tartarus.org/algorithms/porter/stemmer.html
    """
    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicodedata.normalize('NFKD', _unicode(word.upper()))
    word = word.replace('ß', 'SS')
    word = ''.join([c for c in word if c in
                    set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    # Return empty string if there's nothing left to stem
    if len(word) < 3:
        return word

    # Re-map vocalic Y to y (Y will be C, y will be V)
    _vowels = set('AEIOUy')
    for i in _range(1, len(word)):
        if word[i] == 'Y' and word[i-1] not in _vowels:
            word = word[:i] + 'y' + word[i+1:]

    # Step 1a
    if word[-1] == 'S':
        if word[-4:] == 'SSES':
            word = word[:-2]
        elif word[-3:] == 'IES':
            word = word[:-2]
        elif word[-2:] == 'SS':
            pass
        elif word[-1] == 'S':
            word = word[:-1]

    # Step 1b
    step1b_flag = False
    if word[-3:] == 'EED':
        if _m_degree(word[:-3]) > 0:
            word = word[:-1]
    elif word[-2:] == 'ED':
        if _has_vowel(word[:-2]):
            word = word[:-2]
            step1b_flag = True
    elif word[-3:] == 'ING':
        if _has_vowel(word[:-3]):
            word = word[:-3]
            step1b_flag = True

    if step1b_flag:
        if word[-2:] in set(['AT', 'BL', 'IZ']):
            word += 'E'
        elif _ends_in_doubled_cons(word) and word[-1] not in set('LSZ'):
            word = word[:-1]
        elif _m_degree(word) == 1 and _ends_in_cvc(word):
            word += 'E'

    # Step 1c
    if (word[-1] == 'Y' or word[-1] == 'y') and _has_vowel(word[:-1]):
        word = word[:-1] + 'I'

    # Step 2
    if len(word) > 1:
        if word[-2] == 'A':
            if word[-7:] == 'ATIONAL':
                if _m_degree(word[:-7]) > 0:
                    word = word[:-5] + 'E'
            elif word[-6:] == 'TIONAL':
                if _m_degree(word[:-6]) > 0:
                    word = word[:-2]
        elif word[-2] == 'C':
            if word[-4:] in set(['ENCI', 'ANCI']):
                if _m_degree(word[:-4]) > 0:
                    word = word[:-1] + 'E'
        elif word[-2] == 'E':
            if word[-4:] == 'IZER':
                if _m_degree(word[:-4]) > 0:
                    word = word[:-1]
        elif word[-2] == 'G':
            if word[-4:] == 'LOGI':
                if _m_degree(word[:-4]) > 0:
                    word = word[:-1]
        elif word[-2] == 'L':
            if word[-3:] == 'BLI':
                if _m_degree(word[:-3]) > 0:
                    word = word[:-1] + 'E'
            elif word[-4:] == 'ALLI':
                if _m_degree(word[:-4]) > 0:
                    word = word[:-2]
            elif word[-5:] == 'ENTLI':
                if _m_degree(word[:-5]) > 0:
                    word = word[:-2]
            elif word[-3:] == 'ELI':
                if _m_degree(word[:-3]) > 0:
                    word = word[:-2]
            elif word[-5:] == 'OUSLI':
                if _m_degree(word[:-5]) > 0:
                    word = word[:-2]
        elif word[-2] == 'O':
            if word[-7:] == 'IZATION':
                if _m_degree(word[:-7]) > 0:
                    word = word[:-5] + 'E'
            elif word[-5:] == 'ATION':
                if _m_degree(word[:-5]) > 0:
                    word = word[:-3] + 'E'
            elif word[-4:] == 'ATOR':
                if _m_degree(word[:-4]) > 0:
                    word = word[:-2] + 'E'
        elif word[-2] == 'S':
            if word[-5:] == 'ALISM':
                if _m_degree(word[:-5]) > 0:
                    word = word[:-3]
            elif word[-7:] in set(['IVENESS', 'FULNESS', 'OUSNESS']):
                if _m_degree(word[:-7]) > 0:
                    word = word[:-4]
        elif word[-2] == 'T':
            if word[-5:] == 'ALITI':
                if _m_degree(word[:-5]) > 0:
                    word = word[:-3]
            elif word[-5:] == 'IVITI':
                if _m_degree(word[:-5]) > 0:
                    word = word[:-3] + 'E'
            elif word[-6:] == 'BILITI':
                if _m_degree(word[:-6]) > 0:
                    word = word[:-5] + 'LE'

    # Step 3
    if word[-5:] == 'ICATE':
        if _m_degree(word[:-5]) > 0:
            word = word[:-3]
    elif word[-5:] == 'ATIVE':
        if _m_degree(word[:-5]) > 0:
            word = word[:-5]
    elif word[-5:] in set(['ALIZE', 'ICITI']):
        if _m_degree(word[:-5]) > 0:
            word = word[:-3]
    elif word[-4:] == 'ICAL':
        if _m_degree(word[:-4]) > 0:
            word = word[:-2]
    elif word[-3:] == 'FUL':
        if _m_degree(word[:-3]) > 0:
            word = word[:-3]
    elif word[-4:] == 'NESS':
        if _m_degree(word[:-4]) > 0:
            word = word[:-4]

    # Step 4
    if word[-2:] == 'AL':
        if _m_degree(word[:-2]) > 1:
            word = word[:-2]
    elif word[-4:] == 'ANCE':
        if _m_degree(word[:-4]) > 1:
            word = word[:-4]
    elif word[-4:] == 'ENCE':
        if _m_degree(word[:-4]) > 1:
            word = word[:-4]
    elif word[-2:] == 'ER':
        if _m_degree(word[:-2]) > 1:
            word = word[:-2]
    elif word[-2:] == 'IC':
        if _m_degree(word[:-2]) > 1:
            word = word[:-2]
    elif word[-4:] == 'ABLE':
        if _m_degree(word[:-4]) > 1:
            word = word[:-4]
    elif word[-4:] == 'IBLE':
        if _m_degree(word[:-4]) > 1:
            word = word[:-4]
    elif word[-3:] == 'ANT':
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]
    elif word[-5:] == 'EMENT':
        if _m_degree(word[:-5]) > 1:
            word = word[:-5]
    elif word[-4:] == 'MENT':
        if _m_degree(word[:-4]) > 1:
            word = word[:-4]
    elif word[-3:] == 'ENT':
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]
    elif word[-4:] in set(['SION', 'TION']):
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]
    elif word[-2:] == 'OU':
        if _m_degree(word[:-2]) > 1:
            word = word[:-2]
    elif word[-3:] == 'ISM':
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]
    elif word[-3:] == 'ATE':
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]
    elif word[-3:] == 'ITI':
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]
    elif word[-3:] == 'OUS':
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]
    elif word[-3:] == 'IVE':
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]
    elif word[-3:] == 'IZE':
        if _m_degree(word[:-3]) > 1:
            word = word[:-3]

    # Step 5a
    if word[-1] == 'E':
        if _m_degree(word[:-1]) > 1:
            word = word[:-1]
        elif _m_degree(word[:-1]) == 1 and not _ends_in_cvc(word[:-1]):
            word = word[:-1]

    # Step 5b
    if word[-2:] == 'LL' and _m_degree(word) > 1:
        word = word[:-1]

    # Change 'y' back to 'Y' if it survived stemming
    for i in _range(1, len(word)):
        if word[i] == 'y':
            word = word[:i] + 'Y' + word[i+1:]

    return word


def _snowball_r1(term, vowels=set('aeiouy')):
    """Return the R1 region, as defined in the Porter2 specification
    """
    vowel_found = False
    for i in _range(len(term)):
        if not vowel_found and term[i] in vowels:
            vowel_found = True
        elif vowel_found and term[i] not in vowels:
            return term[i+1:]
    return ''

def _snowball_r2(term, vowels=set('aeiouy')):
    """Return the R2 region, as defined in the Porter2 specification
    """
    return _snowball_r1(_snowball_r1(term, vowels), vowels)

def _snowball_short_syllable(term, start=0, vowels=set('aeiouy'),
                             codanonvowels=set('bcdfghjklmnpqrstvz\'')):
    """Return True iff term has a short syllable starting at start,
    according to the Porter2 specification
    """
    if not term or term[start] not in vowels:
        return False
    elif start == 0:
        if term[start+1:start+2] not in vowels:
            return True
    elif term[start+1:start+2] in codanonvowels and term[start-1] not in vowels:
        return True
    return False

def _snowball_ends_in_short_syllable(term, vowels=set('aeiouy'),
                                     codanonvowels=set('bcdfghjklmnpqrstvz\'')):
    """Return True iff term ends in a short syllable,
    according to the Porter2 specification
    """
    for i in reversed(_range(len(term))):
        if term[i] in vowels:
            return _snowball_short_syllable(term, i, vowels, codanonvowels)
    return False

def _snowball_short_word(term, vowels=set('aeiouy'),
                         codanonvowels=set('bcdfghjklmnpqrstvz\'')):
    """Return True iff term is a short word,
    according to the Porter2 specification
    """
    if (_snowball_r1(term, vowels) == '' and
        _snowball_ends_in_short_syllable(term, vowels, codanonvowels)):
        return True
    return False
 

_p2_vowels = set('aeiouy')
_p2_doubles = set(['bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt'])
_p2_li = set('cdeghkmnrt')

def porter2(word):
    """Implementation of Porter2 (Snowball English) stemmer -- ideally returns
    the word stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The Porter2/Snowball English stemmer is defined at
    http://snowball.tartarus.org/algorithms/english/stemmer.html
    """
    # uppercase, normalize, decompose, and filter non-A-Z out
    word = unicodedata.normalize('NFKD', _unicode(word.lower()))
    word = word.replace('ß', 'ss')
    # replace apostrophe-like characters with U+0027, per
    # http://snowball.tartarus.org/texts/apostrophe.html
    word = word.replace('’', '\'')
    word = word.replace('’', '\'')
    word = ''.join([c for c in word if c in
                    set('abcdefghijklmnopqrstuvwxyz\'')])

    # Return empty string if there's nothing left to stem
    if len(word) < 3:
        return word

    # Re-map vocalic Y to y (Y will be C, y will be V)
    if word[0] == 'y':
        word = 'Y' + word[1:]
    for i in _range(1, len(word)):
        if word[i] == 'y' and word[i-1] in _p2_vowels:
            word = word[:i] + 'Y' + word[i+1:]

    # Change 'y' back to 'Y' if it survived stemming
    for i in _range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]

    return word
