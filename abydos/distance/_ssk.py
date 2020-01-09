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

"""abydos.distance._ssk.

String subsequence kernel (SSK) similarity
"""

from ._token_distance import _TokenDistance
from ..tokenizer import QSkipgrams

__all__ = ['SSK']


class SSK(_TokenDistance):
    r"""String subsequence kernel (SSK) similarity.

    This is based on :cite:`Lodhi:2002`.


    .. versionadded:: 0.4.1
    """

    def __init__(self, tokenizer=None, ssk_lambda=0.9, **kwargs):
        """Initialize SSK instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        ssk_lambda : float or Iterable
            A value in the range (0.0, 1.0) used for discouting gaps between
            characters according to the method described in :cite:`Lodhi:2002`.
            To supply multiple values of lambda, provide an Iterable of numeric
            values, such as (0.5, 0.05) or np.arange(0.05, 0.5, 0.05)
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-skipgram. Using this parameter and
            tokenizer=None will cause the instance to use the QGramskipgrams
            tokenizer with this q value.


        .. versionadded:: 0.4.1

        """
        super(SSK, self).__init__(
            tokenizer=tokenizer, ssk_lambda=ssk_lambda, **kwargs
        )

        qval = 2 if 'qval' not in self.params else self.params['qval']
        self.params['tokenizer'] = (
            tokenizer
            if tokenizer is not None
            else QSkipgrams(
                qval=qval, start_stop='', scaler='SSK', ssk_lambda=ssk_lambda
            )
        )

    def sim_score(self, src, tar):
        """Return the SSK similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            String subsequence kernel similarity

        Examples
        --------
        >>> cmp = SSK()
        >>> cmp.dist_abs('cat', 'hat')
        0.6441281138790036
        >>> cmp.dist_abs('Niall', 'Neil')
        0.5290992177869402
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.862398428061774
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.38591004719395017


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        src_wts = self._src_tokens
        tar_wts = self._tar_tokens

        score = sum(
            src_wts[token] * tar_wts[token] for token in src_wts & tar_wts
        )

        return score

    def sim(self, src, tar):
        """Return the normalized SSK similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized string subsequence kernel similarity

        Examples
        --------
        >>> cmp = SSK()
        >>> cmp.sim('cat', 'hat')
        0.3558718861209964
        >>> cmp.sim('Niall', 'Neil')
        0.4709007822130597
        >>> cmp.sim('aluminum', 'Catalan')
        0.13760157193822603
        >>> cmp.sim('ATCG', 'TAGC')
        0.6140899528060498


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        src_wts = self._src_tokens
        tar_wts = self._tar_tokens

        score = sum(
            src_wts[token] * tar_wts[token] for token in src_wts & tar_wts
        )

        norm = (
            sum(src_wts[token] * src_wts[token] for token in src_wts)
            * sum(tar_wts[token] * tar_wts[token] for token in tar_wts)
        ) ** 0.5

        if not score:
            return 0.0
        return score / norm


if __name__ == '__main__':
    import doctest

    doctest.testmod()
