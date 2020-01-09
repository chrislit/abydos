# Copyright 2019-2020 by Christopher C. Little.
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

from ._levenshtein import Levenshtein
from ._token_distance import _TokenDistance

__all__ = ['AverageLinkage']


class AverageLinkage(_TokenDistance):
    r"""Average linkage distance.

    For two lists of tokens X and Y, average linkage distance
    :cite:`Deza:2016` is

        .. math::

            dist_{AverageLinkage}(X, Y) =
            \frac{\sum_{i \in X} \sum_{j \in Y} dist(X_i, Y_j)}{|X| \cdot |Y|}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, metric=None, **kwargs):
        """Initialize AverageLinkage instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        metric : _Distance
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants. (Defaults to Levenshtein distance)
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

    def dist(self, src, tar):
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
        >>> cmp.dist('cat', 'hat')
        0.8125
        >>> cmp.dist('Niall', 'Neil')
        0.8333333333333334
        >>> cmp.dist('aluminum', 'Catalan')
        0.9166666666666666
        >>> cmp.dist('ATCG', 'TAGC')
        0.8


        .. versionadded:: 0.4.0

        """
        if not src and not tar:
            return 0.0

        src = self.params['tokenizer'].tokenize(src).get_list()
        tar = self.params['tokenizer'].tokenize(tar).get_list()

        if not src or not tar:
            return 1.0

        num = 0.0
        den = len(src) * len(tar)

        for term_src in src:
            for term_tar in tar:
                num += self._metric.dist(term_src, term_tar)

        return num / den


if __name__ == '__main__':
    import doctest

    doctest.testmod()
