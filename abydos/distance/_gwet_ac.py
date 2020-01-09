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

"""abydos.distance._gwet_ac.

Gwet's AC correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['GwetAC']


class GwetAC(_TokenDistance):
    r"""Gwet's AC correlation.

    For two sets X and Y and a population N, Gwet's AC correlation
    :cite:`Gwet:2008` is

        .. math::

            corr_{Gwet_{AC}}(X, Y) = AC =
            \frac{p_o - p_e^{AC}}{1 - p_e^{AC}}

    where

        .. math::

            \begin{array}{lll}
            p_o &=&\frac{|X \cap Y| + |(N \setminus X) \setminus Y|}{|N|}

            p_e^{AC}&=&\frac{1}{2}\Big(\frac{|X|+|Y|}{|N|}\cdot
            \frac{|X \setminus Y| + |Y \setminus X|}{|N|}\Big)
            \end{array}


    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            \begin{array}{lll}
            p_o&=&\frac{a+d}{n}

            p_e^{AC}&=&\frac{1}{2}\Big(\frac{2a+b+c}{n}\cdot
            \frac{2d+b+c}{n}\Big)
            \end{array}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize GwetAC instance.

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
        super(GwetAC, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Gwet's AC correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gwet's AC correlation

        Examples
        --------
        >>> cmp = GwetAC()
        >>> cmp.corr('cat', 'hat')
        0.9948456319360438
        >>> cmp.corr('Niall', 'Neil')
        0.990945276504824
        >>> cmp.corr('aluminum', 'Catalan')
        0.9804734301840141
        >>> cmp.corr('ATCG', 'TAGC')
        0.9870811678360627


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = a + b + c + d

        po = (a + d) / n
        q = (2 * a + b + c) / (2 * n)
        pe = 2 * q * (1 - q)

        return (po - pe) / (1 - pe)

    def sim(self, src, tar):
        """Return the Gwet's AC similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gwet's AC similarity

        Examples
        --------
        >>> cmp = GwetAC()
        >>> cmp.sim('cat', 'hat')
        0.9974228159680218
        >>> cmp.sim('Niall', 'Neil')
        0.995472638252412
        >>> cmp.sim('aluminum', 'Catalan')
        0.9902367150920071
        >>> cmp.sim('ATCG', 'TAGC')
        0.9935405839180314


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
