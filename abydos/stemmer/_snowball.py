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

"""abydos.stemmer._snowball.

The stemmer._snowball module defines the stemmers:

    - Porter
    - Porter2 (Snowball English)
    - Snowball German
    - Snowball Dutch
    - Snowball Norwegian
    - Snowball Swedish
    - Snowball Danish
"""

from __future__ import unicode_literals

from unicodedata import normalize

from six import text_type
from six.moves import range

__all__ = [
    'porter',
    'porter2',
    'sb_danish',
    'sb_dutch',
    'sb_german',
    'sb_norwegian',
    'sb_swedish',
]


def _m_degree(term, vowels):
    """Return Porter helper function _m_degree value.

    m-degree is equal to the number of V to C transitions

    :param str term: the word for which to calculate the m-degree
    :param set vowels: the set of vowels in the language
    :returns: the m-degree as defined in the Porter stemmer definition
    :rtype: int
    """
    mdeg = 0
    last_was_vowel = False
    for letter in term:
        if letter in vowels:
            last_was_vowel = True
        else:
            if last_was_vowel:
                mdeg += 1
            last_was_vowel = False
    return mdeg


def _sb_has_vowel(term, vowels):
    """Return Porter helper function _sb_has_vowel value.

    :param str term: the word to scan for vowels
    :param set vowels: the set of vowels in the language
    :returns: true iff a vowel exists in the term (as defined in the Porter
        stemmer definition)
    :rtype: bool
    """
    for letter in term:
        if letter in vowels:
            return True
    return False


def _ends_in_doubled_cons(term, vowels):
    """Return Porter helper function _ends_in_doubled_cons value.

    :param str term: the word to check for a final doubled consonant
    :param set vowels: the set of vowels in the language
    :returns: true iff the stem ends in a doubled consonant (as defined in the
        Porter stemmer definition)
    :rtype: bool
    """
    return len(term) > 1 and term[-1] not in vowels and term[-2] == term[-1]


def _ends_in_cvc(term, vowels):
    """Return Porter helper function _ends_in_cvc value.

    :param str term: the word to scan for cvc
    :param set vowels: the set of vowels in the language
    :returns: true iff the stem ends in cvc (as defined in the Porter stemmer
        definition)
    :rtype: bool
    """
    return len(term) > 2 and (
        term[-1] not in vowels
        and term[-2] in vowels
        and term[-3] not in vowels
        and term[-1] not in tuple('wxY')
    )


