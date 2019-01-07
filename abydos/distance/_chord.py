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

"""abydos.distance._chord.

Chord distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['Chord']


class Chord(_TokenDistance):
    r"""Chord distance.

    For two sets X and Y, the chord distance :cite:`Orloci:1967` is

        .. math::

            sim_{chord}(X, Y) =
            \sqrt{2\Big(1-\frac{|X \cap Y|}{\sqrt{|X| \cdot |Y|}}\Big)}

    In 2x2 matrix, a+b+c+d=n terms, this is

        .. math::

            sim_{chord} =
            \sqrt{2\Big(1-\frac{a}{\sqrt{(a+b)(a+c}}\Big)}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Chord instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:

                - 'crisp': Ordinary intersection, wherein items are entirely
                  members or non-members of the intersection. (Default)
                - 'fuzzy': Fuzzy intersection, defined by :cite:`Wang:2014`,
                  wherein items can be partially members of the intersection
                  if their similarity meets or exceeds a threshold value. This
                  also takes `metric` (by default :class:`Levenshtein()`) and
                  `threshold` (by default 0.8) parameters.
                - 'soft': Soft intersection, defined by :cite:`Russ:2014`,
                  wherein items can be partially members of the intersection
                  depending on their similarity. This also takes a `metric`
                  (by default :class:`DamerauLevenshtein()`) parameter.
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
        super(Chord, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def dist(self, src, tar):
        """Return the Chord distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Chord distance

        Examples
        --------
        >>> cmp = Chord()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self.tokenize(src, tar)

        a = self.intersection_card()
        ab = self.src_card()
        ac = self.tar_card()

        return (2 * (1 - (a / (ab * ac) ** 0.5))) ** 0.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
