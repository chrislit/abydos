# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

r"""abydos.stats._mean.

The stats._mean module defines functions for calculating various statistical
data about linguistic objects.

Functions are provided for calculating the following means:

    - arithmetic
    - geometric
    - harmonic
    - quadratic
    - contraharmonic
    - logarithmic
    - identric (exponential)
    - Seiffert's
    - Lehmer
    - Heronian
    - Hölder (power/generalized)
    - arithmetic-geometric
    - geometric-harmonic
    - arithmetic-geometric-harmonic

And for calculating:

    - midrange
    - median
    - mode
    - variance
    - standard deviation
"""

from __future__ import division, unicode_literals

import math
from collections import Counter

from six.moves import range

from ..util import prod

__all__ = [
    'aghmean',
    'agmean',
    'amean',
    'cmean',
    'ghmean',
    'gmean',
    'heronian_mean',
    'hmean',
    'hoelder_mean',
    'imean',
    'lehmer_mean',
    'lmean',
    'median',
    'midrange',
    'mode',
    'qmean',
    'seiffert_mean',
    'std',
    'var',
]


def amean(nums):
    r"""Return arithmetic mean.

    The arithmetic mean is defined as:
    :math:`\frac{\sum{nums}}{|nums|}`

    Cf. https://en.wikipedia.org/wiki/Arithmetic_mean

    :param list nums: A series of numbers
    :returns: The arithmetric mean of nums
    :rtype: float

    >>> amean([1, 2, 3, 4])
    2.5
    >>> amean([1, 2])
    1.5
    >>> amean([0, 5, 1000])
    335.0
    """
    return sum(nums) / len(nums)


def gmean(nums):
    r"""Return geometric mean.

    The geometric mean is defined as:
    :math:`\sqrt[|nums|]{\prod\limits_{i} nums_{i}}`

    Cf. https://en.wikipedia.org/wiki/Geometric_mean

    :param list nums: A series of numbers
    :returns: The geometric mean of nums
    :rtype: float

    >>> gmean([1, 2, 3, 4])
    2.213363839400643
    >>> gmean([1, 2])
    1.4142135623730951
    >>> gmean([0, 5, 1000])
    0.0
    """
    return prod(nums) ** (1 / len(nums))


def hmean(nums):
    r"""Return harmonic mean.

    The harmonic mean is defined as:
    :math:`\frac{|nums|}{\sum\limits_{i}\frac{1}{nums_i}}`

    Following the behavior of Wolfram|Alpha:
    - If one of the values in nums is 0, return 0.
    - If more than one value in nums is 0, return NaN.

    Cf. https://en.wikipedia.org/wiki/Harmonic_mean

    :param list nums: A series of numbers
    :returns: The harmonic mean of nums
    :rtype: float

    >>> hmean([1, 2, 3, 4])
    1.9200000000000004
    >>> hmean([1, 2])
    1.3333333333333333
    >>> hmean([0, 5, 1000])
    0
    """
    if len(nums) < 1:
        raise AttributeError('hmean requires at least one value')
    elif len(nums) == 1:
        return nums[0]
    else:
        for i in range(1, len(nums)):
            if nums[0] != nums[i]:
                break
        else:
            return nums[0]

    if 0 in nums:
        if nums.count(0) > 1:
            return float('nan')
        return 0
    return len(nums) / sum(1 / i for i in nums)


def qmean(nums):
    r"""Return quadratic mean.

    The quadratic mean of precision and recall is defined as:
    :math:`\sqrt{\sum\limits_{i} \frac{num_i^2}{|nums|}}`

    Cf. https://en.wikipedia.org/wiki/Quadratic_mean

    :param list nums: A series of numbers
    :returns: The quadratic mean of nums
    :rtype: float

    >>> qmean([1, 2, 3, 4])
    2.7386127875258306
    >>> qmean([1, 2])
    1.5811388300841898
    >>> qmean([0, 5, 1000])
    577.3574860228857
    """
    return (sum(i ** 2 for i in nums) / len(nums)) ** 0.5


