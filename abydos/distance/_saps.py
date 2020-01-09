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

"""abydos.distance._saps_alignment.

Syllable Alignment Pattern Searching tokenizer
"""

from numpy import int as np_int
from numpy import zeros as np_zeros

from ._distance import _Distance
from ..tokenizer import SAPSTokenizer

__all__ = ['SAPS']


class SAPS(_Distance):
    """Syllable Alignment Pattern Searching tokenizer.

    This is the alignment and similarity calculation described on p. 917-918 of
    :cite:`Ruibin:2005`.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        cost=(1, -1, -4, 6, -2, -1, -3),
        normalizer=max,
        tokenizer=None,
        **kwargs
    ):
        """Initialize SAPS instance.

        Parameters
        ----------
        cost : tuple
            A 7-tuple representing the cost of the four possible matches:

                - syllable-internal match
                - syllable-internal mis-match
                - syllable-initial match or mismatch with syllable-internal
                - syllable-initial match
                - syllable-initial mis-match
                - syllable-internal gap
                - syllable-initial gap

            (by default: (1, -1, -4, 6, -2, -1, -3))
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(SAPS, self).__init__(**kwargs)
        self._s1, self._s2, self._s3, self._s4, self._s5 = cost[:5]
        self._g1, self._g2 = cost[5:]

        self._normalizer = normalizer
        if tokenizer is None:
            self._tokenizer = SAPSTokenizer()
        else:
            self._tokenizer = tokenizer

    def _s(self, src, tar):
        if src.isupper():
            if tar.isupper():
                return self._s4 if src == tar else self._s5
            else:
                return self._s3
        else:
            if tar.islower():
                return self._s1 if src == tar else self._s2
            else:
                return self._s3

    def _g(self, ch):
        if ch.isupper():
            return self._g2
        else:
            return self._g1

    def sim_score(self, src, tar):
        """Return the SAPS similarity between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The SAPS similarity between src & tar

        Examples
        --------
        >>> cmp = SAPS()
        >>> cmp.sim_score('cat', 'hat')
        0
        >>> cmp.sim_score('Niall', 'Neil')
        3
        >>> cmp.sim_score('aluminum', 'Catalan')
        -11
        >>> cmp.sim_score('ATCG', 'TAGC')
        -1
        >>> cmp.sim_score('Stevenson', 'Stinson')
        16


        .. versionadded:: 0.4.0

        """
        src = self._tokenizer.tokenize(src).get_list()
        tar = self._tokenizer.tokenize(tar).get_list()

        src = ''.join([_[0].upper() + _[1:].lower() for _ in src])
        tar = ''.join([_[0].upper() + _[1:].lower() for _ in tar])

        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_int)
        for i in range(len(src)):
            d_mat[i + 1, 0] = d_mat[i, 0] + self._g(src[i])
        for j in range(len(tar)):
            d_mat[0, j + 1] = d_mat[0, j] + self._g(tar[j])

        for i in range(len(src)):
            for j in range(len(tar)):
                d_mat[i + 1, j + 1] = max(
                    d_mat[i, j + 1] + self._g(src[i]),  # ins
                    d_mat[i + 1, j] + self._g(tar[j]),  # del
                    d_mat[i, j] + self._s(src[i], tar[j]),  # sub/==
                )

        return d_mat[len(src), len(tar)]

    def sim(self, src, tar):
        """Return the normalized SAPS similarity between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized SAPS similarity between src & tar

        Examples
        --------
        >>> cmp = SAPS()
        >>> round(cmp.sim('cat', 'hat'), 12)
        0.0
        >>> round(cmp.sim('Niall', 'Neil'), 12)
        0.2
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        score = self.sim_score(src, tar)
        if score <= 0:
            return 0.0

        src = self._tokenizer.tokenize(src).get_list()
        src_max = sum(5 + len(_) for _ in src)
        tar = self._tokenizer.tokenize(tar).get_list()
        tar_max = sum(5 + len(_) for _ in tar)

        return score / max(src_max, tar_max)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
