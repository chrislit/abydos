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

"""abydos.distance.sequence.

The distance.sequence module implements subsequence and substring edit distance
functions, along with Ratcliff-Obershelp similarity & distance.
"""

from __future__ import division, unicode_literals

from numpy import int as np_int
from numpy import zeros as np_zeros

from six.moves import range


__all__ = [
    'dist_lcsseq',
    'dist_lcsstr',
    'dist_ratcliff_obershelp',
    'lcsseq',
    'lcsstr',
    'sim_lcsseq',
    'sim_lcsstr',
    'sim_ratcliff_obershelp',
]


def lcsseq(src, tar):
    """Return the longest common subsequence of two strings.

    Longest common subsequence (LCSseq) is the longest subsequence of
    characters that two strings have in common.

    Based on the dynamic programming algorithm from
    http://rosettacode.org/wiki/Longest_common_subsequence#Dynamic_Programming_6
    :cite:`rosettacode:2018b`. This is licensed GFDL 1.2.

    Modifications include:
        conversion to a numpy array in place of a list of lists

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: the longest common subsequence
    :rtype: str

    >>> lcsseq('cat', 'hat')
    'at'
    >>> lcsseq('Niall', 'Neil')
    'Nil'
    >>> lcsseq('aluminum', 'Catalan')
    'aln'
    >>> lcsseq('ATCG', 'TAGC')
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


def sim_lcsseq(src, tar):
    r"""Return the longest common subsequence similarity of two strings.

    Longest common subsequence similarity (:math:`sim_{LCSseq}`).

    This employs the LCSseq function to derive a similarity metric:
    :math:`sim_{LCSseq}(s,t) = \\frac{|LCSseq(s,t)|}{max(|s|, |t|)}`

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: LCSseq similarity
    :rtype: float

    >>> sim_lcsseq('cat', 'hat')
    0.6666666666666666
    >>> sim_lcsseq('Niall', 'Neil')
    0.6
    >>> sim_lcsseq('aluminum', 'Catalan')
    0.375
    >>> sim_lcsseq('ATCG', 'TAGC')
    0.5
    """
    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0
    return len(lcsseq(src, tar)) / max(len(src), len(tar))


def dist_lcsseq(src, tar):
    """Return the longest common subsequence distance between two strings.

    Longest common subsequence distance (:math:`dist_{LCSseq}`).

    This employs the LCSseq function to derive a similarity metric:
    :math:`dist_{LCSseq}(s,t) = 1 - sim_{LCSseq}(s,t)`

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: LCSseq distance
    :rtype: float

    >>> dist_lcsseq('cat', 'hat')
    0.33333333333333337
    >>> dist_lcsseq('Niall', 'Neil')
    0.4
    >>> dist_lcsseq('aluminum', 'Catalan')
    0.625
    >>> dist_lcsseq('ATCG', 'TAGC')
    0.5
    """
    return 1 - sim_lcsseq(src, tar)


def lcsstr(src, tar):
    """Return the longest common substring of two strings.

    Longest common substring (LCSstr).

    Based on the code from
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python
    :cite:`Wikibooks:2018`.
    This is licensed Creative Commons: Attribution-ShareAlike 3.0.

    Modifications include:

        - conversion to a numpy array in place of a list of lists
        - conversion to Python 2/3-safe range from xrange via six

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: the longest common substring
    :rtype: str

    >>> lcsstr('cat', 'hat')
    'at'
    >>> lcsstr('Niall', 'Neil')
    'N'
    >>> lcsstr('aluminum', 'Catalan')
    'al'
    >>> lcsstr('ATCG', 'TAGC')
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


