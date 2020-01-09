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

"""abydos.distance._baulieu_vii.

Baulieu VII distance
"""

from ._token_distance import _TokenDistance

__all__ = ['BaulieuVII']


class BaulieuVII(_TokenDistance):
    r"""Baulieu VII distance.

    For two sets X and Y and a population N, Baulieu VII distance
    :cite:`Baulieu:1997` is

        .. math::

            dist_{BaulieuVII}(X, Y) = \frac{|X \setminus Y| + |Y \setminus X|}
            {|N| + |X \cap Y| \cdot (|X \cap Y| - 4)^2}

    This is Baulieu's 25th dissimilarity coefficient. This coefficient fails
    Baulieu's (P4) property, that :math:`D(a+1,b,c,d) \leq D(a,b,c,d) = 0`
    with equality holding iff :math:`D(a,b,c,d) = 0`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{BaulieuVII} = \frac{b+c}{n + a \cdot (a-4)^2}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize BaulieuVII instance.

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
        super(BaulieuVII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Baulieu VII distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baulieu VII distance

        Examples
        --------
        >>> cmp = BaulieuVII()
        >>> cmp.dist('cat', 'hat')
        0.005050505050505051
        >>> cmp.dist('Niall', 'Neil')
        0.008838383838383838
        >>> cmp.dist('aluminum', 'Catalan')
        0.018891687657430732
        >>> cmp.dist('ATCG', 'TAGC')
        0.012755102040816327


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        bpc = self._src_only_card() + self._tar_only_card()
        n = self._population_unique_card()

        return bpc / (n + a * (a - 4) ** 2)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
