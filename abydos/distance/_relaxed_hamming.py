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

"""abydos.distance._discounted_hamming.

Relaxed Hamming distance
"""

from ._distance import _Distance
from ..tokenizer import QGrams

__all__ = ['RelaxedHamming']


class RelaxedHamming(_Distance):
    """Relaxed Hamming distance.

    This is a variant of Hamming distance in which positionally close matches
    are considered partially matching.

    .. versionadded:: 0.4.1
    """

    def __init__(self, tokenizer=None, maxdist=2, discount=0.2, **kwargs):
        """Initialize DiscountedHamming instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        maxdist : int
            The maximum distance to consider for discounting.
        discount : float
            The discount factor multiplied by the distance from the source
            string position.
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.


        .. versionadded:: 0.4.1

        """
        super(RelaxedHamming, self).__init__(**kwargs)

        self.params['tokenizer'] = tokenizer
        if 'qval' in self.params:
            self.params['tokenizer'] = QGrams(
                qval=self.params['qval'], start_stop='$#', skip=0, scaler=None
            )
        self._maxdist = maxdist
        self._discount = discount

    def dist_abs(self, src, tar):
        """Return the discounted Hamming distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Relaxed Hamming distance

        Examples
        --------
        >>> cmp = RelaxedHamming()
        >>> cmp.dist_abs('cat', 'hat')
        1.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.4
        >>> cmp.dist_abs('aluminum', 'Catalan')
        6.4
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.8


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 0

        if len(src) != len(tar):
            replacement_char = 1
            while chr(replacement_char) in src or chr(replacement_char) in tar:
                replacement_char += 1
            replacement_char = chr(replacement_char)
            if len(src) < len(tar):
                src += replacement_char * (len(tar) - len(src))
            else:
                tar += replacement_char * (len(src) - len(tar))

        if self.params['tokenizer']:
            src = self.params['tokenizer'].tokenize(src).get_list()
            tar = self.params['tokenizer'].tokenize(tar).get_list()

        score = 0
        for pos in range(len(src)):
            if src[pos] == tar[pos : pos + 1][0]:
                continue

            try:
                diff = (
                    tar[pos + 1 : pos + self._maxdist + 1].index(src[pos]) + 1
                )
            except ValueError:
                diff = 0
            try:
                found = (
                    tar[max(0, pos - self._maxdist) : pos][::-1].index(
                        src[pos]
                    )
                    + 1
                )
            except ValueError:
                found = 0

            if found and diff:
                diff = min(diff, found)
            elif found:
                diff = found

            if diff:
                score += min(1.0, self._discount * diff)
            else:
                score += 1.0

        return score

    def dist(self, src, tar):
        """Return the normalized relaxed Hamming distance between strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized relaxed Hamming distance

        Examples
        --------
        >>> cmp = RelaxedHamming()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.27999999999999997
        >>> cmp.dist('aluminum', 'Catalan')
        0.8
        >>> cmp.dist('ATCG', 'TAGC')
        0.2


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 0.0
        score = self.dist_abs(src, tar)

        if self.params['tokenizer']:
            src = self.params['tokenizer'].tokenize(src).get_list()
            tar = self.params['tokenizer'].tokenize(tar).get_list()

        return score / max(len(src), len(tar))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
