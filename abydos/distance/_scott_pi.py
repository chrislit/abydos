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

"""abydos.distance._scott_pi.

Scott's Pi correlation
"""

from typing import Any, Counter as TCounter, Optional, Sequence, Set, Union

from ._token_distance import _TokenDistance
from ..tokenizer import _Tokenizer

__all__ = ['ScottPi']


class ScottPi(_TokenDistance):
    r"""Scott's Pi correlation.

    For two sets X and Y and a population N, Scott's :math:`\pi` correlation
    :cite:`Scott:1955` is

        .. math::

            corr_{Scott_\pi}(X, Y) = \pi =
            \frac{p_o - p_e^\pi}{1 - p_e^\pi}

    where

        .. math::

            \begin{array}{ll}
            p_o &= \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}{|N|}

            p_e^\pi &= \Big(\frac{|X| + |Y|}{2 \cdot |N|}\Big)^2 +
            \Big(\frac{|N \setminus X| + |N \setminus Y|}{2 \cdot |N|}\Big)^2
            \end{array}


    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            \begin{array}{ll}
            p_o &= \frac{a+d}{n}

            p_e^\pi &= \Big(\frac{2a+b+c}{2n}\Big)^2 +
            \Big(\frac{2d+b+c}{2n}\Big)^2
            \end{array}


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
        """Initialize ScottPi instance.

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
        """Return the Scott's Pi correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Scott's Pi correlation

        Examples
        --------
        >>> cmp = ScottPi()
        >>> cmp.corr('cat', 'hat')
        0.49743589743589733
        >>> cmp.corr('Niall', 'Neil')
        0.35914053833129245
        >>> cmp.corr('aluminum', 'Catalan')
        0.10798833377524023
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006418485237489689


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = a + b + c + d

        po = (a + d) / n
        pe = ((2 * a + b + c) / (2 * n)) ** 2 + (
            (2 * d + b + c) / (2 * n)
        ) ** 2

        if po != pe:
            return (po - pe) / (1 - pe)
        return 0.0

    def sim(self, src: str, tar: str) -> float:
        """Return the Scott's Pi similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Scott's Pi similarity

        Examples
        --------
        >>> cmp = ScottPi()
        >>> cmp.sim('cat', 'hat')
        0.7487179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.6795702691656462
        >>> cmp.sim('aluminum', 'Catalan')
        0.5539941668876202
        >>> cmp.sim('ATCG', 'TAGC')
        0.49679075738125517


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
