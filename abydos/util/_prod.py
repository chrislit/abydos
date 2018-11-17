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

"""abydos.util._prod.

The util._prod module defines prod, which computes the product of a collection
of numbers (akin to sum, but for product).
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from operator import mul

from six.moves import reduce

__all__ = []


def _prod(nums):
    r"""Return the product of nums.

    The product is :math:`\prod nums`.

    Cf. https://en.wikipedia.org/wiki/Product_(mathematics)

    Parameters
    ----------
    nums : list
        A collection (list, tuple, set, etc.) of numbers

    Returns
    -------
    numeric
        The product of a nums

    Examples
    --------
    >>> _prod([1,1,1,1])
    1
    >>> _prod((2,4,8))
    64
    >>> _prod({1,2,3,4})
    24
    >>> _prod(2**i for i in range(5))
    1024

    """
    return reduce(mul, nums, 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
