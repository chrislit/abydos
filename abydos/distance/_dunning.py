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

"""abydos.distance._dunning.

Dunning similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from ._token_distance import _TokenDistance

__all__ = ['Dunning']


class Dunning(_TokenDistance):
    r"""Dunning similarity.

    For two sets X and Y and a population N, Dunning log-likelihood
    :cite:`Dunning:1993`, following :cite:`Church:1991`, is

        .. math::

            sim_{Dunning}(X, Y) = \lambda =
            |N| log_2(|N|) + |X \cap Y| log_2(|X \cap Y|) +
            |X \setminus Y| log_2(|X \setminus Y|) +
            |Y \setminus X| log_2(|Y \setminus X|) +
            |(N \setminus X) \setminus Y| log_2(|(N \setminus X) \setminus Y|) -
            (|X| log_2(|X|) + |Y| log_2(|Y|) +
            |N \setminus Y| log_2(|N \setminus Y|) +
            |N \setminus X| log_2(|N \setminus X|)) +


    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Dunning} = \lambda =
            n log_2(n) + a log_2(a) + b log_2(b) + c log_2(c) + d log_2(d) -
            ((a+b) log_2(a+b) + (a+c) log_2(a+c) + (b+d) log_2(b+d) +
            (c+d) log_2(c+d))

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Dunning instance.

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
        super(Dunning, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Dunning similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Dunning similarity

        Examples
        --------
        >>> cmp = Dunning()
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

        return (
            (a + b + c + d) * log(a + b + c + d)
            + (a * log(a) + b * log(b) + c * log(c) + d * log(d))
            - (
                (a + b) * log(a + b)
                + (a + c) * log(a + c)
                + (b + d) * log(b + d)
                + (c + d) * log(c + d)
            )
        ) / log(2)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
