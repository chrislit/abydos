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

"""abydos.distance._bhattacharyya.

Bhattacharyya distance
"""

from math import log

from ._token_distance import _TokenDistance

__all__ = ['Bhattacharyya']


class Bhattacharyya(_TokenDistance):
    r"""Bhattacharyya distance.

    For two multisets X and Y drawn from an alphabet S, Bhattacharyya distance
    :cite:`Bhattacharyya:1946` is

        .. math::

            dist_{Bhattacharyya}(X, Y) =
            -log(\sum_{i \in S} \sqrt{X_iY_i})

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Bhattacharyya instance.

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
        super(Bhattacharyya, self).__init__(tokenizer=tokenizer, **kwargs)

    def dist_abs(self, src, tar):
        """Return the Bhattacharyya distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Bhattacharyya distance

        Examples
        --------
        >>> cmp = Bhattacharyya()
        >>> cmp.dist_abs('cat', 'hat')
        0.6931471805599453
        >>> cmp.dist_abs('Niall', 'Neil')
        1.0074515102711326
        >>> cmp.dist_abs('aluminum', 'Catalan')
        2.1383330595080277
        >>> cmp.dist_abs('ATCG', 'TAGC')
        -inf


        .. versionadded:: 0.4.0

        """
        bc = self.dist(src, tar)
        if bc == 0:
            return float('-inf')
        elif bc == 1:
            return 0.0
        else:
            return -log(bc)

    def dist(self, src, tar):
        """Return the Bhattacharyya coefficient of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Bhattacharyya distance

        Examples
        --------
        >>> cmp = Bhattacharyya()
        >>> cmp.dist('cat', 'hat')
        0.5
        >>> cmp.dist('Niall', 'Neil')
        0.3651483716701107
        >>> cmp.dist('aluminum', 'Catalan')
        0.11785113019775792
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        alphabet = self._intersection().keys()
        src_pop = sum(self._src_tokens.values())
        tar_pop = sum(self._tar_tokens.values())

        return float(
            sum(
                (
                    self._src_tokens[tok]
                    / src_pop
                    * self._tar_tokens[tok]
                    / tar_pop
                )
                ** 0.5
                for tok in alphabet
            )
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