def porter(word, early_english=False):
    """Return Porter stem.

    The Porter stemmer is described in :cite:`Porter:1980`.

    :param str word: the word to calculate the stem of
    :param bool early_english: set to True in order to remove -eth & -est
        (2nd & 3rd person singular verbal agreement suffixes)
    :returns: word stem
    :rtype: str

    >>> porter('reading')
    'read'
    >>> porter('suspension')
    'suspens'
    >>> porter('elusiveness')
    'elus'

    >>> porter('eateth', early_english=True)
    'eat'
    """
    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    # Return word if stem is shorter than 2
    if len(word) < 3:
        return word

    _vowels = {'a', 'e', 'i', 'o', 'u', 'y'}
    # Re-map consonantal y to Y (Y will be C, y will be V)
    if word[0] == 'y':
        word = 'Y' + word[1:]
    for i in range(1, len(word)):
        if word[i] == 'y' and word[i - 1] in _vowels:
            word = word[:i] + 'Y' + word[i + 1 :]

    # Step 1a
    if word[-1] == 's':
        if word[-4:] == 'sses':
            word = word[:-2]
        elif word[-3:] == 'ies':
            word = word[:-2]
        elif word[-2:] == 'ss':
            pass
        else:
            word = word[:-1]

    # Step 1b
    step1b_flag = False
    if word[-3:] == 'eed':
        if _m_degree(word[:-3], _vowels) > 0:
            word = word[:-1]
    elif word[-2:] == 'ed':
        if _sb_has_vowel(word[:-2], _vowels):
            word = word[:-2]
            step1b_flag = True
    elif word[-3:] == 'ing':
        if _sb_has_vowel(word[:-3], _vowels):
            word = word[:-3]
            step1b_flag = True
    elif early_english:
        if word[-3:] == 'est':
            if _sb_has_vowel(word[:-3], _vowels):
                word = word[:-3]
                step1b_flag = True
        elif word[-3:] == 'eth':
            if _sb_has_vowel(word[:-3], _vowels):
                word = word[:-3]
                step1b_flag = True

    if step1b_flag:
        if word[-2:] in {'at', 'bl', 'iz'}:
            word += 'e'
        elif _ends_in_doubled_cons(word, _vowels) and word[-1] not in {
            'l',
            's',
            'z',
        }:
            word = word[:-1]
        elif _m_degree(word, _vowels) == 1 and _ends_in_cvc(word, _vowels):
            word += 'e'

    # Step 1c
    if word[-1] in {'Y', 'y'} and _sb_has_vowel(word[:-1], _vowels):
        word = word[:-1] + 'i'

    # Step 2
    if len(word) > 1:
        if word[-2] == 'a':
            if word[-7:] == 'ational':
                if _m_degree(word[:-7], _vowels) > 0:
                    word = word[:-5] + 'e'
            elif word[-6:] == 'tional':
                if _m_degree(word[:-6], _vowels) > 0:
                    word = word[:-2]
        elif word[-2] == 'c':
            if word[-4:] in {'enci', 'anci'}:
                if _m_degree(word[:-4], _vowels) > 0:
                    word = word[:-1] + 'e'
        elif word[-2] == 'e':
            if word[-4:] == 'izer':
                if _m_degree(word[:-4], _vowels) > 0:
                    word = word[:-1]
        elif word[-2] == 'g':
            if word[-4:] == 'logi':
                if _m_degree(word[:-4], _vowels) > 0:
                    word = word[:-1]
        elif word[-2] == 'l':
            if word[-3:] == 'bli':
                if _m_degree(word[:-3], _vowels) > 0:
                    word = word[:-1] + 'e'
            elif word[-4:] == 'alli':
                if _m_degree(word[:-4], _vowels) > 0:
                    word = word[:-2]
            elif word[-5:] == 'entli':
                if _m_degree(word[:-5], _vowels) > 0:
                    word = word[:-2]
            elif word[-3:] == 'eli':
                if _m_degree(word[:-3], _vowels) > 0:
                    word = word[:-2]
            elif word[-5:] == 'ousli':
                if _m_degree(word[:-5], _vowels) > 0:
                    word = word[:-2]
        elif word[-2] == 'o':
            if word[-7:] == 'ization':
                if _m_degree(word[:-7], _vowels) > 0:
                    word = word[:-5] + 'e'
            elif word[-5:] == 'ation':
                if _m_degree(word[:-5], _vowels) > 0:
                    word = word[:-3] + 'e'
            elif word[-4:] == 'ator':
                if _m_degree(word[:-4], _vowels) > 0:
                    word = word[:-2] + 'e'
        elif word[-2] == 's':
            if word[-5:] == 'alism':
                if _m_degree(word[:-5], _vowels) > 0:
                    word = word[:-3]
            elif word[-7:] in {'iveness', 'fulness', 'ousness'}:
                if _m_degree(word[:-7], _vowels) > 0:
                    word = word[:-4]
        elif word[-2] == 't':
            if word[-5:] == 'aliti':
                if _m_degree(word[:-5], _vowels) > 0:
                    word = word[:-3]
            elif word[-5:] == 'iviti':
                if _m_degree(word[:-5], _vowels) > 0:
                    word = word[:-3] + 'e'
            elif word[-6:] == 'biliti':
                if _m_degree(word[:-6], _vowels) > 0:
                    word = word[:-5] + 'le'

    # Step 3
    if word[-5:] == 'icate':
        if _m_degree(word[:-5], _vowels) > 0:
            word = word[:-3]
    elif word[-5:] == 'ative':
        if _m_degree(word[:-5], _vowels) > 0:
            word = word[:-5]
    elif word[-5:] in {'alize', 'iciti'}:
        if _m_degree(word[:-5], _vowels) > 0:
            word = word[:-3]
    elif word[-4:] == 'ical':
        if _m_degree(word[:-4], _vowels) > 0:
            word = word[:-2]
    elif word[-3:] == 'ful':
        if _m_degree(word[:-3], _vowels) > 0:
            word = word[:-3]
    elif word[-4:] == 'ness':
        if _m_degree(word[:-4], _vowels) > 0:
            word = word[:-4]

    # Step 4
    if word[-2:] == 'al':
        if _m_degree(word[:-2], _vowels) > 1:
            word = word[:-2]
    elif word[-4:] == 'ance':
        if _m_degree(word[:-4], _vowels) > 1:
            word = word[:-4]
    elif word[-4:] == 'ence':
        if _m_degree(word[:-4], _vowels) > 1:
            word = word[:-4]
    elif word[-2:] == 'er':
        if _m_degree(word[:-2], _vowels) > 1:
            word = word[:-2]
    elif word[-2:] == 'ic':
        if _m_degree(word[:-2], _vowels) > 1:
            word = word[:-2]
    elif word[-4:] == 'able':
        if _m_degree(word[:-4], _vowels) > 1:
            word = word[:-4]
    elif word[-4:] == 'ible':
        if _m_degree(word[:-4], _vowels) > 1:
            word = word[:-4]
    elif word[-3:] == 'ant':
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]
    elif word[-5:] == 'ement':
        if _m_degree(word[:-5], _vowels) > 1:
            word = word[:-5]
    elif word[-4:] == 'ment':
        if _m_degree(word[:-4], _vowels) > 1:
            word = word[:-4]
    elif word[-3:] == 'ent':
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]
    elif word[-4:] in {'sion', 'tion'}:
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]
    elif word[-2:] == 'ou':
        if _m_degree(word[:-2], _vowels) > 1:
            word = word[:-2]
    elif word[-3:] == 'ism':
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]
    elif word[-3:] == 'ate':
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]
    elif word[-3:] == 'iti':
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]
    elif word[-3:] == 'ous':
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]
    elif word[-3:] == 'ive':
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]
    elif word[-3:] == 'ize':
        if _m_degree(word[:-3], _vowels) > 1:
            word = word[:-3]

    # Step 5a
    if word[-1] == 'e':
        if _m_degree(word[:-1], _vowels) > 1:
            word = word[:-1]
        elif _m_degree(word[:-1], _vowels) == 1 and not _ends_in_cvc(
            word[:-1], _vowels
        ):
            word = word[:-1]

    # Step 5b
    if word[-2:] == 'll' and _m_degree(word, _vowels) > 1:
        word = word[:-1]

    # Change 'Y' back to 'y' if it survived stemming
    for i in range(len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i + 1 :]

    return word


