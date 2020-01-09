# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.distance._weighted_jaccard.

Weighted Jaccard similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['WeightedJaccard']


class WeightedJaccard(_TokenDistance):
    r"""Weighted Jaccard similarity.

    For two sets X and Y and a weight w, the Weighted Jaccard similarity
    :cite:`Legendre:1998` is

        .. math::

            sim_{Jaccard_w}(X, Y) = \frac{w \cdot |X \cap Y|}
            {w \cdot |X \cap Y| + |X \setminus Y| + |Y \setminus X|}

    Here, the intersection between the two sets is weighted by w. Compare to
    Jaccard similarity (:math:`w = 1`), and to Dice similarity (:math:`w = 2`).
    In the default case, the weight of the intersection is 3, following
    :cite:`Legendre:1998`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Jaccard_w} =
            \frac{w\cdot a}{w\cdot a+b+c}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self, tokenizer=None, intersection_type='crisp', weight=3, **kwargs
    ):
        """Initialize TripleWeightedJaccard instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        weight : int
            The weight to apply to the intersection cardinality. (3, by
            default.)
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
        self.weight = weight
        super(WeightedJaccard, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src, tar):
        """Return the Triple Weighted Jaccard similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Weighted Jaccard similarity

        Examples
        --------
        >>> cmp = WeightedJaccard()
        >>> cmp.sim('cat', 'hat')
        0.6
        >>> cmp.sim('Niall', 'Neil')
        0.46153846153846156
        >>> cmp.sim('aluminum', 'Catalan')
        0.16666666666666666
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        return self.weight * a / (self.weight * a + b + c)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
