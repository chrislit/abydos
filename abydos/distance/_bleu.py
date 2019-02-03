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

"""abydos.distance._bleu.

BLEU similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import exp, log

from ._distance import _Distance
from ..tokenizer import QGrams

__all__ = ['BLEU']


class BLEU(_Distance):
    r"""BLEU similarity.

    BLEU similarity
    :cite:`Papineni:2002`

    .. versionadded:: 0.4.0
    """

    def __init__(self, n_min=1, n_max=4, **kwargs):
        """Initialize BLEU instance.

        Parameters
        ----------
        n_min : int
            The minimum q-gram value for BLEU score calculation (1 by default)
        n_max : int
            The maximum q-gram value for BLEU score calculation (4 by default)
        **kwargs
            Arbitrary keyword arguments

        .. versionadded:: 0.4.0

        """
        super(BLEU, self).__init__(**kwargs)
        self._n_min = n_min
        self._n_max = n_max

    def sim(self, src, tar):
        """Return the BLEU similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            BLEU similarity

        Examples
        --------
        >>> cmp = BLEU()
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
        brevity_penalty = (
            1.0 if len(tar) >= len(src) else exp(1 - len(src) / len(tar))
        )

        bleu_sum = 0.0
        n_grams = list(range(self._n_min, self._n_max + 1))

        for n in n_grams:
            tokenizer = QGrams(qval=n, start_stop='')
            src_tokens = tokenizer.tokenize(src).get_counter()
            tar_tokens = tokenizer.tokenize(tar).get_counter()
            tar_total = sum(tar_tokens.values())

            bleu_sum += log(
                sum(
                    min(src_tokens[tok], tar_tokens[tok]) for tok in tar_tokens
                )
                / tar_total
            ) / len(n_grams)

        return brevity_penalty * exp(bleu_sum)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
