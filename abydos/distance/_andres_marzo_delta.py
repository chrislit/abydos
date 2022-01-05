# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.distance._andres_marzo_delta.

Andres & Marzo's Delta correlation
"""

from typing import Any, Counter as TCounter, Optional, Sequence, Set, Union

from ._token_distance import _TokenDistance
from ..tokenizer import _Tokenizer

__all__ = ['AndresMarzoDelta']


class AndresMarzoDelta(_TokenDistance):
    r"""Andres & Marzo's Delta correlation.

    For two sets X and Y and a population N, Andres & Marzo's :math:`\Delta`
    correlation :cite:`Andres:2004` is

        .. math::

            corr_{AndresMarzo_\Delta}(X, Y) = \Delta =
            \frac{|X \cap Y| + |(N \setminus X) \setminus Y| -
            2\sqrt{|X \setminus Y| \cdot |Y \setminus X|}}{|N|}


    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{AndresMarzo_\Delta} = \Delta =
            \frac{a+d-2\sqrt{b \cdot c}}{n}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet: Optional[
            Union[TCounter[str], Sequence[str], Set[str], int]
        ] = None,
        tokenizer: Optional[_Tokenizer] = None,
        intersection_type: str = 'crisp',
        **kwargs: Any
    ) -> None:
        """Initialize AndresMarzoDelta instance.

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
        super().__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src: str, tar: str) -> float:
        """Return the Andres & Marzo's Delta correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Andres & Marzo's Delta correlation

        Examples
        --------
        >>> cmp = AndresMarzoDelta()
        >>> cmp.corr('cat', 'hat')
        0.9897959183673469
        >>> cmp.corr('Niall', 'Neil')
        0.9822344346552608
        >>> cmp.corr('aluminum', 'Catalan')
        0.9618259496215341
        >>> cmp.corr('ATCG', 'TAGC')
        0.9744897959183674


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        num = a + d - 2 * (b * c) ** 0.5

        if num == 0.0:
            return 0.0
        return num / n

    def sim(self, src: str, tar: str) -> float:
        """Return the Andres & Marzo's Delta similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Andres & Marzo's Delta similarity

        Examples
        --------
        >>> cmp = AndresMarzoDelta()
        >>> cmp.sim('cat', 'hat')
        0.9948979591836735
        >>> cmp.sim('Niall', 'Neil')
        0.9911172173276304
        >>> cmp.sim('aluminum', 'Catalan')
        0.980912974810767
        >>> cmp.sim('ATCG', 'TAGC')
        0.9872448979591837


        .. versionadded:: 0.4.0

        """
        return (self.corr(src, tar) + 1) / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
