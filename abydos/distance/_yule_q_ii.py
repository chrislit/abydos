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

"""abydos.distance._yule_q_ii.

Yule's Q dissimilarity
"""

from ._token_distance import _TokenDistance

__all__ = ['YuleQII']


class YuleQII(_TokenDistance):
    r"""Yule's Q dissimilarity.

    For two sets X and Y and a population N, Yule's Q dissimilarity
    :cite:`Yule:1968` is

        .. math::

            dist_{Yule_QII}(X, Y) =
            \frac{2 \cdot |X \setminus Y| \cdot |Y \setminus X|}
            {|X \cap Y| \cdot |(N \setminus X) \setminus Y| +
            |X \setminus Y| \cdot |Y \setminus X|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{Yule_QII} =
            \frac{2bc}{ad+bc}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize YuleQII instance.

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
        super(YuleQII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist_abs(self, src, tar):
        """Return Yule's Q dissimilarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Yule's Q II distance

        Examples
        --------
        >>> cmp = YuleQII()
        >>> cmp.dist_abs('cat', 'hat')
        0.005128205128205128
        >>> cmp.dist_abs('Niall', 'Neil')
        0.015364916773367477
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.13575757575757577
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        if not b or not c:
            return 0.0
        return (2 * b * c) / (a * d + b * c)

    def dist(self, src, tar):
        """Return normalized Yule's Q dissimilarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Yule's Q II distance

        Examples
        --------
        >>> cmp = YuleQII()
        >>> cmp.dist('cat', 'hat')
        0.002564102564102564
        >>> cmp.dist('Niall', 'Neil')
        0.0076824583866837385
        >>> cmp.dist('aluminum', 'Catalan')
        0.06787878787878789
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        return self.dist_abs(src, tar) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
