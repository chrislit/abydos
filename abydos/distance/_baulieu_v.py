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

"""abydos.distance._baulieu_v.

Baulieu V distance
"""

from ._token_distance import _TokenDistance

__all__ = ['BaulieuV']


class BaulieuV(_TokenDistance):
    r"""Baulieu V distance.

    For two sets X and Y and a population N, Baulieu V distance
    :cite:`Baulieu:1997` is

        .. math::

            dist_{BaulieuV}(X, Y) = \frac{|X \setminus Y| + |Y \setminus X| +
            1}{|X \cap Y| + |X \setminus Y| + |Y \setminus X| + 1}

    This is Baulieu's 23rd dissimilarity coefficient. This coefficient fails
    Baulieu's (P2) property, that :math:`D(a,0,0,0) = 0`. Rather,
    :math:`D(a,0,0,0) > 0`, but
    :math:`\lim_{a \to \infty} D(a,0,0,0) = 0`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{BaulieuV} = \frac{b+c+1}{a+b+c+1}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize BaulieuV instance.

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
        super(BaulieuV, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Baulieu V distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baulieu V distance

        Examples
        --------
        >>> cmp = BaulieuV()
        >>> cmp.dist('cat', 'hat')
        0.7142857142857143
        >>> cmp.dist('Niall', 'Neil')
        0.8
        >>> cmp.dist('aluminum', 'Catalan')
        0.9411764705882353
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        return (b + c + 1) / (a + b + c + 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
