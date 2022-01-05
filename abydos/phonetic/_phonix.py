# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.phonetic._phonix.

Phonix
"""

from typing import Any, Optional, Set, Tuple
from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['Phonix']


class Phonix(_Phonetic):
    """Phonix code.

    Phonix is a Soundex-like algorithm defined in :cite:`Gadd:1990`.

    This implementation is based on:
    - :cite:`Pfeifer:2000`
    - :cite:`Christen:2011`
    - :cite:`Kollar:2007`

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230720022455012683070808',
        )
    )

    _alphabetic = dict(zip((ord(_) for _ in '012345678'), 'APKTLNRFS'))

    def __init__(self, max_length: int = 4, zero_pad: bool = True) -> None:
        """Initialize Phonix instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string


        .. versionadded:: 0.3.6

        """
        self._uc_c_set = super()._uc_set - super()._uc_v_set

        self._substitutions = (
            (3, 'DG', 'G'),
            (3, 'CO', 'KO'),
            (3, 'CA', 'KA'),
            (3, 'CU', 'KU'),
            (3, 'CY', 'SI'),
            (3, 'CI', 'SI'),
            (3, 'CE', 'SE'),
            (0, 'CL', 'KL', super()._uc_v_set),
            (3, 'CK', 'K'),
            (1, 'GC', 'K'),
            (1, 'JC', 'K'),
            (0, 'CHR', 'KR', super()._uc_v_set),
            (0, 'CR', 'KR', super()._uc_v_set),
            (0, 'WR', 'R'),
            (3, 'NC', 'NK'),
            (3, 'CT', 'KT'),
            (3, 'PH', 'F'),
            (3, 'AA', 'AR'),
            (3, 'SCH', 'SH'),
            (3, 'BTL', 'TL'),
            (3, 'GHT', 'T'),
            (3, 'AUGH', 'ARF'),
            (
                2,
                'LJ',
                'LD',
                super()._uc_v_set,
                super()._uc_v_set,
            ),
            (3, 'LOUGH', 'LOW'),
            (0, 'Q', 'KW'),
            (0, 'KN', 'N'),
            (1, 'GN', 'N'),
            (3, 'GHN', 'N'),
            (1, 'GNE', 'N'),
            (3, 'GHNE', 'NE'),
            (1, 'GNES', 'NS'),
            (0, 'GN', 'N'),
            (2, 'GN', 'N', None, self._uc_c_set),
            (1, 'GN', 'N'),
            (0, 'PS', 'S'),
            (0, 'PT', 'T'),
            (0, 'CZ', 'C'),
            (2, 'WZ', 'Z', super()._uc_v_set),
            (2, 'CZ', 'CH'),
            (3, 'LZ', 'LSH'),
            (3, 'RZ', 'RSH'),
            (2, 'Z', 'S', None, super()._uc_v_set),
            (3, 'ZZ', 'TS'),
            (2, 'Z', 'TS', self._uc_c_set),
            (3, 'HROUG', 'REW'),
            (3, 'OUGH', 'OF'),
            (
                2,
                'Q',
                'KW',
                super()._uc_v_set,
                super()._uc_v_set,
            ),
            (
                2,
                'J',
                'Y',
                super()._uc_v_set,
                super()._uc_v_set,
            ),
            (0, 'YJ', 'Y', super()._uc_v_set),
            (0, 'GH', 'G'),
            (1, 'GH', 'E', super()._uc_v_set),
            (0, 'CY', 'S'),
            (3, 'NX', 'NKS'),
            (0, 'PF', 'F'),
            (1, 'DT', 'T'),
            (1, 'TL', 'TIL'),
            (1, 'DL', 'DIL'),
            (3, 'YTH', 'ITH'),
            (0, 'TJ', 'CH', super()._uc_v_set),
            (0, 'TSJ', 'CH', super()._uc_v_set),
            (0, 'TS', 'T', super()._uc_v_set),
            (3, 'TCH', 'CH'),
            (2, 'WSK', 'VSKIE', super()._uc_v_set),
            (1, 'WSK', 'VSKIE', super()._uc_v_set),
            (0, 'MN', 'N', super()._uc_v_set),
            (0, 'PN', 'N', super()._uc_v_set),
            (2, 'STL', 'SL', super()._uc_v_set),
            (1, 'STL', 'SL', super()._uc_v_set),
            (1, 'TNT', 'ENT'),
            (1, 'EAUX', 'OH'),
            (3, 'EXCI', 'ECS'),
            (3, 'X', 'ECS'),
            (1, 'NED', 'ND'),
            (3, 'JR', 'DR'),
            (1, 'EE', 'EA'),
            (3, 'ZS', 'S'),
            (2, 'R', 'AH', super()._uc_v_set, self._uc_c_set),
            (1, 'R', 'AH', super()._uc_v_set),
            (2, 'HR', 'AH', super()._uc_v_set, self._uc_c_set),
            (1, 'HR', 'AH', super()._uc_v_set),
            (1, 'HR', 'AH', super()._uc_v_set),
            (1, 'RE', 'AR'),
            (1, 'R', 'AH', super()._uc_v_set),
            (3, 'LLE', 'LE'),
            (1, 'LE', 'ILE', self._uc_c_set),
            (1, 'LES', 'ILES', self._uc_c_set),
            (1, 'E', ''),
            (1, 'ES', 'S'),
            (1, 'SS', 'AS', super()._uc_v_set),
            (1, 'MB', 'M', super()._uc_v_set),
            (3, 'MPTS', 'MPS'),
            (3, 'MPS', 'MS'),
            (3, 'MPT', 'MT'),
        )  # type: Tuple[Tuple[Any, ...], ...]

        # Clamp max_length to [4, 64]
        if max_length != -1:
            self._max_length = min(max(4, max_length), 64)
        else:
            self._max_length = 64

        self._zero_pad = zero_pad

    def encode_alpha(self, word: str) -> str:
        """Return the alphabetic Phonix code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Phonix value

        Examples
        --------
        >>> pe = Phonix()
        >>> pe.encode_alpha('Christopher')
        'KRST'
        >>> pe.encode_alpha('Niall')
        'NL'
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Schmidt')
        'SNT'


        .. versionadded:: 0.4.0

        """
        code = self.encode(word).rstrip('0')
        return code[:1] + code[1:].translate(self._alphabetic)

    def encode(self, word: str) -> str:
        """Return the Phonix code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Phonix value

        Examples
        --------
        >>> pe = Phonix()
        >>> pe.encode('Christopher')
        'K683'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Schmidt')
        'S530'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """

        def _start_repl(
            word: str, src: str, tar: str, post: Optional[Set[str]] = None
        ) -> str:
            """Replace src with tar at the start of word.

            Parameters
            ----------
            word : str
                The word to modify
            src : str
                Substring to match
            tar : str
                Substring to substitute
            post : set
                Following characters

            Returns
            -------
            str
                Modified string

            .. versionadded:: 0.1.0

            """
            if post:
                for i in post:
                    if word.startswith(src + i):
                        return tar + word[len(src) :]
            elif word.startswith(src):
                return tar + word[len(src) :]
            return word

        def _end_repl(
            word: str, src: str, tar: str, pre: Optional[Set[str]] = None
        ) -> str:
            """Replace src with tar at the end of word.

            Parameters
            ----------
            word : str
                The word to modify
            src : str
                Substring to match
            tar : str
                Substring to substitute
            pre : set
                Preceding characters

            Returns
            -------
            str
                Modified string

            .. versionadded:: 0.1.0

            """
            if pre:
                for i in pre:
                    if word.endswith(i + src):
                        return word[: -len(src)] + tar
            elif word.endswith(src):
                return word[: -len(src)] + tar
            return word

        def _mid_repl(
            word: str,
            src: str,
            tar: str,
            pre: Optional[Set[str]] = None,
            post: Optional[Set[str]] = None,
        ) -> str:
            """Replace src with tar in the middle of word.

            Parameters
            ----------
            word : str
                The word to modify
            src : str
                Substring to match
            tar : str
                Substring to substitute
            pre : set
                Preceding characters
            post : set
                Following characters

            Returns
            -------
            str
                Modified string

            .. versionadded:: 0.1.0

            """
            if pre or post:
                if not pre:
                    return word[0] + _all_repl(word[1:], src, tar, pre, post)
                elif not post:
                    return _all_repl(word[:-1], src, tar, pre, post) + word[-1]
                return _all_repl(word, src, tar, pre, post)
            return (
                word[0] + _all_repl(word[1:-1], src, tar, pre, post) + word[-1]
            )

        def _all_repl(
            word: str,
            src: str,
            tar: str,
            pre: Optional[Set[str]] = None,
            post: Optional[Set[str]] = None,
        ) -> str:
            """Replace src with tar anywhere in word.

            Parameters
            ----------
            word : str
                The word to modify
            src : str
                Substring to match
            tar : str
                Substring to substitute
            pre : set
                Preceding characters
            post : set
                Following characters

            Returns
            -------
            str
                Modified string

            .. versionadded:: 0.1.0

            """
            if pre or post:
                post = post if post else {''}
                pre = pre if pre else {''}

                for i, j in ((i, j) for i in pre for j in post):
                    word = word.replace(i + src + j, i + tar + j)
                return word
            else:
                return word.replace(src, tar)

        repl_at = (_start_repl, _end_repl, _mid_repl, _all_repl)

        sdx = ''

        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)
        if word:
            for trans in self._substitutions:
                word = repl_at[trans[0]](word, *trans[1:])
            if word[0] in self._uc_vy_set:
                sdx = f'v{word[1:].translate(self._trans)}'
            else:
                sdx = word[0] + word[1:].translate(self._trans)
            sdx = self._delete_consecutive_repeats(sdx)
            sdx = sdx.replace('0', '')

        if self._zero_pad:
            sdx += '0' * self._max_length
        if not sdx:
            sdx = '0'
        return sdx[: self._max_length]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
