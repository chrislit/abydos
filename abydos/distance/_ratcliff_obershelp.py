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

"""abydos.distance._ratcliff_obershelp.

Ratcliff-Obershelp similarity
"""

from typing import Tuple

from numpy import int_ as np_int
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['RatcliffObershelp']


class RatcliffObershelp(_Distance):
    """Ratcliff-Obershelp similarity.

    This follows the Ratcliff-Obershelp algorithm :cite:`Ratcliff:1988` to
    derive a similarity measure:

        1. Find the length of the longest common substring in src & tar.
        2. Recurse on the strings to the left & right of each this substring
           in src & tar. The base case is a 0 length common substring, in which
           case, return 0. Otherwise, return the sum of the current longest
           common substring and the left & right recursed sums.
        3. Multiply this length by 2 and divide by the sum of the lengths of
           src & tar.

    Cf.
    http://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970

    .. versionadded:: 0.3.6
    """

    def sim(self, src: str, tar: str) -> float:
        """Return the Ratcliff-Obershelp similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Ratcliff-Obershelp similarity

        Examples
        --------
        >>> cmp = RatcliffObershelp()
        >>> round(cmp.sim('cat', 'hat'), 12)
        0.666666666667
        >>> round(cmp.sim('Niall', 'Neil'), 12)
        0.666666666667
        >>> round(cmp.sim('aluminum', 'Catalan'), 12)
        0.4
        >>> cmp.sim('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """

        def _lcsstr_stl(src: str, tar: str) -> Tuple[int, int, int]:
            """Return start positions & length for Ratcliff-Obershelp.

            Parameters
            ----------
            src : str
                Source string for comparison
            tar : str
            Target string for comparison

            Returns
            -------
            tuple
                The start position in the source string, start position in the
                target string, and length of the longest common substring of
                strings src and tar.

            .. versionadded:: 0.1.0

            """
            lengths = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
            longest, src_longest, tar_longest = 0, 0, 0
            for i in range(1, len(src) + 1):
                for j in range(1, len(tar) + 1):
                    if src[i - 1] == tar[j - 1]:
                        lengths[i, j] = lengths[i - 1, j - 1] + 1
                        if lengths[i, j] > longest:
                            longest = lengths[i, j]
                            src_longest = i
                            tar_longest = j
                    else:
                        lengths[i, j] = 0
            return src_longest - longest, tar_longest - longest, longest

        def _sstr_matches(src: str, tar: str) -> int:
            """Return the sum of substring match lengths.

            This follows the Ratcliff-Obershelp algorithm
            :cite:`Ratcliff:1988`:
                 1. Find the length of the longest common substring in src &
                     tar.
                 2. Recurse on the strings to the left & right of each this
                     substring in src & tar.
                 3. Base case is a 0 length common substring, in which case,
                     return 0.
                 4. Return the sum.

            Parameters
            ----------
            src : str
                Source string for comparison
            tar : str
                Target string for comparison

            Returns
            -------
            int
                Sum of substring match lengths

            .. versionadded:: 0.1.0

            """
            src_start, tar_start, length = _lcsstr_stl(src, tar)
            if length == 0:
                return 0
            return (
                _sstr_matches(src[:src_start], tar[:tar_start])
                + length
                + _sstr_matches(
                    src[src_start + length :], tar[tar_start + length :]
                )
            )

        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0
        return 2 * _sstr_matches(src, tar) / (len(src) + len(tar))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
