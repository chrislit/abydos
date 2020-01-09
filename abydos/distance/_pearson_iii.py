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

"""abydos.distance._pearson_iii.

Pearson III correlation
"""

from math import copysign

from ._pearson_phi import PearsonPhi

__all__ = ['PearsonIII']


class PearsonIII(PearsonPhi):
    r"""Pearson III correlation.

    For two sets X and Y and a population N, the Pearson III
    correlation :cite:`Pearson:1913`, Pearson's coefficient of racial likeness,
    is

        .. math::

            corr_{PearsonIII} = \sqrt{\frac{\phi}{|N|+\phi}}

    where

        .. math::

            \phi = corr_{PearsonPhi}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {\sqrt{|X| \cdot |Y| \cdot |N \setminus X| \cdot |N \setminus Y|}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            \phi = corr_{PearsonPhi} =
            \frac{ad-bc}
            {\sqrt{(a+b)(a+c)(b+c)(b+d)}}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize PearsonIII instance.

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
        super(PearsonIII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Pearson III correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson III correlation

        Examples
        --------
        >>> cmp = PearsonIII()
        >>> cmp.corr('cat', 'hat')
        0.025180989806958435
        >>> cmp.corr('Niall', 'Neil')
        0.021444241017487504
        >>> cmp.corr('aluminum', 'Catalan')
        0.011740218922356615
        >>> cmp.corr('ATCG', 'TAGC')
        -0.0028612777635371113


        .. versionadded:: 0.4.0

        """
        phi = super(PearsonIII, self).corr(src, tar)
        return copysign(
            (abs(phi) / (self._population_unique_card() + phi)) ** 0.5, phi
        )

    def sim(self, src, tar):
        """Return the Pearson III similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson III similarity

        Examples
        --------
        >>> cmp = PearsonIII()
        >>> cmp.sim('cat', 'hat')
        0.5125904949034792
        >>> cmp.sim('Niall', 'Neil')
        0.5107221205087438
        >>> cmp.sim('aluminum', 'Catalan')
        0.5058701094611783
        >>> cmp.sim('ATCG', 'TAGC')
        0.49856936111823147


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
