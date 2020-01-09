# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.distance._chord.

Chord distance
"""

from ._token_distance import _TokenDistance

__all__ = ['Chord']


class Chord(_TokenDistance):
    r"""Chord distance.

    For two sets X and Y drawn from an alphabet S, the chord distance
    :cite:`Orloci:1967` is

        .. math::

            sim_{chord}(X, Y) =
            \sqrt{\sum_{i \in S}\Big(\frac{X_i}{\sqrt{\sum_{j \in X} X_j^2}} -
            \frac{Y_i}{\sqrt{\sum_{j \in Y} Y_j^2}}\Big)^2}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Chord instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.
        metric : _Distance
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the ``fuzzy`` variant.


        .. versionadded:: 0.4.0

        """
        super(Chord, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def dist_abs(self, src, tar):
        """Return the Chord distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Chord distance

        Examples
        --------
        >>> cmp = Chord()
        >>> cmp.dist_abs('cat', 'hat')
        1.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.126811100699571
        >>> cmp.dist_abs('aluminum', 'Catalan')
        1.336712116966249
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.414213562373095


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        alphabet = self._total().keys()

        den1 = max(
            1, sum(val * val for val in self._src_tokens.values()) ** 0.5
        )
        den2 = max(
            1, sum(val * val for val in self._tar_tokens.values()) ** 0.5
        )

        return round(
            sum(
                (self._src_tokens[i] / den1 - self._tar_tokens[i] / den2) ** 2
                for i in alphabet
            )
            ** 0.5,
            15,
        )

    def dist(self, src, tar):
        """Return the normalized Chord distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized chord distance

        Examples
        --------
        >>> cmp = Chord()
        >>> cmp.dist('cat', 'hat')
        0.707106781186547
        >>> cmp.dist('Niall', 'Neil')
        0.796775770420944
        >>> cmp.dist('aluminum', 'Catalan')
        0.94519820240106
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        return round(self.dist_abs(src, tar) / (2 ** 0.5), 15)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
