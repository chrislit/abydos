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

"""abydos.stemmer._lovins.

The stemmer._lovins module implements the Lovins stemmer.
"""

from __future__ import unicode_literals

from unicodedata import normalize

from six import text_type
from six.moves import range

__all__ = ['lovins']


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
        return len(word) - suffix_len >= 3

    def cond_c(word, suffix_len):
        """Return Lovins' condition C.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word) - suffix_len >= 4

    def cond_d(word, suffix_len):
        """Return Lovins' condition D.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word) - suffix_len >= 5

    def cond_e(word, suffix_len):
        """Return Lovins' condition E.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] != 'e'

    def cond_f(word, suffix_len):
        """Return Lovins' condition F.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word) - suffix_len >= 3 and word[-suffix_len - 1] != 'e'

    def cond_g(word, suffix_len):
        """Return Lovins' condition G.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word) - suffix_len >= 3 and word[-suffix_len - 1] == 'f'

    def cond_h(word, suffix_len):
        """Return Lovins' condition H.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (
            word[-suffix_len - 1] == 't'
            or word[-suffix_len - 2 : -suffix_len] == 'll'
        )

    def cond_i(word, suffix_len):
        """Return Lovins' condition I.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] not in {'e', 'o'}

    def cond_j(word, suffix_len):
        """Return Lovins' condition J.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] not in {'a', 'e'}

    def cond_k(word, suffix_len):
        """Return Lovins' condition K.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word) - suffix_len >= 3 and (
            word[-suffix_len - 1] in {'i', 'l'}
            or (word[-suffix_len - 3] == 'u' and word[-suffix_len - 1] == 'e')
        )

    def cond_l(word, suffix_len):
        """Return Lovins' condition L.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (
            word[-suffix_len - 1] not in {'s', 'u', 'x'}
            or word[-suffix_len - 1] == 'os'
        )

    def cond_m(word, suffix_len):
        """Return Lovins' condition M.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] not in {'a', 'c', 'e', 'm'}

    def cond_n(word, suffix_len):
        """Return Lovins' condition N.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        if len(word) - suffix_len >= 3:
            if word[-suffix_len - 3] == 's':
                if len(word) - suffix_len >= 4:
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
        return word[-suffix_len - 1] in {'i', 'l'}

    def cond_p(word, suffix_len):
        """Return Lovins' condition P.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] != 'c'

    def cond_q(word, suffix_len):
        """Return Lovins' condition Q.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return len(word) - suffix_len >= 3 and word[-suffix_len - 1] not in {
            'l',
            'n',
        }

    def cond_r(word, suffix_len):
        """Return Lovins' condition R.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] in {'n', 'r'}

    def cond_s(word, suffix_len):
        """Return Lovins' condition S.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 2 : -suffix_len] == 'dr' or (
            word[-suffix_len - 1] == 't'
            and word[-suffix_len - 2 : -suffix_len] != 'tt'
        )

    def cond_t(word, suffix_len):
        """Return Lovins' condition T.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (
            word[-suffix_len - 1] in {'s', 't'}
            and word[-suffix_len - 2 : -suffix_len] != 'ot'
        )

    def cond_u(word, suffix_len):
        """Return Lovins' condition U.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] in {'l', 'm', 'n', 'r'}

    def cond_v(word, suffix_len):
        """Return Lovins' condition V.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] == 'c'

    def cond_w(word, suffix_len):
        """Return Lovins' condition W.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] not in {'s', 'u'}

    def cond_x(word, suffix_len):
        """Return Lovins' condition X.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] in {'i', 'l'} or (
            word[-suffix_len - 3 : -suffix_len] == 'u'
            and word[-suffix_len - 1] == 'e'
        )

    def cond_y(word, suffix_len):
        """Return Lovins' condition Y.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 2 : -suffix_len] == 'in'

    def cond_z(word, suffix_len):
        """Return Lovins' condition Z.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] != 'f'

    def cond_aa(word, suffix_len):
        """Return Lovins' condition AA.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] in {'d', 'f', 'l', 't'} or word[
            -suffix_len - 2 : -suffix_len
        ] in {'ph', 'th', 'er', 'or', 'es'}

    def cond_bb(word, suffix_len):
        """Return Lovins' condition BB.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return (
            len(word) - suffix_len >= 3
            and word[-suffix_len - 3 : -suffix_len] != 'met'
            and word[-suffix_len - 4 : -suffix_len] != 'ryst'
        )

    def cond_cc(word, suffix_len):
        """Return Lovins' condition CC.

        :param str word: word to check
        :param int suffix_len: suffix length
        :rtype: bool
        """
        return word[-suffix_len - 1] == 'l'

    suffix = {
        'alistically': cond_b,
        'arizability': None,
        'izationally': cond_b,
        'antialness': None,
        'arisations': None,
        'arizations': None,
        'entialness': None,
        'allically': cond_c,
        'antaneous': None,
        'antiality': None,
        'arisation': None,
        'arization': None,
        'ationally': cond_b,
        'ativeness': None,
        'eableness': cond_e,
        'entations': None,
        'entiality': None,
        'entialize': None,
        'entiation': None,
        'ionalness': None,
        'istically': None,
        'itousness': None,
        'izability': None,
        'izational': None,
        'ableness': None,
        'arizable': None,
        'entation': None,
        'entially': None,
        'eousness': None,
        'ibleness': None,
        'icalness': None,
        'ionalism': None,
        'ionality': None,
        'ionalize': None,
        'iousness': None,
        'izations': None,
        'lessness': None,
        'ability': None,
        'aically': None,
        'alistic': cond_b,
        'alities': None,
        'ariness': cond_e,
        'aristic': None,
        'arizing': None,
        'ateness': None,
        'atingly': None,
        'ational': cond_b,
        'atively': None,
        'ativism': None,
        'elihood': cond_e,
        'encible': None,
        'entally': None,
        'entials': None,
        'entiate': None,
        'entness': None,
        'fulness': None,
        'ibility': None,
        'icalism': None,
        'icalist': None,
        'icality': None,
        'icalize': None,
        'ication': cond_g,
        'icianry': None,
        'ination': None,
        'ingness': None,
        'ionally': None,
        'isation': None,
        'ishness': None,
        'istical': None,
        'iteness': None,
        'iveness': None,
        'ivistic': None,
        'ivities': None,
        'ization': cond_f,
        'izement': None,
        'oidally': None,
        'ousness': None,
        'aceous': None,
        'acious': cond_b,
        'action': cond_g,
        'alness': None,
        'ancial': None,
        'ancies': None,
        'ancing': cond_b,
        'ariser': None,
        'arized': None,
        'arizer': None,
        'atable': None,
        'ations': cond_b,
        'atives': None,
        'eature': cond_z,
        'efully': None,
        'encies': None,
        'encing': None,
        'ential': None,
        'enting': cond_c,
        'entist': None,
        'eously': None,
        'ialist': None,
        'iality': None,
        'ialize': None,
        'ically': None,
        'icance': None,
        'icians': None,
        'icists': None,
        'ifully': None,
        'ionals': None,
        'ionate': cond_d,
        'ioning': None,
        'ionist': None,
        'iously': None,
        'istics': None,
        'izable': cond_e,
        'lessly': None,
        'nesses': None,
        'oidism': None,
        'acies': None,
        'acity': None,
        'aging': cond_b,
        'aical': None,
        'alist': None,
        'alism': cond_b,
        'ality': None,
        'alize': None,
        'allic': cond_bb,
        'anced': cond_b,
        'ances': cond_b,
        'antic': cond_c,
        'arial': None,
        'aries': None,
        'arily': None,
        'arity': cond_b,
        'arize': None,
        'aroid': None,
        'ately': None,
        'ating': cond_i,
        'ation': cond_b,
        'ative': None,
        'ators': None,
        'atory': None,
        'ature': cond_e,
        'early': cond_y,
        'ehood': None,
        'eless': None,
        'elity': None,
        'ement': None,
        'enced': None,
        'ences': None,
        'eness': cond_e,
        'ening': cond_e,
        'ental': None,
        'ented': cond_c,
        'ently': None,
        'fully': None,
        'ially': None,
        'icant': None,
        'ician': None,
        'icide': None,
        'icism': None,
        'icist': None,
        'icity': None,
        'idine': cond_i,
        'iedly': None,
        'ihood': None,
        'inate': None,
        'iness': None,
        'ingly': cond_b,
        'inism': cond_j,
        'inity': cond_cc,
        'ional': None,
        'ioned': None,
        'ished': None,
        'istic': None,
        'ities': None,
        'itous': None,
        'ively': None,
        'ivity': None,
        'izers': cond_f,
        'izing': cond_f,
        'oidal': None,
        'oides': None,
        'otide': None,
        'ously': None,
        'able': None,
        'ably': None,
        'ages': cond_b,
        'ally': cond_b,
        'ance': cond_b,
        'ancy': cond_b,
        'ants': cond_b,
        'aric': None,
        'arly': cond_k,
        'ated': cond_i,
        'ates': None,
        'atic': cond_b,
        'ator': None,
        'ealy': cond_y,
        'edly': cond_e,
        'eful': None,
        'eity': None,
        'ence': None,
        'ency': None,
        'ened': cond_e,
        'enly': cond_e,
        'eous': None,
        'hood': None,
        'ials': None,
        'ians': None,
        'ible': None,
        'ibly': None,
        'ical': None,
        'ides': cond_l,
        'iers': None,
        'iful': None,
        'ines': cond_m,
        'ings': cond_n,
        'ions': cond_b,
        'ious': None,
        'isms': cond_b,
        'ists': None,
        'itic': cond_h,
        'ized': cond_f,
        'izer': cond_f,
        'less': None,
        'lily': None,
        'ness': None,
        'ogen': None,
        'ward': None,
        'wise': None,
        'ying': cond_b,
        'yish': None,
        'acy': None,
        'age': cond_b,
        'aic': None,
        'als': cond_bb,
        'ant': cond_b,
        'ars': cond_o,
        'ary': cond_f,
        'ata': None,
        'ate': None,
        'eal': cond_y,
        'ear': cond_y,
        'ely': cond_e,
        'ene': cond_e,
        'ent': cond_c,
        'ery': cond_e,
        'ese': None,
        'ful': None,
        'ial': None,
        'ian': None,
        'ics': None,
        'ide': cond_l,
        'ied': None,
        'ier': None,
        'ies': cond_p,
        'ily': None,
        'ine': cond_m,
        'ing': cond_n,
        'ion': cond_q,
        'ish': cond_c,
        'ism': cond_b,
        'ist': None,
        'ite': cond_aa,
        'ity': None,
        'ium': None,
        'ive': None,
        'ize': cond_f,
        'oid': None,
        'one': cond_r,
        'ous': None,
        'ae': None,
        'al': cond_bb,
        'ar': cond_x,
        'as': cond_b,
        'ed': cond_e,
        'en': cond_f,
        'es': cond_e,
        'ia': None,
        'ic': None,
        'is': None,
        'ly': cond_b,
        'on': cond_s,
        'or': cond_t,
        'um': cond_u,
        'us': cond_v,
        'yl': cond_r,
        '\'s': None,
        's\'': None,
        'a': None,
        'e': None,
        'i': None,
        'o': None,
        's': cond_w,
        'y': cond_b,
    }

    for suffix_len in range(11, 0, -1):
        ending = word[-suffix_len:]
        if (
            ending in suffix
            and len(word) - suffix_len >= 2
            and (suffix[ending] is None or suffix[ending](word, suffix_len))
        ):
            word = word[:-suffix_len]
            break

    def recode9(stem):
        """Return Lovins' conditional recode rule 9."""
        if stem[-3:-2] in {'a', 'i', 'o'}:
            return stem
        return stem[:-2] + 'l'

    def recode24(stem):
        """Return Lovins' conditional recode rule 24."""
        if stem[-4:-3] == 's':
            return stem
        return stem[:-1] + 's'

    def recode28(stem):
        """Return Lovins' conditional recode rule 28."""
        if stem[-4:-3] in {'p', 't'}:
            return stem
        return stem[:-1] + 's'

    def recode30(stem):
        """Return Lovins' conditional recode rule 30."""
        if stem[-4:-3] == 'm':
            return stem
        return stem[:-1] + 's'

    def recode32(stem):
        """Return Lovins' conditional recode rule 32."""
        if stem[-3:-2] == 'n':
            return stem
        return stem[:-1] + 's'

    if word[-2:] in {
        'bb',
        'dd',
        'gg',
        'll',
        'mm',
        'nn',
        'pp',
        'rr',
        'ss',
        'tt',
    }:
        word = word[:-1]

    recode = (
        ('iev', 'ief'),
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
        ('yz', 'ys'),
    )

    for ending, replacement in recode:
        if word.endswith(ending):
            if callable(replacement):
                word = replacement(word)
            else:
                word = word[: -len(ending)] + replacement

    return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
