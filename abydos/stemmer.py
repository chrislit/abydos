# -*- coding: utf-8 -*-
"""abydos.stemmer

The stemmer module defines word stemmers including:
    the Lovins stemmer
    the Porter and Porter2 stemmers
    Snowball stemmers for German, Dutch, Norwegian, Swedish, and Danish
    CLEF German, German plus, and Swedish stemmers
    the UEA-lite stemmer
    the Lancaster Stemming Algorithm
    Caumann's German stemmer


Copyright 2014-2015 by Christopher C. Little.
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


def lovins(word):
    """Implementation of Lovins stemmer by Julie Beth Lovins

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The Lovins stemmer is described in her article at
    http://www.mt-archive.info/MT-1968-Lovins.pdf
    """

    stems = frozenset(['alistically', 'arizability', 'izationally',
                       'antialness', 'arisations', 'arizations', 'entialness',
                       'allically', 'antaneous', 'antiality', 'arisation',
                       'arization', 'ationally', 'ativeness', 'eableness',
                       'entations', 'entiality', 'entialize', 'entiation',
                       'ionalness', 'istically', 'itousness', 'izability',
                       'izational', 'ableness', 'arizable', 'entation',
                       'entially', 'eousness', 'ibleness', 'icalness',
                       'ionalism', 'ionality', 'ionalize', 'iousness',
                       'izations', 'lessness', 'ability', 'aically',
                       'alistic', 'alities', 'ariness', 'aristic',
                       'arizing', 'ateness', 'atingly', 'ational',
                       'atively', 'ativism', 'elihood', 'encible',
                       'entally', 'entials', 'entiate', 'entness',
                       'fulness', 'ibility', 'icalism', 'icalist',
                       'icality', 'icalize', 'ication', 'icianry',
                       'ination', 'ingness', 'ionally', 'isation',
                       'ishness', 'istical', 'iteness', 'iveness',
                       'ivistic', 'ivities', 'ization', 'izement',
                       'oidally', 'ousness', 'aceous', 'acious', 'action',
                       'alness', 'ancial', 'ancies', 'ancing', 'ariser',
                       'arized', 'arizer', 'atable', 'ations', 'atives',
                       'eature', 'efully', 'encies', 'encing', 'ential',
                       'enting', 'entist', 'eously', 'ialist', 'iality',
                       'ialize', 'ically', 'icance', 'icians', 'icists',
                       'ifully', 'ionals', 'ionate', 'ioning', 'ionist',
                       'iously', 'istics', 'izable', 'lessly', 'nesses',
                       'oidism', 'acies', 'acity', 'aging', 'aical', 'alist',
                       'alism', 'ality', 'alize', 'allic', 'anced', 'ances',
                       'antic', 'arial', 'aries', 'arily', 'arity', 'arize',
                       'aroid', 'ately', 'ating', 'ation', 'ative', 'ators',
                       'atory', 'ature', 'early', 'ehood', 'eless', 'elity',
                       'ement', 'enced', 'ences', 'eness', 'ening', 'ental',
                       'ented', 'ently', 'fully', 'ially', 'icant', 'ician',
                       'icide', 'icism', 'icist', 'icity', 'idine', 'iedly',
                       'ihood', 'inate', 'iness', 'ingly', 'inism', 'inity',
                       'ional', 'ioned', 'ished', 'istic', 'ities', 'itous',
                       'ively', 'ivity', 'izers', 'izing', 'oidal', 'oides',
                       'otide', 'ously', 'able', 'ably', 'ages', 'ally',
                       'ance', 'ancy', 'ants', 'aric', 'arly', 'ated', 'ates',
                       'atic', 'ator', 'ealy', 'edly', 'eful', 'eity', 'ence',
                       'ency', 'ened', 'enly', 'eous', 'hood', 'ials', 'ians',
                       'ible', 'ibly', 'ical', 'ides', 'iers', 'iful', 'ines',
                       'ings', 'ions', 'ious', 'isms', 'ists', 'itic', 'ized',
                       'izer', 'less', 'lily', 'ness', 'ogen', 'ward', 'wise',
                       'ying', 'yish', 'acy', 'age', 'aic', 'als', 'ant',
                       'ars', 'ary', 'ata', 'ate', 'eal', 'ear', 'ely', 'ene',
                       'ent', 'ery', 'ese', 'ful', 'ial', 'ian', 'ics', 'ide',
                       'ied', 'ier', 'ies', 'ily', 'ine', 'ing', 'ion', 'ish',
                       'ism', 'ist', 'ite', 'ity', 'ium', 'ive', 'ize', 'oid',
                       'one', 'ous', 'ae', 'al', 'ar', 'as', 'ed', 'en', 'es',
                       'ia', 'ic', 'is', 'ly', 'on', 'or', 'um', 'us', 'yl',
                       '\'s', 's\'', 'a', 'e', 'i', 'o', 's', 'y'])

    return word


def _m_degree(term, vowels):
    """Return the m-degree as defined in the Porter stemmer definition

    Arguments:
    term -- the word for which to calculate the m-degree
    vowels -- the set of vowels in the language

    Description:
    m-degree is equal to the number of V to C transitions
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
    """Return true iff a vowel exists in the term (as defined in the Porter
    stemmer definition)

    Arguments:
    term -- the word to scan for vowels
    vowels -- the set of vowels in the language
    """
    for letter in term:
        if letter in vowels:
            return True
    return False


