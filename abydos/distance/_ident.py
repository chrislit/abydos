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

"""abydos.distance._ident.

Identity similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance

__all__ = ['Ident', 'dist_ident', 'sim_ident']


class Ident(_Distance):
    """Identity distance and similarity."""

    def sim(self, src, tar):
        """Return the identity similarity of two strings.

        Identity similarity is 1.0 if the two strings are identical,
        otherwise 0.0

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Identity similarity

        Examples
        --------
        >>> cmp = Ident()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('cat', 'cat')
        1.0

        """
        return 1.0 if src == tar else 0.0


def sim_ident(src, tar):
    """Return the identity similarity of two strings.

    This is a wrapper for :py:meth:`Ident.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Identity similarity


    Examples
    --------
    >>> sim_ident('cat', 'hat')
    0.0
    >>> sim_ident('cat', 'cat')
    1.0

    """
    return Ident().sim(src, tar)


def dist_ident(src, tar):
    """Return the identity distance between two strings.

    This is a wrapper for :py:meth:`Ident.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Identity distance

    Examples
    --------
    >>> dist_ident('cat', 'hat')
    1.0
    >>> dist_ident('cat', 'cat')
    0.0

    """
    return Ident().dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
