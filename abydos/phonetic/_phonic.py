# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.phonetic._phonic.

Phonic
"""

from ._phonetic import _Phonetic

__all__ = ['PHONIC']


class PHONIC(_Phonetic):
    """PHONIC code.

    PHONIC is a Soundex-like algorithm defined in :cite:`Taft:1970`.


    .. versionadded:: 0.4.1
    """

    _trans2 = {
        'CH': '6',
        'SH': '6',
        'PH': '8',
        'CE': '0',
        'CI': '0',
        'CY': '0',
    }

    _trans1 = {
        'D': '1',
        'T': '1',
        'N': '2',
        'M': '3',
        'R': '4',
        'L': '5',
        'J': '6',
        'C': '7',
        'K': '7',
        'G': '7',
        'Q': '7',
        'X': '7',
        'F': '8',
        'V': '8',
        'B': '9',
        'P': '9',
        'S': '0',
        'Z': '0',
    }

    _alphabetic = dict(zip((ord(_) for _ in '0123456789'), 'STNMRLJKFP'))

    def __init__(self, max_length=5, zero_pad=True, extended=False):
        """Initialize PHONIC instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 5)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string
        extended : bool
            If True, this uses Taft's 'Extended PHONIC coding' mode, which
            simply omits the first character of the code.


        .. versionadded:: 0.4.1

        """
        # Require a max_length of at least 5 and not more than 64
        if max_length != -1:
            self._max_length = min(max(5, max_length), 64)
        else:
            self._max_length = 64

        self._zero_pad = zero_pad
        self._extended = extended

    def encode_alpha(self, word):
        """Return the alphabetic PHONIC code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic PHONIC value

        Examples
        --------
        >>> pe = PHONIC()
        >>> pe.encode_alpha('Christopher')
        'JRSTF'
        >>> pe.encode_alpha('Niall')
        'NL'
        >>> pe.encode_alpha('Smith')
        'SMT'
        >>> pe.encode_alpha('Schmidt')
        'SJMT'


        .. versionadded:: 0.4.1

        """
        save_pad = self._zero_pad
        save_ext = self._extended
        self._zero_pad = False
        self._extended = True
        code = self.encode(word)
        self._zero_pad = save_pad
        self._extended = save_ext
        return code.translate(self._alphabetic)

    def encode(self, word):
        """Return the PHONIC code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The PHONIC code

        Examples
        --------
        >>> pe = PHONIC()
        >>> pe.encode('Christopher')
        'C6401'
        >>> pe.encode('Niall')
        'N2500'
        >>> pe.encode('Smith')
        'S0310'
        >>> pe.encode('Schmidt')
        'S0631'


        .. versionadded:: 0.4.1

        """
        # uppercase
        word = word.upper()

        code = []
        pos = 0
        while pos < len(word):
            if word[pos : pos + 2] in self._trans2:
                code.append(self._trans2[word[pos : pos + 2]])
                pos += 1
            elif word[pos] in self._trans1:
                code.append(self._trans1[word[pos]])
            else:
                code.append('.')
            pos += 1

        code = ''.join(code)
        code = self._delete_consecutive_repeats(code)
        code = code.replace('.', '')

        if self._zero_pad:
            code += '0' * (self._max_length - 1 - len(code))

        if not self._extended:
            code = word[:1] + code

        return code[: self._max_length]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
