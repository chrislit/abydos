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

"""abydos.distance._goodman_kruskal_min.

Goodman & Kruskal Min similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['GoodmanKruskalMin']


class GoodmanKruskalMin(_TokenDistance):
    r"""Goodman & Kruskal Min similarity.

    For two sets X and Y and a population N, Goodman & Kruskal Min similarity
    :cite:`Goodman:1954` is

        .. math::

            sim_{GoodmanKruskalMin}(X, Y) =
            \frac{2 \cdot min(|X \cap Y|, |(N \setminus X) \setminus Y|) -
            |X \setminus Y| - |Y \setminus X|}
            {2 \cdot min(|X \cap Y|, |(N \setminus X) \setminus Y|) +
            |X \setminus Y| + |Y \setminus X|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{GoodmanKruskalMin} =
            \frac{2 \cdot min(a, d) - b - c}{2 \cdot min(a, d) + b + c}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize GoodmanKruskalMin instance.

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
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.
        metric : _Distance
            A string distance measure class for use in the 'soft' and 'fuzzy'
            variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the 'fuzzy' variant.


        .. versionadded:: 0.4.0

        """
        super(GoodmanKruskalMin, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return Goodman & Kruskal Min similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Goodman & Kruskal Min similarity

        Examples
        --------
        >>> cmp = GoodmanKruskalMin()
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
        self.tokenize(src, tar)

        mad = min(self.intersection_card(), self.total_complement_card())
        b = self.src_only_card()
        c = self.tar_only_card()

        return (2 * mad - b - c) / (2 * mad + b + c)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