def _ends_in_doubled_cons(term, vowels):
    """Return true iff the stem ends in a doubled consonant (as defined in the
    Porter stemmer definition)

    Arguments:
    term -- the word to check for a final doubled consonant
    vowels -- the set of vowels in the language
    """
    if len(term) > 1 and term[-1] not in vowels and term[-2] == term[-1]:
        return True
    return False


def _ends_in_cvc(term, vowels):
    """Return true iff the stem ends in cvc (as defined in the Porter stemmer
    definition)

    Arguments:
    term -- the word to scan for cvc
    vowels -- the set of vowels in the language
    """
    if len(term) > 2 and (term[-1] not in vowels and
                          term[-2] in vowels and
                          term[-3] not in vowels and
                          term[-1] not in tuple('wxY')):
        return True
    return False


def porter(word, early_english=False):
    """Implementation of Porter stemmer -- ideally returns the word stem

    Arguments:
    word -- the word to calculate the stem of
    early_english -- set to True in order to remove -eth & -est (2nd & 3rd
        person singular verbal agreement suffixes)

    Description:
    The Porter stemmer is defined at
    http://snowball.tartarus.org/algorithms/porter/stemmer.html
    """
    # pylint: disable=too-many-branches

    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))

    # Return word if stem is shorter than 2
    if len(word) < 3:
        return word

    _vowels = frozenset('aeiouy')
    # Re-map consonantal y to Y (Y will be C, y will be V)
    if word[0] == 'y':
        word = 'Y' + word[1:]
    for i in _range(1, len(word)):
        if word[i] == 'y' and word[i-1] in _vowels:
            word = word[:i] + 'Y' + word[i+1:]

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
        if word[-2:] in frozenset(['at', 'bl', 'iz']):
            word += 'e'
        elif (_ends_in_doubled_cons(word, _vowels) and
              word[-1] not in frozenset('lsz')):
            word = word[:-1]
        elif _m_degree(word, _vowels) == 1 and _ends_in_cvc(word, _vowels):
            word += 'e'

    # Step 1c
    if word[-1] in frozenset('Yy') and _sb_has_vowel(word[:-1], _vowels):
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
            if word[-4:] in frozenset(['enci', 'anci']):
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
            elif word[-7:] in frozenset(['iveness', 'fulness', 'ousness']):
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
    elif word[-5:] in frozenset(['alize', 'iciti']):
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
    elif word[-4:] in frozenset(['sion', 'tion']):
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
        elif (_m_degree(word[:-1], _vowels) == 1 and
              not _ends_in_cvc(word[:-1], _vowels)):
            word = word[:-1]

    # Step 5b
    if word[-2:] == 'll' and _m_degree(word, _vowels) > 1:
        word = word[:-1]

    # Change 'Y' back to 'y' if it survived stemming
    for i in _range(len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]

    return word


def _sb_r1(term, vowels, r1_prefixes=None):
    """Return the R1 region, as defined in the Porter2 specification
    """
    vowel_found = False
    if hasattr(r1_prefixes, '__iter__'):
        for prefix in r1_prefixes:
            if term[:len(prefix)] == prefix:
                return len(prefix)

    for i in _range(len(term)):
        if not vowel_found and term[i] in vowels:
            vowel_found = True
        elif vowel_found and term[i] not in vowels:
            return i+1
    return len(term)


