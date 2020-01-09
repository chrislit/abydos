# Copyright 2014-2020 by Christopher C. Little.
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
    - Discounted Levenshtein distance (:py:class:`.DiscountedLevenshtein`)
    - Phonetic edit distance (:py:class:`.PhoneticEditDistance`)

Hamming distance (:py:class:`.Hamming`), Relaxed Hamming distance
(:py:class:`.RelaxedHamming`), and the closely related Modified
Language-Independent Product Name Search distance (:py:class:`.MLIPNS`) are
provided.

Block edit distances:

    - Tichy edit distance (:py:class:`.Tichy`)
    - Levenshtein distance with block operations
      (:py:class:`.BlockLevenshtein`)
    - Rees-Levenshtein distance (:py:class:`.ReesLevenshtein`)
    - Cormode's LZ distance (:py:class:`.CormodeLZ`)
    - Shapira-Storer I edit distance with block moves, greedy algorithm
      (:py:class:`.ShapiraStorerI`)

Distance metrics developed for the US Census or derived from them are included:

    - Jaro distance (:py:class:`.JaroWinkler` with ``mode='Jaro'``)
    - Jaro-Winkler distance (:py:class:`.JaroWinkler`)
    - Strcmp95 distance (:py:class:`.Strcmp95`)
    - Iterative-SubString (I-Sub) correlation
      (:py:class:`.IterativeSubString`)

