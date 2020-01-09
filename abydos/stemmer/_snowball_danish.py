# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.stemmer._snowball_danish.

Snowball Danish stemmer
"""

from unicodedata import normalize

from deprecation import deprecated

from ._snowball import _Snowball
from .. import __version__

__all__ = ['SnowballDanish', 'sb_danish']


class SnowballDanish(_Snowball):
    """Snowball Danish stemmer.

    The Snowball Danish stemmer is defined at:
    http://snowball.tartarus.org/algorithms/danish/stemmer.html

    .. versionadded:: 0.3.6
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

    def stem(self, word):
        """Return Snowball Danish stem.

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
        >>> stmr = SnowballDanish()
        >>> stmr.stem('underviser')
        'undervis'
        >>> stmr.stem('suspension')
        'suspension'
        >>> stmr.stem('sikkerhed')
        'sikker'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', word.lower())

        r1_start = min(max(3, self._sb_r1(word)), len(word))

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
            if len(word) > 1 and word[-2] in self._s_endings:
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
            and word[-1] not in self._vowels
        ):
            word = word[:-1]

        return word


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the SnowballDanish.stem method instead.',
)
def sb_danish(word):
    """Return Snowball Danish stem.

    This is a wrapper for :py:meth:`SnowballDanish.stem`.

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
    >>> sb_danish('underviser')
    'undervis'
    >>> sb_danish('suspension')
    'suspension'
    >>> sb_danish('sikkerhed')
    'sikker'

    .. versionadded:: 0.1.0

    """
    return SnowballDanish().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
