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

"""abydos.distance._lcsseq.

Longest common subsequence
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from numpy import int as np_int
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['LCSseq', 'dist_lcsseq', 'lcsseq', 'sim_lcsseq']


class LCSseq(_Distance):
    """Longest common subsequence.

    Longest common subsequence (LCSseq) is the longest subsequence of
    characters that two strings have in common.
    """

    def lcsseq(self, src, tar):
        """Return the longest common subsequence of two strings.

        Based on the dynamic programming algorithm from
        http://rosettacode.org/wiki/Longest_common_subsequence
        :cite:`rosettacode:2018b`. This is licensed GFDL 1.2.

        Modifications include:
            conversion to a numpy array in place of a list of lists

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        str
            The longest common subsequence

        Examples
        --------
        >>> sseq = LCSseq()
        >>> sseq.lcsseq('cat', 'hat')
        'at'
        >>> sseq.lcsseq('Niall', 'Neil')
        'Nil'
        >>> sseq.lcsseq('aluminum', 'Catalan')
        'aln'
        >>> sseq.lcsseq('ATCG', 'TAGC')
        'AC'

        """
        lengths = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)

        # row 0 and column 0 are initialized to 0 already
        for i, src_char in enumerate(src):
            for j, tar_char in enumerate(tar):
                if src_char == tar_char:
                    lengths[i + 1, j + 1] = lengths[i, j] + 1
                else:
                    lengths[i + 1, j + 1] = max(
                        lengths[i + 1, j], lengths[i, j + 1]
                    )

        # read the substring out from the matrix
        result = ''
        i, j = len(src), len(tar)
        while i != 0 and j != 0:
            if lengths[i, j] == lengths[i - 1, j]:
                i -= 1
            elif lengths[i, j] == lengths[i, j - 1]:
                j -= 1
            else:
                result = src[i - 1] + result
                i -= 1
                j -= 1
        return result

    def sim(self, src, tar):
        r"""Return the longest common subsequence similarity of two strings.

        Longest common subsequence similarity (:math:`sim_{LCSseq}`).

        This employs the LCSseq function to derive a similarity metric:
        :math:`sim_{LCSseq}(s,t) = \frac{|LCSseq(s,t)|}{max(|s|, |t|)}`

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            LCSseq similarity

        Examples
        --------
        >>> sseq = LCSseq()
        >>> sseq.sim('cat', 'hat')
        0.6666666666666666
        >>> sseq.sim('Niall', 'Neil')
        0.6
        >>> sseq.sim('aluminum', 'Catalan')
        0.375
        >>> sseq.sim('ATCG', 'TAGC')
        0.5

        """
        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0
        return len(self.lcsseq(src, tar)) / max(len(src), len(tar))


def lcsseq(src, tar):
    """Return the longest common subsequence of two strings.

    This is a wrapper for :py:meth:`LCSseq.lcsseq`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    str
        The longest common subsequence

    Examples
    --------
    >>> lcsseq('cat', 'hat')
    'at'
    >>> lcsseq('Niall', 'Neil')
    'Nil'
    >>> lcsseq('aluminum', 'Catalan')
    'aln'
    >>> lcsseq('ATCG', 'TAGC')
    'AC'

    """
    return LCSseq().lcsseq(src, tar)


def sim_lcsseq(src, tar):
    r"""Return the longest common subsequence similarity of two strings.

    This is a wrapper for :py:meth:`LCSseq.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        LCSseq similarity

    Examples
    --------
    >>> sim_lcsseq('cat', 'hat')
    0.6666666666666666
    >>> sim_lcsseq('Niall', 'Neil')
    0.6
    >>> sim_lcsseq('aluminum', 'Catalan')
    0.375
    >>> sim_lcsseq('ATCG', 'TAGC')
    0.5

    """
    return LCSseq().sim(src, tar)


def dist_lcsseq(src, tar):
    """Return the longest common subsequence distance between two strings.

    This is a wrapper for :py:meth:`LCSseq.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        LCSseq distance

    Examples
    --------
    >>> dist_lcsseq('cat', 'hat')
    0.33333333333333337
    >>> dist_lcsseq('Niall', 'Neil')
    0.4
    >>> dist_lcsseq('aluminum', 'Catalan')
    0.625
    >>> dist_lcsseq('ATCG', 'TAGC')
    0.5

    """
    return LCSseq().dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
