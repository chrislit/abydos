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

"""abydos.distance._jaccard.

Jaccard similarity coefficient, distance, & Tanimoto coefficient
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from ._tversky import Tversky

__all__ = ['Jaccard', 'dist_jaccard', 'sim_jaccard', 'tanimoto']


class Jaccard(Tversky):
    r"""Jaccard similarity.

    For two sets X and Y, the Jaccard similarity coefficient
    :cite:`Jaccard:1901` is :math:`sim_{Jaccard}(X, Y) =
    \frac{|X \cap Y|}{|X \cup Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958`
    and the Tversky index :cite:`Tversky:1977` for
    :math:`\alpha = \beta = 1`.
    """

    def sim(self, src, tar, qval=2):
        r"""Return the Jaccard similarity of two strings.

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
            Jaccard similarity

        Examples
        --------
        >>> cmp = Jaccard()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        return super(self.__class__, self).sim(src, tar, qval, 1, 1)

    def tanimoto_coeff(self, src, tar, qval=2):
        """Return the Tanimoto distance between two strings.

        Tanimoto distance :cite:`Tanimoto:1958` is
        :math:`-log_{2} sim_{Tanimoto}(X, Y)`.

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
            Tanimoto distance

        Examples
        --------
        >>> cmp = Jaccard()
        >>> cmp.tanimoto_coeff('cat', 'hat')
        -1.5849625007211563
        >>> cmp.tanimoto_coeff('Niall', 'Neil')
        -2.1699250014423126
        >>> cmp.tanimoto_coeff('aluminum', 'Catalan')
        -4.0
        >>> cmp.tanimoto_coeff('ATCG', 'TAGC')
        -inf

        """
        coeff = self.sim(src, tar, qval)
        if coeff != 0:
            return log(coeff, 2)

        return float('-inf')


def sim_jaccard(src, tar, qval=2):
    """Return the Jaccard similarity of two strings.

    This is a wrapper for :py:meth:`Jaccard.sim`.

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
        Jaccard similarity

    Examples
    --------
    >>> sim_jaccard('cat', 'hat')
    0.3333333333333333
    >>> sim_jaccard('Niall', 'Neil')
    0.2222222222222222
    >>> sim_jaccard('aluminum', 'Catalan')
    0.0625
    >>> sim_jaccard('ATCG', 'TAGC')
    0.0

    """
    return Jaccard().sim(src, tar, qval)


def dist_jaccard(src, tar, qval=2):
    """Return the Jaccard distance between two strings.

    This is a wrapper for :py:meth:`Jaccard.dist`.

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
        Jaccard distance

    Examples
    --------
    >>> dist_jaccard('cat', 'hat')
    0.6666666666666667
    >>> dist_jaccard('Niall', 'Neil')
    0.7777777777777778
    >>> dist_jaccard('aluminum', 'Catalan')
    0.9375
    >>> dist_jaccard('ATCG', 'TAGC')
    1.0

    """
    return Jaccard().dist(src, tar, qval)


def tanimoto(src, tar, qval=2):
    """Return the Tanimoto coefficient of two strings.

    This is a wrapper for :py:meth:`Jaccard.tanimoto_coeff`.

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
        Tanimoto distance

    Examples
    --------
    >>> tanimoto('cat', 'hat')
    -1.5849625007211563
    >>> tanimoto('Niall', 'Neil')
    -2.1699250014423126
    >>> tanimoto('aluminum', 'Catalan')
    -4.0
    >>> tanimoto('ATCG', 'TAGC')
    -inf

    """
    return Jaccard().tanimoto_coeff(src, tar, qval)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
