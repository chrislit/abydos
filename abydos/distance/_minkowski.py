# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.distance._minkowski.

Minkowski distance & similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from numbers import Number

from ._token_distance import _TokenDistance

__all__ = ['Minkowski', 'dist_minkowski', 'minkowski', 'sim_minkowski']


class Minkowski(_TokenDistance):
    """Minkowski distance.

    The Minkowski distance :cite:`Minkowski:1910` is a distance metric in
    :math:`L^p-space`.
    """

    def dist_abs(
        self, src, tar, qval=2, pval=1, normalized=False, alphabet=None
    ):
        """Return the Minkowski distance (:math:`L^p`-norm) of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version
        pval : int or float
            The :math:`p`-value of the :math:`L^p`-space
        normalized : bool
            Normalizes to [0, 1] if True
        alphabet : collection or int
            The values or size of the alphabet

        Returns
        -------
        float
            The Minkowski distance

        Examples
        --------
        >>> cmp = Minkowski()
        >>> cmp.dist_abs('cat', 'hat')
        4.0
        >>> cmp.dist_abs('Niall', 'Neil')
        7.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        9.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        10.0

        """
        q_src, q_tar = self._get_qgrams(src, tar, qval)
        diffs = ((q_src - q_tar) + (q_tar - q_src)).values()

        normalizer = 1
        if normalized:
            totals = (q_src + q_tar).values()
            if alphabet is not None:
                # noinspection PyTypeChecker
                normalizer = (
                    alphabet if isinstance(alphabet, Number) else len(alphabet)
                )
            elif pval == 0:
                normalizer = len(totals)
            else:
                normalizer = sum(_ ** pval for _ in totals) ** (1 / pval)

        if len(diffs) == 0:
            return 0.0
        if pval == float('inf'):
            # Chebyshev distance
            return max(diffs) / normalizer
        if pval == 0:
            # This is the l_0 "norm" as developed by David Donoho
            return len(diffs) / normalizer
        return sum(_ ** pval for _ in diffs) ** (1 / pval) / normalizer

    def dist(self, src, tar, qval=2, pval=1, alphabet=None):
        """Return normalized Minkowski distance of two strings.

        The normalized Minkowski distance :cite:`Minkowski:1910` is a distance
        metric in :math:`L^p`-space, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version
        pval : int or float
            The :math:`p`-value of the :math:`L^p`-space
        alphabet : collection or int
            The values or size of the alphabet

        Returns
        -------
        float
            The normalized Minkowski distance

        Examples
        --------
        >>> cmp = Minkowski()
        >>> cmp.dist('cat', 'hat')
        0.5
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.636363636364
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.692307692308
        >>> cmp.dist('ATCG', 'TAGC')
        1.0

        """
        return self.dist_abs(src, tar, qval, pval, True, alphabet)


def minkowski(src, tar, qval=2, pval=1, normalized=False, alphabet=None):
    """Return the Minkowski distance (:math:`L^p`-norm) of two strings.

    This is a wrapper for :py:meth:`Minkowski.dist_abs`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    pval : int or float
        The :math:`p`-value of the :math:`L^p`-space
    normalized : bool
        Normalizes to [0, 1] if True
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The Minkowski distance

    Examples
    --------
    >>> minkowski('cat', 'hat')
    4.0
    >>> minkowski('Niall', 'Neil')
    7.0
    >>> minkowski('Colin', 'Cuilen')
    9.0
    >>> minkowski('ATCG', 'TAGC')
    10.0

    """
    return Minkowski().dist_abs(src, tar, qval, pval, normalized, alphabet)


def dist_minkowski(src, tar, qval=2, pval=1, alphabet=None):
    """Return normalized Minkowski distance of two strings.

    This is a wrapper for :py:meth:`Minkowski.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    pval : int or float
        The :math:`p`-value of the :math:`L^p`-space
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Minkowski distance

    Examples
    --------
    >>> dist_minkowski('cat', 'hat')
    0.5
    >>> round(dist_minkowski('Niall', 'Neil'), 12)
    0.636363636364
    >>> round(dist_minkowski('Colin', 'Cuilen'), 12)
    0.692307692308
    >>> dist_minkowski('ATCG', 'TAGC')
    1.0

    """
    return Minkowski().dist(src, tar, qval, pval, alphabet)


def sim_minkowski(src, tar, qval=2, pval=1, alphabet=None):
    """Return normalized Minkowski similarity of two strings.

    This is a wrapper for :py:meth:`Minkowski.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    pval : int or float
        The :math:`p`-value of the :math:`L^p`-space
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Minkowski similarity

    Examples
    --------
    >>> sim_minkowski('cat', 'hat')
    0.5
    >>> round(sim_minkowski('Niall', 'Neil'), 12)
    0.363636363636
    >>> round(sim_minkowski('Colin', 'Cuilen'), 12)
    0.307692307692
    >>> sim_minkowski('ATCG', 'TAGC')
    0.0

    """
    return Minkowski().sim(src, tar, qval, pval, alphabet)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
