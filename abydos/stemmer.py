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

def _m_degree(term):
    """Return the m-degree as defined in the Porter stemmer definition

    Arguments:
    term -- the word for which to calculate the m-degree

    Description:
    m-degree is equal to the number of V to C transitions
    """
    _vowels = tuple('AEIOU')
    mdeg = 0
    last_was_vowel = False
    for letter in term:
        if letter in _vowels or (last_was_vowel and letter == 'Y'):
            last_was_vowel = True
        else:
            if last_was_vowel:
                mdeg += 1
            last_was_vowel = False
    return mdeg

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

    m_deg = _m_degree(word)
    has_vowel = False
    double_cons_end = False
    cvc_end = False

    # Step 1a
    if word.endswith('SSES'):
        word = word[:-2]
    elif word.endswith('IES'):
        word = word[:-2]
    elif word.endswith('SS'):
        pass
    elif word.endswith('S'):
        word = word[:-1]

    # Step 1b
    oneb_flag = False
    if m_deg > 0 and word.endswith('EED'):
        word = word[:-1]
    elif has_vowel and word.endswith('ED'):
        word = word[:-2]
        oneb_flag = True
    elif has_vowel and word.endswith('ING'):
        word = word[:-3]
        oneb_flag = True

    if oneb_flag:
        if word.endswith('AT') or word.endswith('BL') or word.endswith('IZ'):
            word += 'E'
        elif double_cons_end and word[-1] not in tuple('LSZ'):
            word = word[:-1]
        elif m_deg == 1 and cvc_end:
            word += 'E'

    # Step 1c
    if has_vowel and word.endswith('Y'):
        word = word[:-1] + 'I'

    # Step 2
    if m_deg > 0:
        if word.endswith('ATIONAL'):
            word = word[:-5] + 'E'
        elif word.endswith('TIONAL'):
            word = word[:-2]
        elif word.endswith('ENCI') or word.endswith('ANCI'):
            word = word[:-1] + 'E'
        elif word.endswith('IZER'):
            word = word[:-1]
        elif word.endswith('ABLI'):
            word = word[:-1] + 'E'
        elif (word.endswith('ALLI') or word.endswith('ENTLI') or
              word.endswith('ELI') or word.endswith('OUSLI')):
            word = word[:-2]
        elif word.endswith('IZATION'):
            word = word[:-5] + 'E'
        elif word.endswith('ATION'):
            word = word[:-3] + 'E'
        elif word.endswith('ATOR'):
            word = word[:-2] + 'E'
        elif word.endswith('ALISM'):
            word = word[:-3]
        elif (word.endswith('IVENESS') or word.endswith('FULNESS') or
              word.endswith('OUSNESS')):
            word = word[:-4]
        elif word.endswith('ALITI'):
            word = word[:-3]
        elif word.endswith('IVITI') or word.endswith('BLITI'):
            word = word[:-3] + 'E'

    # Step 3
    if m_deg > 0:
        if word.endswith('ICATE'):
            word = word[:-3]
        elif word.endswith('ATIVE'):
            word = word[:-5]
        elif word.endswith('ALIZE') or word.endsiwth('ICITI'):
            word = word[:-3]
        elif word.endsiwth('ICAL'):
            word = word[:-2]
        elif word.endswith('FUL'):
            word = word[:-3]
        elif word.endswith('NESS'):
            word = word[:-4]

    # Step 4
    if m_deg > 1:
        if word.endswith('AL'):
            word = word[:-2]
        elif word.endswith('ANCE'):
            word = word[:-4]
        elif word.endswith('ENCE'):
            word = word[:-4]
        elif word.endswith('ER'):
            word = word[:-2]
        elif word.endswith('IC'):
            word = word[:-2]
        elif word.endswith('ABLE'):
            word = word[:-4]
        elif word.endswith('IBLE'):
            word = word[:-4]
        elif word.endswith('ANT'):
            word = word[:-3]
        elif word.endswith('EMENT'):
            word = word[:-5]
        elif word.endswith('MENT'):
            word = word[:-4]
        elif word.endswith('ENT'):
            word = word[:-3]
        elif word.endswith('SION') or word.endswith('TION'):
            word = word[:-3]
        elif word.endswith('OU'):
            word = word[:-2]
        elif word.endswith('ISM'):
            word = word[:-3]
        elif word.endswith('ATE'):
            word = word[:-3]
        elif word.endswith('ITI'):
            word = word[:-3]
        elif word.endswith('OUS'):
            word = word[:-3]
        elif word.endswith('IVE'):
            word = word[:-3]
        elif word.endswith('IZE'):
            word = word[:-3]

    # Step 5a
    if m_deg > 1 and word.endswith('E'):
        word = word[:-1]
    elif m_deg == 1 and not cvc_end and word.endswith('E'):
        word = word[:-1]

    # Step 5b
    if m_deg > 1 and double_cons_end and word.endswith('L'):
        word = word[:-1]

    return word
