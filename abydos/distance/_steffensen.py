# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._steffensen.

Steffensen similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from numpy import array as np_array

from ._token_distance import _TokenDistance

__all__ = ['Steffensen']


class Steffensen(_TokenDistance):
    r"""Steffensen similarity.

    For two sets X and Y and a population N, Steffensen similarity
    :math:`\psi^2` :cite:`Steffensen:1934` is

        .. math::

            \begin{array}{ll}
            sim_{Steffensen_{\psi}}(X, Y) = \psi^2 &=
            \sum_{i \in X}\sum_{j \in Y} p_{ij} \phi_{ij}^2
            \\
            \phi_{ij}^2 &= \frac{(p_{ij} - p_{i*}p_{*i})^2}
            {p_{i*}(1-p_{i*})p_{*j}(1-p_{*j})}
            \end{array}

    Where each value :math:`p_{ij}` is drawn from the 2x2 contingency table:

    +----------------+--------------+-----------------+-------+
    |                | |in| ``tar`` | |notin| ``tar`` |       |
    +----------------+--------------+-----------------+-------+
    | |in| ``src``   | |a|          | |b|             | |a+b| |
    +----------------+--------------+-----------------+-------+
    | |notin| ``src``| |c|          | |d|             | |c+d| |
    +----------------+--------------+-----------------+-------+
    |                | |a+c|        | |b+d|           | |n|   |
    +----------------+--------------+-----------------+-------+

    .. |in| replace:: :math:`x \in`
    .. |notin| replace:: :math:`x \notin`

    .. |a| replace:: :math:`p_{11} = a`
    .. |b| replace:: :math:`p_{10} = b`
    .. |c| replace:: :math:`p_{01} = c`
    .. |d| replace:: :math:`p_{00} = d`
    .. |n| replace:: :math:`1`
    .. |a+b| replace:: :math:`p_{1*} = a+b`
    .. |a+c| replace:: :math:`p_{*1} = a+c`
    .. |c+d| replace:: :math:`p_{0*} = c+d`
    .. |b+d| replace:: :math:`p_{*0} = b+d`

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        normalizer='proportional',
        **kwargs
    ):
        """Initialize Steffensen instance.

        Parameters
        ----------
        alphabet : Counter, collection, int, or None
            This represents the alphabet of possible tokens.
            See :ref:`alphabet <alphabet>` description in
            :py:class:`_TokenDistance` for details.
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        normalizer : str
            Specifies the normalization type. See :ref:`normalizer <alphabet>`
            description in :py:class:`_TokenDistance` for details.
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.
        metric : _Distance
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the ``fuzzy`` variant.


        .. versionadded:: 0.4.0

        """
        super(Steffensen, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            normalizer=normalizer,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Steffensen similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Steffensen similarity

        Examples
        --------
        >>> cmp = Steffensen()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = a + b + c + d

        p = np_array([[a, b], [c, d]]) / n

        psisq = 0.0

        for i in range(len(p)):
            pi_star = p[i, :].sum()
            for j in range(len(p[i])):
                pj_star = p[:, j].sum()
                psisq += (
                    p[i, j]
                    * (p[i, j] - pi_star * pj_star) ** 2
                    / (pi_star * (1 - pi_star) * pj_star * (1 - pj_star))
                )

        return psisq


if __name__ == '__main__':
    import doctest

    doctest.testmod()
