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

"""abydos.stemmer.

The stemmer module defines word stemmers including:

    - the Lovins stemmer
    - the Porter and Porter2 (Snowball English) stemmers
    - Snowball stemmers for German, Dutch, Norwegian, Swedish, and Danish
    - CLEF German, German plus, and Swedish stemmers
    - Caumanns German stemmer
    - UEA-Lite Stemmer
    - Paice-Husk Stemmer
    - Schinke Latin stemmer
    - S stemmer
"""

from __future__ import unicode_literals

from re import match as re_match
from unicodedata import normalize

from six import text_type
from six.moves import range

__all__ = ['caumanns', 'clef_german', 'clef_german_plus', 'clef_swedish',
           'lovins', 'paice_husk', 'porter', 'porter2', 's_stemmer',
           'sb_danish', 'sb_dutch', 'sb_german', 'sb_norwegian', 'sb_swedish',
           'schinke', 'uealite']


def lovins(word):
    """Return Lovins stem.

    Lovins stemmer

    The Lovins stemmer is described in Julie Beth Lovins's article
    :cite:`Lovins:1968`.

    :param str word: the word to stem
    :returns: word stem
    :rtype: str

    >>> lovins('reading')
    'read'
    >>> lovins('suspension')
    'suspens'
    >>> lovins('elusiveness')
    'elus'
    """
    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    def cond_b(word, suffix_len):
        """Return Lovins' condition B.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word)-suffix_len >= 3

    def cond_c(word, suffix_len):
        """Return Lovins' condition C.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word)-suffix_len >= 4

    def cond_d(word, suffix_len):
        """Return Lovins' condition D.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word)-suffix_len >= 5

    def cond_e(word, suffix_len):
        """Return Lovins' condition E.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] != 'e'

    def cond_f(word, suffix_len):
        """Return Lovins' condition F.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (len(word)-suffix_len >= 3 and
                word[-suffix_len-1] != 'e')

    def cond_g(word, suffix_len):
        """Return Lovins' condition G.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (len(word)-suffix_len >= 3 and
                word[-suffix_len-1] == 'f')

    def cond_h(word, suffix_len):
        """Return Lovins' condition H.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (word[-suffix_len-1] == 't' or
                word[-suffix_len-2:-suffix_len] == 'll')

    def cond_i(word, suffix_len):
        """Return Lovins' condition I.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] not in {'e', 'o'}

    def cond_j(word, suffix_len):
        """Return Lovins' condition J.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] not in {'a', 'e'}

    def cond_k(word, suffix_len):
        """Return Lovins' condition K.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (len(word)-suffix_len >= 3 and
                (word[-suffix_len-1] in {'i', 'l'} or
                 (word[-suffix_len-3] == 'u' and word[-suffix_len-1] == 'e')))

    def cond_l(word, suffix_len):
        """Return Lovins' condition L.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (word[-suffix_len-1] not in {'s', 'u', 'x'} or
                word[-suffix_len-1] == 'os')

    def cond_m(word, suffix_len):
        """Return Lovins' condition M.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] not in {'a', 'c', 'e', 'm'}

    def cond_n(word, suffix_len):
        """Return Lovins' condition N.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        if len(word)-suffix_len >= 3:
            if word[-suffix_len-3] == 's':
                if len(word)-suffix_len >= 4:
                    return True
            else:
                return True
        return False

    def cond_o(word, suffix_len):
        """Return Lovins' condition O.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] in {'i', 'l'}

    def cond_p(word, suffix_len):
        """Return Lovins' condition P.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] != 'c'

    def cond_q(word, suffix_len):
        """Return Lovins' condition Q.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (len(word)-suffix_len >= 3 and
                word[-suffix_len-1] not in {'l', 'n'})

    def cond_r(word, suffix_len):
        """Return Lovins' condition R.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] in {'n', 'r'}

    def cond_s(word, suffix_len):
        """Return Lovins' condition S.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (word[-suffix_len-2:-suffix_len] == 'dr' or
                (word[-suffix_len-1] == 't' and
                 word[-suffix_len-2:-suffix_len] != 'tt'))

    def cond_t(word, suffix_len):
        """Return Lovins' condition T.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (word[-suffix_len-1] in {'s', 't'} and
                word[-suffix_len-2:-suffix_len] != 'ot')

    def cond_u(word, suffix_len):
        """Return Lovins' condition U.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] in {'l', 'm', 'n', 'r'}

    def cond_v(word, suffix_len):
        """Return Lovins' condition V.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] == 'c'

    def cond_w(word, suffix_len):
        """Return Lovins' condition W.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] not in {'s', 'u'}

    def cond_x(word, suffix_len):
        """Return Lovins' condition X.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (word[-suffix_len-1] in {'i', 'l'} or
                (word[-suffix_len-3:-suffix_len] == 'u' and
                 word[-suffix_len-1] == 'e'))

    def cond_y(word, suffix_len):
        """Return Lovins' condition Y.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-2:-suffix_len] == 'in'

    def cond_z(word, suffix_len):
        """Return Lovins' condition Z.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] != 'f'

    def cond_aa(word, suffix_len):
        """Return Lovins' condition AA.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (word[-suffix_len-1] in {'d', 'f', 'l', 't'} or
                word[-suffix_len-2:-suffix_len] in {'ph', 'th', 'er', 'or',
                                                    'es'})

    def cond_bb(word, suffix_len):
        """Return Lovins' condition BB.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (len(word)-suffix_len >= 3 and
                word[-suffix_len-3:-suffix_len] != 'met' and
                word[-suffix_len-4:-suffix_len] != 'ryst')

    def cond_cc(word, suffix_len):
        """Return Lovins' condition CC.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len-1] == 'l'

    suffix = {'alistically': cond_b, 'arizability': None,
              'izationally': cond_b, 'antialness': None,
              'arisations': None, 'arizations': None, 'entialness': None,
              'allically': cond_c, 'antaneous': None, 'antiality': None,
              'arisation': None, 'arization': None, 'ationally': cond_b,
              'ativeness': None, 'eableness': cond_e, 'entations': None,
              'entiality': None, 'entialize': None, 'entiation': None,
              'ionalness': None, 'istically': None, 'itousness': None,
              'izability': None, 'izational': None, 'ableness': None,
              'arizable': None, 'entation': None, 'entially': None,
              'eousness': None, 'ibleness': None, 'icalness': None,
              'ionalism': None, 'ionality': None, 'ionalize': None,
              'iousness': None, 'izations': None, 'lessness': None,
              'ability': None, 'aically': None, 'alistic': cond_b,
              'alities': None, 'ariness': cond_e, 'aristic': None,
              'arizing': None, 'ateness': None, 'atingly': None,
              'ational': cond_b, 'atively': None, 'ativism': None,
              'elihood': cond_e, 'encible': None, 'entally': None,
              'entials': None, 'entiate': None, 'entness': None,
              'fulness': None, 'ibility': None, 'icalism': None,
              'icalist': None, 'icality': None, 'icalize': None,
              'ication': cond_g, 'icianry': None, 'ination': None,
              'ingness': None, 'ionally': None, 'isation': None,
              'ishness': None, 'istical': None, 'iteness': None,
              'iveness': None, 'ivistic': None, 'ivities': None,
              'ization': cond_f, 'izement': None, 'oidally': None,
              'ousness': None, 'aceous': None, 'acious': cond_b,
              'action': cond_g, 'alness': None, 'ancial': None,
              'ancies': None, 'ancing': cond_b, 'ariser': None,
              'arized': None, 'arizer': None, 'atable': None,
              'ations': cond_b, 'atives': None, 'eature': cond_z,
              'efully': None, 'encies': None, 'encing': None,
              'ential': None, 'enting': cond_c, 'entist': None,
              'eously': None, 'ialist': None, 'iality': None,
              'ialize': None, 'ically': None, 'icance': None,
              'icians': None, 'icists': None, 'ifully': None,
              'ionals': None, 'ionate': cond_d, 'ioning': None,
              'ionist': None, 'iously': None, 'istics': None,
              'izable': cond_e, 'lessly': None, 'nesses': None,
              'oidism': None, 'acies': None, 'acity': None,
              'aging': cond_b, 'aical': None, 'alist': None,
              'alism': cond_b, 'ality': None, 'alize': None,
              'allic': cond_bb, 'anced': cond_b, 'ances': cond_b,
              'antic': cond_c, 'arial': None, 'aries': None,
              'arily': None, 'arity': cond_b, 'arize': None,
              'aroid': None, 'ately': None, 'ating': cond_i,
              'ation': cond_b, 'ative': None, 'ators': None,
              'atory': None, 'ature': cond_e, 'early': cond_y,
              'ehood': None, 'eless': None, 'elity': None,
              'ement': None, 'enced': None, 'ences': None,
              'eness': cond_e, 'ening': cond_e, 'ental': None,
              'ented': cond_c, 'ently': None, 'fully': None,
              'ially': None, 'icant': None, 'ician': None,
              'icide': None, 'icism': None, 'icist': None,
              'icity': None, 'idine': cond_i, 'iedly': None,
              'ihood': None, 'inate': None, 'iness': None,
              'ingly': cond_b, 'inism': cond_j, 'inity': cond_cc,
              'ional': None, 'ioned': None, 'ished': None,
              'istic': None, 'ities': None, 'itous': None,
              'ively': None, 'ivity': None, 'izers': cond_f,
              'izing': cond_f, 'oidal': None, 'oides': None,
              'otide': None, 'ously': None, 'able': None, 'ably': None,
              'ages': cond_b, 'ally': cond_b, 'ance': cond_b, 'ancy': cond_b,
              'ants': cond_b, 'aric': None, 'arly': cond_k, 'ated': cond_i,
              'ates': None, 'atic': cond_b, 'ator': None, 'ealy': cond_y,
              'edly': cond_e, 'eful': None, 'eity': None, 'ence': None,
              'ency': None, 'ened': cond_e, 'enly': cond_e, 'eous': None,
              'hood': None, 'ials': None, 'ians': None, 'ible': None,
              'ibly': None, 'ical': None, 'ides': cond_l, 'iers': None,
              'iful': None, 'ines': cond_m, 'ings': cond_n, 'ions': cond_b,
              'ious': None, 'isms': cond_b, 'ists': None, 'itic': cond_h,
              'ized': cond_f, 'izer': cond_f, 'less': None, 'lily': None,
              'ness': None, 'ogen': None, 'ward': None, 'wise': None,
              'ying': cond_b, 'yish': None, 'acy': None, 'age': cond_b,
              'aic': None, 'als': cond_bb, 'ant': cond_b, 'ars': cond_o,
              'ary': cond_f, 'ata': None, 'ate': None, 'eal': cond_y,
              'ear': cond_y, 'ely': cond_e, 'ene': cond_e, 'ent': cond_c,
              'ery': cond_e, 'ese': None, 'ful': None, 'ial': None,
              'ian': None, 'ics': None, 'ide': cond_l, 'ied': None,
              'ier': None, 'ies': cond_p, 'ily': None, 'ine': cond_m,
              'ing': cond_n, 'ion': cond_q, 'ish': cond_c, 'ism': cond_b,
              'ist': None, 'ite': cond_aa, 'ity': None, 'ium': None,
              'ive': None, 'ize': cond_f, 'oid': None, 'one': cond_r,
              'ous': None, 'ae': None, 'al': cond_bb, 'ar': cond_x,
              'as': cond_b, 'ed': cond_e, 'en': cond_f, 'es': cond_e,
              'ia': None, 'ic': None, 'is': None, 'ly': cond_b,
              'on': cond_s, 'or': cond_t, 'um': cond_u, 'us': cond_v,
              'yl': cond_r, '\'s': None, 's\'': None, 'a': None,
              'e': None, 'i': None, 'o': None, 's': cond_w, 'y': cond_b}

    for suffix_len in range(11, 0, -1):
        ending = word[-suffix_len:]
        if (ending in suffix and
                len(word)-suffix_len >= 2 and
                (suffix[ending] is None or
                 suffix[ending](word, suffix_len))):
            word = word[:-suffix_len]
            break

    def recode9(stem):
        """Return Lovins' conditional recode rule 9."""
        if stem[-3:-2] in {'a', 'i', 'o'}:
            return stem
        return stem[:-2]+'l'

    def recode24(stem):
        """Return Lovins' conditional recode rule 24."""
        if stem[-4:-3] == 's':
            return stem
        return stem[:-1]+'s'

    def recode28(stem):
        """Return Lovins' conditional recode rule 28."""
        if stem[-4:-3] in {'p', 't'}:
            return stem
        return stem[:-1]+'s'

    def recode30(stem):
        """Return Lovins' conditional recode rule 30."""
        if stem[-4:-3] == 'm':
            return stem
        return stem[:-1]+'s'

    def recode32(stem):
        """Return Lovins' conditional recode rule 32."""
        if stem[-3:-2] == 'n':
            return stem
        return stem[:-1]+'s'

    if word[-2:] in {'bb', 'dd', 'gg', 'll', 'mm', 'nn', 'pp', 'rr', 'ss',
                     'tt'}:
        word = word[:-1]

    recode = (('iev', 'ief'),
              ('uct', 'uc'),
              ('umpt', 'um'),
              ('rpt', 'rb'),
              ('urs', 'ur'),
              ('istr', 'ister'),
              ('metr', 'meter'),
              ('olv', 'olut'),
              ('ul', recode9),
              ('bex', 'bic'),
              ('dex', 'dic'),
              ('pex', 'pic'),
              ('tex', 'tic'),
              ('ax', 'ac'),
              ('ex', 'ec'),
              ('ix', 'ic'),
              ('lux', 'luc'),
              ('uad', 'uas'),
              ('vad', 'vas'),
              ('cid', 'cis'),
              ('lid', 'lis'),
              ('erid', 'eris'),
              ('pand', 'pans'),
              ('end', recode24),
              ('ond', 'ons'),
              ('lud', 'lus'),
              ('rud', 'rus'),
              ('her', recode28),
              ('mit', 'mis'),
              ('ent', recode30),
              ('ert', 'ers'),
              ('et', recode32),
              ('yt', 'ys'),
              ('yz', 'ys'))

    for ending, replacement in recode:
        if word.endswith(ending):
            if callable(replacement):
                word = replacement(word)
            else:
                word = word[:-len(ending)] + replacement

    return word


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
    return (len(term) > 2 and (term[-1] not in vowels and
                               term[-2] in vowels and
                               term[-3] not in vowels and
                               term[-1] not in tuple('wxY')))


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
        if word[-2:] in {'at', 'bl', 'iz'}:
            word += 'e'
        elif (_ends_in_doubled_cons(word, _vowels) and
              word[-1] not in {'l', 's', 'z'}):
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
        elif (_m_degree(word[:-1], _vowels) == 1 and
              not _ends_in_cvc(word[:-1], _vowels)):
            word = word[:-1]

    # Step 5b
    if word[-2:] == 'll' and _m_degree(word, _vowels) > 1:
        word = word[:-1]

    # Change 'Y' back to 'y' if it survived stemming
    for i in range(len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]

    return word


