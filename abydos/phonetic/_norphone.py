# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.phonetic._norphone.

Norphone
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


from ._phonetic import _Phonetic

__all__ = ['Norphone', 'norphone']


class Norphone(_Phonetic):
    """Norphone.

    The reference implementation by Lars Marius Garshol is available in
    :cite:`Garshol:2015`.

    Norphone was designed for Norwegian, but this implementation has been
    extended to support Swedish vowels as well. This function incorporates
    the "not implemented" rules from the above file's rule set.
    """

    _uc_v_set = {'A', 'E', 'I', 'O', 'U', 'Y', 'Å', 'Æ', 'Ø', 'Ä', 'Ö'}

    _replacements = {
        4: {'SKEI': 'X'},
        3: {'SKJ': 'X', 'KEI': 'X'},
        2: {
            'CH': 'K',
            'CK': 'K',
            'GJ': 'J',
            'GH': 'K',
            'HG': 'K',
            'HJ': 'J',
            'HL': 'L',
            'HR': 'R',
            'KJ': 'X',
            'KI': 'X',
            'LD': 'L',
            'ND': 'N',
            'PH': 'F',
            'TH': 'T',
            'SJ': 'X',
        },
        1: {'W': 'V', 'X': 'KS', 'Z': 'S', 'D': 'T', 'G': 'K'},
    }

    def encode(self, word):
        """Return the Norphone code.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Norphone code

        Examples
        --------
        >>> pe = Norphone()
        >>> pe.encode('Hansen')
        'HNSN'
        >>> pe.encode('Larsen')
        'LRSN'
        >>> pe.encode('Aagaard')
        'ÅKRT'
        >>> pe.encode('Braaten')
        'BRTN'
        >>> pe.encode('Sandvik')
        'SNVK'

        """
        word = word.upper()

        code = ''
        skip = 0

        if word[0:2] == 'AA':
            code = 'Å'
            skip = 2
        elif word[0:2] == 'GI':
            code = 'J'
            skip = 2
        elif word[0:3] == 'SKY':
            code = 'X'
            skip = 3
        elif word[0:2] == 'EI':
            code = 'Æ'
            skip = 2
        elif word[0:2] == 'KY':
            code = 'X'
            skip = 2
        elif word[:1] == 'C':
            code = 'K'
            skip = 1
        elif word[:1] == 'Ä':
            code = 'Æ'
            skip = 1
        elif word[:1] == 'Ö':
            code = 'Ø'
            skip = 1

        if word[-2:] == 'DT':
            word = word[:-2] + 'T'
        # Though the rules indicate this rule applies in all positions, the
        # reference implementation indicates it applies only in final position.
        elif word[-2:-1] in self._uc_v_set and word[-1:] == 'D':
            word = word[:-2]

        for pos, char in enumerate(word):
            if skip:
                skip -= 1
            else:
                for length in sorted(self._replacements, reverse=True):
                    if word[pos : pos + length] in self._replacements[length]:
                        code += self._replacements[length][
                            word[pos : pos + length]
                        ]
                        skip = length - 1
                        break
                else:
                    if not pos or char not in self._uc_v_set:
                        code += char

        code = self._delete_consecutive_repeats(code)

        return code


def norphone(word):
    """Return the Norphone code.

    This is a wrapper for :py:meth:`Norphone.encode`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    str
        The Norphone code

    Examples
    --------
    >>> norphone('Hansen')
    'HNSN'
    >>> norphone('Larsen')
    'LRSN'
    >>> norphone('Aagaard')
    'ÅKRT'
    >>> norphone('Braaten')
    'BRTN'
    >>> norphone('Sandvik')
    'SNVK'

    """
    return Norphone().encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
