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

"""abydos.distance._fuzzy_token_distance.

The distance._FuzzyTokenDistance module implements abstract class
_FuzzyTokenDistance.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter

from ._levenshtein import Levenshtein
from ._token_distance import _TokenDistance
from ..tokenizer import QGrams, WhitespaceTokenizer


class _FuzzyTokenDistance(_TokenDistance):
    """Abstract Fuzzy Token Distance class.

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, threshold=0.8, metric=None, **kwargs):
        """Initialize _FuzzyTokenDistance instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the abydos.tokenizer package, defaulting
            to the QGrams tokenizer with q=4
        threshold : float
            The minimum similarity for a pair of tokens to contribute to
            similarity
        metric : _Distance
            A distance instance from the abydos.distance package, defaulting
            to normalized Levenshtein similarity
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
        qval = 4 if 'qval' not in kwargs else kwargs['qval']
        tokenizer = (
            tokenizer
            if tokenizer is not None
            else WhitespaceTokenizer(scaler='set')
            if qval == 0
            else QGrams(qval=qval, start_stop='$#', skip=0, scaler='set')
        )

        super(_FuzzyTokenDistance, self).__init__(tokenizer, **kwargs)

        self.params['threshold'] = threshold
        self.params['metric'] = metric if metric is not None else Levenshtein()

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

        .. versionadded:: 0.4.0

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

    def fuzzy_intersection(self):
        """Return the fuzzy intersection of the tokens in src and tar."""
        overlap = len(self.intersection())
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