def _sb_r2(term, vowels, r1_prefixes=None):
    """Return the R2 region, as defined in the Porter2 specification
    """
    r1_start = _sb_r1(term, vowels, r1_prefixes)
    return r1_start + _sb_r1(term[r1_start:], vowels)


def _sb_ends_in_short_syllable(term, vowels, codanonvowels):
    """Return True iff term ends in a short syllable,
    according to the Porter2 specification

    NB: This is akin to the CVC test from the Porter stemmer. The description
    is unfortunately poor/ambiguous.
    """
    if not term:
        return False
    if len(term) == 2:
        if term[-2] in vowels and term[-1] not in vowels:
            return True
    elif len(term) >= 3:
        if ((term[-3] not in vowels and term[-2] in vowels and
             term[-1] in codanonvowels)):
            return True
    return False


def _sb_short_word(term, vowels, codanonvowels, r1_prefixes=None):
    """Return True iff term is a short word,
    according to the Porter2 specification
    """
    if ((_sb_r1(term, vowels, r1_prefixes) == len(term) and
         _sb_ends_in_short_syllable(term, vowels, codanonvowels))):
        return True
    return False


def porter2(word, early_english=False):
    """Implementation of Porter2 (Snowball English) stemmer -- ideally returns
    the word stem

    Arguments:
    word -- the word to calculate the stem of
    early_english -- set to True in order to remove -eth & -est (2nd & 3rd
        person singular verbal agreement suffixes)

    Description:
    The Porter2/Snowball English stemmer is defined at
    http://snowball.tartarus.org/algorithms/english/stemmer.html
    """
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-return-statements

    _vowels = frozenset('aeiouy')
    _codanonvowels = frozenset('bcdfghjklmnpqrstvz\'')
    _doubles = frozenset(['bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr',
                          'tt'])
    _li = frozenset('cdeghkmnrt')

    # R1 prefixes should be in order from longest to shortest to prevent
    # masking
    _r1_prefixes = ('commun', 'gener', 'arsen')
    _exception1dict = {  # special changes:
                       'skis': 'ski', 'skies': 'sky', 'dying': 'die',
                       'lying': 'lie', 'tying': 'tie',
                       # special -LY cases:
                       'idly': 'idl', 'gently': 'gentl', 'ugly': 'ugli',
                       'early': 'earli', 'only': 'onli', 'singly': 'singl'}
    _exception1set = frozenset(['sky', 'news', 'howe', 'atlas', 'cosmos',
                                'bias', 'andes'])
    _exception2set = frozenset(['inning', 'outing', 'canning', 'herring',
                                'earring', 'proceed', 'exceed', 'succeed'])

    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))
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
    for i in _range(1, len(word)):
        if word[i] == 'y' and word[i-1] in _vowels:
            word = word[:i] + 'Y' + word[i+1:]

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
    elif word[-3:] in frozenset(['ied', 'ies']):
        if len(word) > 4:
            word = word[:-2]
        else:
            word = word[:-1]
    elif word[-2:] in frozenset(['us', 'ss']):
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
        if word[-2:] in frozenset(['at', 'bl', 'iz']):
            word += 'e'
        elif word[-2:] in _doubles:
            word = word[:-1]
        elif _sb_short_word(word, _vowels, _codanonvowels, _r1_prefixes):
            word += 'e'

    # Step 1c
    if ((len(word) > 2 and word[-1] in frozenset('Yy') and
         word[-2] not in _vowels)):
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
        if word[-4:] in frozenset(['enci', 'anci']):
            if len(word[r1_start:]) >= 4:
                word = word[:-1] + 'e'
    elif word[-2] == 'e':
        if word[-4:] == 'izer':
            if len(word[r1_start:]) >= 4:
                word = word[:-1]
    elif word[-2] == 'g':
        if word[-3:] == 'ogi':
            if ((r1_start >= 1 and len(word[r1_start:]) >= 3 and
                 word[-4] == 'l')):
                word = word[:-1]
    elif word[-2] == 'l':
        if word[-6:] == 'lessli':
            if len(word[r1_start:]) >= 6:
                word = word[:-2]
        elif word[-5:] in frozenset(['entli', 'fulli', 'ousli']):
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
            if ((r1_start >= 1 and len(word[r1_start:]) >= 2 and
                 word[-3] in _li)):
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
        if word[-7:] in frozenset(['fulness', 'ousness', 'iveness']):
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
    elif word[-5:] in frozenset(['alize', 'icate', 'iciti']):
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
    for suffix in ('ement', 'ance', 'ence', 'able', 'ible', 'ment', 'ant',
                   'ent', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize', 'al', 'er',
                   'ic'):
        if word[-len(suffix):] == suffix:
            if len(word[r2_start:]) >= len(suffix):
                word = word[:-len(suffix)]
            break
    else:
        if word[-3:] == 'ion':
            if ((len(word[r2_start:]) >= 3 and len(word) >= 4 and
                 word[-4] in tuple('st'))):
                word = word[:-3]

    # Step 5
    if word[-1] == 'e':
        if (len(word[r2_start:]) >= 1 or
            (len(word[r1_start:]) >= 1 and
             not _sb_ends_in_short_syllable(word[:-1], _vowels,
                                            _codanonvowels))):
            word = word[:-1]
    elif word[-1] == 'l':
        if len(word[r2_start:]) >= 1 and word[-2] == 'l':
            word = word[:-1]

    # Change 'Y' back to 'y' if it survived stemming
    for i in _range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]

    return word


