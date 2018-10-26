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

"""abydos.distance.jaro.

The distance.jaro module implements distance metrics based on
:cite:`Jaro:1989` and subsequent works:

    - Jaro distance
    - Jaro-Winkler distance
    - the strcmp95 algorithm variant of Jaro-Winkler distance
"""

from __future__ import division, unicode_literals

from collections import defaultdict

from six.moves import range

from ..tokenizer import QGrams


__all__ = [
    'dist_jaro_winkler',
    'dist_strcmp95',
    'sim_jaro_winkler',
    'sim_strcmp95',
]


def sim_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 similarity of two strings.

    This is a Python translation of the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    :cite:`Winkler:1994`.
    The above file is a US Government publication and, accordingly,
    in the public domain.

    This is based on the Jaro-Winkler distance, but also attempts to correct
    for some common typos and frequently confused characters. It is also
    limited to uppercase ASCII characters, so it is appropriate to American
    names, but not much else.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large. It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :returns: strcmp95 similarity
    :rtype: float

    >>> sim_strcmp95('cat', 'hat')
    0.7777777777777777
    >>> sim_strcmp95('Niall', 'Neil')
    0.8454999999999999
    >>> sim_strcmp95('aluminum', 'Catalan')
    0.6547619047619048
    >>> sim_strcmp95('ATCG', 'TAGC')
    0.8333333333333334
    """

    def _in_range(char):
        """Return True if char is in the range (0, 91)."""
        return 91 > ord(char) > 0

    ying = src.strip().upper()
    yang = tar.strip().upper()

    if ying == yang:
        return 1.0
    # If either string is blank - return - added in Version 2
    if not ying or not yang:
        return 0.0

    adjwt = defaultdict(int)
    sp_mx = (
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

    # Initialize the adjwt array on the first call to the function only.
    # The adjwt array is used to give partial credit for characters that
    # may be errors due to known phonetic or character recognition errors.
    # A typical example is to match the letter "O" with the number "0"
    for i in sp_mx:
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

    # Looking only within the search range, count and flag the matched pairs.
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


def dist_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 distance between two strings.

    strcmp95 distance is the complement of strcmp95 similarity:
    :math:`dist_{strcmp95} = 1 - sim_{strcmp95}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large. It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :returns: strcmp95 distance
    :rtype: float

    >>> round(dist_strcmp95('cat', 'hat'), 12)
    0.222222222222
    >>> round(dist_strcmp95('Niall', 'Neil'), 12)
    0.1545
    >>> round(dist_strcmp95('aluminum', 'Catalan'), 12)
    0.345238095238
    >>> round(dist_strcmp95('ATCG', 'TAGC'), 12)
    0.166666666667
    """
    return 1 - sim_strcmp95(src, tar, long_strings)


