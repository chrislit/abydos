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

"""abydos.distance._gilbert_wells.

Gilbert & Wells similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import factorial, log, pi

from ._token_distance import _TokenDistance

__all__ = ['GilbertWells']


class GilbertWells(_TokenDistance):
    r"""Gilbert & Wells similarity.

    For two sets X and Y and a population N, the Gilbert & Wells
    similarity :cite:`Gilbert:1966` is

        .. math::

            sim_{GilbertWells}(X, Y) =
            ln \frac{|N|^3}{2\pi |X| \cdot |Y| \cdot
            |N \setminus Y| \cdot |N \setminus X|} + 2ln
            \frac{|N|! \cdot |X \cap Y|! \cdot |X \setminus Y|! \cdot
            |Y \setminus X|! \cdot |(N \setminus X) \setminus Y|!}
            {|X|! \cdot |Y|! \cdot |N \setminus Y|! \cdot |N \setminus X|!}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{GilbertWells} =
            ln \frac{n^3}{2\pi (a+b)(a+c)(b+d)(c+d)} +
            2ln \frac{n!a!b!c!d!}{(a+b)!(a+c)!(b+d)!(c+d)!}

    Most lists of similarity & distance measures, including
    :cite:`Hubalek:1982,Choi:2010,Morris:2012` have a quite different formula,
    which would be :math:`ln a - ln b - ln \frac{a+b}{n} - ln \frac{a+c}{n} =
    ln\frac{an}{(a+b)(a+c)}`. However, neither this formula nor anything
    similar or equivalent to it appears anywhere within the cited work,
    :cite:`Gilbert:1966`.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize GilbertWells instance.

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
        super(GilbertWells, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Gilbert & Wells similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gilbert & Wells similarity

        Examples
        --------
        >>> cmp = GilbertWells()
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
        n = self._population_unique_card()

        return log(
            n ** 3 / (2 * pi * (a + b) * (a + c) * (b + d) * (c + d))
        ) + 2 * (
            log(factorial(n))
            + log(factorial(a))
            + log(factorial(b))
            + log(factorial(c))
            + log(factorial(d))
            - log(factorial(a + b))
            - log(factorial(a + c))
            - log(factorial(b + d))
            - log(factorial(c + d))
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
