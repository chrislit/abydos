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

"""abydos.distance._eudex.

eudex distance functions
"""

from types import GeneratorType
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    List,
    Optional,
    Union,
    cast,
)

from ._distance import _Distance
from ..phonetic import Eudex as EudexPhonetic

__all__ = ['Eudex']


class Eudex(_Distance):
    """Distance between the Eudex hashes of two terms.

    Cf. :cite:`Ticki:2016`.

    .. versionadded:: 0.3.6
    """

    @staticmethod
    def gen_fibonacci() -> Generator[int, None, None]:
        """Yield the next Fibonacci number.

        Based on https://www.python-course.eu/generators.php
        Starts at Fibonacci number 3 (the second 1)

        Yields
        ------
        int
            The next Fibonacci number


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        num_a, num_b = 1, 2
        while True:
            yield num_a
            num_a, num_b = num_b, num_a + num_b

    @staticmethod
    def gen_exponential(base: int = 2) -> Generator[int, None, None]:
        """Yield the next value in an exponential series of the base.

        Starts at base**0

        Parameters
        ----------
        base : int
            The base to exponentiate

        Yields
        ------
        int
            The next power of `base`


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        exp = 0
        while True:
            yield base ** exp
            exp += 1

    def __init__(
        self,
        weights: Optional[
            Union[
                str,
                Iterable[float],
                Callable[[], Generator[int, None, None]],
            ]
        ] = 'exponential',
        max_length: int = 8,
        **kwargs: Any
    ) -> None:
        """Initialize Eudex instance.

        Parameters
        ----------
        weights : str, iterable, or generator function
            The weights or weights generator function

                - If set to ``None``, a simple Hamming distance is calculated.
                - If set to ``exponential``, weight decays by powers of 2, as
                  proposed in the eudex specification:
                  https://github.com/ticki/eudex.
                - If set to ``fibonacci``, weight decays through the Fibonacci
                  series, as in the eudex reference implementation.
                - If set to a callable function, this assumes it creates a
                  generator and the generator is used to populate a series of
                  weights.
                - If set to an iterable, the iterable's values should be
                  integers and will be used as the weights.

            In all cases, the weights should be ordered or generated from least
            significant to most significant, so larger values should generally
            come first.

        max_length : int
            The number of characters to encode as a eudex hash
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(Eudex, self).__init__(**kwargs)
        self._weights = weights
        self._max_length = max_length
        self._phonetic_alg = EudexPhonetic(max_length=max_length)

    def dist_abs(
        self, src: str, tar: str, normalized: bool = False
    ) -> float:
        """Calculate the distance between the Eudex hashes of two terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        normalized : bool
            Normalizes to [0, 1] if True

        Returns
        -------
        int
            The Eudex Hamming distance

        Examples
        --------
        >>> cmp = Eudex()
        >>> cmp.dist_abs('cat', 'hat')
        128
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('Colin', 'Cuilen')
        10
        >>> cmp.dist_abs('ATCG', 'TAGC')
        403

        >>> cmp = Eudex(weights='fibonacci')
        >>> cmp.dist_abs('cat', 'hat')
        34
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('Colin', 'Cuilen')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        117

        >>> cmp = Eudex(weights=None)
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        1
        >>> cmp.dist_abs('Colin', 'Cuilen')
        2
        >>> cmp.dist_abs('ATCG', 'TAGC')
        9

        >>> # Using the OEIS A000142:
        >>> cmp = Eudex(weights=[1, 1, 2, 6, 24, 120, 720, 5040])
        >>> cmp.dist_abs('cat', 'hat')
        5040
        >>> cmp.dist_abs('Niall', 'Neil')
        1
        >>> cmp.dist_abs('Colin', 'Cuilen')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        15130


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """

        # Calculate the eudex hashes and XOR them
        xored = int(self._phonetic_alg.encode(src)) ^ int(
            self._phonetic_alg.encode(tar)
        )

        # Simple hamming distance (all bits are equal)
        if not self._weights:
            binary = bin(xored)
            distance = binary.count('1')  # type: float
            if normalized:
                return distance / (len(binary) - 2)
            return distance

        # If self._weights is a function, it should create a generator,
        # which we now use to populate a list
        if hasattr(self._weights, '__iter__') and not isinstance(
            self._weights, str
        ):
            weights_list = cast(List[float], self._weights)[::-1]
            weights_gen = None
        elif callable(self._weights):
            weights_gen = self._weights()
        elif self._weights == 'exponential':
            weights_gen = Eudex.gen_exponential()
        elif self._weights == 'fibonacci':
            weights_gen = Eudex.gen_fibonacci()
        else:
            raise ValueError('Unrecognized weights value or type.')

        if isinstance(weights_gen, GeneratorType):
            weights_list = [
                next(weights_gen) for _ in range(self._max_length)
            ][::-1]

        # Sum the weighted hamming distance
        distance = 0
        max_distance = 0  # type: float
        while (xored or normalized) and weights_list:
            max_distance += 8 * weights_list[-1]
            distance += bin(xored & 0xFF).count('1') * weights_list.pop()
            xored >>= 8

        if normalized:
            distance /= max_distance

        return distance

    def dist(self, src: str, tar: str) -> float:
        """Return normalized distance between the Eudex hashes of two terms.

        This is Eudex distance normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The normalized Eudex Hamming distance

        Examples
        --------
        >>> cmp = Eudex()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.062745098039
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.000980392157
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.004901960784
        >>> round(cmp.dist('ATCG', 'TAGC'), 12)
        0.197549019608


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return self.dist_abs(src, tar, True)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