def sim_jaro_winkler(
    src,
    tar,
    qval=1,
    mode='winkler',
    long_strings=False,
    boost_threshold=0.7,
    scaling_factor=0.1,
):
    """Return the Jaro or Jaro-Winkler similarity of two strings.

    Jaro(-Winkler) distance is a string edit distance initially proposed by
    Jaro and extended by Winkler :cite:`Jaro:1989,Winkler:1990`.

    This is Python based on the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    :cite:`Winkler:1994`. The above file is a US Government publication and,
    accordingly, in the public domain.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param int qval: the length of each q-gram (defaults to 1: character-wise
        matching)
    :param str mode: indicates which variant of this distance metric to
        compute:

            - 'winkler' -- computes the Jaro-Winkler distance (default) which
              increases the score for matches near the start of the word
            - 'jaro' -- computes the Jaro distance

    The following arguments apply only when mode is 'winkler':

    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large.  It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :param float boost_threshold: a value between 0 and 1, below which the
        Winkler boost is not applied (defaults to 0.7)
    :param float scaling_factor: a value between 0 and 0.25, indicating by how
        much to boost scores for matching prefixes (defaults to 0.1)

    :returns: Jaro or Jaro-Winkler similarity
    :rtype: float

    >>> round(sim_jaro_winkler('cat', 'hat'), 12)
    0.777777777778
    >>> round(sim_jaro_winkler('Niall', 'Neil'), 12)
    0.805
    >>> round(sim_jaro_winkler('aluminum', 'Catalan'), 12)
    0.60119047619
    >>> round(sim_jaro_winkler('ATCG', 'TAGC'), 12)
    0.833333333333

    >>> round(sim_jaro_winkler('cat', 'hat', mode='jaro'), 12)
    0.777777777778
    >>> round(sim_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
    0.783333333333
    >>> round(sim_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
    0.60119047619
    >>> round(sim_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
    0.833333333333
    """
    if mode == 'winkler':
        if boost_threshold > 1 or boost_threshold < 0:
            raise ValueError(
                'Unsupported boost_threshold assignment; '
                + 'boost_threshold must be between 0 and 1.'
            )
        if scaling_factor > 0.25 or scaling_factor < 0:
            raise ValueError(
                'Unsupported scaling_factor assignment; '
                + 'scaling_factor must be between 0 and 0.25.'
            )

    if src == tar:
        return 1.0

    src = QGrams(src.strip(), qval).ordered_list
    tar = QGrams(tar.strip(), qval).ordered_list

    lens = len(src)
    lent = len(tar)

    # If either string is blank - return - added in Version 2
    if lens == 0 or lent == 0:
        return 0.0

    if lens > lent:
        search_range = lens
        minv = lent
    else:
        search_range = lent
        minv = lens

    # Zero out the flags
    src_flag = [0] * search_range
    tar_flag = [0] * search_range
    search_range = max(0, search_range // 2 - 1)

    # Looking only within the search range, count and flag the matched pairs.
    num_com = 0
    yl1 = lent - 1
    for i in range(lens):
        low_lim = (i - search_range) if (i >= search_range) else 0
        hi_lim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in range(low_lim, hi_lim + 1):
            if (tar_flag[j] == 0) and (tar[j] == src[i]):
                tar_flag[j] = 1
                src_flag[i] = 1
                num_com += 1
                break

    # If no characters in common - return
    if num_com == 0:
        return 0.0

    # Count the number of transpositions
    k = n_trans = 0
    for i in range(lens):
        if src_flag[i] != 0:
            j = 0
            for j in range(k, lent):  # pragma: no branch
                if tar_flag[j] != 0:
                    k = j + 1
                    break
            if src[i] != tar[j]:
                n_trans += 1
    n_trans //= 2

    # Main weight computation for Jaro distance
    weight = num_com / lens + num_com / lent + (num_com - n_trans) / num_com
    weight /= 3.0

    # Continue to boost the weight if the strings are similar
    # This is the Winkler portion of Jaro-Winkler distance
    if mode == 'winkler' and weight > boost_threshold:

        # Adjust for having up to the first 4 characters in common
        j = 4 if (minv >= 4) else minv
        i = 0
        while (i < j) and (src[i] == tar[i]):
            i += 1
        weight += i * scaling_factor * (1.0 - weight)

        # Optionally adjust for long strings.

        # After agreeing beginning chars, at least two more must agree and
        # the agreeing characters must be > .5 of remaining characters.
        if (
            long_strings
            and (minv > 4)
            and (num_com > i + 1)
            and (2 * num_com >= minv + i)
        ):
            weight += (1.0 - weight) * (
                (num_com - i - 1) / (lens + lent - i * 2 + 2)
            )

    return weight


def dist_jaro_winkler(
    src,
    tar,
    qval=1,
    mode='winkler',
    long_strings=False,
    boost_threshold=0.7,
    scaling_factor=0.1,
):
    """Return the Jaro or Jaro-Winkler distance between two strings.

    Jaro(-Winkler) similarity is the complement of Jaro(-Winkler) distance:
    :math:`sim_{Jaro(-Winkler)} = 1 - dist_{Jaro(-Winkler)}`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param int qval: the length of each q-gram (defaults to 1: character-wise
        matching)
    :param str mode: indicates which variant of this distance metric to
        compute:

            - 'winkler' -- computes the Jaro-Winkler distance (default) which
              increases the score for matches near the start of the word
            - 'jaro' -- computes the Jaro distance

    The following arguments apply only when mode is 'winkler':

    :param bool long_strings: set to True to "Increase the probability of a
        match when the number of matched characters is large.  This option
        allows for a little more tolerance when the strings are large.  It is
        not an appropriate test when comparing fixed length fields such as
        phone and social security numbers."
    :param float boost_threshold: a value between 0 and 1, below which the
        Winkler boost is not applied (defaults to 0.7)
    :param float scaling_factor: a value between 0 and 0.25, indicating by how
        much to boost scores for matching prefixes (defaults to 0.1)

    :returns: Jaro or Jaro-Winkler distance
    :rtype: float

    >>> round(dist_jaro_winkler('cat', 'hat'), 12)
    0.222222222222
    >>> round(dist_jaro_winkler('Niall', 'Neil'), 12)
    0.195
    >>> round(dist_jaro_winkler('aluminum', 'Catalan'), 12)
    0.39880952381
    >>> round(dist_jaro_winkler('ATCG', 'TAGC'), 12)
    0.166666666667

    >>> round(dist_jaro_winkler('cat', 'hat', mode='jaro'), 12)
    0.222222222222
    >>> round(dist_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
    0.216666666667
    >>> round(dist_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
    0.39880952381
    >>> round(dist_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
    0.166666666667
    """
    return 1 - sim_jaro_winkler(
        src, tar, qval, mode, long_strings, boost_threshold, scaling_factor
    )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
