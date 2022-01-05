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

"""abydos.distance._bisim.

BI-SIM similarity
"""

from typing import Any, cast

from numpy import float_ as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['BISIM']


class BISIM(_Distance):
    r"""BI-SIM similarity.

    BI-SIM similarity :cite:`Kondrak:2003` is an n-gram based, edit-distance
    derived similarity measure.

    .. versionadded:: 0.4.0
    """

    def __init__(self, qval: int = 2, **kwargs: Any) -> None:
        """Initialize BISIM instance.

        Parameters
        ----------
        qval : int
            The number of characters to consider in each n-gram (q-gram). By
            default this is 2, hence BI-SIM. But TRI-SIM can be calculated by
            setting this to 3.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super().__init__(**kwargs)
        self._qval = qval

    def sim(self, src: str, tar: str) -> float:
        """Return the BI-SIM similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            BI-SIM similarity

        Examples
        --------
        >>> cmp = BISIM()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.4
        >>> cmp.sim('aluminum', 'Catalan')
        0.3125
        >>> cmp.sim('ATCG', 'TAGC')
        0.375


        .. versionadded:: 0.4.0

        """
        src_len = len(src)
        tar_len = len(tar)

        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        def _id(src_pos: int, tar_pos: int) -> float:
            s = 0
            for i in range(self._qval):
                s += int(src[src_pos + i] == tar[tar_pos + i])
            return s / self._qval

        src = src[0].swapcase() * (self._qval - 1) + src
        tar = tar[0].swapcase() * (self._qval - 1) + tar

        d_mat = np_zeros((src_len + 1, tar_len + 1), dtype=np_float)

        for i in range(1, src_len + 1):
            for j in range(1, tar_len + 1):
                d_mat[i, j] = max(
                    d_mat[i - 1, j - 1] + _id(i - 1, j - 1),  # sub/==
                    d_mat[i - 1, j],  # ins
                    d_mat[i, j - 1],  # del
                )
        return cast(float, d_mat[src_len, tar_len]) / max(src_len, tar_len)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