def _sb_r1(term, vowels, r1_prefixes=None):
    """Return the R1 region, as defined in the Porter2 specification."""
    vowel_found = False
    if hasattr(r1_prefixes, '__iter__'):
        for prefix in r1_prefixes:
            if term[:len(prefix)] == prefix:
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
        if ((term[-3] not in vowels and term[-2] in vowels and
             term[-1] in codanonvowels)):
            return True
    return False


def _sb_short_word(term, vowels, codanonvowels, r1_prefixes=None):
    """Return True iff term is a short word.

    (...according to the Porter2 specification.)
    """
    if ((_sb_r1(term, vowels, r1_prefixes) == len(term) and
         _sb_ends_in_short_syllable(term, vowels, codanonvowels))):
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
    _codanonvowels = {"'", 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                      'n', 'p', 'q', 'r', 's', 't', 'v', 'z'}
    _doubles = {'bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt'}
    _li = {'c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't'}

    # R1 prefixes should be in order from longest to shortest to prevent
    # masking
    _r1_prefixes = ('commun', 'gener', 'arsen')
    _exception1dict = {  # special changes:
        'skis': 'ski', 'skies': 'sky', 'dying': 'die',
        'lying': 'lie', 'tying': 'tie',
        # special -LY cases:
        'idly': 'idl', 'gently': 'gentl', 'ugly': 'ugli',
        'early': 'earli', 'only': 'onli', 'singly': 'singl'}
    _exception1set = {'sky', 'news', 'howe', 'atlas', 'cosmos', 'bias',
                      'andes'}
    _exception2set = {'inning', 'outing', 'canning', 'herring', 'earring',
                      'proceed', 'exceed', 'succeed'}

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
    if ((len(word) > 2 and word[-1] in {'Y', 'y'} and
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
        if word[-4:] in {'enci', 'anci'}:
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
    for i in range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]

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
    elif word[-4:] in {'lich', 'heit'}:
        if len(word[r2_start:]) >= 4:
            word = word[:-4]
            if ((word[-2:] in {'er', 'en'} and
                 len(word[r1_start:]) >= 2)):
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
            if ((word[-2:] == 'ig' and len(word[r2_start:]) >= 2 and
                 word[-3] != 'e')):
                word = word[:-2]
    elif word[-2:] in {'ig', 'ik'}:
        if len(word[r2_start:]) >= 2 and word[-3] != 'e':
            word = word[:-2]

    # Change 'Y' and 'U' back to lowercase if survived stemming
    for i in range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]
        elif word[i] == 'U':
            word = word[:i] + 'u' + word[i+1:]

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
        if ((len(word) > 1 and word[-1] == word[-2] and
             word[-1] in {'d', 'k', 't'})):
            return word[:-1]
        return word

    # lowercase, normalize, decompose, filter umlauts & acutes out, and compose
    word = normalize('NFC', text_type(word.lower()))
    _accented = dict(zip((ord(_) for _ in 'äëïöüáéíóú'), 'aeiouaeiou'))
    word = word.translate(_accented)

    for i in range(len(word)):
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
         word[-3] == word[-2] and word[-2] in {'a', 'e', 'o', 'u'} and
         word[-4] not in _vowels and
         word[-1] not in _vowels and word[-1] != 'I')):
        word = word[:-2] + word[-1]

    # Change 'Y' and 'U' back to lowercase if survived stemming
    for i in range(0, len(word)):
        if word[i] == 'Y':
            word = word[:i] + 'y' + word[i+1:]
        elif word[i] == 'I':
            word = word[:i] + 'i' + word[i+1:]

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
    _s_endings = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 'n', 'o', 'p',
                  'r', 't', 'v', 'y', 'z'}
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
    elif _r1[-3:] in {'ede', 'ane', 'ene', 'ens', 'ers', 'ets', 'het', 'ast',
                      'ert'}:
        if word[-3:] == 'ert':
            word = word[:-1]
        else:
            word = word[:-3]
    elif _r1[-2:] in {'en', 'ar', 'er', 'as', 'es', 'et'}:
        word = word[:-2]
    elif _r1[-1:] in {'a', 'e'}:
        word = word[:-1]
    elif _r1[-1:] == 's':
        if (((len(word) > 1 and word[-2] in _s_endings) or
             (len(word) > 2 and word[-2] == 'k' and word[-3] not in _vowels))):
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
    _s_endings = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
                  'o', 'p', 'r', 't', 'v', 'y'}

    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    r1_start = min(max(3, _sb_r1(word, _vowels)), len(word))

    # Step 1
    _r1 = word[r1_start:]
    if _r1[-7:] == 'heterna':
        word = word[:-7]
    elif _r1[-6:] == 'hetens':
        word = word[:-6]
    elif _r1[-5:] in {'anden', 'heten', 'heter', 'arnas', 'ernas', 'ornas',
                      'andes', 'arens', 'andet'}:
        word = word[:-5]
    elif _r1[-4:] in {'arna', 'erna', 'orna', 'ande', 'arne', 'aste', 'aren',
                      'ades', 'erns'}:
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
    _s_endings = {'a', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
                  'o', 'p', 'r', 't', 'v', 'y', 'z', 'å'}

    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    r1_start = min(max(3, _sb_r1(word, _vowels)), len(word))

    # Step 1
    _r1 = word[r1_start:]
    if _r1[-7:] == 'erendes':
        word = word[:-7]
    elif _r1[-6:] in {'erende', 'hedens'}:
        word = word[:-6]
    elif _r1[-5:] in {'ethed', 'erede', 'heden', 'heder', 'endes', 'ernes',
                      'erens', 'erets'}:
        word = word[:-5]
    elif _r1[-4:] in {'ered', 'ende', 'erne', 'eren', 'erer', 'heds', 'enes',
                      'eres', 'eret'}:
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
    if ((len(word[r1_start:]) >= 1 and len(word) >= 2 and
         word[-1] == word[-2] and word[-1] not in _vowels)):
        word = word[:-1]

    return word


