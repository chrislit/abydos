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

"""abydos.stemmer._snowball_norwegian.

Snowball Norwegian stemmer
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize

from six import text_type

from ._snowball import _Snowball

__all__ = ['SnowballNorwegian', 'sb_norwegian']


class SnowballNorwegian(_Snowball):
    """Snowball Norwegian stemmer.

    The Snowball Norwegian stemmer is defined at:
    http://snowball.tartarus.org/algorithms/norwegian/stemmer.html
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

    def stem(self, word):
        """Return Snowball Norwegian stem.

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
        >>> stmr = SnowballNorwegian()
        >>> stmr.stem('lese')
        'les'
        >>> stmr.stem('suspensjon')
        'suspensjon'
        >>> stmr.stem('sikkerhet')
        'sikker'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))

        r1_start = min(max(3, self._sb_r1(word)), len(word))

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
            if (len(word) > 1 and word[-2] in self._s_endings) or (
                len(word) > 2
                and word[-2] == 'k'
                and word[-3] not in self._vowels
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


def sb_norwegian(word):
    """Return Snowball Norwegian stem.

    This is a wrapper for :py:meth:`SnowballNorwegian.stem`.

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
    >>> sb_norwegian('lese')
    'les'
    >>> sb_norwegian('suspensjon')
    'suspensjon'
    >>> sb_norwegian('sikkerhet')
    'sikker'

    """
    return SnowballNorwegian().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
