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
    # pylint: disable=too-many-branches

    # lowercase, normalize, and compose
    word = unicodedata.normalize('NFC', _unicode(word.lower()))

    def cond_a(word, suffix_len):
        """Lovins' condition A
        """
        return True

    def cond_b(word, suffix_len):
        """Lovins' condition B
        """
        return len(word)-suffix_len >= 3

    def cond_c(word, suffix_len):
        """Lovins' condition C
        """
        return len(word)-suffix_len >= 4

    def cond_d(word, suffix_len):
        """Lovins' condition D
        """
        return len(word)-suffix_len >= 5

    def cond_e(word, suffix_len):
        """Lovins' condition E
        """
        return word[-suffix_len-1] != 'e'

    def cond_f(word, suffix_len):
        """Lovins' condition F
        """
        return (len(word)-suffix_len >= 3 and
                word[-suffix_len-1] != 'e')

    def cond_g(word, suffix_len):
        """Lovins' condition G
        """
        return (len(word)-suffix_len >= 3 and
                word[-suffix_len-1] == 'f')

    def cond_h(word, suffix_len):
        """Lovins' condition H
        """
        return (word[-suffix_len-1] == 't' or
                word[-suffix_len-2:-suffix_len] == 'll')

    def cond_i(word, suffix_len):
        """Lovins' condition I
        """
        return word[-suffix_len-1] not in frozenset('oe')

    def cond_j(word, suffix_len):
        """Lovins' condition J
        """
        return word[-suffix_len-1] not in frozenset('ae')

    def cond_k(word, suffix_len):
        """Lovins' condition K
        """
        return (len(word)-suffix_len >= 3 and
                (word[-suffix_len-1] in frozenset('li') or
                 (word[-suffix_len-3] == 'u' and word[-suffix_len-1] == 'e')))

    def cond_l(word, suffix_len):
        """Lovins' condition L
        """
        return (word[-suffix_len-1] not in frozenset('uxs') or
                word[-suffix_len-1] == 'os')

    def cond_m(word, suffix_len):
        """Lovins' condition M
        """
        return word[-suffix_len-1] not in frozenset('acem')

    def cond_n(word, suffix_len):
        """Lovins' condition N
        """
        if len(word)-suffix_len >= 3:
            if word[-suffix_len-3] == 's':
                if len(word)-suffix_len >= 4:
                    return True
            else:
                return True
        return False

    def cond_o(word, suffix_len):
        """Lovins' condition O
        """
        return word[-suffix_len-1] in frozenset('li')

    def cond_p(word, suffix_len):
        """Lovins' condition P
        """
        return word[-suffix_len-1] != 'c'

    def cond_q(word, suffix_len):
        """Lovins' condition Q
        """
        return (len(word)-suffix_len >= 3 and
                word[-suffix_len-1] not in frozenset('ln'))

    def cond_r(word, suffix_len):
        """Lovins' condition R
        """
        return word[-suffix_len-1] in frozenset('nr')

    def cond_s(word, suffix_len):
        """Lovins' condition S
        """
        return (word[-suffix_len-2:-suffix_len] == 'dr' or
                (word[-suffix_len-1] == 't' and
                 word[-suffix_len-2:-suffix_len] != 'tt'))

    def cond_t(word, suffix_len):
        """Lovins' condition T
        """
        return (word[-suffix_len-1] in frozenset('st') and
                word[-suffix_len-2:-suffix_len] != 'ot')

    def cond_u(word, suffix_len):
        """Lovins' condition U
        """
        return word[-suffix_len-1] in frozenset('lmnr')

    def cond_v(word, suffix_len):
        """Lovins' condition V
        """
        return word[-suffix_len-1] == 'c'

    def cond_w(word, suffix_len):
        """Lovins' condition W
        """
        return word[-suffix_len-1] not in frozenset('su')

    def cond_x(word, suffix_len):
        """Lovins' condition X
        """
        return (word[-suffix_len-1] in frozenset('li') or
                (word[-suffix_len-3:-suffix_len] == 'u' and
                 word[-suffix_len-1] == 'e'))

    def cond_y(word, suffix_len):
        """Lovins' condition Y
        """
        return word[-suffix_len-2:-suffix_len] == 'in'

    def cond_z(word, suffix_len):
        """Lovins' condition Z
        """
        return word[-suffix_len-1] != 'f'

    def cond_aa(word, suffix_len):
        """Lovins' condition AA
        """
        return (word[-suffix_len-1] in frozenset('dflt') or
                word[-suffix_len-2:-suffix_len] in frozenset(['ph', 'th', 'er',
                                                              'or', 'es']))

    def cond_bb(word, suffix_len):
        """Lovins' condition BB
        """
        return (len(word)-suffix_len >= 3 and
                word[-suffix_len-3:-suffix_len] != 'met' and
                word[-suffix_len-4:-suffix_len] != 'ryst')

    def cond_cc(word, suffix_len):
        """Lovins' condition CC
        """
        return word[-suffix_len-1] == 'l'

    suffix = {'alistically': cond_b, 'arizability': cond_a,
              'izationally': cond_b, 'antialness': cond_a,
              'arisations': cond_a, 'arizations': cond_a, 'entialness': cond_a,
              'allically': cond_c, 'antaneous': cond_a, 'antiality': cond_a,
              'arisation': cond_a, 'arization': cond_a, 'ationally': cond_b,
              'ativeness': cond_a, 'eableness': cond_e, 'entations': cond_a,
              'entiality': cond_a, 'entialize': cond_a, 'entiation': cond_a,
              'ionalness': cond_a, 'istically': cond_a, 'itousness': cond_a,
              'izability': cond_a, 'izational': cond_a, 'ableness': cond_a,
              'arizable': cond_a, 'entation': cond_a, 'entially': cond_a,
              'eousness': cond_a, 'ibleness': cond_a, 'icalness': cond_a,
              'ionalism': cond_a, 'ionality': cond_a, 'ionalize': cond_a,
              'iousness': cond_a, 'izations': cond_a, 'lessness': cond_a,
              'ability': cond_a, 'aically': cond_a, 'alistic': cond_b,
              'alities': cond_a, 'ariness': cond_e, 'aristic': cond_a,
              'arizing': cond_a, 'ateness': cond_a, 'atingly': cond_a,
              'ational': cond_b, 'atively': cond_a, 'ativism': cond_a,
              'elihood': cond_e, 'encible': cond_a, 'entally': cond_a,
              'entials': cond_a, 'entiate': cond_a, 'entness': cond_a,
              'fulness': cond_a, 'ibility': cond_a, 'icalism': cond_a,
              'icalist': cond_a, 'icality': cond_a, 'icalize': cond_a,
              'ication': cond_g, 'icianry': cond_a, 'ination': cond_a,
              'ingness': cond_a, 'ionally': cond_a, 'isation': cond_a,
              'ishness': cond_a, 'istical': cond_a, 'iteness': cond_a,
              'iveness': cond_a, 'ivistic': cond_a, 'ivities': cond_a,
              'ization': cond_f, 'izement': cond_a, 'oidally': cond_a,
              'ousness': cond_a, 'aceous': cond_a, 'acious': cond_b,
              'action': cond_g, 'alness': cond_a, 'ancial': cond_a,
              'ancies': cond_a, 'ancing': cond_b, 'ariser': cond_a,
              'arized': cond_a, 'arizer': cond_a, 'atable': cond_a,
              'ations': cond_b, 'atives': cond_a, 'eature': cond_z,
              'efully': cond_a, 'encies': cond_a, 'encing': cond_a,
              'ential': cond_a, 'enting': cond_c, 'entist': cond_a,
              'eously': cond_a, 'ialist': cond_a, 'iality': cond_a,
              'ialize': cond_a, 'ically': cond_a, 'icance': cond_a,
              'icians': cond_a, 'icists': cond_a, 'ifully': cond_a,
              'ionals': cond_a, 'ionate': cond_d, 'ioning': cond_a,
              'ionist': cond_a, 'iously': cond_a, 'istics': cond_a,
              'izable': cond_e, 'lessly': cond_a, 'nesses': cond_a,
              'oidism': cond_a, 'acies': cond_a, 'acity': cond_a,
              'aging': cond_b, 'aical': cond_a, 'alist': cond_a,
              'alism': cond_b, 'ality': cond_a, 'alize': cond_a,
              'allic': cond_bb, 'anced': cond_b, 'ances': cond_b,
              'antic': cond_c, 'arial': cond_a, 'aries': cond_a,
              'arily': cond_a, 'arity': cond_b, 'arize': cond_a,
              'aroid': cond_a, 'ately': cond_a, 'ating': cond_i,
              'ation': cond_b, 'ative': cond_a, 'ators': cond_a,
              'atory': cond_a, 'ature': cond_e, 'early': cond_y,
              'ehood': cond_a, 'eless': cond_a, 'elity': cond_a,
              'ement': cond_a, 'enced': cond_a, 'ences': cond_a,
              'eness': cond_e, 'ening': cond_e, 'ental': cond_a,
              'ented': cond_c, 'ently': cond_a, 'fully': cond_a,
              'ially': cond_a, 'icant': cond_a, 'ician': cond_a,
              'icide': cond_a, 'icism': cond_a, 'icist': cond_a,
              'icity': cond_a, 'idine': cond_i, 'iedly': cond_a,
              'ihood': cond_a, 'inate': cond_a, 'iness': cond_a,
              'ingly': cond_b, 'inism': cond_j, 'inity': cond_cc,
              'ional': cond_a, 'ioned': cond_a, 'ished': cond_a,
              'istic': cond_a, 'ities': cond_a, 'itous': cond_a,
              'ively': cond_a, 'ivity': cond_a, 'izers': cond_f,
              'izing': cond_f, 'oidal': cond_a, 'oides': cond_a,
              'otide': cond_a, 'ously': cond_a, 'able': cond_a, 'ably': cond_a,
              'ages': cond_b, 'ally': cond_b, 'ance': cond_b, 'ancy': cond_b,
              'ants': cond_b, 'aric': cond_a, 'arly': cond_k, 'ated': cond_i,
              'ates': cond_a, 'atic': cond_b, 'ator': cond_a, 'ealy': cond_y,
              'edly': cond_e, 'eful': cond_a, 'eity': cond_a, 'ence': cond_a,
              'ency': cond_a, 'ened': cond_e, 'enly': cond_e, 'eous': cond_a,
              'hood': cond_a, 'ials': cond_a, 'ians': cond_a, 'ible': cond_a,
              'ibly': cond_a, 'ical': cond_a, 'ides': cond_l, 'iers': cond_a,
              'iful': cond_a, 'ines': cond_m, 'ings': cond_n, 'ions': cond_b,
              'ious': cond_a, 'isms': cond_b, 'ists': cond_a, 'itic': cond_h,
              'ized': cond_f, 'izer': cond_f, 'less': cond_a, 'lily': cond_a,
              'ness': cond_a, 'ogen': cond_a, 'ward': cond_a, 'wise': cond_a,
              'ying': cond_b, 'yish': cond_a, 'acy': cond_a, 'age': cond_b,
              'aic': cond_a, 'als': cond_bb, 'ant': cond_b, 'ars': cond_o,
              'ary': cond_f, 'ata': cond_a, 'ate': cond_a, 'eal': cond_y,
              'ear': cond_y, 'ely': cond_e, 'ene': cond_e, 'ent': cond_c,
              'ery': cond_e, 'ese': cond_a, 'ful': cond_a, 'ial': cond_a,
              'ian': cond_a, 'ics': cond_a, 'ide': cond_l, 'ied': cond_a,
              'ier': cond_a, 'ies': cond_p, 'ily': cond_a, 'ine': cond_m,
              'ing': cond_n, 'ion': cond_q, 'ish': cond_c, 'ism': cond_b,
              'ist': cond_a, 'ite': cond_aa, 'ity': cond_a, 'ium': cond_a,
              'ive': cond_a, 'ize': cond_f, 'oid': cond_a, 'one': cond_r,
              'ous': cond_a, 'ae': cond_a, 'al': cond_bb, 'ar': cond_x,
              'as': cond_b, 'ed': cond_e, 'en': cond_f, 'es': cond_e,
              'ia': cond_a, 'ic': cond_a, 'is': cond_a, 'ly': cond_b,
              'on': cond_s, 'or': cond_t, 'um': cond_u, 'us': cond_v,
              'yl': cond_r, '\'s': cond_a, 's\'': cond_a, 'a': cond_a,
              'e': cond_a, 'i': cond_a, 'o': cond_a, 's': cond_w, 'y': cond_b}

    for suffix_len in _range(11, 0, -1):
        if ((word[-suffix_len:] in suffix and
             len(word)-suffix_len >= 2 and
             suffix[word[-suffix_len:]](word, suffix_len))):
            word = word[:-suffix_len]
            break

    def recode9(stem):
        """Lovins' conditional recode rule 9
        """
        if stem[-3:-2] in frozenset('aio'):
            return stem
        else:
            return stem[:-2]+'l'

    def recode24(stem):
        """Lovins' conditional recode rule 24
        """
        if stem[-4:-3] == 's':
            return stem
        else:
            return stem[:-1]+'s'

    def recode28(stem):
        """Lovins' conditional recode rule 28
        """
        if stem[-4:-3] in frozenset('pt'):
            return stem
        else:
            return stem[:-1]+'s'

    def recode30(stem):
        """Lovins' conditional recode rule 30
        """
        if stem[-4:-3] == 'm':
            return stem
        else:
            return stem[:-1]+'s'

    def recode32(stem):
        """Lovins' conditional recode rule 32
        """
        if stem[-3:-2] == 'n':
            return stem
        else:
            return stem[:-1]+'s'

    if word[-2:] in frozenset(['bb', 'dd', 'gg', 'll', 'mm', 'nn', 'pp', 'rr',
                               'ss', 'tt']):
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


