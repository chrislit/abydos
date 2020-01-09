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

"""abydos.distance._positional_q_gram_overlap.

Positional Q-Gram Overlap coefficient
"""

from collections import defaultdict

from ._distance import _Distance
from ..tokenizer import QGrams, WhitespaceTokenizer

__all__ = ['PositionalQGramOverlap']


class PositionalQGramOverlap(_Distance):
    r"""Positional Q-Gram Overlap coefficient.

    Positional Q-Gram Overlap coefficient :cite:`Gravano:2001,Christen:2006`

    .. versionadded:: 0.4.0
    """

    def __init__(self, max_dist=1, tokenizer=None, **kwargs):
        """Initialize PositionalQGramOverlap instance.

        Parameters
        ----------
        max_dist : int
            The maximum positional distance between to q-grams to count as a
            match.
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
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
        super(PositionalQGramOverlap, self).__init__(
            tokenizer=tokenizer, **kwargs
        )
        self._max_dist = max_dist

        qval = 2 if 'qval' not in self.params else self.params['qval']
        self.params['tokenizer'] = (
            tokenizer
            if tokenizer is not None
            else WhitespaceTokenizer()
            if qval == 0
            else QGrams(qval=qval, start_stop='$#', skip=0, scaler=None)
        )

    def sim(self, src, tar):
        """Return the Positional Q-Gram Overlap coefficient of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Positional Q-Gram Overlap coefficient

        Examples
        --------
        >>> cmp = PositionalQGramOverlap()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.4
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        src_list = self.params['tokenizer'].tokenize(src).get_list()
        tar_list = self.params['tokenizer'].tokenize(tar).get_list()

        src_pos = defaultdict(list)
        tar_pos = defaultdict(list)

        intersection = 0

        for pos in range(len(src_list)):
            src_pos[src_list[pos]].append(pos)
        for pos in range(len(tar_list)):
            tar_pos[tar_list[pos]].append(pos)

        src_matched = []
        tar_matched = []

        for tok in src_pos:
            if tok in tar_pos:
                for sp in src_pos[tok]:
                    for tp in tar_pos[tok]:
                        if (
                            abs(sp - tp) <= self._max_dist
                            and sp not in src_matched
                            and tp not in tar_matched
                        ):
                            intersection += 1
                            src_matched.append(sp)
                            tar_matched.append(tp)

        denom = min(len(src_list), len(tar_list))

        return intersection / denom


if __name__ == '__main__':
    import doctest

    doctest.testmod()
