# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.distance._gwet_gamma.

Gwet's Gamma similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['GwetGamma']


class GwetGamma(_TokenDistance):
    r"""Gwet's Gamma similarity.

    For two sets X and Y and a population N, Gwet's \gamma similarity
    :cite:`Gwet:2008` is

        .. math::

            sim_{Gwet_\gamma}(X, Y) = \gamma =
            \frac{p_o - p_e^\gamma}{1 - p_e^\gamma}

    where

        .. math::

            p_o = \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}{|N|}

            p_e^\gamma = \Big(\frac{\frac{|X|}{|N|}+\frac{|Y|}{|N|}}{2}\Big)
            \cdot \Big(\frac{\frac{|N \setminus Y|}{|N|}+
            \frac{|N \setminus X|}{|N|}}{2}\Big)

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            p_o = \frac{a+d}{n}

            p_e^\gamma = \Big(\frac{\frac{a+b}{n}+\frac{a+c}{n}}{2}\Big) \cdot
            \Big(\frac{\frac{b+d}{n}+\frac{c+d}{n}}{2}\Big)

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize GwetGamma instance.

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
            A string distance measure class for use in the 'soft' and 'fuzzy'
            variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the 'fuzzy' variant.


        .. versionadded:: 0.4.0

        """
        super(GwetGamma, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Gwet's Gamma similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gwet's Gamma similarity

        Examples
        --------
        >>> cmp = GwetGamma()
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
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        return (2 * a ** 2 - b ** 2 - 2 * b * c - c ** 2 + 2 * d ** 2) / (
            2 * a ** 2
            + 2 * a * (b + c)
            + b ** 2
            + 2 * b * (c + d)
            + c ** 2
            + 2 * d * (c + d)
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