def cmean(nums):
    r"""Return contraharmonic mean.

    The contraharmonic mean is:
    :math:`\frac{\sum\limits_i x_i^2}{\sum\limits_i x_i}`

    Cf. https://en.wikipedia.org/wiki/Contraharmonic_mean

    :param list nums: A series of numbers
    :returns: The contraharmonic mean of nums
    :rtype: float

    >>> cmean([1, 2, 3, 4])
    3.0
    >>> cmean([1, 2])
    1.6666666666666667
    >>> cmean([0, 5, 1000])
    995.0497512437811
    """
    return sum(x ** 2 for x in nums) / sum(nums)


def lmean(nums):
    r"""Return logarithmic mean.

    The logarithmic mean of an arbitrarily long series is defined by
    http://www.survo.fi/papers/logmean.pdf
    as:
    :math:`L(x_1, x_2, ..., x_n) =
    (n-1)! \sum\limits_{i=1}^n \frac{x_i}
    {\prod\limits_{\substack{j = 1\\j \ne i}}^n
    ln \frac{x_i}{x_j}}`

    Cf. https://en.wikipedia.org/wiki/Logarithmic_mean

    :param list nums: A series of numbers
    :returns: The logarithmic mean of nums
    :rtype: float

    >>> lmean([1, 2, 3, 4])
    2.2724242417489258
    >>> lmean([1, 2])
    1.4426950408889634
    """
    if len(nums) != len(set(nums)):
        raise AttributeError('No two values in the nums list may be equal.')
    rolling_sum = 0
    for i in range(len(nums)):
        rolling_prod = 1
        for j in range(len(nums)):
            if i != j:
                rolling_prod *= math.log(nums[i] / nums[j])
        rolling_sum += nums[i] / rolling_prod
    return math.factorial(len(nums) - 1) * rolling_sum


def imean(nums):
    r"""Return identric (exponential) mean.

    The identric mean of two numbers x and y is:
    x if x = y
    otherwise :math:`\frac{1}{e} \sqrt[x-y]{\frac{x^x}{y^y}}`

    Cf. https://en.wikipedia.org/wiki/Identric_mean

    :param list nums: A series of numbers
    :returns: The identric mean of nums
    :rtype: float

    >>> imean([1, 2])
    1.4715177646857693
    >>> imean([1, 0])
    nan
    >>> imean([2, 4])
    2.9430355293715387
    """
    if len(nums) == 1:
        return nums[0]
    if len(nums) > 2:
        raise AttributeError('imean supports no more than two values')
    if nums[0] <= 0 or nums[1] <= 0:
        return float('NaN')
    elif nums[0] == nums[1]:
        return nums[0]
    return (1 / math.e) * (nums[0] ** nums[0] / nums[1] ** nums[1]) ** (
        1 / (nums[0] - nums[1])
    )


def seiffert_mean(nums):
    r"""Return Seiffert's mean.

    Seiffert's mean of two numbers x and y is:
    :math:`\frac{x - y}{4 \cdot arctan \sqrt{\frac{x}{y}} - \pi}`

    Cf. http://www.helsinki.fi/~hasto/pp/miaPreprint.pdf

    :param list nums: A series of numbers
    :returns: Sieffert's mean of nums
    :rtype: float

    >>> seiffert_mean([1, 2])
    1.4712939827611637
    >>> seiffert_mean([1, 0])
    0.3183098861837907
    >>> seiffert_mean([2, 4])
    2.9425879655223275
    >>> seiffert_mean([2, 1000])
    336.84053300118825
    """
    if len(nums) == 1:
        return nums[0]
    if len(nums) > 2:
        raise AttributeError('seiffert_mean supports no more than two values')
    if nums[0] + nums[1] == 0 or nums[0] - nums[1] == 0:
        return float('NaN')
    return (nums[0] - nums[1]) / (
        2 * math.asin((nums[0] - nums[1]) / (nums[0] + nums[1]))
    )


def lehmer_mean(nums, exp=2):
    r"""Return Lehmer mean.

    The Lehmer mean is:
    :math:`\frac{\sum\limits_i{x_i^p}}{\sum\limits_i{x_i^(p-1)}}`

    Cf. https://en.wikipedia.org/wiki/Lehmer_mean

    :param list nums: A series of numbers
    :param numeric exp: The exponent of the Lehmer mean
    :returns: The Lehmer mean of nums for the given exponent
    :rtype: float

    >>> lehmer_mean([1, 2, 3, 4])
    3.0
    >>> lehmer_mean([1, 2])
    1.6666666666666667
    >>> lehmer_mean([0, 5, 1000])
    995.0497512437811
    """
    return sum(x ** exp for x in nums) / sum(x ** (exp - 1) for x in nums)


