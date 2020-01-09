# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.distance._token_distance.

The distance._token_distance._TokenDistance module implements abstract class
_TokenDistance.
"""

from collections import Counter, OrderedDict
from itertools import product
from math import exp, log1p

import numpy as np
from numpy import zeros as np_zeros

from ._damerau_levenshtein import DamerauLevenshtein
from ._distance import _Distance
from ._lcprefix import LCPrefix
from ._levenshtein import Levenshtein
from ..stats import ConfusionTable
from ..tokenizer import QGrams, QSkipgrams, WhitespaceTokenizer

__all__ = ['_TokenDistance']


class _TokenDistance(_Distance):
    r"""Abstract Token Distance class.

    .. _confusion_table:

    +----------------+--------------+-----------------+-------+
    |                | |in| ``tar`` | |notin| ``tar`` |       |
    +----------------+--------------+-----------------+-------+
    | |in| ``src``   | |a|          | |b|             | |a+b| |
    +----------------+--------------+-----------------+-------+
    | |notin| ``src``| |c|          | |d|             | |c+d| |
    +----------------+--------------+-----------------+-------+
    |                | |a+c|        | |b+d|           | |n|   |
    +----------------+--------------+-----------------+-------+

    .. |in| replace:: :math:`x \in`
    .. |notin| replace:: :math:`x \notin`

    .. |a| replace:: :math:`a = |X \cap Y|`
    .. |b| replace:: :math:`b = |X\setminus Y|`
    .. |c| replace:: :math:`c = |Y \setminus X|`
    .. |d| replace:: :math:`d = |(N\setminus X)\setminus Y|`
    .. |n| replace:: :math:`n = |N|`
    .. |a+b| replace:: :math:`p_1 = a+b = |X|`
    .. |a+c| replace:: :math:`p_2 = a+c = |Y|`
    .. |c+d| replace:: :math:`q_1 = c+d = |N\setminus X|`
    .. |b+d| replace:: :math:`q_2 = b+d = |N\setminus Y|`

    .. versionadded:: 0.3.6
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        r"""Initialize _TokenDistance instance.

        .. _intersection_type:

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:

                - 'crisp': Ordinary intersection, wherein items are entirely
                  members or non-members of the intersection. (Default)
                - ``fuzzy``: Fuzzy intersection, defined by :cite:`Wang:2014`,
                  wherein items can be partially members of the intersection
                  if their similarity meets or exceeds a threshold value. This
                  also takes `metric` (by default :class:`Levenshtein()`) and
                  `threshold` (by default 0.8) parameters.
                - ``soft``: Soft intersection, defined by :cite:`Russ:2014`,
                  wherein items can be partially members of the intersection
                  depending on their similarity. This also takes a `metric`
                  (by default :class:`DamerauLevenshtein()`) parameter.
                - ``linkage``: Group linkage, defined by :cite:`On:2007`. Like
                  the soft intersection, items can be partially members of the
                  intersection, but the method of pairing similar members is
                  somewhat more complex. See the cited paper for details. This
                  also takes `metric`
                  (by default :class:`DamerauLevenshtein()`) and `threshold`
                  (by default 0.1) parameters.
        **kwargs
            Arbitrary keyword arguments


        .. _alphabet:

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.
        metric : _Distance
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the ``fuzzy`` variant.
        alphabet : Counter, collection, int, or None
            This represents the alphabet of possible tokens.

                - If a Counter is supplied, it is used directly in computing
                  the complement of the tokens in both sets.
                - If a collection is supplied, it is converted to a Counter
                  and used directly. In the case of a single string being
                  supplied and the QGram tokenizer being used, the full
                  alphabet is inferred (i.e.
                  :math:`len(set(alphabet+QGrams.start\_stop))^{QGrams.qval}`
                  is used as the cardinality of the full alphabet.
                - If an int is supplied, it is used as the cardinality of the
                  full alphabet.
                - If None is supplied, the cardinality of the full alphabet
                  is inferred if QGram of QSkipgrams tokenization is used (i.e.
                  :math:`28^{QGrams.qval}` is used as the cardinality of the
                  full alphabet or :math:`26` if QGrams.qval is 1, which
                  assumes the strings are English language strings and only
                  contain letters of a single case). Otherwise, the cardinality
                  of the complement of the total will be 0.
        normalizer : str
            This represents the normalization applied to the values in the
            2x2 contingency table prior to any of the cardinality (\*_card)
            methods returning a value. By default, no normalization is applied,
            but the following values are supported:

                - ``proportional`` : :math:`\frac{x}{n}`, where n is the total
                  population
                - ``log`` : :math:`log(1+x)`
                - ``exp`` : :math:`e^x`
                - ``laplace`` : :math:`x+1`
                - ``inverse`` : :math:`\frac{1}{x}`
                - ``complement`` : :math:`n-x`, where n is the total population

        .. versionadded:: 0.4.0

        """
        super(_TokenDistance, self).__init__(
            intersection_type=intersection_type, **kwargs
        )

        qval = 2 if 'qval' not in self.params else self.params['qval']
        self.params['tokenizer'] = (
            tokenizer
            if tokenizer is not None
            else WhitespaceTokenizer()
            if qval == 0
            else QGrams(qval=qval, start_stop='$#', skip=0, scaler=None)
        )

        if hasattr(self.params['tokenizer'], 'qval'):
            if isinstance(self.params['tokenizer'].qval, int):
                qvals = [self.params['tokenizer'].qval]
            else:
                qvals = list(self.params['tokenizer'].qval)
        else:
            qvals = []

        if 'alphabet' in self.params:
            if isinstance(self.params['alphabet'], str):
                self.params['alphabet'] = set(self.params['alphabet'])
                if isinstance(self.params['tokenizer'], (QGrams, QSkipgrams)):
                    self.params['alphabet'] |= set(
                        self.params['tokenizer'].start_stop
                    )
                    self.params['alphabet'] = sum(
                        len(self.params['alphabet']) ** qval for qval in qvals
                    )
            if hasattr(self.params['alphabet'], '__len__') and not isinstance(
                self.params['alphabet'], Counter
            ):
                self.params['alphabet'] = len(self.params['alphabet'])
            elif self.params['alphabet'] is None and isinstance(
                self.params['tokenizer'], (QGrams, QSkipgrams)
            ):
                self.params['alphabet'] = sum(
                    28 ** qval if qval > 1 else 26 for qval in qvals
                )
        else:
            if isinstance(self.params['tokenizer'], (QGrams, QSkipgrams)):
                self.params['alphabet'] = sum(
                    28 ** qval if qval > 1 else 26 for qval in qvals
                )
            else:
                self.params['alphabet'] = None

        if intersection_type == 'soft':
            if 'metric' not in self.params or self.params['metric'] is None:
                self.params['metric'] = Levenshtein()
            self._lcprefix = LCPrefix()
            self._intersection = self._soft_intersection
        elif intersection_type == 'fuzzy':
            if 'metric' not in self.params or self.params['metric'] is None:
                self.params['metric'] = Levenshtein()
            if 'threshold' not in self.params:
                self.params['threshold'] = 0.8
            self._intersection = self._fuzzy_intersection
        elif intersection_type == 'linkage':
            if 'metric' not in self.params or self.params['metric'] is None:
                self.params['metric'] = DamerauLevenshtein()
            if 'threshold' not in self.params:
                self.params['threshold'] = 0.1
            self._intersection = self._group_linkage_intersection
        else:
            self._intersection = self._crisp_intersection

        self._src_tokens = Counter()
        self._tar_tokens = Counter()
        self._population_card_value = 0

        # initialize normalizer
        self.normalizer = self._norm_none

        self._norm_dict = {
            'proportional': self._norm_proportional,
            'log': self._norm_log,
            'exp': self._norm_exp,
            'laplace': self._norm_laplace,
            'inverse': self._norm_inverse,
            'complement': self._norm_complement,
        }

        # initialize values for soft intersection
        self._soft_intersection_precalc = None
        self._soft_src_only = None
        self._soft_tar_only = None

    def _norm_none(self, x, _squares, _pop):
        return x

    def _norm_proportional(self, x, _squares, pop):
        return x / max(1, pop)

    def _norm_log(self, x, _squares, _pop):
        return log1p(x)

    def _norm_exp(self, x, _squares, _pop):
        return exp(x)

    def _norm_laplace(self, x, squares, _pop):
        return x + squares

    def _norm_inverse(self, x, _squares, pop):
        return 1 / x if x else pop

    def _norm_complement(self, x, _squares, pop):
        return pop - x

    def _tokenize(self, src, tar):
        """Return the Q-Grams in src & tar.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        tuple of Counters
            Q-Grams

        Examples
        --------
        >>> pe = _TokenDistance()
        >>> pe._tokenize('AT', 'TT')._get_tokens()
        (Counter({'$A': 1, 'AT': 1, 'T#': 1}),
         Counter({'$T': 1, 'TT': 1, 'T#': 1}))


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        self._src_orig = src
        self._tar_orig = tar

        if isinstance(src, Counter):
            self._src_tokens = src
        else:
            self._src_tokens = (
                self.params['tokenizer'].tokenize(src).get_counter()
            )
        if isinstance(tar, Counter):
            self._tar_tokens = tar
        else:
            self._tar_tokens = (
                self.params['tokenizer'].tokenize(tar).get_counter()
            )

        self._population_card_value = self._calc_population_card()

        # Set up the normalizer, a function of two variables:
        # x is the value in the contingency table square(s)
        # n is the number of squares that x represents
        if (
            'normalizer' in self.params
            and self.params['normalizer'] in self._norm_dict
        ):
            self.normalizer = self._norm_dict[self.params['normalizer']]

        # clear values for soft intersection
        self._soft_intersection_precalc = None
        self._soft_src_only = None
        self._soft_tar_only = None

        return self

    def _get_tokens(self):
        """Return the src and tar tokens as a tuple."""
        return self._src_tokens, self._tar_tokens

    def _src_card(self):
        r"""Return the cardinality of the tokens in the source set."""
        if self.params['intersection_type'] == 'soft':
            if not self._soft_intersection_precalc:
                self._intersection()
            return self.normalizer(
                sum(
                    abs(val)
                    for val in (
                        self._soft_intersection_precalc + self._soft_src_only
                    ).values()
                ),
                2,
                self._population_card_value,
            )
        return self.normalizer(
            sum(abs(val) for val in self._src_tokens.values()),
            2,
            self._population_card_value,
        )

    def _src_only(self):
        r"""Return the src tokens minus the tar tokens.

        For (multi-)sets S and T, this is :math:`S \setminus T`.
        """
        if self.params['intersection_type'] == 'soft':
            if not self._soft_intersection_precalc:
                self._intersection()
            return self._soft_src_only
        src_only = self._src_tokens - self._intersection()
        if self.params['intersection_type'] != 'crisp':
            src_only -= self._intersection() - self._crisp_intersection()
        return src_only

    def _src_only_card(self):
        """Return the cardinality of the tokens only in the source set."""
        return self.normalizer(
            sum(abs(val) for val in self._src_only().values()),
            1,
            self._population_card_value,
        )

    def _tar_card(self):
        r"""Return the cardinality of the tokens in the target set."""
        if self.params['intersection_type'] == 'soft':
            if not self._soft_intersection_precalc:
                self._intersection()
            return self.normalizer(
                sum(
                    abs(val)
                    for val in (
                        self._soft_intersection_precalc + self._soft_tar_only
                    ).values()
                ),
                2,
                self._population_card_value,
            )
        return self.normalizer(
            sum(abs(val) for val in self._tar_tokens.values()),
            2,
            self._population_card_value,
        )

    def _tar_only(self):
        r"""Return the tar tokens minus the src tokens.

        For (multi-)sets S and T, this is :math:`T \setminus S`.
        """
        if self.params['intersection_type'] == 'soft':
            if not self._soft_intersection_precalc:
                self._intersection()
            return self._soft_tar_only
        tar_only = self._tar_tokens - self._intersection()
        if self.params['intersection_type'] != 'crisp':
            tar_only -= self._intersection() - self._crisp_intersection()
        return tar_only

    def _tar_only_card(self):
        """Return the cardinality of the tokens only in the target set."""
        return self.normalizer(
            sum(abs(val) for val in self._tar_only().values()),
            1,
            self._population_card_value,
        )

    def _symmetric_difference(self):
        r"""Return the symmetric difference of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \triangle T`.
        """
        return self._src_only() + self._tar_only()

    def _symmetric_difference_card(self):
        """Return the cardinality of the symmetric difference."""
        return self.normalizer(
            sum(abs(val) for val in self._symmetric_difference().values()),
            2,
            self._population_card_value,
        )

    def _total(self):
        """Return the sum of the sets.

        For (multi-)sets S and T, this is :math:`S + T`.

        In the case of multisets, this counts values in the interesection
        twice. In the case of sets, this is identical to the union.
        """
        if self.params['intersection_type'] == 'soft':
            if not self._soft_intersection_precalc:
                self._intersection()
            return (
                self._soft_tar_only
                + self._soft_src_only
                + self._soft_intersection_precalc
                + self._soft_intersection_precalc
            )
        return self._src_tokens + self._tar_tokens

    def _total_card(self):
        """Return the cardinality of the complement of the total."""
        return self.normalizer(
            sum(abs(val) for val in self._total().values()),
            3,
            self._population_card_value,
        )

    def _total_complement_card(self):
        """Return the cardinality of the complement of the total."""
        if self.params['alphabet'] is None:
            return self.normalizer(0, 1, self._population_card_value)
        elif isinstance(self.params['alphabet'], Counter):
            return self.normalizer(
                max(
                    0,
                    sum(
                        abs(val)
                        for val in (
                            self.params['alphabet'] - self._total()
                        ).values()
                    ),
                ),
                1,
                self._population_card_value,
            )
        return self.normalizer(
            max(0, self.params['alphabet'] - len(self._total().values())),
            1,
            self._population_card_value,
        )

    def _calc_population_card(self):
        """Return the cardinality of the population."""
        save_normalizer = self.normalizer
        self.normalizer = self._norm_none
        save_intersection = self.params['intersection_type']
        self.params['intersection_type'] = 'crisp'
        pop = self._total_card() + self._total_complement_card()
        self.normalizer = save_normalizer
        self.params['intersection_type'] = save_intersection
        return pop

    def _population_card(self):
        """Return the cardinality of the population."""
        return self.normalizer(
            self._population_card_value, 4, self._population_card_value
        )

    def _population_unique_card(self):
        """Return the cardinality of the population minus the intersection."""
        return self.normalizer(
            self._population_card_value - self._intersection_card(),
            4,
            self._population_card_value,
        )

    def _union(self):
        r"""Return the union of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \cup T`.
        """
        if self.params['intersection_type'] == 'soft':
            if not self._soft_intersection_precalc:
                self._intersection()
            return (
                self._soft_tar_only
                + self._soft_src_only
                + self._soft_intersection_precalc
            )
        union = self._total() - self._intersection()
        if self.params['intersection_type'] != 'crisp':
            union -= self._intersection() - self._crisp_intersection()
        return union

    def _union_card(self):
        """Return the cardinality of the union."""
        return self.normalizer(
            sum(abs(val) for val in self._union().values()),
            3,
            self._population_card_value,
        )

    def _difference(self):
        """Return the difference of the tokens, supporting negative values."""
        if self.params['intersection_type'] == 'soft':
            if not self._soft_intersection_precalc:
                self._intersection()
            _src_copy = Counter(self._soft_src_only)
            _src_copy.subtract(self._soft_tar_only)
            return _src_copy
        _src_copy = Counter(self._src_tokens)
        _src_copy.subtract(self._tar_tokens)
        return _src_copy

    def _crisp_intersection(self):
        r"""Return the intersection of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \cap T`.
        """
        return self._src_tokens & self._tar_tokens

    def _soft_intersection(self):
        """Return the soft source, target, & intersection tokens & weights.

        This implements the soft intersection defined by :cite:`Russ:2014` in
        a way that can reproduce the results in the paper.
        """
        if not hasattr(self.params['metric'], 'alignment'):
            raise TypeError(
                "Soft similarity requires a 'metric' with an alignment \
member function, such as Levenshtein."
            )

        intersection = self._crisp_intersection()
        src_only = self._src_tokens - self._tar_tokens
        tar_only = self._tar_tokens - self._src_tokens

        src_new = Counter()
        tar_new = Counter()

        def _membership(src, tar):
            greater_length = max(len(src), len(tar))
            return (
                max(
                    greater_length - self.params['metric'].dist_abs(src, tar),
                    self._lcprefix.dist_abs(src, tar),
                )
                / greater_length
            )

        def _token_src_tar_int(src, tar):
            src_tok = []
            tar_tok = []
            int_tok = []

            src_val = 0
            tar_val = 0
            int_val = 0

            _cost, _src, _tar = self.params['metric'].alignment(src, tar)

            for i in range(len(_src)):
                if _src[i] == _tar[i]:
                    src_tok.append('-')
                    tar_tok.append('-')
                    int_tok.append(_src[i])
                    int_val += 1
                else:
                    src_tok.append(_src[i])
                    if _src[i] != '-':
                        src_val += 1
                    tar_tok.append(_tar[i])
                    if _tar[i] != '-':
                        tar_val += 1
                    int_tok.append('-')

            src_val /= len(_src)
            tar_val /= len(_src)
            int_val /= len(_src)

            src_tok = ''.join(src_tok).strip('-')
            tar_tok = ''.join(tar_tok).strip('-')
            int_tok = ''.join(int_tok).strip('-')

            return src_tok, src_val, tar_tok, tar_val, int_tok, int_val

        # Dictionary ordering is important for reproducibility, so insertion
        # order needs to be controlled and retained.
        memberships = OrderedDict(
            ((src, tar), _membership(src, tar))
            for src, tar in sorted(product(src_only, tar_only))
        )

        while memberships:
            src_tok, tar_tok = max(memberships, key=memberships.get)
            if memberships[src_tok, tar_tok] > 0.0:
                pairings = min(src_only[src_tok], tar_only[tar_tok])
                if pairings:
                    (
                        src_ntok,
                        src_val,
                        tar_ntok,
                        tar_val,
                        int_ntok,
                        int_val,
                    ) = _token_src_tar_int(src_tok, tar_tok)

                    src_new[src_ntok] += src_val * pairings
                    tar_new[tar_ntok] += tar_val * pairings
                    intersection[int_ntok] += int_val * pairings

                    # Remove pairings from src_only/tar_only
                    src_only[src_tok] -= pairings
                    tar_only[tar_tok] -= pairings

            del memberships[src_tok, tar_tok]

        # Add src_new/tar_new back into src_only/tar_only
        src_only += src_new
        tar_only += tar_new

        # Save src_only/tar_only to the instance for retrieval later.
        self._soft_src_only = src_only
        self._soft_tar_only = tar_only
        self._soft_intersection_precalc = intersection

        return intersection

    def _fuzzy_intersection(self):
        r"""Return the fuzzy intersection of the tokens in src and tar.

        This implements the fuzzy intersection defined by :cite:`Wang:2014`.

        For two sets X and Y, the intersection :cite:`Wang:2014` is the sum of
        similarities of all tokens in the two sets that are greater than or
        equal to some threshold value (:math:`\delta`).

        The lower bound of on this intersection and the value when
        :math:`\delta = 1.0`, is the crisp intersection. Tokens shorter than
        :math:`\frac{\delta}{1-\delta}`, 4 in the case of the default threshold
        :math:`\delta = 0.8`, must match exactly to be included in the
        intersection.


        .. versionadded:: 0.4.0

        """
        intersection = self._crisp_intersection()
        src_only = self._src_tokens - self._tar_tokens
        tar_only = self._tar_tokens - self._src_tokens

        pair = {}
        for src_tok in sorted(src_only):
            for tar_tok in sorted(tar_only):
                sim = self.params['metric'].sim(src_tok, tar_tok)
                if sim >= self.params['threshold']:
                    pair[(src_tok, tar_tok)] = sim

        ordered_keys = [(pair[_], _[0], _[1]) for _ in pair]
        ordered_keys.sort(key=lambda x: x[2])
        ordered_keys.sort(key=lambda x: x[1])
        ordered_keys.sort(key=lambda x: x[0], reverse=True)

        for _, src_tok, tar_tok in ordered_keys:
            pairings = min(src_only[src_tok], tar_only[tar_tok])
            if pairings:
                sim = pair[(src_tok, tar_tok)]

                intersection[src_tok] += sim / 2 * pairings
                intersection[tar_tok] += sim / 2 * pairings

                src_only[src_tok] -= pairings
                tar_only[tar_tok] -= pairings

        """
        # Here is a slightly different optimization method, which is even
        # greedier than the above.
        # ordered by sim*pairings rather than just sim

        pair = {}
        for src_tok in sorted(src_only):
            for tar_tok in sorted(tar_only):
                sim = self.params['metric'].sim(src_tok, tar_tok)
                if sim >= self.params['threshold']:
                    pairings = min(src_only[src_tok], tar_only[tar_tok])
                    pair[(src_tok, tar_tok)] = sim*pairings

        for src_tok, tar_tok in sorted(pair, key=pair.get, reverse=True):
            pairings = min(src_only[src_tok], tar_only[tar_tok])
            if pairings:
                sim = pair[(src_tok, tar_tok)]

                intersection[src_tok] += sim / 2
                intersection[tar_tok] += sim / 2

                src_only[src_tok] -= pairings
                tar_only[tar_tok] -= pairings
        """

        return intersection

    def _group_linkage_intersection(self):
        r"""Return the group linkage intersection of the tokens in src and tar.

        This is based on group linkage, as defined by :cite:`On:2007`.

        Most of this method is concerned with solving the assignment problem,
        in order to find the weight of the maximum weight bipartite matching.
        The Hungarian algorithm of Munkres :cite:`Munkres:1957`, implemented
        below in Python & Numpy is used to solve the assignment problem since
        it is roughly twice as fast as SciPy's implementation.

        .. versionadded:: 0.4.0
        .. versionchanged:: 0.4.1
            Corrected the Hungarian algorithm & optimized it so that SciPy's
            version is no longer needed.

        """
        intersection = self._crisp_intersection()
        src_only_tok = sorted(self._src_tokens - self._tar_tokens)
        tar_only_tok = sorted(self._tar_tokens - self._src_tokens)
        src_only = self._src_tokens - self._tar_tokens
        tar_only = self._tar_tokens - self._src_tokens

        # Quoted text below is from Munkres (1957), cited above.

        # Pre-preliminaries: create square the matrix of scores
        n = max(len(src_only_tok), len(tar_only_tok))
        arr = np_zeros((n, n), dtype=float)

        for col in range(len(src_only_tok)):
            for row in range(len(tar_only_tok)):
                arr[row, col] = self.params['metric'].dist(
                    src_only_tok[col], tar_only_tok[row]
                )

        src_only_tok += [''] * (n - len(src_only_tok))
        tar_only_tok += [''] * (n - len(tar_only_tok))

        starred = np.zeros((n, n), dtype=np.bool)
        primed = np.zeros((n, n), dtype=np.bool)
        row_covered = np.zeros(n, dtype=np.bool)
        col_covered = np.zeros(n, dtype=np.bool)

        orig_sim = 1 - np.copy(arr)
        # Preliminaries:
        # P: "No lines are covered; no zeros are starred or primed."
        # P: "Consider a row of matrix A; subtract from each element in
        # this row the smallest element of this row. Do the same for each
        # row of A."
        arr -= arr.min(axis=1, keepdims=True)
        # P: "Then consider each column of the resulting matrix and
        # subtract from each column its smallest entry."
        arr -= arr.min(axis=0, keepdims=True)

        # P: "Consider a zero Z of the matrix. If there is no starred zero
        # in its row and none in its column, star Z. Repeat, considering
        # each zero in the matrix in turn. Then cover every column
        # containing a starred zero.
        for col in range(n):
            for row in range(n):
                if arr[row, col] == 0:
                    if (
                        np.count_nonzero(starred[row, :]) == 0
                        and np.count_nonzero(starred[:, col]) == 0
                    ):
                        starred[row, col] = True
                        col_covered[col] = True

        step = 1
        # This is the simple case where independent assignments are obvious
        # and found without the rest of the algorithm.
        if np.count_nonzero(col_covered) == n:
            step = 4

        while step < 4:
            if step == 1:
                # Step 1:
                # 1: "Choose a non-covered zero and prime it. Consider the
                # row containing it. If there is no starred zero in this
                # row, go at once to Step 2. If there is a starred zero Z
                # in this row, cover this row and uncover the column of Z."
                # 1: Repeat until all zeros are covered. Go to Step 3."
                zeros = tuple(zip(*((arr == 0).nonzero())))
                while step == 1:
                    for row, col in zeros:
                        if not (col_covered[col] | row_covered[row]):
                            primed[row, col] = True
                            z_cols = (starred[row, :]).nonzero()[0]
                            if not z_cols.size:
                                step = 2
                                break
                            else:
                                row_covered[row] = True
                                col_covered[z_cols[0]] = False

                    if step != 1:
                        break

                    for row, col in zeros:
                        if not (col_covered[col] | row_covered[row]):
                            break
                    else:
                        step = 3

            if step == 2:
                # Step 2:
                # 2: "There is a sequence of alternating starred and primed
                # zeros, constructed as follows: Let Z_0 denote the
                # uncovered 0'. [There is only one.] Let Z_1 denote the 0*
                # in Z_0's column (if any). Let Z_2 denote the 0' in Z_1's
                # row (we must prove that it exists). Let Z_3 denote the 0*
                # in Z_2's column (if any). Similarly continue until the
                # sequence stops at a 0', Z_{2k}, which has no 0* in its
                # column."
                z_series = []
                for row, col in zeros:  # pragma: no branch
                    if primed[row, col] and not (
                        row_covered[row] | col_covered[col]
                    ):
                        z_series.append((row, col))
                        break
                col = z_series[-1][1]
                while True:
                    row = tuple(
                        set((arr[:, col] == 0).nonzero()[0])
                        & set((starred[:, col]).nonzero()[0])
                    )
                    if row:
                        row = row[0]
                        z_series.append((row, col))
                        col = tuple(
                            set((arr[row, :] == 0).nonzero()[0])
                            & set((primed[row, :]).nonzero()[0])
                        )[0]
                        z_series.append((row, col))
                    else:
                        break

                # 2: "Unstar each starred zero of the sequence and star
                # each primed zero of the sequence. Erase all primes,
                # uncover every row, and cover every column containing a
                # 0*."
                primed[:, :] = False
                row_covered[:] = False
                col_covered[:] = False
                for row, col in z_series:
                    starred[row, col] = not starred[row, col]
                for col in range(n):
                    if np.count_nonzero(starred[:, col]):
                        col_covered[col] = True
                # 2: "If all columns are covered, the starred zeros form
                # the desired independent set. Otherwise, return to Step
                # 1."
                if np.count_nonzero(col_covered) == n:
                    step = 4
                else:
                    step = 1

            if step == 3:
                # Step 3:
                # 3: "Let h denote the smallest non-covered element of the
                # matrix; it will be positive. Add h to each covered row;
                # then subtract h from each uncovered column."
                h_val = float('inf')
                for col in range(n):
                    if not (col_covered[col]):
                        for row in range(n):
                            if (
                                not (row_covered[row])
                                and arr[row, col] < h_val
                            ):
                                h_val = arr[row, col]
                for row in range(n):
                    if row_covered[row]:
                        arr[row, :] += h_val
                for col in range(n):
                    if not (col_covered[col]):
                        arr[:, col] -= h_val

                # 3: "Return to Step 1, without altering any asterisks,
                # primes, or covered lines."
                step = 1

        for row, col in tuple(zip(*(starred.nonzero()))):
            sim = orig_sim[row, col]
            if sim >= self.params['threshold']:
                score = float(
                    (sim / 2)
                    * min(
                        src_only[src_only_tok[col]],
                        tar_only[tar_only_tok[row]],
                    )
                )
                intersection[src_only_tok[col]] += score
                intersection[tar_only_tok[row]] += score

        return intersection

    def _intersection_card(self):
        """Return the cardinality of the intersection."""
        return self.normalizer(
            sum(abs(val) for val in self._intersection().values()),
            1,
            self._population_card_value,
        )

    def _intersection(self):
        """Return the intersection.

        This function may be overridden by setting the intersection_type during
        initialization.
        """
        return self._crisp_intersection()  # pragma: no cover

    def _get_confusion_table(self):
        """Return the token counts as a ConfusionTable object."""
        return ConfusionTable(
            self._intersection_card(),
            self._total_complement_card(),
            self._src_only_card(),
            self._tar_only_card(),
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
