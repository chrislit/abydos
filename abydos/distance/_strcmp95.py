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

"""abydos.distance._strcmp95.

The strcmp95 algorithm variant of Jaro-Winkler distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import defaultdict

from six.moves import range

from ._distance import _Distance

__all__ = ['Strcmp95', 'dist_strcmp95', 'sim_strcmp95']


class Strcmp95(_Distance):
    """Strcmp95.

    This is a Python translation of the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    :cite:`Winkler:1994`.
    The above file is a US Government publication and, accordingly,
    in the public domain.

    This is based on the Jaro-Winkler distance, but also attempts to correct
    for some common typos and frequently confused characters. It is also
    limited to uppercase ASCII characters, so it is appropriate to American
    names, but not much else.
    """

    _sp_mx = (
        ('A', 'E'),
        ('A', 'I'),
        ('A', 'O'),
        ('A', 'U'),
        ('B', 'V'),
        ('E', 'I'),
        ('E', 'O'),
        ('E', 'U'),
        ('I', 'O'),
        ('I', 'U'),
        ('O', 'U'),
        ('I', 'Y'),
        ('E', 'Y'),
        ('C', 'G'),
        ('E', 'F'),
        ('W', 'U'),
        ('W', 'V'),
        ('X', 'K'),
        ('S', 'Z'),
        ('X', 'S'),
        ('Q', 'C'),
        ('U', 'V'),
        ('M', 'N'),
        ('L', 'I'),
        ('Q', 'O'),
        ('P', 'R'),
        ('I', 'J'),
        ('2', 'Z'),
        ('5', 'S'),
        ('8', 'B'),
        ('1', 'I'),
        ('1', 'L'),
        ('0', 'O'),
        ('0', 'Q'),
        ('C', 'K'),
        ('G', 'J'),
    )

    def sim(self, src, tar, long_strings=False):
        """Return the strcmp95 similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        long_strings : bool
            Set to True to increase the probability of a match when the number
            of matched characters is large. This option allows for a little
            more tolerance when the strings are large. It is not an appropriate
            test when comparing fixed length fields such as phone and social
            security numbers.

        Returns
        -------
        float
            Strcmp95 similarity

        Examples
        --------
        >>> cmp = Strcmp95()
        >>> cmp.sim('cat', 'hat')
        0.7777777777777777
        >>> cmp.sim('Niall', 'Neil')
        0.8454999999999999
        >>> cmp.sim('aluminum', 'Catalan')
        0.6547619047619048
        >>> cmp.sim('ATCG', 'TAGC')
        0.8333333333333334

        """

        def _in_range(char):
            """Return True if char is in the range (0, 91).

            Parameters
            ----------
            char : str
                The character to check

            Returns
            -------
            bool
                True if char is in the range (0, 91)

            """
            return 91 > ord(char) > 0

        ying = src.strip().upper()
        yang = tar.strip().upper()

        if ying == yang:
            return 1.0
        # If either string is blank - return - added in Version 2
        if not ying or not yang:
            return 0.0

        adjwt = defaultdict(int)

        # Initialize the adjwt array on the first call to the function only.
        # The adjwt array is used to give partial credit for characters that
        # may be errors due to known phonetic or character recognition errors.
        # A typical example is to match the letter "O" with the number "0"
        for i in self._sp_mx:
            adjwt[(i[0], i[1])] = 3
            adjwt[(i[1], i[0])] = 3

        if len(ying) > len(yang):
            search_range = len(ying)
            minv = len(yang)
        else:
            search_range = len(yang)
            minv = len(ying)

        # Blank out the flags
        ying_flag = [0] * search_range
        yang_flag = [0] * search_range
        search_range = max(0, search_range // 2 - 1)

        # Looking only within the search range,
        # count and flag the matched pairs.
        num_com = 0
        yl1 = len(yang) - 1
        for i in range(len(ying)):
            low_lim = (i - search_range) if (i >= search_range) else 0
            hi_lim = (i + search_range) if ((i + search_range) <= yl1) else yl1
            for j in range(low_lim, hi_lim + 1):
                if (yang_flag[j] == 0) and (yang[j] == ying[i]):
                    yang_flag[j] = 1
                    ying_flag[i] = 1
                    num_com += 1
                    break

        # If no characters in common - return
        if num_com == 0:
            return 0.0

        # Count the number of transpositions
        k = n_trans = 0
        for i in range(len(ying)):
            if ying_flag[i] != 0:
                j = 0
                for j in range(k, len(yang)):  # pragma: no branch
                    if yang_flag[j] != 0:
                        k = j + 1
                        break
                if ying[i] != yang[j]:
                    n_trans += 1
        n_trans //= 2

        # Adjust for similarities in unmatched characters
        n_simi = 0
        if minv > num_com:
            for i in range(len(ying)):
                if ying_flag[i] == 0 and _in_range(ying[i]):
                    for j in range(len(yang)):
                        if yang_flag[j] == 0 and _in_range(yang[j]):
                            if (ying[i], yang[j]) in adjwt:
                                n_simi += adjwt[(ying[i], yang[j])]
                                yang_flag[j] = 2
                                break
        num_sim = n_simi / 10.0 + num_com

        # Main weight computation
        weight = (
            num_sim / len(ying)
            + num_sim / len(yang)
            + (num_com - n_trans) / num_com
        )
        weight /= 3.0

        # Continue to boost the weight if the strings are similar
        if weight > 0.7:

            # Adjust for having up to the first 4 characters in common
            j = 4 if (minv >= 4) else minv
            i = 0
            while (i < j) and (ying[i] == yang[i]) and (not ying[i].isdigit()):
                i += 1
            if i:
                weight += i * 0.1 * (1.0 - weight)

            # Optionally adjust for long strings.

            # After agreeing beginning chars, at least two more must agree and
            # the agreeing characters must be > .5 of remaining characters.
            if (
                long_strings
                and (minv > 4)
                and (num_com > i + 1)
                and (2 * num_com >= minv + i)
            ):
                if not ying[0].isdigit():
                    weight += (1.0 - weight) * (
                        (num_com - i - 1) / (len(ying) + len(yang) - i * 2 + 2)
                    )

        return weight


def sim_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 similarity of two strings.

    This is a wrapper for :py:meth:`Strcmp95.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    long_strings : bool
        Set to True to increase the probability of a match when the number of
        matched characters is large. This option allows for a little more
        tolerance when the strings are large. It is not an appropriate test
        when comparing fixed length fields such as phone and social security
        numbers.

    Returns
    -------
    float
        Strcmp95 similarity

    Examples
    --------
    >>> sim_strcmp95('cat', 'hat')
    0.7777777777777777
    >>> sim_strcmp95('Niall', 'Neil')
    0.8454999999999999
    >>> sim_strcmp95('aluminum', 'Catalan')
    0.6547619047619048
    >>> sim_strcmp95('ATCG', 'TAGC')
    0.8333333333333334

    """
    return Strcmp95().sim(src, tar, long_strings)


def dist_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 distance between two strings.

    This is a wrapper for :py:meth:`Strcmp95.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    long_strings : bool
        Set to True to increase the probability of a match when the number of
        matched characters is large. This option allows for a little more
        tolerance when the strings are large. It is not an appropriate test
        when comparing fixed length fields such as phone and social security
        numbers.

    Returns
    -------
    float
        Strcmp95 distance

    Examples
    --------
    >>> round(dist_strcmp95('cat', 'hat'), 12)
    0.222222222222
    >>> round(dist_strcmp95('Niall', 'Neil'), 12)
    0.1545
    >>> round(dist_strcmp95('aluminum', 'Catalan'), 12)
    0.345238095238
    >>> round(dist_strcmp95('ATCG', 'TAGC'), 12)
    0.166666666667

    """
    return Strcmp95().dist(src, tar, long_strings)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
