# -*- coding: utf-8 -*-
"""abydos.util

The util module defines various utility functions for other modules within
Abydos, including:


Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import division
import sys
if sys.version_info[0] == 3:
    # pylint: disable=redefined-builtin
    from functools import reduce    # pragma: no cover
    # pylint: enable=redefined-builtin
from numpy.random import uniform
from math import floor, log10
from ._compat import _range, numeric_type


def prod(nums):
    """Return the product of a series of numbers

    Arguments:
    nums -- a tuple, list, or set of numbers

    The product is Π(nums).

    Cf. https://en.wikipedia.org/wiki/Product_(mathematics)
    """
    return reduce(lambda x, y: x*y, nums, 1)


def jitter(nums, factor=1, amount=None, min_val=None, max_val=None):
    """Return list of numbers with random noise added, according to the R
    jitter function, q.v.:

    Arguments:
    x --  numeric collection to which jitter should be added
    factor --  numeric
    amount --  numeric; if positive, used as amount (see below), otherwise,
        if = 0 the default is factor * z/50.
        Default (NULL): factor * d/5 where d is about the smallest difference
        between x values.
    min_val -- the minimum permitted value in the returned list
    max_val -- the maximum permitted value in the returned list

    Description:
    (adapted from R documentation as this is ported directly from the R code)
    The result, say r, is r = x + numpy.random.uniform(-a, a) where n = len(x)
    and a is the amount argument (if specified).

    Let z = max(x) - min(x) (assuming the usual case). The amount a to be added
    is either provided as positive argument amount or otherwise computed from z,
    as follows:

    If amount == 0, we set a = factor * z/50 (same as S).

    If amount is None (default), we set a = factor * d/5 where d is the
    smallest difference between adjacent unique x values.

    Source:
    http://svn.r-project.org/R/trunk/src/library/base/R/jitter.R
    """
    if isinstance(nums, numeric_type):
        return jitter([nums])[0]
    if len(nums) == 0:
        return []
    if (sum([isinstance(i, numeric_type) for i in nums]) !=
        len(nums)):
        raise AttributeError('All members of nums must be numeric.')

    rng = (min(nums), max(nums))
    diff = rng[1]-rng[0]
    if diff == 0:
        diff = abs(rng[0])
    if diff == 0:
        diff = 1

    if min_val == None:
        min_val = rng[0]-diff
    elif rng[0] < min_val:
        raise AttributeError('Minimum of nums is less than min_val.')

    if max_val == None:
        max_val = rng[1]+diff
    elif rng[1] > max_val:
        raise AttributeError('Maximum of nums is greater than max_val.')

    if amount == None:
        ndigits = int(3 - floor(log10(diff)))
        snums = sorted(set([round(i, ndigits) for i in nums]))
        if len(snums) == 1:
            if snums[0] != 0:
                scaler = snums[0]/10
            else:
                scaler = diff/10
        else:
            scaler = min([j - snums[i - 1] for i, j in enumerate(snums)
                          if i > 0])
        amount = factor/5 * abs(scaler)
    elif amount == 0:
        amount = factor * (diff/50)

    amount = abs(amount)

    newnums = [i + uniform(-amount, amount) for i in nums]

    # Check that we haven't introduced values that exceed specified bounds
    # and aren't too far outside of normal
    # (This is an addition to the standard R algorithm)
    for i in _range(len(newnums)):
        while newnums[i] < min_val or newnums[i] > max_val:
            newnums[i] = (newnums[i] +
                          uniform(-amount, amount)) # pragma: no cover

    # In the unlikely event that two equal values are in the list, try again
    if len(newnums) != len(set(newnums)):
        newnums = jitter(nums, factor, amount,
                         min_val, max_val) # pragma: no cover

    return newnums
