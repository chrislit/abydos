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
    from functools import reduce
    # pylint: enable=redefined-builtin


def prod(nums):
    """Return the product of a series of numbers

    Arguments:
    nums -- a tuple, list, or set of numbers

    The product is Π(nums).

    Cf. https://en.wikipedia.org/wiki/Product_(mathematics)
    """
    return reduce(lambda x, y: x*y, nums, 1)
