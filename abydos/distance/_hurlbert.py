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

"""abydos.distance._hurlbert.

Hurlbert similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import ceil, copysign, floor

from ._token_distance import _TokenDistance

__all__ = ['Hurlbert']


class Hurlbert(_TokenDistance):
    r"""Hurlbert similarity.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    Hurlbert's coefficient of interspecific association :cite:`Hurlbert:1969`
    is

        .. math::

            sim_{Hurlbert} =
            \frac{ad-bc}{|ad-bc|} \sqrt{\frac{Obs_{\chi^2}-Min_{\chi^2}}
            {Max_{\chi^2}-Min_{\chi^2}}}

    Where:

        .. math::

            Obs_{\chi^2} = \frac{(ad-bc)^2n}{(a+b)(a+c)(b+d)(c+d)}

            Max_{\chi^2} = \frac{(a+b)(b+d)n}{(a+c)(c+d)} \textrm{ when }
            ad \geq bc

            Max_{\chi^2} = \frac{(a+b)(a+c)n}{(b+d)(c+d)} \textrm{ when }
            ad < bc \textrm{ and } a \leq d

            Max_{\chi^2} = \frac{(b+d)(c+d)n}{(a+b)(a+c)} \textrm{ when }
            ad < bc \textrm{ and } a > d

            Min_{\chi^2} = \frac{n^3 (\hat{a} - g(\hat{a}))^2}
            {(a+b)(a+c)(c+d)(b+d)}

            \textrm{where } \hat{a} = \frac{(a+b)(a+c)}{n}

            \textrm{and } g(\hat{a}) = \lfloor\hat{a}\rfloor
            \textrm{ when } ad < bc
            \textrm{, otherwise } g(\hat{a}) = \lceil\hat{a}\rceil

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Hurlbert instance.

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
        super(Hurlbert, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Hurlbert similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Hurlbert similarity

        Examples
        --------
        >>> cmp = Hurlbert()
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

        admbc = a * d - b * c
        marginals_product = (a + b) * (a + c) * (b + d) * (c + d)

        obs_chisq = admbc ** 2 * n / marginals_product
        if a * d >= b * c:
            max_chisq = (a + b) * (b + d) * n / ((a + c) * (c + d))
        elif a <= d:
            max_chisq = (a + b) * (a + c) * n / ((b + d) * (c + d))
        else:
            max_chisq = (b + d) * (c + d) * n / ((a + b) * (a + c))

        a_hat = (a + b) * (a + c) / n
        g_a_hat = ceil(a_hat) if a * d < b * c else floor(a_hat)

        min_chisq = n ** 2 * (a_hat - g_a_hat) ** 2 / marginals_product

        return copysign(
            ((obs_chisq - min_chisq) / (max_chisq - min_chisq)) ** 0.5, admbc
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
