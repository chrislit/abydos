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

"""abydos.phonetic._pshp_soundex_first.

PSHP Soundex/Viewex Coding for first names
"""

from unicodedata import normalize as unicode_normalize

from ._phonetic import _Phonetic

__all__ = ['PSHPSoundexFirst']


class PSHPSoundexFirst(_Phonetic):
    """PSHP Soundex/Viewex Coding of a first name.

    This coding is based on :cite:`Hershberg:1976`.

    Reference was also made to the German version of the same:
    :cite:`Hershberg:1979`.

    A separate class, :py:class:`PSHPSoundexLast` is used for last names.

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
        """Initialize PSHPSoundexFirst instance.

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

    def encode_alpha(self, fname: str) -> str:
        """Calculate the alphabetic PSHP Soundex/Viewex Coding of a first name.

        Parameters
        ----------
        fname : str
            The first name to encode

        Returns
        -------
        str
            The alphabetic PSHP Soundex/Viewex Coding

        Examples
        --------
        >>> pe = PSHPSoundexFirst()
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Waters')
        'WTNK'
        >>> pe.encode_alpha('James')
        'JN'
        >>> pe.encode_alpha('Schmidt')
        'SN'
        >>> pe.encode_alpha('Ashcroft')
        'AKK'
        >>> pe.encode_alpha('John')
        'JN'
        >>> pe.encode_alpha('Colin')
        'KL'
        >>> pe.encode_alpha('Niall')
        'NL'
        >>> pe.encode_alpha('Sally')
        'SL'
        >>> pe.encode_alpha('Jane')
        'JN'


        .. versionadded:: 0.4.0

        """
        code = self.encode(fname).rstrip('0')
        if code == 'J7':
            return 'JN'
        elif code == 'P7':
            return 'PT'
        return code[:1] + code[1:].translate(self._alphabetic)

    def encode(self, fname: str) -> str:
        """Calculate the PSHP Soundex/Viewex Coding of a first name.

        Parameters
        ----------
        fname : str
            The first name to encode

        Returns
        -------
        str
            The PSHP Soundex/Viewex Coding

        Examples
        --------
        >>> pe = PSHPSoundexFirst()
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Waters')
        'W352'
        >>> pe.encode('James')
        'J700'
        >>> pe.encode('Schmidt')
        'S500'
        >>> pe.encode('Ashcroft')
        'A220'
        >>> pe.encode('John')
        'J500'
        >>> pe.encode('Colin')
        'K400'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Sally')
        'S400'
        >>> pe.encode('Jane')
        'J500'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        fname = unicode_normalize('NFKD', fname.upper())
        fname = ''.join(c for c in fname if c in self._uc_set)

        # special rules
        if fname == 'JAMES':
            code = 'J7'
        elif fname == 'PAT':
            code = 'P7'

        else:
            # A. Prefix treatment
            if fname[:2] in {'GE', 'GI', 'GY'}:
                fname = f"J{fname[1:]}"
            elif fname[:2] in {'CE', 'CI', 'CY'}:
                fname = f"S{fname[1:]}"
            elif fname[:3] == 'CHR':
                fname = f"K{fname[1:]}"
            elif fname[:1] == 'C' and fname[:2] != 'CH':
                fname = f"K{fname[1:]}"

            if fname[:2] == 'KN':
                fname = f"N{fname[1:]}"
            elif fname[:2] == 'PH':
                fname = f"F{fname[1:]}"
            elif fname[:3] in {'WIE', 'WEI'}:
                fname = f"V{fname[1:]}"

            if self._german and fname[:1] in {'W', 'M', 'Y', 'Z'}:
                fname = {'W': 'V', 'M': 'N', 'Y': 'J', 'Z': 'S'}[
                    fname[0]
                ] + fname[1:]

            code = fname[:1]

            # B. Soundex coding
            # code for Y unspecified, but presumably is 0
            fname = fname.translate(self._trans)
            fname = self._delete_consecutive_repeats(fname)

            code += fname[1:]
            syl_ptr = code.find('0')
            syl2_ptr = code[syl_ptr + 1 :].find('0')
            if syl_ptr != -1 and syl2_ptr != -1 and syl2_ptr - syl_ptr > -1:
                code = code[: syl_ptr + 2]

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
