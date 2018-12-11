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

"""abydos.distance._fuzzy_dice.

Fuzzy Dice similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._fuzzy_tversky import FuzzyTversky
__all__ = ['FuzzyDice']


class FuzzyDice(FuzzyTversky):
    r"""Fuzzy Dice similarity.

    For two sets X and Y, the Fuzzy Dice similarity :cite:`Wang:2014` is:
    :math:`sim_{Fuzzy Dice_\delta}(X, Y) = \frac{2 \cdot |X \widetilde\cap_\delta Y|}{|X| + |Y|}`,
    where :math:`|X \widetilde\cap_\delta Y|` is the fuzzy overlap or fuzzy
    intersection. This fuzzy intersection is sum of similarities of all tokens
    in the two sets that are greater than equal to some threshold value
    (:math:`\delta`).

    The lower bound of Fuzzy Dice similarity, and the value when
    :math:`\delta = 1.0`, is the Dice similarity. Tokens shorter than
    :math:`\frac{\delta}{1-\delta}`, 4 in the case of the default threshold
    :math:`\delta = 0.8`, must match exactly to contribute to similarity.

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, threshold=0.8, metric=None, **kwargs):
        """Initialize FuzzyDice instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the abydos.tokenizer package
        threshold : float
            The minimum similarity for a pair of tokens to contribute to
            similarity
        metric : _Distance
            A distance instance from the abydos.distance package, defaulting
            to normalized Levenshtein similarity
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
        super(FuzzyDice, self).__init__(
            alpha=0.5, beta=0.5, bias=None, tokenizer=tokenizer, threshold=threshold, metric=metric, **kwargs
        )

    def sim(self, src, tar):
        """Return the Fuzzy Dice similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fuzzy Dice similarity

        Examples
        --------
        >>> cmp = FuzzyDice()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.36363636363636365
        >>> cmp.sim('aluminum', 'Catalan')
        0.11764705882352941
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        .. versionadded:: 0.4.0

        """
        return super(FuzzyDice, self).sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
