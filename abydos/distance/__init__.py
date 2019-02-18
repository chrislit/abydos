# -*- coding: utf-8 -*-

# Copyright 2014-2019 by Christopher C. Little.
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

r"""abydos.distance.

The distance package implements string distance measure and metric classes:

These include traditional Levenshtein edit distance and related algorithms:

    - Levenshtein distance (:py:class:`.Levenshtein`)
    - Optimal String Alignment distance (:py:class:`.Levenshtein` with
      ``mode='osa'``)
    - Damerau-Levenshtein distance (:py:class:`.DamerauLevenshtein`)
    - Shapira-Storer edit distance with moves (:py:class:`.ShapiraStorer`)
    - Yujian-Bo normalized edit distance (:py:class:`.YujianBo`)
    - Higuera-Micó contextual normalized edit distance
      (:py:class:`.HigueraMico`)
    - Indel distance (:py:class:`.Indel`)
    - Syllable Alignment Pattern Searching similarity
      (:py:class:`.distance.SAPS`)
    - Meta-Levenshtein distance (:py:class:`.MetaLevenshtein`)
    - Covington distance (:py:class:`.Covington`)
    - ALINE distance (:py:class:`.ALINE`)
    - FlexMetric distance (:py:class:`.FlexMetric`)
    - BI-SIM similarity (:py:class:`.BISIM`)

Hamming distance (:py:class:`.Hamming`) and the closely related Modified
Language-Independent Product Name Search distance (:py:class:`.MLIPNS`) are
provided.

Block edit distances:

    - Tichy edit distance (:py:class:`.Tichy`)
    - Levenshtein distance with block operations
      (:py:class:`.BlockLevenshtein`)
    - Rees-Levenshtein distance (:py:class:`.ReesLevenshtein`)
    - Cormode's LZ distance (:py:class:`.CormodeLZ`)

Distance metrics developed for the US Census or derived from them are included:

    - Jaro distance (:py:class:`.JaroWinkler` with ``mode='Jaro'``)
    - Jaro-Winkler distance (:py:class:`.JaroWinkler`)
    - Strcmp95 distance (:py:class:`.Strcmp95`)
    - Iterative-SubString (I-Sub) similarity
      (:py:class:`.StoilosStamouKollias`)

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
    - Russell & Rao similarity (:py:class:`.RussellRao`)
    - AMPLE similarity (:py:class:`.AMPLE`)
    - AZZOO similarity (:py:class:`.AZZOO`)
    - Anderberg similarity (:py:class:`.Anderberg`)
    - Andres & Marzo's Delta similarity (:py:class:`.AndresMarzoDelta`)
    - Baroni-Urbani & Buser I similarity (:py:class:`.BaroniUrbaniBuserI`)
    - Baroni-Urbani & Buser II similarity (:py:class:`.BaroniUrbaniBuserII`)
    - Batagelj & Bren similarity (:py:class:`.BatageljBren`)
    - Baulieu I distance (:py:class:`.BaulieuI`)
    - Baulieu II distance (:py:class:`.BaulieuII`)
    - Baulieu III distance (:py:class:`.BaulieuIII`)
    - Benini similarity (:py:class:`.Benini`)
    - Bennet's Sigma similarity (:py:class:`.BennetSigma`)
    - Braun & Blanquet similarity (:py:class:`.BraunBlanquet`)
    - Canberra distance (:py:class:`.Canberra`)
    - Chord distance (:py:class:`.Chord`)
    - Clement similarity (:py:class:`.Clement`)
    - Cohen's Kappa similarity (:py:class:`.CohenKappa`)
    - Cole similarity (:py:class:`.Cole`)
    - Consonni & Todeschini I similarity (:py:class:`.ConsonniTodeschiniI`)
    - Consonni & Todeschini II similarity (:py:class:`.ConsonniTodeschiniII`)
    - Consonni & Todeschini III similarity (:py:class:`.ConsonniTodeschiniIII`)
    - Consonni & Todeschini IV similarity (:py:class:`.ConsonniTodeschiniIV`)
    - Consonni & Todeschini V similarity (:py:class:`.ConsonniTodeschiniV`)
    - Dennis similarity (:py:class:`.Dennis`)
    - Dice's Asymmetric I similarity (:py:class:`.DiceAsymmetricI`)
    - Dice's Asymmetric II similarity (:py:class:`.DiceAsymmetricII`)
    - Digby similarity (:py:class:`.Digby`)
    - Dispersion similarity (:py:class:`.Dispersion`)
    - Doolittle similarity (:py:class:`.Doolittle`)
    - Dunning similarity (:py:class:`.Dunning`)
    - Eyraud similarity (:py:class:`.Eyraud`)
    - Fager similarity (:py:class:`.Fager`)
    - Fager & McGowan similarity (:py:class:`.FagerMcGowan`)
    - Faith similarity (:py:class:`.Faith`)
    - Fidelity similarity (:py:class:`.Fidelity`)
    - Fleiss similarity (:py:class:`.Fleiss`)
    - Fleiss-Levin-Paik similarity (:py:class:`.FleissLevinPaik`)
    - Forbes I similarity (:py:class:`.ForbesI`)
    - Forbes II similarity (:py:class:`.ForbesII`)
    - Fossum similarity (:py:class:`.Fossum`)
    - Generalized Fleiss similarity (:py:class:`.GeneralizedFleiss`)
    - Gilbert similarity (:py:class:`.Gilbert`)
    - Gilbert & Wells similarity (:py:class:`.GilbertWells`)
    - Gini distance (:py:class:`.Gini`)
    - Goodall similarity (:py:class:`.Goodall`)
    - Goodman & Kruskal's Lambda similarity (:py:class:`.GoodmanKruskalLambda`)
    - Goodman & Kruskal's Lambda R similarity
      (:py:class:`.GoodmanKruskalLambdaR`)
    - Goodman & Kruskal's Tau A similarity (:py:class:`.GoodmanKruskalTauA`)
    - Goodman & Kruskal's Tau B similarity (:py:class:`.GoodmanKruskalTauB`)
    - Gower & Legendre similarity (:py:class:`.GowerLegendre`)
    - Guttman Lambda A similarity (:py:class:`.GuttmanLambdaA`)
    - Guttman Lambda B similarity (:py:class:`.GuttmanLambdaB`)
    - Gwet's Gamma similarity (:py:class:`.GwetGamma`)
    - Hamann similarity (:py:class:`.Hamann`)
    - Harris & Lahey similarity (:py:class:`.HarrisLahey`)
    - Hassanat distance (:py:class:`.Hassanat`)
    - Hawkins & Dotson similarity (:py:class:`.HawkinsDotson`)
    - Hellinger distance (:py:class:`.Hellinger`)
    - Hurlbert similarity (:py:class:`.Hurlbert`)
    - Jaccard-NM similarity (:py:class:`.JaccardNM`)
    - Johnson similarity (:py:class:`.Johnson`)
    - Kendall's Tau similarity (:py:class:`.KendallTau`)
    - Kent & Foster I similarity (:py:class:`.KentFosterI`)
    - Kent & Foster II similarity (:py:class:`.KentFosterII`)
    - Köppen I similarity (:py:class:`.KoppenI`)
    - Köppen II similarity (:py:class:`.KoppenII`)
    - Kuder & Richardson similarity (:py:class:`.KuderRichardson`)
    - Kuhns I similarity (:py:class:`.KuhnsI`)
    - Kuhns II similarity (:py:class:`.KuhnsII`)
    - Kuhns III similarity (:py:class:`.KuhnsIII`)
    - Kuhns IV similarity (:py:class:`.KuhnsIV`)
    - Kuhns IX similarity (:py:class:`.KuhnsIX`)
    - Kuhns V similarity (:py:class:`.KuhnsV`)
    - Kuhns VI similarity (:py:class:`.KuhnsVI`)
    - Kuhns VII similarity (:py:class:`.KuhnsVII`)
    - Kuhns VIII similarity (:py:class:`.KuhnsVIII`)
    - Kuhns X similarity (:py:class:`.KuhnsX`)
    - Kuhns XI similarity (:py:class:`.KuhnsXI`)
    - Kuhns XII similarity (:py:class:`.KuhnsXII`)
    - Kulczynski I similarity (:py:class:`.KulczynskiI`)
    - Kulczynski II similarity (:py:class:`.KulczynskiII`)
    - Lorentzian distance (:py:class:`.Lorentzian`)
    - Maarel similarity (:py:class:`.Maarel`)
    - marking distance (:py:class:`.Marking`)
    - MASI similarity (:py:class:`.MASI`)
    - Matusita distance (:py:class:`.Matusita`)
    - Maxwell & Pilliner similarity (:py:class:`.MaxwellPilliner`)
    - McConnaughey similarity (:py:class:`.McConnaughey`)
    - Michael similarity (:py:class:`.Michael`)
    - Mountford similarity (:py:class:`.Mountford`)
    - Mutual Information similarity (:py:class:`.MutualInformation`)
    - Pattern difference (:py:class:`.Pattern`)
    - Pearson & Heron II similarity (:py:class:`.PearsonHeronII`)
    - Pearson II similarity (:py:class:`.PearsonII`)
    - Pearson III similarity (:py:class:`.PearsonIII`)
    - Pearson's Chi-Squared similarity (:py:class:`.PearsonChiSquared`)
    - Pearson's Phi (:py:class:`.PearsonPhi`)
    - Peirce similarity (:py:class:`.Peirce`)
    - q-gram distance (:py:class:`.QGram`)
    - Rogers & Tanimoto similarity (:py:class:`.RogersTanimoto`)
    - Rogot & Goldberg similarity (:py:class:`.RogotGoldberg`)
    - Scott's Pi similarity (:py:class:`.ScottPi`)
    - Shape difference (:py:class:`.Shape`)
    - Size difference (:py:class:`.Size`)
    - Sokal & Michener similarity (:py:class:`.SokalMichener`)
    - Sokal & Sneath I similarity (:py:class:`.SokalSneathI`)
    - Sokal & Sneath II similarity (:py:class:`.SokalSneathII`)
    - Sokal & Sneath III similarity (:py:class:`.SokalSneathIII`)
    - Sokal & Sneath IV similarity (:py:class:`.SokalSneathIV`)
    - Sokal & Sneath V similarity (:py:class:`.SokalSneathV`)
    - Sorgenfrei similarity (:py:class:`.Sorgenfrei`)
    - Steffensen similarity (:py:class:`.Steffensen`)
    - Stiles similarity (:py:class:`.Stiles`)
    - Stuart's Tau similarity (:py:class:`.StuartTau`)
    - Tarantula similarity (:py:class:`.Tarantula`)
    - Tarwid similarity (:py:class:`.Tarwid`)
    - Tulloss' R similarity (:py:class:`.TullossR`)
    - Tulloss' S similarity (:py:class:`.TullossS`)
    - Tulloss' T similarity (:py:class:`.TullossT`)
    - Tulloss' U similarity (:py:class:`.TullossU`)
    - Weighted Jaccard similarity (:py:class:`.WeightedJaccard`)
    - Unknown A similarity (:py:class:`.UnknownA`)
    - Unknown B similarity (:py:class:`.UnknownB`)
    - Unknown C similarity (:py:class:`.UnknownC`)
    - Unknown D similarity (:py:class:`.UnknownD`)
    - Unknown E similarity (:py:class:`.UnknownE`)
    - Unknown F similarity (:py:class:`.UnknownF`)
    - Unknown G similarity (:py:class:`.UnknownG`)
    - Unknown H similarity (:py:class:`.UnknownH`)
    - Unknown I similarity (:py:class:`.UnknownI`)
    - Unknown J similarity (:py:class:`.UnknownJ`)
    - Unknown K similarity (:py:class:`.UnknownK`)
    - Unknown L similarity (:py:class:`.UnknownL`)
    - Unknown M similarity (:py:class:`.UnknownM`)
    - Unknown N similarity (:py:class:`.UnknownN`)
    - Unknown O similarity (:py:class:`.UnknownO`)
    - Upholt similarity (:py:class:`.Upholt`)
    - Warrens I similarity (:py:class:`.WarrensI`)
    - Warrens II similarity (:py:class:`.WarrensII`)
    - Warrens III similarity (:py:class:`.WarrensIII`)
    - Warrens IV similarity (:py:class:`.WarrensIV`)
    - Warrens V similarity (:py:class:`.WarrensV`)
    - Whittaker distance (:py:class:`.Whittaker`)
    - Yates' Chi-Squared similarity (:py:class:`.YatesChiSquared`)
    - Yule's Q similarity (:py:class:`.YuleQ`)
    - Yule's Q II distance (:py:class:`.YuleQII`)
    - Yule's Y similarity (:py:class:`.YuleY`)
    - YJHHR distance (:py:class:`.YJHHR`)

    - Bhattacharyya distance (:py:class:`.Bhattacharyya`)
    - Brainerd-Robinson similarity (:py:class:`.BrainerdRobinson`)
    - Quantitative Cosine similarity (:py:class:`.QuantitativeCosine`)
    - Quantitative Dice similarity (:py:class:`.QuantitativeDice`)
    - Quantitative Jaccard similarity (:py:class:`.QuantitativeJaccard`)
    - Roberts similarity (:py:class:`.Roberts`)
    - Average linkage distance (:py:class:`.AverageLinkage`)
    - Single linkage distance (:py:class:`.SingleLinkage`)
    - Complete linkage distance (:py:class:`.CompleteLinkage`)

    - Bag distance (:py:class:`.Bag`)
    - Soft cosine similarity (:py:class:`.SoftCosine`)
    - Monge-Elkan distance (:py:class:`.MongeElkan`)
    - TF-IDF similarity (:py:class:`.TFIDF`)
    - SoftTF-IDF similarity (:py:class:`.SoftTFIDF`)
    - Jensen-Shannon distance (:py:class:`.JensenShannon`)
    - Simplified Fellegi-Sunter distance (:py:class:`.FellegiSunter`)
    - MinHash similarity (:py:class:`.MinHash`)

    - BLEU similarity (:py:class:`.BLEU`)
    - Rouge-L similarity (:py:class:`.RougeL`)
    - Rouge-W similarity (:py:class:`.RougeW`)
    - Rouge-S similarity (:py:class:`.RougeS`)
    - Rouge-SU similarity (:py:class:`.RougeSU`)

    - Positional Q-Gram Dice distance (:py:class:`.PositionalQGramDice`)
    - Positional Q-Gram Jaccard distance (:py:class:`.PositionalQGramJaccard`)
    - Positional Q-Gram Overlap distance (:py:class:`.PositionalQGramOverlap`)

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
    - LZSS (:py:class:`.NCDlzss`)
    - arithmetic coding (:py:class:`.NCDarith`)
    - PAQ9A (:py:class:`.NCDpaq9a`)
    - BWT plus RLE (:py:class:`.NCDbwtrle`)
    - RLE (:py:class:`.NCDrle`)

Three similarity measures from SeatGeek's FuzzyWuzzy:

    - FuzzyWuzzy Partial String similarity
      (:py:class:`FuzzyWuzzyPartialString`)
    - FuzzyWuzzy Token Sort similarity (:py:class:`FuzzyWuzzyTokenSort`)
    - FuzzyWuzzy Token Set similarity (:py:class:`FuzzyWuzzyTokenSet`)

The remaining distance measures & metrics include:

    - Western Airlines' Match Rating Algorithm comparison
      (:py:class:`.distance.MRA`)
    - Editex (:py:class:`.Editex`)
    - Bavarian Landesamt für Statistik distance (:py:class:`.Baystat`)
    - Eudex distance (:py:class:`.distance.Eudex`)
    - Sift4 distance (:py:class:`.Sift4`, :py:class:`.Sift4Simplest`,
      :py:class:`.Sift4Extended`)
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

from ._aline import ALINE
from ._ample import AMPLE
from ._anderberg import Anderberg
from ._andres_marzo_delta import AndresMarzoDelta
from ._average_linkage import AverageLinkage
from ._azzoo import AZZOO
from ._bag import Bag, bag, dist_bag, sim_bag
from ._baroni_urbani_buser_i import BaroniUrbaniBuserI
from ._baroni_urbani_buser_ii import BaroniUrbaniBuserII
from ._batagelj_bren import BatageljBren
from ._baulieu_i import BaulieuI
from ._baulieu_ii import BaulieuII
from ._baulieu_iii import BaulieuIII
from ._baystat import Baystat, dist_baystat, sim_baystat
from ._benini import Benini
from ._bennet_sigma import BennetSigma
from ._bhattacharyya import Bhattacharyya
from ._bi_sim import BISIM
from ._bleu import BLEU
from ._block_levenshtein import BlockLevenshtein
from ._brainerd_robinson import BrainerdRobinson
from ._braun_blanquet import BraunBlanquet
from ._canberra import Canberra
from ._chebyshev import Chebyshev, chebyshev
from ._chord import Chord
from ._clement import Clement
from ._cohen_kappa import CohenKappa
from ._cole import Cole
from ._complete_linkage import CompleteLinkage
from ._consonni_todeschini_i import ConsonniTodeschiniI
from ._consonni_todeschini_ii import ConsonniTodeschiniII
from ._consonni_todeschini_iii import ConsonniTodeschiniIII
from ._consonni_todeschini_iv import ConsonniTodeschiniIV
from ._consonni_todeschini_v import ConsonniTodeschiniV
from ._cormode_lz import CormodeLZ
from ._cosine import Cosine, dist_cosine, sim_cosine
from ._covington import Covington
from ._damerau_levenshtein import (
    DamerauLevenshtein,
    damerau_levenshtein,
    dist_damerau,
    sim_damerau,
)
from ._dennis import Dennis
from ._dice import Dice, dist_dice, sim_dice
from ._dice_asymmetric_i import DiceAsymmetricI
from ._dice_asymmetric_ii import DiceAsymmetricII
from ._digby import Digby
from ._dispersion import Dispersion
from ._distance import _Distance
from ._doolittle import Doolittle
from ._dunning import Dunning
from ._editex import Editex, dist_editex, editex, sim_editex
from ._euclidean import Euclidean, dist_euclidean, euclidean, sim_euclidean
from ._eudex import Eudex, dist_eudex, eudex_hamming, sim_eudex
from ._eyraud import Eyraud
from ._fager import Fager
from ._fager_mcgowan import FagerMcGowan
from ._faith import Faith
from ._fellegi_sunter import FellegiSunter
from ._fidelity import Fidelity
from ._fleiss import Fleiss
from ._fleiss_levin_paik import FleissLevinPaik
from ._flexmetric import FlexMetric
from ._forbes_i import ForbesI
from ._forbes_ii import ForbesII
from ._fossum import Fossum
from ._fuzzywuzzy_partial_string import FuzzyWuzzyPartialString
from ._fuzzywuzzy_token_set import FuzzyWuzzyTokenSet
from ._fuzzywuzzy_token_sort import FuzzyWuzzyTokenSort
from ._generalized_fleiss import GeneralizedFleiss
from ._gilbert import Gilbert
from ._gilbert_wells import GilbertWells
from ._gini import Gini
from ._goodall import Goodall
from ._goodman_kruskal_lambda import GoodmanKruskalLambda
from ._goodman_kruskal_lambda_r import GoodmanKruskalLambdaR
from ._goodman_kruskal_tau_a import GoodmanKruskalTauA
from ._goodman_kruskal_tau_b import GoodmanKruskalTauB
from ._gotoh import Gotoh, gotoh
from ._gower_legendre import GowerLegendre
from ._guttman_lambda_a import GuttmanLambdaA
from ._guttman_lambda_b import GuttmanLambdaB
from ._gwet_gamma import GwetGamma
from ._hamann import Hamann
from ._hamming import Hamming, dist_hamming, hamming, sim_hamming
from ._harris_lahey import HarrisLahey
from ._hassanat import Hassanat
from ._hawkins_dotson import HawkinsDotson
from ._hellinger import Hellinger
from ._higuera_mico import HigueraMico
from ._hurlbert import Hurlbert
from ._ident import Ident, dist_ident, sim_ident
from ._indel import Indel, dist_indel, indel, sim_indel
from ._iterative_substring import IterativeSubString
from ._jaccard import Jaccard, dist_jaccard, sim_jaccard, tanimoto
from ._jaccard_nm import JaccardNM
from ._jaro_winkler import JaroWinkler, dist_jaro_winkler, sim_jaro_winkler
from ._jensen_shannon import JensenShannon
from ._johnson import Johnson
from ._kendall_tau import KendallTau
from ._kent_foster_i import KentFosterI
from ._kent_foster_ii import KentFosterII
from ._koppen_i import KoppenI
from ._koppen_ii import KoppenII
from ._kuder_richardson import KuderRichardson
from ._kuhns_i import KuhnsI
from ._kuhns_ii import KuhnsII
from ._kuhns_iii import KuhnsIII
from ._kuhns_iv import KuhnsIV
from ._kuhns_ix import KuhnsIX
from ._kuhns_v import KuhnsV
from ._kuhns_vi import KuhnsVI
from ._kuhns_vii import KuhnsVII
from ._kuhns_viii import KuhnsVIII
from ._kuhns_x import KuhnsX
from ._kuhns_xi import KuhnsXI
from ._kuhns_xii import KuhnsXII
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
from ._lorentzian import Lorentzian
from ._maarel import Maarel
from ._manhattan import Manhattan, dist_manhattan, manhattan, sim_manhattan
from ._marking import Marking
from ._masi import MASI
from ._matusita import Matusita
from ._maxwell_pilliner import MaxwellPilliner
from ._mcconnaughey import McConnaughey
from ._mcewen_michael import McEwenMichael
from ._meta_levenshtein import MetaLevenshtein
from ._minhash import MinHash
from ._minkowski import Minkowski, dist_minkowski, minkowski, sim_minkowski
from ._mlipns import MLIPNS, dist_mlipns, sim_mlipns
from ._monge_elkan import MongeElkan, dist_monge_elkan, sim_monge_elkan
from ._mountford import Mountford
from ._mra import MRA, dist_mra, mra_compare, sim_mra
from ._ms_contingency import MSContingency
from ._mutual_information import MutualInformation
from ._ncd_arith import NCDarith, dist_ncd_arith, sim_ncd_arith
from ._ncd_bwtrle import NCDbwtrle, dist_ncd_bwtrle, sim_ncd_bwtrle
from ._ncd_bz2 import NCDbz2, dist_ncd_bz2, sim_ncd_bz2
from ._ncd_lzma import NCDlzma, dist_ncd_lzma, sim_ncd_lzma
from ._ncd_lzss import NCDlzss
from ._ncd_paq9a import NCDpaq9a
from ._ncd_rle import NCDrle, dist_ncd_rle, sim_ncd_rle
from ._ncd_zlib import NCDzlib, dist_ncd_zlib, sim_ncd_zlib
from ._needleman_wunsch import NeedlemanWunsch, needleman_wunsch
from ._overlap import Overlap, dist_overlap, sim_overlap
from ._ozbay import Ozbay
from ._pattern import Pattern
from ._pearson_chi_squared import PearsonChiSquared
from ._pearson_heron_ii import PearsonHeronII
from ._pearson_ii import PearsonII
from ._pearson_iii import PearsonIII
from ._pearson_phi import PearsonPhi
from ._peirce import Peirce
from ._positional_q_gram_dice import PositionalQGramDice
from ._positional_q_gram_jaccard import PositionalQGramJaccard
from ._positional_q_gram_overlap import PositionalQGramOverlap
from ._prefix import Prefix, dist_prefix, sim_prefix
from ._q_gram import QGram
from ._quantitative_cosine import QuantitativeCosine
from ._quantitative_dice import QuantitativeDice
from ._quantitative_jaccard import QuantitativeJaccard
from ._ratcliff_obershelp import (
    RatcliffObershelp,
    dist_ratcliff_obershelp,
    sim_ratcliff_obershelp,
)
from ._rees_levenshtein import ReesLevenshtein
from ._roberts import Roberts
from ._rogers_tanimoto import RogersTanimoto
from ._rogot_goldberg import RogotGoldberg
from ._rouge_l import RougeL
from ._rouge_s import RougeS
from ._rouge_su import RougeSU
from ._rouge_w import RougeW
from ._russell_rao import RussellRao
from ._saps import SAPS
from ._scott_pi import ScottPi
from ._shape import Shape
from ._shapira_storer import ShapiraStorer
from ._sift4 import Sift4, dist_sift4, sift4_common, sim_sift4
from ._sift4_extended import Sift4Extended
from ._sift4_simplest import Sift4Simplest, sift4_simplest
from ._single_linkage import SingleLinkage
from ._size import Size
from ._smith_waterman import SmithWaterman, smith_waterman
from ._soft_cosine import SoftCosine
from ._softtf_idf import SoftTFIDF
from ._sokal_michener import SokalMichener
from ._sokal_sneath_i import SokalSneathI
from ._sokal_sneath_ii import SokalSneathII
from ._sokal_sneath_iii import SokalSneathIII
from ._sokal_sneath_iv import SokalSneathIV
from ._sokal_sneath_v import SokalSneathV
from ._sorgenfrei import Sorgenfrei
from ._steffensen import Steffensen
from ._stiles import Stiles
from ._strcmp95 import Strcmp95, dist_strcmp95, sim_strcmp95
from ._stuart_tau import StuartTau
from ._suffix import Suffix, dist_suffix, sim_suffix
from ._synoname import Synoname, synoname
from ._tarantula import Tarantula
from ._tarwid import Tarwid
from ._tetrachoric import Tetrachoric
from ._tf_idf import TFIDF
from ._tichy import Tichy
from ._token_distance import _TokenDistance
from ._tulloss_r import TullossR
from ._tulloss_s import TullossS
from ._tulloss_t import TullossT
from ._tulloss_u import TullossU
from ._tversky import Tversky, dist_tversky, sim_tversky
from ._typo import Typo, dist_typo, sim_typo, typo
from ._unknown_a import UnknownA
from ._unknown_b import UnknownB
from ._unknown_c import UnknownC
from ._unknown_d import UnknownD
from ._unknown_e import UnknownE
from ._unknown_f import UnknownF
from ._unknown_g import UnknownG
from ._unknown_h import UnknownH
from ._unknown_i import UnknownI
from ._unknown_j import UnknownJ
from ._unknown_k import UnknownK
from ._unknown_l import UnknownL
from ._unknown_m import UnknownM
from ._unknown_n import UnknownN
from ._unknown_o import UnknownO
from ._upholt import Upholt
from ._warrens_i import WarrensI
from ._warrens_ii import WarrensII
from ._warrens_iii import WarrensIII
from ._warrens_iv import WarrensIV
from ._warrens_v import WarrensV
from ._weighted_jaccard import WeightedJaccard
from ._whittaker import Whittaker
from ._yates_chi_squared import YatesChiSquared
from ._yjhhr import YJHHR
from ._yujian_bo import YujianBo
from ._yule_q import YuleQ
from ._yule_q_ii import YuleQII
from ._yule_y import YuleY

__all__ = [
    '_Distance',
    '_TokenDistance',
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
    'ShapiraStorer',
    'Marking',
    'YujianBo',
    'HigueraMico',
    'Indel',
    'indel',
    'dist_indel',
    'sim_indel',
    'SAPS',
    'MetaLevenshtein',
    'Covington',
    'ALINE',
    'FlexMetric',
    'BISIM',
    'Hamming',
    'hamming',
    'dist_hamming',
    'sim_hamming',
    'MLIPNS',
    'dist_mlipns',
    'sim_mlipns',
    'Tichy',
    'BlockLevenshtein',
    'CormodeLZ',
    'JaroWinkler',
    'dist_jaro_winkler',
    'sim_jaro_winkler',
    'Strcmp95',
    'dist_strcmp95',
    'sim_strcmp95',
    'IterativeSubString',
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
    'AZZOO',
    'Anderberg',
    'AndresMarzoDelta',
    'BaroniUrbaniBuserI',
    'BaroniUrbaniBuserII',
    'BatageljBren',
    'BaulieuI',
    'BaulieuII',
    'BaulieuIII',
    'Benini',
    'BennetSigma',
    'BraunBlanquet',
    'Canberra',
    'Chord',
    'Clement',
    'Cole',
    'ConsonniTodeschiniI',
    'ConsonniTodeschiniII',
    'ConsonniTodeschiniIII',
    'ConsonniTodeschiniIV',
    'ConsonniTodeschiniV',
    'CohenKappa',
    'Dennis',
    'DiceAsymmetricI',
    'DiceAsymmetricII',
    'Digby',
    'Dispersion',
    'Doolittle',
    'Dunning',
    'Eyraud',
    'Fager',
    'FagerMcGowan',
    'Faith',
    'Fidelity',
    'Fleiss',
    'FleissLevinPaik',
    'ForbesI',
    'ForbesII',
    'Fossum',
    'GeneralizedFleiss',
    'Gilbert',
    'GilbertWells',
    'Gini',
    'Goodall',
    'GoodmanKruskalLambdaR',
    'GoodmanKruskalLambda',
    'GoodmanKruskalTauA',
    'GoodmanKruskalTauB',
    'GowerLegendre',
    'GuttmanLambdaA',
    'GuttmanLambdaB',
    'GwetGamma',
    'Hamann',
    'HarrisLahey',
    'Hassanat',
    'HawkinsDotson',
    'Hellinger',
    'Hurlbert',
    'JaccardNM',
    'Johnson',
    'KentFosterI',
    'KentFosterII',
    'KendallTau',
    'KentFosterI',
    'KentFosterII',
    'KoppenI',
    'KoppenII',
    'KuderRichardson',
    'KuhnsI',
    'KuhnsII',
    'KuhnsIII',
    'KuhnsIV',
    'KuhnsIX',
    'KuhnsV',
    'KuhnsVI',
    'KuhnsVII',
    'KuhnsVIII',
    'KuhnsX',
    'KuhnsXI',
    'KuhnsXII',
    'KulczynskiI',
    'KulczynskiII',
    'Lorentzian',
    'Maarel',
    'MASI',
    'Matusita',
    'MaxwellPilliner',
    'McConnaughey',
    'McEwenMichael',
    'Mountford',
    'MutualInformation',
    'MSContingency',
    'Pattern',
    'PearsonHeronII',
    'PearsonII',
    'PearsonIII',
    'PearsonChiSquared',
    'PearsonPhi',
    'Peirce',
    'QGram',
    'ReesLevenshtein',
    'RogersTanimoto',
    'RogotGoldberg',
    'ScottPi',
    'Shape',
    'Size',
    'SokalMichener',
    'SokalSneathI',
    'SokalSneathII',
    'SokalSneathIII',
    'SokalSneathIV',
    'SokalSneathV',
    'Sorgenfrei',
    'Steffensen',
    'Stiles',
    'StuartTau',
    'Tarantula',
    'Tarwid',
    'Tetrachoric',
    'TullossR',
    'TullossS',
    'TullossT',
    'TullossU',
    'UnknownA',
    'UnknownB',
    'UnknownC',
    'UnknownD',
    'UnknownE',
    'UnknownF',
    'UnknownG',
    'UnknownH',
    'UnknownI',
    'UnknownJ',
    'UnknownK',
    'UnknownL',
    'UnknownM',
    'UnknownN',
    'UnknownO',
    'Upholt',
    'WarrensI',
    'WarrensII',
    'WarrensIII',
    'WarrensIV',
    'WarrensV',
    'WeightedJaccard',
    'Whittaker',
    'YatesChiSquared',
    'YuleQ',
    'YuleQII',
    'YuleY',
    'YJHHR',
    'Bhattacharyya',
    'BrainerdRobinson',
    'QuantitativeCosine',
    'QuantitativeDice',
    'QuantitativeJaccard',
    'Roberts',
    'AverageLinkage',
    'SingleLinkage',
    'CompleteLinkage',
    'Bag',
    'bag',
    'dist_bag',
    'sim_bag',
    'SoftCosine',
    'MongeElkan',
    'dist_monge_elkan',
    'sim_monge_elkan',
    'TFIDF',
    'SoftTFIDF',
    'JensenShannon',
    'FellegiSunter',
    'MinHash',
    'BLEU',
    'RougeL',
    'RougeW',
    'RougeS',
    'RougeSU',
    'PositionalQGramDice',
    'PositionalQGramJaccard',
    'PositionalQGramOverlap',
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
    'NCDpaq9a',
    'NCDlzss',
    'FuzzyWuzzyPartialString',
    'FuzzyWuzzyTokenSort',
    'FuzzyWuzzyTokenSet',
    'MRA',
    'mra_compare',
    'dist_mra',
    'sim_mra',
    'Editex',
    'editex',
    'dist_editex',
    'sim_editex',
    'Baystat',
    'dist_baystat',
    'sim_baystat',
    'Eudex',
    'eudex_hamming',
    'dist_eudex',
    'sim_eudex',
    'Sift4',
    'Sift4Simplest',
    'Sift4Extended',
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
