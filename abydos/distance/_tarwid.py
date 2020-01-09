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

"""abydos.distance._tarwid.

Tarwid correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['Tarwid']


class Tarwid(_TokenDistance):
    r"""Tarwid correlation.

    For two sets X and Y and a population N, the Tarwid correlation
    :cite:`Tarwid:1960` is

        .. math::

            corr_{Tarwid}(X, Y) =
            \frac{|N| \cdot |X \cap Y| - |X| \cdot |Y|}
            {|N| \cdot |X \cap Y| + |X| \cdot |Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{Tarwid} =
            \frac{na-(a+b)(a+c)}{na+(a+b)(a+c)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Tarwid instance.

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
        super(Tarwid, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Tarwid correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Tarwid correlation

        Examples
        --------
        >>> cmp = Tarwid()
        >>> cmp.corr('cat', 'hat')
        0.9797979797979798
        >>> cmp.corr('Niall', 'Neil')
        0.9624530663329162
        >>> cmp.corr('aluminum', 'Catalan')
        0.8319719953325554
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        nta = self._population_unique_card() * self._intersection_card()
        abtac = self._src_card() * self._tar_card()

        if nta == abtac:
            return 0.0
        return (nta - abtac) / (nta + abtac)

    def sim(self, src, tar):
        """Return the Tarwid similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Tarwid similarity

        Examples
        --------
        >>> cmp = Tarwid()
        >>> cmp.sim('cat', 'hat')
        0.9898989898989898
        >>> cmp.sim('Niall', 'Neil')
        0.981226533166458
        >>> cmp.sim('aluminum', 'Catalan')
        0.9159859976662776
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
