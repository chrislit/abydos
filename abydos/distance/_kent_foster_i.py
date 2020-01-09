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

"""abydos.distance._kent_foster_i.

Kent & Foster I similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['KentFosterI']


class KentFosterI(_TokenDistance):
    r"""Kent & Foster I similarity.

    For two sets X and Y and a population N, Kent & Foster I similarity
    :cite:`Kent:1977`, :math:`K_{occ}`, is

        .. math::

            sim_{KentFosterI}(X, Y) =
            \frac{|X \cap Y| - \frac{|X|\cdot|Y|}{|X \cup Y|}}
            {|X \cap Y| - \frac{|X|\cdot|Y|}{|X \cup Y|} +
            |X \setminus Y| + |Y \setminus X|}

    Kent & Foster derived this from Cohen's :math:`\kappa` by "subtracting
    appropriate chance agreement correction figures from the numerators and
    denominators" to arrive at an occurrence reliability measure.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{KentFosterI} =
            \frac{a-\frac{(a+b)(a+c)}{a+b+c}}{a-\frac{(a+b)(a+c)}{a+b+c}+b+c}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize KentFosterI instance.

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
        super(KentFosterI, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Kent & Foster I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kent & Foster I similarity

        Examples
        --------
        >>> cmp = KentFosterI()
        >>> cmp.sim_score('cat', 'hat')
        -0.19999999999999996
        >>> cmp.sim_score('Niall', 'Neil')
        -0.23529411764705888
        >>> cmp.sim_score('aluminum', 'Catalan')
        -0.30434782608695654
        >>> cmp.sim_score('ATCG', 'TAGC')
        -0.3333333333333333


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        num = (a + b) * (a + c)
        if not num:
            bigterm = a
        else:
            bigterm = a - (num / (a + b + c))

        if bigterm:
            return bigterm / (bigterm + b + c)
        return 0.0

    def sim(self, src, tar):
        """Return the normalized Kent & Foster I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Kent & Foster I similarity

        Examples
        --------
        >>> cmp = KentFosterI()
        >>> cmp.sim('cat', 'hat')
        0.8
        >>> cmp.sim('Niall', 'Neil')
        0.7647058823529411
        >>> cmp.sim('aluminum', 'Catalan')
        0.6956521739130435
        >>> cmp.sim('ATCG', 'TAGC')
        0.6666666666666667


        .. versionadded:: 0.4.0

        """
        return 1.0 + self.sim_score(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
