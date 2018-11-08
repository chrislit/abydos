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

"""abydos.distance.hamming.

The distance.hamming module implements Hamming and related distance functions.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._Hamming import Hamming

__all__ = ['MLIPNS', 'dist_mlipns', 'sim_mlipns']


class MLIPNS(Hamming):
    """MLIPNS similarity.

    Modified Language-Independent Product Name Search (MLIPNS) is described in
    :cite:`Shannaq:2010`. This function returns only 1.0 (similar) or 0.0
    (not similar). LIPNS similarity is identical to normalized Hamming
    similarity.
    """

    # TODO: should Hamming.dist be available? Hamming.dist_abs?
    # TODO: should we just incorporate a Hamming object?

    def sim(self, src, tar, threshold=0.25, max_mismatches=2):
        """Return the MLIPNS similarity of two strings.

        Args:
            src (str): Source string for comparison
            tar (str): Target string for comparison
            threshold (float): A number [0, 1] indicating the maximum
                similarity score, below which the strings are considered
                'similar' (0.25 by default)
            max_mismatches (int): A number indicating the allowable number of
                mismatches to remove before declaring two strings not similar
                (2 by default)

        Returns:
            float: MLIPNS similarity

        Examples:
            >>> sim_mlipns('cat', 'hat')
            1.0
            >>> sim_mlipns('Niall', 'Neil')
            0.0
            >>> sim_mlipns('aluminum', 'Catalan')
            0.0
            >>> sim_mlipns('ATCG', 'TAGC')
            0.0

        """
        if tar == src:
            return 1.0
        if not src or not tar:
            return 0.0

        mismatches = 0
        ham = super(MLIPNS, self).dist_abs(src, tar, diff_lens=True)
        max_length = max(len(src), len(tar))
        while src and tar and mismatches <= max_mismatches:
            if (
                max_length < 1
                or (1 - (max_length - ham) / max_length) <= threshold
            ):
                return 1.0
            else:
                mismatches += 1
                ham -= 1
                max_length -= 1

        if max_length < 1:
            return 1.0
        return 0.0


def sim_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS similarity of two strings.

    Args:
        src (str): Source string for comparison
        tar (str): Target string for comparison
        threshold (float): A number [0, 1] indicating the maximum similarity
            score, below which the strings are considered 'similar' (0.25 by
            default)
        max_mismatches (int): A number indicating the allowable number of
            mismatches to remove before declaring two strings not similar (2 by
            default)

    Returns:
        float: MLIPNS similarity

    Examples:
        >>> sim_mlipns('cat', 'hat')
        1.0
        >>> sim_mlipns('Niall', 'Neil')
        0.0
        >>> sim_mlipns('aluminum', 'Catalan')
        0.0
        >>> sim_mlipns('ATCG', 'TAGC')
        0.0

    """
    return MLIPNS().sim(src, tar, threshold, max_mismatches)


def dist_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS distance between two strings.

    MLIPNS distance is the complement of MLIPNS similarity:
    :math:`dist_{MLIPNS} = 1 - sim_{MLIPNS}`. This function returns only 0.0
    (distant) or 1.0 (not distant).

    Args:
        src (str): Source string for comparison
        tar (str): Target string for comparison
        threshold (float): A number [0, 1] indicating the maximum similarity
            score, below which the strings are considered 'similar' (0.25 by
            default)
        max_mismatches (int): A number indicating the allowable number of
            mismatches to remove before declaring two strings not similar (2 by
            default)

    Returns:
        float: MLIPNS distance

    Examples:
        >>> dist_mlipns('cat', 'hat')
        0.0
        >>> dist_mlipns('Niall', 'Neil')
        1.0
        >>> dist_mlipns('aluminum', 'Catalan')
        1.0
        >>> dist_mlipns('ATCG', 'TAGC')
        1.0

    """
    return MLIPNS().dist(src, tar, threshold, max_mismatches)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
