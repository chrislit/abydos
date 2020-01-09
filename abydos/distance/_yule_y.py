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

"""abydos.distance._yule_y.

Yule's Y correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['YuleY']


class YuleY(_TokenDistance):
    r"""Yule's Y correlation.

    For two sets X and Y and a population N, Yule's Y correlation
    :cite:`Yule:1912` is

        .. math::

            corr_{Yule_Y}(X, Y) =
            \frac{\sqrt{|X \cap Y| \cdot |(N \setminus X) \setminus Y|} -
            \sqrt{|X \setminus Y| \cdot |Y \setminus X|}}
            {\sqrt{|X \cap Y| \cdot |(N \setminus X) \setminus Y|} +
            \sqrt{|X \setminus Y| \cdot |Y \setminus X|}}

    In :cite:`Yule:1912`, this is labeled :math:`\omega`, so it is sometimes
    referred to as Yule's :math:`\omega`. Yule himself terms this the
    coefficient of colligation.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{Yule_Y} =
            \frac{\sqrt{ad}-\sqrt{bc}}{\sqrt{ad}+\sqrt{bc}}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize YuleY instance.

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
        super(YuleY, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return Yule's Y correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Yule's Y correlation

        Examples
        --------
        >>> cmp = YuleY()
        >>> cmp.corr('cat', 'hat')
        0.9034892632818762
        >>> cmp.corr('Niall', 'Neil')
        0.8382551144735259
        >>> cmp.corr('aluminum', 'Catalan')
        0.5749826820237787
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        admbc = (a * d) ** 0.5 - (b * c) ** 0.5
        if admbc:
            return admbc / ((a * d) ** 0.5 + (b * c) ** 0.5)
        return 0.0

    def sim(self, src, tar):
        """Return Yule's Y similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Yule's Y similarity

        Examples
        --------
        >>> cmp = YuleY()
        >>> cmp.sim('cat', 'hat')
        0.9517446316409381
        >>> cmp.sim('Niall', 'Neil')
        0.919127557236763
        >>> cmp.sim('aluminum', 'Catalan')
        0.7874913410118893
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
