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

"""abydos.distance._kuhns_viii.

Kuhns VIII correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['KuhnsVIII']


class KuhnsVIII(_TokenDistance):
    r"""Kuhns VIII correlation.

    For two sets X and Y and a population N, Kuhns VIII correlation
    :cite:`Kuhns:1965`, the excess of coefficient by the arithmetic mean over
    its independence value (E), is

        .. math::

            corr_{KuhnsVIII}(X, Y) =
            \frac{\delta(X, Y)}{|X \cap Y|+\frac{1}{2}\cdot|X \triangle Y|}

    where

        .. math::

            \delta(X, Y) = |X \cap Y| - \frac{|X| \cdot |Y|}{|N|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{KuhnsVIII} =
            \frac{\delta(a+b, a+c)}{a+\frac{1}{2}(b+c)}

    where

        .. math::

            \delta(a+b, a+c) = a - \frac{(a+b)(a+c)}{n}

    Notes
    -----
    The coefficient presented in :cite:`Eidenberger:2014,Morris:2012` as Kuhns'
    "Coefficient of arithmetic means" is a significantly different
    coefficient, not evidenced in :cite:`Kuhns:1965`.

    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize KuhnsVIII instance.

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
        super(KuhnsVIII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Kuhns VIII correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns VIII correlation

        Examples
        --------
        >>> cmp = KuhnsVIII()
        >>> cmp.corr('cat', 'hat')
        0.49489795918367346
        >>> cmp.corr('Niall', 'Neil')
        0.35667903525046385
        >>> cmp.corr('aluminum', 'Catalan')
        0.10685650056200824
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006377551020408163


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
            return delta_ab / (a + 0.5 * (b + c))

    def sim(self, src, tar):
        """Return the Kuhns VIII similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns VIII similarity

        Examples
        --------
        >>> cmp = KuhnsVIII()
        >>> cmp.sim('cat', 'hat')
        0.663265306122449
        >>> cmp.sim('Niall', 'Neil')
        0.5711193568336426
        >>> cmp.sim('aluminum', 'Catalan')
        0.40457100037467214
        >>> cmp.sim('ATCG', 'TAGC')
        0.32908163265306123


        .. versionadded:: 0.4.0

        """
        return (0.5 + self.corr(src, tar)) / 1.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
