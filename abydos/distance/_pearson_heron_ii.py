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

"""abydos.distance._pearson_heron_ii.

Pearson & Heron II correlation
"""

from math import cos, pi

from ._token_distance import _TokenDistance

__all__ = ['PearsonHeronII']


class PearsonHeronII(_TokenDistance):
    r"""Pearson & Heron II correlation.

    For two sets X and Y and a population N, Pearson & Heron II correlation
    :cite:`Pearson:1913` is

        .. math::

            corr_{PearsonHeronII}(X, Y) =
            \cos \Big(\frac{\pi\sqrt{|X \setminus Y| \cdot |Y \setminus X|}}
            {\sqrt{|X \cap Y| \cdot |(N \setminus X) \setminus Y|} +
            \sqrt{|X \setminus Y| \cdot |Y \setminus X|}}\Big)

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{PearsonHeronII} =
            \cos \Big(\frac{\pi\sqrt{bc}}{\sqrt{ad}+\sqrt{bc}}\Big)

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize PearsonHeronII instance.

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
        super(PearsonHeronII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Pearson & Heron II correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson & Heron II correlation

        Examples
        --------
        >>> cmp = PearsonHeronII()
        >>> cmp.corr('cat', 'hat')
        0.9885309061036239
        >>> cmp.corr('Niall', 'Neil')
        0.9678978997263907
        >>> cmp.corr('aluminum', 'Catalan')
        0.7853000893691571
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return -1.0

        self._tokenize(src, tar)

        root_ad = (
            self._intersection_card() * self._total_complement_card()
        ) ** 0.5
        root_bc = (self._src_only_card() * self._tar_only_card()) ** 0.5

        num = pi * root_bc
        return cos((num / (root_ad + root_bc)) if num else 0.0)

    def sim(self, src, tar):
        """Return the Pearson & Heron II similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson & Heron II similarity

        Examples
        --------
        >>> cmp = PearsonHeronII()
        >>> cmp.sim('cat', 'hat')
        0.994265453051812
        >>> cmp.sim('Niall', 'Neil')
        0.9839489498631954
        >>> cmp.sim('aluminum', 'Catalan')
        0.8926500446845785
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
