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

"""abydos.distance._lcsstr.

Longest common substring
"""

from typing import Any, Callable, List

from numpy import int_ as np_int
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['LCSstr']


class LCSstr(_Distance):
    """Longest common substring.

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

    def lcsstr(self, src: str, tar: str) -> str:
        """Return the longest common substring of two strings.

        Longest common substring (LCSstr).

        Based on the code from
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring
        :cite:`Wikibooks:2018`.
        This is licensed Creative Commons: Attribution-ShareAlike 3.0.

        Modifications include:

            - conversion to a numpy array in place of a list of lists

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        str
            The longest common substring

        Examples
        --------
        >>> sstr = LCSstr()
        >>> sstr.lcsstr('cat', 'hat')
        'at'
        >>> sstr.lcsstr('Niall', 'Neil')
        'N'
        >>> sstr.lcsstr('aluminum', 'Catalan')
        'al'
        >>> sstr.lcsstr('ATCG', 'TAGC')
        'A'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        lengths = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
        longest, i_longest = 0, 0
        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                if src[i - 1] == tar[j - 1]:
                    lengths[i, j] = lengths[i - 1, j - 1] + 1
                    if lengths[i, j] > longest:
                        longest = lengths[i, j]
                        i_longest = i
                else:
                    lengths[i, j] = 0
        return src[i_longest - longest : i_longest]

    def sim(self, src: str, tar: str) -> float:
        r"""Return the longest common substring similarity of two strings.

        Longest common substring similarity (:math:`sim_{LCSstr}`).

        This employs the LCS function to derive a similarity metric:
        :math:`sim_{LCSstr}(s,t) = \frac{|LCSstr(s,t)|}{max(|s|, |t|)}`

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            LCSstr similarity

        Examples
        --------
        >>> sstr = LCSstr()
        >>> sstr.sim('cat', 'hat')
        0.6666666666666666
        >>> sstr.sim('Niall', 'Neil')
        0.2
        >>> sstr.sim('aluminum', 'Catalan')
        0.25
        >>> sstr.sim('ATCG', 'TAGC')
        0.25


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
        return len(self.lcsstr(src, tar)) / self._normalizer(
            [len(src), len(tar)]
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
