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


_vowels = tuple('AEIOUy')

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
    """Return true iff a vowel exists in the term (as defined in the Porter stemmer definition)

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
                    tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])

    # Return empty string if there's nothing left to stem
    if not word:
        return ''

    # Re-map vocalic Y to y (Y will be C, y will be V)
    _vowels = tuple('AEIOUy')
    for i in _range(1, len(word)):
        if word[i] == 'Y' and word[i-1] not in _vowels:
            word = word[:i] + 'y' + word[i+1:]

    # Step 1a
    if len(word) and word[-1] == 'S':
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
    if word[-3:] == 'EED' and _m_degree(word[:-3]) > 0:
        word = word[:-1]
    elif word[-2:] == 'ED' and _has_vowel(word[:-2]):
        word = word[:-2]
        step1b_flag = True
    elif word[-3:] == 'ING' and _has_vowel(word[:-3]):
        word = word[:-3]
        step1b_flag = True

    if step1b_flag:
        if word[-2:] in ('AT', 'BL', 'IZ'):
            word += 'E'
        elif _ends_in_doubled_cons(word) and word[-1] not in tuple('LSZ'):
            word = word[:-1]
        elif _m_degree(word) == 1 and _ends_in_cvc(word):
            word += 'E'

    # Return early if no letters remain
    if not word:
        return ''

    # Step 1c
    if word[-1] == 'Y' and _has_vowel(word[:-1]):
        word = word[:-1] + 'I'

    # Step 2
    if len(word) > 1:
        if word[-2] == 'A':
            if word[-7:] == 'ATIONAL' and _m_degree(word[:-7]) > 0:
                word = word[:-5] + 'E'
            elif word[-6:] == 'TIONAL' and _m_degree(word[:-6]) > 0:
                word = word[:-2]
        elif word[-2] == 'C':
            if (word[-4:] in ('ENCI', 'ANCI') and
                _m_degree(word[:-4]) > 0):
                word = word[:-1] + 'E'
        elif word[-2] == 'E':
            if word[-4:] == 'IZER' and _m_degree(word[:-4]) > 0:
                word = word[:-1]
        elif word[-2] == 'L':
            if word[-4:] == 'ABLI' and _m_degree(word[:-4]) > 0:
                word = word[:-1] + 'E'
            elif word[-4:] == 'ALLI' and _m_degree(word[:-4]) > 0:
                word = word[:-2]
            elif word[-5:] == 'ENTLI' and _m_degree(word[:-5]) > 0:
                word = word[:-2]
            elif word[-3:] == 'ELI' and _m_degree(word[:-3]) > 0:
                word = word[:-2]
            elif word[-5:] == 'OUSLI' and _m_degree(word[:-5]) > 0:
                word = word[:-2]
        elif word[-2] == 'O':
            if word[-7:] == 'IZATION' and _m_degree(word[:-7]) > 0:
                word = word[:-5] + 'E'
            elif word[-5:] == 'ATION' and _m_degree(word[:-5]) > 0:
                word = word[:-3] + 'E'
            elif word[-4:] == 'ATOR' and _m_degree(word[:-4]) > 0:
                word = word[:-2] + 'E'
        elif word[-2] == 'S':
            if word[-5:] == 'ALISM' and _m_degree(word[:-5]) > 0:
                word = word[:-3]
            elif (word[-7:] in ('IVENESS', 'FULNESS', 'OUSNESS') and
                  _m_degree(word[:-7]) > 0):
                word = word[:-4]
        elif word[-2] == 'T':
            if word[-5:] == 'ALITI' and _m_degree(word[:-5]) > 0:
                word = word[:-3]
            elif word[-5:] == 'IVITI' and _m_degree(word[:-5]) > 0:
                word = word[:-3] + 'E'
            elif word[-6:] == 'BILITI' and _m_degree(word[:-6]) > 0:
                word = word[:-5] + 'LE'

    # Step 3
    if word[-5:] == 'ICATE' and _m_degree(word[:-5]) > 0:
        word = word[:-3]
    elif word[-5:] == 'ATIVE' and _m_degree(word[:-5]) > 0:
        word = word[:-5]
    elif ((word[-5:] == 'ALIZE' or word[-5:] == 'ICITI') and
          _m_degree(word[:-5]) > 0):
        word = word[:-3]
    elif word[-4:] == 'ICAL' and _m_degree(word[:-4]) > 0:
        word = word[:-2]
    elif word[-3:] == 'FUL' and _m_degree(word[:-3]) > 0:
        word = word[:-3]
    elif word[-4:] == 'NESS' and _m_degree(word[:-4]) > 0:
        word = word[:-4]

    # Step 4
    if word[-2:] == 'AL' and _m_degree(word[:-2]) > 0:
        word = word[:-2]
    elif word[-4:] == 'ANCE' and _m_degree(word[:-4]) > 0:
        word = word[:-4]
    elif word[-4:] == 'ENCE' and _m_degree(word[:-4]) > 0:
        word = word[:-4]
    elif word[-2:] == 'ER' and _m_degree(word[:-2]) > 0:
        word = word[:-2]
    elif word[-2:] == 'IC' and _m_degree(word[:-2]) > 0:
        word = word[:-2]
    elif word[-4:] == 'ABLE' and _m_degree(word[:-4]) > 0:
        word = word[:-4]
    elif word[-4:] == 'IBLE' and _m_degree(word[:-4]) > 0:
        word = word[:-4]
    elif word[-3:] == 'ANT' and _m_degree(word[:-3]) > 0:
        word = word[:-3]
    elif word[-5:] == 'EMENT' and _m_degree(word[:-5]) > 0:
        word = word[:-5]
    elif word[-4:] == 'MENT' and _m_degree(word[:-4]) > 0:
        word = word[:-4]
    elif word[-3:] == 'ENT' and _m_degree(word[:-3]) > 0:
        word = word[:-3]
    elif (word[-4:] in ('SION', 'TION') and
          _m_degree(word[:-3]) > 0):
        word = word[:-3]
    elif word[-2:] == 'OU' and _m_degree(word[:-2]) > 0:
        word = word[:-2]
    elif word[-3:] == 'ISM' and _m_degree(word[:-3]) > 0:
        word = word[:-3]
    elif word[-3:] == 'ATE' and _m_degree(word[:-3]) > 0:
        word = word[:-3]
    elif word[-3:] == 'ITI' and _m_degree(word[:-3]) > 0:
        word = word[:-3]
    elif word[-3:] == 'OUS' and _m_degree(word[:-3]) > 0:
        word = word[:-3]
    elif word[-3:] == 'IVE' and _m_degree(word[:-3]) > 0:
        word = word[:-3]
    elif word[-3:] == 'IZE' and _m_degree(word[:-3]) > 0:
        word = word[:-3]

    # Step 5a
    if word[-1] == 'E' and _m_degree(word[:-1]) > 1:
        word = word[:-1]
    elif (word[-1] == 'E' and
          _m_degree(word[:-1]) == 1 and not _ends_in_cvc(word[:-1])):
        word = word[:-1]

    # Step 5b
    if word[-2:] == 'LL' and _m_degree(word) > 1:
        word = word[:-1]

    return word
