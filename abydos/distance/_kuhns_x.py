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

"""abydos.distance._kuhns_x.

Kuhns X correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['KuhnsX']


class KuhnsX(_TokenDistance):
    r"""Kuhns X correlation.

    For two sets X and Y and a population N, Kuhns X correlation
    :cite:`Kuhns:1965`, the excess of Yule's Q over its independence value (Q),
    is

        .. math::

            corr_{KuhnsX}(X, Y) =
            \frac{|N| \cdot \delta(X, Y)}{|X \cap Y| \cdot
            |(N \setminus X) \setminus Y| +
            |X \setminus Y| \cdot |Y \setminus X|}

    where

        .. math::

            \delta(X, Y) = |X \cap Y| - \frac{|X| \cdot |Y|}{|N|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{KuhnsX} =
            \frac{n \cdot \delta(a+b, a+c)}{ad+bc}

    where

        .. math::

            \delta(a+b, a+c) = a - \frac{(a+b)(a+c)}{n}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize KuhnsX instance.

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
        super(KuhnsX, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Kuhns X correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns X correlation

        Examples
        --------
        >>> cmp = KuhnsX()
        >>> cmp.corr('cat', 'hat')
        0.994871794871795
        >>> cmp.corr('Niall', 'Neil')
        0.984635083226633
        >>> cmp.corr('aluminum', 'Catalan')
        0.864242424242424
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = max(1, self._total_complement_card())
        n = self._population_unique_card()
        if a == n:
            n += 1

        apbmapc = (a + b) * (a + c)
        if not apbmapc:
            delta_ab = a
        else:
            delta_ab = a - apbmapc / n
        if not delta_ab:
            return 0.0
        else:
            # clamp to [-1.0, 1.0], strictly due to floating point precision
            # issues
            return round(
                max(-1.0, min(1.0, (n * delta_ab) / (a * d + b * c))), 15
            )

    def sim(self, src, tar):
        """Return the Kuhns X similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns X similarity

        Examples
        --------
        >>> cmp = KuhnsX()
        >>> cmp.sim('cat', 'hat')
        0.9974358974358974
        >>> cmp.sim('Niall', 'Neil')
        0.9923175416133165
        >>> cmp.sim('aluminum', 'Catalan')
        0.932121212121212
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
