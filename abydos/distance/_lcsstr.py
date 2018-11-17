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

"""abydos.distance._lcsstr.

Longest common substring
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from numpy import int as np_int
from numpy import zeros as np_zeros

from six.moves import range

from ._distance import _Distance

__all__ = ['LCSstr', 'dist_lcsstr', 'lcsstr', 'sim_lcsstr']


class LCSstr(_Distance):
    """Longest common substring."""

    def lcsstr(self, src, tar):
        """Return the longest common substring of two strings.

        Longest common substring (LCSstr).

        Based on the code from
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring
        :cite:`Wikibooks:2018`.
        This is licensed Creative Commons: Attribution-ShareAlike 3.0.

        Modifications include:

            - conversion to a numpy array in place of a list of lists
            - conversion to Python 2/3-safe range from xrange via six

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        str
            The longest common substring

        Examples
        --------
        >>> sstr = LCSstr()
        >>> sstr.lcsstr('cat', 'hat')
        'at'
        >>> sstr.lcsstr('Niall', 'Neil')
        'N'
        >>> sstr.lcsstr('aluminum', 'Catalan')
        'al'
        >>> sstr.lcsstr('ATCG', 'TAGC')
        'A'

        """
        lengths = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
        longest, i_longest = 0, 0
        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                if src[i - 1] == tar[j - 1]:
                    lengths[i, j] = lengths[i - 1, j - 1] + 1
                    if lengths[i, j] > longest:
                        longest = lengths[i, j]
                        i_longest = i
                else:
                    lengths[i, j] = 0
        return src[i_longest - longest : i_longest]

    def sim(self, src, tar):
        r"""Return the longest common substring similarity of two strings.

        Longest common substring similarity (:math:`sim_{LCSstr}`).

        This employs the LCS function to derive a similarity metric:
        :math:`sim_{LCSstr}(s,t) = \frac{|LCSstr(s,t)|}{max(|s|, |t|)}`

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            LCSstr similarity

        Examples
        --------
        >>> sim_lcsstr('cat', 'hat')
        0.6666666666666666
        >>> sim_lcsstr('Niall', 'Neil')
        0.2
        >>> sim_lcsstr('aluminum', 'Catalan')
        0.25
        >>> sim_lcsstr('ATCG', 'TAGC')
        0.25

        """
        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0
        return len(self.lcsstr(src, tar)) / max(len(src), len(tar))


def lcsstr(src, tar):
    """Return the longest common substring of two strings.

    This is a wrapper for :py:meth:`LCSstr.lcsstr`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    str
        The longest common substring

    Examples
    --------
    >>> lcsstr('cat', 'hat')
    'at'
    >>> lcsstr('Niall', 'Neil')
    'N'
    >>> lcsstr('aluminum', 'Catalan')
    'al'
    >>> lcsstr('ATCG', 'TAGC')
    'A'

    """
    return LCSstr().lcsstr(src, tar)


def sim_lcsstr(src, tar):
    """Return the longest common substring similarity of two strings.

    This is a wrapper for :py:meth:`LCSstr.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        LCSstr similarity

    Examples
    --------
    >>> sim_lcsstr('cat', 'hat')
    0.6666666666666666
    >>> sim_lcsstr('Niall', 'Neil')
    0.2
    >>> sim_lcsstr('aluminum', 'Catalan')
    0.25
    >>> sim_lcsstr('ATCG', 'TAGC')
    0.25

    """
    return LCSstr().sim(src, tar)


def dist_lcsstr(src, tar):
    """Return the longest common substring distance between two strings.

    This is a wrapper for :py:meth:`LCSstr.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        LCSstr distance

    Examples
    --------
    >>> dist_lcsstr('cat', 'hat')
    0.33333333333333337
    >>> dist_lcsstr('Niall', 'Neil')
    0.8
    >>> dist_lcsstr('aluminum', 'Catalan')
    0.75
    >>> dist_lcsstr('ATCG', 'TAGC')
    0.75

    """
    return LCSstr().dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
