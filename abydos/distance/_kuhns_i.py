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

"""abydos.distance._kuhns_i.

Kuhns I correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['KuhnsI']


class KuhnsI(_TokenDistance):
    r"""Kuhns I correlation.

    For two sets X and Y and a population N, Kuhns I correlation
    :cite:`Kuhns:1965`, the excess of separation over its independence value
    (S), is

        .. math::

            corr_{KuhnsI}(X, Y) =
            \frac{2\delta(X, Y)}{|N|}

    where

        .. math::

            \delta(X, Y) = |X \cap Y| - \frac{|X| \cdot |Y|}{|N|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{KuhnsI} =
            \frac{2\delta(a+b, a+c)}{n}

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
        """Initialize KuhnsI instance.

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
        super(KuhnsI, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Kuhns I correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns I correlation

        Examples
        --------
        >>> cmp = KuhnsI()
        >>> cmp.corr('cat', 'hat')
        0.005049979175343606
        >>> cmp.corr('Niall', 'Neil')
        0.005004425239483548
        >>> cmp.corr('aluminum', 'Catalan')
        0.0023140898210880765
        >>> cmp.corr('ATCG', 'TAGC')
        -8.134631403581842e-05


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        n = self._population_unique_card()

        apbmapc = (a + b) * (a + c)
        if not apbmapc:
            delta_ab = a
        else:
            delta_ab = a - apbmapc / n
        if not delta_ab:
            return 0.0
        else:
            return 2 * delta_ab / n

    def sim(self, src, tar):
        """Return the Kuhns I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns I similarity

        Examples
        --------
        >>> cmp = KuhnsI()
        >>> cmp.sim('cat', 'hat')
        0.5050499791753436
        >>> cmp.sim('Niall', 'Neil')
        0.5050044252394835
        >>> cmp.sim('aluminum', 'Catalan')
        0.502314089821088
        >>> cmp.sim('ATCG', 'TAGC')
        0.49991865368596416


        .. versionadded:: 0.4.0

        """
        return 0.5 + self.corr(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
