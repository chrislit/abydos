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

"""abydos.distance._whittaker.

Whittaker distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['Whittaker']


class Whittaker(_TokenDistance):
    r"""Whittaker distance.

    For two multisets X and Y drawn from an alphabet S, Whittaker distance
    :cite:`Whittaker:1952` is

        .. math::

            sim_{Whittaker}(X, Y) =
            \frac{1}{2}\sum_{i \in S} \big| \frac{X_i}{\sum_{i \in S} X_i} -
            \frac{Y_i}{\sum_{i \in S} Y_i} \big|

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Whittaker instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.


        .. versionadded:: 0.4.0

        """
        super(Whittaker, self).__init__(tokenizer=tokenizer, **kwargs)

    def sim(self, src, tar):
        """Return the Whittaker distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Whittaker distance

        Examples
        --------
        >>> cmp = Whittaker()
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

        alphabet = self._total().keys()

        src_card = self._src_card()
        tar_card = self._tar_card()

        return 0.5 * sum(
            abs(
                self._src_tokens[tok] / src_card
                - self._tar_tokens[tok] / tar_card
            )
            for tok in alphabet
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
