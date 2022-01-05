# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.distance._baroni_urbani_buser_ii.

Baroni-Urbani & Buser II correlation
"""

from typing import Any, Counter as TCounter, Optional, Sequence, Set, Union

from ._token_distance import _TokenDistance
from ..tokenizer import _Tokenizer

__all__ = ['BaroniUrbaniBuserII']


class BaroniUrbaniBuserII(_TokenDistance):
    r"""Baroni-Urbani & Buser II correlation.

    For two sets X and Y and a population N, the Baroni-Urbani & Buser II
    correlation :cite:`BaroniUrbani:1976` is

        .. math::

            corr_{BaroniUrbaniBuserII}(X, Y) =
            \frac{\sqrt{|X \cap Y| \cdot |(N \setminus X) \setminus Y|} +
            |X \cap Y| - |X \setminus Y| - |Y \setminus X|}
            {\sqrt{|X \cap Y| \cdot |(N \setminus X) \setminus Y|} +
            |X \cap Y| + |X \setminus Y| + |Y \setminus X|}

    This is the first, but less commonly used and referenced of the two
    similarities proposed by Baroni-Urbani & Buser.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{BaroniUrbaniBuserII} =
            \frac{\sqrt{ad}+a-b-c}{\sqrt{ad}+a+b+c}

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
        """Initialize BaroniUrbaniBuserII instance.

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
        """Return the Baroni-Urbani & Buser II correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baroni-Urbani & Buser II correlation

        Examples
        --------
        >>> cmp = BaroniUrbaniBuserII()
        >>> cmp.corr('cat', 'hat')
        0.8239675481756209
        >>> cmp.corr('Niall', 'Neil')
        0.7105646350028408
        >>> cmp.corr('aluminum', 'Catalan')
        0.31398542410970204
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        return ((a * d) ** 0.5 + a - b - c) / ((a * d) ** 0.5 + a + b + c)

    def sim(self, src: str, tar: str) -> float:
        """Return the Baroni-Urbani & Buser II similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Baroni-Urbani & Buser II similarity

        Examples
        --------
        >>> cmp = BaroniUrbaniBuserII()
        >>> cmp.sim('cat', 'hat')
        0.9119837740878105
        >>> cmp.sim('Niall', 'Neil')
        0.8552823175014204
        >>> cmp.sim('aluminum', 'Catalan')
        0.656992712054851
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (self.corr(src, tar) + 1) / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
