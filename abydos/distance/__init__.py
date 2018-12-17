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
    - Russel & Rao similarity (:py:class:`.RusselRao`)
    - AMPLE similarity (:py:class:`.AMPLE`)
    - Anderberg similarity (:py:class:`.Anderberg`)
    - Baroni-Urbani & Buser I similarity (:py:class:`.BaroniUrbaniBuserI`)
    - Baroni-Urbani & Buser II similarity (:py:class:`.BaroniUrbaniBuserII`)
    - Braun & Banquest similarity (:py:class:`.BraunBanquest`)
    - Canberra distance (:py:class:`.Canberra`)
    - Chord distance (:py:class:`.Chord`)
    - Cole similarity (:py:class:`.Cole`)
    - Czekanowski similarity (:py:class:`.Czekanowski`)
    - Dennis similarity (:py:class:`.Dennis`)
    - Dispersion similarity (:py:class:`.Dispersion`)
    - Driver & Kroeber similarity (:py:class:`.DriverKroeber`)
    - Dunning similarity (:py:class:`.Dunning`)
    - Excoffier similarity (:py:class:`.Excoffier`)
    - Eyraud similarity (:py:class:`.Eyraud`)
    - Fager similarity (:py:class:`.Fager`)
    - Fager & McGowan similarity (:py:class:`.FagerMcGowan`)
    - Faith similarity (:py:class:`.Faith`)
    - Forbes I similarity (:py:class:`.ForbesI`)
    - Forbes II similarity (:py:class:`.ForbesII`)
    - Fossum similarity (:py:class:`.Fossum`)
    - Gilbert & Wells similarity (:py:class:`.GilbertWells`)
    - Goodman & Kruskal similarity (:py:class:`.GoodmanKruskal`)
    - Gower similarity (:py:class:`.Gower`)
    - Gower & Legendre similarity (:py:class:`.GowerLegendre`)
    - Hamann similarity (:py:class:`.Hamann`)
    - Hellinger distance (:py:class:`.Hellinger`)
    - Johnson similarity (:py:class:`.Johnson`)
    - Kocher & Wong similarity (:py:class:`.KocherWong`)
    - Kulczynski I similarity (:py:class:`.KulczynskiI`)
    - Kulczynski II similarity (:py:class:`.KulczynskiII`)
    - McConnaughey similarity (:py:class:`.McConnaughey`)
    - Mean Manhattan distance (:py:class:`.MeanManhattan`)
    - Michael similarity (:py:class:`.Michael`)
    - Michelet similarity (:py:class:`.Michelet`)
    - Mountford similarity (:py:class:`.Mountford`)
    - Mutual Information similarity (:py:class:`.MutualInformation`)
    - Nei & Li similarity (:py:class:`.NeiLi`)
    - Ochiai II similarity (:py:class:`.OchiaiII`)
    - Pattern Difference distance (:py:class:`.PatternDifference`)
    - Pearson & Heron II similarity (:py:class:`.PearsonHeronII`)
    - Pearson II similarity (:py:class:`.PearsonII`)
    - Pearson III similarity (:py:class:`.PearsonIII`)
    - Pearson's Chi-Squared similarity (:py:class:`.PearsonChiSquared`)
    - Pearson's Phi similarity (:py:class:`.PearsonPhi`)
    - Peirce similarity (:py:class:`.Peirce`)
    - Phi Squared similarity (:py:class:`.PhiSquared`)
    - Rogers & Tanimoto similarity (:py:class:`.RogersTanimoto`)
    - Roux I similarity (:py:class:`.RouxI`)
    - Roux II similarity (:py:class:`.RouxII`)
    - Shape Difference distance (:py:class:`.ShapeDifference`)
    - Simpson similarity (:py:class:`.Simpson`)
    - Size Difference distance (:py:class:`.SizeDifference`)
    - Sokal & Michener similarity (:py:class:`.SokalMichener`)
    - Sokal & Sneath I similarity (:py:class:`.SokalSneathI`)
    - Sokal & Sneath II similarity (:py:class:`.SokalSneathII`)
    - Sokal & Sneath III similarity (:py:class:`.SokalSneathIII`)
    - Sokal & Sneath IV similarity (:py:class:`.SokalSneathIV`)
    - Sokal & Sneath V similarity (:py:class:`.SokalSneathV`)
    - Sorgenfrei similarity (:py:class:`.Sorgenfrei`)
    - Squared Euclid distance (:py:class:`.SquaredEuclid`)
    - Stiles similarity (:py:class:`.Stiles`)
    - Tarantula similarity (:py:class:`.Tarantula`)
    - Tarwid similarity (:py:class:`.Tarwid`)
    - Triple Weighted Jaccard similarity (:py:class:`.TripleWeightedJaccard`)
    - Upholt similarity (:py:class:`.Upholt`)
    - Vari distance (:py:class:`.Vari`)
    - Yule's Q similarity (:py:class:`.YuleQ`)
    - Yule's Sigma similarity (:py:class:`.YuleSigma`)
    - Bag distance (:py:class:`.Bag`)
    - Monge-Elkan distance (:py:class:`.MongeElkan`)

