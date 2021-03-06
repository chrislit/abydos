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

"""abydos.distance._dunning.

Dunning similarity
"""

from math import log
from typing import Any, Counter as TCounter, Optional, Sequence, Set, Union

from ._token_distance import _TokenDistance
from ..tokenizer import _Tokenizer

__all__ = ['Dunning']


class Dunning(_TokenDistance):
    r"""Dunning similarity.

    For two sets X and Y and a population N, Dunning log-likelihood
    :cite:`Dunning:1993`, following :cite:`Church:1991`, is

        .. math::

            sim_{Dunning}(X, Y) = \lambda =
            |X \cap Y| \cdot log_2(|X \cap Y|) +\\
            |X \setminus Y| \cdot log_2(|X \setminus Y|) +
            |Y \setminus X| \cdot log_2(|Y \setminus X|) +\\
            |(N \setminus X) \setminus Y| \cdot
            log_2(|(N \setminus X) \setminus Y|) -\\
            (|X| \cdot log_2(|X|) +
            |Y| \cdot log_2(|Y|) +\\
            |N \setminus Y| \cdot log_2(|N \setminus Y|) +
            |N \setminus X| \cdot log_2(|N \setminus X|))


    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Dunning} = \lambda =
            a \cdot log_2(a) +\\
            b \cdot log_2(b) + c \cdot log_2(c) +
            d \cdot log_2(d) - \\
            ((a+b) \cdot log_2(a+b) + (a+c) \cdot log_2(a+c) +\\
            (b+d) \cdot log_2(b+d) + (c+d) log_2(c+d))

    Notes
    -----
    To avoid NaNs, every logarithm is calculated as the logarithm of 1 greater
    than the value in question. (Python's math.log1p function is used.)


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
        """Initialize Dunning instance.

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
        super(Dunning, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src: str, tar: str) -> float:
        """Return the Dunning similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Dunning similarity

        Examples
        --------
        >>> cmp = Dunning()
        >>> cmp.sim('cat', 'hat')
        0.33462839191969423
        >>> cmp.sim('Niall', 'Neil')
        0.19229445539929793
        >>> cmp.sim('aluminum', 'Catalan')
        0.03220862737070572
        >>> cmp.sim('ATCG', 'TAGC')
        0.0010606026735052122


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = a + b + c + d

        # a should not equal n, because 0 will result
        # As a workaround, we set d to 1 and add one to n.
        if a == n:
            d = 1
            n += 1

        a /= n
        b /= n
        c /= n
        d /= n

        score = 0.0
        for i in [a, b, c, d]:
            if i > 0:
                score += i * log(i)
        for i in [a, d]:
            for j in [b, c]:
                ij = i + j
                if ij > 0:
                    score -= ij * log(ij)
        score *= 2
        score /= log(2)

        return abs(round(score, 15))

    def sim(self, src: str, tar: str) -> float:
        """Return the normalized Dunning similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Dunning similarity

        Examples
        --------
        >>> cmp = Dunning()
        >>> cmp.sim('cat', 'hat')
        0.33462839191969423
        >>> cmp.sim('Niall', 'Neil')
        0.19229445539929793
        >>> cmp.sim('aluminum', 'Catalan')
        0.03220862737070572
        >>> cmp.sim('ATCG', 'TAGC')
        0.0010606026735052122


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        score = self.sim_score(src, tar)
        if not score:
            return 0.0

        norm = max(self.sim_score(src, src), self.sim_score(tar, tar))
        return score / norm


if __name__ == '__main__':
    import doctest

    doctest.testmod()
