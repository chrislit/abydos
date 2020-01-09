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

"""abydos.distance._kuhns_vi.

Kuhns VI correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['KuhnsVI']


class KuhnsVI(_TokenDistance):
    r"""Kuhns VI correlation.

    For two sets X and Y and a population N, Kuhns VI correlation
    :cite:`Kuhns:1965`, the excess of probability differences V over its
    independence value (V), is

        .. math::

            corr_{KuhnsVI}(X, Y) =
            \frac{\delta(X, Y)}
            {min\big(|X|\cdot(1-\frac{|X|}{|N|}), |Y|(1-\frac{|Y|}{|N|})\big)}

    where

        .. math::

            \delta(X, Y) = |X \cap Y| - \frac{|X| \cdot |Y|}{|N|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{KuhnsVI} =
            \frac{\delta(a+b, a+c)}
            {min\big((a+b)(1-\frac{a+b}{n}), (a+c)(1-\frac{a+c}{n})\big)}

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
        """Initialize KuhnsVI instance.

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
        super(KuhnsVI, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Kuhns VI correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns VI correlation

        Examples
        --------
        >>> cmp = KuhnsVI()
        >>> cmp.corr('cat', 'hat')
        0.497435897435897
        >>> cmp.corr('Niall', 'Neil')
        0.394865211810013
        >>> cmp.corr('aluminum', 'Catalan')
        0.11470398970399
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006418485237484


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = a + b + c + d

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
                max(
                    -1.0,
                    min(
                        1.0,
                        delta_ab
                        * n
                        / min(
                            max(1, a + b) * max(1, c + d),
                            max(1, a + c) * max(1, b + d),
                        ),
                    ),
                ),
                15,
            )

    def sim(self, src, tar):
        """Return the Kuhns VI similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns VI similarity

        Examples
        --------
        >>> cmp = KuhnsVI()
        >>> cmp.sim('cat', 'hat')
        0.7487179487179485
        >>> cmp.sim('Niall', 'Neil')
        0.6974326059050064
        >>> cmp.sim('aluminum', 'Catalan')
        0.557351994851995
        >>> cmp.sim('ATCG', 'TAGC')
        0.496790757381258


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
