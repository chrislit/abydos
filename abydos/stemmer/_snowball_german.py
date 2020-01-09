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

"""abydos.stemmer._snowball_german.

Snowball German stemmer
"""

from unicodedata import normalize

from deprecation import deprecated

from ._snowball import _Snowball
from .. import __version__

__all__ = ['SnowballGerman', 'sb_german']


class SnowballGerman(_Snowball):
    """Snowball German stemmer.

    The Snowball German stemmer is defined at:
    http://snowball.tartarus.org/algorithms/german/stemmer.html

    .. versionadded:: 0.3.6
    """

    _vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ö', 'ü'}
    _s_endings = {'b', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'r', 't'}
    _st_endings = {'b', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 't'}

    def __init__(self, alternate_vowels=False):
        """Initialize SnowballGerman instance.

        Parameters
        ----------
        alternate_vowels : bool
            Composes ae as ä, oe as ö, and ue as ü before running the algorithm


        .. versionadded:: 0.4.0

        """
        self._alternate_vowels = alternate_vowels

    def stem(self, word):
        """Return Snowball German stem.

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
        >>> stmr = SnowballGerman()
        >>> stmr.stem('lesen')
        'les'
        >>> stmr.stem('graues')
        'grau'
        >>> stmr.stem('buchstabieren')
        'buchstabi'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', word.lower())
        word = word.replace('ß', 'ss')

        if len(word) > 2:
            for i in range(2, len(word)):
                if word[i] in self._vowels and word[i - 2] in self._vowels:
                    if word[i - 1] == 'u':
                        word = word[: i - 1] + 'U' + word[i:]
                    elif word[i - 1] == 'y':
                        word = word[: i - 1] + 'Y' + word[i:]

        if self._alternate_vowels:
            word = word.replace('ae', 'ä')
            word = word.replace('oe', 'ö')
            word = word.replace('que', 'Q')
            word = word.replace('ue', 'ü')
            word = word.replace('Q', 'que')

        r1_start = max(3, self._sb_r1(word))
        r2_start = self._sb_r2(word)

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
                and word[-2] in self._s_endings
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
                and word[-3] in self._st_endings
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


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the SnowballGerman.stem method instead.',
)
def sb_german(word, alternate_vowels=False):
    """Return Snowball German stem.

    This is a wrapper for :py:meth:`SnowballGerman.stem`.

    Parameters
    ----------
    word : str
        The word to stem
    alternate_vowels : bool
        Composes ae as ä, oe as ö, and ue as ü before running the algorithm

    Returns
    -------
    str
        Word stem

    Examples
    --------
    >>> sb_german('lesen')
    'les'
    >>> sb_german('graues')
    'grau'
    >>> sb_german('buchstabieren')
    'buchstabi'

    .. versionadded:: 0.1.0

    """
    return SnowballGerman(alternate_vowels).stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