def sb_german(word, alternate_vowels=False):
    """Implementation of Snowball German stemmer -- ideally returns the word
    stem

    Arguments:
    word -- the word to calculate the stem of
    alternate_vowels -- composes ae as ä, oe as ö, and ue as ü before running
        the algorithm

    Description:
    The Snowball German stemmer is defined at
    http://snowball.tartarus.org/algorithms/german/stemmer.html
    """
    # pylint: disable=too-many-branches

    _vowels = frozenset('aeiouyäöü')
    _s_endings = frozenset('bdfghklmnrt')
    _st_endings = frozenset('bdfghklmnt')

    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', word.lower())
    word = word.replace('ß', 'ss')

    if len(word) > 2:
        for i in _range(2, len(word)):
            if word[i] in _vowels and word[i-2] in _vowels:
                if word[i-1] == 'u':
                    word = word[:i-1] + 'U' + word[i:]
                elif word[i-1] == 'y':
                    word = word[:i-1] + 'Y' + word[i:]

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
        if ((len(word[r1_start:]) >= 1 and len(word) >= 2 and
             word[-2] in _s_endings)):
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
        if ((len(word[r1_start:]) >= 2 and len(word) >= 6 and
             word[-3] in _st_endings)):
            word = word[:-2]

    # Step 3
    if word[-4:] == 'isch':
        if len(word[r2_start:]) >= 4 and word[-5] != 'e':
            word = word[:-4]
    elif word[-4:] in frozenset(['lich', 'heit']):
        if len(word[r2_start:]) >= 4:
            word = word[:-4]
            if ((word[-2:] in frozenset(['er', 'en']) and
                 len(word[r1_start:]) >= 2)):
                word = word[:-2]
    elif word[-4:] == 'keit':
        if len(word[r2_start:]) >= 4:
            word = word[:-4]
            if word[-4:] == 'lich' and len(word[r2_start:]) >= 4:
                word = word[:-4]
            elif word[-2:] == 'ig' and len(word[r2_start:]) >= 2:
                word = word[:-2]
    elif word[-3:] in frozenset(['end', 'ung']):
        if len(word[r2_start:]) >= 3:
            word = word[:-3]
            if ((word[-2:] == 'ig' and len(word[r2_start:]) >= 2 and
                 word[-3] != 'e')):
                word = word[:-2]
    elif word[-2:] in frozenset(['ig', 'ik']):
        if len(word[r2_start:]) >= 2 and word[-3] != 'e':
            word = word[:-2]

    # Change 'Y' and 'U' back to lowercase if survived stemming
    for i in _range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]
        elif word[i] == 'U':
            word = word[:i] + 'u' + word[i+1:]

    # Remove umlauts
    _umlauts = dict(zip([ord(_) for _ in 'äöü'], 'aou'))
    word = word.translate(_umlauts)

    return word