def clef_german(word):
    """Return CLEF German stem.

    The CLEF German stemmer is defined at :cite:`Savoy:2005`.

    :param str word: the word to calculate the stem of
    :returns: word stem
    :rtype: str

    >>> clef_german('lesen')
    'lese'
    >>> clef_german('graues')
    'grau'
    >>> clef_german('buchstabieren')
    'buchstabier'
    """
    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    # remove umlauts
    _umlauts = dict(zip((ord(_) for _ in 'äöü'), 'aou'))
    word = word.translate(_umlauts)

    # remove plurals
    wlen = len(word)-1

    if wlen > 3:
        if wlen > 5:
            if word[-3:] == 'nen':
                return word[:-3]
        if wlen > 4:
            if word[-2:] in {'en', 'se', 'es', 'er'}:
                return word[:-2]
        if word[-1] in {'e', 'n', 'r', 's'}:
            return word[:-1]
    return word


def clef_german_plus(word):
    """Return 'CLEF German stemmer plus' stem.

    The CLEF German stemmer plus is defined at :cite:`Savoy:2005`.

    :param str word: the word to calculate the stem of
    :returns: word stem
    :rtype: str

    >>> clef_german_plus('lesen')
    'les'
    >>> clef_german_plus('graues')
    'grau'
    >>> clef_german_plus('buchstabieren')
    'buchstabi'
    """
    _st_ending = {'b', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 't'}

    # lowercase, normalize, and compose
    word = normalize('NFC', text_type(word.lower()))

    # remove umlauts
    _accents = dict(zip((ord(_) for _ in 'äàáâöòóôïìíîüùúû'),
                        'aaaaooooiiiiuuuu'))
    word = word.translate(_accents)

    # Step 1
    wlen = len(word)-1
    if wlen > 4 and word[-3:] == 'ern':
        word = word[:-3]
    elif wlen > 3 and word[-2:] in {'em', 'en', 'er', 'es'}:
        word = word[:-2]
    elif wlen > 2 and (word[-1] == 'e' or
                       (word[-1] == 's' and word[-2] in _st_ending)):
        word = word[:-1]

    # Step 2
    wlen = len(word)-1
    if wlen > 4 and word[-3:] == 'est':
        word = word[:-3]
    elif wlen > 3 and (word[-2:] in {'er', 'en'} or
                       (word[-2:] == 'st' and word[-3] in _st_ending)):
        word = word[:-2]

    return word


