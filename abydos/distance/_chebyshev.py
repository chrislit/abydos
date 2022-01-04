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

"""abydos.distance._chebyshev.

Chebyshev distance
"""

from typing import (
    Any,
    Counter as TCounter,
    NoReturn,
    Optional,
    Sequence,
    Set,
    Union,
)

from ._minkowski import Minkowski
from ..tokenizer import _Tokenizer

__all__ = ['Chebyshev']


class Chebyshev(Minkowski):
    r"""Chebyshev distance.

    Euclidean distance is the chessboard distance,
    equivalent to Minkowski distance in :math:`L^\infty`-space.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self,
        alphabet: Optional[
            Union[TCounter[str], Sequence[str], Set[str], int]
        ] = 0,
        tokenizer: Optional[_Tokenizer] = None,
        intersection_type: str = 'crisp',
        **kwargs: Any
    ) -> None:
        """Initialize Euclidean instance.

        Parameters
        ----------
        alphabet : collection or int
            The values or size of the alphabet
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
            pval=float('inf'),
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist_abs(self, src: str, tar: str, *args: Any, **kwargs: Any) -> float:
        r"""Return the Chebyshev distance between two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            The Chebyshev distance

        Examples
        --------
        >>> cmp = Chebyshev()
        >>> cmp.dist_abs('cat', 'hat')
        1.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        1.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.0

        >>> cmp = Chebyshev(qval=1)
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.0
        >>> cmp.dist_abs('ATCGATTCGGAATTTC', 'TAGCATAATCGCCG')
        3.0


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return super().dist_abs(src, tar, False)

    def sim(self, *args: Any, **kwargs: Any) -> NoReturn:
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Chebyshev distance


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError('Method disabled for Chebyshev distance.')

    def dist(self, *args: Any, **kwargs: Any) -> NoReturn:
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Chebyshev distance


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError('Method disabled for Chebyshev distance.')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
