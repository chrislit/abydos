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

"""abydos.distance._baulieu_xii.

Baulieu XII distance
"""

from ._token_distance import _TokenDistance

__all__ = ['BaulieuXII']


class BaulieuXII(_TokenDistance):
    r"""Baulieu XII distance.

    For two sets X and Y and a population N, Baulieu XII distance
    :cite:`Baulieu:1997` is

        .. math::

            dist_{BaulieuXII}(X, Y) = \frac{|X \setminus Y| + |Y \setminus X|}
            {|X \cap Y| + |X \setminus Y| + |Y \setminus X| - 1}

    This is Baulieu's 30th dissimilarity coefficient. This coefficient fails
    Baulieu's (P5) property, that :math:`D(a,b+1,c,d) \geq D(a,b,c,d)`,
    with equality holding if :math:`D(a,b,c,d) = 1`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{BaulieuXII} = \frac{b+c}{a+b+c-1}

    Notes
    -----
    In the special case of comparisons where the intersection (a) contains 0
    members, the size of the intersection is set to 1, resulting in a distance
    of 1.0. This prevents the distance from exceeding 1.0 and similarity from
    becoming negative.


    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize BaulieuXII instance.

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
        super(BaulieuXII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Baulieu XII distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baulieu XII distance

        Examples
        --------
        >>> cmp = BaulieuXII()
        >>> cmp.dist('cat', 'hat')
        0.8
        >>> cmp.dist('Niall', 'Neil')
        0.875
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = max(1.0, self._intersection_card())
        bpc = self._src_only_card() + self._tar_only_card()

        if bpc == 0.0:
            return 0.0
        return bpc / (a + bpc - 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
