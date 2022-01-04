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

"""abydos.distance._stuart_tau.

Stuart's Tau correlation
"""

from typing import Any, Counter as TCounter, Optional, Sequence, Set, Union

from ._token_distance import _TokenDistance
from ..tokenizer import _Tokenizer

__all__ = ['StuartTau']


class StuartTau(_TokenDistance):
    r"""Stuart's Tau correlation.

    For two sets X and Y and a population N, Stuart's Tau-C correlation
    :cite:`Stuart:1953` is

        .. math::

            corr_{Stuart_{\tau_c}}(X, Y) =
            \frac{4 \cdot (|X \cap Y| + |(N \setminus X) \setminus Y| -
            |X \triangle Y|)}{|N|^2}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{Stuart_{\tau_c}} =
            \frac{4 \cdot ((a+d)-(b+c))}{n^2}

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
        """Initialize StuartTau instance.

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
        """Return the Stuart's Tau correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Stuart's Tau correlation

        Examples
        --------
        >>> cmp = StuartTau()
        >>> cmp.corr('cat', 'hat')
        0.005049979175343606
        >>> cmp.corr('Niall', 'Neil')
        0.005010932944606414
        >>> cmp.corr('aluminum', 'Catalan')
        0.004900807334983164
        >>> cmp.corr('ATCG', 'TAGC')
        0.0049718867138692216


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        if not n:
            return 1.0
        return max(-1.0, min(1.0, 4 * (a + d - b - c) / (n ** 2)))

    def sim(self, src: str, tar: str) -> float:
        """Return the Stuart's Tau similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Stuart's Tau similarity

        Examples
        --------
        >>> cmp = StuartTau()
        >>> cmp.sim('cat', 'hat')
        0.5025249895876718
        >>> cmp.sim('Niall', 'Neil')
        0.5025054664723032
        >>> cmp.sim('aluminum', 'Catalan')
        0.5024504036674916
        >>> cmp.sim('ATCG', 'TAGC')
        0.5024859433569346


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
