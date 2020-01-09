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

"""abydos.distance._unknown_m.

Unknown M similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['UnknownM']


class UnknownM(_TokenDistance):
    r"""Unknown M similarity.

    For two sets X and Y and a population N, Unknown < similarity, which
    :cite:`SequentiX:2018` attributes to "Roux" but could not be
    located, is

        .. math::

            sim_{UnknownM}(X, Y) =
            \frac{|N|-|X \cap Y| \cdot |(N \setminus X) \setminus Y|}
            {\sqrt{|X| \cdot |N \setminus X| \cdot |Y| \cdot |N \setminus Y|}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{UnknownM} =
            \frac{n-ad}{\sqrt{(a+b)(c+d)(a+c)(b+d)}}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize UnknownM instance.

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
        super(UnknownM, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Unknown M similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unknown M similarity

        Examples
        --------
        >>> cmp = UnknownM()
        >>> cmp.sim_score('cat', 'hat')
        -0.24743589743589745
        >>> cmp.sim_score('Niall', 'Neil')
        -0.17964271701223158
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.0024283560516135103
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.2012836970474968


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        return (n - a * d) / (
            max(1.0, a + b)
            * max(1.0, c + d)
            * max(1.0, a + c)
            * max(1.0, b + d)
        ) ** 0.5

    def sim(self, src, tar):
        """Return the normalized Unknown M similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Unknown M similarity

        Examples
        --------
        >>> cmp = UnknownM()
        >>> cmp.sim('cat', 'hat')
        0.6237179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.5898213585061158
        >>> cmp.sim('aluminum', 'Catalan')
        0.49878582197419324
        >>> cmp.sim('ATCG', 'TAGC')
        0.3993581514762516


        .. versionadded:: 0.4.0

        """
        return (1.0 - self.sim_score(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