def sb_dutch(word):
    """Implementation of Snowball Dutch stemmer -- ideally returns the word
    stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The Snowball Dutch stemmer is defined at
    http://snowball.tartarus.org/algorithms/dutch/stemmer.html
    """
    # pylint: disable=too-many-branches

    _vowels = frozenset('aeiouyè')
    _not_s_endings = frozenset('aeiouyèj')

    def _undouble(word):
        """Undouble endings -kk, -dd, and -tt
        """
        if ((len(word) > 1 and word[-1] == word[-2] and
             word[-1] in frozenset('kdt'))):
            return word[:-1]
        return word

    # lowercase, normalize, decompose, filter umlauts & acutes out, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))
    _accented = dict(zip([ord(_) for _ in 'äëïöüáéíóú'], 'aeiouaeiou'))
    word = word.translate(_accented)

    for i in _range(len(word)):
        if i == 0 and word[0] == 'y':
            word = 'Y' + word[1:]
        elif word[i] == 'y' and word[i-1] in _vowels:
            word = word[:i] + 'Y' + word[i+1:]
        elif (word[i] == 'i' and word[i-1] in _vowels and i+1 < len(word) and
              word[i+1] in _vowels):
            word = word[:i] + 'I' + word[i+1:]

    r1_start = max(3, _sb_r1(word, _vowels))
    r2_start = _sb_r2(word, _vowels)

    # Step 1
    if word[-5:] == 'heden':
        if len(word[r1_start:]) >= 5:
            word = word[:-3] + 'id'
    elif word[-3:] == 'ene':
        if ((len(word[r1_start:]) >= 3 and
             (word[-4] not in _vowels and word[-6:-3] != 'gem'))):
            word = _undouble(word[:-3])
    elif word[-2:] == 'en':
        if ((len(word[r1_start:]) >= 2 and
             (word[-3] not in _vowels and word[-5:-2] != 'gem'))):
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
                if ((len(word[r1_start:]) >= 2 and
                     (word[-3] not in _vowels and word[-5:-2] != 'gem'))):
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
            if ((word[-2:] == 'ig' and len(word[r2_start:]) >= 2 and
                 word[-3] != 'e')):
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
    if ((len(word) >= 4 and
         word[-3] == word[-2] and word[-2] in frozenset('aeou') and
         word[-4] not in _vowels and
         word[-1] not in _vowels and word[-1] != 'I')):
        word = word[:-2] + word[-1]

    # Change 'Y' and 'U' back to lowercase if survived stemming
    for i in _range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]
        elif word[i] == 'I':
            word = word[:i] + 'i' + word[i+1:]

    return word


def sb_norwegian(word):
    """Implementation of Snowball Norwegian stemmer -- ideally returns the word
    stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The Snowball Norwegian stemmer is defined at
    http://snowball.tartarus.org/algorithms/norwegian/stemmer.html
    """
    _vowels = frozenset('aeiouyæåø')
    _s_endings = frozenset('bcdfghjlmnoprtvyz')

    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))

    r1_start = min(max(3, _sb_r1(word, _vowels)), len(word))

    # Step 1
    _r1 = word[r1_start:]
    if _r1[-7:] == 'hetenes':
        word = word[:-7]
    elif _r1[-6:] in frozenset(['hetene', 'hetens']):
        word = word[:-6]
    elif _r1[-5:] in frozenset(['heten', 'heter', 'endes']):
        word = word[:-5]
    elif _r1[-4:] in frozenset(['ande', 'ende', 'edes', 'enes', 'erte']):
        if word[-4:] == 'erte':
            word = word[:-2]
        else:
            word = word[:-4]
    elif _r1[-3:] in frozenset(['ede', 'ane', 'ene', 'ens', 'ers', 'ets',
                                'het', 'ast', 'ert']):
        if word[-3:] == 'ert':
            word = word[:-1]
        else:
            word = word[:-3]
    elif _r1[-2:] in frozenset(['en', 'ar', 'er', 'as', 'es', 'et']):
        word = word[:-2]
    elif _r1[-1:] in frozenset('ae'):
        word = word[:-1]
    elif _r1[-1:] == 's':
        if (((len(word) > 1 and word[-2] in _s_endings) or
             (len(word) > 2 and word[-2] == 'k' and word[-3] not in _vowels))):
            word = word[:-1]

    # Step 2
    if word[r1_start:][-2:] in frozenset(['dt', 'vt']):
        word = word[:-1]

    # Step 3
    _r1 = word[r1_start:]
    if _r1[-7:] == 'hetslov':
        word = word[:-7]
    elif _r1[-4:] in frozenset(['eleg', 'elig', 'elov', 'slov']):
        word = word[:-4]
    elif _r1[-3:] in frozenset(['leg', 'eig', 'lig', 'els', 'lov']):
        word = word[:-3]
    elif _r1[-2:] == 'ig':
        word = word[:-2]

    return word


