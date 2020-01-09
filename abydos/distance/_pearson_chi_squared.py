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

"""abydos.distance._pearson_chi_squared.

Pearson's Chi-Squared similarity
"""

from math import copysign

from ._token_distance import _TokenDistance

__all__ = ['PearsonChiSquared']


class PearsonChiSquared(_TokenDistance):
    r"""Pearson's Chi-Squared similarity.

    For two sets X and Y and a population N, the Pearson's :math:`\chi^2`
    similarity :cite:`Pearson:1913` is

        .. math::

            sim_{PearsonChiSquared}(X, Y) =
            \frac{|N| \cdot (|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)^2}
            {|X| \cdot |Y| \cdot |N \setminus X| \cdot |N \setminus Y|}

    This is also Pearson I similarity.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{PearsonChiSquared} =
            \frac{n(ad-bc)^2}{(a+b)(a+c)(b+d)(c+d)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize PearsonChiSquared instance.

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
        super(PearsonChiSquared, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return Pearson's Chi-Squared similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson's Chi-Squared similarity

        Examples
        --------
        >>> cmp = PearsonChiSquared()
        >>> cmp.sim_score('cat', 'hat')
        193.99489809335964
        >>> cmp.sim_score('Niall', 'Neil')
        101.99771068526542
        >>> cmp.sim_score('aluminum', 'Catalan')
        9.19249664336649
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.032298410951138765


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()
        ab = self._src_card()
        ac = self._tar_card()

        if src == tar:
            return float(n)
        if not src or not tar:
            return 0.0
        num = n * (a * d - b * c) ** 2
        if num:
            return num / (ab * ac * (b + d) * (c + d))
        return 0.0

    def corr(self, src, tar):
        """Return Pearson's Chi-Squared correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson's Chi-Squared correlation

        Examples
        --------
        >>> cmp = PearsonChiSquared()
        >>> cmp.corr('cat', 'hat')
        0.2474424720578567
        >>> cmp.corr('Niall', 'Neil')
        0.1300991207720222
        >>> cmp.corr('aluminum', 'Catalan')
        0.011710186806836291
        >>> cmp.corr('ATCG', 'TAGC')
        -4.1196952743799446e-05


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        score = self.sim_score(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        score /= a + b + c + d

        return copysign(score, a * d - b * c)

    def sim(self, src, tar):
        """Return Pearson's normalized Chi-Squared similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Pearson's Chi-Squared similarity

        Examples
        --------
        >>> cmp = PearsonChiSquared()
        >>> cmp.corr('cat', 'hat')
        0.2474424720578567
        >>> cmp.corr('Niall', 'Neil')
        0.1300991207720222
        >>> cmp.corr('aluminum', 'Catalan')
        0.011710186806836291
        >>> cmp.corr('ATCG', 'TAGC')
        -4.1196952743799446e-05


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