def _sb_r1(term, vowels, r1_prefixes=None):
    """Return the R1 region, as defined in the Porter2 specification."""
    vowel_found = False
    if hasattr(r1_prefixes, '__iter__'):
        for prefix in r1_prefixes:
            if term[: len(prefix)] == prefix:
                return len(prefix)

    for i in range(len(term)):
        if not vowel_found and term[i] in vowels:
            vowel_found = True
        elif vowel_found and term[i] not in vowels:
            return i + 1
    return len(term)


def _sb_r2(term, vowels, r1_prefixes=None):
    """Return the R2 region, as defined in the Porter2 specification."""
    r1_start = _sb_r1(term, vowels, r1_prefixes)
    return r1_start + _sb_r1(term[r1_start:], vowels)


def _sb_ends_in_short_syllable(term, vowels, codanonvowels):
    """Return True iff term ends in a short syllable.

    (...according to the Porter2 specification.)

    NB: This is akin to the CVC test from the Porter stemmer. The description
    is unfortunately poor/ambiguous.
    """
    if not term:
        return False
    if len(term) == 2:
        if term[-2] in vowels and term[-1] not in vowels:
            return True
    elif len(term) >= 3:
        if (
            term[-3] not in vowels
            and term[-2] in vowels
            and term[-1] in codanonvowels
        ):
            return True
    return False


def _sb_short_word(term, vowels, codanonvowels, r1_prefixes=None):
    """Return True iff term is a short word.

    (...according to the Porter2 specification.)
    """
    if _sb_r1(term, vowels, r1_prefixes) == len(
        term
    ) and _sb_ends_in_short_syllable(term, vowels, codanonvowels):
        return True
    return False