def clef_swedish(word):
    """Return CLEF Swedish stem.

    The CLEF Swedish stemmer is defined at :cite:`Savoy:2005`.

    :param str word: the word to calculate the stem of
    :returns: word stem
    :rtype: str

    >>> clef_swedish('undervisa')
    'undervis'
    >>> clef_swedish('suspension')
    'suspensio'
    >>> clef_swedish('visshet')
    'viss'
    """
    wlen = len(word)-1

    if wlen > 3 and word[-1] == 's':
        word = word[:-1]
        wlen -= 1

    if wlen > 6:
        if word[-5:] in {'elser', 'heten'}:
            return word[:-5]
    if wlen > 5:
        if word[-4:] in {'arne', 'erna', 'ande', 'else', 'aste', 'orna',
                         'aren'}:
            return word[:-4]
    if wlen > 4:
        if word[-3:] in {'are', 'ast', 'het'}:
            return word[:-3]
    if wlen > 3:
        if word[-2:] in {'ar', 'er', 'or', 'en', 'at', 'te', 'et'}:
            return word[:-2]
    if wlen > 2:
        if word[-1] in {'a', 'e', 'n', 't'}:
            return word[:-1]
    return word


def caumanns(word):
    """Return Caumanns German stem.

    Jörg Caumanns' stemmer is described in his article in
    :cite:`Caumanns:1999`.

    This implementation is based on the GermanStemFilter described at
    :cite:`Lang:2013`.

    :param str word: the word to calculate the stem of
    :returns: word stem
    :rtype: str

    >>> caumanns('lesen')
    'les'
    >>> caumanns('graues')
    'grau'
    >>> caumanns('buchstabieren')
    'buchstabier'
    """
    if not word:
        return ''

    upper_initial = word[0].isupper()
    word = normalize('NFC', text_type(word.lower()))

    # # Part 2: Substitution
    # 1. Change umlauts to corresponding vowels & ß to ss
    _umlauts = dict(zip((ord(_) for _ in 'äöü'), 'aou'))
    word = word.translate(_umlauts)
    word = word.replace('ß', 'ss')

    # 2. Change second of doubled characters to *
    new_word = word[0]
    for i in range(1, len(word)):
        if new_word[i-1] == word[i]:
            new_word += '*'
        else:
            new_word += word[i]
    word = new_word

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
        if (((len(word) > 4 and word[-2:] in {'em', 'er'}) or
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
                                i in range(1, len(word))])

    # Finally, convert gege to ge
    if len(word) > 4:
        word = word.replace('gege', 'ge', 1)

    return word


