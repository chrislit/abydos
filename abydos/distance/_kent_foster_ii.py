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

"""abydos.distance._kent_foster_ii.

Kent & Foster II similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['KentFosterII']


class KentFosterII(_TokenDistance):
    r"""Kent & Foster II similarity.

    For two sets X and Y and a population N, Kent & Foster II similarity
    :cite:`Kent:1977`, :math:`K_{nonocc}`, is

        .. math::

            sim_{KentFosterII}(X, Y) =
            \frac{|(N \setminus X) \setminus Y| -
            \frac{|X \setminus Y|\cdot|Y \setminus X|}
            {|N \setminus (X \cap Y)|}}
            {|(N \setminus X) \setminus Y| -
            \frac{|X \setminus Y|\cdot|Y \setminus X|}
            {|N \setminus (X \cap Y)|} +
            |X \setminus Y| + |Y \setminus X|}

    Kent & Foster derived this from Cohen's :math:`\kappa` by "subtracting
    appropriate chance agreement correction figures from the numerators and
    denominators" to arrive at an non-occurrence reliability measure.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{KentFosterII} =
            \frac{d-\frac{(b+d)(c+d)}{b+c+d}}{d-\frac{(b+d)(c+d)}{b+c+d}+b+c}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize KentFosterII instance.

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
        super(KentFosterII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Kent & Foster II similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kent & Foster II similarity

        Examples
        --------
        >>> cmp = KentFosterII()
        >>> cmp.sim_score('cat', 'hat')
        -0.0012804097311239404
        >>> cmp.sim_score('Niall', 'Neil')
        -0.002196997436837158
        >>> cmp.sim_score('aluminum', 'Catalan')
        -0.004784688995214218
        >>> cmp.sim_score('ATCG', 'TAGC')
        -0.0031989763275758767


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        num = (b + d) * (c + d)
        if not num:
            bigterm = d
        else:
            bigterm = d - (num / (b + c + d))

        if bigterm:
            return bigterm / (bigterm + b + c)
        return 0.0

    def sim(self, src, tar):
        """Return the normalized Kent & Foster II similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Kent & Foster II similarity

        Examples
        --------
        >>> cmp = KentFosterII()
        >>> cmp.sim('cat', 'hat')
        0.998719590268876
        >>> cmp.sim('Niall', 'Neil')
        0.9978030025631628
        >>> cmp.sim('aluminum', 'Catalan')
        0.9952153110047858
        >>> cmp.sim('ATCG', 'TAGC')
        0.9968010236724241


        .. versionadded:: 0.4.0

        """
        return 1.0 + self.sim_score(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