def porter2(word, early_english=False):
    """Return the Porter2 (Snowball English) stem.

    The Porter2 (Snowball English) stemmer is defined in :cite:`Porter:2002`.

    :param str word: the word to calculate the stem of
    :param bool early_english: set to True in order to remove -eth & -est
        (2nd & 3rd person singular verbal agreement suffixes)
    :returns: word stem
    :rtype: str

    >>> porter2('reading')
    'read'
    >>> porter2('suspension')
    'suspens'
    >>> porter2('elusiveness')
    'elus'

    >>> porter2('eateth', early_english=True)
    'eat'
    """
    _vowels = {'a', 'e', 'i', 'o', 'u', 'y'}
    _codanonvowels = {
        "'",
        'b',
        'c',
        'd',
        'f',
        'g',
        'h',
        'j',
        'k',
        'l',
        'm',
        'n',
        'p',
        'q',
        'r',
        's',
        't',
        'v',
        'z',
    }
    _doubles = {'bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt'}
    _li = {'c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't'}

    # R1 prefixes should be in order from longest to shortest to prevent
    # masking
    _r1_prefixes = ('commun', 'gener', 'arsen')
    _exception1dict = {  # special changes:
        'skis': 'ski',
        'skies': 'sky',
        'dying': 'die',
        'lying': 'lie',
        'tying': 'tie',
        # special -LY cases:
        'idly': 'idl',
        'gently': 'gentl',
        'ugly': 'ugli',
        'early': 'earli',
        'only': 'onli',
        'singly': 'singl',
    }
    _exception1set = {
        'sky',
        'news',
        'howe',
        'atlas',
        'cosmos',
        'bias',
        'andes',
    }
    _exception2set = {
        'inning',
        'outing',
        'canning',
        'herring',
        'earring',
        'proceed',
        'exceed',
        'succeed',
    }

    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))
    # replace apostrophe-like characters with U+0027, per
    # http://snowball.tartarus.org/texts/apostrophe.html
    word = word.replace('’', '\'')
    word = word.replace('’', '\'')

    # Exceptions 1
    if word in _exception1dict:
        return _exception1dict[word]
    elif word in _exception1set:
        return word

    # Return word if stem is shorter than 3
    if len(word) < 3:
        return word

    # Remove initial ', if present.
    while word and word[0] == '\'':
        word = word[1:]
        # Return word if stem is shorter than 2
        if len(word) < 2:
            return word

    # Re-map vocalic Y to y (Y will be C, y will be V)
    if word[0] == 'y':
        word = 'Y' + word[1:]
    for i in range(1, len(word)):
        if word[i] == 'y' and word[i - 1] in _vowels:
            word = word[:i] + 'Y' + word[i + 1 :]

    r1_start = _sb_r1(word, _vowels, _r1_prefixes)
    r2_start = _sb_r2(word, _vowels, _r1_prefixes)

    # Step 0
    if word[-3:] == '\'s\'':
        word = word[:-3]
    elif word[-2:] == '\'s':
        word = word[:-2]
    elif word[-1:] == '\'':
        word = word[:-1]
    # Return word if stem is shorter than 2
    if len(word) < 3:
        return word

    # Step 1a
    if word[-4:] == 'sses':
        word = word[:-2]
    elif word[-3:] in {'ied', 'ies'}:
        if len(word) > 4:
            word = word[:-2]
        else:
            word = word[:-1]
    elif word[-2:] in {'us', 'ss'}:
        pass
    elif word[-1] == 's':
        if _sb_has_vowel(word[:-2], _vowels):
            word = word[:-1]

    # Exceptions 2
    if word in _exception2set:
        return word

    # Step 1b
    step1b_flag = False
    if word[-5:] == 'eedly':
        if len(word[r1_start:]) >= 5:
            word = word[:-3]
    elif word[-5:] == 'ingly':
        if _sb_has_vowel(word[:-5], _vowels):
            word = word[:-5]
            step1b_flag = True
    elif word[-4:] == 'edly':
        if _sb_has_vowel(word[:-4], _vowels):
            word = word[:-4]
            step1b_flag = True
    elif word[-3:] == 'eed':
        if len(word[r1_start:]) >= 3:
            word = word[:-1]
    elif word[-3:] == 'ing':
        if _sb_has_vowel(word[:-3], _vowels):
            word = word[:-3]
            step1b_flag = True
    elif word[-2:] == 'ed':
        if _sb_has_vowel(word[:-2], _vowels):
            word = word[:-2]
            step1b_flag = True
    elif early_english:
        if word[-3:] == 'est':
            if _sb_has_vowel(word[:-3], _vowels):
                word = word[:-3]
                step1b_flag = True
        elif word[-3:] == 'eth':
            if _sb_has_vowel(word[:-3], _vowels):
                word = word[:-3]
                step1b_flag = True

    if step1b_flag:
        if word[-2:] in {'at', 'bl', 'iz'}:
            word += 'e'
        elif word[-2:] in _doubles:
            word = word[:-1]
        elif _sb_short_word(word, _vowels, _codanonvowels, _r1_prefixes):
            word += 'e'

    # Step 1c
    if len(word) > 2 and word[-1] in {'Y', 'y'} and word[-2] not in _vowels:
        word = word[:-1] + 'i'

    # Step 2
    if word[-2] == 'a':
        if word[-7:] == 'ational':
            if len(word[r1_start:]) >= 7:
                word = word[:-5] + 'e'
        elif word[-6:] == 'tional':
            if len(word[r1_start:]) >= 6:
                word = word[:-2]
    elif word[-2] == 'c':
        if word[-4:] in {'enci', 'anci'}:
            if len(word[r1_start:]) >= 4:
                word = word[:-1] + 'e'
    elif word[-2] == 'e':
        if word[-4:] == 'izer':
            if len(word[r1_start:]) >= 4:
                word = word[:-1]
    elif word[-2] == 'g':
        if word[-3:] == 'ogi':
            if r1_start >= 1 and len(word[r1_start:]) >= 3 and word[-4] == 'l':
                word = word[:-1]
    elif word[-2] == 'l':
        if word[-6:] == 'lessli':
            if len(word[r1_start:]) >= 6:
                word = word[:-2]
        elif word[-5:] in {'entli', 'fulli', 'ousli'}:
            if len(word[r1_start:]) >= 5:
                word = word[:-2]
        elif word[-4:] == 'abli':
            if len(word[r1_start:]) >= 4:
                word = word[:-1] + 'e'
        elif word[-4:] == 'alli':
            if len(word[r1_start:]) >= 4:
                word = word[:-2]
        elif word[-3:] == 'bli':
            if len(word[r1_start:]) >= 3:
                word = word[:-1] + 'e'
        elif word[-2:] == 'li':
            if r1_start >= 1 and len(word[r1_start:]) >= 2 and word[-3] in _li:
                word = word[:-2]
    elif word[-2] == 'o':
        if word[-7:] == 'ization':
            if len(word[r1_start:]) >= 7:
                word = word[:-5] + 'e'
        elif word[-5:] == 'ation':
            if len(word[r1_start:]) >= 5:
                word = word[:-3] + 'e'
        elif word[-4:] == 'ator':
            if len(word[r1_start:]) >= 4:
                word = word[:-2] + 'e'
    elif word[-2] == 's':
        if word[-7:] in {'fulness', 'ousness', 'iveness'}:
            if len(word[r1_start:]) >= 7:
                word = word[:-4]
        elif word[-5:] == 'alism':
            if len(word[r1_start:]) >= 5:
                word = word[:-3]
    elif word[-2] == 't':
        if word[-6:] == 'biliti':
            if len(word[r1_start:]) >= 6:
                word = word[:-5] + 'le'
        elif word[-5:] == 'aliti':
            if len(word[r1_start:]) >= 5:
                word = word[:-3]
        elif word[-5:] == 'iviti':
            if len(word[r1_start:]) >= 5:
                word = word[:-3] + 'e'

    # Step 3
    if word[-7:] == 'ational':
        if len(word[r1_start:]) >= 7:
            word = word[:-5] + 'e'
    elif word[-6:] == 'tional':
        if len(word[r1_start:]) >= 6:
            word = word[:-2]
    elif word[-5:] in {'alize', 'icate', 'iciti'}:
        if len(word[r1_start:]) >= 5:
            word = word[:-3]
    elif word[-5:] == 'ative':
        if len(word[r2_start:]) >= 5:
            word = word[:-5]
    elif word[-4:] == 'ical':
        if len(word[r1_start:]) >= 4:
            word = word[:-2]
    elif word[-4:] == 'ness':
        if len(word[r1_start:]) >= 4:
            word = word[:-4]
    elif word[-3:] == 'ful':
        if len(word[r1_start:]) >= 3:
            word = word[:-3]

    # Step 4
    for suffix in (
        'ement',
        'ance',
        'ence',
        'able',
        'ible',
        'ment',
        'ant',
        'ent',
        'ism',
        'ate',
        'iti',
        'ous',
        'ive',
        'ize',
        'al',
        'er',
        'ic',
    ):
        if word[-len(suffix) :] == suffix:
            if len(word[r2_start:]) >= len(suffix):
                word = word[: -len(suffix)]
            break
    else:
        if word[-3:] == 'ion':
            if (
                len(word[r2_start:]) >= 3
                and len(word) >= 4
                and word[-4] in tuple('st')
            ):
                word = word[:-3]

    # Step 5
    if word[-1] == 'e':
        if len(word[r2_start:]) >= 1 or (
            len(word[r1_start:]) >= 1
            and not _sb_ends_in_short_syllable(
                word[:-1], _vowels, _codanonvowels
            )
        ):
            word = word[:-1]
    elif word[-1] == 'l':
        if len(word[r2_start:]) >= 1 and word[-2] == 'l':
            word = word[:-1]

    # Change 'Y' back to 'y' if it survived stemming
    for i in range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i + 1 :]

    return word


