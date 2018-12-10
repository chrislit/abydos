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

"""abydos.distance._fuzzy_overlap.

Fuzzy overlap similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._fuzzy_token_distance import _FuzzyTokenDistance

__all__ = ['FuzzyOverlap']


class FuzzyOverlap(_FuzzyTokenDistance):
    r"""Fuzzy overlap coefficient.

    For two sets X and Y, the overlap coefficient
    :cite:`Szymkiewicz:1934,Simpson:1949`, also called the
    Szymkiewicz-Simpson coefficient, is
    :math:`sim_{overlap}(X, Y) = \frac{|X \cap Y|}{min(|X|, |Y|)}`.

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, threshold=0.8, metric=None, **kwargs):
        """Initialize FuzzyOverlap instance.

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
        super(FuzzyOverlap, self).__init__(tokenizer=tokenizer, threshold=threshold, metric=metric, **kwargs)

    def sim(self, src, tar):
        r"""Return the fuzzy overlap coefficient of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fuzzy overlap similarity

        Examples
        --------
        >>> cmp = FuzzyOverlap()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.4
        >>> cmp.sim('aluminum', 'Catalan')
        0.125
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0

        self.tokenize(src, tar)

        q_src_mag = sum(self._src_tokens.values())
        q_tar_mag = sum(self._tar_tokens.values())
        q_intersection_mag = self.fuzzy_overlap()

        return q_intersection_mag / min(q_src_mag, q_tar_mag)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
