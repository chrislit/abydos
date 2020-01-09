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

"""abydos.distance._baulieu_iii.

Baulieu III distance
"""

from ._token_distance import _TokenDistance

__all__ = ['BaulieuIII']


class BaulieuIII(_TokenDistance):
    r"""Baulieu III distance.

    For two sets X and Y and a population N, Baulieu III distance
    :cite:`Baulieu:1989` is

        .. math::

            sim_{BaulieuIII}(X, Y) =
            \frac{|N|^2 - 4(|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)}{2 \cdot |N|^2}

    This is based on Baulieu's 20th dissimilarity coefficient.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{BaulieuIII} =
            \frac{n^2 - 4(ad-bc)}{2n^2}

    Notes
    -----
    It should be noted that this is *based on* Baulieu's 20th dissimilarity
    coefficient. This distance is exactly half Baulieu's 20th dissimilarity.
    According to :cite:`Baulieu:1989`, the 20th dissimilarity should be a
    value in the range [0.0, 1.0], meeting the article's (P1) property, but the
    formula given ranges [0.0, 2.0], so dividing by 2 corrects the formula to
    meet the article's expectations.


    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize BaulieuIII instance.

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
        super(BaulieuIII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Baulieu III distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baulieu III distance

        Examples
        --------
        >>> cmp = BaulieuIII()
        >>> cmp.dist('cat', 'hat')
        0.4949500208246564
        >>> cmp.dist('Niall', 'Neil')
        0.4949955747605165
        >>> cmp.dist('aluminum', 'Catalan')
        0.49768591017891195
        >>> cmp.dist('ATCG', 'TAGC')
        0.5000813463140358


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        num = n * n - 4 * (a * d - b * c)

        if num == 0:
            return 0.0
        return num / (2 * n * n)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
