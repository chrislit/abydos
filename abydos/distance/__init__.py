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

from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
)

from ._Ident import Ident, dist_ident, sim_ident
from ._Length import Length, dist_length, sim_length
from ._Prefix import Prefix, dist_prefix, sim_prefix
from ._Suffix import Suffix, dist_suffix, sim_suffix
from ._Baystat import Baystat, dist_baystat, sim_baystat
from ._NCDarith import NCDarith, dist_ncd_arith, sim_ncd_arith
from ._NCDbwtrle import NCDbwtrle, dist_ncd_bwtrle, sim_ncd_bwtrle
from ._NCDbz2 import NCDbz2, dist_ncd_bz2, sim_ncd_bz2
from ._NCDlzma import NCDlzma, dist_ncd_lzma, sim_ncd_lzma
from ._NCDrle import NCDrle, dist_ncd_rle, sim_ncd_rle
from ._NCDzlib import NCDzlib, dist_ncd_zlib, sim_ncd_zlib
from ._editex import Editex, dist_editex, editex, sim_editex
from ._eudex import Eudex, dist_eudex, eudex_hamming, sim_eudex
from ._Hamming import Hamming, dist_hamming, hamming, sim_hamming
from ._MLIPNS import MLIPNS, dist_mlipns, sim_mlipns
from ._jaro import (
    JaroWinkler,
    Strcmp95,
    dist_jaro_winkler,
    dist_strcmp95,
    sim_jaro_winkler,
    sim_strcmp95,
)
from ._levenshtein import (
    DamerauLevenshtein,
    Indel,
    Levenshtein,
    damerau_levenshtein,
    dist_damerau,
    dist_indel,
    dist_levenshtein,
    levenshtein,
    sim_damerau,
    sim_indel,
    sim_levenshtein,
)
from ._minkowski import (
    Chebyshev,
    Euclidean,
    Manhattan,
    Minkowski,
    chebyshev,
    dist_euclidean,
    dist_manhattan,
    dist_minkowski,
    euclidean,
    manhattan,
    minkowski,
    sim_euclidean,
    sim_manhattan,
    sim_minkowski,
)
from ._mra import MRA, dist_mra, mra_compare, sim_mra
from ._seqalign import (
    Gotoh,
    NeedlemanWunsch,
    SmithWaterman,
    gotoh,
    needleman_wunsch,
    smith_waterman,
)
from ._sequence import (
    LCSseq,
    LCSstr,
    RatcliffObershelp,
    dist_lcsseq,
    dist_lcsstr,
    dist_ratcliff_obershelp,
    lcsseq,
    lcsstr,
    sim_lcsseq,
    sim_lcsstr,
    sim_ratcliff_obershelp,
)
from ._sift4 import (
    Sift4,
    Sift4Simplest,
    dist_sift4,
    sift4_common,
    sift4_simplest,
    sim_sift4,
)
from ._synoname import Synoname, synoname
from ._token import (
    Bag,
    Cosine,
    Dice,
    Jaccard,
    MongeElkan,
    Overlap,
    Tversky,
    bag,
    dist_bag,
    dist_cosine,
    dist_dice,
    dist_jaccard,
    dist_monge_elkan,
    dist_overlap,
    dist_tversky,
    sim_bag,
    sim_cosine,
    sim_dice,
    sim_jaccard,
    sim_monge_elkan,
    sim_overlap,
    sim_tversky,
    tanimoto,
)
from ._typo import Typo, dist_typo, sim_typo, typo

