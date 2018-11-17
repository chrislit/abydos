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

The distance package implements string distance measure and metric classes:

These include traditional Levenshtein edit distance and related algorithms:

    - Levenshtein distance (:py:class:`.Levenshtein`)
    - Optimal String Alignment distance (:py:class:`.Levenshtein` with
      ``mode='osa'``)
    - Damerau-Levenshtein distance (:py:class:`.DamerauLevenshtein`)
    - Indel distance (:py:class:`.Indel`)

Hamming distance (:py:class:`.Hamming`) and the closely related Modified
Language-Independent Product Name Search distance (:py:class:`.MLIPNS`) are
provided.

Distance metrics developed for the US Census are included:

    - Jaro distance (:py:class:`.JaroWinkler` with ``mode='Jaro'``)
    - Jaro-Winkler distance (:py:class:`.JaroWinkler`)
    - Strcmp95 distance (:py:class:`.Strcmp95`)

A large set of multi-set token-based distance metrics are provided, including:

    - Generalized Minkowski distance (:py:class:`.Minkowski`)
    - Manhattan distance (:py:class:`.Manhattan`)
    - Euclidean distance (:py:class:`.Euclidean`)
    - Chebyshev distance (:py:class:`.Chebyshev`)
    - Generalized Tversky distance (:py:class:`.Tversky`)
    - Sørensen–Dice coefficient (:py:class:`.Dice`)
    - Jaccard similarity (:py:class:`.Jaccard`)
    - Tanimoto coefficient (:py:meth:`.Jaccard.tanimoto_coeff`)
    - Overlap distance (:py:class:`.Overlap`)
    - Cosine similarity (:py:class:`.Cosine`)
    - Bag distance (:py:class:`.Bag`)
    - Monge-Elkan distance (:py:class:`.MongeElkan`)

Three popular sequence alignment algorithms are provided:

    - Needleman-Wunsch score (:py:class:`.NeedlemanWunsch`)
    - Smith-Waterman score (:py:class:`.SmithWaterman`)
    - Gotoh score (:py:class:`.Gotoh`)

Classes relating to substring and subsequence distances include:

    - Longest common subsequence (:py:class:`.LCSseq`)
    - Longest common substring (:py:class:`.LCSstr`)
    - Ratcliff-Obserhelp distance (:py:class:`.RatcliffObershelp`)

A number of simple distance classes provided in the package include:

    - Identity distance (:py:class:`.Ident`)
    - Length distance (:py:class:`.Length`)
    - Prefix distance (:py:class:`.Prefix`)
    - Suffix distance (:py:class:`.Suffix`)

Normalized compression distance classes for a variety of compression algorithms
are provided:

    - zlib (:py:class:`.NCDzlib`)
    - bzip2 (:py:class:`.NCDbz2`)
    - lzma (:py:class:`.NCDlzma`)
    - arithmetic coding (:py:class:`.NCDarith`)
    - BWT plus RLE (:py:class:`.NCDbwtrle`)
    - RLE (:py:class:`.NCDrle`)

The remaining distance measures & metrics include:

    - Western Airlines' Match Rating Algorithm comparison
      (:py:class:`.distance.MRA`)
    - Editex (:py:class:`.Editex`)
    - Bavarian Landesamt für Statistik distance (:py:class:`.Baystat`)
    - Eudex distance (:py:class:`.distance.Eudex`)
    - Sift4 distance (:py:class:`.Sift4` and :py:class:`.Sift4Simplest`)
    - Typo distance (:py:class:`.Typo`)
    - Synoname (:py:class:`.Synoname`)

Most of the distance and similarity measures have ``sim`` and ``dist`` methods,
which return a measure that is normalized to the range :math:`[0, 1]`. The
normalized distance and similarity are always complements, so the normalized
distance will always equal 1 - the similarity for a particular measure supplied
with the same input. Some measures have an absolute distance method
``dist_abs`` that is not limited to any range.

All three methods can be demonstrated using the :py:class:`.DamerauLevenshtein`
class:

>>> dl = DamerauLevenshtein()
>>> dl.dist_abs('orange', 'strange')
2
>>> dl.dist('orange', 'strange')
0.2857142857142857
>>> dl.sim('orange', 'strange')
0.7142857142857143

