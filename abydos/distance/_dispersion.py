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

"""abydos.distance._dispersion.

Dispersion correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['Dispersion']


class Dispersion(_TokenDistance):
    r"""Dispersion correlation.

    For two sets X and Y and a population N, the dispersion
    correlation :cite:`IBM:2017` is

        .. math::

            corr_{dispersion}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {|N|^2}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{dispersion} =
            \frac{ad-bc}{n^2}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Dispersion instance.

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
        super(Dispersion, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Dispersion correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Dispersion correlation

        Examples
        --------
        >>> cmp = Dispersion()
        >>> cmp.corr('cat', 'hat')
        0.002524989587671803
        >>> cmp.corr('Niall', 'Neil')
        0.002502212619741774
        >>> cmp.corr('aluminum', 'Catalan')
        0.0011570449105440383
        >>> cmp.corr('ATCG', 'TAGC')
        -4.06731570179092e-05


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        admbc = a * d - b * c
        if admbc == 0.0:
            return 0.0
        return admbc / n ** 2

    def sim(self, src, tar):
        """Return the Dispersion similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Dispersion similarity

        Examples
        --------
        >>> cmp = Dispersion()
        >>> cmp.sim('cat', 'hat')
        0.5012624947938359
        >>> cmp.sim('Niall', 'Neil')
        0.5012511063098709
        >>> cmp.sim('aluminum', 'Catalan')
        0.500578522455272
        >>> cmp.sim('ATCG', 'TAGC')
        0.499979663421491


        .. versionadded:: 0.4.0

        """
        return (1 + self.corr(src, tar)) / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