def uealite(word, max_word_length=20, max_acro_length=8, return_rule_no=False,
            var=None):
    """Return UEA-Lite stem.

    The UEA-Lite stemmer is discussed in :cite:`Jenkins:2005`.

    This is chiefly based on the Java implementation of the algorithm, with
    variants based on the Perl implementation and Jason Adams' Ruby port.

    Java version: :cite:`Churchill:2005`
    Perl version: :cite:`Jenkins:2005`
    Ruby version: :cite:`Adams:2017`

    :param str word: the word to calculate the stem of
    :param int max_word_length: the maximum word length allowed
    :param int max_acro_length: the maximum acryonym length allowed
    :param bool return_rule_no: if True, returns the stem along with rule
        number
    :param str var: variant to use (set to 'Adams' to use Jason Adams' rules,
        or 'Perl' to use the original Perl set of rules)
    :returns: word stem
    :rtype: str or (str, int)

    >>> uealite('readings')
    'read'
    >>> uealite('insulted')
    'insult'
    >>> uealite('cussed')
    'cuss'
    >>> uealite('fancies')
    'fancy'
    >>> uealite('eroded')
    'erode'
    """
    problem_words = {'is', 'as', 'this', 'has', 'was', 'during'}

    # rule table format:
    # top-level dictionary: length-of-suffix: dict-of-rules
    # dict-of-rules: suffix: (rule_no, suffix_length_to_delete,
    #                         suffix_to_append)
    rule_table = {7: {'titudes': (30, 1, None),
                      'fulness': (34, 4, None),
                      'ousness': (35, 4, None),
                      'eadings': (40.7, 4, None),
                      'oadings': (40.6, 4, None),
                      'ealings': (42.4, 4, None),
                      'ailings': (42.2, 4, None),
                      },
                  6: {'aceous': (1, 6, None),
                      'aining': (24, 3, None),
                      'acting': (25, 3, None),
                      'ttings': (26, 5, None),
                      'viding': (27, 3, 'e'),
                      'ssings': (37, 4, None),
                      'ulting': (38, 3, None),
                      'eading': (40.7, 3, None),
                      'oading': (40.6, 3, None),
                      'edings': (40.5, 4, None),
                      'ddings': (40.4, 5, None),
                      'ldings': (40.3, 4, None),
                      'rdings': (40.2, 4, None),
                      'ndings': (40.1, 4, None),
                      'llings': (41, 5, None),
                      'ealing': (42.4, 3, None),
                      'olings': (42.3, 4, None),
                      'ailing': (42.2, 3, None),
                      'elings': (42.1, 4, None),
                      'mmings': (44.3, 5, None),
                      'ngings': (45.2, 4, None),
                      'ggings': (45.1, 5, None),
                      'stings': (47, 4, None),
                      'etings': (48.4, 4, None),
                      'ntings': (48.2, 4, None),
                      'irings': (54.4, 4, 'e'),
                      'urings': (54.3, 4, 'e'),
                      'ncings': (54.2, 4, 'e'),
                      'things': (58.1, 1, None),
                      },
                  5: {'iases': (11.4, 2, None),
                      'ained': (13.6, 2, None),
                      'erned': (13.5, 2, None),
                      'ifted': (14, 2, None),
                      'ected': (15, 2, None),
                      'vided': (16, 1, None),
                      'erred': (19, 3, None),
                      'urred': (20.5, 3, None),
                      'lored': (20.4, 2, None),
                      'eared': (20.3, 2, None),
                      'tored': (20.2, 1, None),
                      'noted': (22.4, 1, None),
                      'leted': (22.3, 1, None),
                      'anges': (23, 1, None),
                      'tting': (26, 4, None),
                      'ulted': (32, 2, None),
                      'uming': (33, 3, 'e'),
                      'rabed': (36.1, 1, None),
                      'rebed': (36.1, 1, None),
                      'ribed': (36.1, 1, None),
                      'robed': (36.1, 1, None),
                      'rubed': (36.1, 1, None),
                      'ssing': (37, 3, None),
                      'vings': (39, 4, 'e'),
                      'eding': (40.5, 3, None),
                      'dding': (40.4, 4, None),
                      'lding': (40.3, 3, None),
                      'rding': (40.2, 3, None),
                      'nding': (40.1, 3, None),
                      'dings': (40, 4, 'e'),
                      'lling': (41, 4, None),
                      'oling': (42.3, 3, None),
                      'eling': (42.1, 3, None),
                      'lings': (42, 4, 'e'),
                      'mming': (44.3, 4, None),
                      'rming': (44.2, 3, None),
                      'lming': (44.1, 3, None),
                      'mings': (44, 4, 'e'),
                      'nging': (45.2, 3, None),
                      'gging': (45.1, 4, None),
                      'gings': (45, 4, 'e'),
                      'aning': (46.6, 3, None),
                      'ening': (46.5, 3, None),
                      'gning': (46.4, 3, None),
                      'nning': (46.3, 4, None),
                      'oning': (46.2, 3, None),
                      'rning': (46.1, 3, None),
                      'sting': (47, 3, None),
                      'eting': (48.4, 3, None),
                      'pting': (48.3, 3, None),
                      'nting': (48.2, 3, None),
                      'cting': (48.1, 3, None),
                      'tings': (48, 4, 'e'),
                      'iring': (54.4, 3, 'e'),
                      'uring': (54.3, 3, 'e'),
                      'ncing': (54.2, 3, 'e'),
                      'sings': (54, 4, 'e'),
                      # 'lling': (55, 3, None),  # masked by 41
                      'ating': (57, 3, 'e'),
                      'thing': (58.1, 0, None),
                      },
                  4: {'eeds': (7, 1, None),
                      'uses': (11.3, 1, None),
                      'sses': (11.2, 2, None),
                      'eses': (11.1, 2, 'is'),
                      'tled': (12.5, 1, None),
                      'pled': (12.4, 1, None),
                      'bled': (12.3, 1, None),
                      'eled': (12.2, 2, None),
                      'lled': (12.1, 2, None),
                      'ened': (13.7, 2, None),
                      'rned': (13.4, 2, None),
                      'nned': (13.3, 3, None),
                      'oned': (13.2, 2, None),
                      'gned': (13.1, 2, None),
                      'ered': (20.1, 2, None),
                      'reds': (20, 2, None),
                      'tted': (21, 3, None),
                      'uted': (22.2, 1, None),
                      'ated': (22.1, 1, None),
                      'ssed': (28, 2, None),
                      'umed': (31, 1, None),
                      'beds': (36, 3, None),
                      'ving': (39, 3, 'e'),
                      'ding': (40, 3, 'e'),
                      'ling': (42, 3, 'e'),
                      'nged': (43.2, 1, None),
                      'gged': (43.1, 3, None),
                      'ming': (44, 3, 'e'),
                      'ging': (45, 3, 'e'),
                      'ning': (46, 3, 'e'),
                      'ting': (48, 3, 'e'),
                      # 'ssed': (49, 2, None),  # masked by 28
                      # 'lled': (53, 2, None),  # masked by 12.1
                      'zing': (54.1, 3, 'e'),
                      'sing': (54, 3, 'e'),
                      'lves': (60.1, 3, 'f'),
                      'aped': (61.3, 1, None),
                      'uded': (61.2, 1, None),
                      'oded': (61.1, 1, None),
                      # 'ated': (61, 1, None),  # masked by 22.1
                      'ones': (63.6, 1, None),
                      'izes': (63.5, 1, None),
                      'ures': (63.4, 1, None),
                      'ines': (63.3, 1, None),
                      'ides': (63.2, 1, None),
                      },
                  3: {'ces': (2, 1, None),
                      'sis': (4, 0, None),
                      'tis': (5, 0, None),
                      'eed': (7, 0, None),
                      'ued': (8, 1, None),
                      'ues': (9, 1, None),
                      'ees': (10, 1, None),
                      'ses': (11, 1, None),
                      'led': (12, 2, None),
                      'ned': (13, 1, None),
                      'ved': (17, 1, None),
                      'ced': (18, 1, None),
                      'red': (20, 1, None),
                      'ted': (22, 2, None),
                      'sed': (29, 1, None),
                      'bed': (36, 2, None),
                      'ged': (43, 1, None),
                      'les': (50, 1, None),
                      'tes': (51, 1, None),
                      'zed': (52, 1, None),
                      'ied': (56, 3, 'y'),
                      'ies': (59, 3, 'y'),
                      'ves': (60, 1, None),
                      'pes': (63.8, 1, None),
                      'mes': (63.7, 1, None),
                      'ges': (63.1, 1, None),
                      'ous': (65, 0, None),
                      'ums': (66, 0, None),
                      },
                  2: {'cs': (3, 0, None),
                      'ss': (6, 0, None),
                      'es': (63, 2, None),
                      'is': (64, 2, 'e'),
                      'us': (67, 0, None),
                      }}

    if var == 'Perl':
        perl_deletions = {7: ['eadings', 'oadings', 'ealings', 'ailings'],
                          6: ['ttings', 'ssings', 'edings', 'ddings',
                              'ldings', 'rdings', 'ndings', 'llings',
                              'olings', 'elings', 'mmings', 'ngings',
                              'ggings', 'stings', 'etings', 'ntings',
                              'irings', 'urings', 'ncings', 'things'],
                          5: ['vings', 'dings', 'lings', 'mings', 'gings',
                              'tings', 'sings'],
                          4: ['eeds', 'reds', 'beds']}

        # Delete the above rules from rule_table
        for del_len in perl_deletions:
            for term in perl_deletions[del_len]:
                del rule_table[del_len][term]

    elif var == 'Adams':
        adams_additions = {6: {'chited': (22.8, 1, None)},
                           5: {'dying': (58.2, 4, 'ie'),
                               'tying': (58.2, 4, 'ie'),
                               'vited': (22.6, 1, None),
                               'mited': (22.5, 1, None),
                               'vided': (22.9, 1, None),
                               'mided': (22.10, 1, None),
                               'lying': (58.2, 4, 'ie'),
                               'arred': (19.1, 3, None),
                               },
                           4: {'ited': (22.7, 2, None),
                               'oked': (31.1, 1, None),
                               'aked': (31.1, 1, None),
                               'iked': (31.1, 1, None),
                               'uked': (31.1, 1, None),
                               'amed': (31, 1, None),
                               'imed': (31, 1, None),
                               'does': (31.2, 2, None),
                               },
                           3: {'oed': (31.3, 1, None),
                               'oes': (31.2, 1, None),
                               'kes': (63.1, 1, None),
                               'des': (63.10, 1, None),
                               'res': (63.9, 1, None),
                               }}

        # Add the above additional rules to rule_table
        for del_len in adams_additions:
            rule_table[del_len] = dict(rule_table[del_len],
                                       **adams_additions[del_len])
        # Add additional problem word
        problem_words.add('menses')

    def _stem_with_duplicate_character_check(word, del_len):
        if word[-1] == 's':
            del_len += 1
        stemmed_word = word[:-del_len]
        if re_match(r'.*(\w)\1$', stemmed_word):
            stemmed_word = stemmed_word[:-1]
        return stemmed_word

    def _stem(word):
        stemmed_word = word
        rule_no = 0

        if not word:
            return word, 0
        if word in problem_words:
            return word, 90
        if max_word_length and len(word) > max_word_length:
            return word, 95

        if "'" in word:
            if word[-2:] in {"'s", "'S"}:
                stemmed_word = word[:-2]
            if word[-1:] == "'":
                stemmed_word = word[:-1]
            stemmed_word = stemmed_word.replace("n't", 'not')
            stemmed_word = stemmed_word.replace("'ve", 'have')
            stemmed_word = stemmed_word.replace("'re", 'are')
            stemmed_word = stemmed_word.replace("'m", 'am')
            return stemmed_word, 94

        if word.isdigit():
            return word, 90.3
        else:
            hyphen = word.find('-')
            if len(word) > hyphen > 0:
                if word[:hyphen].isalpha() and word[hyphen+1:].isalpha():
                    return word, 90.2
                else:
                    return word, 90.1
            elif '_' in word:
                return word, 90
            elif word[-1] == 's' and word[:-1].isupper():
                if var == 'Adams' and len(word)-1 > max_acro_length:
                    return word, 96
                return word[:-1], 91.1
            elif word.isupper():
                if var == 'Adams' and len(word) > max_acro_length:
                    return word, 96
                return word, 91
            elif re_match(r'^.*[A-Z].*[A-Z].*$', word):
                return word, 92
            elif word[0].isupper():
                return word, 93
            elif var == 'Adams' and re_match(r'^[a-z](|[rl])(ing|ed)$', word):
                return word, 97

        for n in range(7, 1, -1):
            if word[-n:] in rule_table[n]:
                rule_no, del_len, add_str = rule_table[n][word[-n:]]
                if del_len:
                    stemmed_word = word[:-del_len]
                else:
                    stemmed_word = word
                if add_str:
                    stemmed_word += add_str
                break

        if not rule_no:
            if re_match(r'.*\w\wings?$', word):  # rule 58
                stemmed_word = _stem_with_duplicate_character_check(word, 3)
                rule_no = 58
            elif re_match(r'.*\w\weds?$', word):  # rule 62
                stemmed_word = _stem_with_duplicate_character_check(word, 2)
                rule_no = 62
            elif word[-1] == 's':  # rule 68
                stemmed_word = word[:-1]
                rule_no = 68

        return stemmed_word, rule_no

    stem, rule_no = _stem(word)
    if return_rule_no:
        return stem, rule_no
    return stem


