# -*- coding: utf-8 -*-

# Copyright 2018-2019 by Christopher C. Little.
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

"""abydos.distance._pearson_phi.

Pearson's Phi
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['PearsonPhi']


class PearsonPhi(_TokenDistance):
    r"""Pearson's Phi.

    For two sets X and Y and a population N, the Pearson's :math:`\phi`
    similarity :cite:`Pearson:1900,Pearson:1913,Guilford:1956` is

        .. math::

            sim_{PearsonPhi}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {\sqrt{|X| \cdot |Y| \cdot |N \setminus X| \cdot |N \setminus Y|}}

    This is also Pearson & Heron I similarity.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{PearsonPhi} =
            \frac{ad-bc}
            {\sqrt{(a+b)(a+c)(b+d)(c+d)}}

    Notes
    -----
    In terms of a confusion matrix, this is equivalent to the Matthews
    correlation coefficient :py:meth:`ConfusionTable.mcc`.

    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize PearsonPhi instance.

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
        super(PearsonPhi, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return Pearson's Phi of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson's Phi

        Examples
        --------
        >>> cmp = PearsonPhi()
        >>> cmp.corr('cat', 'hat')
        0.0
        >>> cmp.corr('Niall', 'Neil')
        0.0
        >>> cmp.corr('aluminum', 'Catalan')
        0.0
        >>> cmp.corr('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        ab = self._src_card()
        ac = self._tar_card()

        return (a * d - b * c) / (ab * ac * (b + d) * (c + d)) ** 0.5

    def sim(self, src, tar):
        """Return the normalized Pearson's Phi similarity of two strings.

        This is normalized to [0, 1] by adding 1 and dividing by 2.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson's Phi similarity

        Examples
        --------
        >>> cmp = PearsonPhi()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (self.corr(src, tar) + 1) / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