def sb_german(word, alternate_vowels=False):
    """Return Snowball German stem.

    The Snowball German stemmer is defined at:
    http://snowball.tartarus.org/algorithms/german/stemmer.html

    :param str word: the word to calculate the stem of
    :param bool alternate_vowels: composes ae as ä, oe as ö, and ue as ü before
        running the algorithm
    :returns: word stem
    :rtype: str

    >>> sb_german('lesen')
    'les'
    >>> sb_german('graues')
    'grau'
    >>> sb_german('buchstabieren')
    'buchstabi'
    """
    _vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ö', 'ü'}
    _s_endings = {'b', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'r', 't'}
    _st_endings = {'b', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 't'}

    # lowercase, normalize, and compose
    word = normalize('NFC', word.lower())
    word = word.replace('ß', 'ss')

    if len(word) > 2:
        for i in range(2, len(word)):
            if word[i] in _vowels and word[i - 2] in _vowels:
                if word[i - 1] == 'u':
                    word = word[: i - 1] + 'U' + word[i:]
                elif word[i - 1] == 'y':
                    word = word[: i - 1] + 'Y' + word[i:]

    if alternate_vowels:
        word = word.replace('ae', 'ä')
        word = word.replace('oe', 'ö')
        word = word.replace('que', 'Q')
        word = word.replace('ue', 'ü')
        word = word.replace('Q', 'que')

    r1_start = max(3, _sb_r1(word, _vowels))
    r2_start = _sb_r2(word, _vowels)

    # Step 1
    niss_flag = False
    if word[-3:] == 'ern':
        if len(word[r1_start:]) >= 3:
            word = word[:-3]
    elif word[-2:] == 'em':
        if len(word[r1_start:]) >= 2:
            word = word[:-2]
    elif word[-2:] == 'er':
        if len(word[r1_start:]) >= 2:
            word = word[:-2]
    elif word[-2:] == 'en':
        if len(word[r1_start:]) >= 2:
            word = word[:-2]
            niss_flag = True
    elif word[-2:] == 'es':
        if len(word[r1_start:]) >= 2:
            word = word[:-2]
            niss_flag = True
    elif word[-1:] == 'e':
        if len(word[r1_start:]) >= 1:
            word = word[:-1]
            niss_flag = True
    elif word[-1:] == 's':
        if (
            len(word[r1_start:]) >= 1
            and len(word) >= 2
            and word[-2] in _s_endings
        ):
            word = word[:-1]

    if niss_flag and word[-4:] == 'niss':
        word = word[:-1]

    # Step 2
    if word[-3:] == 'est':
        if len(word[r1_start:]) >= 3:
            word = word[:-3]
    elif word[-2:] == 'en':
        if len(word[r1_start:]) >= 2:
            word = word[:-2]
    elif word[-2:] == 'er':
        if len(word[r1_start:]) >= 2:
            word = word[:-2]
    elif word[-2:] == 'st':
        if (
            len(word[r1_start:]) >= 2
            and len(word) >= 6
            and word[-3] in _st_endings
        ):
            word = word[:-2]

    # Step 3
    if word[-4:] == 'isch':
        if len(word[r2_start:]) >= 4 and word[-5] != 'e':
            word = word[:-4]
    elif word[-4:] in {'lich', 'heit'}:
        if len(word[r2_start:]) >= 4:
            word = word[:-4]
            if word[-2:] in {'er', 'en'} and len(word[r1_start:]) >= 2:
                word = word[:-2]
    elif word[-4:] == 'keit':
        if len(word[r2_start:]) >= 4:
            word = word[:-4]
            if word[-4:] == 'lich' and len(word[r2_start:]) >= 4:
                word = word[:-4]
            elif word[-2:] == 'ig' and len(word[r2_start:]) >= 2:
                word = word[:-2]
    elif word[-3:] in {'end', 'ung'}:
        if len(word[r2_start:]) >= 3:
            word = word[:-3]
            if (
                word[-2:] == 'ig'
                and len(word[r2_start:]) >= 2
                and word[-3] != 'e'
            ):
                word = word[:-2]
    elif word[-2:] in {'ig', 'ik'}:
        if len(word[r2_start:]) >= 2 and word[-3] != 'e':
            word = word[:-2]

    # Change 'Y' and 'U' back to lowercase if survived stemming
    for i in range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i + 1 :]
        elif word[i] == 'U':
            word = word[:i] + 'u' + word[i + 1 :]

    # Remove umlauts
    _umlauts = dict(zip((ord(_) for _ in 'äöü'), 'aou'))
    word = word.translate(_umlauts)

    return word