A large set of multi-set token-based distance metrics are provided, including:

    - AMPLE similarity (:py:class:`.AMPLE`)
    - AZZOO similarity (:py:class:`.AZZOO`)
    - Anderberg's D similarity (:py:class:`.Anderberg`)
    - Andres & Marzo's Delta correlation (:py:class:`.AndresMarzoDelta`)
    - Baroni-Urbani & Buser I similarity (:py:class:`.BaroniUrbaniBuserI`)
    - Baroni-Urbani & Buser II correlation (:py:class:`.BaroniUrbaniBuserII`)
    - Batagelj & Bren similarity (:py:class:`.BatageljBren`)
    - Baulieu I distance (:py:class:`.BaulieuI`)
    - Baulieu II distance (:py:class:`.BaulieuII`)
    - Baulieu III distance (:py:class:`.BaulieuIII`)
    - Baulieu IV distance (:py:class:`.BaulieuIV`)
    - Baulieu V distance (:py:class:`.BaulieuV`)
    - Baulieu VI distance (:py:class:`.BaulieuVI`)
    - Baulieu VII distance (:py:class:`.BaulieuVII`)
    - Baulieu VIII distance (:py:class:`.BaulieuVIII`)
    - Baulieu IX distance (:py:class:`.BaulieuIX`)
    - Baulieu X distance (:py:class:`.BaulieuX`)
    - Baulieu XI distance (:py:class:`.BaulieuXI`)
    - Baulieu XII distance (:py:class:`.BaulieuXII`)
    - Baulieu XIII distance (:py:class:`.BaulieuXIII`)
    - Baulieu XIV distance (:py:class:`.BaulieuXIV`)
    - Baulieu XV distance (:py:class:`.BaulieuXV`)
    - Benini I correlation (:py:class:`.BeniniI`)
    - Benini II correlation (:py:class:`.BeniniII`)
    - Bennet's S correlation (:py:class:`.Bennet`)
    - Braun-Blanquet similarity (:py:class:`.BraunBlanquet`)
    - Canberra distance (:py:class:`.Canberra`)
    - Cao similarity (:py:class:`.Cao`)
    - Chao's Dice similarity (:py:class:`.ChaoDice`)
    - Chao's Jaccard similarity (:py:class:`.ChaoJaccard`)
    - Chebyshev distance (:py:class:`.Chebyshev`)
    - Chord distance (:py:class:`.Chord`)
    - Clark distance (:py:class:`.Clark`)
    - Clement similarity (:py:class:`.Clement`)
    - Cohen's Kappa similarity (:py:class:`.CohenKappa`)
    - Cole correlation (:py:class:`.Cole`)
    - Consonni & Todeschini I similarity (:py:class:`.ConsonniTodeschiniI`)
    - Consonni & Todeschini II similarity (:py:class:`.ConsonniTodeschiniII`)
    - Consonni & Todeschini III similarity (:py:class:`.ConsonniTodeschiniIII`)
    - Consonni & Todeschini IV similarity (:py:class:`.ConsonniTodeschiniIV`)
    - Consonni & Todeschini V correlation (:py:class:`.ConsonniTodeschiniV`)
    - Cosine similarity (:py:class:`.Cosine`)
    - Dennis similarity (:py:class:`.Dennis`)
    - Dice's Asymmetric I similarity (:py:class:`.DiceAsymmetricI`)
    - Dice's Asymmetric II similarity (:py:class:`.DiceAsymmetricII`)
    - Digby correlation (:py:class:`.Digby`)
    - Dispersion correlation (:py:class:`.Dispersion`)
    - Doolittle similarity (:py:class:`.Doolittle`)
    - Dunning similarity (:py:class:`.Dunning`)
    - Euclidean distance (:py:class:`.Euclidean`)
    - Eyraud similarity (:py:class:`.Eyraud`)
    - Fager & McGowan similarity (:py:class:`.FagerMcGowan`)
    - Faith similarity (:py:class:`.Faith`)
    - Fidelity similarity (:py:class:`.Fidelity`)
    - Fleiss correlation (:py:class:`.Fleiss`)
    - Fleiss-Levin-Paik similarity (:py:class:`.FleissLevinPaik`)
    - Forbes I similarity (:py:class:`.ForbesI`)
    - Forbes II correlation (:py:class:`.ForbesII`)
    - Fossum similarity (:py:class:`.Fossum`)
    - Generalized Fleiss correlation (:py:class:`.GeneralizedFleiss`)
    - Gilbert correlation (:py:class:`.Gilbert`)
    - Gilbert & Wells similarity (:py:class:`.GilbertWells`)
    - Gini I correlation (:py:class:`.GiniI`)
    - Gini II correlation (:py:class:`.GiniII`)
    - Goodall similarity (:py:class:`.Goodall`)
    - Goodman & Kruskal's Lambda similarity (:py:class:`.GoodmanKruskalLambda`)
    - Goodman & Kruskal's Lambda-r correlation
      (:py:class:`.GoodmanKruskalLambdaR`)
    - Goodman & Kruskal's Tau A similarity (:py:class:`.GoodmanKruskalTauA`)
    - Goodman & Kruskal's Tau B similarity (:py:class:`.GoodmanKruskalTauB`)
    - Gower & Legendre similarity (:py:class:`.GowerLegendre`)
    - Guttman Lambda A similarity (:py:class:`.GuttmanLambdaA`)
    - Guttman Lambda B similarity (:py:class:`.GuttmanLambdaB`)
    - Gwet's AC correlation (:py:class:`.GwetAC`)
    - Hamann correlation (:py:class:`.Hamann`)
    - Harris & Lahey similarity (:py:class:`.HarrisLahey`)
    - Hassanat distance (:py:class:`.Hassanat`)
    - Hawkins & Dotson similarity (:py:class:`.HawkinsDotson`)
    - Hellinger distance (:py:class:`.Hellinger`)
    - Henderson-Heron similarity (:py:class:`.HendersonHeron`)
    - Horn-Morisita similarity (:py:class:`.HornMorisita`)
    - Hurlbert correlation (:py:class:`.Hurlbert`)
    - Jaccard similarity (:py:class:`.Jaccard`) &
      Tanimoto coefficient (:py:meth:`.Jaccard.tanimoto_coeff`)
    - Jaccard-NM similarity (:py:class:`.JaccardNM`)
    - Johnson similarity (:py:class:`.Johnson`)
    - Kendall's Tau correlation (:py:class:`.KendallTau`)
    - Kent & Foster I similarity (:py:class:`.KentFosterI`)
    - Kent & Foster II similarity (:py:class:`.KentFosterII`)
    - Köppen I correlation (:py:class:`.KoppenI`)
    - Köppen II similarity (:py:class:`.KoppenII`)
    - Kuder & Richardson correlation (:py:class:`.KuderRichardson`)
    - Kuhns I correlation (:py:class:`.KuhnsI`)
    - Kuhns II correlation (:py:class:`.KuhnsII`)
    - Kuhns III correlation (:py:class:`.KuhnsIII`)
    - Kuhns IV correlation (:py:class:`.KuhnsIV`)
    - Kuhns V correlation (:py:class:`.KuhnsV`)
    - Kuhns VI correlation (:py:class:`.KuhnsVI`)
    - Kuhns VII correlation (:py:class:`.KuhnsVII`)
    - Kuhns VIII correlation (:py:class:`.KuhnsVIII`)
    - Kuhns IX correlation (:py:class:`.KuhnsIX`)
    - Kuhns X correlation (:py:class:`.KuhnsX`)
    - Kuhns XI correlation (:py:class:`.KuhnsXI`)
    - Kuhns XII similarity (:py:class:`.KuhnsXII`)
    - Kulczynski I similarity (:py:class:`.KulczynskiI`)
    - Kulczynski II similarity (:py:class:`.KulczynskiII`)
    - Lorentzian distance (:py:class:`.Lorentzian`)
    - Maarel correlation (:py:class:`.Maarel`)
    - Manhattan distance (:py:class:`.Manhattan`)
    - Morisita similarity (:py:class:`.Morisita`)
    - marking distance (:py:class:`.Marking`)
    - marking metric (:py:class:`.MarkingMetric`)
    - MASI similarity (:py:class:`.MASI`)
    - Matusita distance (:py:class:`.Matusita`)
    - Maxwell & Pilliner correlation (:py:class:`.MaxwellPilliner`)
    - McConnaughey correlation (:py:class:`.McConnaughey`)
    - McEwen & Michael correlation (:py:class:`.McEwenMichael`)
    - mean squared contingency correlation (:py:class:`.MSContingency`)
    - Michael similarity (:py:class:`.Michael`)
    - Michelet similarity (:py:class:`.Michelet`)
    - Millar distance (:py:class:`.Millar`)
    - Minkowski distance (:py:class:`.Minkowski`)
    - Mountford similarity (:py:class:`.Mountford`)
    - Mutual Information similarity (:py:class:`.MutualInformation`)
    - Overlap distance (:py:class:`.Overlap`)
    - Pattern difference (:py:class:`.Pattern`)
    - Pearson & Heron II correlation (:py:class:`.PearsonHeronII`)
    - Pearson II similarity (:py:class:`.PearsonII`)
    - Pearson III correlation (:py:class:`.PearsonIII`)
    - Pearson's Chi-Squared similarity (:py:class:`.PearsonChiSquared`)
    - Pearson's Phi correlation (:py:class:`.PearsonPhi`)
    - Peirce correlation (:py:class:`.Peirce`)
    - q-gram distance (:py:class:`.QGram`)
    - Raup-Crick similarity (:py:class:`.RaupCrick`)
    - Rogers & Tanimoto similarity (:py:class:`.RogersTanimoto`)
    - Rogot & Goldberg similarity (:py:class:`.RogotGoldberg`)
    - Russell & Rao similarity (:py:class:`.RussellRao`)
    - Scott's Pi correlation (:py:class:`.ScottPi`)
    - Shape difference (:py:class:`.Shape`)
    - Size difference (:py:class:`.Size`)
    - Sokal & Michener similarity (:py:class:`.SokalMichener`)
    - Sokal & Sneath I similarity (:py:class:`.SokalSneathI`)
    - Sokal & Sneath II similarity (:py:class:`.SokalSneathII`)
    - Sokal & Sneath III similarity (:py:class:`.SokalSneathIII`)
    - Sokal & Sneath IV similarity (:py:class:`.SokalSneathIV`)
    - Sokal & Sneath V similarity (:py:class:`.SokalSneathV`)
    - Sørensen–Dice coefficient (:py:class:`.Dice`)
    - Sorgenfrei similarity (:py:class:`.Sorgenfrei`)
    - Steffensen similarity (:py:class:`.Steffensen`)
    - Stiles similarity (:py:class:`.Stiles`)
    - Stuart's Tau correlation (:py:class:`.StuartTau`)
    - Tarantula similarity (:py:class:`.Tarantula`)
    - Tarwid correlation (:py:class:`.Tarwid`)
    - Tetrachoric correlation coefficient (:py:class:`.Tetrachronic`)
    - Tulloss' R similarity (:py:class:`.TullossR`)
    - Tulloss' S similarity (:py:class:`.TullossS`)
    - Tulloss' T similarity (:py:class:`.TullossT`)
    - Tulloss' U similarity (:py:class:`.TullossU`)
    - Tversky distance (:py:class:`.Tversky`)
    - Weighted Jaccard similarity (:py:class:`.WeightedJaccard`)
    - Unigram subtuple similarity (:py:class:`.UnigramSubtuple`)
    - Unknown A correlation (:py:class:`.UnknownA`)
    - Unknown B similarity (:py:class:`.UnknownB`)
    - Unknown C similarity (:py:class:`.UnknownC`)
    - Unknown D similarity (:py:class:`.UnknownD`)
    - Unknown E correlation (:py:class:`.UnknownE`)
    - Unknown F similarity (:py:class:`.UnknownF`)
    - Unknown G similarity (:py:class:`.UnknownG`)
    - Unknown H similarity (:py:class:`.UnknownH`)
    - Unknown I similarity (:py:class:`.UnknownI`)
    - Unknown J similarity (:py:class:`.UnknownJ`)
    - Unknown K distance (:py:class:`.UnknownK`)
    - Unknown L similarity (:py:class:`.UnknownL`)
    - Unknown M similarity (:py:class:`.UnknownM`)
    - Upholt similarity (:py:class:`.Upholt`)
    - Warrens I correlation (:py:class:`.WarrensI`)
    - Warrens II similarity (:py:class:`.WarrensII`)
    - Warrens III correlation (:py:class:`.WarrensIII`)
    - Warrens IV similarity (:py:class:`.WarrensIV`)
    - Warrens V similarity (:py:class:`.WarrensV`)
    - Whittaker distance (:py:class:`.Whittaker`)
    - Yates' Chi-Squared similarity (:py:class:`.YatesChiSquared`)
    - Yule's Q correlation (:py:class:`.YuleQ`)
    - Yule's Q II distance (:py:class:`.YuleQII`)
    - Yule's Y correlation (:py:class:`.YuleY`)
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
    - Jensen-Shannon divergence (:py:class:`.JensenShannon`)
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

