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

"""abydos.distance._gini_i.

Gini I correlation
"""

from sys import float_info

from ._token_distance import _TokenDistance

__all__ = ['GiniI']

_epsilon = float_info.epsilon


class GiniI(_TokenDistance):
    r"""Gini I correlation.

    For two sets X and Y and a population N, Gini I correlation
    :cite:`Gini:1912`, using the formula from :cite:`Goodman:1959`, is

        .. math::

            corr_{GiniI}(X, Y) =
            \frac{\frac{|X \cap Y|+|(N \setminus X) \setminus Y|}{|N|} -
            \frac{|X| \cdot |Y|}{|N|} +
            \frac{|N \setminus Y| \cdot |N \setminus X|}{|N|}}
            {\sqrt{(1-(\frac{|X|}{|N|}^2+\frac{|Y|}{|N|}^2)) \cdot
            (1-(\frac{|N \setminus Y|}{|N|}^2 +
            \frac{|N \setminus X|}{|N|}^2))}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    after each term has been converted to a proportion by dividing by n, this
    is

        .. math::

            corr_{GiniI} =
            \frac{(a+d)-(a+b)(a+c) + (b+d)(c+d)}
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
        """Initialize GiniI instance.

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
        super(GiniI, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            normalizer=normalizer,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Gini I correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gini I correlation

        Examples
        --------
        >>> cmp = GiniI()
        >>> cmp.corr('cat', 'hat')
        0.49722814498933254
        >>> cmp.corr('Niall', 'Neil')
        0.39649090262533215
        >>> cmp.corr('aluminum', 'Catalan')
        0.14887105223941113
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006418485237489576


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        return ((a + d) - ((a + b) * (a + c) + (c + d) * (b + d))) / (
            (1 + _epsilon - ((a + b) ** 2 + (c + d) ** 2))
            * (1 + _epsilon - ((a + c) ** 2 + (b + d) ** 2))
        ) ** 0.5

    def sim(self, src, tar):
        """Return the normalized Gini I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Gini I similarity

        Examples
        --------
        >>> cmp = GiniI()
        >>> cmp.sim('cat', 'hat')
        0.7486140724946663
        >>> cmp.sim('Niall', 'Neil')
        0.6982454513126661
        >>> cmp.sim('aluminum', 'Catalan')
        0.5744355261197056
        >>> cmp.sim('ATCG', 'TAGC')
        0.4967907573812552


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
