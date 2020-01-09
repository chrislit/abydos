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

"""abydos.distance._baulieu_x.

Baulieu X distance
"""

from ._token_distance import _TokenDistance

__all__ = ['BaulieuX']


class BaulieuX(_TokenDistance):
    r"""Baulieu X distance.

    For two sets X and Y and a population N, Baulieu X distance
    :cite:`Baulieu:1997` is

        .. math::

            dist_{BaulieuX}(X, Y) = \frac{|X \setminus Y| + |Y \setminus X| +
            max(|X \setminus Y|, |Y \setminus X|)}{|N| +
            max(|X \setminus Y|, |Y \setminus X|)}

    This is Baulieu's 28th dissimilarity coefficient. This coefficient fails
    Baulieu's (P8) property, that :math:`D` is a rational function whose
    numerator and denominator are both (total) linear.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{BaulieuX} = \frac{b+c+max(b,c)}{n+max(b,c)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize BaulieuX instance.

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
        super(BaulieuX, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Baulieu X distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baulieu X distance

        Examples
        --------
        >>> cmp = BaulieuX()
        >>> cmp.dist('cat', 'hat')
        0.007633587786259542
        >>> cmp.dist('Niall', 'Neil')
        0.013959390862944163
        >>> cmp.dist('aluminum', 'Catalan')
        0.029003783102143757
        >>> cmp.dist('ATCG', 'TAGC')
        0.019011406844106463


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        b = self._src_only_card()
        c = self._tar_only_card()
        n = self._population_unique_card()

        num = b + c + max(b, c)

        if num == 0.0:
            return 0.0
        return num / (n + max(b, c))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
