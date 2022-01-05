# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.distance._rouge_w.

Rouge-W similarity
"""

from typing import Any, Callable, Optional, cast

from numpy import int_ as np_int
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['RougeW']


class RougeW(_Distance):
    r"""Rouge-W similarity.

    Rouge-W similarity :cite:`Lin:2004`

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        f_func: Optional[Callable[[float], float]] = None,
        f_inv: Optional[Callable[[float], float]] = None,
        **kwargs: Any
    ) -> None:
        """Initialize RougeW instance.

        Parameters
        ----------
        f_func : function
            A weighting function based on the value supplied to this function,
            such that f(x+y) > f(x) + f(y)
        f_inv : function
            The close form inverse of f_func
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super().__init__(**kwargs)

        if f_func is not None:
            self._f_func = f_func  # type: Callable[[float], float]
        else:
            self._f_func = RougeW._square  # noqa: SF01

        if f_inv is not None:
            self._f_inv = f_inv  # type: Callable[[float], float]
        else:
            self._f_inv = RougeW._sqrt  # noqa: SF01

    @staticmethod
    def _square(n: float) -> float:
        return float(n * n)

    @staticmethod
    def _sqrt(n: float) -> float:
        return n ** 0.5

    def wlcs(self, src: str, tar: str) -> float:
        """Return the Rouge-W weighted longest common sub-sequence length.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int (may return a float if cost has float values)
            The Levenshtein distance between src & tar

        Examples
        --------
        >>> cmp = RougeW()
        >>> cmp.wlcs('cat', 'hat')
        4
        >>> cmp.wlcs('Niall', 'Neil')
        3
        >>> cmp.wlcs('aluminum', 'Catalan')
        5
        >>> cmp.wlcs('ATCG', 'TAGC')
        3

        .. versionadded:: 0.4.0

        """
        src_len = len(src)
        tar_len = len(tar)

        if src == tar:
            return self._f_func(len(src))
        if not src:
            return 0
        if not tar:
            return 0

        c_mat = np_zeros((src_len, tar_len), dtype=np_int)
        w_mat = np_zeros((src_len, tar_len), dtype=np_int)

        for i in range(src_len):
            for j in range(tar_len):
                if src[i] == tar[j]:
                    k = w_mat[i - 1, j - 1]
                    c_mat[i, j] = (
                        c_mat[i - 1, j - 1]
                        + self._f_func(k + 1)
                        - self._f_func(k)
                    )
                    w_mat[i, j] = k + 1
                else:
                    if c_mat[i - 1, j] > c_mat[i, j - 1]:
                        c_mat[i, j] = c_mat[i - 1, j]
                        w_mat[i, j] = 0
                    else:
                        c_mat[i, j] = c_mat[i, j - 1]
                        w_mat[i, j] = 0

        return cast(float, c_mat[src_len - 1, tar_len - 1])

    def sim(self, src: str, tar: str, beta: float = 8) -> float:
        """Return the Rouge-W similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        beta : int or float
            A weighting factor to prejudice similarity towards src

        Returns
        -------
        float
            Rouge-W similarity

        Examples
        --------
        >>> cmp = RougeW()
        >>> cmp.sim('cat', 'hat')
        0.6666666666666666
        >>> cmp.sim('Niall', 'Neil')
        0.34747932867894143
        >>> cmp.sim('aluminum', 'Catalan')
        0.280047049205176
        >>> cmp.sim('ATCG', 'TAGC')
        0.43301270189221935


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        wlcs = self.wlcs(src, tar)
        r_wlcs = self._f_inv(wlcs / self._f_func(len(src)))
        p_wlcs = self._f_inv(wlcs / self._f_func(len(tar)))
        beta_sq = beta * beta

        if r_wlcs and p_wlcs:
            return (
                (1 + beta_sq) * r_wlcs * p_wlcs / (r_wlcs + beta_sq * p_wlcs)
            )
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
