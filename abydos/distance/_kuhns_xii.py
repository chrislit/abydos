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

"""abydos.distance._kuhns_xii.

Kuhns XII similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['KuhnsXII']


class KuhnsXII(_TokenDistance):
    r"""Kuhns XII similarity.

    For two sets X and Y and a population N, Kuhns XII similarity
    :cite:`Kuhns:1965`, the excess of index of independence over its
    independence value (I), is

        .. math::

            sim_{KuhnsXII}(X, Y) =
            \frac{|N| \cdot \delta(X, Y)}{|X| \cdot |Y|}

    where

        .. math::

            \delta(X, Y) = |X \cap Y| - \frac{|X| \cdot |Y|}{|N|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{KuhnsXII} =
            \frac{n \cdot \delta(a+b, a+c)}{(a+b)(a+c)}

    where

        .. math::

            \delta(a+b, a+c) = a - \frac{(a+b)(a+c)}{n}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize KuhnsXII instance.

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
        super(KuhnsXII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Kuhns XII similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns XII similarity

        Examples
        --------
        >>> cmp = KuhnsXII()
        >>> cmp.sim_score('cat', 'hat')
        97.0
        >>> cmp.sim_score('Niall', 'Neil')
        51.266666666666666
        >>> cmp.sim_score('aluminum', 'Catalan')
        9.902777777777779
        >>> cmp.sim_score('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        n = self._population_unique_card()

        apbmapc = (a + b) * (a + c)
        if not apbmapc:
            delta_ab = a
        else:
            delta_ab = a - apbmapc / n
        if not delta_ab:
            return 0.0
        else:
            return max(-1.0, n * delta_ab / ((a + b) * (a + c)))

    def sim(self, src, tar):
        """Return the normalized Kuhns XII similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Kuhns XII similarity

        Examples
        --------
        >>> cmp = KuhnsXII()
        >>> cmp.sim('cat', 'hat')
        0.2493573264781491
        >>> cmp.sim('Niall', 'Neil')
        0.1323010752688172
        >>> cmp.sim('aluminum', 'Catalan')
        0.012877474353417137
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        score = self.sim_score(src, tar)
        minval, maxval = sorted(
            [self._intersection_card(), self._total_complement_card()]
        )
        if score < 0.0:
            return min(1.0, (1.0 + score) / 2.0)
        norm = 1.0
        if minval and maxval:
            norm = maxval / minval
        return min(1.0, score / norm)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
