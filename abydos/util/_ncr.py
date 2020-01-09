# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.util._ncr.

The util._ncr module defines _ncr, which computes n Choose r.
"""

from math import factorial, gamma

__all__ = []


def _ncr(n, r):
    r"""Return n Choose r.

    Cf. https://en.wikipedia.org/wiki/Combination

    Parameters
    ----------
    n : float
        The number of elements in the set/multiset
    r : float
        The number of elements to choose

    Returns
    -------
    int or float
        n Choose r

    Examples
    --------
    >>> _ncr(4, 2)
    6
    >>> _ncr(10, 3)
    120

    .. versionadded:: 0.4.0

    """
    if isinstance(r, int) and isinstance(n, int):
        if not r:
            return 1
        if r > n:
            return 0
        return int(factorial(n) / (factorial(r) * factorial(n - r)))
    return gamma(n + 1) / (gamma(r + 1) * gamma(n - r + 1))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
