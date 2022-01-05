# Copyright 2019-2022 by Christopher C. Little.
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

import pickle  # noqa: S403
from codecs import open as c_open
from collections import Counter, defaultdict
from math import log1p
from typing import Any, Callable, DefaultDict, Optional, Tuple

from ..tokenizer import _Tokenizer

__all__ = ['UnigramCorpus']


def _dd_default(*args: Any) -> Tuple[int, int]:
    return 0, 0


class UnigramCorpus:
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
        corpus_text: str = '',
        documents: int = 0,
        word_transform: Optional[Callable[[str], str]] = None,
        word_tokenizer: Optional[_Tokenizer] = None,
    ) -> None:
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
        self.corpus = defaultdict(
            _dd_default
        )  # type: DefaultDict[str, Tuple[int, int]]
        self.transform = word_transform
        self.tokenizer = word_tokenizer
        self.doc_count = documents

        self.add_document(corpus_text)

    def add_document(self, doc: str) -> None:
        """Add a new document to the corpus.

        Parameters
        ----------
        doc : str
            A string, representing the document to be added.


        .. versionadded:: 0.4.0

        """
        for word, count in Counter(doc.split()).items():
            self._add_word(word, count, 1)
        self.doc_count += 1

    def save_corpus(self, filename: str) -> None:
        """Save the corpus to a file.

        This employs pickle to save the corpus (a defaultdict). Other
        parameters of the corpus, such as its word_tokenizer, will not be
        affected and should be set during initialization.

        Parameters
        ----------
        filename : str
            The filename to save the corpus to.


        .. versionadded:: 0.4.0

        """
        with open(filename, mode='wb') as pkl:
            pickle.dump(self.corpus, pkl)

    def load_corpus(self, filename: str) -> None:
        """Load the corpus from a file.

        This employs pickle to load the corpus (a defaultdict). Other
        parameters of the corpus, such as its word_tokenizer, will not be
        affected and should be set during initialization.

        Parameters
        ----------
        filename : str
            The filename to load the corpus from.


        .. versionadded:: 0.4.0

        """
        with open(filename, mode='rb') as pkl:
            self.corpus = pickle.load(pkl)  # noqa: S301
        self._update_doc_count()

    def _update_doc_count(self) -> None:
        """Update document count, if necessary.

        .. versionadded:: 0.4.0
        """
        max_docs = max(self.corpus.values(), key=lambda _: _[1])[1]
        self.doc_count = max(max_docs, self.doc_count)

    def _add_word(self, word: str, count: int, doc_count: int) -> None:
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
            self.tokenizer.tokenize(word)
            tokens = self.tokenizer.get_counter()
            for tok in tokens:
                n = tokens[tok] * count
                prior_count, prior_doc_count = self.corpus[tok]
                self.corpus[tok] = (
                    prior_count + n,
                    prior_doc_count + doc_count,
                )
        else:
            prior_count, prior_doc_count = self.corpus[word]
            self.corpus[word] = (
                prior_count + count,
                prior_doc_count + doc_count,
            )

    def gng_importer(self, corpus_file: str) -> None:
        """Fill in self.corpus from a Google NGram corpus file.

        Parameters
        ----------
        corpus_file : file
            The Google NGram file from which to initialize the n-gram corpus


        .. versionadded:: 0.4.0

        """
        with c_open(corpus_file, 'r', encoding='utf-8') as gng:
            for line in gng:
                word, _, count, doc_count = line.rstrip().split('\t')
                if '_' in word:
                    word = word[: word.find('_')]

                self._add_word(word, int(count), int(doc_count))
            self._update_doc_count()

    def idf(self, term: str) -> float:
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
            return log1p(self.doc_count / term_doc_count)
        else:
            return float('inf')


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
