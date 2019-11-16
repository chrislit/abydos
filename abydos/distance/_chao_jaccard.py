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

"""abydos.distance._chao_jaccard.

Chao's Jaccard similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter
from random import sample

from ._token_distance import _TokenDistance

__all__ = ['ChaoJaccard']


class ChaoJaccard(_TokenDistance):
    r"""Chao's Jaccard similarity.

    Chao's Jaccard similarity :cite:`Chao:2004`

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize ChaoJaccard instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(ChaoJaccard, self).__init__(**kwargs)

    def sim(self, src, tar):
        """Return Chao's Jaccard similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Chao's Jaccard similarity

        Examples
        --------
        >>> cmp = ChaoJaccard()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        u_hat, v_hat = self._get_estimates(src, tar)

        num = u_hat * v_hat
        if num:
            return num / (u_hat + v_hat - u_hat * v_hat)
        return 0.0

    def _get_estimates(self, src, tar):
        """Get the estimates U-hat & V-hat used for Chao's measures.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        tuple(float, float)
            The estimates U-hat & V-hat

        .. versionadded:: 0.4.1

        """
        src_card = self._src_card()  # n
        tar_card = self._tar_card()  # m

        src_token_list = self.params['tokenizer'].tokenize(src).get_list()
        tar_token_list = self.params['tokenizer'].tokenize(tar).get_list()

        src_sampled = Counter(sample(src_token_list, src_card))
        tar_sampled = Counter(sample(tar_token_list, tar_card))
        sample_intersection = src_sampled & tar_sampled

        f_1_plus = sum(
            1 if src_sampled[tok] == 1 and tar_sampled[tok] >= 1 else 0
            for tok in sample_intersection
        )
        f_2_plus = max(
            sum(
                1 if src_sampled[tok] == 2 and tar_sampled[tok] >= 1 else 0
                for tok in sample_intersection
            ),
            1,
        )
        f_plus_1 = sum(
            1 if src_sampled[tok] >= 1 and tar_sampled[tok] == 1 else 0
            for tok in sample_intersection
        )
        f_plus_2 = max(
            sum(
                1 if src_sampled[tok] >= 1 and tar_sampled[tok] == 2 else 0
                for tok in sample_intersection
            ),
            1,
        )

        u_hat = 0
        if src_card:
            u_hat += sum(
                src_sampled[tok] / src_card
                for tok in sample_intersection.keys()
            )
        if tar_card:
            u_hat += (
                (tar_card - 1)
                / tar_card
                * f_plus_1
                / (2 * f_plus_2)
                * sum(
                    src_sampled[tok] / src_card * (tar_sampled[tok] == 1)
                    for tok in sample_intersection.keys()
                )
            )

        v_hat = 0
        if tar_card:
            v_hat += sum(
                tar_sampled[tok] / tar_card
                for tok in sample_intersection.keys()
            )
        if src_card:
            v_hat += (
                (src_card - 1)
                / src_card
                * f_1_plus
                / (2 * f_2_plus)
                * sum(
                    tar_sampled[tok] / tar_card * (src_sampled[tok] == 1)
                    for tok in sample_intersection.keys()
                )
            )

        return u_hat, v_hat


if __name__ == '__main__':
    import doctest

    doctest.testmod()