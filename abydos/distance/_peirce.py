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

"""abydos.distance._peirce.

Peirce correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['Peirce']


class Peirce(_TokenDistance):
    r"""Peirce correlation.

    For two sets X and Y and a population N, the Peirce correlation
    :cite:`Peirce:1884` is

        .. math::

            corr_{Peirce}(X, Y) = \frac{|X \cap Y| \cdot
            |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus Y|}
            {|X| \cdot |N \setminus X|}

    Both :cite:`Choi:2010` and :cite:`Hubalek:1982` present a different formula
    and incorrectly attribute it to Peirce. Likewise, :cite:`Doolittle:1884`
    presents a different formula and incorrectly attributes it to Peirce. This
    is distinct from the formula he presents and attributes to himself.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{Peirce} =
            \frac{ad-bc}{(a+b)(c+d)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Peirce instance.

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
        super(Peirce, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Peirce correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Peirce correlation

        Examples
        --------
        >>> cmp = Peirce()
        >>> cmp.corr('cat', 'hat')
        0.49743589743589745
        >>> cmp.corr('Niall', 'Neil')
        0.32947729220222793
        >>> cmp.corr('aluminum', 'Catalan')
        0.10209049255441008
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006418485237483954


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        num = a * d - b * c
        if num:
            return num / ((a + b) * (c + d))
        return 0.0

    def sim(self, src, tar):
        """Return the Peirce similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Peirce similarity

        Examples
        --------
        >>> cmp = Peirce()
        >>> cmp.sim('cat', 'hat')
        0.7487179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.664738646101114
        >>> cmp.sim('aluminum', 'Catalan')
        0.5510452462772051
        >>> cmp.sim('ATCG', 'TAGC')
        0.496790757381258


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
