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

"""abydos.distance._lcsseq.

Longest common subsequence
"""

from typing import Any, Callable, List

from numpy import int_ as np_int
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['LCSseq']


class LCSseq(_Distance):
    """Longest common subsequence.

    Longest common subsequence (LCSseq) is the longest subsequence of
    characters that two strings have in common.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self, normalizer: Callable[[List[float]], float] = max, **kwargs: Any
    ) -> None:
        r"""Initialize LCSseq.

        Parameters
        ----------
        normalizer : function
            A normalization function for the normalized similarity & distance.
            By default, the max of the lengths of the input strings. If
            lambda x: sum(x)/2.0 is supplied, the normalization proposed in
            :cite:`Radev:2001` is used, i.e.
            :math:`\frac{2 \dot |LCS(src, tar)|}{|src| + |tar|}`.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super().__init__(**kwargs)
        self._normalizer = normalizer

    def lcsseq(self, src: str, tar: str) -> str:
        """Return the longest common subsequence of two strings.

        Based on the dynamic programming algorithm from
        http://rosettacode.org/wiki/Longest_common_subsequence
        :cite:`rosettacode:2018b`. This is licensed GFDL 1.2.

        Modifications include:
            conversion to a numpy array in place of a list of lists

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        str
            The longest common subsequence

        Examples
        --------
        >>> sseq = LCSseq()
        >>> sseq.lcsseq('cat', 'hat')
        'at'
        >>> sseq.lcsseq('Niall', 'Neil')
        'Nil'
        >>> sseq.lcsseq('aluminum', 'Catalan')
        'aln'
        >>> sseq.lcsseq('ATCG', 'TAGC')
        'AC'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        lengths = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)

        # row 0 and column 0 are initialized to 0 already
        for i, src_char in enumerate(src):
            for j, tar_char in enumerate(tar):
                if src_char == tar_char:
                    lengths[i + 1, j + 1] = lengths[i, j] + 1
                else:
                    lengths[i + 1, j + 1] = max(
                        lengths[i + 1, j], lengths[i, j + 1]
                    )

        # read the substring out from the matrix
        result = ''
        i, j = len(src), len(tar)
        while i != 0 and j != 0:
            if lengths[i, j] == lengths[i - 1, j]:
                i -= 1
            elif lengths[i, j] == lengths[i, j - 1]:
                j -= 1
            else:
                result = src[i - 1] + result
                i -= 1
                j -= 1
        return result

    def sim(self, src: str, tar: str) -> float:
        r"""Return the longest common subsequence similarity of two strings.

        Longest common subsequence similarity (:math:`sim_{LCSseq}`).

        This employs the LCSseq function to derive a similarity metric:
        :math:`sim_{LCSseq}(s,t) = \frac{|LCSseq(s,t)|}{max(|s|, |t|)}`

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            LCSseq similarity

        Examples
        --------
        >>> sseq = LCSseq()
        >>> sseq.sim('cat', 'hat')
        0.6666666666666666
        >>> sseq.sim('Niall', 'Neil')
        0.6
        >>> sseq.sim('aluminum', 'Catalan')
        0.375
        >>> sseq.sim('ATCG', 'TAGC')
        0.5

        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class
        .. versionchanged:: 0.4.0
            Added normalization option

        """
        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0
        return len(self.lcsseq(src, tar)) / self._normalizer(
            [len(src), len(tar)]
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
