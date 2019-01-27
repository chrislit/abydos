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

"""abydos.distance._tf_idf.

TF-IDF similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from ._token_distance import _TokenDistance
from ..corpus import UnigramCorpus

__all__ = ['TFIDF']


class TFIDF(_TokenDistance):
    r"""TF-IDF similarity.

    For two sets X and Y and a population N, TF-IDF similarity
    :cite:`CITATION` is

        .. math::

            sim_{TFIDF}(X, Y) =

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{TFIDF} =

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        tokenizer=None,
        intersection_type='crisp',
        corpus=None,
        **kwargs
    ):
        """Initialize TFIDF instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        corpus : UnigramCorpus
            A unigram corpus :py:class:`UnigramCorpus`. If None, a corpus will
            be created from the two words when a similarity function is called.
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
        super(TFIDF, self).__init__(
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )
        self._corpus = corpus

    def sim(self, src, tar):
        """Return the TF-IDF similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            TF-IDF similarity

        Examples
        --------
        >>> cmp = TFIDF()
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
        self._tokenize(src, tar)

        src_tok, tar_tok = self._get_tokens()

        if self._corpus is None:
            corpus = UnigramCorpus()
            for word, count in src_tok.items():
                corpus.add_to_corpus(word, count, 1)
            for word, count in tar_tok.items():
                corpus.add_to_corpus(word, count, 1)
        else:
            corpus = self._corpus

        vws_dict = {}
        vwt_dict = {}
        for token in self._intersection().keys():
            vws_dict[token] = (1+log(src_tok[token])) * corpus.idf(token)
            vwt_dict[token] = (1+log(tar_tok[token])) * corpus.idf(token)

        vws_rss = sum(score**2 for score in vws_dict.values())**0.5
        vwt_rss = sum(score**2 for score in vwt_dict.values())**0.5

        return sum(vws_dict[token]/vws_rss * vwt_dict[token]/vwt_rss for token in self._intersection().keys())


if __name__ == '__main__':
    import doctest

    doctest.testmod()
