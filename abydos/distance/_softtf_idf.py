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

"""abydos.distance._softtf_idf.

SoftTF-IDF similarity
"""

from collections import Counter
from math import log1p

from ._jaro_winkler import JaroWinkler
from ._token_distance import _TokenDistance
from ..corpus import UnigramCorpus

__all__ = ['SoftTFIDF']


class SoftTFIDF(_TokenDistance):
    r"""SoftTF-IDF similarity.

    For two sets X and Y and a population N, SoftTF-IDF similarity
    :cite:`Cohen:2003` is

        .. math::

            \begin{array}{ll}
            sim_{SoftTF-IDF}(X, Y) &= \sum_{w \in \{sim_{metric}(x, y) \ge
            \theta | x \in X, y \in Y \}} V(w, S) \cdot V(w, X) \cdot V(w, Y)
            \\
            \\
            V(w, S) &= \frac{V'(w, S)}{\sqrt{\sum_{w \in S} V'(w, S)^2}}
            \\
            \\
            V'(w, S) &= log(1+TF_{w,S}) \cdot log(1+IDF_w)
            \end{array}

    Notes
    -----
    One is added to both the TF & IDF values before taking the logarithm to
    ensure the logarithms do not fall to 0, which will tend to result in 0.0
    similarities even when there is a degree of matching.

    Rather than needing to exceed the threshold value, as in :cite:`Cohen:2003`
    the similarity must be greater than or equal to the threshold.

    .. versionadded:: 0.4.0

    """

    def __init__(
        self, tokenizer=None, corpus=None, metric=None, threshold=0.9, **kwargs
    ):
        """Initialize SoftTFIDF instance.

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
        threshold : float
            A threshold value, similarities above which are counted as
            soft matches, by default 0.9.
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
        super(SoftTFIDF, self).__init__(tokenizer=tokenizer, **kwargs)
        self._corpus = corpus
        self._metric = metric
        self._threshold = threshold

        if self._metric is None:
            self._metric = JaroWinkler()

    def sim(self, src, tar):
        """Return the SoftTF-IDF similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            SoftTF-IDF similarity

        Examples
        --------
        >>> cmp = SoftTFIDF()
        >>> cmp.sim('cat', 'hat')
        0.30404449697373
        >>> cmp.sim('Niall', 'Neil')
        0.20108911303601
        >>> cmp.sim('aluminum', 'Catalan')
        0.05355175631194
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        src_tok, tar_tok = self._get_tokens()

        if self._corpus is None:
            corpus = UnigramCorpus(word_tokenizer=self.params['tokenizer'])
            corpus.add_document(src)
            corpus.add_document(tar)
        else:
            corpus = self._corpus

        matches = {(tok, tok): 1.0 for tok in self._crisp_intersection()}
        sims = Counter()
        s_toks = set(self._src_only().keys())
        t_toks = set(self._tar_only().keys())
        for s_tok in s_toks:
            for t_tok in t_toks:
                sim = self._metric.sim(s_tok, t_tok)
                if sim > self._threshold:
                    sims[(s_tok, t_tok)] = sim
        for tokens, value in sims.most_common():
            if tokens[0] in s_toks and tokens[1] in t_toks:
                matches[tokens] = value
                s_toks.remove(tokens[0])
                t_toks.remove(tokens[1])

        vws_dict = {}
        vwt_dict = {}
        for token in src_tok.keys():
            vws_dict[token] = log1p(src_tok[token]) * corpus.idf(token)
        for token in tar_tok.keys():
            vwt_dict[token] = log1p(tar_tok[token]) * corpus.idf(token)

        vws_rss = sum(score ** 2 for score in vws_dict.values()) ** 0.5
        vwt_rss = sum(score ** 2 for score in vwt_dict.values()) ** 0.5

        return float(
            round(
                sum(
                    vws_dict[s_tok]
                    / vws_rss
                    * vwt_dict[t_tok]
                    / vwt_rss
                    * matches[(s_tok, t_tok)]
                    for s_tok, t_tok in matches.keys()
                ),
                14,
            )
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