def heronian_mean(nums):
    r"""Return Heronian mean.

    The Heronian mean is:
    :math:`\frac{\sum\limits_{i, j}\sqrt{{x_i \cdot x_j}}}
    {|nums| \cdot \frac{|nums| + 1}{2}}`
    for :math:`j \ge i`

    Cf. https://en.wikipedia.org/wiki/Heronian_mean

    :param list nums: A series of numbers
    :returns: The Heronian mean of nums
    :rtype: float

    >>> heronian_mean([1, 2, 3, 4])
    2.3888282852609093
    >>> heronian_mean([1, 2])
    1.4714045207910316
    >>> heronian_mean([0, 5, 1000])
    179.28511301977582
    """
    mag = len(nums)
    rolling_sum = 0
    for i in range(mag):
        for j in range(i, mag):
            if nums[i] == nums[j]:
                rolling_sum += nums[i]
            else:
                rolling_sum += (nums[i] * nums[j]) ** 0.5
    return rolling_sum * 2 / (mag * (mag + 1))


def hoelder_mean(nums, exp=2):
    r"""Return Hölder (power/generalized) mean.

    The Hölder mean is defined as:
    :math:`\sqrt[p]{\frac{1}{|nums|} \cdot \sum\limits_i{x_i^p}}`
    for :math:`p \ne 0`, and the geometric mean for :math:`p = 0`

    Cf. https://en.wikipedia.org/wiki/Generalized_mean

    :param list nums: A series of numbers
    :param numeric exp: The exponent of the Hölder mean
    :returns: The Hölder mean of nums for the given exponent
    :rtype: float

    >>> hoelder_mean([1, 2, 3, 4])
    2.7386127875258306
    >>> hoelder_mean([1, 2])
    1.5811388300841898
    >>> hoelder_mean([0, 5, 1000])
    577.3574860228857
    """
    if exp == 0:
        return gmean(nums)
    return ((1 / len(nums)) * sum(i ** exp for i in nums)) ** (1 / exp)


def agmean(nums):
    """Return arithmetic-geometric mean.

    Iterates between arithmetic & geometric means until they converge to
    a single value (rounded to 12 digits).

    Cf. https://en.wikipedia.org/wiki/Arithmetic-geometric_mean

    :param list nums: A series of numbers
    :returns: The arithmetic-geometric mean of nums
    :rtype: float

    >>> agmean([1, 2, 3, 4])
    2.3545004777751077
    >>> agmean([1, 2])
    1.4567910310469068
    >>> agmean([0, 5, 1000])
    2.9753977059954195e-13
    """
    m_a = amean(nums)
    m_g = gmean(nums)
    if math.isnan(m_a) or math.isnan(m_g):
        return float('nan')
    while round(m_a, 12) != round(m_g, 12):
        m_a, m_g = (m_a + m_g) / 2, (m_a * m_g) ** (1 / 2)
    return m_a


def ghmean(nums):
    """Return geometric-harmonic mean.

    Iterates between geometric & harmonic means until they converge to
    a single value (rounded to 12 digits).

    Cf. https://en.wikipedia.org/wiki/Geometric-harmonic_mean

    :param list nums: A series of numbers
    :returns: The geometric-harmonic mean of nums
    :rtype: float

    >>> ghmean([1, 2, 3, 4])
    2.058868154613003
    >>> ghmean([1, 2])
    1.3728805006183502
    >>> ghmean([0, 5, 1000])
    0.0

    >>> ghmean([0, 0])
    0.0
    >>> ghmean([0, 0, 5])
    nan
    """
    m_g = gmean(nums)
    m_h = hmean(nums)
    if math.isnan(m_g) or math.isnan(m_h):
        return float('nan')
    while round(m_h, 12) != round(m_g, 12):
        m_g, m_h = (m_g * m_h) ** (1 / 2), (2 * m_g * m_h) / (m_g + m_h)
    return m_g


