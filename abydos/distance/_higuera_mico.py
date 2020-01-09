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

"""abydos.distance._higuera_mico.

The Higuera-Micó contextual normalized edit distance
"""

from numpy import full as np_full

from ._distance import _Distance

__all__ = ['HigueraMico']


class HigueraMico(_Distance):
    """The Higuera-Micó contextual normalized edit distance.

    This is presented in :cite:`Higuera:2008`.

    This measure is not normalized to a particular range. Indeed, for an
    string of infinite length as and a string of 0 length, the contextual
    normalized edit distance would be infinity. But so long as the relative
    difference in string lengths is not too great, the distance will generally
    remain below 1.0

    Notes
    -----
    The "normalized" version of this distance, implemented in the dist method
    is merely the minimum of the distance and 1.0.

    .. versionadded:: 0.4.0

    """

    def __init__(self, **kwargs):
        """Initialize Levenshtein instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(HigueraMico, self).__init__(**kwargs)

    def dist_abs(self, src, tar):
        """Return the Higuera-Micó distance between two strings.

        This is a straightforward implementation of Higuera & Micó pseudocode
        from :cite:`Higuera:2008`, ported to Numpy.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The Higuera-Micó distance between src & tar

        Examples
        --------
        >>> cmp = HigueraMico()
        >>> cmp.dist_abs('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist_abs('Niall', 'Neil')
        0.5333333333333333
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.7916666666666667
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.6000000000000001

        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        mx = np_full(
            (len(src) + 1, len(tar) + 1, len(src) + len(tar) + 1),
            fill_value=float('-inf'),
            dtype=float,
        )

        for i in range(1, len(src) + 1):
            mx[i, 0, i] = 0
        for j in range(len(tar) + 1):
            mx[0, j, j] = j
        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                if src[i - 1] == tar[j - 1]:
                    for k in range(len(src) + len(tar) + 1):
                        mx[i, j, k] = mx[i - 1, j - 1, k]
                else:
                    for k in range(1, len(src) + len(tar) + 1):
                        mx[i, j, k] = mx[i - 1, j - 1, k - 1]
                for k in range(1, len(src) + len(tar) + 1):
                    mx[i, j, k] = max(
                        mx[i - 1, j, k - 1],
                        mx[i, j - 1, k - 1] + 1,
                        mx[i, j, k],
                    )

        min_dist = float('inf')
        for k in range(len(src) + len(tar) + 1):
            if mx[len(src), len(tar), k] >= 0:
                n_i = int(mx[len(src), len(tar), k])
                n_d = len(src) - len(tar) + n_i
                n_s = k - (n_i + n_d)
                loc_dist = 0
                for i in range(len(src) + 1, len(src) + n_i + 1):
                    loc_dist += 1 / i
                loc_dist += n_s / (len(src) + n_i)
                for i in range(len(tar) + 1, len(tar) + n_d + 1):
                    loc_dist += 1 / i
                if loc_dist < min_dist:
                    min_dist = loc_dist

        return min_dist

    def dist(self, src, tar):
        """Return the bounded Higuera-Micó distance between two strings.

        This is the distance bounded to the range [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The bounded Higuera-Micó distance between src & tar

        Examples
        --------
        >>> cmp = HigueraMico()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.5333333333333333
        >>> cmp.dist('aluminum', 'Catalan')
        0.7916666666666667
        >>> cmp.dist('ATCG', 'TAGC')
        0.6000000000000001

        .. versionadded:: 0.4.0

        """
        return min(1.0, self.dist_abs(src, tar))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