def sim_lcsstr(src, tar):
    r"""Return the longest common substring similarity of two strings.

    Longest common substring similarity (:math:`sim_{LCSstr}`).

    This employs the LCS function to derive a similarity metric:
    :math:`sim_{LCSstr}(s,t) = \\frac{|LCSstr(s,t)|}{max(|s|, |t|)}`

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: LCSstr similarity
    :rtype: float

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
    return len(lcsstr(src, tar)) / max(len(src), len(tar))


def dist_lcsstr(src, tar):
    """Return the longest common substring distance between two strings.

    Longest common substring distance (:math:`dist_{LCSstr}`).

    This employs the LCS function to derive a similarity metric:
    :math:`dist_{LCSstr}(s,t) = 1 - sim_{LCSstr}(s,t)`

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: LCSstr distance
    :rtype: float

    >>> dist_lcsstr('cat', 'hat')
    0.33333333333333337
    >>> dist_lcsstr('Niall', 'Neil')
    0.8
    >>> dist_lcsstr('aluminum', 'Catalan')
    0.75
    >>> dist_lcsstr('ATCG', 'TAGC')
    0.75
    """
    return 1 - sim_lcsstr(src, tar)


def sim_ratcliff_obershelp(src, tar):
    """Return the Ratcliff-Obershelp similarity of two strings.

    This follows the Ratcliff-Obershelp algorithm :cite:`Ratcliff:1988` to
    derive a similarity measure:

        1. Find the length of the longest common substring in src & tar.
        2. Recurse on the strings to the left & right of each this substring
           in src & tar. The base case is a 0 length common substring, in which
           case, return 0. Otherwise, return the sum of the current longest
           common substring and the left & right recursed sums.
        3. Multiply this length by 2 and divide by the sum of the lengths of
           src & tar.

    Cf.
    http://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: Ratcliff-Obershelp similarity
    :rtype: float

    >>> round(sim_ratcliff_obershelp('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_ratcliff_obershelp('Niall', 'Neil'), 12)
    0.666666666667
    >>> round(sim_ratcliff_obershelp('aluminum', 'Catalan'), 12)
    0.4
    >>> sim_ratcliff_obershelp('ATCG', 'TAGC')
    0.5
    """

    def _lcsstr_stl(src, tar):
        """Return start positions & length for Ratcliff-Obershelp.

        Return the start position in the source string, start position in
        the target string, and length of the longest common substring of
        strings src and tar.
        """
        lengths = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
        longest, src_longest, tar_longest = 0, 0, 0
        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                if src[i - 1] == tar[j - 1]:
                    lengths[i, j] = lengths[i - 1, j - 1] + 1
                    if lengths[i, j] > longest:
                        longest = lengths[i, j]
                        src_longest = i
                        tar_longest = j
                else:
                    lengths[i, j] = 0
        return src_longest - longest, tar_longest - longest, longest

    def _sstr_matches(src, tar):
        """Return the sum of substring match lengths.

        This follows the Ratcliff-Obershelp algorithm :cite:`Ratcliff:1988`:
             1. Find the length of the longest common substring in src & tar.
             2. Recurse on the strings to the left & right of each this
                 substring in src & tar.
             3. Base case is a 0 length common substring, in which case,
                 return 0.
             4. Return the sum.
        """
        src_start, tar_start, length = _lcsstr_stl(src, tar)
        if length == 0:
            return 0
        return (
            _sstr_matches(src[:src_start], tar[:tar_start])
            + length
            + _sstr_matches(
                src[src_start + length :], tar[tar_start + length :]
            )
        )

    if src == tar:
        return 1.0
    elif not src or not tar:
        return 0.0
    return 2 * _sstr_matches(src, tar) / (len(src) + len(tar))


def dist_ratcliff_obershelp(src, tar):
    """Return the Ratcliff-Obershelp distance between two strings.

    Ratcliff-Obsershelp distance the complement of Ratcliff-Obershelp
    similarity:
    :math:`dist_{Ratcliff-Obershelp} = 1 - sim_{Ratcliff-Obershelp}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: Ratcliff-Obershelp distance
    :rtype: float

    >>> round(dist_ratcliff_obershelp('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_ratcliff_obershelp('Niall', 'Neil'), 12)
    0.333333333333
    >>> round(dist_ratcliff_obershelp('aluminum', 'Catalan'), 12)
    0.6
    >>> dist_ratcliff_obershelp('ATCG', 'TAGC')
    0.5
    """
    return 1 - sim_ratcliff_obershelp(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
