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

"""abydos.distance.eudex.

The distance.eudex module implements eudex distance functions.
"""

from __future__ import division, unicode_literals

from types import GeneratorType

from six.moves import range

from ..phonetic import eudex

__all__ = ['dist_eudex', 'eudex_hamming', 'sim_eudex']


def eudex_hamming(
    src, tar, weights='exponential', max_length=8, normalized=False
):
    """Calculate the Hamming distance between the Eudex hashes of two terms.

    Cf. :cite:`Ticki:2016`.

    - If weights is set to None, a simple Hamming distance is calculated.
    - If weights is set to 'exponential', weight decays by powers of 2, as
      proposed in the eudex specification: https://github.com/ticki/eudex.
    - If weights is set to 'fibonacci', weight decays through the Fibonacci
      series, as in the eudex reference implementation.
    - If weights is set to a callable function, this assumes it creates a
      generator and the generator is used to populate a series of weights.
    - If weights is set to an iterable, the iterable's values should be
      integers and will be used as the weights.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str, iterable, or generator function weights: the weights or weights
        generator function
    :param max_length: the number of characters to encode as a eudex hash
    :param bool normalized: normalizes to [0, 1] if True
    :returns: the Eudex Hamming distance
    :rtype: int

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

    def _gen_fibonacci():
        """Yield the next Fibonacci number.

        Based on https://www.python-course.eu/generators.php
        Starts at Fibonacci number 3 (the second 1)

        :returns: the next Fibonacci number
        :rtype: int
        """
        num_a, num_b = 1, 2
        while True:
            yield num_a
            num_a, num_b = num_b, num_a + num_b

    def _gen_exponential(base=2):
        """Yield the next value in an exponential series of the base.

        Starts at base**0

        :param int base: the base to exponentiate
        :returns: the next power of `base`
        :rtype: int
        """
        exp = 0
        while True:
            yield base ** exp
            exp += 1

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
        weights = _gen_exponential()
    elif weights == 'fibonacci':
        weights = _gen_fibonacci()
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


def dist_eudex(src, tar, weights='exponential', max_length=8):
    """Return normalized Hamming distance between Eudex hashes of two terms.

    This is Eudex distance normalized to [0, 1].

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str, iterable, or generator function weights: the weights or weights
        generator function
    :param max_length: the number of characters to encode as a eudex hash
    :returns: the normalized Eudex distance
    :rtype: float

    >>> round(dist_eudex('cat', 'hat'), 12)
    0.062745098039
    >>> round(dist_eudex('Niall', 'Neil'), 12)
    0.000980392157
    >>> round(dist_eudex('Colin', 'Cuilen'), 12)
    0.004901960784
    >>> round(dist_eudex('ATCG', 'TAGC'), 12)
    0.197549019608
    """
    return eudex_hamming(src, tar, weights, max_length, True)


def sim_eudex(src, tar, weights='exponential', max_length=8):
    """Return normalized Hamming similarity between Eudex hashes of two terms.

    Normalized Eudex similarity is the complement of normalized Eudex distance:
    :math:`sim_{Eudex} = 1 - dist_{Eudex}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param str, iterable, or generator function weights: the weights or weights
        generator function
    :param max_length: the number of characters to encode as a eudex hash
    :returns: the normalized Eudex similarity
    :rtype: float

    >>> round(sim_eudex('cat', 'hat'), 12)
    0.937254901961
    >>> round(sim_eudex('Niall', 'Neil'), 12)
    0.999019607843
    >>> round(sim_eudex('Colin', 'Cuilen'), 12)
    0.995098039216
    >>> round(sim_eudex('ATCG', 'TAGC'), 12)
    0.802450980392
    """
    return 1 - dist_eudex(src, tar, weights, max_length)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
