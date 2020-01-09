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

"""abydos.distance._yates_chi_squared.

Yates's Chi-Squared similarity
"""

from math import copysign

from ._token_distance import _TokenDistance

__all__ = ['YatesChiSquared']


class YatesChiSquared(_TokenDistance):
    r"""Yates's Chi-Squared similarity.

    For two sets X and Y and a population N, Yates's :math:`\chi^2` similarity
    :cite:`Yates:1934` is

        .. math::

            sim_{Yates_{\chi^2}}(X, Y) =
            \frac{|N| \cdot (||X \cap Y| \cdot
            |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|| -
            \frac{|N|}{2})^2}
            {|X| \cdot |N \setminus X| \cdot |Y| \cdot
            |N \setminus Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Yates_{\chi^2}} =
            \frac{n \cdot (|ad-bc| - \frac{n}{2})^2}{(a+b)(c+d)(a+c)(b+d)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize YatesChiSquared instance.

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
        super(YatesChiSquared, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar, signed=False):
        """Return Yates's Chi-Squared similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        signed : bool
            If True, negative correlations will carry a negative sign

        Returns
        -------
        float
            Yates's Chi-Squared similarity

        Examples
        --------
        >>> cmp = YatesChiSquared()
        >>> cmp.sim_score('cat', 'hat')
        108.37343852728468
        >>> cmp.sim_score('Niall', 'Neil')
        56.630055670871954
        >>> cmp.sim_score('aluminum', 'Catalan')
        1.8574215841854373
        >>> cmp.sim_score('ATCG', 'TAGC')
        6.960385076156687


        .. versionadded:: 0.4.0

        """
        if not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        admbc = a * d - b * c
        num = n * (abs(admbc) - n / 2) ** 2
        denom = (
            max(1, (a + b))
            * max(1, (c + d))
            * max(1, (a + c))
            * max(1, (b + d))
        )
        if num:
            score = num / denom
            if signed:
                score = copysign(score, admbc)
            return score
        return 0.0

    def sim(self, src, tar):
        """Return Yates's normalized Chi-Squared similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Yates's Chi-Squared similarity

        Examples
        --------
        >>> cmp = YatesChiSquared()
        >>> cmp.sim('cat', 'hat')
        0.18081199852082455
        >>> cmp.sim('Niall', 'Neil')
        0.08608296705052738
        >>> cmp.sim('aluminum', 'Catalan')
        0.0026563223707532654
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        score = self.sim_score(src, tar, signed=True)
        if score < 0:
            return 0.0
        norm = max(self.sim_score(src, src), self.sim_score(tar, tar))
        return score / norm


if __name__ == '__main__':
    import doctest

    doctest.testmod()
