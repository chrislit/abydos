# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.distance._cosine.

Cosine similarity & distance
"""

from math import sqrt
from typing import Optional

from ._token_distance import _TokenDistance
from ..tokenizer import _Tokenizer

__all__ = ['Cosine']


class Cosine(_TokenDistance):
    r"""Cosine similarity.

    For two sets X and Y, the cosine similarity, Otsuka-Ochiai coefficient, or
    Ochiai coefficient :cite:`Otsuka:1936,Ochiai:1957` is

        .. math::

            sim_{cosine}(X, Y) = \frac{|X \cap Y|}{\sqrt{|X| \cdot |Y|}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{cosine} =
            \frac{a}{\sqrt{(a+b)(a+c)}}

    Notes
    -----
    This measure is also known as the Fowlkes-Mallows index
    :cite:`Fowlkes:1983` for two classes and G-measure, the geometric mean of
    precision & recall.


    .. versionadded:: 0.3.6

    """

    def __init__(
        self,
        tokenizer: Optional[_Tokenizer] = None,
        intersection_type: str = 'crisp',
        **kwargs
    ):
        """Initialize Cosine instance.

        Parameters
        ----------
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
        super(Cosine, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src: str, tar: str) -> float:
        r"""Return the cosine similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Cosine similarity

        Examples
        --------
        >>> cmp = Cosine()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3651483716701107
        >>> cmp.sim('aluminum', 'Catalan')
        0.11785113019775793
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        num = self._intersection_card()

        if num:
            return num / sqrt(self._src_card() * self._tar_card())
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
