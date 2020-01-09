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

"""abydos.distance._hellinger.

Hellinger distance
"""

from ._token_distance import _TokenDistance

__all__ = ['Hellinger']


class Hellinger(_TokenDistance):
    r"""Hellinger distance.

    For two multisets X and Y drawn from an alphabet S, Hellinger distance
    :cite:`Hellinger:1909` is

        .. math::

            dist_{Hellinger}(X, Y) =
            \sqrt{2 \cdot \sum_{i \in S} (\sqrt{|A_i|} - \sqrt{|B_i|})^2}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Hellinger instance.

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
        super(Hellinger, self).__init__(tokenizer=tokenizer, **kwargs)

    def dist_abs(self, src, tar):
        """Return the Hellinger distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Hellinger distance

        Examples
        --------
        >>> cmp = Hellinger()
        >>> cmp.dist_abs('cat', 'hat')
        2.8284271247461903
        >>> cmp.dist_abs('Niall', 'Neil')
        3.7416573867739413
        >>> cmp.dist_abs('aluminum', 'Catalan')
        5.477225575051661
        >>> cmp.dist_abs('ATCG', 'TAGC')
        4.47213595499958


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        alphabet = self._total().keys()

        return (
            2
            * sum(
                (
                    (abs(self._src_tokens[tok])) ** 0.5
                    - (abs(self._tar_tokens[tok])) ** 0.5
                )
                ** 2
                for tok in alphabet
            )
        ) ** 0.5

    def dist(self, src, tar):
        """Return the normalized Hellinger distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Hellinger distance

        Examples
        --------
        >>> cmp = Hellinger()
        >>> cmp.dist('cat', 'hat')
        0.8164965809277261
        >>> cmp.dist('Niall', 'Neil')
        0.881917103688197
        >>> cmp.dist('aluminum', 'Catalan')
        0.9128709291752769
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        score = self.dist_abs(src, tar)
        norm = (
            2
            * sum(
                max(self._src_tokens[tok], self._tar_tokens[tok]) ** 2
                for tok in self._total().keys()
            )
        ) ** 0.5
        return score / norm


if __name__ == '__main__':
    import doctest

    doctest.testmod()