def sb_swedish(word):
    """Implementation of Snowball Swedish stemmer -- ideally returns the word
    stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The Snowball Swedish stemmer is defined at
    http://snowball.tartarus.org/algorithms/swedish/stemmer.html
    """
    _vowels = frozenset('aeiouyäåö')
    _s_endings = frozenset('bcdfghjklmnoprtvy')

    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))

    r1_start = min(max(3, _sb_r1(word, _vowels)), len(word))

    # Step 1
    _r1 = word[r1_start:]
    if _r1[-7:] == 'heterna':
        word = word[:-7]
    elif _r1[-6:] == 'hetens':
        word = word[:-6]
    elif _r1[-5:] in frozenset(['anden', 'heten', 'heter', 'arnas', 'ernas',
                                'ornas', 'andes', 'arens', 'andet']):
        word = word[:-5]
    elif _r1[-4:] in frozenset(['arna', 'erna', 'orna', 'ande', 'arne', 'aste',
                                'aren', 'ades', 'erns']):
        word = word[:-4]
    elif _r1[-3:] in frozenset(['ade', 'are', 'ern', 'ens', 'het', 'ast']):
        word = word[:-3]
    elif _r1[-2:] in frozenset(['ad', 'en', 'ar', 'er', 'or', 'as', 'es',
                                'at']):
        word = word[:-2]
    elif _r1[-1:] in frozenset('ae'):
        word = word[:-1]
    elif _r1[-1:] == 's':
        if len(word) > 1 and word[-2] in _s_endings:
            word = word[:-1]

    # Step 2
    if word[r1_start:][-2:] in frozenset(['dd', 'gd', 'nn', 'dt', 'gt', 'kt',
                                          'tt']):
        word = word[:-1]

    # Step 3
    _r1 = word[r1_start:]
    if _r1[-5:] == 'fullt':
        word = word[:-1]
    elif _r1[-4:] == 'löst':
        word = word[:-1]
    elif _r1[-3:] in frozenset(['lig', 'els']):
        word = word[:-3]
    elif _r1[-2:] == 'ig':
        word = word[:-2]

    return word


def sb_danish(word):
    """Implementation of Snowball Danish stemmer -- ideally returns the word
    stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The Snowball Danish stemmer is defined at
    http://snowball.tartarus.org/algorithms/danish/stemmer.html
    """
    _vowels = frozenset('aeiouyæåø')
    _s_endings = frozenset('abcdfghjklmnoprtvyzå')

    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))

    r1_start = min(max(3, _sb_r1(word, _vowels)), len(word))

    # Step 1
    _r1 = word[r1_start:]
    if _r1[-7:] == 'erendes':
        word = word[:-7]
    elif _r1[-6:] in frozenset(['erende', 'hedens']):
        word = word[:-6]
    elif _r1[-5:] in frozenset(['ethed', 'erede', 'heden', 'heder', 'endes',
                                'ernes', 'erens', 'erets']):
        word = word[:-5]
    elif _r1[-4:] in frozenset(['ered', 'ende', 'erne', 'eren', 'erer', 'heds',
                                'enes', 'eres', 'eret']):
        word = word[:-4]
    elif _r1[-3:] in frozenset(['hed', 'ene', 'ere', 'ens', 'ers', 'ets']):
        word = word[:-3]
    elif _r1[-2:] in frozenset(['en', 'er', 'es', 'et']):
        word = word[:-2]
    elif _r1[-1:] == 'e':
        word = word[:-1]
    elif _r1[-1:] == 's':
        if len(word) > 1 and word[-2] in _s_endings:
            word = word[:-1]

    # Step 2
    if word[r1_start:][-2:] in frozenset(['gd', 'dt', 'gt', 'kt']):
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
    elif _r1[-3:] in frozenset(['lig', 'els']):
        word = word[:-3]
        repeat_step2 = True
    elif _r1[-2:] == 'ig':
        word = word[:-2]
        repeat_step2 = True

    if repeat_step2:
        if word[r1_start:][-2:] in frozenset(['gd', 'dt', 'gt', 'kt']):
            word = word[:-1]

    # Step 4
    if ((len(word[r1_start:]) >= 1 and len(word) >= 2 and
         word[-1] == word[-2] and word[-1] not in _vowels)):
        word = word[:-1]

    return word


