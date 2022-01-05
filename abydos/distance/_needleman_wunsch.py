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

"""abydos.distance._needleman_wunsch.

Needleman-Wunsch score
"""

from typing import Any, Callable, Dict, Optional, Tuple, cast

from numpy import float_ as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['NeedlemanWunsch']


class NeedlemanWunsch(_Distance):
    """Needleman-Wunsch score.

    The Needleman-Wunsch score :cite:`Needleman:1970` is a standard edit
    distance measure.


    .. versionadded:: 0.3.6
    """

    @staticmethod
    def sim_matrix(
        src: str,
        tar: str,
        mat: Optional[Dict[Tuple[str, str], int]] = None,
        mismatch_cost: float = 0,
        match_cost: float = 1,
        symmetric: bool = True,
        alphabet: Optional[str] = None,
    ) -> float:
        """Return the matrix similarity of two strings.

        With the default parameters, this is identical to sim_ident.
        It is possible for sim_matrix to return values outside of the range
        :math:`[0, 1]`, if values outside that range are present in mat,
        mismatch_cost, or match_cost.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        mat : dict
            A dict mapping tuples to costs; the tuples are (src, tar) pairs of
            symbols from the alphabet parameter
        mismatch_cost : float
            The value returned if (src, tar) is absent from mat when src does
            not equal tar
        match_cost : float
            The value returned if (src, tar) is absent from mat when src equals
            tar
        symmetric : bool
            True if the cost of src not matching tar is identical to the cost
            of tar not matching src; in this case, the values in mat need only
            contain (src, tar) or (tar, src), not both
        alphabet : str
            A collection of tokens from which src and tar are drawn; if this is
            defined a ValueError is raised if either tar or src have symbols not
            found in alphabet

        Returns
        -------
        float
            Matrix similarity

        Raises
        ------
        ValueError
            src value not in alphabet
        ValueError
            tar value not in alphabet

        Examples
        --------
        >>> NeedlemanWunsch.sim_matrix('cat', 'hat')
        0
        >>> NeedlemanWunsch.sim_matrix('hat', 'hat')
        1


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if alphabet:
            alpha_set = set(alphabet)
            for i in src:
                if i not in alpha_set:
                    raise ValueError('src value not in alphabet')
            for i in tar:
                if i not in alpha_set:
                    raise ValueError('tar value not in alphabet')

        if src == tar:
            if mat and (src, src) in mat:
                return mat[(src, src)]
            return match_cost
        if mat and (src, tar) in mat:
            return mat[(src, tar)]
        elif symmetric and mat and (tar, src) in mat:
            return mat[(tar, src)]
        return mismatch_cost

    def __init__(
        self,
        gap_cost: float = 1,
        sim_func: Optional[Callable[[str, str], float]] = None,
        **kwargs: Any
    ) -> None:
        """Initialize NeedlemanWunsch instance.

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
        super().__init__(**kwargs)
        self._gap_cost = gap_cost
        self._sim_func = cast(
            Callable[[str, str], float],
            NeedlemanWunsch.sim_matrix if sim_func is None else sim_func,
        )  # type: Callable[[str, str], float]

    def sim_score(self, src: str, tar: str) -> float:
        """Return the Needleman-Wunsch score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Needleman-Wunsch score

        Examples
        --------
        >>> cmp = NeedlemanWunsch()
        >>> cmp.sim_score('cat', 'hat')
        2.0
        >>> cmp.sim_score('Niall', 'Neil')
        1.0
        >>> cmp.sim_score('aluminum', 'Catalan')
        -1.0
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float)

        for i in range(len(src) + 1):
            d_mat[i, 0] = -(i * self._gap_cost)
        for j in range(len(tar) + 1):
            d_mat[0, j] = -(j * self._gap_cost)
        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                match = d_mat[i - 1, j - 1] + self._sim_func(
                    src[i - 1], tar[j - 1]
                )
                delete = d_mat[i - 1, j] - self._gap_cost
                insert = d_mat[i, j - 1] - self._gap_cost
                d_mat[i, j] = max(match, delete, insert)
        return cast(float, d_mat[d_mat.shape[0] - 1, d_mat.shape[1] - 1])

    def sim(self, src: str, tar: str) -> float:
        """Return the normalized Needleman-Wunsch score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Needleman-Wunsch score

        Examples
        --------
        >>> cmp = NeedlemanWunsch()
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
