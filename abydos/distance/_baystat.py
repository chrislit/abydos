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

"""abydos.distance._baystat.

Baystat similarity.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance

__all__ = ['Baystat', 'dist_baystat', 'sim_baystat']


class Baystat(_Distance):
    """Baystat similarity and distance.

    Good results for shorter words are reported when setting min_ss_len to 1
    and either left_ext OR right_ext to 1.

    The Baystat similarity is defined in :cite:`Furnohr:2002`.

    This is ostensibly a port of the R module PPRL's implementation:
    https://github.com/cran/PPRL/blob/master/src/MTB_Baystat.cpp
    :cite:`Rukasz:2018`. As such, this could be made more pythonic.
    """

    def sim(self, src, tar, min_ss_len=None, left_ext=None, right_ext=None):
        """Return the Baystat similarity.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        min_ss_len : int
            Minimum substring length to be considered
        left_ext :int
            Left-side extension length
        right_ext :int
            Right-side extension length

        Returns
        -------
        float
            The Baystat similarity

        Examples
        --------
        >>> cmp = Baystat()
        >>> round(cmp.sim('cat', 'hat'), 12)
        0.666666666667
        >>> cmp.sim('Niall', 'Neil')
        0.4
        >>> round(cmp.sim('Colin', 'Cuilen'), 12)
        0.166666666667
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        max_len = max(len(src), len(tar))

        if not (min_ss_len and left_ext and right_ext):
            # These can be set via arguments to the function. Otherwise they
            # are set automatically based on values from the article.
            if max_len >= 7:
                min_ss_len = 2
                left_ext = 2
                right_ext = 2
            else:
                # The paper suggests that for short names, (exclusively) one or
                # the other of left_ext and right_ext can be 1, with good
                # results. I use 0 & 0 as the default in this case.
                min_ss_len = 1
                left_ext = 0
                right_ext = 0

        pos = 0
        match_len = 0

        while True:
            if pos + min_ss_len > len(src):
                return match_len / max_len

            hit_len = 0
            ix = 1

            substring = src[pos : pos + min_ss_len]
            search_begin = pos - left_ext

            if search_begin < 0:
                search_begin = 0
                left_ext_len = pos
            else:
                left_ext_len = left_ext

            if pos + min_ss_len + right_ext >= len(tar):
                right_ext_len = len(tar) - pos - min_ss_len
            else:
                right_ext_len = right_ext

            if (
                search_begin + left_ext_len + min_ss_len + right_ext_len
                > search_begin
            ):
                search_val = tar[
                    search_begin : (
                        search_begin
                        + left_ext_len
                        + min_ss_len
                        + right_ext_len
                    )
                ]
            else:
                search_val = ''

            flagged_tar = ''
            while substring in search_val and pos + ix <= len(src):
                hit_len = len(substring)
                flagged_tar = tar.replace(substring, '#' * hit_len)

                if pos + min_ss_len + ix <= len(src):
                    substring = src[pos : pos + min_ss_len + ix]

                if pos + min_ss_len + right_ext_len + 1 <= len(tar):
                    right_ext_len += 1

                # The following is unnecessary, I think
                # if (search_begin + left_ext_len + min_ss_len + right_ext_len
                #     <= len(tar)):
                search_val = tar[
                    search_begin : (
                        search_begin
                        + left_ext_len
                        + min_ss_len
                        + right_ext_len
                    )
                ]

                ix += 1

            if hit_len > 0:
                tar = flagged_tar

            match_len += hit_len
            pos += ix


def sim_baystat(src, tar, min_ss_len=None, left_ext=None, right_ext=None):
    """Return the Baystat similarity.

    This is a wrapper for :py:meth:`Baystat.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    min_ss_len : int
        Minimum substring length to be considered
    left_ext :int
        Left-side extension length
    right_ext :int
        Right-side extension length

    Returns
    -------
    float
        The Baystat similarity

    Examples
    --------
    >>> round(sim_baystat('cat', 'hat'), 12)
    0.666666666667
    >>> sim_baystat('Niall', 'Neil')
    0.4
    >>> round(sim_baystat('Colin', 'Cuilen'), 12)
    0.166666666667
    >>> sim_baystat('ATCG', 'TAGC')
    0.0

    """
    return Baystat().sim(src, tar, min_ss_len, left_ext, right_ext)


def dist_baystat(src, tar, min_ss_len=None, left_ext=None, right_ext=None):
    """Return the Baystat distance.

    This is a wrapper for :py:meth:`Baystat.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    min_ss_len : int
        Minimum substring length to be considered
    left_ext : int
        Left-side extension length
    right_ext : int
        Right-side extension length

    Returns
    -------
    float
        The Baystat distance

    Examples
    --------
    >>> round(dist_baystat('cat', 'hat'), 12)
    0.333333333333
    >>> dist_baystat('Niall', 'Neil')
    0.6
    >>> round(dist_baystat('Colin', 'Cuilen'), 12)
    0.833333333333
    >>> dist_baystat('ATCG', 'TAGC')
    1.0

    """
    return Baystat().dist(src, tar, min_ss_len, left_ext, right_ext)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
