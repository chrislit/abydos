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

"""abydos.phonetic._dolby.

Dolby Code
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['Dolby', 'dolby']


class Dolby(_Phonetic):
    """Dolby Code.

    This follows "A Spelling Equivalent Abbreviation Algorithm For Personal
    Names" from :cite:`Dolby:1970` and :cite:`Cunningham:1969`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, max_length=-1, keep_vowels=False, vowel_char='*'):
        r"""Initialize Dolby instance.

        Parameters
        ----------
        max_length : int
            Maximum length of the returned Dolby code -- this also activates
            the fixed-length code mode if it is greater than 0
        keep_vowels : bool
            If True, retains all vowel markers
        vowel_char : str
            The vowel marker character (default to \*)


        .. versionadded:: 0.4.0

        """
        self._max_length = max_length
        self._keep_vowels = keep_vowels
        self._vowel_char = vowel_char

    def encode_alpha(self, word):
        """Return the alphabetic Dolby Code of a name.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Dolby Code

        Examples
        --------
        >>> pe = Dolby()
        >>> pe.encode_alpha('Hansen')
        'HANSN'
        >>> pe.encode_alpha('Larsen')
        'LARSN'
        >>> pe.encode_alpha('Aagaard')
        'AGR'
        >>> pe.encode_alpha('Braaten')
        'BRADN'
        >>> pe.encode_alpha('Sandvik')
        'SANVK'


        .. versionadded:: 0.4.0

        """
        return self.encode(word).replace(self._vowel_char, 'A')

    def encode(self, word):
        """Return the Dolby Code of a name.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Dolby Code

        Examples
        --------
        >>> pe = Dolby()
        >>> pe.encode('Hansen')
        'H*NSN'
        >>> pe.encode('Larsen')
        'L*RSN'
        >>> pe.encode('Aagaard')
        '*GR'
        >>> pe.encode('Braaten')
        'BR*DN'
        >>> pe.encode('Sandvik')
        'S*NVK'

        >>> pe_6 = Dolby(max_length=6)
        >>> pe_6.encode('Hansen')
        'H*NS*N'
        >>> pe_6.encode('Larsen')
        'L*RS*N'
        >>> pe_6.encode('Aagaard')
        '*G*R  '
        >>> pe_6.encode('Braaten')
        'BR*D*N'
        >>> pe_6.encode('Sandvik')
        'S*NF*K'

        >>> pe.encode('Smith')
        'SM*D'
        >>> pe.encode('Waters')
        'W*DRS'
        >>> pe.encode('James')
        'J*MS'
        >>> pe.encode('Schmidt')
        'SM*D'
        >>> pe.encode('Ashcroft')
        '*SKRFD'

        >>> pe_6.encode('Smith')
        'SM*D  '
        >>> pe_6.encode('Waters')
        'W*D*RS'
        >>> pe_6.encode('James')
        'J*M*S '
        >>> pe_6.encode('Schmidt')
        'SM*D  '
        >>> pe_6.encode('Ashcroft')
        '*SKRFD'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', word.upper())
        word = ''.join(c for c in word if c in self._uc_set)

        # Rule 1 (FL2)
        if word[:3] in {'MCG', 'MAG', 'MAC'}:
            word = 'MK' + word[3:]
        elif word[:2] == 'MC':
            word = 'MK' + word[2:]

        # Rule 2 (FL3)
        pos = len(word) - 2
        while pos > -1:
            if word[pos : pos + 2] in {
                'DT',
                'LD',
                'ND',
                'NT',
                'RC',
                'RD',
                'RT',
                'SC',
                'SK',
                'ST',
            }:
                word = word[: pos + 1] + word[pos + 2 :]
                pos += 1
            pos -= 1

        # Rule 3 (FL4)
        # Although the rule indicates "after the first letter", the test cases
        # make it clear that these apply to the first letter also.
        word = word.replace('X', 'KS')
        word = word.replace('CE', 'SE')
        word = word.replace('CI', 'SI')
        word = word.replace('CY', 'SI')

        # not in the rule set, but they seem to have intended it
        word = word.replace('TCH', 'CH')

        pos = word.find('CH', 1)
        while pos != -1:
            if word[pos - 1 : pos] not in self._uc_vy_set:
                word = word[:pos] + 'S' + word[pos + 1 :]
            pos = word.find('CH', pos + 1)

        word = word.replace('C', 'K')
        word = word.replace('Z', 'S')

        word = word.replace('WR', 'R')
        word = word.replace('DG', 'G')
        word = word.replace('QU', 'K')
        word = word.replace('T', 'D')
        word = word.replace('PH', 'F')

        # Rule 4 (FL5)
        # Although the rule indicates "after the first letter", the test cases
        # make it clear that these apply to the first letter also.
        pos = word.find('K', 0)
        while pos != -1:
            if pos > 1 and word[pos - 1 : pos] not in self._uc_vy_set | {
                'L',
                'N',
                'R',
            }:
                word = word[: pos - 1] + word[pos:]
                pos -= 1
            pos = word.find('K', pos + 1)

        # Rule FL6
        if self._max_length > 0 and word[-1:] == 'E':
            word = word[:-1]

        # Rule 5 (FL7)
        word = self._delete_consecutive_repeats(word)

        # Rule 6 (FL8)
        if word[:2] == 'PF':
            word = word[1:]
        if word[-2:] == 'PF':
            word = word[:-1]
        elif word[-2:] == 'GH':
            if word[-3:-2] in self._uc_vy_set:
                word = word[:-2] + 'F'
            else:
                word = word[:-2] + 'G'
        word = word.replace('GH', '')

        # Rule FL9
        if self._max_length > 0:
            word = word.replace('V', 'F')

        # Rules 7-9 (FL10-FL12)
        first = 1 + (1 if self._max_length > 0 else 0)
        code = ''
        for pos, char in enumerate(word):
            if char in self._uc_vy_set:
                if first or self._keep_vowels:
                    code += self._vowel_char
                    first -= 1
            elif pos > 0 and char in {'W', 'H'}:
                continue
            else:
                code += char

        if self._max_length > 0:
            # Rule FL13
            if len(code) > self._max_length and code[-1:] == 'S':
                code = code[:-1]
            if self._keep_vowels:
                code = code[: self._max_length]
            else:
                # Rule FL14
                code = code[: self._max_length + 2]
                # Rule FL15
                while len(code) > self._max_length:
                    vowels = len(code) - self._max_length
                    excess = vowels - 1
                    word = code
                    code = ''
                    for char in word:
                        if char == self._vowel_char:
                            if vowels:
                                code += char
                                vowels -= 1
                        else:
                            code += char
                    code = code[: self._max_length + excess]

            # Rule FL16
            code += ' ' * (self._max_length - len(code))

        return code


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Dolby.encode method instead.',
)
def dolby(word, max_length=-1, keep_vowels=False, vowel_char='*'):
    r"""Return the Dolby Code of a name.

    This is a wrapper for :py:meth:`Dolby.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        Maximum length of the returned Dolby code -- this also activates the
        fixed-length code mode if it is greater than 0
    keep_vowels : bool
        If True, retains all vowel markers
    vowel_char : str
        The vowel marker character (default to \*)

    Returns
    -------
    str
        The Dolby Code

    Examples
    --------
    >>> dolby('Hansen')
    'H*NSN'
    >>> dolby('Larsen')
    'L*RSN'
    >>> dolby('Aagaard')
    '*GR'
    >>> dolby('Braaten')
    'BR*DN'
    >>> dolby('Sandvik')
    'S*NVK'
    >>> dolby('Hansen', max_length=6)
    'H*NS*N'
    >>> dolby('Larsen', max_length=6)
    'L*RS*N'
    >>> dolby('Aagaard', max_length=6)
    '*G*R  '
    >>> dolby('Braaten', max_length=6)
    'BR*D*N'
    >>> dolby('Sandvik', max_length=6)
    'S*NF*K'

    >>> dolby('Smith')
    'SM*D'
    >>> dolby('Waters')
    'W*DRS'
    >>> dolby('James')
    'J*MS'
    >>> dolby('Schmidt')
    'SM*D'
    >>> dolby('Ashcroft')
    '*SKRFD'
    >>> dolby('Smith', max_length=6)
    'SM*D  '
    >>> dolby('Waters', max_length=6)
    'W*D*RS'
    >>> dolby('James', max_length=6)
    'J*M*S '
    >>> dolby('Schmidt', max_length=6)
    'SM*D  '
    >>> dolby('Ashcroft', max_length=6)
    '*SKRFD'

    .. versionadded:: 0.3.0

    """
    return Dolby(max_length, keep_vowels, vowel_char).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
