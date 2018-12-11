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

"""abydos.distance._fuzzy_cosine.

Fuzzy Cosine similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import sqrt

from ._fuzzy_token_distance import _FuzzyTokenDistance

__all__ = ['FuzzyCosine']


class FuzzyCosine(_FuzzyTokenDistance):
    r"""Fuzzy Cosine similarity.

    For two sets X and Y, the Fuzzy Cosine similarity :cite:`Wang:2014` is:
    :math:`sim_{Fuzzy Cosine_\delta}(X, Y) = \frac{|X \widetilde\cap_\delta Y|}{\sqrt{|X| \cdot |Y|}}`,
    where :math:`|X \widetilde\cap_\delta Y|` is the fuzzy overlap or fuzzy
    intersection. This fuzzy intersection is sum of similarities of all tokens
    in the two sets that are greater than equal to some threshold value
    (:math:`\delta`).

    The lower bound of Fuzzy Cosine similarity, and the value when
    :math:`\delta = 1.0`, is the cosine similarity. Tokens shorter than
    :math:`\frac{\delta}{1-\delta}`, 4 in the case of the default threshold
    :math:`\delta = 0.8`, must match exactly to contribute to similarity.

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, threshold=0.8, metric=None, **kwargs):
        """Initialize FuzzyCosine instance.

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
        super(FuzzyCosine, self).__init__(tokenizer=tokenizer, threshold=threshold, metric=metric, **kwargs)

    def sim(self, src, tar):
        r"""Return the Fuzzy Cosine similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fuzzy Cosine similarity

        Examples
        --------
        >>> cmp = FuzzyCosine()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3651483716701107
        >>> cmp.sim('aluminum', 'Catalan')
        0.11785113019775793
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        self.tokenize(src, tar)

        return self.fuzzy_intersection() / sqrt(
            sum(self._src_tokens.values()) * sum(self._tar_tokens.values())
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