A convenience class, allowing one to pass a list of string transforms (phonetic
algorithms, string transforms, and/or stemmers) and, optionally, a string
distance measure to compute the similarity/distance of two strings that have
undergone each transform, is provided in:

    - Phonetic distance (:py:class:`.PhoneticDistance`)

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
    - Indice de Similitude-Guth (:py:class:`.ISG`)
    - INClusion Programme (:py:class:`.Inclusion`)
    - Guth (:py:class:`.Guth`)
    - Victorian Panel Study (:py:class:`.VPS`)
    - LIG3 (:py:class:`.LIG3`)
    - String subsequence kernel (SSK) (:py:class:`.SSK`)

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
from ._baulieu_iv import BaulieuIV
from ._baulieu_ix import BaulieuIX
from ._baulieu_v import BaulieuV
from ._baulieu_vi import BaulieuVI
from ._baulieu_vii import BaulieuVII
from ._baulieu_viii import BaulieuVIII
from ._baulieu_x import BaulieuX
from ._baulieu_xi import BaulieuXI
from ._baulieu_xii import BaulieuXII
from ._baulieu_xiii import BaulieuXIII
from ._baulieu_xiv import BaulieuXIV
from ._baulieu_xv import BaulieuXV
from ._baystat import Baystat, dist_baystat, sim_baystat
from ._benini_i import BeniniI
from ._benini_ii import BeniniII
from ._bennet import Bennet
from ._bhattacharyya import Bhattacharyya
from ._bisim import BISIM
from ._bleu import BLEU
from ._block_levenshtein import BlockLevenshtein
from ._brainerd_robinson import BrainerdRobinson
from ._braun_blanquet import BraunBlanquet
from ._canberra import Canberra
from ._cao import Cao
from ._chao_dice import ChaoDice
from ._chao_jaccard import ChaoJaccard
from ._chebyshev import Chebyshev, chebyshev
from ._chord import Chord
from ._clark import Clark
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
from ._discounted_levenshtein import DiscountedLevenshtein
from ._dispersion import Dispersion
from ._distance import _Distance
from ._doolittle import Doolittle
from ._dunning import Dunning
from ._editex import Editex, dist_editex, editex, sim_editex
from ._euclidean import Euclidean, dist_euclidean, euclidean, sim_euclidean
from ._eudex import Eudex, dist_eudex, eudex_hamming, sim_eudex
from ._eyraud import Eyraud
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
from ._gini_i import GiniI
from ._gini_ii import GiniII
from ._goodall import Goodall
from ._goodman_kruskal_lambda import GoodmanKruskalLambda
from ._goodman_kruskal_lambda_r import GoodmanKruskalLambdaR
from ._goodman_kruskal_tau_a import GoodmanKruskalTauA
from ._goodman_kruskal_tau_b import GoodmanKruskalTauB
from ._gotoh import Gotoh, gotoh
from ._gower_legendre import GowerLegendre
from ._guth import Guth
from ._guttman_lambda_a import GuttmanLambdaA
from ._guttman_lambda_b import GuttmanLambdaB
from ._gwet_ac import GwetAC
from ._hamann import Hamann
from ._hamming import Hamming, dist_hamming, hamming, sim_hamming
from ._harris_lahey import HarrisLahey
from ._hassanat import Hassanat
from ._hawkins_dotson import HawkinsDotson
from ._hellinger import Hellinger
from ._henderson_heron import HendersonHeron
from ._higuera_mico import HigueraMico
from ._horn_morisita import HornMorisita
from ._hurlbert import Hurlbert
from ._ident import Ident, dist_ident, sim_ident
from ._inclusion import Inclusion
from ._indel import Indel, dist_indel, indel, sim_indel
from ._isg import ISG
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
from ._lig3 import LIG3
from ._lorentzian import Lorentzian
from ._maarel import Maarel
from ._manhattan import Manhattan, dist_manhattan, manhattan, sim_manhattan
from ._marking import Marking
from ._marking_metric import MarkingMetric
from ._masi import MASI
from ._matusita import Matusita
from ._maxwell_pilliner import MaxwellPilliner
from ._mcconnaughey import McConnaughey
from ._mcewen_michael import McEwenMichael
from ._meta_levenshtein import MetaLevenshtein
from ._michelet import Michelet
from ._millar import Millar
from ._minhash import MinHash
from ._minkowski import Minkowski, dist_minkowski, minkowski, sim_minkowski
from ._mlipns import MLIPNS, dist_mlipns, sim_mlipns
from ._monge_elkan import MongeElkan, dist_monge_elkan, sim_monge_elkan
from ._morisita import Morisita
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
from ._phonetic_distance import PhoneticDistance
from ._phonetic_edit_distance import PhoneticEditDistance
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
from ._raup_crick import RaupCrick
from ._rees_levenshtein import ReesLevenshtein
from ._relaxed_hamming import RelaxedHamming
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
from ._shapira_storer_i import ShapiraStorerI
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
from ._ssk import SSK
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
from ._unigram_subtuple import UnigramSubtuple
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
from ._upholt import Upholt
from ._vps import VPS
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
    'ShapiraStorerI',
    'Marking',
    'MarkingMetric',
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
    'DiscountedLevenshtein',
    'PhoneticEditDistance',
    'Hamming',
    'hamming',
    'dist_hamming',
    'sim_hamming',
    'MLIPNS',
    'dist_mlipns',
    'sim_mlipns',
    'RelaxedHamming',
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
    'BaulieuIV',
    'BaulieuV',
    'BaulieuVI',
    'BaulieuVII',
    'BaulieuVIII',
    'BaulieuIX',
    'BaulieuX',
    'BaulieuXI',
    'BaulieuXII',
    'BaulieuXIII',
    'BaulieuXIV',
    'BaulieuXV',
    'BeniniI',
    'BeniniII',
    'Bennet',
    'BraunBlanquet',
    'Canberra',
    'Cao',
    'ChaoDice',
    'ChaoJaccard',
    'Chebyshev',
    'chebyshev',
    'Chord',
    'Clark',
    'Clement',
    'CohenKappa',
    'Cole',
    'ConsonniTodeschiniI',
    'ConsonniTodeschiniII',
    'ConsonniTodeschiniIII',
    'ConsonniTodeschiniIV',
    'ConsonniTodeschiniV',
    'Cosine',
    'dist_cosine',
    'sim_cosine',
    'Dennis',
    'Dice',
    'dist_dice',
    'sim_dice',
    'DiceAsymmetricI',
    'DiceAsymmetricII',
    'Digby',
    'Dispersion',
    'Doolittle',
    'Dunning',
    'Euclidean',
    'euclidean',
    'dist_euclidean',
    'sim_euclidean',
    'Eyraud',
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
    'GiniI',
    'GiniII',
    'Goodall',
    'GoodmanKruskalLambda',
    'GoodmanKruskalLambdaR',
    'GoodmanKruskalTauA',
    'GoodmanKruskalTauB',
    'GowerLegendre',
    'GuttmanLambdaA',
    'GuttmanLambdaB',
    'GwetAC',
    'Hamann',
    'HarrisLahey',
    'Hassanat',
    'HawkinsDotson',
    'Hellinger',
    'HendersonHeron',
    'HornMorisita',
    'Hurlbert',
    'Jaccard',
    'dist_jaccard',
    'sim_jaccard',
    'tanimoto',
    'JaccardNM',
    'Johnson',
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
    'KuhnsV',
    'KuhnsVI',
    'KuhnsVII',
    'KuhnsVIII',
    'KuhnsIX',
    'KuhnsX',
    'KuhnsXI',
    'KuhnsXII',
    'KulczynskiI',
    'KulczynskiII',
    'Lorentzian',
    'Maarel',
    'Morisita',
    'Manhattan',
    'manhattan',
    'dist_manhattan',
    'sim_manhattan',
    'Michelet',
    'Millar',
    'Minkowski',
    'minkowski',
    'dist_minkowski',
    'sim_minkowski',
    'MASI',
    'Matusita',
    'MaxwellPilliner',
    'McConnaughey',
    'McEwenMichael',
    'Mountford',
    'MutualInformation',
    'MSContingency',
    'Overlap',
    'dist_overlap',
    'sim_overlap',
    'Pattern',
    'PearsonHeronII',
    'PearsonII',
    'PearsonIII',
    'PearsonChiSquared',
    'PearsonPhi',
    'Peirce',
    'QGram',
    'RaupCrick',
    'ReesLevenshtein',
    'RogersTanimoto',
    'RogotGoldberg',
    'RussellRao',
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
    'Tversky',
    'dist_tversky',
    'sim_tversky',
    'UnigramSubtuple',
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
    'PhoneticDistance',
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
    'ISG',
    'Inclusion',
    'Guth',
    'VPS',
    'LIG3',
    'SSK',
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
