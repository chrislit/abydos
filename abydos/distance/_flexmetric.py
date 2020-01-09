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

"""abydos.distance._flexmetric.

FlexMetric distance
"""

from numpy import float as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['FlexMetric']


class FlexMetric(_Distance):
    r"""FlexMetric distance.

    FlexMetric distance :cite:`Kempken:2005`

    .. versionadded:: 0.4.0
    """

    def __init__(
        self, normalizer=max, indel_costs=None, subst_costs=None, **kwargs
    ):
        """Initialize FlexMetric instance.

        Parameters
        ----------
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
        indel_costs : list of tuples
            A list of insertion and deletion costs. Each list element should
            be a tuple consisting of an iterable (sets are best) and a float
            value. The iterable consists of those letters whose insertion
            or deletion has a cost equal to the float value.
        subst_costs : list of tuples
            A list of substitution costs. Each list element should
            be a tuple consisting of an iterable (sets are best) and a float
            value. The iterable consists of the letters in each letter class,
            which may be substituted for each other at cost equal to the float
            value.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(FlexMetric, self).__init__(**kwargs)
        self._normalizer = normalizer

        if indel_costs is None:
            self._indel_costs = [
                (frozenset('dtch'), 0.4),
                (frozenset('e'), 0.5),
                (frozenset('u'), 0.9),
                (frozenset('rpn'), 0.95),
            ]
        else:
            self._indel_costs = indel_costs

        def _get_second(s):
            return s[1]

        if subst_costs is None:
            self._subst_costs = [
                (frozenset('szß'), 0.1),
                (frozenset('dt'), 0.1),
                (frozenset('iy'), 0.1),
                (frozenset('ckq'), 0.1),
                (frozenset('eä'), 0.1),
                (frozenset('uüv'), 0.1),
                (frozenset('iü'), 0.1),
                (frozenset('fv'), 0.1),
                (frozenset('zc'), 0.1),
                (frozenset('ij'), 0.1),
                (frozenset('bp'), 0.1),
                (frozenset('eoö'), 0.2),
                (frozenset('aä'), 0.2),
                (frozenset('mbp'), 0.4),
                (frozenset('uw'), 0.4),
                (frozenset('uo'), 0.8),
                (frozenset('aeiouy'), 0.9),
            ]
        else:
            self._subst_costs = sorted(subst_costs, key=_get_second)

    def _cost(self, src, s_pos, tar, t_pos):
        if s_pos == -1:
            if t_pos > 0 and tar[t_pos - 1] == tar[t_pos]:
                return 0.0
            for letter_set in self._indel_costs:
                if tar[t_pos] in letter_set[0]:
                    return letter_set[1]
            else:
                return 1.0
        elif t_pos == -1:
            if s_pos > 0 and src[s_pos - 1] == src[s_pos]:
                return 0.0
            for letter_set in self._indel_costs:
                if src[s_pos] in letter_set[0]:
                    return letter_set[1]
            else:
                return 1.0
        for letter_set in self._subst_costs:
            if src[s_pos] in letter_set[0] and tar[t_pos] in letter_set[0]:
                return letter_set[1]
        else:
            return 1.0

    def dist_abs(self, src, tar):
        """Return the FlexMetric distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            FlexMetric distance

        Examples
        --------
        >>> cmp = FlexMetric()
        >>> cmp.dist_abs('cat', 'hat')
        0.8
        >>> cmp.dist_abs('Niall', 'Neil')
        1.5
        >>> cmp.dist_abs('aluminum', 'Catalan')
        6.7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.1999999999999997


        .. versionadded:: 0.4.0

        """
        src_len = len(src)
        tar_len = len(tar)

        if src == tar:
            return 0
        if not src:
            return sum(self._cost('', -1, tar, j) for j in range(len(tar)))
        if not tar:
            return sum(self._cost(src, i, '', -1) for i in range(len(src)))

        d_mat = np_zeros((src_len + 1, tar_len + 1), dtype=np_float)
        for i in range(1, src_len + 1):
            d_mat[i, 0] = d_mat[i - 1, 0] + self._cost(src, i - 1, '', -1)
        for j in range(1, tar_len + 1):
            d_mat[0, j] = d_mat[0, j - 1] + self._cost('', -1, tar, j - 1)

        src_lc = src.lower()
        tar_lc = tar.lower()

        for i in range(src_len):
            for j in range(tar_len):
                d_mat[i + 1, j + 1] = min(
                    d_mat[i + 1, j] + self._cost('', -1, tar_lc, j),  # ins
                    d_mat[i, j + 1] + self._cost(src_lc, i, '', -1),  # del
                    d_mat[i, j]
                    + (
                        self._cost(src_lc, i, tar_lc, j)
                        if src[i] != tar[j]
                        else 0
                    ),  # sub/==
                )

        return d_mat[src_len, tar_len]

    def dist(self, src, tar):
        """Return the normalized FlexMetric distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized FlexMetric distance

        Examples
        --------
        >>> cmp = FlexMetric()
        >>> cmp.dist('cat', 'hat')
        0.26666666666666666
        >>> cmp.dist('Niall', 'Neil')
        0.3
        >>> cmp.dist('aluminum', 'Catalan')
        0.8375
        >>> cmp.dist('ATCG', 'TAGC')
        0.5499999999999999


        .. versionadded:: 0.4.0

        """
        score = self.dist_abs(src, tar)
        if score:
            return score / self._normalizer([len(src), len(tar)])
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
