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

"""abydos.distance._batagelj_bren.

Batagelj & Bren distance
"""

from ._token_distance import _TokenDistance

__all__ = ['BatageljBren']


class BatageljBren(_TokenDistance):
    r"""Batagelj & Bren distance.

    For two sets X and Y and a population N, the Batagelj & Bren
    distance :cite:`Batagelj:1995`, Batagelj & Bren's :math:`Q_0`, is

        .. math::

            dist_{BatageljBren}(X, Y) =
            \frac{|X \setminus Y| \cdot |Y \setminus X|}
            {|X \cap Y| \cdot |(N \setminus X) \setminus Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{BatageljBren} =
            \frac{bc}{ad}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize BatageljBren instance.

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
        super(BatageljBren, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist_abs(self, src, tar):
        """Return the Batagelj & Bren distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Batagelj & Bren distance

        Examples
        --------
        >>> cmp = BatageljBren()
        >>> cmp.dist_abs('cat', 'hat')
        0.002570694087403599
        >>> cmp.dist_abs('Niall', 'Neil')
        0.007741935483870968
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.07282184655396619
        >>> cmp.dist_abs('ATCG', 'TAGC')
        inf


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        if a == 0 or d == 0:
            return float('inf')
        return b * c / (a * d)

    def dist(self, src, tar):
        """Return the normalized Batagelj & Bren distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Batagelj & Bren distance

        Examples
        --------
        >>> cmp = BatageljBren()
        >>> cmp.dist('cat', 'hat')
        3.2789465400556106e-06
        >>> cmp.dist('Niall', 'Neil')
        9.874917709019092e-06
        >>> cmp.dist('aluminum', 'Catalan')
        9.276668350823718e-05
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        if a == 0 or d == 0:
            return 1.0
        return (b * c / (a * d)) / (a + b + c + d)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
