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

"""abydos.distance._minhash.

MinHash similarity
"""

from hashlib import sha512

import numpy as np

from ._distance import _Distance
from ..tokenizer import QGrams, WhitespaceTokenizer

__all__ = ['MinHash']


_MININT = np.iinfo(np.int64).min
_MAXINT = np.iinfo(np.int64).max


class MinHash(_Distance):
    r"""MinHash similarity.

    MinHash similarity :cite:`Broder:1997` is a method of approximating the
    intersection over the union of two sets. This implementation is based on
    :cite:`Kula:2015`.

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, k=0, seed=10, **kwargs):
        """Initialize MinHash instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        k : int
            The number of hash functions to use for similarity estimation
        seed : int
            A seed value for the random functions
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
        self._k = k
        self._seed = seed
        super(MinHash, self).__init__(tokenizer=tokenizer, **kwargs)

        qval = 2 if 'qval' not in self.params else self.params['qval']
        self.params['tokenizer'] = (
            tokenizer
            if tokenizer is not None
            else WhitespaceTokenizer()
            if qval == 0
            else QGrams(qval=qval, start_stop='$#', skip=0, scaler=None)
        )

    def sim(self, src, tar):
        """Return the MinHash similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            MinHash similarity

        Examples
        --------
        >>> cmp = MinHash()
        >>> cmp.sim('cat', 'hat')
        0.75
        >>> cmp.sim('Niall', 'Neil')
        1.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.5
        >>> cmp.sim('ATCG', 'TAGC')
        0.6


        .. versionadded:: 0.4.0

        """
        if not src and not tar:
            return 1.0

        src_tokens = self.params['tokenizer'].tokenize(src).get_set()
        tar_tokens = self.params['tokenizer'].tokenize(tar).get_set()

        k = self._k if self._k else max(len(src_tokens), len(tar_tokens))

        masks = np.random.RandomState(seed=self._seed).randint(
            _MININT, _MAXINT, k, dtype=np.int64
        )

        hashes_src = np.full(k, _MAXINT, dtype=np.int64)
        hashes_tar = np.full(k, _MAXINT, dtype=np.int64)

        for tok in src_tokens:
            hashes_src = np.minimum(
                hashes_src,
                np.bitwise_xor(
                    masks, int(sha512(tok.encode()).hexdigest(), 16)
                ),
            )

        for tok in tar_tokens:
            hashes_tar = np.minimum(
                hashes_tar,
                np.bitwise_xor(
                    masks, int(sha512(tok.encode()).hexdigest(), 16)
                ),
            )

        return (hashes_src == hashes_tar).sum() / k


if __name__ == '__main__':
    import doctest

    doctest.testmod()