def clef_german(word):
    """Implementation of CLEF German stemmer -- ideally returns the word
    stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The CLEF German stemmer is defined at
    http://members.unine.ch/jacques.savoy/clef/germanStemmer.txt
    """
    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))

    # remove umlauts
    _umlauts = dict(zip([ord(_) for _ in 'äöü'], 'aou'))
    word = word.translate(_umlauts)

    # remove plurals
    wlen = len(word)-1

    if wlen > 3:
        if wlen > 5:
            if word[-3:] == 'nen':
                return word[:-3]
        if wlen > 4:
            if word[-2:] in frozenset(['en', 'se', 'es', 'er']):
                return word[:-2]
        if word[-1] in frozenset('nsre'):
            return word[:-1]
    return word


def clef_german_plus(word):
    """Implementation of CLEF German stemmer plus -- ideally returns the word
    stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The CLEF German stemmer plus is defined at
    http://members.unine.ch/jacques.savoy/clef/germanStemmerPlus.txt
    """
    _st_ending = frozenset('bdfghklmnt')

    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))

    # remove umlauts
    _accents = dict(zip([ord(_) for _ in 'äàáâöòóôïìíîüùúû'],
                        'aaaaooooiiiiuuuu'))
    word = word.translate(_accents)

    # Step 1
    wlen = len(word)-1
    if wlen > 4 and word[-3:] == 'ern':
        word = word[:-3]
    elif wlen > 3 and word[-2:] in frozenset(['em', 'en', 'er', 'es']):
        word = word[:-2]
    elif wlen > 2 and (word[-1] == 'e' or
                       (word[-1] == 's' and word[-2] in _st_ending)):
        word = word[:-1]

    # Step 2
    wlen = len(word)-1
    if wlen > 4 and word[-3:] == 'est':
        word = word[:-3]
    elif wlen > 3 and (word[-2:] in frozenset(['er', 'en']) or
                       (word[-2:] == 'st' and word[-3] in _st_ending)):
        word = word[:-2]

    return word


def clef_swedish(word):
    """Implementation of CLEF Swedish stemmer -- ideally returns the word
    stem

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The CLEF Swedish stemmer is defined at
    http://members.unine.ch/jacques.savoy/clef/swedishStemmer.txt
    """
    wlen = len(word)-1

    if wlen > 3 and word[-1] == 's':
        word = word[:-1]
        wlen -= 1

    if wlen > 6:
        if word[-5:] in frozenset(['elser', 'heten']):
            return word[:-5]
    if wlen > 5:
        if word[-4:] in frozenset(['arne', 'erna', 'ande', 'else', 'aste',
                                   'orna', 'aren']):
            return word[:-4]
    if wlen > 4:
        if word[-3:] in frozenset(['are', 'ast', 'het']):
            return word[:-3]
    if wlen > 3:
        if word[-2:] in frozenset(['ar', 'er', 'or', 'en', 'at', 'te', 'et']):
            return word[:-2]
    if wlen > 2:
        if word[-1] in frozenset('taen'):
            return word[:-1]
    return word


def uealite(word):
    """Implementation of the UEA-Lite stemmer

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The UEA-Lite stemmer is defined in Marie-Claire Jenkins and Dan Smith's
    article at
    http://wayback.archive.org/web/20121012154211/http://www.uea.ac.uk/polopoly_fs/1.85493!stemmer25feb.pdf
    """
    return word


