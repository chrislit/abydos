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

"""abydos.distance.compression.

The distance.compression module implements compression distance measures.
"""

from __future__ import division, unicode_literals

from codecs import encode

from ..compression import ac_encode, ac_train, rle_encode

try:
    import lzma
except ImportError:  # pragma: no cover
    # If the system lacks the lzma library, that's fine, but lzma compression
    # similarity won't be supported.
    lzma = None

__all__ = [
    'dist_ncd_arith',
    'dist_ncd_bwtrle',
    'dist_ncd_bz2',
    'dist_ncd_lzma',
    'dist_ncd_rle',
    'dist_ncd_zlib',
    'sim_ncd_arith',
    'sim_ncd_bwtrle',
    'sim_ncd_bz2',
    'sim_ncd_lzma',
    'sim_ncd_rle',
    'sim_ncd_zlib',
]


def dist_ncd_arith(src, tar, probs=None):
    """Return the NCD between two strings using arithmetic coding.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param dict probs: a dictionary trained with arithmetic.train (for the
        arith compressor only)
    :returns: compression distance
    :rtype: float

    >>> dist_ncd_arith('cat', 'hat')
    0.5454545454545454
    >>> dist_ncd_arith('Niall', 'Neil')
    0.6875
    >>> dist_ncd_arith('aluminum', 'Catalan')
    0.8275862068965517
    >>> dist_ncd_arith('ATCG', 'TAGC')
    0.6923076923076923
    """
    if src == tar:
        return 0.0

    if probs is None:
        # lacking a reasonable dictionary, train on the strings themselves
        probs = ac_train(src + tar)
    src_comp = ac_encode(src, probs)[1]
    tar_comp = ac_encode(tar, probs)[1]
    concat_comp = ac_encode(src + tar, probs)[1]
    concat_comp2 = ac_encode(tar + src, probs)[1]

    return (min(concat_comp, concat_comp2) - min(src_comp, tar_comp)) / max(
        src_comp, tar_comp
    )


def sim_ncd_arith(src, tar, probs=None):
    """Return the NCD similarity between two strings using arithmetic coding.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param dict probs: a dictionary trained with ac_train (for the
        arith compressor only)
    :returns: compression similarity
    :rtype: float

    >>> sim_ncd_arith('cat', 'hat')
    0.4545454545454546
    >>> sim_ncd_arith('Niall', 'Neil')
    0.3125
    >>> sim_ncd_arith('aluminum', 'Catalan')
    0.1724137931034483
    >>> sim_ncd_arith('ATCG', 'TAGC')
    0.3076923076923077
    """
    return 1 - dist_ncd_arith(src, tar, probs)


def dist_ncd_rle(src, tar, use_bwt=False):
    """Return the NCD between two strings using RLE.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool use_bwt: boolean indicating whether to perform BWT encoding
        before RLE encoding
    :returns: compression distance
    :rtype: float

    >>> dist_ncd_rle('cat', 'hat')
    1.0
    >>> dist_ncd_rle('Niall', 'Neil')
    1.0
    >>> dist_ncd_rle('aluminum', 'Catalan')
    1.0
    >>> dist_ncd_rle('ATCG', 'TAGC')
    1.0
    """
    if src == tar:
        return 0.0

    src_comp = rle_encode(src, use_bwt)
    tar_comp = rle_encode(tar, use_bwt)
    concat_comp = rle_encode(src + tar, use_bwt)
    concat_comp2 = rle_encode(tar + src, use_bwt)

    return (
        min(len(concat_comp), len(concat_comp2))
        - min(len(src_comp), len(tar_comp))
    ) / max(len(src_comp), len(tar_comp))


def sim_ncd_rle(src, tar, use_bwt=False):
    """Return the NCD similarity between two strings using RLE.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param bool use_bwt: boolean indicating whether to perform BWT encoding
        before RLE encoding
    :returns: compression similarity
    :rtype: float

    >>> sim_ncd_rle('cat', 'hat')
    0.0
    >>> sim_ncd_rle('Niall', 'Neil')
    0.0
    >>> sim_ncd_rle('aluminum', 'Catalan')
    0.0
    >>> sim_ncd_rle('ATCG', 'TAGC')
    0.0
    """
    return 1 - dist_ncd_rle(src, tar, use_bwt)


def dist_ncd_bwtrle(src, tar):
    """Return the NCD between two strings using BWT plus RLE.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: compression distance
    :rtype: float

    >>> dist_ncd_bwtrle('cat', 'hat')
    0.75
    >>> dist_ncd_bwtrle('Niall', 'Neil')
    0.8333333333333334
    >>> dist_ncd_bwtrle('aluminum', 'Catalan')
    1.0
    >>> dist_ncd_bwtrle('ATCG', 'TAGC')
    0.8
    """
    return dist_ncd_rle(src, tar, True)


def sim_ncd_bwtrle(src, tar):
    """Return the NCD similarity between two strings using BWT plus RLE.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: compression similarity
    :rtype: float

    >>> sim_ncd_bwtrle('cat', 'hat')
    0.25
    >>> sim_ncd_bwtrle('Niall', 'Neil')
    0.16666666666666663
    >>> sim_ncd_bwtrle('aluminum', 'Catalan')
    0.0
    >>> sim_ncd_bwtrle('ATCG', 'TAGC')
    0.19999999999999996
    """
    return 1 - dist_ncd_bwtrle(src, tar)


