# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.distance._dice.

Sørensen–Dice coefficient & distance
"""

from typing import Any, Optional

from ._tversky import Tversky
from ..tokenizer import _Tokenizer

__all__ = ['Dice']


class Dice(Tversky):
    r"""Sørensen–Dice coefficient.

    For two sets X and Y, the Sørensen–Dice coefficient
    :cite:`Dice:1945,Sorensen:1948,Czekanowski:1909,Motyka:1950` is

        .. math::

            sim_{Dice}(X, Y) = \frac{2 \cdot |X \cap Y|}{|X| + |Y|}

    This is the complement of Bray & Curtis dissimilarity :cite:`Bray:1957`,
    also known as the Lance & Williams dissimilarity :cite:`Lance:1967`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958` and the Tversky index :cite:`Tversky:1977` for
    :math:`\alpha = \beta = 0.5`.

    In the Ruby text library this is identified as White similarity, after
    :cite:`White:Nd`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Dice} =
            \frac{2a}{2a+b+c}

    Notes
    -----
    In terms of a confusion matrix, this is equivalent to :math:`F_1` score
    :py:meth:`ConfusionTable.f1_score`.

    The multiset variant is termed Gleason similarity :cite:`Gleason:1920`.

    .. versionadded:: 0.3.6

    """

    def __init__(
        self,
        tokenizer: Optional[_Tokenizer] = None,
        intersection_type: str = 'crisp',
        **kwargs: Any
    ) -> None:
        """Initialize Dice instance.

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
        super().__init__(
            alpha=0.5,
            beta=0.5,
            bias=None,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src: str, tar: str) -> float:
        """Return the Sørensen–Dice coefficient of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Sørensen–Dice similarity

        Examples
        --------
        >>> cmp = Dice()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.36363636363636365
        >>> cmp.sim('aluminum', 'Catalan')
        0.11764705882352941
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return super().sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
