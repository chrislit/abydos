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

"""abydos.fingerprint._lc_cutter.

Library of Congress Cutter table encoding
"""

from ._fingerprint import _Fingerprint

__all__ = ['LCCutter']


class LCCutter(_Fingerprint):
    """Library of Congress Cutter table encoding.

    This is based on the Library of Congress Cutter table encoding scheme, as
    described at https://www.loc.gov/aba/pcc/053/table.html :cite:`LOC:2013`.
    Handling for numerals is not included.

    .. versionadded:: 0.4.1
    """

    _vowels = set('AEIOU')
    _after_initial_vowel = ['C', 'K', 'M', 'O', 'Q', 'R', 'T']
    _after_initial_s = ['C', 'D', 'G', 'L', 'S', 'T', 'U']
    _after_initial_qu = ['D', 'H', 'N', 'Q', 'S', 'X']
    _after_initial_cons = ['D', 'H', 'N', 'Q', 'T', 'X']

    _expansions = ['D', 'H', 'L', 'O', 'S', 'V']

    def __init__(self, max_length=64):
        """Initialize LCCutter instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 64)


        .. versionadded:: 0.4.1

        """
        # Require a max_length of at least 2 and not more than 64
        if max_length != -1:
            self._max_length = min(max(2, max_length), 64)
        else:
            self._max_length = 64

    def fingerprint(self, word):
        """Return the Library of Congress Cutter table encoding of a word.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        str
            The Library of Congress Cutter table encoding

        Examples
        --------
        >>> cf = LCCutter()
        >>> cf.fingerprint('hat')
        'H38'
        >>> cf.fingerprint('niall')
        'N5355'
        >>> cf.fingerprint('colin')
        'C6556'
        >>> cf.fingerprint('atcg')
        'A834'
        >>> cf.fingerprint('entreatment')
        'E5874386468'


        .. versionadded:: 0.4.1

        """
        # uppercase
        uc = ''.join(letter for letter in word.upper() if letter.isalpha())

        if not uc:
            return ''

        code = uc[0]

        # length 1
        if len(uc) == 1:
            return code

        # length 2+
        code = [code]

        # first cutter
        pos = 1
        if uc[0] in self._vowels:
            cval = 2
            for letter in self._after_initial_vowel:
                if uc[1] > letter:
                    cval += 1
                else:
                    break
        elif uc[0] == 'S':
            cval = 2
            for letter in self._after_initial_s:
                if uc[1] > letter:
                    cval += 1
                elif uc[1] == 'C' and uc[1:3] < 'CI':
                    cval += 1
                    pos += 1
                    break
                else:
                    break
        elif uc[0:2] == 'QU':
            cval = 3
            pos += 1
            for letter in self._after_initial_qu:
                if uc[2:3] > letter:
                    cval += 1
                else:
                    break
        elif 'QA' <= uc[0:2] <= 'QT':
            cval = 2
        else:
            cval = 3
            for letter in self._after_initial_cons:
                if uc[1] > letter:
                    cval += 1
                else:
                    break
        code.append(str(cval))

        # length 3+
        for ch in uc[pos + 1 :]:
            if len(code) >= self._max_length:
                break
            cval = 3
            for letter in self._expansions:
                if ch > letter:
                    cval += 1
                else:
                    break
            code.append(str(cval))

        return ''.join(code[: self._max_length])


if __name__ == '__main__':
    import doctest

    doctest.testmod()
