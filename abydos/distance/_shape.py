# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.distance._shape_difference.

Penrose's shape difference
"""

from ._token_distance import _TokenDistance

__all__ = ['Shape']


class Shape(_TokenDistance):
    r"""Penrose's shape difference.

    For two sets X and Y and a population N, the Penrose's shape difference
    :cite:`Penrose:1952` is

        .. math::

            dist_{Shape}(X, Y) =
            \frac{1}{|N|}\cdot\Big(\sum_{x \in (X \triangle Y)} x^2\Big) -
            \Big(\frac{|X \triangle Y|}{|N|}\Big)^2

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Shape} =
            \frac{1}{n}\Big(\sum_{x \in b} x^2 + \sum_{x \in c} x^2\Big) -
            \Big(\frac{b+c}{n}\Big)^2

    In :cite:`IBM:2017`, the formula is instead
    :math:`\frac{n(b+c)-(b-c)^2}{n^2}`, but it is clear from
    :cite:`Penrose:1952` that this should not be an assymmetric value with
    respect to the ordering of the two sets, among other errors in this
    formula. Meanwhile, :cite:`Deza:2016` gives the formula
    :math:`\sqrt{\sum((x_i-\bar{x})-(y_i-\bar{y}))^2}`.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Shape instance.

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
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the ``fuzzy`` variant.


        .. versionadded:: 0.4.0

        """
        super(Shape, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Penrose's shape difference of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Shape ifference

        Examples
        --------
        >>> cmp = Shape()
        >>> cmp.sim('cat', 'hat')
        0.994923990004165
        >>> cmp.sim('Niall', 'Neil')
        0.9911511479591837
        >>> cmp.sim('aluminum', 'Catalan')
        0.9787090754188811
        >>> cmp.sim('ATCG', 'TAGC')
        0.9874075905872554


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        symdiff = self._symmetric_difference().values()

        dist = sum(symdiff)
        dist_sq = sum(_ ** 2 for _ in symdiff)
        n = self._population_unique_card()

        return dist_sq / n - (dist / n) ** 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