def sb_dutch(word):
    """Return Snowball Dutch stem.

    The Snowball Dutch stemmer is defined at:
    http://snowball.tartarus.org/algorithms/dutch/stemmer.html

    :param str word: the word to calculate the stem of
    :returns: word stem
    :rtype: str

    >>> sb_dutch('lezen')
    'lez'
    >>> sb_dutch('opschorting')
    'opschort'
    >>> sb_dutch('ongrijpbaarheid')
    'ongrijp'
    """
    _vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'è'}
    _not_s_endings = {'a', 'e', 'i', 'j', 'o', 'u', 'y', 'è'}

    def _undouble(word):
        """Undouble endings -kk, -dd, and -tt."""
        if (
            len(word) > 1
            and word[-1] == word[-2]
            and word[-1] in {'d', 'k', 't'}
        ):
            return word[:-1]
        return word

    # lowercase, normalize, decompose, filter umlauts & acutes out, and compose
    word = normalize('NFC', text_type(word.lower()))
    _accented = dict(zip((ord(_) for _ in 'äëïöüáéíóú'), 'aeiouaeiou'))
    word = word.translate(_accented)

    for i in range(len(word)):
        if i == 0 and word[0] == 'y':
            word = 'Y' + word[1:]
        elif word[i] == 'y' and word[i - 1] in _vowels:
            word = word[:i] + 'Y' + word[i + 1 :]
        elif (
            word[i] == 'i'
            and word[i - 1] in _vowels
            and i + 1 < len(word)
            and word[i + 1] in _vowels
        ):
            word = word[:i] + 'I' + word[i + 1 :]

    r1_start = max(3, _sb_r1(word, _vowels))
    r2_start = _sb_r2(word, _vowels)

    # Step 1
    if word[-5:] == 'heden':
        if len(word[r1_start:]) >= 5:
            word = word[:-3] + 'id'
    elif word[-3:] == 'ene':
        if len(word[r1_start:]) >= 3 and (
            word[-4] not in _vowels and word[-6:-3] != 'gem'
        ):
            word = _undouble(word[:-3])
    elif word[-2:] == 'en':
        if len(word[r1_start:]) >= 2 and (
            word[-3] not in _vowels and word[-5:-2] != 'gem'
        ):
            word = _undouble(word[:-2])
    elif word[-2:] == 'se':
        if len(word[r1_start:]) >= 2 and word[-3] not in _not_s_endings:
            word = word[:-2]
    elif word[-1:] == 's':
        if len(word[r1_start:]) >= 1 and word[-2] not in _not_s_endings:
            word = word[:-1]

    # Step 2
    e_removed = False
    if word[-1:] == 'e':
        if len(word[r1_start:]) >= 1 and word[-2] not in _vowels:
            word = _undouble(word[:-1])
            e_removed = True

    # Step 3a
    if word[-4:] == 'heid':
        if len(word[r2_start:]) >= 4 and word[-5] != 'c':
            word = word[:-4]
            if word[-2:] == 'en':
                if len(word[r1_start:]) >= 2 and (
                    word[-3] not in _vowels and word[-5:-2] != 'gem'
                ):
                    word = _undouble(word[:-2])

    # Step 3b
    if word[-4:] == 'lijk':
        if len(word[r2_start:]) >= 4:
            word = word[:-4]
            # Repeat step 2
            if word[-1:] == 'e':
                if len(word[r1_start:]) >= 1 and word[-2] not in _vowels:
                    word = _undouble(word[:-1])
    elif word[-4:] == 'baar':
        if len(word[r2_start:]) >= 4:
            word = word[:-4]
    elif word[-3:] in ('end', 'ing'):
        if len(word[r2_start:]) >= 3:
            word = word[:-3]
            if (
                word[-2:] == 'ig'
                and len(word[r2_start:]) >= 2
                and word[-3] != 'e'
            ):
                word = word[:-2]
            else:
                word = _undouble(word)
    elif word[-3:] == 'bar':
        if len(word[r2_start:]) >= 3 and e_removed:
            word = word[:-3]
    elif word[-2:] == 'ig':
        if len(word[r2_start:]) >= 2 and word[-3] != 'e':
            word = word[:-2]

    # Step 4
    if (
        len(word) >= 4
        and word[-3] == word[-2]
        and word[-2] in {'a', 'e', 'o', 'u'}
        and word[-4] not in _vowels
        and word[-1] not in _vowels
        and word[-1] != 'I'
    ):
        word = word[:-2] + word[-1]

    # Change 'Y' and 'U' back to lowercase if survived stemming
    for i in range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i + 1 :]
        elif word[i] == 'I':
            word = word[:i] + 'i' + word[i + 1 :]

    return word