def paice_husk(word):
    """Return Paice-Husk stem.

    Implementation of the Paice-Husk Stemmer, also known as the Lancaster
    Stemmer, developed by Chris Paice, with the assistance of Gareth Husk

    This is based on the algorithm's description in :cite:`Paice:1990`.

    :param str word: the word to stem
    :returns: the stemmed word
    :rtype: str

    >>> paice_husk('assumption')
    'assum'
    >>> paice_husk('verifiable')
    'ver'
    >>> paice_husk('fancies')
    'fant'
    >>> paice_husk('fanciful')
    'fancy'
    >>> paice_husk('torment')
    'tor'
    """
    rule_table = {6: {'ifiabl': (False, 6, None, True),
                      'plicat': (False, 4, 'y', True)},
                  5: {'guish': (False, 5, 'ct', True),
                      'sumpt': (False, 2, None, True),
                      'istry': (False, 5, None, True)},
                  4: {'ytic': (False, 3, 's', True),
                      'ceed': (False, 2, 'ss', True),
                      'hood': (False, 4, None, False),
                      'lief': (False, 1, 'v', True),
                      'verj': (False, 1, 't', True),
                      'misj': (False, 2, 't', True),
                      'iabl': (False, 4, 'y', True),
                      'iful': (False, 4, 'y', True),
                      'sion': (False, 4, 'j', False),
                      'xion': (False, 4, 'ct', True),
                      'ship': (False, 4, None, False),
                      'ness': (False, 4, None, False),
                      'ment': (False, 4, None, False),
                      'ript': (False, 2, 'b', True),
                      'orpt': (False, 2, 'b', True),
                      'duct': (False, 1, None, True),
                      'cept': (False, 2, 'iv', True),
                      'olut': (False, 2, 'v', True),
                      'sist': (False, 0, None, True)},
                  3: {'ied': (False, 3, 'y', False),
                      'eed': (False, 1, None, True),
                      'ing': (False, 3, None, False),
                      'iag': (False, 3, 'y', True),
                      'ish': (False, 3, None, False),
                      'fuj': (False, 1, 's', True),
                      'hej': (False, 1, 'r', True),
                      'abl': (False, 3, None, False),
                      'ibl': (False, 3, None, True),
                      'bil': (False, 2, 'l', False),
                      'ful': (False, 3, None, False),
                      'ial': (False, 3, None, False),
                      'ual': (False, 3, None, False),
                      'ium': (False, 3, None, True),
                      'ism': (False, 3, None, False),
                      'ion': (False, 3, None, False),
                      'ian': (False, 3, None, False),
                      'een': (False, 0, None, True),
                      'ear': (False, 0, None, True),
                      'ier': (False, 3, 'y', False),
                      'ies': (False, 3, 'y', False),
                      'sis': (False, 2, None, True),
                      'ous': (False, 3, None, False),
                      'ent': (False, 3, None, False),
                      'ant': (False, 3, None, False),
                      'ist': (False, 3, None, False),
                      'iqu': (False, 3, None, True),
                      'ogu': (False, 1, None, True),
                      'siv': (False, 3, 'j', False),
                      'eiv': (False, 0, None, True),
                      'bly': (False, 1, None, False),
                      'ily': (False, 3, 'y', False),
                      'ply': (False, 0, None, True),
                      'ogy': (False, 1, None, True),
                      'phy': (False, 1, None, True),
                      'omy': (False, 1, None, True),
                      'opy': (False, 1, None, True),
                      'ity': (False, 3, None, False),
                      'ety': (False, 3, None, False),
                      'lty': (False, 2, None, True),
                      'ary': (False, 3, None, False),
                      'ory': (False, 3, None, False),
                      'ify': (False, 3, None, True),
                      'ncy': (False, 2, 't', False),
                      'acy': (False, 3, None, False)},
                  2: {'ia': (True, 2, None, True),
                      'bb': (False, 1, None, True),
                      'ic': (False, 2, None, False),
                      'nc': (False, 1, 't', False),
                      'dd': (False, 1, None, True),
                      'ed': (False, 2, None, False),
                      'if': (False, 2, None, False),
                      'ag': (False, 2, None, False),
                      'gg': (False, 1, None, True),
                      'th': (True, 2, None, True),
                      'ij': (False, 1, 'd', True),
                      'uj': (False, 1, 'd', True),
                      'oj': (False, 1, 'd', True),
                      'nj': (False, 1, 'd', True),
                      'cl': (False, 1, None, True),
                      'ul': (False, 2, None, True),
                      'al': (False, 2, None, False),
                      'll': (False, 1, None, True),
                      'um': (True, 2, None, True),
                      'mm': (False, 1, None, True),
                      'an': (False, 2, None, False),
                      'en': (False, 2, None, False),
                      'nn': (False, 1, None, True),
                      'pp': (False, 1, None, True),
                      'er': (False, 2, None, False),
                      'ar': (False, 2, None, True),
                      'or': (False, 2, None, False),
                      'ur': (False, 2, None, False),
                      'rr': (False, 1, None, True),
                      'tr': (False, 1, None, False),
                      'is': (False, 2, None, False),
                      'ss': (False, 0, None, True),
                      'us': (True, 2, None, True),
                      'at': (False, 2, None, False),
                      'tt': (False, 1, None, True),
                      'iv': (False, 2, None, False),
                      'ly': (False, 2, None, False),
                      'iz': (False, 2, None, False),
                      'yz': (False, 1, 's', True)},
                  1: {'a': (True, 1, None, True),
                      'e': (False, 1, None, False),
                      'i': ((True, 1, None, True), (False, 1, 'y', False)),
                      'j': (False, 1, 's', True),
                      's': ((True, 1, None, False), (False, 0, None, True))}}

    def _has_vowel(word):
        for char in word:
            if char in {'a', 'e', 'i', 'o', 'u', 'y'}:
                return True
        return False

    def _acceptable(word):
        if word and word[0] in {'a', 'e', 'i', 'o', 'u'}:
            return len(word) > 1
        return len(word) > 2 and _has_vowel(word[1:])

    def _apply_rule(word, rule, intact):
        old_word = word
        only_intact, del_len, add_str, set_terminate = rule
        # print(word, word[-n:], rule)

        if (not only_intact) or (intact and only_intact):
            if del_len:
                word = word[:-del_len]
            if add_str:
                word += add_str
        else:
            return word, False, intact, terminate

        if _acceptable(word):
            return word, True, False, set_terminate
        else:
            return old_word, False, intact, terminate

    terminate = False
    intact = True
    while not terminate:
        for n in range(6, 0, -1):
            if word[-n:] in rule_table[n]:
                accept = False
                if len(rule_table[n][word[-n:]]) < 4:
                    for rule in rule_table[n][word[-n:]]:
                        (word, accept, intact,
                         terminate) = _apply_rule(word, rule, intact)
                        if accept:
                            break
                else:
                    rule = rule_table[n][word[-n:]]
                    (word, accept, intact,
                     terminate) = _apply_rule(word, rule, intact)

                if accept:
                    break
        else:
            break

    return word


