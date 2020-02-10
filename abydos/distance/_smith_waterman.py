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

"""abydos.distance._smith_waterman.

Smith-Waterman score
"""

from typing import Any, Callable, Optional, cast

from numpy import float_ as np_float
from numpy import zeros as np_zeros

from ._needleman_wunsch import NeedlemanWunsch

__all__ = ['SmithWaterman']


class SmithWaterman(NeedlemanWunsch):
    """Smith-Waterman score.

    The Smith-Waterman score :cite:`Smith:1981` is a standard edit distance
    measure, differing from Needleman-Wunsch in that it focuses on local
    alignment and disallows negative scores.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self,
        gap_cost: float = 1.0,
        sim_func: Optional[Callable[[str, str], float]] = None,
        **kwargs: Any
    ) -> None:
        """Initialize SmithWaterman instance.

        Parameters
        ----------
        gap_cost : float
            The cost of an alignment gap (1 by default)
        sim_func : function
            A function that returns the similarity of two characters (identity
            similarity by default)
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(SmithWaterman, self).__init__(**kwargs)
        self._gap_cost = gap_cost
        self._sim_func = cast(
            Callable[[str, str], float],
            NeedlemanWunsch.sim_matrix if sim_func is None else sim_func,
        )  # type: Callable[[str, str], float]

    def sim_score(self, src: str, tar: str) -> float:
        """Return the Smith-Waterman score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Smith-Waterman score

        Examples
        --------
        >>> cmp = SmithWaterman()
        >>> cmp.sim_score('cat', 'hat')
        2.0
        >>> cmp.sim_score('Niall', 'Neil')
        1.0
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.0
        >>> cmp.sim_score('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float)

        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                match = d_mat[i - 1, j - 1] + self._sim_func(
                    src[i - 1], tar[j - 1]
                )
                delete = d_mat[i - 1, j] - self._gap_cost
                insert = d_mat[i, j - 1] - self._gap_cost
                d_mat[i, j] = max(0, match, delete, insert)
        return cast(float, d_mat[d_mat.shape[0] - 1, d_mat.shape[1] - 1])

    def sim(self, src: str, tar: str) -> float:
        """Return the normalized Smith-Waterman score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Smith-Waterman score

        Examples
        --------
        >>> cmp = SmithWaterman()
        >>> cmp.sim('cat', 'hat')
        0.6666666666666667
        >>> cmp.sim('Niall', 'Neil')
        0.22360679774997896
        >>> round(cmp.sim('aluminum', 'Catalan'), 12)
        0.0
        >>> cmp.sim('cat', 'hat')
        0.6666666666666667


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0
        return max(0.0, self.sim_score(src, tar)) / (
            self.sim_score(src, src) ** 0.5 * self.sim_score(tar, tar) ** 0.5
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