def sb_norwegian(word):
    """Return Snowball Norwegian stem.

    The Snowball Norwegian stemmer is defined at:
    http://snowball.tartarus.org/algorithms/norwegian/stemmer.html

    :param str word: the word to calculate the stem of
    :returns: word stem
    :rtype: str

    >>> sb_norwegian('lese')
    'les'
    >>> sb_norwegian('suspensjon')
    'suspensjon'
    >>> sb_norwegian('sikkerhet')
    'sikker'
    """
    _vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'å', 'æ', 'ø'}
    _s_endings = {
        'b',
        'c',
        'd',
        'f',
        'g',
        'h',
        'j',
        'l',
        'm',
        'n',
        'o',
        'p',
        'r',
        't',
        'v',
        'y',
        'z',
    }
    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    r1_start = min(max(3, _sb_r1(word, _vowels)), len(word))

    # Step 1
    _r1 = word[r1_start:]
    if _r1[-7:] == 'hetenes':
        word = word[:-7]
    elif _r1[-6:] in {'hetene', 'hetens'}:
        word = word[:-6]
    elif _r1[-5:] in {'heten', 'heter', 'endes'}:
        word = word[:-5]
    elif _r1[-4:] in {'ande', 'ende', 'edes', 'enes', 'erte'}:
        if word[-4:] == 'erte':
            word = word[:-2]
        else:
            word = word[:-4]
    elif _r1[-3:] in {
        'ede',
        'ane',
        'ene',
        'ens',
        'ers',
        'ets',
        'het',
        'ast',
        'ert',
    }:
        if word[-3:] == 'ert':
            word = word[:-1]
        else:
            word = word[:-3]
    elif _r1[-2:] in {'en', 'ar', 'er', 'as', 'es', 'et'}:
        word = word[:-2]
    elif _r1[-1:] in {'a', 'e'}:
        word = word[:-1]
    elif _r1[-1:] == 's':
        if (len(word) > 1 and word[-2] in _s_endings) or (
            len(word) > 2 and word[-2] == 'k' and word[-3] not in _vowels
        ):
            word = word[:-1]

    # Step 2
    if word[r1_start:][-2:] in {'dt', 'vt'}:
        word = word[:-1]

    # Step 3
    _r1 = word[r1_start:]
    if _r1[-7:] == 'hetslov':
        word = word[:-7]
    elif _r1[-4:] in {'eleg', 'elig', 'elov', 'slov'}:
        word = word[:-4]
    elif _r1[-3:] in {'leg', 'eig', 'lig', 'els', 'lov'}:
        word = word[:-3]
    elif _r1[-2:] == 'ig':
        word = word[:-2]

    return word