def schinke(word):
    """Return the stem of a word according to the Schinke stemmer.

    This is defined in :cite:`Schinke:1996`.

    :param str word: the word to stem
    :returns: a dict of the noun- and verb-stemmed word
    :rtype: dict

    >>> schinke('atque')
    {'n': 'atque', 'v': 'atque'}
    >>> schinke('census')
    {'n': 'cens', 'v': 'censu'}
    >>> schinke('virum')
    {'n': 'uir', 'v': 'uiru'}
    >>> schinke('populusque')
    {'n': 'popul', 'v': 'populu'}
    >>> schinke('senatus')
    {'n': 'senat', 'v': 'senatu'}
    """
    word = normalize('NFKD', text_type(word.lower()))
    word = ''.join(c for c in word if c in
                   {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                    'y', 'z'})

    # Rule 2
    word = word.replace('j', 'i').replace('v', 'u')

    # Rule 3
    keep_que = {'at', 'quo', 'ne', 'ita', 'abs', 'aps', 'abus', 'adae', 'adus',
                'deni', 'de', 'sus', 'obli', 'perae', 'plenis', 'quando',
                'quis', 'quae', 'cuius', 'cui', 'quem', 'quam', 'qua', 'qui',
                'quorum', 'quarum', 'quibus', 'quos', 'quas', 'quotusquis',
                'quous', 'ubi', 'undi', 'us', 'uter', 'uti', 'utro', 'utribi',
                'tor', 'co', 'conco', 'contor', 'detor', 'deco', 'exco',
                'extor', 'obtor', 'optor', 'retor', 'reco', 'attor', 'inco',
                'intor', 'praetor'}
    if word[-3:] == 'que':
        # This diverges from the paper by also returning 'que' itself unstemmed
        if word[:-3] in keep_que or word == 'que':
            return {'n': word, 'v': word}
        else:
            word = word[:-3]

    # Base case will mean returning the words as is
    noun = word
    verb = word

    # Rule 4
    n_endings = {4: {'ibus'},
                 3: {'ius'},
                 2: {'is', 'nt', 'ae', 'os', 'am', 'ud', 'as', 'um', 'em',
                     'us', 'es', 'ia'},
                 1: {'a', 'e', 'i', 'o', 'u'}}
    for endlen in range(4, 0, -1):
        if word[-endlen:] in n_endings[endlen]:
            if len(word)-2 >= endlen:
                noun = word[:-endlen]
            else:
                noun = word
            break

    v_endings_strip = {6: {},
                       5: {},
                       4: {'mini', 'ntur', 'stis'},
                       3: {'mur', 'mus', 'ris', 'sti', 'tis', 'tur'},
                       2: {'ns', 'nt', 'ri'},
                       1: {'m', 'r', 's', 't'}}
    v_endings_alter = {6: {'iuntur'},
                       5: {'beris', 'erunt', 'untur'},
                       4: {'iunt'},
                       3: {'bor', 'ero', 'unt'},
                       2: {'bo'},
                       1: {}}
    for endlen in range(6, 0, -1):
        if word[-endlen:] in v_endings_strip[endlen]:
            if len(word)-2 >= endlen:
                verb = word[:-endlen]
            else:
                verb = word
            break
        if word[-endlen:] in v_endings_alter[endlen]:
            if word[-endlen:] in {'iuntur', 'erunt', 'untur', 'iunt', 'unt'}:
                new_word = word[:-endlen]+'i'
                addlen = 1
            elif word[-endlen:] in {'beris', 'bor', 'bo'}:
                new_word = word[:-endlen]+'bi'
                addlen = 2
            else:
                new_word = word[:-endlen]+'eri'
                addlen = 3

            # Technically this diverges from the paper by considering the
            # length of the stem without the new suffix
            if len(new_word) >= 2+addlen:
                verb = new_word
            else:
                verb = word
            break

    return {'n': noun, 'v': verb}


def s_stemmer(word):
    """Return the S-stemmed form of a word.

    The S stemmer is defined in :cite:`Harman:1991`.

    :param str word: the word to stem
    :returns: the stemmed word
    :rtype: str

    >>> s_stemmer('summaries')
    'summary'
    >>> s_stemmer('summary')
    'summary'
    >>> s_stemmer('towers')
    'tower'
    >>> s_stemmer('reading')
    'reading'
    >>> s_stemmer('census')
    'census'
    """
    lowered = word.lower()
    if lowered[-3:] == 'ies' and lowered[-4:-3] not in {'e', 'a'}:
        return word[:-3] + ('Y' if word[-1:].isupper() else 'y')
    if lowered[-2:] == 'es' and lowered[-3:-2] not in {'a', 'e', 'o'}:
        return word[:-1]
    if lowered[-1:] == 's' and lowered[-2:-1] not in {'u', 's'}:
        return word[:-1]
    return word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
