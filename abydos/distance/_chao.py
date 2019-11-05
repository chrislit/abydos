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

"""abydos.distance._chao.

Chao similarity
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

__all__ = ['Chao']


class Chao(_TokenDistance):
    r"""Chao similarity.

    Chao similarity :cite:`Chao:2004`

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize Chao instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(Chao, self).__init__(**kwargs)

    def sim(self, src, tar):
        """Return the Chao similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Chao similarity

        Examples
        --------
        >>> cmp = Chao()
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

        src_tok = self._src_tokens
        tar_tok = self._tar_tokens

        alphabet = set(src_tok.keys() | tar_tok.keys())
        shared = self._intersection().keys()

        src_card = self._src_card()  # n
        tar_card = self._tar_card()  # m

        tar_token_list = self.params['tokenizer'].get_list()
        src_token_list = self.params['tokenizer'].tokenize(src).get_list()

        src_sampled = Counter(sample(src_token_list, src_card))
        tar_sampled = Counter(sample(tar_token_list, tar_card))
        sample_intersection = src_sampled & tar_sampled
        unseen_shared_species = shared - set(sample_intersection)

        f_1_plus = sum(
            1 if src_sampled[tok] == 1 and tar_sampled[tok] >= 1 else 0
            for tok in sample_intersection
        )
        f_2_plus = sum(
            1 if src_sampled[tok] == 2 and tar_sampled[tok] >= 1 else 0
            for tok in sample_intersection
        )
        f_plus_1 = sum(
            1 if src_sampled[tok] >= 1 and tar_sampled[tok] == 1 else 0
            for tok in sample_intersection
        )
        f_plus_2 = sum(
            1 if src_sampled[tok] >= 1 and tar_sampled[tok] == 2 else 0
            for tok in sample_intersection
        )

        """
        tar_prob = Counter()
        src_prob = Counter()

        for tok in shared:
            src_prob[tok] = src_tok[tok] / src_card
            tar_prob[tok] = tar_tok[tok] / tar_card

        U = sum(src_prob.values())
        V = sum(tar_prob.values())

        #return U*V/(U+V-U*V)
        """
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
