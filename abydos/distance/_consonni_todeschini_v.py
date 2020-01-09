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

"""abydos.distance._consonni_todeschini_v.

Consonni & Todeschini V correlation
"""

from math import log1p

from ._token_distance import _TokenDistance

__all__ = ['ConsonniTodeschiniV']


class ConsonniTodeschiniV(_TokenDistance):
    r"""Consonni & Todeschini V correlation.

    For two sets X and Y and a population N, Consonni & Todeschini V
    correlation :cite:`Consonni:2012` is

        .. math::

            corr_{ConsonniTodeschiniV}(X, Y) =
            \frac{log(1+|X \cap Y| \cdot |(N \setminus X) \setminus Y|)-
            log(1+|X \setminus Y| \cdot |Y \setminus X|)}
            {log(1+\frac{|N|^2}{4})}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{ConsonniTodeschiniV} =
            \frac{log(1+ad)-log(1+bc)}{log(1+\frac{n^2}{4})}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize ConsonniTodeschiniV instance.

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
        super(ConsonniTodeschiniV, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Consonni & Todeschini V correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Consonni & Todeschini V correlation

        Examples
        --------
        >>> cmp = ConsonniTodeschiniV()
        >>> cmp.corr('cat', 'hat')
        0.48072545510682463
        >>> cmp.corr('Niall', 'Neil')
        0.4003930264973547
        >>> cmp.corr('aluminum', 'Catalan')
        0.21794239483504532
        >>> cmp.corr('ATCG', 'TAGC')
        -0.2728145951429799


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        num = log1p(a * d) - log1p(b * c)
        if num == 0.0:
            return 0.0

        return num / log1p(n ** 2 / 4)

    def sim(self, src, tar):
        """Return the Consonni & Todeschini V similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Consonni & Todeschini V similarity

        Examples
        --------
        >>> cmp = ConsonniTodeschiniV()
        >>> cmp.sim('cat', 'hat')
        0.7403627275534124
        >>> cmp.sim('Niall', 'Neil')
        0.7001965132486774
        >>> cmp.sim('aluminum', 'Catalan')
        0.6089711974175227
        >>> cmp.sim('ATCG', 'TAGC')
        0.36359270242851005


        .. versionadded:: 0.4.0

        """
        return (1 + self.corr(src, tar)) / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
