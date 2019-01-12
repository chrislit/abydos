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

"""abydos.distance._koppen_i.

Köppen I similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['KoppenI']


class KoppenI(_TokenDistance):
    r"""Köppen I similarity.

    For two sets X and Y and an alphabet N, provided that :math:`|X| = |Y|`,
    Köppen I similarity :cite:`Koppen:1870,Goodman:1959` is

        .. math::

            sim_{KoppenI}(X, Y) =
            \frac{|X| \cdot |N \setminus X| - |X \setminus Y|}
            {|X| \cdot |N \setminus X|}

    To support cases where :math:`|X| \neq |Y|`, this class implements a slight
    variation, while still providing the expected results when
    :math:`|X| = |Y|`:

        .. math::

            sim_{KoppenI}(X, Y) =
            \frac{\frac{|X|+|Y|}{2} \cdot
            \frac{|N \setminus X|+|N \setminus Y|}{2}-
            \frac{|X \triangle Y|}{2}}
            {\frac{|X|+|Y|}{2} \cdot
            \frac{|N \setminus X|+|N \setminus Y|}{2}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{KoppenI} =
            \frac{\frac{2a+b+c}{2} \cdot (n-\frac{2a+b+c}{2})-
            \frac{b+c}{2}}
            {\frac{2a+b+c}{2} \cdot (n-\frac{2a+b+c}{2}}

    Note
    ----

    In the usual case all of the above values should be proportional to the
    total number of samples n. I.e., a, b, c, d, & n should all be divided by
    n prior to calculating the coefficient. This class's default normalizer
    is, accordingly, 'proportional'.

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
        """Initialize KoppenI instance.

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
        super(KoppenI, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            normalizer=normalizer,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Köppen I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Köppen I similarity

        Examples
        --------
        >>> cmp = KoppenI()
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
        self.tokenize(src, tar)

        a = self.intersection_card()
        b = self.src_only_card()
        c = self.tar_only_card()
        n = self.population_card()

        abac_mean = (2 * a + b + c) / 2

        return (abac_mean * (n - abac_mean) - (b + c) / 2) / (
            abac_mean * (n - abac_mean)
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
