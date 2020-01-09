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

"""abydos.phonetic._spfc.

Standardized Phonetic Frequency Code (SPFC) algorithm
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['SPFC', 'spfc']


class SPFC(_Phonetic):
    """Standardized Phonetic Frequency Code (SPFC).

    Standardized Phonetic Frequency Code is roughly Soundex-like.
    This implementation is based on page 19-21 of :cite:`Moore:1977`.

    .. versionadded:: 0.3.6
    """

    _pf1 = dict(
        zip(
            (ord(_) for _ in 'SZCKQVFPUWABLORDHIEMNXGJT'),
            '0011112222334445556666777',
        )
    )
    _pf2 = dict(
        zip(
            (ord(_) for _ in 'SZCKQFPXABORDHIMNGJTUVWEL'),
            '0011122233445556677788899',
        )
    )
    _pf3 = dict(
        zip(
            (ord(_) for _ in 'BCKQVDTFLPGJXMNRSZAEHIOUWY'),
            '00000112223334456677777777',
        )
    )

    _substitutions = (
        ('DK', 'K'),
        ('DT', 'T'),
        ('SC', 'S'),
        ('KN', 'N'),
        ('MN', 'N'),
    )

    _pf1_alphabetic = dict(zip((ord(_) for _ in '01234567'), 'SCFALDEG'))
    _pf2_alphabetic = dict(zip((ord(_) for _ in '0123456789'), 'SCFAODMGUE'))
    _pf3_alphabetic = dict(zip((ord(_) for _ in '01234567'), 'BDFGMRSZ'))

    def encode_alpha(self, word):
        """Return the alphabetic SPFC of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic SPFC value

        Examples
        --------
        >>> pe = SPFC()
        >>> pe.encode_alpha('Christopher Smith')
        'SDCMS'
        >>> pe.encode_alpha('Christopher Schmidt')
        'SDCMS'
        >>> pe.encode_alpha('Niall Smith')
        'SDMMS'
        >>> pe.encode_alpha('Niall Schmidt')
        'SDMMS'

        >>> pe.encode_alpha('L.Smith')
        'SDEMS'
        >>> pe.encode_alpha('R.Miller')
        'EROES'

        >>> pe.encode_alpha(('L', 'Smith'))
        'SDEMS'
        >>> pe.encode_alpha(('R', 'Miller'))
        'EROES'


        .. versionadded:: 0.4.0

        """
        code = self.encode(word)

        return (
            code[:1].translate(self._pf1_alphabetic)
            + code[1:2].translate(self._pf3_alphabetic)
            + code[2:].translate(self._pf2_alphabetic)
        )

    def encode(self, word):
        """Return the Standardized Phonetic Frequency Code (SPFC) of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The SPFC value

        Raises
        ------
        AttributeError
            Word attribute must be a string with a space or period dividing the
            first and last names or a tuple/list consisting of the first and
            last names

        Examples
        --------
        >>> pe = SPFC()
        >>> pe.encode('Christopher Smith')
        '01160'
        >>> pe.encode('Christopher Schmidt')
        '01160'
        >>> pe.encode('Niall Smith')
        '01660'
        >>> pe.encode('Niall Schmidt')
        '01660'

        >>> pe.encode('L.Smith')
        '01960'
        >>> pe.encode('R.Miller')
        '65490'

        >>> pe.encode(('L', 'Smith'))
        '01960'
        >>> pe.encode(('R', 'Miller'))
        '65490'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """

        def _raise_word_ex():
            """Raise an AttributeError.

            Raises
            ------
            AttributeError
                Word attribute must be a string with a space or period dividing
                the first and last names or a tuple/list consisting of the
                first and last names

            .. versionadded:: 0.1.0

            """
            raise AttributeError(
                'Word attribute must be a string with a space or period '
                + 'dividing the first and last names or a tuple/list '
                + 'consisting of the first and last names'
            )

        if not word:
            return ''

        names = []
        if isinstance(word, str):
            names = word.split('.', 1)
            if len(names) != 2:
                names = word.split(' ', 1)
                if len(names) != 2:
                    _raise_word_ex()
        elif hasattr(word, '__iter__'):
            if len(word) != 2:
                _raise_word_ex()
            names = word
        else:
            _raise_word_ex()

        names = [unicode_normalize('NFKD', _.strip().upper()) for _ in names]
        code = ''

        def _steps_one_to_three(name):
            """Perform the first three steps of SPFC.

            Parameters
            ----------
            name : str
                Name to transform

            Returns
            -------
            str
                Transformed name

            .. versionadded:: 0.1.0

            """
            # filter out non A-Z
            name = ''.join(_ for _ in name if _ in self._uc_set)

            # 1. In the field, convert DK to K, DT to T, SC to S, KN to N,
            # and MN to N
            for subst in self._substitutions:
                name = name.replace(subst[0], subst[1])

            # 2. In the name field, replace multiple letters with a single
            # letter
            name = self._delete_consecutive_repeats(name)

            # 3. Remove vowels, W, H, and Y, but keep the first letter in the
            # name field.
            if name:
                name = name[0] + ''.join(
                    _
                    for _ in name[1:]
                    if _ not in {'A', 'E', 'H', 'I', 'O', 'U', 'W', 'Y'}
                )
            return name

        names = [_steps_one_to_three(_) for _ in names]

        # 4. The first digit of the code is obtained using PF1 and the first
        # letter of the name field. Remove this letter after coding.
        if names[1]:
            code += names[1][0].translate(self._pf1)
            names[1] = names[1][1:]

        # 5. Using the last letters of the name, use Table PF3 to obtain the
        # second digit of the code. Use as many letters as possible and remove
        # after coding.
        if names[1]:
            if names[1][-3:] in {'DRS', 'STN', 'PRS', 'STR'}:
                code += '7'
                names[1] = names[1][:-3]
            elif names[1][-2:] in {'MN', 'TR', 'SN', 'SR', 'TN', 'TD'}:
                code += '7'
                names[1] = names[1][:-2]
            else:
                code += names[1][-1].translate(self._pf3)
                names[1] = names[1][:-1]

        # 6. The third digit is found using Table PF2 and the first character
        # of the first name. Remove after coding.
        if names[0]:
            code += names[0][0].translate(self._pf2)
            names[0] = names[0][1:]

        # 7. The fourth digit is found using Table PF2 and the first character
        # of the name field. If no letters remain use zero. After coding remove
        # the letter.
        # 8. The fifth digit is found in the same manner as the fourth using
        # the remaining characters of the name field if any.
        for _ in range(2):
            if names[1]:
                code += names[1][0].translate(self._pf2)
                names[1] = names[1][1:]
            else:
                code += '0'

        return code


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the SPFC.encode method instead.',
)
def spfc(word):
    """Return the Standardized Phonetic Frequency Code (SPFC) of a word.

    This is a wrapper for :py:meth:`SPFC.encode`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    str
        The SPFC value

    Examples
    --------
    >>> spfc('Christopher Smith')
    '01160'
    >>> spfc('Christopher Schmidt')
    '01160'
    >>> spfc('Niall Smith')
    '01660'
    >>> spfc('Niall Schmidt')
    '01660'

    >>> spfc('L.Smith')
    '01960'
    >>> spfc('R.Miller')
    '65490'

    >>> spfc(('L', 'Smith'))
    '01960'
    >>> spfc(('R', 'Miller'))
    '65490'

    .. versionadded:: 0.1.0

    """
    return SPFC().encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
