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

"""abydos.distance._overlap.

Overlap similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from deprecation import deprecated

from ._token_distance import _TokenDistance
from .. import __version__

__all__ = ['Overlap', 'dist_overlap', 'sim_overlap']


class Overlap(_TokenDistance):
    r"""Overlap coefficient.

    For two sets X and Y, the overlap coefficient
    :cite:`Szymkiewicz:1934,Simpson:1949`, also called the
    Szymkiewicz-Simpson coefficient, is
    :math:`sim_{overlap}(X, Y) = \frac{|X \cap Y|}{min(|X|, |Y|)}`.

    .. versionadded:: 0.3.6
    """

    def sim(self, src, tar, tokenizer=None, *args, **kwargs):
        r"""Return the overlap coefficient of two strings.

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
            Overlap similarity

        Examples
        --------
        >>> cmp = Overlap()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.4
        >>> cmp.sim('aluminum', 'Catalan')
        0.125
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0

        q_src, q_tar = self._get_qgrams(src, tar, qval)
        q_src_mag = sum(q_src.values())
        q_tar_mag = sum(q_tar.values())
        q_intersection_mag = sum((q_src & q_tar).values())

        return q_intersection_mag / min(q_src_mag, q_tar_mag)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Overlap.sim method instead.',
)
def sim_overlap(src, tar, tokenizer=None, *args, **kwargs):
    r"""Return the overlap coefficient of two strings.

    This is a wrapper for :py:meth:`Overlap.sim`.

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
        Overlap similarity

    Examples
    --------
    >>> sim_overlap('cat', 'hat')
    0.5
    >>> sim_overlap('Niall', 'Neil')
    0.4
    >>> sim_overlap('aluminum', 'Catalan')
    0.125
    >>> sim_overlap('ATCG', 'TAGC')
    0.0

    .. versionadded:: 0.1.0

    """
    return Overlap().sim(src, tar, tokenizer=tokenizer, args=args, kwargs=kwargs)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Overlap.dist method instead.',
)
def dist_overlap(src, tar, tokenizer=None, *args, **kwargs):
    """Return the overlap distance between two strings.

    This is a wrapper for :py:meth:`Overlap.dist`.

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
        Overlap distance

    Examples
    --------
    >>> dist_overlap('cat', 'hat')
    0.5
    >>> dist_overlap('Niall', 'Neil')
    0.6
    >>> dist_overlap('aluminum', 'Catalan')
    0.875
    >>> dist_overlap('ATCG', 'TAGC')
    1.0

    .. versionadded:: 0.1.0

    """
    return Overlap().dist(src, tar, tokenizer=tokenizer, args=args, kwargs=kwargs)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
