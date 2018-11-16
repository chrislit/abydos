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

"""abydos.distance._tversky.

Tversky index
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['Tversky', 'dist_tversky', 'sim_tversky']


class Tversky(_TokenDistance):
    r"""Tversky index.

    The Tversky index :cite:`Tversky:1977` is defined as:
    For two sets X and Y:
    :math:`sim_{Tversky}(X, Y) = \frac{|X \cap Y|}
    {|X \cap Y| + \alpha|X - Y| + \beta|Y - X|}`.

    :math:`\alpha = \beta = 1` is equivalent to the Jaccard & Tanimoto
    similarity coefficients.

    :math:`\alpha = \beta = 0.5` is equivalent to the Sørensen-Dice
    similarity coefficient :cite:`Dice:1945,Sorensen:1948`.

    Unequal α and β will tend to emphasize one or the other set's
    contributions:

        - :math:`\alpha > \beta` emphasizes the contributions of X over Y
        - :math:`\alpha < \beta` emphasizes the contributions of Y over X)

    Parameter values' relation to 1 emphasizes different types of
    contributions:

        - :math:`\alpha and \beta > 1` emphsize unique contributions over the
          intersection
        - :math:`\alpha and \beta < 1` emphsize the intersection over unique
          contributions

    The symmetric variant is defined in :cite:`Jiminez:2013`. This is activated
    by specifying a bias parameter.
    """

    def sim(self, src, tar, qval=2, alpha=1, beta=1, bias=None):
        """Return the Tversky index of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version
        alpha : float
            Tversky index parameter as described above
        beta : float
            Tversky index parameter as described above
        bias : float
            The symmetric Tversky index bias parameter

        Returns
        -------
        float
            Tversky similarity

        Raises
        ------
        ValueError
            Unsupported weight assignment; alpha and beta must be greater than
            or equal to 0.

        Examples
        --------
        >>> cmp = Tversky()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if alpha < 0 or beta < 0:
            raise ValueError(
                'Unsupported weight assignment; alpha and beta '
                + 'must be greater than or equal to 0.'
            )

        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0

        q_src, q_tar = self._get_qgrams(src, tar, qval)
        q_src_mag = sum(q_src.values())
        q_tar_mag = sum(q_tar.values())
        q_intersection_mag = sum((q_src & q_tar).values())

        if not q_src or not q_tar:
            return 0.0

        if bias is None:
            return q_intersection_mag / (
                q_intersection_mag
                + alpha * (q_src_mag - q_intersection_mag)
                + beta * (q_tar_mag - q_intersection_mag)
            )

        a_val = min(
            q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag
        )
        b_val = max(
            q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag
        )
        c_val = q_intersection_mag + bias
        return c_val / (beta * (alpha * a_val + (1 - alpha) * b_val) + c_val)


def sim_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky index of two strings.

    This is a wrapper for :py:meth:`Tversky.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    alpha : float
        Tversky index parameter as described above
    beta : float
        Tversky index parameter as described above
    bias : float
        The symmetric Tversky index bias parameter

    Returns
    -------
    float
        Tversky similarity

    Examples
    --------
    >>> sim_tversky('cat', 'hat')
    0.3333333333333333
    >>> sim_tversky('Niall', 'Neil')
    0.2222222222222222
    >>> sim_tversky('aluminum', 'Catalan')
    0.0625
    >>> sim_tversky('ATCG', 'TAGC')
    0.0

    """
    return Tversky().sim(src, tar, qval, alpha, beta, bias)


def dist_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky distance between two strings.

    This is a wrapper for :py:meth:`Tversky.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    alpha : float
        Tversky index parameter as described above
    beta : float
        Tversky index parameter as described above
    bias : float
        The symmetric Tversky index bias parameter

    Returns
    -------
    float
        Tversky distance

    Examples
    --------
    >>> dist_tversky('cat', 'hat')
    0.6666666666666667
    >>> dist_tversky('Niall', 'Neil')
    0.7777777777777778
    >>> dist_tversky('aluminum', 'Catalan')
    0.9375
    >>> dist_tversky('ATCG', 'TAGC')
    1.0

    """
    return Tversky().dist(src, tar, qval, alpha, beta, bias)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