def dist_ncd_zlib(src, tar):
    """Return the NCD between two strings using zlib compression.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: compression distance
    :rtype: float

    >>> dist_ncd_zlib('cat', 'hat')
    0.3333333333333333
    >>> dist_ncd_zlib('Niall', 'Neil')
    0.45454545454545453
    >>> dist_ncd_zlib('aluminum', 'Catalan')
    0.5714285714285714
    >>> dist_ncd_zlib('ATCG', 'TAGC')
    0.4
    """
    if src == tar:
        return 0.0

    src = src.encode('utf-8')
    tar = tar.encode('utf-8')

    src_comp = encode(src, 'zlib_codec')[2:]
    tar_comp = encode(tar, 'zlib_codec')[2:]
    concat_comp = encode(src + tar, 'zlib_codec')[2:]
    concat_comp2 = encode(tar + src, 'zlib_codec')[2:]

    return (
        min(len(concat_comp), len(concat_comp2))
        - min(len(src_comp), len(tar_comp))
    ) / max(len(src_comp), len(tar_comp))


def sim_ncd_zlib(src, tar):
    """Return the NCD similarity between two strings using zlib compression.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: compression similarity
    :rtype: float

    >>> sim_ncd_zlib('cat', 'hat')
    0.6666666666666667
    >>> sim_ncd_zlib('Niall', 'Neil')
    0.5454545454545454
    >>> sim_ncd_zlib('aluminum', 'Catalan')
    0.4285714285714286
    >>> sim_ncd_zlib('ATCG', 'TAGC')
    0.6
    """
    return 1 - dist_ncd_zlib(src, tar)


def dist_ncd_bz2(src, tar):
    """Return the NCD between two strings using bz2 compression.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: compression distance
    :rtype: float

    >>> dist_ncd_bz2('cat', 'hat')
    0.08
    >>> dist_ncd_bz2('Niall', 'Neil')
    0.037037037037037035
    >>> dist_ncd_bz2('aluminum', 'Catalan')
    0.20689655172413793
    >>> dist_ncd_bz2('ATCG', 'TAGC')
    0.037037037037037035
    """
    if src == tar:
        return 0.0

    src = src.encode('utf-8')
    tar = tar.encode('utf-8')

    src_comp = encode(src, 'bz2_codec')[15:]
    tar_comp = encode(tar, 'bz2_codec')[15:]
    concat_comp = encode(src + tar, 'bz2_codec')[15:]
    concat_comp2 = encode(tar + src, 'bz2_codec')[15:]

    return (
        min(len(concat_comp), len(concat_comp2))
        - min(len(src_comp), len(tar_comp))
    ) / max(len(src_comp), len(tar_comp))


def sim_ncd_bz2(src, tar):
    """Return the NCD similarity between two strings using bz2 compression.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: compression similarity
    :rtype: float

    >>> sim_ncd_bz2('cat', 'hat')
    0.92
    >>> sim_ncd_bz2('Niall', 'Neil')
    0.962962962962963
    >>> sim_ncd_bz2('aluminum', 'Catalan')
    0.7931034482758621
    >>> sim_ncd_bz2('ATCG', 'TAGC')
    0.962962962962963
    """
    return 1 - dist_ncd_bz2(src, tar)


def dist_ncd_lzma(src, tar):
    """Return the NCD between two strings using lzma compression.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: compression distance
    :rtype: float

    >>> dist_ncd_lzma('cat', 'hat')
    0.08695652173913043
    >>> dist_ncd_lzma('Niall', 'Neil')
    0.16
    >>> dist_ncd_lzma('aluminum', 'Catalan')
    0.16
    >>> dist_ncd_lzma('ATCG', 'TAGC')
    0.08695652173913043
    """
    if src == tar:
        return 0.0

    src = src.encode('utf-8')
    tar = tar.encode('utf-8')

    if lzma is not None:
        src_comp = lzma.compress(src)[14:]
        tar_comp = lzma.compress(tar)[14:]
        concat_comp = lzma.compress(src + tar)[14:]
        concat_comp2 = lzma.compress(tar + src)[14:]
    else:  # pragma: no cover
        raise ValueError(
            'Install the PylibLZMA module in order to use lzma '
            + 'compression similarity'
        )

    return (
        min(len(concat_comp), len(concat_comp2))
        - min(len(src_comp), len(tar_comp))
    ) / max(len(src_comp), len(tar_comp))


def sim_ncd_lzma(src, tar):
    """Return the NCD similarity between two strings using lzma compression.

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: compression similarity
    :rtype: float

    >>> sim_ncd_lzma('cat', 'hat')
    0.9130434782608696
    >>> sim_ncd_lzma('Niall', 'Neil')
    0.84
    >>> sim_ncd_lzma('aluminum', 'Catalan')
    0.84
    >>> sim_ncd_lzma('ATCG', 'TAGC')
    0.9130434782608696
    """
    return 1 - dist_ncd_lzma(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
