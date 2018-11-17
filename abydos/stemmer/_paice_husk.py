# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.stemmer._paice_husk.

Paice-Husk Stemmer
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six.moves import range

from ._stemmer import _Stemmer

__all__ = ['PaiceHusk', 'paice_husk']


class PaiceHusk(_Stemmer):
    """Paice-Husk stemmer.

    Implementation of the Paice-Husk Stemmer, also known as the Lancaster
    Stemmer, developed by Chris Paice, with the assistance of Gareth Husk

    This is based on the algorithm's description in :cite:`Paice:1990`.
    """

    _rule_table = {
        6: {'ifiabl': (False, 6, None, True), 'plicat': (False, 4, 'y', True)},
        5: {
            'guish': (False, 5, 'ct', True),
            'sumpt': (False, 2, None, True),
            'istry': (False, 5, None, True),
        },
        4: {
            'ytic': (False, 3, 's', True),
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
            'sist': (False, 0, None, True),
        },
        3: {
            'ied': (False, 3, 'y', False),
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
            'acy': (False, 3, None, False),
        },
        2: {
            'ia': (True, 2, None, True),
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
            'yz': (False, 1, 's', True),
        },
        1: {
            'a': (True, 1, None, True),
            'e': (False, 1, None, False),
            'i': ((True, 1, None, True), (False, 1, 'y', False)),
            'j': (False, 1, 's', True),
            's': ((True, 1, None, False), (False, 0, None, True)),
        },
    }

    def _has_vowel(self, word):
        for char in word:
            if char in {'a', 'e', 'i', 'o', 'u', 'y'}:
                return True
        return False

    def _acceptable(self, word):
        if word and word[0] in {'a', 'e', 'i', 'o', 'u'}:
            return len(word) > 1
        return len(word) > 2 and self._has_vowel(word[1:])

    def _apply_rule(self, word, rule, intact, terminate):
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

        if self._acceptable(word):
            return word, True, False, set_terminate
        else:
            return old_word, False, intact, terminate

    def stem(self, word):
        """Return Paice-Husk stem.

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
        >>> stmr = PaiceHusk()
        >>> stmr.stem('assumption')
        'assum'
        >>> stmr.stem('verifiable')
        'ver'
        >>> stmr.stem('fancies')
        'fant'
        >>> stmr.stem('fanciful')
        'fancy'
        >>> stmr.stem('torment')
        'tor'

        """
        terminate = False
        intact = True
        while not terminate:
            for n in range(6, 0, -1):
                if word[-n:] in self._rule_table[n]:
                    accept = False
                    if len(self._rule_table[n][word[-n:]]) < 4:
                        for rule in self._rule_table[n][word[-n:]]:
                            (
                                word,
                                accept,
                                intact,
                                terminate,
                            ) = self._apply_rule(word, rule, intact, terminate)
                            if accept:
                                break
                    else:
                        rule = self._rule_table[n][word[-n:]]
                        (word, accept, intact, terminate) = self._apply_rule(
                            word, rule, intact, terminate
                        )

                    if accept:
                        break
            else:
                break

        return word


def paice_husk(word):
    """Return Paice-Husk stem.

    This is a wrapper for :py:meth:`PaiceHusk.stem`.

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
    return PaiceHusk().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
