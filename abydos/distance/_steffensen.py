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

"""abydos.distance._steffensen.

Steffensen similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['Steffensen']


class Steffensen(_TokenDistance):
    r"""Steffensen similarity.

    For two sets X and Y and a population N, Steffensen similarity
    :cite:`Steffensen:1934` is

        .. math::

            sim_{Steffensen}(X, Y) =
            \frac{\frac{|X \cap Y|}{|N|} \cdot (\frac{|X \cap Y|}{|N|}-
            \frac{|X|}{|N|} \cdot \frac{|Y|}{|N|})^2}
            {\frac{|X|}{|N|} \cdot (1-\frac{|X|}{|N|}) \cdot \frac{|Y|}{|N|}
            \cdot (1-\frac{|Y|}{|N|})}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    after each term has been converted to a proportion by dividing by n, this
    is

        .. math::

            sim_{Steffensen} =
            \frac{a(a-(a+b)(a+c))^2}{(a+b)(1-(a+b))(a+c)(1-(a+c))}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        normalizer='proportional',
        **kwargs
    ):
        """Initialize Steffensen instance.

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
        normalizer : str
            Specifies the normalization type. See :ref:`normalizer <alphabet>`
            description in :py:class:`_TokenDistance` for details.
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
        super(Steffensen, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            normalizer=normalizer,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Steffensen similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Steffensen similarity

        Examples
        --------
        >>> cmp = Steffensen()
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

        return (
            a
            * (a - (a + b) * (a + c)) ** 2
            / ((a + b) * (1 - (a + b)) * (a + c) * (1 - (a + c)))
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
