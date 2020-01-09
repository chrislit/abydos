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

"""abydos.distance._single_linkage.

single linkage distance
"""

from ._levenshtein import Levenshtein
from ._token_distance import _TokenDistance

__all__ = ['SingleLinkage']


class SingleLinkage(_TokenDistance):
    r"""Single linkage distance.

    For two multisets X and Y, single linkage distance
    :cite:`Deza:2016` is

        .. math::

            dist_{SingleLinkage}(X, Y) =
            min_{i \in X, j \in Y} dist(X_i, Y_j)

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, metric=None, **kwargs):
        """Initialize SingleLinkage instance.

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
        super(SingleLinkage, self).__init__(tokenizer=tokenizer, **kwargs)
        if metric is None:
            self._metric = Levenshtein()
        else:
            self._metric = metric

    def dist_abs(self, src, tar):
        """Return the single linkage distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            single linkage distance

        Examples
        --------
        >>> cmp = SingleLinkage()
        >>> cmp.dist_abs('cat', 'hat')
        0.0
        >>> cmp.dist_abs('Niall', 'Neil')
        0.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        src, tar = self._get_tokens()

        min_val = float('inf')

        for term_src in src.keys():
            for term_tar in tar.keys():
                min_val = min(
                    min_val, self._metric.dist_abs(term_src, term_tar)
                )

        return float(min_val)

    def dist(self, src, tar):
        """Return the normalized single linkage distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            normalized single linkage distance

        Examples
        --------
        >>> cmp = SingleLinkage()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        src, tar = self._get_tokens()

        min_val = 1.0

        for term_src in src.keys():
            for term_tar in tar.keys():
                min_val = min(min_val, self._metric.dist(term_src, term_tar))

        return float(min_val)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
