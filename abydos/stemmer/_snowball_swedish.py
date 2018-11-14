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

"""abydos.stemmer._snowball_swedish.

Snowball Swedish stemmer
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

__all__ = ['SnowballSwedish', 'sb_swedish']


class SnowballSwedish(_Snowball):
    """Snowball Swedish stemmer.

    The Snowball Swedish stemmer is defined at:
    http://snowball.tartarus.org/algorithms/swedish/stemmer.html
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

    def stem(self, word):
        """Return Snowball Swedish stem.

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
        >>> stmr = SnowballSwedish()
        >>> stmr.stem('undervisa')
        'undervis'
        >>> stmr.stem('suspension')
        'suspension'
        >>> stmr.stem('visshet')
        'viss'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))

        r1_start = min(max(3, self._sb_r1(word)), len(word))

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
            if len(word) > 1 and word[-2] in self._s_endings:
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


def sb_swedish(word):
    """Return Snowball Swedish stem.

    This is a wrapper for :py:meth:`SnowballSwedish.stem`.

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
    >>> sb_swedish('undervisa')
    'undervis'
    >>> sb_swedish('suspension')
    'suspension'
    >>> sb_swedish('visshet')
    'viss'

    """
    return SnowballSwedish().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
