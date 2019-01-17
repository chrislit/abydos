# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter
from itertools import product
from math import exp, log1p

from ._damerau_levenshtein import DamerauLevenshtein
from ._distance import _Distance
from ._lcprefix import LCPrefix
from ._levenshtein import Levenshtein
from ..stats import ConfusionTable
from ..tokenizer import QGrams, WhitespaceTokenizer

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
                - 'fuzzy': Fuzzy intersection, defined by :cite:`Wang:2014`,
                  wherein items can be partially members of the intersection
                  if their similarity meets or exceeds a threshold value. This
                  also takes `metric` (by default :class:`Levenshtein()`) and
                  `threshold` (by default 0.8) parameters.
                - 'soft': Soft intersection, defined by :cite:`Russ:2014`,
                  wherein items can be partially members of the intersection
                  depending on their similarity. This also takes a `metric`
                  (by default :class:`DamerauLevenshtein()`) parameter.
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
            A string distance measure class for use in the 'soft' and 'fuzzy'
            variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the 'fuzzy' variant.
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
                  is inferred if QGram tokenization is used (i.e.
                  :math:`28^{QGrams.qval}` is used as the cardinality of the
                  full alphabet or :math:`26` if QGrams.qval is 1, which
                  assumes the strings are English language strings). Otherwise,
                  The cardinality of the complement of the total will be 0.
        normalizer : str
            This represents the normalization applied to the values in the
            2x2 contingency table prior to any of the cardinality (\*_card)
            methods returning a value. By default, no normalization is applied,
            but the following values are supported:

                - 'proportional' : :math:`\frac{x}{n}`, where n is the total
                  population
                - 'log' : :math:`log(1+x)`
                - 'exp' : :math:`e^x`
                - 'laplace' : :math:`x+1`
                - 'inverse' : :math:`\frac{1}{x}`
                - 'complement' : :math:`n-x`, where n is the total population

        .. versionadded:: 0.4.0

        """
        super(_TokenDistance, self).__init__(**kwargs)

        qval = 2 if 'qval' not in self.params else self.params['qval']
        self.params['tokenizer'] = (
            tokenizer
            if tokenizer is not None
            else WhitespaceTokenizer()
            if qval == 0
            else QGrams(qval=qval, start_stop='$#', skip=0, scaler=None)
        )

        if 'alphabet' in self.params:
            if isinstance(self.params['alphabet'], str):
                self.params['alphabet'] = set(self.params['alphabet'])
                if isinstance(self.params['tokenizer'], QGrams):
                    self.params['alphabet'] |= set(
                        self.params['tokenizer'].start_stop
                    )
                    self.params['alphabet'] = (
                        len(self.params['alphabet'])
                        ** self.params['tokenizer'].qval
                    )
            if hasattr(self.params['alphabet'], '__len__'):
                self.params['alphabet'] = len(self.params['alphabet'])
        else:
            if isinstance(self.params['tokenizer'], QGrams):
                self.params['alphabet'] = (
                    26 + len(set(self.params['tokenizer'].start_stop))
                ) ** self.params['tokenizer'].qval
            else:
                self.params['alphabet'] = None

        if intersection_type == 'soft':
            if 'metric' not in self.params or self.params['metric'] is None:
                self.params['metric'] = DamerauLevenshtein()
            self._lcprefix = LCPrefix()
            self.intersection = self._soft_intersection
        elif intersection_type == 'fuzzy':
            if 'metric' not in self.params or self.params['metric'] is None:
                self.params['metric'] = Levenshtein()
            if 'threshold' not in self.params:
                self.params['threshold'] = 0.8
            self.intersection = self._fuzzy_intersection
        else:
            self.intersection = self._crisp_intersection

        self._src_tokens = Counter()
        self._tar_tokens = Counter()
        self._population_card = 0

        # Set up the normalizer, a function of two variables:
        # x is the value in the contingency table square(s)
        # n is the number of squares that x represents
        self.normalizer = lambda x, n: x
        if 'normalizer' in self.params:
            if self.params['normalizer'] == 'proportional':
                self.normalizer = lambda x, n: x / self._population_card
            elif self.params['normalizer'] == 'log':
                self.normalizer = lambda x, n: log1p(x)
            elif self.params['normalizer'] == 'exp':
                self.normalizer = lambda x, n: exp(x)
            elif self.params['normalizer'] == 'laplace':
                self.normalizer = lambda x, n: x + n
            elif self.params['normalizer'] == 'inverse:':
                self.normalizer = (
                    lambda x, n: 1 / x if x else self._population_card
                )
            elif self.params['normalizer'] == 'complement':
                self.normalizer = lambda x, n: self._population_card - x

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
        if isinstance(src, Counter):
            self._src_tokens = src
        else:
            self._src_tokens = (
                self.params['tokenizer'].tokenize(src).get_counter()
            )
        if isinstance(src, Counter):
            self._tar_tokens = tar
        else:
            self._tar_tokens = (
                self.params['tokenizer'].tokenize(tar).get_counter()
            )

        self._population_card = self._calc_population_card()

        return self

    def _get_tokens(self):
        """Return the src and tar tokens as a tuple."""
        return self._src_tokens, self._tar_tokens

    def _src_card(self):
        r"""Return the cardinality of the tokens in the source set."""
        return self.normalizer(
            sum(abs(val) for val in self._src_tokens.values()), 2
        )

    def _src_only(self):
        r"""Return the src tokens minus the tar tokens.

        For (multi-)sets S and T, this is :math:`S \setminus T`.
        """
        return self._src_tokens - self.intersection()

    def _src_only_card(self):
        """Return the cardinality of the tokens only in the source set."""
        return self.normalizer(
            sum(abs(val) for val in self._src_only().values()), 1
        )

    def _tar_card(self):
        r"""Return the cardinality of the tokens in the target set."""
        return self.normalizer(
            sum(abs(val) for val in self._tar_tokens.values()), 2
        )

    def _tar_only(self):
        r"""Return the tar tokens minus the src tokens.

        For (multi-)sets S and T, this is :math:`T \setminus S`.
        """
        return self._tar_tokens - self.intersection()

    def _tar_only_card(self):
        """Return the cardinality of the tokens only in the target set."""
        return self.normalizer(
            sum(abs(val) for val in self._tar_only().values()), 1
        )

    def _symmetric_difference(self):
        r"""Return the symmetric difference of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \triangle T`.
        """
        return self._src_only() + self._tar_only()

    def _symmetric_difference_card(self):
        """Return the cardinality of the symmetric difference."""
        return self.normalizer(
            sum(abs(val) for val in self._symmetric_difference().values()), 2
        )

    def _total(self):
        """Return the sum of the sets.

        For (multi-)sets S and T, this is :math:`S + T`.

        In the case of multisets, this counts values in the interesection
        twice. In the case of sets, this is identical to the union.
        """
        return self._src_tokens + self._tar_tokens

    def _total_card(self):
        """Return the cardinality of the complement of the total."""
        return self.normalizer(
            sum(abs(val) for val in self._total().values()), 3
        )

    def _total_complement_card(self):
        """Return the cardinality of the complement of the total."""
        if self.params['alphabet'] is None:
            return self.normalizer(0, 1)
        elif isinstance(self.params['alphabet'], Counter):
            return self.normalizer(
                sum(
                    abs(val)
                    for val in (self.params['alphabet']).values()
                    - self._total()
                ),
                1,
            )
        return self.normalizer(
            self.params['alphabet'] - len(self._total().values()), 1
        )

    def _calc_population_card(self):
        """Return the cardinality of the population."""
        return self._total_card() + self._total_complement_card()

    def _population_card(self):
        """Return the cardinality of the population."""
        return self.normalizer(self._population_card, 4)

    def _union(self):
        r"""Return the union of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \cup T`.
        """
        return self._total() - self.intersection()

    def _union_card(self):
        """Return the cardinality of the union."""
        return self.normalizer(
            sum(abs(val) for val in self._union().values()), 3
        )

    def _difference(self):
        """Return the difference of the tokens, supporting negative values."""
        _src_copy = Counter(self._src_tokens)
        _src_copy.subtract(self._tar_tokens)
        return _src_copy

    def _crisp_intersection(self):
        r"""Return the intersection of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \cap T`.
        """
        return self._src_tokens & self._tar_tokens

    def _soft_intersection(self):
        """Return the soft intersection of the tokens in src and tar.

        This implements the soft intersection defined by :cite:`Russ:2014`.
        """
        intersection = self._crisp_intersection()
        src_only = self._src_tokens - self._tar_tokens
        tar_only = self._tar_tokens - self._src_tokens

        def _membership(src, tar):
            greater_length = max(len(src), len(tar))
            return (
                max(
                    greater_length - self.params['metric'].dist_abs(src, tar),
                    self._lcprefix.dist_abs(src, tar),
                )
                / greater_length
            )

        memberships = {
            (src, tar): _membership(src, tar)
            for src, tar in product(src_only, tar_only)
        }
        while memberships:
            src_tok, tar_tok = max(memberships, key=memberships.get)
            if memberships[src_tok, tar_tok] == 0.0:
                break
            pairings = min(src_only[src_tok], tar_only[tar_tok])
            intersection[src_tok] += (
                memberships[src_tok, tar_tok] * pairings / 2
            )
            intersection[tar_tok] += (
                memberships[src_tok, tar_tok] * pairings / 2
            )
            src_only[src_tok] -= pairings
            tar_only[tar_tok] -= pairings
            del memberships[src_tok, tar_tok]

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

        for src_tok in src_only:
            for tar_tok in tar_only:
                sim = self.params['metric'].sim(src_tok, tar_tok)
                if sim >= self.params['threshold']:
                    intersection[src_tok] += sim / 2
                    intersection[tar_tok] += sim / 2

        return intersection

    def _intersection_card(self):
        """Return the cardinality of the intersection."""
        return self.normalizer(
            sum(abs(val) for val in self.intersection().values()), 1
        )

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
