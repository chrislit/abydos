# Copyright 2019-2020 by Christopher C. Little.
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

from math import exp, log

from ._distance import _Distance
from ..tokenizer import QGrams

__all__ = ['BLEU']


class BLEU(_Distance):
    r"""BLEU similarity.

    BLEU similarity :cite:`Papineni:2002` compares two strings for similarity
    using a set of tokenizers and a brevity penalty:

        .. math::

            BP =
            \left\{
            \begin{array}{lrl}
                1 & \textup{if} & c > r \\
                e^{(1-\frac{r}{c})} & \textup{if} & c \leq r
            \end{array}
            \right.

    The BLEU score is then:

        .. math::

            \textup{B\textsc{leu}} = BP \cdot e^{\sum_{n=1}^N w_n log p_n}

    For tokenizers 1 to N, by default q-gram tokenizers for q=1 to N in
    Abydos, weights :math:`w_n`, which are uniformly :math:`\frac{1}{N}`,
    and :math:`p_n`:

        .. math::

            p_n = \frac{\sum_{token \in tar} min(Count(token \in tar),
            Count(token \in src))}{|tar|}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self, n_min=1, n_max=4, tokenizers=None, weights=None, **kwargs
    ):
        """Initialize BLEU instance.

        Parameters
        ----------
        n_min : int
            The minimum q-gram value for BLEU score calculation (1 by default)
        n_max : int
            The maximum q-gram value for BLEU score calculation (4 by default)
        tokenizers : list(_Tokenizer)
            A list of initialized tokenizers
        weights : list(float)
            A list of floats representing the weights of the tokenizers. If
            tokenizers is set, this must have the same length. If n_min and
            n_max are used to set tokenizers, this must have length equal to
            n_max-n_min-1. Otherwise, uniform weights will be used.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(BLEU, self).__init__(**kwargs)
        self._tokenizers = (
            [QGrams(qval=n, start_stop='') for n in range(n_min, n_max + 1)]
            if tokenizers is None
            else tokenizers
        )
        self._weights = weights
        if not weights or len(weights) != len(self._tokenizers):
            self._weights = [
                1.0 / len(self._tokenizers)
                for _ in range(len(self._tokenizers))
            ]

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
        0.7598356856515925
        >>> cmp.sim('Niall', 'Neil')
        0.7247557929987696
        >>> cmp.sim('aluminum', 'Catalan')
        0.44815260192961937
        >>> cmp.sim('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        if not src or not tar:
            return 0.0

        brevity_penalty = (
            1.0 if len(tar) >= len(src) else exp(1 - len(src) / len(tar))
        )

        bleu_sum = 0.0
        bleu_null = True

        for i in range(len(self._tokenizers)):
            tar_tokens = self._tokenizers[i].tokenize(tar).get_counter()
            tokens_int = (
                self._tokenizers[i].tokenize(src).get_counter() & tar_tokens
            )
            tar_total = sum(tar_tokens.values())

            if tokens_int:
                bleu_null = False
                bleu_sum += (
                    log(sum(tokens_int.values()) / tar_total)
                    * self._weights[i]
                )

        if bleu_null:
            return 0.0

        return brevity_penalty * exp(bleu_sum)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
