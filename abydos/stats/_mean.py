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

The stats._mean module defines functions for calculating means and other
measures of central tendencies.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import math
from collections import Counter

from six.moves import range

from ..util._prod import _prod

__all__ = [
    'amean',
    'gmean',
    'hmean',
    'agmean',
    'ghmean',
    'aghmean',
    'cmean',
    'imean',
    'lmean',
    'qmean',
    'heronian_mean',
    'hoelder_mean',
    'lehmer_mean',
    'seiffert_mean',
    'median',
    'midrange',
    'mode',
    'std',
    'var',
]


def amean(nums):
    r"""Return arithmetic mean.

    The arithmetic mean is defined as:
    :math:`\frac{\sum{nums}}{|nums|}`

    Cf. https://en.wikipedia.org/wiki/Arithmetic_mean

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The arithmetric mean of nums

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The geometric mean of nums

    Examples
    --------
    >>> gmean([1, 2, 3, 4])
    2.213363839400643
    >>> gmean([1, 2])
    1.4142135623730951
    >>> gmean([0, 5, 1000])
    0.0

    """
    return _prod(nums) ** (1 / len(nums))


def hmean(nums):
    r"""Return harmonic mean.

    The harmonic mean is defined as:
    :math:`\frac{|nums|}{\sum\limits_{i}\frac{1}{nums_i}}`

    Following the behavior of Wolfram|Alpha:
    - If one of the values in nums is 0, return 0.
    - If more than one value in nums is 0, return NaN.

    Cf. https://en.wikipedia.org/wiki/Harmonic_mean

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The harmonic mean of nums

    Raises
    ------
    AttributeError
        hmean requires at least one value

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The quadratic mean of nums

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The contraharmonic mean of nums

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The logarithmic mean of nums

    Raises
    ------
    AttributeError
        No two values in the nums list may be equal

    Examples
    --------
    >>> lmean([1, 2, 3, 4])
    2.2724242417489258
    >>> lmean([1, 2])
    1.4426950408889634

    """
    if len(nums) != len(set(nums)):
        raise AttributeError('No two values in the nums list may be equal')
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The identric mean of nums

    Raises
    ------
    AttributeError
        imean supports no more than two values

    Examples
    --------
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

    It is defined in :cite:`Seiffert:1993`.

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        Sieffert's mean of nums

    Raises
    ------
    AttributeError
        seiffert_mean supports no more than two values

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers
    exp : numeric
        The exponent of the Lehmer mean

    Returns
    -------
    float
        The Lehmer mean of nums for the given exponent

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The Heronian mean of nums

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers
    exp : numeric
        The exponent of the Hölder mean

    Returns
    -------
    float
        The Hölder mean of nums for the given exponent

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The arithmetic-geometric mean of nums

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The geometric-harmonic mean of nums

    Examples
    --------
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
    method described in :cite:`Raissouli:2009`.

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The arithmetic-geometric-harmonic mean of nums

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The midrange of nums

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    int or float
        The median of nums

    Examples
    --------
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

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    int or float
        The mode of nums

    Example
    -------
    >>> mode([1, 2, 2, 3])
    2

    """
    return Counter(nums).most_common(1)[0][0]


def var(nums, mean_func=amean, ddof=0):
    r"""Calculate the variance.

    The variance (:math:`\sigma^2`) of a series of numbers (:math:`x_i`) with
    mean :math:`\mu` and population :math:`N` is:

    :math:`\sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2`.

    Cf. https://en.wikipedia.org/wiki/Variance

    Parameters
    ----------
    nums : list
        A series of numbers
    mean_func : function
        A mean function (amean by default)
    ddof : int
        The degrees of freedom (0 by default)

    Returns
    -------
    float
        The variance of the values in the series

    Examples
    --------
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

    The standard deviation of a series of values is the square root of the
    variance.

    Cf. https://en.wikipedia.org/wiki/Standard_deviation

    Parameters
    ----------
    nums : list
        A series of numbers
    mean_func : function
        A mean function (amean by default)
    ddof : int
        The degrees of freedom (0 by default)

    Returns
    -------
    float
        The standard deviation of the values in the series

    Examples
    --------
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