__all__ = [
    'sim',
    'dist',
    'Levenshtein',
    'levenshtein',
    'dist_levenshtein',
    'sim_levenshtein',
    'DamerauLevenshtein',
    'damerau_levenshtein',
    'dist_damerau',
    'sim_damerau',
    'Indel',
    'dist_indel',
    'sim_indel',
    'Hamming',
    'hamming',
    'dist_hamming',
    'sim_hamming',
    'JaroWinkler',
    'dist_jaro_winkler',
    'sim_jaro_winkler',
    'Strcmp95',
    'dist_strcmp95',
    'sim_strcmp95',
    'Minkowski',
    'minkowski',
    'dist_minkowski',
    'sim_minkowski',
    'Manhattan',
    'manhattan',
    'dist_manhattan',
    'sim_manhattan',
    'Euclidean',
    'euclidean',
    'dist_euclidean',
    'sim_euclidean',
    'Chebyshev',
    'chebyshev',
    'Tversky',
    'dist_tversky',
    'sim_tversky',
    'Dice',
    'dist_dice',
    'sim_dice',
    'Jaccard',
    'dist_jaccard',
    'sim_jaccard',
    'tanimoto',
    'Overlap',
    'dist_overlap',
    'sim_overlap',
    'Cosine',
    'dist_cosine',
    'sim_cosine',
    'Bag',
    'bag',
    'dist_bag',
    'sim_bag',
    'MongeElkan',
    'dist_monge_elkan',
    'sim_monge_elkan',
    'NeedlemanWunsch',
    'needleman_wunsch',
    'SmithWaterman',
    'smith_waterman',
    'Gotoh',
    'gotoh',
    'LCSseq',
    'lcsseq',
    'dist_lcsseq',
    'sim_lcsseq',
    'LCSstr',
    'lcsstr',
    'dist_lcsstr',
    'sim_lcsstr',
    'RatcliffObershelp',
    'dist_ratcliff_obershelp',
    'sim_ratcliff_obershelp',
    'Ident',
    'dist_ident',
    'sim_ident',
    'Length',
    'dist_length',
    'sim_length',
    'Prefix',
    'dist_prefix',
    'sim_prefix',
    'Suffix',
    'dist_suffix',
    'sim_suffix',
    'NCDzlib',
    'dist_ncd_zlib',
    'sim_ncd_zlib',
    'NCDbz2',
    'dist_ncd_bz2',
    'sim_ncd_bz2',
    'NCDlzma',
    'dist_ncd_lzma',
    'sim_ncd_lzma',
    'NCDbwtrle',
    'dist_ncd_bwtrle',
    'sim_ncd_bwtrle',
    'NCDrle',
    'dist_ncd_rle',
    'sim_ncd_rle',
    'NCDarith',
    'dist_ncd_arith',
    'sim_ncd_arith',
    'MRA',
    'mra_compare',
    'dist_mra',
    'sim_mra',
    'Editex',
    'editex',
    'dist_editex',
    'sim_editex',
    'MLIPNS',
    'dist_mlipns',
    'sim_mlipns',
    'Baystat',
    'dist_baystat',
    'sim_baystat',
    'Eudex',
    'eudex_hamming',
    'dist_eudex',
    'sim_eudex',
    'Sift4',
    'Sift4Simplest',
    'sift4_common',
    'sift4_simplest',
    'dist_sift4',
    'sim_sift4',
    'Typo',
    'typo',
    'dist_typo',
    'sim_typo',
    'Synoname',
    'synoname',
]


def sim(src, tar, method=sim_levenshtein):
    """Return a similarity of two strings.

    This is a generalized function for calling other similarity functions.

    Args:
        src (str): Source string for comparison
        tar (str): Target string for comparison
        method (function): Specifies the similarity metric
            (:py:func:`sim_levenshtein` by default)

    Returns:
        float: Similarity according to the specified function

    Raises:
        AttributeError: Unknown distance function

    Examples:
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

    Args:
        src (str): Source string for comparison
        tar (str): Target string for comparison
        method (function): Specifies the similarity metric
            (:py:func:`sim_levenshtein` by default) -- Note that this takes
            a similarity metric function, not a distance metric function.

    Returns:
        float: distance according to the specified function

    Raises:
        AttributeError: Unknown distance function

    Examples:
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
