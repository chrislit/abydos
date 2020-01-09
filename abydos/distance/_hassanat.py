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

"""abydos.distance._hassanat.

Hassanat distance
"""

from ._token_distance import _TokenDistance

__all__ = ['Hassanat']


class Hassanat(_TokenDistance):
    r"""Hassanat distance.

    For two multisets X and Y drawn from an alphabet S, Hassanat distance
    :cite:`Hassanat:2014` is

        .. math::

            dist_{Hassanat}(X, Y) = \sum_{i \in S} D(X_i, Y_i)

    where

        .. math::

            D(X_i, Y_i) =
            \left\{\begin{array}{ll}
                1-\frac{1+min(X_i, Y_i)}{1+max(X_i, Y_i)}&,
                min(X_i, Y_i) \geq 0
                \\
                \\
                1-\frac{1+min(X_i, Y_i)+|min(X_i, Y_i)|}
                {1+max(X_i, Y_i)+|min(X_i, Y_i)|}&,
                min(X_i, Y_i) < 0
            \end{array}\right.

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Hassanat instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
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
        super(Hassanat, self).__init__(tokenizer=tokenizer, **kwargs)

    def dist_abs(self, src, tar):
        """Return the Hassanat distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Hassanat distance

        Examples
        --------
        >>> cmp = Hassanat()
        >>> cmp.dist_abs('cat', 'hat')
        2.0
        >>> cmp.dist_abs('Niall', 'Neil')
        3.5
        >>> cmp.dist_abs('aluminum', 'Catalan')
        7.166666666666667
        >>> cmp.dist_abs('ATCG', 'TAGC')
        5.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        distance = 0.0

        for tok in self._total().keys():
            x = self._src_tokens[tok]
            y = self._tar_tokens[tok]

            min_val = min(x, y)
            if min_val >= 0:
                distance += 1 - (1 + min_val) / (1 + max(x, y))
            else:
                distance += 1 - 1 / (1 + max(x, y) - min_val)

        return distance

    def dist(self, src, tar):
        """Return the normalized Hassanat distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Hassanat distance

        Examples
        --------
        >>> cmp = Hassanat()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.3888888888888889
        >>> cmp.dist('aluminum', 'Catalan')
        0.4777777777777778
        >>> cmp.dist('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0
        return self.dist_abs(src, tar) / len(self._total().keys())


if __name__ == '__main__':
    import doctest

    doctest.testmod()