----

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._bag import Bag, bag, dist_bag, sim_bag
from ._baystat import Baystat, dist_baystat, sim_baystat
from ._chebyshev import Chebyshev, chebyshev
from ._cosine import Cosine, dist_cosine, sim_cosine
from ._damerau_levenshtein import (
    DamerauLevenshtein,
    damerau_levenshtein,
    dist_damerau,
    sim_damerau,
)
from ._dice import Dice, dist_dice, sim_dice
from ._editex import Editex, dist_editex, editex, sim_editex
from ._euclidean import Euclidean, dist_euclidean, euclidean, sim_euclidean
from ._eudex import Eudex, dist_eudex, eudex_hamming, sim_eudex
from ._gotoh import Gotoh, gotoh
from ._hamming import Hamming, dist_hamming, hamming, sim_hamming
from ._ident import Ident, dist_ident, sim_ident
from ._indel import Indel, dist_indel, indel, sim_indel
from ._jaccard import Jaccard, dist_jaccard, sim_jaccard, tanimoto
from ._jaro_winkler import JaroWinkler, dist_jaro_winkler, sim_jaro_winkler
from ._lcsseq import LCSseq, dist_lcsseq, lcsseq, sim_lcsseq
from ._lcsstr import LCSstr, dist_lcsstr, lcsstr, sim_lcsstr
from ._length import Length, dist_length, sim_length
from ._levenshtein import (
    Levenshtein,
    dist_levenshtein,
    levenshtein,
    sim_levenshtein,
)
from ._manhattan import Manhattan, dist_manhattan, manhattan, sim_manhattan
from ._minkowski import Minkowski, dist_minkowski, minkowski, sim_minkowski
from ._mlipns import MLIPNS, dist_mlipns, sim_mlipns
from ._monge_elkan import MongeElkan, dist_monge_elkan, sim_monge_elkan
from ._mra import MRA, dist_mra, mra_compare, sim_mra
from ._ncd_arith import NCDarith, dist_ncd_arith, sim_ncd_arith
from ._ncd_bwtrle import NCDbwtrle, dist_ncd_bwtrle, sim_ncd_bwtrle
from ._ncd_bz2 import NCDbz2, dist_ncd_bz2, sim_ncd_bz2
from ._ncd_lzma import NCDlzma, dist_ncd_lzma, sim_ncd_lzma
from ._ncd_rle import NCDrle, dist_ncd_rle, sim_ncd_rle
from ._ncd_zlib import NCDzlib, dist_ncd_zlib, sim_ncd_zlib
from ._needleman_wunsch import NeedlemanWunsch, needleman_wunsch
from ._overlap import Overlap, dist_overlap, sim_overlap
from ._prefix import Prefix, dist_prefix, sim_prefix
from ._ratcliff_obershelp import (
    RatcliffObershelp,
    dist_ratcliff_obershelp,
    sim_ratcliff_obershelp,
)
from ._sift4 import Sift4, dist_sift4, sift4_common, sim_sift4
from ._sift4_simplest import Sift4Simplest, sift4_simplest
from ._smith_waterman import SmithWaterman, smith_waterman
from ._strcmp95 import Strcmp95, dist_strcmp95, sim_strcmp95
from ._suffix import Suffix, dist_suffix, sim_suffix
from ._synoname import Synoname, synoname
from ._tversky import Tversky, dist_tversky, sim_tversky
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
    'indel',
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
    'NCDarith',
    'dist_ncd_arith',
    'sim_ncd_arith',
    'NCDbwtrle',
    'dist_ncd_bwtrle',
    'sim_ncd_bwtrle',
    'NCDrle',
    'dist_ncd_rle',
    'sim_ncd_rle',
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

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    method : function
        Specifies the similarity metric (:py:func:`sim_levenshtein` by default)

    Returns
    -------
    float
        Similarity according to the specified function

    Raises
    ------
    AttributeError
        Unknown distance function

    Examples
    --------
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

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    method : function
        Specifies the similarity metric (:py:func:`sim_levenshtein` by default)
        -- Note that this takes a similarity metric function, not a distance
        metric function.

    Returns
    -------
    float
        Distance according to the specified function

    Raises
    ------
    AttributeError
        Unknown distance function

    Examples
    --------
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
