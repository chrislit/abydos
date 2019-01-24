# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._average_linkage.

Average linkage distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance
from ._levenshtein import Levenshtein

__all__ = ['AverageLinkage']


class AverageLinkage(_TokenDistance):
    r"""Average linkage distance.

    For two multisets X and Y, average linkage distance
    :cite:`Deza:2016` is

        .. math::

            dist_{AverageLinkage}(X, Y) =
            \frac{\sum_{i \in X} \sum{j \in Y} dist(X_i, Y_j)
            \cdot |X_i| \cdot |Y_j|}{|X| \cdot |Y|}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, metric=None, **kwargs):
        """Initialize AverageLinkage instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        metric : _Distance
            A string distance measure class for use in the 'soft' and 'fuzzy'
            variants. (Defaults to Levenshtein distance)
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
        super(AverageLinkage, self).__init__(tokenizer=tokenizer, **kwargs)
        if metric is None:
            self._metric = Levenshtein()
        else:
            self._metric = metric

    def sim(self, src, tar):
        """Return the average linkage distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            average linkage distance

        Examples
        --------
        >>> cmp = AverageLinkage()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        src, tar = self._get_tokens()

        num = 0
        den = sum(src.values()) * sum(src.values())

        for term_src, wt_src in src.items():
            for term_tar, wt_tar in tar.items():
                num += self._metric.dist(term_src, term_tar) * wt_src * wt_tar

        return num / den


if __name__ == '__main__':
    import doctest

    doctest.testmod()
