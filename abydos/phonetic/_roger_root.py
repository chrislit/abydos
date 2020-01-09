# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.phonetic._roger_root.

Roger Root phonetic algorithm
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['RogerRoot', 'roger_root']


class RogerRoot(_Phonetic):
    """Roger Root code.

    This is Roger Root name coding, described in :cite:`Moore:1977`.

    .. versionadded:: 0.3.6
    """

    # '*' is used to prevent combining by _delete_consecutive_repeats()
    _init_patterns = {
        4: {'TSCH': '06'},
        3: {'TSH': '06', 'SCH': '06'},
        2: {
            'CE': '0*0',
            'CH': '06',
            'CI': '0*0',
            'CY': '0*0',
            'DG': '07',
            'GF': '08',
            'GM': '03',
            'GN': '02',
            'KN': '02',
            'PF': '08',
            'PH': '08',
            'PN': '02',
            'SH': '06',
            'TS': '0*0',
            'WR': '04',
        },
        1: {
            'A': '1',
            'B': '09',
            'C': '07',
            'D': '01',
            'E': '1',
            'F': '08',
            'G': '07',
            'H': '2',
            'I': '1',
            'J': '3',
            'K': '07',
            'L': '05',
            'M': '03',
            'N': '02',
            'O': '1',
            'P': '09',
            'Q': '07',
            'R': '04',
            'S': '0*0',
            'T': '01',
            'U': '1',
            'V': '08',
            'W': '4',
            'X': '07',
            'Y': '5',
            'Z': '0*0',
        },
    }

    _med_patterns = {
        4: {'TSCH': '6'},
        3: {'TSH': '6', 'SCH': '6'},
        2: {
            'CE': '0',
            'CH': '6',
            'CI': '0',
            'CY': '0',
            'DG': '7',
            'PH': '8',
            'SH': '6',
            'TS': '0',
        },
        1: {
            'B': '9',
            'C': '7',
            'D': '1',
            'F': '8',
            'G': '7',
            'J': '6',
            'K': '7',
            'L': '5',
            'M': '3',
            'N': '2',
            'P': '9',
            'Q': '7',
            'R': '4',
            'S': '0',
            'T': '1',
            'V': '8',
            'X': '7',
            'Z': '0',
            'A': '*',
            'E': '*',
            'H': '*',
            'I': '*',
            'O': '*',
            'U': '*',
            'W': '*',
            'Y': '*',
        },
    }

    _alphabetic_initial = dict(zip((ord(_) for _ in '012345'), ' AHJWY'))
    _alphabetic = dict(zip((ord(_) for _ in '0123456789'), 'STNMRLJKFP'))

    def __init__(self, max_length=5, zero_pad=True):
        """Initialize RogerRoot instance.

        Parameters
        ----------
        max_length : int
            The maximum length (default 5) of the code to return
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length
        self._zero_pad = zero_pad

    def encode_alpha(self, word):
        """Return the alphabetic Roger Root code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Roger Root code

        Examples
        --------
        >>> pe = RogerRoot()
        >>> pe.encode_alpha('Christopher')
        'JRST'
        >>> pe.encode_alpha('Niall')
        'NL'
        >>> pe.encode_alpha('Smith')
        'SMT'
        >>> pe.encode_alpha('Schmidt')
        'JMT'


        .. versionadded:: 0.4.0

        """
        code = self.encode(word).rstrip('0')
        return code[:1].translate(self._alphabetic_initial).strip() + code[
            1:
        ].translate(self._alphabetic)

    def encode(self, word):
        """Return the Roger Root code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Roger Root code

        Examples
        --------
        >>> pe = RogerRoot()
        >>> pe.encode('Christopher')
        '06401'
        >>> pe.encode('Niall')
        '02500'
        >>> pe.encode('Smith')
        '00310'
        >>> pe.encode('Schmidt')
        '06310'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)

        code = ''
        pos = 0

        # Do first digit(s) first
        for num in range(4, 0, -1):
            if word[:num] in self._init_patterns[num]:
                code = self._init_patterns[num][word[:num]]
                pos += num
                break

        # Then code subsequent digits
        while pos < len(word):
            for num in range(4, 0, -1):  # pragma: no branch
                if word[pos : pos + num] in self._med_patterns[num]:
                    code += self._med_patterns[num][word[pos : pos + num]]
                    pos += num
                    break

        code = self._delete_consecutive_repeats(code)
        code = code.replace('*', '')

        if self._zero_pad:
            code += '0' * self._max_length

        return code[: self._max_length]


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the RogerRoot.encode method instead.',
)
def roger_root(word, max_length=5, zero_pad=True):
    """Return the Roger Root code for a word.

    This is a wrapper for :py:meth:`RogerRoot.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The maximum length (default 5) of the code to return
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The Roger Root code

    Examples
    --------
    >>> roger_root('Christopher')
    '06401'
    >>> roger_root('Niall')
    '02500'
    >>> roger_root('Smith')
    '00310'
    >>> roger_root('Schmidt')
    '06310'

    .. versionadded:: 0.3.0

    """
    return RogerRoot(max_length, zero_pad).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
