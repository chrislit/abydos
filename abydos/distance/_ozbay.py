# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.distance._ozbay.

Ozbay metric
"""

from . import Jaccard, LCSstr, Levenshtein
from ._distance import _Distance
from ..tokenizer import QGrams

__all__ = ['Ozbay']


class Ozbay(_Distance):
    """Ozbay metric.

    The Ozbay metric :cite:`Ozbay:2015` is a string distance measure developed
    by Hakan Ozbay, which combines Jaccard distance, Levenshtein distance, and
    longest common substring distance.

    The normalized variant should be considered experimental.

    .. versionadded:: 0.4.0

    """

    _lev = Levenshtein()
    _jac = Jaccard(tokenizer=QGrams(qval=1, start_stop='', scaler='set'))
    _lcs = LCSstr()

    def dist_abs(self, src, tar):
        """Return the Ozbay metric.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Ozbay metric

        Examples
        --------
        >>> cmp = Ozbay()
        >>> round(cmp.dist_abs('cat', 'hat'), 12)
        0.75
        >>> round(cmp.dist_abs('Niall', 'Neil'), 12)
        6.0
        >>> round(cmp.dist_abs('Colin', 'Cuilen'), 12)
        7.714285714286
        >>> cmp.dist_abs('ATCG', 'TAGC')
        3.0


        .. versionadded:: 0.4.0

        """
        lev_dist = self._lev.dist_abs(src, tar)
        lev_metric = 0.0 if lev_dist == 0 else lev_dist / len(src)
        jac_metric = self._jac.dist_abs(src, tar)
        lcs_metric = self._lcs.sim(src, tar)

        if jac_metric == 1.0:
            ozbay_metric = lev_dist
        elif jac_metric == 0.0:
            ozbay_metric = lev_metric
        else:
            ozbay_metric = jac_metric * lev_dist

        if lcs_metric > 0.0:
            ozbay_metric /= lcs_metric
        else:
            ozbay_metric *= min(len(src), len(tar))

        return ozbay_metric

    def dist(self, src, tar):
        """Return the normalized Ozbay distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Ozbay distance

        Examples
        --------
        >>> cmp = Ozbay()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.027777777778
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.24
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.214285714286
        >>> cmp.dist('ATCG', 'TAGC')
        0.140625


        .. versionadded:: 0.4.0

        """
        dist = self.dist_abs(src, tar)
        if dist:
            return dist / (len(src) * len(tar) / self._lcs.dist(src, tar))
        return dist


if __name__ == '__main__':
    import doctest

    doctest.testmod()