def lancaster(word):
    """Implementation of the Lancaster Stemming Algorithm, developed by
    Chris Paice, with the assistance of Gareth Husk

    Arguments:
    word -- the word to calculate the stem of

    Description:
    The Lancaster Stemming Algorithm, described at:
    http://wayback.archive.org/web/20140724170659/http://www.comp.lancs.ac.uk/computing/research/stemming/Links/paice.htm
    """
    _lancaster_rules = ('ai*2.', 'a*1.', 'bb1.', 'city3s.', 'ci2>', 'cn1t>',
                        'dd1.', 'dei3y>', 'deec2ss.', 'dee1.', 'de2>',
                        'dooh4>', 'e1>', 'feil1v.', 'fi2>', 'gni3>', 'gai3y.',
                        'ga2>', 'gg1.', 'ht*2.', 'hsiug5ct.', 'hsi3>', 'i*1.',
                        'i1y>', 'ji1d.', 'juf1s.', 'ju1d.', 'jo1d.', 'jeh1r.',
                        'jrev1t.', 'jsim2t.', 'jn1d.', 'j1s.', 'lbaifi6.',
                        'lbai4y.', 'lba3>', 'lbi3.', 'lib2l>', 'lc1.',
                        'lufi4y.', 'luf3>', 'lu2.', 'lai3>', 'lau3>', 'la2>',
                        'll1.', 'mui3.', 'mu*2.', 'msi3>', 'mm1.', 'nois4j>',
                        'noix4ct.', 'noi3>', 'nai3>', 'na2>', 'nee0.', 'ne2>',
                        'nn1.', 'pihs4>', 'pp1.', 're2>', 'rae0.', 'ra2.',
                        'ro2>', 'ru2>', 'rr1.', 'rt1>', 'rei3y>', 'sei3y>',
                        'sis2.', 'si2>', 'ssen4>', 'ss0.', 'suo3>', 'su*2.',
                        's*1>', 's0.', 'tacilp4y.', 'ta2>', 'tnem4>', 'tne3>',
                        'tna3>', 'tpir2b.', 'tpro2b.', 'tcud1.', 'tpmus2.',
                        'tpec2iv.', 'tulo2v.', 'tsis0.', 'tsi3>', 'tt1.',
                        'uqi3.', 'ugo1.', 'vis3j>', 'vie0.', 'vi2>', 'ylb1>',
                        'yli3y>', 'ylp0.', 'yl2>', 'ygo1.', 'yhp1.', 'ymo1.',
                        'ypo1.', 'yti3>', 'yte3>', 'ytl2.', 'yrtsi5.',
                        'yra3>', 'yro3>', 'yfi3.', 'ycn2t>', 'yca3>', 'zi2>',
                        'zy1s.')

    return word


def caumanns(word):
    """Implementation of the Jörg Caumanns' German stemmer

    Arguments:
    word -- the word to calculate the stem of

    Description:
    Caumanns' stemmer is described in his article at
    http://edocs.fu-berlin.de/docs/servlets/MCRFileNodeServlet/FUDOCS_derivate_000000000350/tr-b-99-16.pdf
    This implementation is based on the GermanStemFilter described at
    http://www.evelix.ch/unternehmen/Blog/evelix/2013/11/11/inner-workings-of-the-german-analyzer-in-lucene
    """
    if not len(word):
        return ''

    upper_initial = word[0].isupper()
    word = unicodedata.normalize('NFC', _unicode(word.lower()))

    # # Part 2: Substitution
    # 1. Change umlauts to corresponding vowels & ß to ss
    _umlauts = dict(zip([ord(_) for _ in 'äöü'], 'aou'))
    word = word.translate(_umlauts)
    word = word.replace('ß', 'ss')

    # 2. Change second of doubled characters to *
    newword = word[0]
    for i in _range(1, len(word)):
        if newword[i-1] == word[i]:
            newword += '*'
        else:
            newword += word[i]
    word = newword

    # 3. Replace sch, ch, ei, ie with $, §, %, &
    word = word.replace('sch', '$')
    word = word.replace('ch', '§')
    word = word.replace('ei', '%')
    word = word.replace('ie', '&')
    word = word.replace('ig', '#')
    word = word.replace('st', '!')

    # # Part 1: Recursive Context-Free Stripping
    # 1. Remove the following 7 suffixes recursively
    while len(word) > 3:
        if (((len(word) > 4 and word[-2:] in frozenset(['em', 'er'])) or
             (len(word) > 5 and word[-2:] == 'nd'))):
            word = word[:-2]
        elif ((word[-1] in {'e', 's', 'n'}) or
              (not upper_initial and word[-1] in {'t', '!'})):
            word = word[:-1]
        else:
            break

    # Additional optimizations:
    if len(word) > 5 and word[-5:] == 'erin*':
        word = word[:-1]
    if word[-1] == 'z':
        word = word[:-1] + 'x'

    # Reverse substitutions:
    word = word.replace('$', 'sch')
    word = word.replace('§', 'ch')
    word = word.replace('%', 'ei')
    word = word.replace('&', 'ie')
    word = word.replace('#', 'ig')
    word = word.replace('!', 'st')

    # Expand doubled
    word = ''.join([word[0]] + [word[i-1] if word[i] == '*' else word[i] for
                                i in _range(1, len(word))])

    # Finally, convert gege to ge
    if len(word) > 4:
        word = word.replace('gege', 'ge', 1)

    return word
