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

"""abydos.distance._baulieu_vi.

Baulieu VI distance
"""

from ._token_distance import _TokenDistance

__all__ = ['BaulieuVI']


class BaulieuVI(_TokenDistance):
    r"""Baulieu VI distance.

    For two sets X and Y and a population N, Baulieu VI distance
    :cite:`Baulieu:1997` is

        .. math::

            dist_{BaulieuVI}(X, Y) = \frac{|X \setminus Y| + |Y \setminus X|}
            {|X \cap Y| + |X \setminus Y| + |Y \setminus X| + 1}

    This is Baulieu's 24th dissimilarity coefficient. This coefficient fails
    Baulieu's (P3) property, that :math:`D(a,b,c,d) = 1` for some (a,b,c,d).
    Rather, :math:`D(a,b,c,d) < 1`, but
    :math:`\lim_{b \to \infty, c \to \infty} D(a,b,c,d) = 0` for :math:`a = 0`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{BaulieuVI} = \frac{b+c}{a+b+c+1}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize BaulieuVI instance.

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
        super(BaulieuVI, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Baulieu VI distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baulieu VI distance

        Examples
        --------
        >>> cmp = BaulieuVI()
        >>> cmp.dist('cat', 'hat')
        0.5714285714285714
        >>> cmp.dist('Niall', 'Neil')
        0.7
        >>> cmp.dist('aluminum', 'Catalan')
        0.8823529411764706
        >>> cmp.dist('ATCG', 'TAGC')
        0.9090909090909091


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        return (b + c) / (a + b + c + 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
