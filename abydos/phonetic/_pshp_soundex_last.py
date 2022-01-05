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

"""abydos.phonetic._pshp_soundex_last.

PSHP Soundex/Viewex Coding for last names
"""

from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['PSHPSoundexLast']


class PSHPSoundexLast(_Phonetic):
    """PSHP Soundex/Viewex Coding of a last name.

    This coding is based on :cite:`Hershberg:1976`.

    Reference was also made to the German version of the same:
    :cite:`Hershberg:1979`.

    A separate function, :py:class:`PSHPSoundexFirst` is used for first names.

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230120022455012523010202',
        )
    )

    _alphabetic = dict(zip((ord(_) for _ in '12345'), 'PKTLN'))

    def __init__(self, max_length: int = 4, german: bool = False) -> None:
        """Initialize PSHPSoundexLast instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 4)
        german : bool
            Set to True if the name is German (different rules apply)


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length
        self._german = german

    def encode_alpha(self, lname: str) -> str:
        """Calculate the alphabetic PSHP Soundex/Viewex Coding of a last name.

        Parameters
        ----------
        lname : str
            The last name to encode

        Returns
        -------
        str
            The PSHP alphabetic Soundex/Viewex Coding

        Examples
        --------
        >>> pe = PSHPSoundexLast()
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Waters')
        'WTN'
        >>> pe.encode_alpha('James')
        'JN'
        >>> pe.encode_alpha('Schmidt')
        'SNT'
        >>> pe.encode_alpha('Ashcroft')
        'AKKN'


        .. versionadded:: 0.4.0

        """
        code = self.encode(lname).rstrip('0')
        return code[:1] + code[1:].translate(self._alphabetic)

    def encode(self, lname: str) -> str:
        """Calculate the PSHP Soundex/Viewex Coding of a last name.

        Parameters
        ----------
        lname : str
            The last name to encode

        Returns
        -------
        str
            The PSHP Soundex/Viewex Coding

        Examples
        --------
        >>> pe = PSHPSoundexLast()
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Waters')
        'W350'
        >>> pe.encode('James')
        'J500'
        >>> pe.encode('Schmidt')
        'S530'
        >>> pe.encode('Ashcroft')
        'A225'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        lname = unicode_normalize('NFKD', lname.upper())
        lname = ''.join(c for c in lname if c in self._uc_set)

        # A. Prefix treatment
        if lname[:3] == 'VON' or lname[:3] == 'VAN':
            lname = lname[3:].strip()

        # The rule implemented below says "MC, MAC become 1". I believe it
        # meant to say they become M except in German data (where superscripted
        # 1 indicates "except in German data"). It doesn't make sense for them
        # to become 1 (BPFV -> 1) or to apply outside German. Unfortunately,
        # both articles have this error(?).
        if not self._german:
            if lname[:3] == 'MAC':
                lname = f'M{lname[3:]}'
            elif lname[:2] == 'MC':
                lname = f'M{lname[2:]}'

        # The non-German-only rule to strip ' is unnecessary due to filtering

        if lname[:1] in {'E', 'I', 'O', 'U'}:
            lname = f'A{lname[1:]}'
        elif lname[:2] in {'GE', 'GI', 'GY'}:
            lname = f'J{lname[1:]}'
        elif lname[:2] in {'CE', 'CI', 'CY'}:
            lname = f'S{lname[1:]}'
        elif lname[:3] == 'CHR':
            lname = f'K{lname[1:]}'
        elif lname[:1] == 'C' and lname[:2] != 'CH':
            lname = f'K{lname[1:]}'

        if lname[:2] == 'KN':
            lname = f'N{lname[1:]}'
        elif lname[:2] == 'PH':
            lname = f'F{lname[1:]}'
        elif lname[:3] in {'WIE', 'WEI'}:
            lname = f'V{lname[1:]}'

        if self._german and lname[:1] in {'W', 'M', 'Y', 'Z'}:
            lname = {'W': 'V', 'M': 'N', 'Y': 'J', 'Z': 'S'}[lname[0]] + lname[
                1:
            ]

        code = lname[:1]

        # B. Postfix treatment
        if self._german:  # moved from end of postfix treatment due to blocking
            if lname[-3:] == 'TES':
                lname = lname[:-3]
            elif lname[-2:] == 'TS':
                lname = lname[:-2]
            if lname[-3:] == 'TZE':
                lname = lname[:-3]
            elif lname[-2:] == 'ZE':
                lname = lname[:-2]
            if lname[-1:] == 'Z':
                lname = lname[:-1]
            elif lname[-2:] == 'TE':
                lname = lname[:-2]

        if lname[-1:] == 'R':
            lname = f'{lname[:-1]}N'
        elif lname[-2:] in {'SE', 'CE'}:
            lname = lname[:-2]
        if lname[-2:] == 'SS':
            lname = lname[:-2]
        elif lname[-1:] == 'S':
            lname = lname[:-1]

        if not self._german:
            l5_repl = {'STOWN': 'SAWON', 'MPSON': 'MASON'}
            l4_repl = {
                'NSEN': 'ASEN',
                'MSON': 'ASON',
                'STEN': 'SAEN',
                'STON': 'SAON',
            }
            if lname[-5:] in l5_repl:
                lname = lname[:-5] + l5_repl[lname[-5:]]
            elif lname[-4:] in l4_repl:
                lname = lname[:-4] + l4_repl[lname[-4:]]

        if lname[-2:] in {'NG', 'ND'}:
            lname = lname[:-1]
        if not self._german and lname[-3:] in {'GAN', 'GEN'}:
            lname = f'{lname[:-3]}A{lname[-2:]}'

        # C. Infix Treatment
        lname = lname.replace('CK', 'C')
        lname = lname.replace('SCH', 'S')
        lname = lname.replace('DT', 'T')
        lname = lname.replace('ND', 'N')
        lname = lname.replace('NG', 'N')
        lname = lname.replace('LM', 'M')
        lname = lname.replace('MN', 'M')
        lname = lname.replace('WIE', 'VIE')
        lname = lname.replace('WEI', 'VEI')

        # D. Soundexing
        # code for X & Y are unspecified, but presumably are 2 & 0

        lname = lname.translate(self._trans)
        lname = self._delete_consecutive_repeats(lname)

        code += lname[1:]
        code = code.replace('0', '')  # rule 1

        if self._max_length != -1:
            if len(code) < self._max_length:
                code += '0' * (self._max_length - len(code))
            else:
                code = code[: self._max_length]

        return code


if __name__ == '__main__':
    import doctest

    doctest.testmod()
