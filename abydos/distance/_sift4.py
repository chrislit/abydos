# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.distance.sift4.

The distance.sift4 module implements Sift4 approximate string distance
functions.
"""

from __future__ import division, unicode_literals

from six.moves import range


__all__ = ['dist_sift4', 'sift4_common', 'sift4_simplest', 'sim_sift4']


def sift4_simplest(src, tar, max_offset=5):
    """Return the "simplest" Sift4 distance between two terms.

    This is an approximation of edit distance, described in
    :cite:`Zackwehdex:2014`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param max_offset: the number of characters to search for matching letters
    :returns: the Sift4 distance according to the simplest formula
    :rtype: int

    >>> sift4_simplest('cat', 'hat')
    1
    >>> sift4_simplest('Niall', 'Neil')
    2
    >>> sift4_simplest('Colin', 'Cuilen')
    3
    >>> sift4_simplest('ATCG', 'TAGC')
    2
    """
    if not src:
        return len(tar)

    if not tar:
        return len(src)

    src_len = len(src)
    tar_len = len(tar)

    src_cur = 0
    tar_cur = 0
    lcss = 0
    local_cs = 0

    while (src_cur < src_len) and (tar_cur < tar_len):
        if src[src_cur] == tar[tar_cur]:
            local_cs += 1
        else:
            lcss += local_cs
            local_cs = 0
            if src_cur != tar_cur:
                src_cur = tar_cur = max(src_cur, tar_cur)
            for i in range(max_offset):
                if not ((src_cur + i < src_len) or (tar_cur + i < tar_len)):
                    break
                if (src_cur + i < src_len) and (
                    src[src_cur + i] == tar[tar_cur]
                ):
                    src_cur += i
                    local_cs += 1
                    break
                if (tar_cur + i < tar_len) and (
                    src[src_cur] == tar[tar_cur + i]
                ):
                    tar_cur += i
                    local_cs += 1
                    break

        src_cur += 1
        tar_cur += 1

    lcss += local_cs
    return round(max(src_len, tar_len) - lcss)


def sift4_common(src, tar, max_offset=5, max_distance=0):
    """Return the "common" Sift4 distance between two terms.

    This is an approximation of edit distance, described in
    :cite:`Zackwehdex:2014`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :returns: the Sift4 distance according to the common formula
    :rtype: int

    >>> sift4_common('cat', 'hat')
    1
    >>> sift4_common('Niall', 'Neil')
    2
    >>> sift4_common('Colin', 'Cuilen')
    3
    >>> sift4_common('ATCG', 'TAGC')
    2
    """
    if not src:
        return len(tar)

    if not tar:
        return len(src)

    src_len = len(src)
    tar_len = len(tar)

    src_cur = 0
    tar_cur = 0
    lcss = 0
    local_cs = 0
    trans = 0
    offset_arr = []

    while (src_cur < src_len) and (tar_cur < tar_len):
        if src[src_cur] == tar[tar_cur]:
            local_cs += 1
            is_trans = False
            i = 0
            while i < len(offset_arr):
                ofs = offset_arr[i]
                if src_cur <= ofs['src_cur'] or tar_cur <= ofs['tar_cur']:
                    is_trans = abs(tar_cur - src_cur) >= abs(
                        ofs['tar_cur'] - ofs['src_cur']
                    )
                    if is_trans:
                        trans += 1
                    elif not ofs['trans']:
                        ofs['trans'] = True
                        trans += 1
                    break
                elif src_cur > ofs['tar_cur'] and tar_cur > ofs['src_cur']:
                    del offset_arr[i]
                else:
                    i += 1

            offset_arr.append(
                {'src_cur': src_cur, 'tar_cur': tar_cur, 'trans': is_trans}
            )
        else:
            lcss += local_cs
            local_cs = 0
            if src_cur != tar_cur:
                src_cur = tar_cur = min(src_cur, tar_cur)
            for i in range(max_offset):
                if not ((src_cur + i < src_len) or (tar_cur + i < tar_len)):
                    break
                if (src_cur + i < src_len) and (
                    src[src_cur + i] == tar[tar_cur]
                ):
                    src_cur += i - 1
                    tar_cur -= 1
                    break
                if (tar_cur + i < tar_len) and (
                    src[src_cur] == tar[tar_cur + i]
                ):
                    src_cur -= 1
                    tar_cur += i - 1
                    break

        src_cur += 1
        tar_cur += 1

        if max_distance:
            temporary_distance = max(src_cur, tar_cur) - lcss + trans
            if temporary_distance >= max_distance:
                return round(temporary_distance)

        if (src_cur >= src_len) or (tar_cur >= tar_len):
            lcss += local_cs
            local_cs = 0
            src_cur = tar_cur = min(src_cur, tar_cur)

    lcss += local_cs
    return round(max(src_len, tar_len) - lcss + trans)


def dist_sift4(src, tar, max_offset=5, max_distance=0):
    """Return the normalized "common" Sift4 distance between two terms.

    This is Sift4 distance, normalized to [0, 1].

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :returns: the normalized Sift4 distance
    :rtype: float

    >>> round(dist_sift4('cat', 'hat'), 12)
    0.333333333333
    >>> dist_sift4('Niall', 'Neil')
    0.4
    >>> dist_sift4('Colin', 'Cuilen')
    0.5
    >>> dist_sift4('ATCG', 'TAGC')
    0.5
    """
    return sift4_common(src, tar, max_offset, max_distance) / (
        max(len(src), len(tar), 1)
    )


def sim_sift4(src, tar, max_offset=5, max_distance=0):
    """Return the normalized "common" Sift4 similarity of two terms.

    Normalized Sift4 similarity is the complement of normalized Sift4 distance:
    :math:`sim_{Sift4} = 1 - dist_{Sift4}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param max_offset: the number of characters to search for matching letters
    :param max_distance: the distance at which to stop and exit
    :returns: the normalized Sift4 similarity
    :rtype: float

    >>> round(sim_sift4('cat', 'hat'), 12)
    0.666666666667
    >>> sim_sift4('Niall', 'Neil')
    0.6
    >>> sim_sift4('Colin', 'Cuilen')
    0.5
    >>> sim_sift4('ATCG', 'TAGC')
    0.5
    """
    return 1 - dist_sift4(src, tar, max_offset, max_distance)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
