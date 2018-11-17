# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from types import GeneratorType

from six.moves import range

from ._distance import _Distance
from ..phonetic import eudex

__all__ = ['Eudex', 'dist_eudex', 'eudex_hamming', 'sim_eudex']


class Eudex(_Distance):
    """Distance between the Eudex hashes of two terms.

    Cf. :cite:`Ticki:2016`.
    """

    @staticmethod
    def gen_fibonacci():
        """Yield the next Fibonacci number.

        Based on https://www.python-course.eu/generators.php
        Starts at Fibonacci number 3 (the second 1)

        Yields
        ------
        int
            The next Fibonacci number

        """
        num_a, num_b = 1, 2
        while True:
            yield num_a
            num_a, num_b = num_b, num_a + num_b

    @staticmethod
    def gen_exponential(base=2):
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

        """
        exp = 0
        while True:
            yield base ** exp
            exp += 1

    def dist_abs(
        self, src, tar, weights='exponential', max_length=8, normalized=False
    ):
        """Calculate the distance between the Eudex hashes of two terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
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

        max_length : int
            The number of characters to encode as a eudex hash
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

        >>> cmp.dist_abs('cat', 'hat', weights='fibonacci')
        34
        >>> cmp.dist_abs('Niall', 'Neil', weights='fibonacci')
        2
        >>> cmp.dist_abs('Colin', 'Cuilen', weights='fibonacci')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC', weights='fibonacci')
        117

        >>> cmp.dist_abs('cat', 'hat', weights=None)
        1
        >>> cmp.dist_abs('Niall', 'Neil', weights=None)
        1
        >>> cmp.dist_abs('Colin', 'Cuilen', weights=None)
        2
        >>> cmp.dist_abs('ATCG', 'TAGC', weights=None)
        9

        >>> # Using the OEIS A000142:
        >>> cmp.dist_abs('cat', 'hat', [1, 1, 2, 6, 24, 120, 720, 5040])
        1
        >>> cmp.dist_abs('Niall', 'Neil', [1, 1, 2, 6, 24, 120, 720, 5040])
        720
        >>> cmp.dist_abs('Colin', 'Cuilen',
        ... [1, 1, 2, 6, 24, 120, 720, 5040])
        744
        >>> cmp.dist_abs('ATCG', 'TAGC', [1, 1, 2, 6, 24, 120, 720, 5040])
        6243

        """
        # Calculate the eudex hashes and XOR them
        xored = eudex(src, max_length=max_length) ^ eudex(
            tar, max_length=max_length
        )

        # Simple hamming distance (all bits are equal)
        if not weights:
            binary = bin(xored)
            distance = binary.count('1')
            if normalized:
                return distance / (len(binary) - 2)
            return distance

        # If weights is a function, it should create a generator,
        # which we now use to populate a list
        if callable(weights):
            weights = weights()
        elif weights == 'exponential':
            weights = Eudex.gen_exponential()
        elif weights == 'fibonacci':
            weights = Eudex.gen_fibonacci()
        if isinstance(weights, GeneratorType):
            weights = [next(weights) for _ in range(max_length)][::-1]

        # Sum the weighted hamming distance
        distance = 0
        max_distance = 0
        while (xored or normalized) and weights:
            max_distance += 8 * weights[-1]
            distance += bin(xored & 0xFF).count('1') * weights.pop()
            xored >>= 8

        if normalized:
            distance /= max_distance

        return distance

    def dist(self, src, tar, weights='exponential', max_length=8):
        """Return normalized distance between the Eudex hashes of two terms.

        This is Eudex distance normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        weights : str, iterable, or generator function
            The weights or weights generator function
        max_length : int
            The number of characters to encode as a eudex hash

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

        """
        return self.dist_abs(src, tar, weights, max_length, True)


def eudex_hamming(
    src, tar, weights='exponential', max_length=8, normalized=False
):
    """Calculate the Hamming distance between the Eudex hashes of two terms.

    This is a wrapper for :py:meth:`Eudex.eudex_hamming`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    weights : str, iterable, or generator function
        The weights or weights generator function
    max_length : int
        The number of characters to encode as a eudex hash
    normalized : bool
        Normalizes to [0, 1] if True

    Returns
    -------
    int
        The Eudex Hamming distance

    Examples
    --------
    >>> eudex_hamming('cat', 'hat')
    128
    >>> eudex_hamming('Niall', 'Neil')
    2
    >>> eudex_hamming('Colin', 'Cuilen')
    10
    >>> eudex_hamming('ATCG', 'TAGC')
    403

    >>> eudex_hamming('cat', 'hat', weights='fibonacci')
    34
    >>> eudex_hamming('Niall', 'Neil', weights='fibonacci')
    2
    >>> eudex_hamming('Colin', 'Cuilen', weights='fibonacci')
    7
    >>> eudex_hamming('ATCG', 'TAGC', weights='fibonacci')
    117

    >>> eudex_hamming('cat', 'hat', weights=None)
    1
    >>> eudex_hamming('Niall', 'Neil', weights=None)
    1
    >>> eudex_hamming('Colin', 'Cuilen', weights=None)
    2
    >>> eudex_hamming('ATCG', 'TAGC', weights=None)
    9

    >>> # Using the OEIS A000142:
    >>> eudex_hamming('cat', 'hat', [1, 1, 2, 6, 24, 120, 720, 5040])
    1
    >>> eudex_hamming('Niall', 'Neil', [1, 1, 2, 6, 24, 120, 720, 5040])
    720
    >>> eudex_hamming('Colin', 'Cuilen', [1, 1, 2, 6, 24, 120, 720, 5040])
    744
    >>> eudex_hamming('ATCG', 'TAGC', [1, 1, 2, 6, 24, 120, 720, 5040])
    6243

    """
    return Eudex().dist_abs(src, tar, weights, max_length, normalized)


def dist_eudex(src, tar, weights='exponential', max_length=8):
    """Return normalized Hamming distance between Eudex hashes of two terms.

    This is a wrapper for :py:meth:`Eudex.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    weights : str, iterable, or generator function
        The weights or weights generator function
    max_length : int
        The number of characters to encode as a eudex hash

    Returns
    -------
    int
        The normalized Eudex Hamming distance

    Examples
    --------
    >>> round(dist_eudex('cat', 'hat'), 12)
    0.062745098039
    >>> round(dist_eudex('Niall', 'Neil'), 12)
    0.000980392157
    >>> round(dist_eudex('Colin', 'Cuilen'), 12)
    0.004901960784
    >>> round(dist_eudex('ATCG', 'TAGC'), 12)
    0.197549019608

    """
    return Eudex().dist(src, tar, weights, max_length)


def sim_eudex(src, tar, weights='exponential', max_length=8):
    """Return normalized Hamming similarity between Eudex hashes of two terms.

    This is a wrapper for :py:meth:`Eudex.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    weights : str, iterable, or generator function
        The weights or weights generator function
    max_length : int
        The number of characters to encode as a eudex hash

    Returns
    -------
    int
        The normalized Eudex Hamming similarity

    Examples
    --------
    >>> round(sim_eudex('cat', 'hat'), 12)
    0.937254901961
    >>> round(sim_eudex('Niall', 'Neil'), 12)
    0.999019607843
    >>> round(sim_eudex('Colin', 'Cuilen'), 12)
    0.995098039216
    >>> round(sim_eudex('ATCG', 'TAGC'), 12)
    0.802450980392

    """
    return Eudex().sim(src, tar, weights, max_length)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
