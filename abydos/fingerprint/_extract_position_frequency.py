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

"""abydos.fingerprint._extract_position_frequence.

Taft's extract - position & frequency coding
"""

from ._fingerprint import _Fingerprint

__all__ = ['ExtractPositionFrequency']


class ExtractPositionFrequency(_Fingerprint):
    """Extract - Position & Frequency fingerprint.

    Based on the extract - position & frequency coding from :cite:`Taft:1970`.

    .. versionadded:: 0.4.1
    """

    _frequency = {
        x: y
        for x, y in zip(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            (
                5,
                1,
                5,
                0,
                7,
                1,
                2,
                5,
                6,
                0,
                1,
                5,
                1,
                3,
                4,
                3,
                0,
                4,
                5,
                3,
                4,
                1,
                1,
                0,
                2,
                1,
            ),
        )
    }
    _position = (0, 1, 2, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7)

    def fingerprint(self, word):
        """Return the extract - position & frequency coding.

        Parameters
        ----------
        word : str
            The word to fingerprint

        Returns
        -------
        int
            The extract - position & frequency coding

        Examples
        --------
        >>> fp = ExtractPositionFrequency()
        >>> fp.fingerprint('hat')
        'HAT'
        >>> fp.fingerprint('niall')
        'NILL'
        >>> fp.fingerprint('colin')
        'COLN'
        >>> fp.fingerprint('atcg')
        'ATCG'
        >>> fp.fingerprint('entreatment')
        'NMNT'


        .. versionadded:: 0.4.1

        """
        # uppercase & reverse
        word = [_ for _ in word.upper() if _ in self._frequency]
        scores = [[] for _ in range(len(word))]

        pos = 0
        for i in range(len(word)):
            scores[pos].append(self._frequency[word[pos]])
            scores[pos][0] += self._position[min(i, 15)]
            scores[pos].append(len(word) + pos if pos < 0 else pos)
            pos = -(pos if pos < 0 else pos + 1)
        positions = sorted(pos[1] for pos in sorted(scores, reverse=True)[-4:])

        return ''.join(word[_] for _ in positions)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
