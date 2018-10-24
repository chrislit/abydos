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

from __future__ import division, unicode_literals

__all__ = [
    'dist_hamming',
    'dist_mlipns',
    'hamming',
    'sim_hamming',
    'sim_mlipns',
]


def hamming(src, tar, diff_lens=True):
    """Return the Hamming distance between two strings.

    Hamming distance :cite:`Hamming:1950` equals the number of character
    positions at which two strings differ. For strings of unequal lengths,
    it is not normally defined. By default, this implementation calculates the
    Hamming distance of the first n characters where n is the lesser of the two
    strings' lengths and adds to this the difference in string lengths.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool diff_lens:
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending
        the shorter string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.
    :returns: the Hamming distance between src & tar
    :rtype: int

    >>> hamming('cat', 'hat')
    1
    >>> hamming('Niall', 'Neil')
    3
    >>> hamming('aluminum', 'Catalan')
    8
    >>> hamming('ATCG', 'TAGC')
    4
    """
    if not diff_lens and len(src) != len(tar):
        raise ValueError(
            'Undefined for sequences of unequal length; set '
            + 'diff_lens to True for Hamming distance between '
            + 'strings of unequal lengths.'
        )

    hdist = 0
    if diff_lens:
        hdist += abs(len(src) - len(tar))
    hdist += sum(c1 != c2 for c1, c2 in zip(src, tar))

    return hdist


def dist_hamming(src, tar, diff_lens=True):
    """Return the normalized Hamming distance between two strings.

    Hamming distance normalized to the interval [0, 1].

    The Hamming distance is normalized by dividing it
    by the greater of the number of characters in src & tar (unless diff_lens
    is set to False, in which case an exception is raised).

    The arguments are identical to those of the hamming() function.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool diff_lens:
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending
        the shorter string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.
    :returns: normalized Hamming distance
    :rtype: float

    >>> round(dist_hamming('cat', 'hat'), 12)
    0.333333333333
    >>> dist_hamming('Niall', 'Neil')
    0.6
    >>> dist_hamming('aluminum', 'Catalan')
    1.0
    >>> dist_hamming('ATCG', 'TAGC')
    1.0
    """
    if src == tar:
        return 0
    return hamming(src, tar, diff_lens) / max(len(src), len(tar))


def sim_hamming(src, tar, diff_lens=True):
    """Return the normalized Hamming similarity of two strings.

    Hamming similarity normalized to the interval [0, 1].

    Hamming similarity is the complement of normalized Hamming distance:
    :math:`sim_{Hamming} = 1 - dist{Hamming}`.

    Provided that diff_lens==True, the Hamming similarity is identical to the
    Language-Independent Product Name Search (LIPNS) similarity score. For
    further information, see the sim_mlipns documentation.

    The arguments are identical to those of the hamming() function.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool diff_lens:
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending
        the shorter string with obligatorily non-matching characters.
        If False, an exception is raised in the case of strings of unequal
        lengths.
    :returns: normalized Hamming similarity
    :rtype: float

    >>> round(sim_hamming('cat', 'hat'), 12)
    0.666666666667
    >>> sim_hamming('Niall', 'Neil')
    0.4
    >>> sim_hamming('aluminum', 'Catalan')
    0.0
    >>> sim_hamming('ATCG', 'TAGC')
    0.0
    """
    return 1 - dist_hamming(src, tar, diff_lens)


def sim_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS similarity of two strings.

    Modified Language-Independent Product Name Search (MLIPNS) is described in
    :cite:`Shannaq:2010`. This function returns only 1.0 (similar) or 0.0
    (not similar). LIPNS similarity is identical to normalized Hamming
    similarity.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param float threshold: a number [0, 1] indicating the maximum similarity
        score, below which the strings are considered 'similar' (0.25 by
        default)
    :param int max_mismatches: a number indicating the allowable number of
        mismatches to remove before declaring two strings not similar (2 by
        default)
    :returns: MLIPNS similarity
    :rtype: float

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
    ham = hamming(src, tar, diff_lens=True)
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


def dist_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS distance between two strings.

    MLIPNS distance is the complement of MLIPNS similarity:
    :math:`dist_{MLIPNS} = 1 - sim_{MLIPNS}`. This function returns only 0.0
    (distant) or 1.0 (not distant).

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param float threshold: a number [0, 1] indicating the maximum similarity
        score, below which the strings are considered 'similar' (0.25 by
        default)
    :param int max_mismatches: a number indicating the allowable number of
        mismatches to remove before declaring two strings not similar (2 by
        default)
    :returns: MLIPNS distance
    :rtype: float

    >>> dist_mlipns('cat', 'hat')
    0.0
    >>> dist_mlipns('Niall', 'Neil')
    1.0
    >>> dist_mlipns('aluminum', 'Catalan')
    1.0
    >>> dist_mlipns('ATCG', 'TAGC')
    1.0
    """
    return 1.0 - sim_mlipns(src, tar, threshold, max_mismatches)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
