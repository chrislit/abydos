# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.phonetic._parmar_kumbharana.

Parmar-Kumbharana phonetic algorithm
"""

from ._phonetic import _Phonetic

__all__ = ['ParmarKumbharana']


class ParmarKumbharana(_Phonetic):
    """Parmar-Kumbharana code.

    This is based on the phonetic algorithm proposed in :cite:`Parmar:2014`.

    .. versionadded:: 0.3.6
    """

    _rules = {
        4: {'OUGH': 'F'},
        3: {'DGE': 'J', 'OUL': 'U', 'GHT': 'T'},
        2: {
            'CE': 'S',
            'CI': 'S',
            'CY': 'S',
            'GE': 'J',
            'GI': 'J',
            'GY': 'J',
            'WR': 'R',
            'GN': 'N',
            'KN': 'N',
            'PN': 'N',
            'CK': 'K',
            'SH': 'S',
        },
    }
    _del_trans = {65: '', 69: '', 73: '', 79: '', 85: '', 89: ''}

    def encode(self, word: str) -> str:
        """Return the Parmar-Kumbharana encoding of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Parmar-Kumbharana encoding

        Examples
        --------
        >>> pe = ParmarKumbharana()
        >>> pe.encode('Gough')
        'GF'
        >>> pe.encode('pneuma')
        'NM'
        >>> pe.encode('knight')
        'NT'
        >>> pe.encode('trice')
        'TRS'
        >>> pe.encode('judge')
        'JJ'


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = word.upper()  # Rule 3
        word = self._delete_consecutive_repeats(word)  # Rule 4

        # Rule 5
        i = 0
        while i < len(word):
            for match_len in range(4, 1, -1):
                if word[i : i + match_len] in self._rules[match_len]:
                    repl = self._rules[match_len][word[i : i + match_len]]
                    word = word[:i] + repl + word[i + match_len :]
                    i += len(repl)
                    break
            else:
                i += 1

        word = word[:1] + word[1:].translate(self._del_trans)  # Rule 6
        return word


if __name__ == '__main__':
    import doctest

    doctest.testmod()
