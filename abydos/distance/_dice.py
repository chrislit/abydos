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

"""abydos.distance._dice.

Sørensen–Dice coefficient & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._tversky import Tversky

__all__ = ['Dice', 'dist_dice', 'sim_dice']


class Dice(Tversky):
    r"""Sørensen–Dice coefficient.

    For two sets X and Y, the Sørensen–Dice coefficient
    :cite:`Dice:1945,Sorensen:1948` is
    :math:`sim_{dice}(X, Y) = \frac{2 \cdot |X \cap Y|}{|X| + |Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958` and the Tversky index :cite:`Tversky:1977` for
    :math:`\alpha = \beta = 0.5`.
    """

    def sim(self, src, tar, qval=2):
        """Return the Sørensen–Dice coefficient of two strings.

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
            Sørensen–Dice similarity

        Examples
        --------
        >>> cmp = Dice()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.36363636363636365
        >>> cmp.sim('aluminum', 'Catalan')
        0.11764705882352941
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        return super(self.__class__, self).sim(src, tar, qval, 0.5, 0.5)


def sim_dice(src, tar, qval=2):
    """Return the Sørensen–Dice coefficient of two strings.

    This is a wrapper for :py:meth:`Dice.sim`.

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
        Sørensen–Dice similarity

    Examples
    --------
    >>> sim_dice('cat', 'hat')
    0.5
    >>> sim_dice('Niall', 'Neil')
    0.36363636363636365
    >>> sim_dice('aluminum', 'Catalan')
    0.11764705882352941
    >>> sim_dice('ATCG', 'TAGC')
    0.0

    """
    return Dice().sim(src, tar, qval)


def dist_dice(src, tar, qval=2):
    """Return the Sørensen–Dice distance between two strings.

    This is a wrapper for :py:meth:`Dice.dist`.

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
        Sørensen–Dice distance

    Examples
    --------
    >>> dist_dice('cat', 'hat')
    0.5
    >>> dist_dice('Niall', 'Neil')
    0.6363636363636364
    >>> dist_dice('aluminum', 'Catalan')
    0.8823529411764706
    >>> dist_dice('ATCG', 'TAGC')
    1.0

    """
    return Dice().dist(src, tar, qval)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