# def uealite(word):
#     """Implementation of the UEA-Lite stemmer
#
#     Arguments:
#     word -- the word to calculate the stem of
#
#     Description:
#     The UEA-Lite stemmer is defined in Marie-Claire Jenkins and Dan Smith's
#     article at
# http://wayback.archive.org/web/20121012154211/http://www.uea.ac.uk/polopoly_fs/1.85493!stemmer25feb.pdf
#     """
#     return word
#
#
# def lancaster(word):
#     """Implementation of the Lancaster Stemming Algorithm, developed by
#     Chris Paice, with the assistance of Gareth Husk
#
#     Arguments:
#     word -- the word to calculate the stem of
#
#     Description:
#     The Lancaster Stemming Algorithm, described at:
# http://wayback.archive.org/web/20140724170659/http://www.comp.lancs.ac.uk/computing/research/stemming/Links/paice.htm
#     """
#     lancaster_rules = ('ai*2.', 'a*1.', 'bb1.', 'city3s.', 'ci2>', 'cn1t>',
#                        'dd1.', 'dei3y>', 'deec2ss.', 'dee1.', 'de2>',
#                        'dooh4>', 'e1>', 'feil1v.', 'fi2>', 'gni3>', 'gai3y.',
#                        'ga2>', 'gg1.', 'ht*2.', 'hsiug5ct.', 'hsi3>', 'i*1.',
#                        'i1y>', 'ji1d.', 'juf1s.', 'ju1d.', 'jo1d.', 'jeh1r.',
#                        'jrev1t.', 'jsim2t.', 'jn1d.', 'j1s.', 'lbaifi6.',
#                        'lbai4y.', 'lba3>', 'lbi3.', 'lib2l>', 'lc1.',
#                        'lufi4y.', 'luf3>', 'lu2.', 'lai3>', 'lau3>', 'la2>',
#                        'll1.', 'mui3.', 'mu*2.', 'msi3>', 'mm1.', 'nois4j>',
#                        'noix4ct.', 'noi3>', 'nai3>', 'na2>', 'nee0.', 'ne2>',
#                        'nn1.', 'pihs4>', 'pp1.', 're2>', 'rae0.', 'ra2.',
#                        'ro2>', 'ru2>', 'rr1.', 'rt1>', 'rei3y>', 'sei3y>',
#                        'sis2.', 'si2>', 'ssen4>', 'ss0.', 'suo3>', 'su*2.',
#                        's*1>', 's0.', 'tacilp4y.', 'ta2>', 'tnem4>', 'tne3>',
#                        'tna3>', 'tpir2b.', 'tpro2b.', 'tcud1.', 'tpmus2.',
#                        'tpec2iv.', 'tulo2v.', 'tsis0.', 'tsi3>', 'tt1.',
#                        'uqi3.', 'ugo1.', 'vis3j>', 'vie0.', 'vi2>', 'ylb1>',
#                        'yli3y>', 'ylp0.', 'yl2>', 'ygo1.', 'yhp1.', 'ymo1.',
#                        'ypo1.', 'yti3>', 'yte3>', 'ytl2.', 'yrtsi5.',
#                        'yra3>', 'yro3>', 'yfi3.', 'ycn2t>', 'yca3>', 'zi2>',
#                        'zy1s.')
#
#     return word
