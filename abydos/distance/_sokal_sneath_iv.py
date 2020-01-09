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

"""abydos.distance._sokal_sneath_iv.

Sokal & Sneath IV similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['SokalSneathIV']


class SokalSneathIV(_TokenDistance):
    r"""Sokal & Sneath IV similarity.

    For two sets X and Y and a population N, Sokal & Sneath IV similarity
    :cite:`Sokal:1963` is

        .. math::

            sim_{SokalSneathIV}(X, Y) =
            \frac{1}{4}\Bigg(
            \frac{|X \cap Y|}{|X|}+
            \frac{|X \cap Y|}{|Y|}+
            \frac{|(N \setminus X) \setminus Y|}
            {|N \setminus Y|}+
            \frac{|(N \setminus X) \setminus Y|}
            {|N \setminus X|}
            \Bigg)

    This is the fourth of five "Unnamed coefficients" presented in
    :cite:`Sokal:1963`. It corresponds to the first "Marginal totals in the
    Denominator" with "Negative Matches in Numerator Included".
    "Negative Matches in Numerator Excluded" corresponds to the Kulczynski II
    similarity, :class:`.KulczynskiII`. This is also Rogot & Goldberg's
    "adjusted agreement" :math:`A_1` :cite:`Rogot:1966`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{SokalSneathIV} =
            \frac{1}{4}\Big(\frac{a}{a+b}+\frac{a}{a+c}+
            \frac{d}{b+d}+\frac{d}{c+d}\Big)

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize SokalSneathIV instance.

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
        super(SokalSneathIV, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Sokal & Sneath IV similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Sokal & Sneath IV similarity

        Examples
        --------
        >>> cmp = SokalSneathIV()
        >>> cmp.sim('cat', 'hat')
        0.7487179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.6810856260030602
        >>> cmp.sim('aluminum', 'Catalan')
        0.5541986205645999
        >>> cmp.sim('ATCG', 'TAGC')
        0.496790757381258


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        a_part = 0 if a == 0 else (a / (a + b) + a / (a + c))
        d_part = 0 if d == 0 else (d / (b + d) + d / (c + d))

        return 0.25 * (a_part + d_part)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
