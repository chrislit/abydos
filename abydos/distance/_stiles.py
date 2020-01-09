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

"""abydos.distance._stiles.

Stiles similarity
"""

from math import copysign, log10

from ._token_distance import _TokenDistance

__all__ = ['Stiles']


class Stiles(_TokenDistance):
    r"""Stiles similarity.

    For two sets X and Y and a population N, Stiles similarity
    :cite:`Stiles:1961` is

        .. math::

            sim_{Stiles}(X, Y) = log_{10}
            \frac{|N| \Big(||X \cap Y| \cdot
            |N| -
            |X \setminus Y| \cdot |Y \setminus X|| -
            \frac{|N|}{2}\Big)^2}
            {|X \setminus Y| \cdot |Y \setminus X| \cdot
            (|N| - |X \setminus Y|) \cdot
            (|N| - |Y \setminus X|)}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Stiles} =
            log_{10} \frac{n(|an-bc|-\frac{1}{2}n)^2}{bc(n-b)(n-c)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Stiles instance.

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
        super(Stiles, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Stiles similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Stiles similarity

        Examples
        --------
        >>> cmp = Stiles()
        >>> cmp.sim_score('cat', 'hat')
        2.6436977886009236
        >>> cmp.sim_score('Niall', 'Neil')
        2.1622951406967723
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.41925115106844024
        >>> cmp.sim_score('ATCG', 'TAGC')
        -0.8426334527850912


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        eps = 0.0000001
        a = max(self._intersection_card(), eps)
        b = max(self._src_only_card(), eps)
        c = max(self._tar_only_card(), eps)
        n = max(self._total_complement_card(), eps) + a + b + c

        anmbc = a * n - b * c

        return copysign(
            log10(
                n
                * max((abs(anmbc) - n / 2) ** 2, eps)
                / (b * (n - b) * c * (n - c))
            ),
            anmbc,
        )

    def corr(self, src, tar):
        """Return the Stiles correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Stiles correlation

        Examples
        --------
        >>> cmp = Stiles()
        >>> cmp.corr('cat', 'hat')
        0.14701542182970487
        >>> cmp.corr('Niall', 'Neil')
        0.11767566062554877
        >>> cmp.corr('aluminum', 'Catalan')
        0.022355640924908403
        >>> cmp.corr('ATCG', 'TAGC')
        -0.046296656196428934


        .. versionadded:: 0.4.0

        """
        return self.sim_score(src, tar) / max(
            self.sim_score(src, src), self.sim_score(tar, tar)
        )

    def sim(self, src, tar):
        """Return the normalized Stiles similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Stiles similarity

        Examples
        --------
        >>> cmp = Stiles()
        >>> cmp.sim('cat', 'hat')
        0.5735077109148524
        >>> cmp.sim('Niall', 'Neil')
        0.5588378303127743
        >>> cmp.sim('aluminum', 'Catalan')
        0.5111778204624542
        >>> cmp.sim('ATCG', 'TAGC')
        0.4768516719017855


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
