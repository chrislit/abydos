# -*- coding: utf-8 -*-

# Copyright 2018-2019 by Christopher C. Little.
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

"""abydos.distance._gini.

Gini distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['Gini']


class Gini(_TokenDistance):
    r"""Gini distance.

    For two sets X and Y and a population N, Gini distance
    :cite:`Gini:1912` is

        .. math::

            sim_{Gini}(X, Y) =
            \frac{\frac{|X \cap Y|+|(N \setminus X) \setminus Y|}{|N|} -
            \frac{|X|+|Y|}{|N|} \cdot
            \frac{|N \setminus Y|+|N \setminus X|}{|N|}}
            {\sqrt{(1-(\frac{|X|}{|N|}^2+\frac{|Y|}{|N|}^2)) \cdot
            (1-(\frac{|N \setminus Y|}{|N|}^2 +
            \frac{|N \setminus X|}{|N|}^2))}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    after each term has been converted to a proportion by dividing by n, this
    is

        .. math::

            sim_{Gini} =
            \frac{(a+d)-((a+b)(a+c) + (b+d)(c+d))}
            {\sqrt{(1-((a+b)^2+(c+d)^2))\cdot(1-((a+c)^2+(b+d)^2))}}

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
        """Initialize Gini instance.

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
            A string distance measure class for use in the 'soft' and 'fuzzy'
            variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the 'fuzzy' variant.


        .. versionadded:: 0.4.0

        """
        super(Gini, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            normalizer=normalizer,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Gini distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gini distance

        Examples
        --------
        >>> cmp = Gini()
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
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        return ((a + d) - ((a + b) * (a + c) + (c + d) * (b + d))) / (
            (1 - ((a + b) ** 2 + (c + d) ** 2))
            * (1 - ((a + c) ** 2 + (b + d) ** 2))
        ) ** 0.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
