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

"""abydos.distance._goodman_kruskal_lambda_r.

Goodman & Kruskal Lambda-r correlation.
"""

from ._token_distance import _TokenDistance

__all__ = ['GoodmanKruskalLambdaR']


class GoodmanKruskalLambdaR(_TokenDistance):
    r"""Goodman & Kruskal Lambda-r correlation.

    For two sets X and Y and a population N, Goodman & Kruskal
    :math:`\lambda_r` correlation :cite:`Goodman:1954` is

        .. math::

            corr_{GK_{\lambda_r}}(X, Y) =
            \frac{|X \cap Y| + |(N \setminus X) \setminus Y| -
            \frac{1}{2}(max(|X|, |N \setminus X|) + max(|Y|, |N \setminus Y|))}
            {|N| -
            \frac{1}{2}(max(|X|, |N \setminus X|) + max(|Y|, |N \setminus Y|))}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{GK_{\lambda_r}} =
            \frac{a + d - \frac{1}{2}(max(a+b,c+d)+max(a+c,b+d))}
            {n - \frac{1}{2}(max(a+b,c+d)+max(a+c,b+d))}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize GoodmanKruskalLambdaR instance.

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
        super(GoodmanKruskalLambdaR, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return Goodman & Kruskal Lambda-r correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Goodman & Kruskal Lambda-r correlation

        Examples
        --------
        >>> cmp = GoodmanKruskalLambdaR()
        >>> cmp.corr('cat', 'hat')
        0.0
        >>> cmp.corr('Niall', 'Neil')
        -0.2727272727272727
        >>> cmp.corr('aluminum', 'Catalan')
        -0.7647058823529411
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        if not self._src_card() or not self._tar_card():
            return -1.0

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        sigma_prime = max(a + b, c + d) + max(a + c, b + d)

        num = 2 * (a + d) - sigma_prime

        if num:
            return num / (2 * n - sigma_prime)
        return 0.0

    def sim(self, src, tar):
        """Return Goodman & Kruskal Lambda-r similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Goodman & Kruskal Lambda-r similarity

        Examples
        --------
        >>> cmp = GoodmanKruskalLambdaR()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.36363636363636365
        >>> cmp.sim('aluminum', 'Catalan')
        0.11764705882352944
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
