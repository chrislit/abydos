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

Lovins stemmer.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize

from six import text_type
from six.moves import range

from ._stemmer import _Stemmer

__all__ = ['Lovins', 'lovins']


class Lovins(_Stemmer):
    """Lovins stemmer.

    The Lovins stemmer is described in Julie Beth Lovins's article
    :cite:`Lovins:1968`.
    """

    def _cond_b(self, word, suffix_len):
        """Return Lovins' condition B.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return len(word) - suffix_len >= 3

    def _cond_c(self, word, suffix_len):
        """Return Lovins' condition C.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return len(word) - suffix_len >= 4

    def _cond_d(self, word, suffix_len):
        """Return Lovins' condition D.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return len(word) - suffix_len >= 5

    def _cond_e(self, word, suffix_len):
        """Return Lovins' condition E.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] != 'e'

    def _cond_f(self, word, suffix_len):
        """Return Lovins' condition F.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return len(word) - suffix_len >= 3 and word[-suffix_len - 1] != 'e'

    def _cond_g(self, word, suffix_len):
        """Return Lovins' condition G.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return len(word) - suffix_len >= 3 and word[-suffix_len - 1] == 'f'

    def _cond_h(self, word, suffix_len):
        """Return Lovins' condition H.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return (
            word[-suffix_len - 1] == 't'
            or word[-suffix_len - 2 : -suffix_len] == 'll'
        )

    def _cond_i(self, word, suffix_len):
        """Return Lovins' condition I.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] not in {'e', 'o'}

    def _cond_j(self, word, suffix_len):
        """Return Lovins' condition J.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] not in {'a', 'e'}

    def _cond_k(self, word, suffix_len):
        """Return Lovins' condition K.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return (len(word) - suffix_len >= 3) and (
            word[-suffix_len - 1] in {'i', 'l'}
            or (word[-suffix_len - 3] == 'u' and word[-suffix_len - 1] == 'e')
        )

    def _cond_l(self, word, suffix_len):
        """Return Lovins' condition L.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return (
            word[-suffix_len - 1] not in {'s', 'u', 'x'}
            or word[-suffix_len - 1] == 'os'
        )

    def _cond_m(self, word, suffix_len):
        """Return Lovins' condition M.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] not in {'a', 'c', 'e', 'm'}

    def _cond_n(self, word, suffix_len):
        """Return Lovins' condition N.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        if len(word) - suffix_len >= 3:
            if word[-suffix_len - 3] == 's':
                if len(word) - suffix_len >= 4:
                    return True
            else:
                return True
        return False

    def _cond_o(self, word, suffix_len):
        """Return Lovins' condition O.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] in {'i', 'l'}

    def _cond_p(self, word, suffix_len):
        """Return Lovins' condition P.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] != 'c'

    def _cond_q(self, word, suffix_len):
        """Return Lovins' condition Q.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return len(word) - suffix_len >= 3 and word[-suffix_len - 1] not in {
            'l',
            'n',
        }

    def _cond_r(self, word, suffix_len):
        """Return Lovins' condition R.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] in {'n', 'r'}

    def _cond_s(self, word, suffix_len):
        """Return Lovins' condition S.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 2 : -suffix_len] == 'dr' or (
            word[-suffix_len - 1] == 't'
            and word[-suffix_len - 2 : -suffix_len] != 'tt'
        )

    def _cond_t(self, word, suffix_len):
        """Return Lovins' condition T.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return (
            word[-suffix_len - 1] in {'s', 't'}
            and word[-suffix_len - 2 : -suffix_len] != 'ot'
        )

    def _cond_u(self, word, suffix_len):
        """Return Lovins' condition U.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] in {'l', 'm', 'n', 'r'}

    def _cond_v(self, word, suffix_len):
        """Return Lovins' condition V.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] == 'c'

    def _cond_w(self, word, suffix_len):
        """Return Lovins' condition W.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] not in {'s', 'u'}

    def _cond_x(self, word, suffix_len):
        """Return Lovins' condition X.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] in {'i', 'l'} or (
            word[-suffix_len - 3 : -suffix_len] == 'u'
            and word[-suffix_len - 1] == 'e'
        )

    def _cond_y(self, word, suffix_len):
        """Return Lovins' condition Y.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 2 : -suffix_len] == 'in'

    def _cond_z(self, word, suffix_len):
        """Return Lovins' condition Z.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] != 'f'

    def _cond_aa(self, word, suffix_len):
        """Return Lovins' condition AA.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] in {'d', 'f', 'l', 't'} or word[
            -suffix_len - 2 : -suffix_len
        ] in {'ph', 'th', 'er', 'or', 'es'}

    def _cond_bb(self, word, suffix_len):
        """Return Lovins' condition BB.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return (
            len(word) - suffix_len >= 3
            and word[-suffix_len - 3 : -suffix_len] != 'met'
            and word[-suffix_len - 4 : -suffix_len] != 'ryst'
        )

    def _cond_cc(self, word, suffix_len):
        """Return Lovins' condition CC.

        Parameters
        ----------
        word : str
            Word to check
        suffix_len : int
            Suffix length

        Returns
        -------
        bool
            True if condition is met

        """
        return word[-suffix_len - 1] == 'l'

    def _recode9(self, stem):
        """Return Lovins' conditional recode rule 9.

        Parameters
        ----------
        stem : str
            Word to stem

        Returns
        -------
        str
            Word stripped of suffix

        """
        if stem[-3:-2] in {'a', 'i', 'o'}:
            return stem
        return stem[:-2] + 'l'

    def _recode24(self, stem):
        """Return Lovins' conditional recode rule 24.

        Parameters
        ----------
        stem : str
            Word to stem

        Returns
        -------
        str
            Word stripped of suffix

        """
        if stem[-4:-3] == 's':
            return stem
        return stem[:-1] + 's'

    def _recode28(self, stem):
        """Return Lovins' conditional recode rule 28.

        Parameters
        ----------
        stem : str
            Word to stem

        Returns
        -------
        str
            Word stripped of suffix

        """
        if stem[-4:-3] in {'p', 't'}:
            return stem
        return stem[:-1] + 's'

    def _recode30(self, stem):
        """Return Lovins' conditional recode rule 30.

        Parameters
        ----------
        stem : str
            Word to stem

        Returns
        -------
        str
            Word stripped of suffix

        """
        if stem[-4:-3] == 'm':
            return stem
        return stem[:-1] + 's'

    def _recode32(self, stem):
        """Return Lovins' conditional recode rule 32.

        Parameters
        ----------
        stem : str
            Word to stem

        Returns
        -------
        str
            Word stripped of suffix

        """
        if stem[-3:-2] == 'n':
            return stem
        return stem[:-1] + 's'

    _suffix = {}
    _recode = ()

    def __init__(self):
        """Initialize the stemmer."""
        self._suffix = {
            'alistically': self._cond_b,
            'arizability': None,
            'izationally': self._cond_b,
            'antialness': None,
            'arisations': None,
            'arizations': None,
            'entialness': None,
            'allically': self._cond_c,
            'antaneous': None,
            'antiality': None,
            'arisation': None,
            'arization': None,
            'ationally': self._cond_b,
            'ativeness': None,
            'eableness': self._cond_e,
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
            'alistic': self._cond_b,
            'alities': None,
            'ariness': self._cond_e,
            'aristic': None,
            'arizing': None,
            'ateness': None,
            'atingly': None,
            'ational': self._cond_b,
            'atively': None,
            'ativism': None,
            'elihood': self._cond_e,
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
            'ication': self._cond_g,
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
            'ization': self._cond_f,
            'izement': None,
            'oidally': None,
            'ousness': None,
            'aceous': None,
            'acious': self._cond_b,
            'action': self._cond_g,
            'alness': None,
            'ancial': None,
            'ancies': None,
            'ancing': self._cond_b,
            'ariser': None,
            'arized': None,
            'arizer': None,
            'atable': None,
            'ations': self._cond_b,
            'atives': None,
            'eature': self._cond_z,
            'efully': None,
            'encies': None,
            'encing': None,
            'ential': None,
            'enting': self._cond_c,
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
            'ionate': self._cond_d,
            'ioning': None,
            'ionist': None,
            'iously': None,
            'istics': None,
            'izable': self._cond_e,
            'lessly': None,
            'nesses': None,
            'oidism': None,
            'acies': None,
            'acity': None,
            'aging': self._cond_b,
            'aical': None,
            'alist': None,
            'alism': self._cond_b,
            'ality': None,
            'alize': None,
            'allic': self._cond_bb,
            'anced': self._cond_b,
            'ances': self._cond_b,
            'antic': self._cond_c,
            'arial': None,
            'aries': None,
            'arily': None,
            'arity': self._cond_b,
            'arize': None,
            'aroid': None,
            'ately': None,
            'ating': self._cond_i,
            'ation': self._cond_b,
            'ative': None,
            'ators': None,
            'atory': None,
            'ature': self._cond_e,
            'early': self._cond_y,
            'ehood': None,
            'eless': None,
            'elity': None,
            'ement': None,
            'enced': None,
            'ences': None,
            'eness': self._cond_e,
            'ening': self._cond_e,
            'ental': None,
            'ented': self._cond_c,
            'ently': None,
            'fully': None,
            'ially': None,
            'icant': None,
            'ician': None,
            'icide': None,
            'icism': None,
            'icist': None,
            'icity': None,
            'idine': self._cond_i,
            'iedly': None,
            'ihood': None,
            'inate': None,
            'iness': None,
            'ingly': self._cond_b,
            'inism': self._cond_j,
            'inity': self._cond_cc,
            'ional': None,
            'ioned': None,
            'ished': None,
            'istic': None,
            'ities': None,
            'itous': None,
            'ively': None,
            'ivity': None,
            'izers': self._cond_f,
            'izing': self._cond_f,
            'oidal': None,
            'oides': None,
            'otide': None,
            'ously': None,
            'able': None,
            'ably': None,
            'ages': self._cond_b,
            'ally': self._cond_b,
            'ance': self._cond_b,
            'ancy': self._cond_b,
            'ants': self._cond_b,
            'aric': None,
            'arly': self._cond_k,
            'ated': self._cond_i,
            'ates': None,
            'atic': self._cond_b,
            'ator': None,
            'ealy': self._cond_y,
            'edly': self._cond_e,
            'eful': None,
            'eity': None,
            'ence': None,
            'ency': None,
            'ened': self._cond_e,
            'enly': self._cond_e,
            'eous': None,
            'hood': None,
            'ials': None,
            'ians': None,
            'ible': None,
            'ibly': None,
            'ical': None,
            'ides': self._cond_l,
            'iers': None,
            'iful': None,
            'ines': self._cond_m,
            'ings': self._cond_n,
            'ions': self._cond_b,
            'ious': None,
            'isms': self._cond_b,
            'ists': None,
            'itic': self._cond_h,
            'ized': self._cond_f,
            'izer': self._cond_f,
            'less': None,
            'lily': None,
            'ness': None,
            'ogen': None,
            'ward': None,
            'wise': None,
            'ying': self._cond_b,
            'yish': None,
            'acy': None,
            'age': self._cond_b,
            'aic': None,
            'als': self._cond_bb,
            'ant': self._cond_b,
            'ars': self._cond_o,
            'ary': self._cond_f,
            'ata': None,
            'ate': None,
            'eal': self._cond_y,
            'ear': self._cond_y,
            'ely': self._cond_e,
            'ene': self._cond_e,
            'ent': self._cond_c,
            'ery': self._cond_e,
            'ese': None,
            'ful': None,
            'ial': None,
            'ian': None,
            'ics': None,
            'ide': self._cond_l,
            'ied': None,
            'ier': None,
            'ies': self._cond_p,
            'ily': None,
            'ine': self._cond_m,
            'ing': self._cond_n,
            'ion': self._cond_q,
            'ish': self._cond_c,
            'ism': self._cond_b,
            'ist': None,
            'ite': self._cond_aa,
            'ity': None,
            'ium': None,
            'ive': None,
            'ize': self._cond_f,
            'oid': None,
            'one': self._cond_r,
            'ous': None,
            'ae': None,
            'al': self._cond_bb,
            'ar': self._cond_x,
            'as': self._cond_b,
            'ed': self._cond_e,
            'en': self._cond_f,
            'es': self._cond_e,
            'ia': None,
            'ic': None,
            'is': None,
            'ly': self._cond_b,
            'on': self._cond_s,
            'or': self._cond_t,
            'um': self._cond_u,
            'us': self._cond_v,
            'yl': self._cond_r,
            '\'s': None,
            's\'': None,
            'a': None,
            'e': None,
            'i': None,
            'o': None,
            's': self._cond_w,
            'y': self._cond_b,
        }

        self._recode = (
            ('iev', 'ief'),
            ('uct', 'uc'),
            ('umpt', 'um'),
            ('rpt', 'rb'),
            ('urs', 'ur'),
            ('istr', 'ister'),
            ('metr', 'meter'),
            ('olv', 'olut'),
            ('ul', self._recode9),
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
            ('end', self._recode24),
            ('ond', 'ons'),
            ('lud', 'lus'),
            ('rud', 'rus'),
            ('her', self._recode28),
            ('mit', 'mis'),
            ('ent', self._recode30),
            ('ert', 'ers'),
            ('et', self._recode32),
            ('yt', 'ys'),
            ('yz', 'ys'),
        )

    def stem(self, word):
        """Return Lovins stem.

        Parameters
        ----------
        word : str
            The word to stem

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = Lovins()
        >>> stmr.stem('reading')
        'read'
        >>> stmr.stem('suspension')
        'suspens'
        >>> stmr.stem('elusiveness')
        'elus'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))

        for suffix_len in range(11, 0, -1):
            ending = word[-suffix_len:]
            if (
                ending in self._suffix
                and len(word) - suffix_len >= 2
                and (
                    self._suffix[ending] is None
                    or self._suffix[ending](word, suffix_len)
                )
            ):
                word = word[:-suffix_len]
                break

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

        for ending, replacement in self._recode:
            if word.endswith(ending):
                if callable(replacement):
                    word = replacement(word)
                else:
                    word = word[: -len(ending)] + replacement

        return word


def lovins(word):
    """Return Lovins stem.

    This is a wrapper for :py:meth:`Lovins.stem`.

    Parameters
    ----------
    word : str
        The word to stem

    Returns
    -------
    str: Word stem

    Examples
    --------
    >>> lovins('reading')
    'read'
    >>> lovins('suspension')
    'suspens'
    >>> lovins('elusiveness')
    'elus'

    """
    return Lovins().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
