# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._scott_pi.

Scott's Pi similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['ScottPi']


class ScottPi(_TokenDistance):
    r"""Scott's Pi similarity.

    For two sets X and Y and a population N, Scott's \pi similarity
    :cite:`Scott:1955` is

        .. math::

            sim_{Scott_\pi}(X, Y) = \pi =
            \frac{p_o - p_e^\pi}{1 - p_e^\pi}

    where

        .. math::

            p_o = \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}{|N|}

            p_e^\pi = \Big(\frac{\frac{|X|}{|N|} + \frac{|Y|}{|N|}}{2}\Big)^2 +
            \Big(\frac{\frac{|N \setminus X|}{|N|} +
            \frac{|N \setminus Y|}{|N|}}{2}\Big)^2


    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            p_o = \frac{a+d}{n}

            p_e^\pi = \Big(\frac{\frac{a+b}{n} + \frac{a+c}{n}}{2}\Big)^2 +
            \Big(\frac{\frac{b+d}{n} + \frac{c+d}{n}}{2}\Big)^2


    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize ScottPi instance.

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
        super(ScottPi, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Scott's Pi similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Scott's Pi similarity

        Examples
        --------
        >>> cmp = ScottPi()
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

        return (4 * a * d - b * b - 2 * b * c - c * c) / (
            (2 * a + b + c) * (2 * d + b + c)
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
