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

"""abydos.corpus._unigram_corpus.

Unigram Corpus
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from codecs import open as c_open
from collections import defaultdict, Counter
from math import log1p

__all__ = ['UnigramCorpus']


class UnigramCorpus(object):
    """Unigram corpus class.

    Largely intended for calculating inverse document frequence (IDF) from a
    large corpus of unigram (or smaller) tokens, this class encapsulates a
    dict object. Each key is a unigram token whose value is a tuple consisting
    of the number of times a term appeared and the number of distinct documents
    in which it appeared.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        corpus_text='',
        documents=0,
        word_transform=None,
        word_tokenizer=None,
    ):
        r"""Initialize UnigramCorpus.

        Parameters
        ----------
        corpus_text : str
            The corpus text as a single string
        documents : int
            The number of documents in the corpus. If equal to 0 (the default)
            then the maximum from the internal dictionary's distinct
            documents count.
        word_transform : function
            A function to apply to each term before term tokenization and
            addition to the corpus. One might use this, for example, to apply
            Soundex encoding to each term.
        word_tokenizer : _Tokenizer
            A tokenizer to apply to each sentence in order to retrieve the
            individual "word" tokens. If set to none, str.split() will be used.

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = UnigramCorpus(tqbf)


        .. versionadded:: 0.4.0

        """
        self.corpus = defaultdict(lambda: (0,0))
        self.transform = word_transform
        self.tokenizer = word_tokenizer
        self.doc_count = documents

        for word, count in Counter(corpus_text.split()).items():
            self.add_to_corpus(word, count, 1)
        self._update_doc_count()

    def _update_doc_count(self):
        if self.corpus:
            max_docs = max(self.corpus.values(), key=lambda _: _[1])[1]
            self.doc_count = max(max_docs, self.doc_count)

    def add_to_corpus(self, word, count, doc_count):
        """Add a term to the corpus, possibly after tokenization.

        Parameters
        ----------
        word : str
            Word to add to the corpus
        count : int
            Count of word appearances
        doc_count : int
            Count of distinct documents in which word appears


        .. versionadded:: 0.4.0

        """
        if self.transform is not None:
            word = self.transform(word)

        if self.tokenizer is not None:
            tokens = self.tokenizer.tokenize(word).get_counter()
            for tok in tokens:
                n = tokens[tok]*count
                prior_count, prior_doc_count = self.corpus[tok]
                self.corpus[tok] = (prior_count + n, prior_doc_count + doc_count)
        else:
            prior_count, prior_doc_count = self.corpus[word]
            self.corpus[word] = (prior_count + count, prior_doc_count + doc_count)

    def gng_importer(self, corpus_file):
        """Fill in self.corpus from a Google NGram corpus file.

        Parameters
        ----------
        corpus_file : file
            The Google NGram file from which to initialize the n-gram corpus


        .. versionadded:: 0.4.0

        """
        with c_open(corpus_file, 'r', encoding='utf-8') as gng:
            for line in gng:
                line = line.rstrip().split('\t')
                word = line[0]
                if '_' in word:
                    word = word[:word.find('_')]

                self.add_to_corpus(word, int(line[2]), int(line[3]))
            self._update_doc_count()

    def idf(self, term):
        r"""Calculate the Inverse Document Frequency of a term in the corpus.

        Parameters
        ----------
        term : str
            The term to calculate the IDF of

        Returns
        -------
        float
            The IDF

        Examples
        --------
        >>> tqbf = 'the quick brown fox jumped over the lazy dog\n\n'
        >>> tqbf += 'and then it slept\n\n and the dog ran off'
        >>> corp = UnigramCorpus(tqbf)
        >>> round(corp.idf('dog'), 10)
        0.6931471806
        >>> round(corp.idf('the'), 10)
        0.6931471806


        .. versionadded:: 0.4.0

        """
        if term in self.corpus:
            count, term_doc_count = self.corpus[term]
            print(count, term_doc_count)
            return log1p(self.doc_count / term_doc_count)
        else:
            return float('inf')


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
