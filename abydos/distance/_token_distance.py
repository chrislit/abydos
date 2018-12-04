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

The distance._TokenDistance module implements abstract class _TokenDistance.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter

from ._distance import _Distance
from ..tokenizer import QGrams, WhitespaceTokenizer


class _TokenDistance(_Distance):
    """Abstract Token Distance class.

    .. versionadded:: 0.3.6
    """

    def __init__(self, tokenizer=None, **kwargs):
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
        """Return the src tokens minus the tar tokens."""
        return self._src_tokens - self._tar_tokens

    def tar_only(self):
        """Return the tar tokens minus the src tokens."""
        return self._tar_tokens - self._src_tokens

    def union(self):
        """Return the union (sum) of tokens from src and tar."""
        return self._src_tokens + self._tar_tokens

    def intersection(self):
        """Return the intersection of tokens from src and tar."""
        return self._src_tokens & self._tar_tokens

    def difference(self):
        """Return the difference of the tokens, supporting negative values."""
        _src_copy = Counter(self._src_tokens)
        _src_copy.subtract(self._tar_tokens)
        return _src_copy


if __name__ == '__main__':
    import doctest

    doctest.testmod()
