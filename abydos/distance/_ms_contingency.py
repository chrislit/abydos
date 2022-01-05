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

"""abydos.distance._ms_contingency.

Mean squared contingency correlation
"""

from typing import Any, Counter as TCounter, Optional, Sequence, Set, Union

from ._token_distance import _TokenDistance
from ..tokenizer import _Tokenizer

__all__ = ['MSContingency']


class MSContingency(_TokenDistance):
    r"""Mean squared contingency correlation.

    For two sets X and Y and a population N, the mean squared contingency
    correlation :cite:`Cole:1949` is

        .. math::

            corr_{MSContingency}(X, Y) =
            \frac{\sqrt{2}(|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)}
            {\sqrt{(|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)^2 +
            |X| \cdot |Y| \cdot |N \setminus X| \cdot |N \setminus Y|}}

    :cite:`Hubalek:1982` and :cite:`Choi:2010` identify this as Cole
    similarity. Although Cole discusses this correlation, he does not claim to
    have developed it. Rather, he presents his coefficient of interspecific
    association as being his own development: :class:`.Cole`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{MSContingency} =
            \frac{\sqrt{2}(ad-bc)}{\sqrt{(ad-bc)^2+(a+b)(a+c)(b+d)(c+d)}}

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
        """Initialize MSContingency instance.

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
        """Return the normalized mean squared contingency corr. of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Mean squared contingency correlation

        Examples
        --------
        >>> cmp = MSContingency()
        >>> cmp.corr('cat', 'hat')
        0.6298568508557214
        >>> cmp.corr('Niall', 'Neil')
        0.4798371954796814
        >>> cmp.corr('aluminum', 'Catalan')
        0.15214891090821628
        >>> cmp.corr('ATCG', 'TAGC')
        -0.009076921903905553


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return -1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        ab = self._src_card()
        ac = self._tar_card()
        admbc = a * d - b * c

        if admbc:
            return (
                2 ** 0.5
                * admbc
                / (admbc ** 2 + ab * ac * (b + d) * (c + d)) ** 0.5
            )
        return 0.0

    def sim(self, src: str, tar: str) -> float:
        """Return the normalized ms contingency similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Mean squared contingency similarity

        Examples
        --------
        >>> cmp = MSContingency()
        >>> cmp.sim('cat', 'hat')
        0.8149284254278607
        >>> cmp.sim('Niall', 'Neil')
        0.7399185977398407
        >>> cmp.sim('aluminum', 'Catalan')
        0.5760744554541082
        >>> cmp.sim('ATCG', 'TAGC')
        0.49546153904804724


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