A set of fuzzy token-based distance metrics are provided:

    - Fuzzy Tversky distance (:py:class:`.FuzzyTversky`)
    - Fuzzy Dice similarity (:py:class:`.FuzzyDice`)
    - Fuzzy Jaccard similarity (:py:class:`.FuzzyJaccard`)
    - Fuzzy Tanimoto coefficient (:py:meth:`.FuzzyJaccard.tanimoto_coeff`)
    - Fuzzy overlap distance (:py:class:`.FuzzyOverlap`)
    - Fuzzy cosine similarity (:py:class:`.FuzzyCosine`)

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
    - Ozbay metric (:py:class:`.Ozbay`)

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

from ._ample import AMPLE
from ._anderberg import Anderberg
from ._bag import Bag, bag, dist_bag, sim_bag
from ._baroni_urbani_buser_i import BaroniUrbaniBuserI
from ._baroni_urbani_buser_ii import BaroniUrbaniBuserII
from ._baystat import Baystat, dist_baystat, sim_baystat
from ._braun_banquest import BraunBanquest
from ._canberra import Canberra
from ._chebyshev import Chebyshev, chebyshev
from ._chord import Chord
from ._cole import Cole
from ._cosine import Cosine, dist_cosine, sim_cosine
from ._czekanowski import Czekanowski
from ._damerau_levenshtein import (
    DamerauLevenshtein,
    damerau_levenshtein,
    dist_damerau,
    sim_damerau,
)
from ._dennis import Dennis
from ._dice import Dice, dist_dice, sim_dice
from ._dispersion import Dispersion
from ._driver_kroeber import DriverKroeber
from ._dunning import Dunning
from ._editex import Editex, dist_editex, editex, sim_editex
from ._euclidean import Euclidean, dist_euclidean, euclidean, sim_euclidean
from ._eudex import Eudex, dist_eudex, eudex_hamming, sim_eudex
from ._excoffier import Excoffier
from ._eyraud import Eyraud
from ._fager import Fager
from ._fager_mcgowan import FagerMcGowan
from ._faith import Faith
from ._forbes_i import ForbesI
from ._forbes_ii import ForbesII
from ._fossum import Fossum
from ._gilbert_wells import GilbertWells
from ._goodman_kruskal import GoodmanKruskal
from ._gotoh import Gotoh, gotoh
from ._gower import Gower
from ._gower_legendre import GowerLegendre
from ._hamann import Hamann
from ._hamming import Hamming, dist_hamming, hamming, sim_hamming
from ._hellinger import Hellinger
from ._ident import Ident, dist_ident, sim_ident
from ._indel import Indel, dist_indel, indel, sim_indel
from ._jaccard import Jaccard, dist_jaccard, sim_jaccard, tanimoto
from ._jaro_winkler import JaroWinkler, dist_jaro_winkler, sim_jaro_winkler
from ._johnson import Johnson
from ._kocher_wong import KocherWong
from ._kulczynski_i import KulczynskiI
from ._kulczynski_ii import KulczynskiII
from ._lcprefix import LCPrefix
from ._lcsseq import LCSseq, dist_lcsseq, lcsseq, sim_lcsseq
from ._lcsstr import LCSstr, dist_lcsstr, lcsstr, sim_lcsstr
from ._lcsuffix import LCSuffix
from ._length import Length, dist_length, sim_length
from ._levenshtein import (
    Levenshtein,
    dist_levenshtein,
    levenshtein,
    sim_levenshtein,
)
from ._manhattan import Manhattan, dist_manhattan, manhattan, sim_manhattan
from ._mcconnaughey import McConnaughey
from ._mean_manhattan import MeanManhattan
from ._michael import Michael
from ._michelet import Michelet
from ._minkowski import Minkowski, dist_minkowski, minkowski, sim_minkowski
from ._mlipns import MLIPNS, dist_mlipns, sim_mlipns
from ._monge_elkan import MongeElkan, dist_monge_elkan, sim_monge_elkan
from ._mountford import Mountford
from ._mra import MRA, dist_mra, mra_compare, sim_mra
from ._mutual_information import MutualInformation
from ._ncd_arith import NCDarith, dist_ncd_arith, sim_ncd_arith
from ._ncd_bwtrle import NCDbwtrle, dist_ncd_bwtrle, sim_ncd_bwtrle
from ._ncd_bz2 import NCDbz2, dist_ncd_bz2, sim_ncd_bz2
from ._ncd_lzma import NCDlzma, dist_ncd_lzma, sim_ncd_lzma
from ._ncd_rle import NCDrle, dist_ncd_rle, sim_ncd_rle
from ._ncd_zlib import NCDzlib, dist_ncd_zlib, sim_ncd_zlib
from ._needleman_wunsch import NeedlemanWunsch, needleman_wunsch
from ._nei_li import NeiLi
from ._ochiai_ii import OchiaiII
from ._overlap import Overlap, dist_overlap, sim_overlap
from ._ozbay import Ozbay
from ._pattern_difference import PatternDifference
from ._pearson_heron_ii import PearsonHeronII
from ._pearson_ii import PearsonII
from ._pearson_iii import PearsonIII
from ._pearson_chi_squared import PearsonChiSquared
from ._pearson_phi import PearsonPhi
from ._peirce import Peirce
from ._phi_squared import PhiSquared
from ._prefix import Prefix, dist_prefix, sim_prefix
from ._ratcliff_obershelp import (
    RatcliffObershelp,
    dist_ratcliff_obershelp,
    sim_ratcliff_obershelp,
)
from ._rogers_tanimoto import RogersTanimoto
from ._roux_i import RouxI
from ._roux_ii import RouxII
from ._russell_rao import RussellRao
from ._shape_difference import ShapeDifference
from ._sift4 import Sift4, dist_sift4, sift4_common, sim_sift4
from ._sift4_simplest import Sift4Simplest, sift4_simplest
from ._simpson import Simpson
from ._size_difference import SizeDifference
from ._smith_waterman import SmithWaterman, smith_waterman
from ._soft_cosine import SoftCosine
from ._sokal_michener import SokalMichener
from ._sokal_sneath_i import SokalSneathI
from ._sokal_sneath_ii import SokalSneathII
from ._sokal_sneath_iii import SokalSneathIII
from ._sokal_sneath_iv import SokalSneathIV
from ._sokal_sneath_v import SokalSneathV
from ._sorgenfrei import Sorgenfrei
from ._squared_euclid import SquaredEuclid
from ._stiles import Stiles
from ._strcmp95 import Strcmp95, dist_strcmp95, sim_strcmp95
from ._suffix import Suffix, dist_suffix, sim_suffix
from ._synoname import Synoname, synoname
from ._tarantula import Tarantula
from ._tarwid import Tarwid
from ._triple_weighted_jaccard import TripleWeightedJaccard
from ._tversky import Tversky, dist_tversky, sim_tversky
from ._typo import Typo, dist_typo, sim_typo, typo
from ._upholt import Upholt
from ._vari import Vari
from ._yule_q import YuleQ
from ._yule_sigma import YuleSigma

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
    'RussellRao',
    'AMPLE',
    'Anderberg',
    'BaroniUrbaniBuserI',
    'BaroniUrbaniBuserII',
    'BraunBanquest',
    'Canberra',
    'Chord',
    'Cole',
    'Czekanowski',
    'Dennis',
    'Dispersion',
    'DriverKroeber',
    'Dunning',
    'Excoffier',
    'Eyraud',
    'Fager',
    'FagerMcGowan',
    'Faith',
    'ForbesI',
    'ForbesII',
    'Fossum',
    'GilbertWells',
    'GoodmanKruskal',
    'Gower',
    'GowerLegendre',
    'Hamann',
    'Hellinger',
    'Johnson',
    'KocherWong',
    'KulczynskiI',
    'KulczynskiII',
    'McConnaughey',
    'MeanManhattan',
    'Michael',
    'Michelet',
    'Mountford',
    'MutualInformation',
    'NeiLi',
    'OchiaiII',
    'PatternDifference',
    'PearsonHeronII',
    'PearsonII',
    'PearsonIII',
    'PearsonChiSquared',
    'PearsonPhi',
    'Peirce',
    'PhiSquared',
    'RogersTanimoto',
    'RouxI',
    'RouxII',
    'ShapeDifference',
    'Simpson',
    'SizeDifference',
    'SokalMichener',
    'SokalSneathI',
    'SokalSneathII',
    'SokalSneathIII',
    'SokalSneathIV',
    'SokalSneathV',
    'Sorgenfrei',
    'SquaredEuclid',
    'Stiles',
    'Tarantula',
    'Tarwid',
    'TripleWeightedJaccard',
    'Upholt',
    'Vari',
    'YuleQ',
    'YuleSigma',
    'Bag',
    'bag',
    'dist_bag',
    'sim_bag',
    'MongeElkan',
    'dist_monge_elkan',
    'sim_monge_elkan',
    'SoftCosine',
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
    'LCPrefix',
    'LCSuffix',
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
    'Ozbay',
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

    .. versionadded:: 0.1.0

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

    .. versionadded:: 0.1.0

    """
    if callable(method):
        return 1 - method(src, tar)
    else:
        raise AttributeError('Unknown distance function: ' + str(method))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
