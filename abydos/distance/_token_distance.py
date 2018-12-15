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

from ._damerau_levenshtein import DamerauLevenshtein
from ._lcprefix import LCPrefix
from ._levenshtein import Levenshtein
from ._distance import _Distance
from ..tokenizer import QGrams, WhitespaceTokenizer


class _TokenDistance(_Distance):
    """Abstract Token Distance class.

    .. versionadded:: 0.3.6
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize _TokenDistance instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the abydos.tokenizer package
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.

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
            if hasattr(self.params['alphabet'], '__len__'):
                self.params['alphabet'] = len(self.params['alphabet'])
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

    def tokenize(self, src, tar):
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
        >>> pe.tokenize('AT', 'TT').get_tokens()
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

        return self

    def get_tokens(self):
        """Return the src and tar tokens as a tuple."""
        return self._src_tokens, self._tar_tokens

    def src_only(self):
        """Return the src tokens minus the tar tokens.

        For (multi-)sets S and T, this is :math:`S \setminus T`.
        """
        return self._src_tokens - self.intersection()

    def tar_only(self):
        """Return the tar tokens minus the src tokens.

        For (multi-)sets S and T, this is :math:`T \setminus S`.
        """
        return self._tar_tokens - self.intersection()

    def symmetric_difference(self):
        """Return the symmetric difference of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \triangle T`.
        """
        return self.src_only() + self.tar_only()

    def total(self):
        """Return the sum of the sets.

        For (multi-)sets S and T, this is :math:`S + T`.

        In the case of multisets, this counts values in the interesection
        twice. In the case of sets, this is identical to the union.
        """
        return self._src_tokens + self._tar_tokens

    def union(self):
        """Return the union of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \cup T`.
        """
        return self.total() - self.intersection()

    def _crisp_intersection(self):
        """Return the intersection of tokens from src and tar.

        For (multi-)sets S and T, this is :math:`S \cap T`.
        """
        return self._src_tokens & self._tar_tokens

    def difference(self):
        """Return the difference of the tokens, supporting negative values."""
        _src_copy = Counter(self._src_tokens)
        _src_copy.subtract(self._tar_tokens)
        return _src_copy

    def _soft_intersection(self):
        """Return the soft intersection of the tokens in src and tar."""
        intersection = sum(self._crisp_intersection().values())

        src_only = self.src_only()
        tar_only = self.tar_only()

        def _membership(src, tar):
            greater_length = max(len(src), len(tar))
            return max(greater_length - self.params['metric'].dist_abs(src, tar),
                       self._lcprefix.dist_abs(src, tar)) / greater_length

        memberships = {(src, tar): _membership(src, tar) for src, tar in product(self.src_only().items(), self.tar_only().items())}
        while memberships:
            src_tok, tar_tok = max(memberships, key=memberships.get)
            if memberships[src_tok, tar_tok] == 0.0:
                break
            pairings = min(src_only[src_tok], tar_only[tar_tok])
            intersection += memberships[src_tok, tar_tok]*pairings
            src_only[src_tok] -= pairings
            tar_only[tar_tok] -= pairings
            del memberships[src_tok, tar_tok]

        return intersection

    def _fuzzy_intersection(self):
        """Return the fuzzy intersection of the tokens in src and tar."""
        overlap = sum(self._crisp_intersection().values())
        src_only = self.src_only()
        tar_only = self.tar_only()

        for src_tok in src_only:
            for tar_tok in tar_only:
                sim = self.params['metric'].sim(src_tok, tar_tok)
                if sim >= self.params['threshold']:
                    overlap += sim

        return overlap

if __name__ == '__main__':
    import doctest

    doctest.testmod()