def aghmean(nums):
    """Return arithmetic-geometric-harmonic mean.

    Iterates over arithmetic, geometric, & harmonic means until they
    converge to a single value (rounded to 12 digits), following the
    method described by Raïssouli, Leazizi, & Chergui:
    http://www.emis.de/journals/JIPAM/images/014_08_JIPAM/014_08.pdf

    :param list nums: A series of numbers
    :returns: The arithmetic-geometric-harmonic mean of nums
    :rtype: float

    >>> aghmean([1, 2, 3, 4])
    2.198327159900212
    >>> aghmean([1, 2])
    1.4142135623731884
    >>> aghmean([0, 5, 1000])
    335.0
    """
    m_a = amean(nums)
    m_g = gmean(nums)
    m_h = hmean(nums)
    if math.isnan(m_a) or math.isnan(m_g) or math.isnan(m_h):
        return float('nan')
    while round(m_a, 12) != round(m_g, 12) and round(m_g, 12) != round(
        m_h, 12
    ):
        m_a, m_g, m_h = (
            (m_a + m_g + m_h) / 3,
            (m_a * m_g * m_h) ** (1 / 3),
            3 / (1 / m_a + 1 / m_g + 1 / m_h),
        )
    return m_a


def midrange(nums):
    """Return midrange.

    The midrange is the arithmetic mean of the maximum & minimum of a series.

    Cf. https://en.wikipedia.org/wiki/Midrange

    :param list nums: A series of numbers
    :returns: The midrange of nums
    :rtype: float

    >>> midrange([1, 2, 3])
    2.0
    >>> midrange([1, 2, 2, 3])
    2.0
    >>> midrange([1, 2, 1000, 3])
    500.5
    """
    return 0.5 * (max(nums) + min(nums))


def median(nums):
    """Return median.

    With numbers sorted by value, the median is the middle value (if there is
    an odd number of values) or the arithmetic mean of the two middle values
    (if there is an even number of values).

    Cf. https://en.wikipedia.org/wiki/Median

    :param list nums: A series of numbers
    :returns: The median of nums
    :rtype: int or float

    >>> median([1, 2, 3])
    2
    >>> median([1, 2, 3, 4])
    2.5
    >>> median([1, 2, 2, 4])
    2
    """
    nums = sorted(nums)
    mag = len(nums)
    if mag % 2:
        mag = int((mag - 1) / 2)
        return nums[mag]
    mag = int(mag / 2)
    med = (nums[mag - 1] + nums[mag]) / 2
    return med if not med.is_integer() else int(med)


def mode(nums):
    """Return the mode.

    The mode of a series is the most common element of that series

    Cf. https://en.wikipedia.org/wiki/Mode_(statistics)

    :param list nums: A series of numbers
    :returns: The mode of nums
    :rtype: float

    >>> mode([1, 2, 2, 3])
    2
    """
    return Counter(nums).most_common(1)[0][0]


def var(nums, mean_func=amean, ddof=0):
    """Calculate the variance.

    :param list nums: A series of numbers
    :param function mean_func: A mean function (amean by default)
    :param int ddof: The degrees of freedom (0 by default)
    :returns: The variance of the values in the series
    :rtype: float


    >>> var([1, 1, 1, 1])
    0.0
    >>> var([1, 2, 3, 4])
    1.25
    >>> round(var([1, 2, 3, 4], ddof=1), 12)
    1.666666666667
    """
    x_bar = mean_func(nums)
    return sum((x - x_bar) ** 2 for x in nums) / (len(nums) - ddof)


def std(nums, mean_func=amean, ddof=0):
    """Return the standard deviation.

    :param list nums: A series of numbers
    :param function mean_func: A mean function (amean by default)
    :param int ddof: The degrees of freedom (0 by default)
    :returns: The standard deviation of the values in the series
    :rtype: float

    >>> std([1, 1, 1, 1])
    0.0
    >>> round(std([1, 2, 3, 4]), 12)
    1.11803398875
    >>> round(std([1, 2, 3, 4], ddof=1), 12)
    1.290994448736
    """
    return var(nums, mean_func, ddof) ** 0.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
