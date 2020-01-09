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

"""abydos.distance._unknown_k.

Unknown K distance
"""

from ._token_distance import _TokenDistance

__all__ = ['UnknownK']


class UnknownK(_TokenDistance):
    r"""Unknown K distance.

    For two sets X and Y and a population N, Unknown K distance, which
    :cite:`SequentiX:2018` attributes to "Excoffier" but could not be
    located, is

        .. math::

            dist_{UnknownK}(X, Y) =
            |N| \cdot (1 - \frac{|X \cap Y|}{|N|})

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{UnknownK} =
            n \cdot (1 - \frac{a}{n})

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize UnknownK instance.

        Parameters
        ----------
        alphabet : Counter, collection, int, or None
            This represents the alphabet of possible tokens.
            See :ref:`alphabet <alphabet>` description in
            :py:class:`_TokenDistance` for details.
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
        super(UnknownK, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist_abs(self, src, tar):
        """Return the Unknown K distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unknown K distance

        Examples
        --------
        >>> cmp = UnknownK()
        >>> cmp.dist_abs('cat', 'hat')
        782.0
        >>> cmp.dist_abs('Niall', 'Neil')
        782.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        784.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        784.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        n = self._population_unique_card()

        if not n:
            return 0.0
        return n * (1 - a / n)

    def dist(self, src, tar):
        """Return the normalized Unknown K distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Unknown K distance

        Examples
        --------
        >>> cmp = UnknownK()
        >>> cmp.dist('cat', 'hat')
        0.9974489795918368
        >>> cmp.dist('Niall', 'Neil')
        0.9974489795918368
        >>> cmp.dist('aluminum', 'Catalan')
        0.9987261146496815
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        score = self.dist_abs(src, tar)
        norm = self._population_unique_card()
        if score:
            return score / norm
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