def sb_swedish(word):
    """Return Snowball Swedish stem.

    The Snowball Swedish stemmer is defined at:
    http://snowball.tartarus.org/algorithms/swedish/stemmer.html

    :param str word: the word to calculate the stem of
    :returns: word stem
    :rtype: str

    >>> sb_swedish('undervisa')
    'undervis'
    >>> sb_swedish('suspension')
    'suspension'
    >>> sb_swedish('visshet')
    'viss'
    """
    _vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'ä', 'å', 'ö'}
    _s_endings = {
        'b',
        'c',
        'd',
        'f',
        'g',
        'h',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'r',
        't',
        'v',
        'y',
    }

    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    r1_start = min(max(3, _sb_r1(word, _vowels)), len(word))

    # Step 1
    _r1 = word[r1_start:]
    if _r1[-7:] == 'heterna':
        word = word[:-7]
    elif _r1[-6:] == 'hetens':
        word = word[:-6]
    elif _r1[-5:] in {
        'anden',
        'heten',
        'heter',
        'arnas',
        'ernas',
        'ornas',
        'andes',
        'arens',
        'andet',
    }:
        word = word[:-5]
    elif _r1[-4:] in {
        'arna',
        'erna',
        'orna',
        'ande',
        'arne',
        'aste',
        'aren',
        'ades',
        'erns',
    }:
        word = word[:-4]
    elif _r1[-3:] in {'ade', 'are', 'ern', 'ens', 'het', 'ast'}:
        word = word[:-3]
    elif _r1[-2:] in {'ad', 'en', 'ar', 'er', 'or', 'as', 'es', 'at'}:
        word = word[:-2]
    elif _r1[-1:] in {'a', 'e'}:
        word = word[:-1]
    elif _r1[-1:] == 's':
        if len(word) > 1 and word[-2] in _s_endings:
            word = word[:-1]

    # Step 2
    if word[r1_start:][-2:] in {'dd', 'gd', 'nn', 'dt', 'gt', 'kt', 'tt'}:
        word = word[:-1]

    # Step 3
    _r1 = word[r1_start:]
    if _r1[-5:] == 'fullt':
        word = word[:-1]
    elif _r1[-4:] == 'löst':
        word = word[:-1]
    elif _r1[-3:] in {'lig', 'els'}:
        word = word[:-3]
    elif _r1[-2:] == 'ig':
        word = word[:-2]

    return word


def sb_danish(word):
    """Return Snowball Danish stem.

    The Snowball Danish stemmer is defined at:
    http://snowball.tartarus.org/algorithms/danish/stemmer.html

    :param str word: the word to calculate the stem of
    :returns: word stem
    :rtype: str

    >>> sb_danish('underviser')
    'undervis'
    >>> sb_danish('suspension')
    'suspension'
    >>> sb_danish('sikkerhed')
    'sikker'
    """
    _vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'å', 'æ', 'ø'}
    _s_endings = {
        'a',
        'b',
        'c',
        'd',
        'f',
        'g',
        'h',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'r',
        't',
        'v',
        'y',
        'z',
        'å',
    }

    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    r1_start = min(max(3, _sb_r1(word, _vowels)), len(word))

    # Step 1
    _r1 = word[r1_start:]
    if _r1[-7:] == 'erendes':
        word = word[:-7]
    elif _r1[-6:] in {'erende', 'hedens'}:
        word = word[:-6]
    elif _r1[-5:] in {
        'ethed',
        'erede',
        'heden',
        'heder',
        'endes',
        'ernes',
        'erens',
        'erets',
    }:
        word = word[:-5]
    elif _r1[-4:] in {
        'ered',
        'ende',
        'erne',
        'eren',
        'erer',
        'heds',
        'enes',
        'eres',
        'eret',
    }:
        word = word[:-4]
    elif _r1[-3:] in {'hed', 'ene', 'ere', 'ens', 'ers', 'ets'}:
        word = word[:-3]
    elif _r1[-2:] in {'en', 'er', 'es', 'et'}:
        word = word[:-2]
    elif _r1[-1:] == 'e':
        word = word[:-1]
    elif _r1[-1:] == 's':
        if len(word) > 1 and word[-2] in _s_endings:
            word = word[:-1]

    # Step 2
    if word[r1_start:][-2:] in {'gd', 'dt', 'gt', 'kt'}:
        word = word[:-1]

    # Step 3
    if word[-4:] == 'igst':
        word = word[:-2]

    _r1 = word[r1_start:]
    repeat_step2 = False
    if _r1[-4:] == 'elig':
        word = word[:-4]
        repeat_step2 = True
    elif _r1[-4:] == 'løst':
        word = word[:-1]
    elif _r1[-3:] in {'lig', 'els'}:
        word = word[:-3]
        repeat_step2 = True
    elif _r1[-2:] == 'ig':
        word = word[:-2]
        repeat_step2 = True

    if repeat_step2:
        if word[r1_start:][-2:] in {'gd', 'dt', 'gt', 'kt'}:
            word = word[:-1]

    # Step 4
    if (
        len(word[r1_start:]) >= 1
        and len(word) >= 2
        and word[-1] == word[-2]
        and word[-1] not in _vowels
    ):
        word = word[:-1]

    return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
