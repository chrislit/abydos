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

"""abydos.distance._pearson_ii.

Pearson II similarity
"""

from ._pearson_chi_squared import PearsonChiSquared

__all__ = ['PearsonII']


class PearsonII(PearsonChiSquared):
    r"""Pearson II similarity.

    For two sets X and Y and a population N, the Pearson II
    similarity :cite:`Pearson:1913`, Pearson's coefficient of mean square
    contingency, is

        .. math::

            corr_{PearsonII} = \sqrt{\frac{\chi^2}{|N|+\chi^2}}

    where

        .. math::

            \chi^2 = sim_{PearsonChiSquared}(X, Y) =
            \frac{|N| \cdot (|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)^2}
            {|X| \cdot |Y| \cdot |N \setminus X| \cdot |N \setminus Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            \chi^2 = sim_{PearsonChiSquared} =
            \frac{n \cdot (ad-bc)^2}{(a+b)(a+c)(b+d)(c+d)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize PearsonII instance.

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
        super(PearsonII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Pearson II similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson II similarity

        Examples
        --------
        >>> cmp = PearsonII()
        >>> cmp.sim_score('cat', 'hat')
        0.44537605041688455
        >>> cmp.sim_score('Niall', 'Neil')
        0.3392961347892176
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.10758552665334761
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.006418353030552324


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 2 ** 0.5 / 2
        chi2 = super(PearsonII, self).sim_score(src, tar)
        return (chi2 / (self._population_unique_card() + chi2)) ** 0.5

    def sim(self, src, tar):
        """Return the normalized Pearson II similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Pearson II similarity

        Examples
        --------
        >>> cmp = PearsonII()
        >>> cmp.sim('cat', 'hat')
        0.6298568508557214
        >>> cmp.sim('Niall', 'Neil')
        0.47983719547968123
        >>> cmp.sim('aluminum', 'Catalan')
        0.15214891090821628
        >>> cmp.sim('ATCG', 'TAGC')
        0.009076921903905551


        .. versionadded:: 0.4.0

        """
        return self.sim_score(src, tar) * 2 / 2 ** 0.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
