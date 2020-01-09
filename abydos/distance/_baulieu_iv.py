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

"""abydos.distance._baulieu_iv.

Baulieu IV distance
"""

from math import e

from ._token_distance import _TokenDistance

__all__ = ['BaulieuIV']


class BaulieuIV(_TokenDistance):
    r"""Baulieu IV distance.

    For two sets X and Y, a population N, and a positive irractional number k,
    Baulieu IV distance :cite:`Baulieu:1997` is

        .. math::

            dist_{BaulieuIV}(X, Y) = \frac{|X \setminus Y| + |Y \setminus X| -
            (|X \cap Y| + \frac{1}{2}) \cdot (|(N \setminus X) \setminus Y| +
            \frac{1}{2}) \cdot |(N \setminus X) \setminus Y| \cdot k}{|N|}

    This is Baulieu's 22nd dissimilarity coefficient.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{BaulieuIV} = \frac{b+c-(a+\frac{1}{2})(d+\frac{1}{2})dk}{n}

    Notes
    -----
    The default value of k is Euler's number :math:`e`, but other irrationals
    such as :math:`\pi` or :math:`\sqrt{2}` could be substituted at
    initialization.


    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        positive_irrational=e,
        **kwargs
    ):
        """Initialize BaulieuIV instance.

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
        super(BaulieuIV, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )
        self._positive_irrational = positive_irrational

    def dist_abs(self, src, tar):
        """Return the Baulieu IV distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baulieu IV distance

        Examples
        --------
        >>> cmp = BaulieuIV()
        >>> cmp.dist_abs('cat', 'hat')
        -5249.96272285802
        >>> cmp.dist_abs('Niall', 'Neil')
        -5209.561726488335
        >>> cmp.dist_abs('aluminum', 'Catalan')
        -3073.6070822721244
        >>> cmp.dist_abs('ATCG', 'TAGC')
        -1039.2151656463932


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()
        k = self._positive_irrational

        num = (b + c) - (a + 0.5) * (d + 0.5) * d * k

        if num == 0.0:
            return 0.0
        return num / n

    def dist(self, src, tar):
        """Return the normalized Baulieu IV distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Baulieu IV distance

        Examples
        --------
        >>> cmp = BaulieuIV()
        >>> cmp.dist('cat', 'hat')
        0.49999799606535283
        >>> cmp.dist('Niall', 'Neil')
        0.49999801148659684
        >>> cmp.dist('aluminum', 'Catalan')
        0.49999883126809364
        >>> cmp.dist('ATCG', 'TAGC')
        0.4999996033268451


        .. versionadded:: 0.4.0

        """
        distance = self.dist_abs(src, tar)
        n3 = self._population_unique_card() ** 3
        k = self._positive_irrational

        num = distance + n3 * k

        if num == 0.0:
            return 0.0
        return (distance + n3 * k) / (2 * n3 * k)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
