# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.distance._cosine.

Cosine similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import sqrt

from ._token_distance import _TokenDistance

__all__ = ['Cosine', 'dist_cosine', 'sim_cosine']


class Cosine(_TokenDistance):
    r"""Cosine similarity.

    For two sets X and Y, the cosine similarity, Otsuka-Ochiai coefficient, or
    Ochiai coefficient :cite:`Otsuka:1936,Ochiai:1957` is:
    :math:`sim_{cosine}(X, Y) = \frac{|X \cap Y|}{\sqrt{|X| \cdot |Y|}}`.
    """

    def sim(self, src, tar, qval=2):
        r"""Return the cosine similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version

        Returns
        -------
        float
            Cosine similarity

        Examples
        --------
        >>> cmp = Cosine()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3651483716701107
        >>> cmp.sim('aluminum', 'Catalan')
        0.11785113019775793
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        q_src, q_tar = self._get_qgrams(src, tar, qval)
        q_src_mag = sum(q_src.values())
        q_tar_mag = sum(q_tar.values())
        q_intersection_mag = sum((q_src & q_tar).values())

        return q_intersection_mag / sqrt(q_src_mag * q_tar_mag)


def sim_cosine(src, tar, qval=2):
    r"""Return the cosine similarity of two strings.

    This is a wrapper for :py:meth:`Cosine.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version

    Returns
    -------
    float
        Cosine similarity

    Examples
    --------
    >>> sim_cosine('cat', 'hat')
    0.5
    >>> sim_cosine('Niall', 'Neil')
    0.3651483716701107
    >>> sim_cosine('aluminum', 'Catalan')
    0.11785113019775793
    >>> sim_cosine('ATCG', 'TAGC')
    0.0

    """
    return Cosine().sim(src, tar, qval)


def dist_cosine(src, tar, qval=2):
    """Return the cosine distance between two strings.

    This is a wrapper for :py:meth:`Cosine.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version

    Returns
    -------
    float
        Cosine distance

    Examples
    --------
    >>> dist_cosine('cat', 'hat')
    0.5
    >>> dist_cosine('Niall', 'Neil')
    0.6348516283298893
    >>> dist_cosine('aluminum', 'Catalan')
    0.882148869802242
    >>> dist_cosine('ATCG', 'TAGC')
    1.0

    """
    return Cosine().dist(src, tar, qval)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
