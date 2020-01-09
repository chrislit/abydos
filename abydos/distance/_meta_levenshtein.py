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

"""abydos.distance._meta_levenshtein.

Meta-Levenshtein distance
"""

from collections import Counter
from math import log1p

from numpy import float as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance
from ._jaro_winkler import JaroWinkler
from ..corpus import UnigramCorpus
from ..tokenizer import QGrams, WhitespaceTokenizer

__all__ = ['MetaLevenshtein']


class MetaLevenshtein(_Distance):
    r"""Meta-Levenshtein distance.

    Meta-Levenshtein distance :cite:`Moreau:2008` combines Soft-TFIDF with
    Levenshtein alignment.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        tokenizer=None,
        corpus=None,
        metric=None,
        normalizer=max,
        **kwargs
    ):
        """Initialize MetaLevenshtein instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        corpus : UnigramCorpus
            A unigram corpus :py:class:`UnigramCorpus`. If None, a corpus will
            be created from the two words when a similarity function is called.
        metric : _Distance
            A string distance measure class for making soft matches, by default
            Jaro-Winkler.
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
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
        super(MetaLevenshtein, self).__init__(**kwargs)
        self._corpus = corpus
        self._metric = metric
        self._normalizer = normalizer

        qval = 2 if 'qval' not in self.params else self.params['qval']
        self.params['tokenizer'] = (
            tokenizer
            if tokenizer is not None
            else WhitespaceTokenizer()
            if qval == 0
            else QGrams(qval=qval, start_stop='$#', skip=0, scaler=None)
        )

        if self._metric is None:
            self._metric = JaroWinkler()

    def dist_abs(self, src, tar):
        """Return the Meta-Levenshtein distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Meta-Levenshtein distance

        Examples
        --------
        >>> cmp = MetaLevenshtein()
        >>> cmp.dist_abs('cat', 'hat')
        0.6155602628882225
        >>> cmp.dist_abs('Niall', 'Neil')
        2.538900657220556
        >>> cmp.dist_abs('aluminum', 'Catalan')
        6.940747163450747
        >>> cmp.dist_abs('ATCG', 'TAGC')
        3.2311205257764453


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0
        if not src:
            return float(len(tar))
        if not tar:
            return float(len(src))

        src_tok = self.params['tokenizer'].tokenize(src)
        src_ordered = src_tok.get_list()
        src_tok = src_tok.get_counter()

        tar_tok = self.params['tokenizer'].tokenize(tar)
        tar_ordered = tar_tok.get_list()
        tar_tok = tar_tok.get_counter()

        if self._corpus is None:
            corpus = UnigramCorpus(word_tokenizer=self.params['tokenizer'])
            corpus.add_document(src)
            corpus.add_document(tar)
        else:
            corpus = self._corpus

        dists = Counter()
        s_toks = set(src_tok.keys())
        t_toks = set(tar_tok.keys())
        for s_tok in s_toks:
            for t_tok in t_toks:
                dists[(s_tok, t_tok)] = (
                    self._metric.dist(s_tok, t_tok) if s_tok != t_tok else 0
                )

        vws_dict = {}
        vwt_dict = {}
        for token in src_tok.keys():
            vws_dict[token] = log1p(src_tok[token]) * corpus.idf(token)
        for token in tar_tok.keys():
            vwt_dict[token] = log1p(tar_tok[token]) * corpus.idf(token)

        def _dist(s_tok, t_tok):
            return dists[(s_tok, t_tok)] * vws_dict[s_tok] * vwt_dict[t_tok]

        d_mat = np_zeros(
            (len(src_ordered) + 1, len(tar_ordered) + 1), dtype=np_float
        )
        for i in range(len(src_ordered) + 1):
            d_mat[i, 0] = i
        for j in range(len(tar_ordered) + 1):
            d_mat[0, j] = j

        for i in range(len(src_ordered)):
            for j in range(len(tar_ordered)):
                d_mat[i + 1, j + 1] = min(
                    d_mat[i + 1, j] + 1,  # ins
                    d_mat[i, j + 1] + 1,  # del
                    d_mat[i, j]
                    + _dist(src_ordered[i], tar_ordered[j]),  # sub/==
                )

        return d_mat[len(src_ordered), len(tar_ordered)]

    def dist(self, src, tar):
        """Return the normalized Levenshtein distance between two strings.

        The Levenshtein distance is normalized by dividing the Levenshtein
        distance (calculated by any of the three supported methods) by the
        greater of the number of characters in src times the cost of a delete
        and the number of characters in tar times the cost of an insert.
        For the case in which all operations have :math:`cost = 1`, this is
        equivalent to the greater of the length of the two strings src & tar.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Levenshtein distance between src & tar

        Examples
        --------
        >>> cmp = MetaLevenshtein()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.205186754296
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.507780131444
        >>> cmp.dist('aluminum', 'Catalan')
        0.8675933954313434
        >>> cmp.dist('ATCG', 'TAGC')
        0.8077801314441113


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0

        return self.dist_abs(src, tar) / (
            self._normalizer(
                [
                    self.dist_abs(src, ' ' * len(tar)),
                    self.dist_abs(src, ' ' * len(src)),
                ]
            )
            if self._corpus
            else self._normalizer([len(src), len(tar)])
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
