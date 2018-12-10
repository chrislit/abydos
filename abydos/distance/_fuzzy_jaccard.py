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

"""abydos.distance._fuzzy_jaccard.

Fuzzy Jaccard similarity coefficient, distance, & Fuzzy Tanimoto coefficient
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from ._fuzzy_tversky import FuzzyTversky

__all__ = ['FuzzyJaccard']


class FuzzyJaccard(FuzzyTversky):
    r"""Fuzzy Jaccard similarity.

    For two sets X and Y, the Jaccard similarity coefficient
    :cite:`Jaccard:1901` is :math:`sim_{Jaccard}(X, Y) =
    \frac{|X \cap Y|}{|X \cup Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958`
    and the Tversky index :cite:`Tversky:1977` for
    :math:`\alpha = \beta = 1`.

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, threshold=0.8, metric=None, **kwargs):
        """Initialize FuzzyJaccard instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the abydos.tokenizer package
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
        super(FuzzyJaccard, self).__init__(
            alpha=1, beta=1, bias=None, tokenizer=tokenizer, threshold=threshold, metric=metric, **kwargs
        )

    def sim(self, src, tar):
        r"""Return the fuzzy Jaccard similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fuzzy Jaccard similarity

        Examples
        --------
        >>> cmp = FuzzyJaccard()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        .. versionadded:: 0.4.0

        """
        return super(FuzzyJaccard, self).sim(src, tar)

    def tanimoto_coeff(self, src, tar):
        """Return the Fuzzy Tanimoto distance between two strings.

        Tanimoto distance :cite:`Tanimoto:1958` is
        :math:`-log_{2} sim_{Tanimoto}(X, Y)`.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fuzzy Tanimoto distance

        Examples
        --------
        >>> cmp = FuzzyJaccard()
        >>> cmp.tanimoto_coeff('cat', 'hat')
        -1.5849625007211563
        >>> cmp.tanimoto_coeff('Niall', 'Neil')
        -2.1699250014423126
        >>> cmp.tanimoto_coeff('aluminum', 'Catalan')
        -4.0
        >>> cmp.tanimoto_coeff('ATCG', 'TAGC')
        -inf

        .. versionadded:: 0.4.0

        """
        coeff = self.sim(src, tar)
        if coeff != 0:
            return log(coeff, 2)

        return float('-inf')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
