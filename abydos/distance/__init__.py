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

"""abydos.distance.

The distance module implements string edit distance functions including:

    - Levenshtein distance
    - Optimal String Alignment distance
    - Levenshtein-Damerau distance
    - Hamming distance
    - Tversky index
    - Sørensen–Dice coefficient & distance
    - Jaccard similarity coefficient & distance
    - overlap similarity & distance
    - Tanimoto coefficient & distance
    - Minkowski distance & similarity
    - Manhattan distance & similarity
    - Euclidean distance & similarity
    - Chebyshev distance
    - cosine similarity & distance
    - Jaro distance
    - Jaro-Winkler distance (incl. the strcmp95 algorithm variant)
    - Longest common substring
    - Ratcliff-Obershelp similarity & distance
    - Match Rating Algorithm similarity
    - Normalized Compression Distance (NCD) & similarity
    - Monge-Elkan similarity & distance
    - Matrix similarity
    - Needleman-Wunsch score
    - Smith-Waterman score
    - Gotoh score
    - Length similarity
    - Prefix, Suffix, and Identity similarity & distance
    - Modified Language-Independent Product Name Search (MLIPNS) similarity &
      distance
    - Bag similarity & distance
    - Editex distance
    - Eudex distances
    - Sift4 distance
    - Baystat distance & similarity
    - Typo distance
    - Indel distance
    - Synoname

Functions beginning with the prefixes 'sim' and 'dist' are guaranteed to be
in the range [0, 1], and sim_X = 1 - dist_X since the two are complements.
If a sim_X function is supplied identical src & tar arguments, it is guaranteed
to return 1; the corresponding dist_X function is guaranteed to return 0.
"""

from __future__ import unicode_literals

from ._basic import dist_ident, dist_length, dist_prefix, dist_suffix, sim_ident, sim_length, sim_prefix, sim_suffix
from ._baystat import dist_baystat, sim_baystat
from ._compression import dist_ncd_arith, dist_ncd_bwtrle, dist_ncd_bz2, dist_ncd_lzma, dist_ncd_rle, dist_ncd_zlib, sim_ncd_arith, sim_ncd_bwtrle, sim_ncd_bz2, sim_ncd_lzma, sim_ncd_rle, sim_ncd_zlib
from ._editex import dist_editex, editex, sim_editex
from ._eudex import dist_eudex, eudex_hamming, sim_eudex
from ._hamming import dist_hamming, dist_mlipns, hamming, sim_hamming, sim_mlipns
from ._jaro import dist_jaro_winkler, dist_strcmp95, sim_jaro_winkler, sim_strcmp95
from ._levenshtein import damerau_levenshtein, dist_damerau, dist_indel, dist_levenshtein, levenshtein, sim_damerau, sim_indel, sim_levenshtein
from ._minkowski import chebyshev, dist_euclidean, dist_manhattan, dist_minkowski, euclidean, manhattan, minkowski, sim_euclidean, sim_manhattan, sim_minkowski
from ._mra import dist_mra, mra_compare, sim_mra
from ._seqalign import gotoh, needleman_wunsch, sim_matrix, smith_waterman
from ._sequence import dist_lcsseq, dist_lcsstr, dist_ratcliff_obershelp, lcsseq, lcsstr, sim_lcsseq, sim_lcsstr, sim_ratcliff_obershelp
from ._sift4 import dist_sift4, sift4_common, sift4_simplest, sim_sift4
from ._synoname import synoname
from ._token import bag, dist_bag, dist_cosine, dist_dice, dist_jaccard, dist_monge_elkan, dist_overlap, dist_tversky, sim_bag, sim_cosine, sim_dice, sim_jaccard, sim_monge_elkan, sim_overlap, sim_tanimoto, sim_tversky, tanimoto
from ._typo import dist_typo, sim_typo, typo
from ._util import _get_qgrams

__all__ = ['sim', 'dist',
    'dist_ident',
    'dist_length',
    'dist_prefix',
    'dist_suffix',
    'sim_ident',
    'sim_length',
    'sim_prefix',
    'sim_suffix',
    'dist_baystat',
    'sim_baystat',
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
    'dist_editex',
    'editex',
    'sim_editex',
    'dist_eudex',
    'eudex_hamming',
    'sim_eudex',
    'dist_hamming',
    'dist_mlipns',
    'hamming',
    'sim_hamming',
    'sim_mlipns',
    'dist_jaro_winkler',
    'dist_strcmp95',
    'sim_jaro_winkler',
    'sim_strcmp95',
    'damerau_levenshtein',
    'dist_damerau',
    'dist_indel',
    'dist_levenshtein',
    'levenshtein',
    'sim_damerau',
    'sim_indel',
    'sim_levenshtein',
    'chebyshev',
    'dist_euclidean',
    'dist_manhattan',
    'dist_minkowski',
    'euclidean',
    'manhattan',
    'minkowski',
    'sim_euclidean',
    'sim_manhattan',
    'sim_minkowski',
    'dist_mra',
    'mra_compare',
    'sim_mra',
    'gotoh',
    'needleman_wunsch',
    'sim_matrix',
    'smith_waterman',
    'dist_lcsseq',
    'dist_lcsstr',
    'dist_ratcliff_obershelp',
    'lcsseq',
    'lcsstr',
    'sim_lcsseq',
    'sim_lcsstr',
    'sim_ratcliff_obershelp',
    'dist_sift4',
    'sift4_common',
    'sift4_simplest',
    'sim_sift4',
    'synoname',
    'bag',
    'dist_bag',
    'dist_cosine',
    'dist_dice',
    'dist_jaccard',
    'dist_monge_elkan',
    'dist_overlap',
    'dist_tversky',
    'sim_bag',
    'sim_cosine',
    'sim_dice',
    'sim_jaccard',
    'sim_monge_elkan',
    'sim_overlap',
    'sim_tanimoto',
    'sim_tversky',
    'tanimoto',
    'dist_typo',
    'sim_typo',
    'typo'
]


def sim(src, tar, method=sim_levenshtein):
    """Return a similarity of two strings.

    This is a generalized function for calling other similarity functions.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param function method: specifies the similarity metric (sim_levenshtein by
        default)
    :returns: similarity according to the specified function
    :rtype: float

    >>> round(sim('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim('Niall', 'Neil'), 12)
    0.4
    >>> sim('aluminum', 'Catalan')
    0.125
    >>> sim('ATCG', 'TAGC')
    0.25
    """
    if callable(method):
        return method(src, tar)
    else:
        raise AttributeError('Unknown similarity function: ' + str(method))


def dist(src, tar, method=sim_levenshtein):
    """Return a distance between two strings.

    This is a generalized function for calling other distance functions.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :param function method: specifies the similarity metric (sim_levenshtein by
        default) -- Note that this takes a similarity metric function, not
        a distance metric function.
    :returns: distance according to the specified function
    :rtype: float

    >>> round(dist('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist('Niall', 'Neil'), 12)
    0.6
    >>> dist('aluminum', 'Catalan')
    0.875
    >>> dist('ATCG', 'TAGC')
    0.75
    """
    if callable(method):
        return 1 - method(src, tar)
    else:
        raise AttributeError('Unknown distance function: ' + str(method))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
