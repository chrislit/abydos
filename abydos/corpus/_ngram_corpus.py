# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.corpus._ngram_corpus.

The NGram class is a container for an n-gram corpus
"""

from codecs import open as c_open
from collections import Counter
from typing import Any, Counter as TCounter, List, Optional, Union, cast

from ._corpus import Corpus

__all__ = ['NGramCorpus']


class NGramCorpus:
    """The NGramCorpus class.

    Internally, this is a set of recursively embedded dicts, with n layers for
    a corpus of n-grams. E.g. for a trigram corpus, this will be a dict of
    dicts of dicts. More precisely, ``collections.Counter`` is used in place of
    dict, making multiset operations valid and allowing unattested n-grams to
    be queried.

    The key at each level is a word. The value at the most deeply embedded
    level is a numeric value representing the frequency of the trigram. E.g.
    the trigram frequency of 'colorless green ideas' would be the value stored
    in ``self.ngcorpus['colorless']['green']['ideas'][None]``.

    .. versionadded:: 0.3.0
    """

    def __init__(self, corpus: Optional[Corpus] = None) -> None:
        r"""Initialize Corpus.

        Parameters
        ----------
        corpus : Corpus
            The :py:class:`Corpus` from which to initialize the n-gram corpus.
            By default, this is None, which initializes an empty NGramCorpus.
            This can then be populated using NGramCorpus methods.

        Raises
        ------
        TypeError
            Corpus argument must be None or of type abydos.Corpus

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> ngcorp = NGramCorpus(Corpus(tqbf))


        .. versionadded:: 0.3.0

        """
        self.ngcorpus = Counter()  # type: TCounter[Optional[str]]

        if corpus is None:
            return
        elif isinstance(corpus, Corpus):
            self.corpus_importer(corpus)
        else:
            raise TypeError(
                f'Corpus argument must be None or of type abydos.corpus.Corpus.'
                f' {type(corpus)} found.'
            )

    def corpus_importer(
        self,
        corpus: Corpus,
        n_val: int = 1,
        bos: str = '_START_',
        eos: str = '_END_',
    ) -> None:
        r"""Fill in self.ngcorpus from a Corpus argument.

        Parameters
        ----------
        corpus : Corpus
            The Corpus from which to initialize the n-gram corpus
        n_val : int
            Maximum n value for n-grams
        bos : str
            String to insert as an indicator of beginning of sentence
        eos : str
            String to insert as an indicator of end of sentence

        Raises
        ------
        TypeError
            Corpus argument of the Corpus class required.

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> ngcorp = NGramCorpus()
        >>> ngcorp.corpus_importer(Corpus(tqbf))


        .. versionadded:: 0.3.0

        """
        if not corpus or not isinstance(corpus, Corpus):
            raise TypeError('Corpus argument of the Corpus class required.')

        sentences = corpus.sents()

        for sent in sentences:
            ngs = Counter(sent)
            for key in ngs.keys():
                self._add_to_ngcorpus(self.ngcorpus, [key], ngs[key])

            if n_val > 1:
                if bos and bos != '':
                    sent = [bos] + sent
                if eos and eos != '':
                    sent += [eos]
                for i in range(2, n_val + 1):
                    for j in range(len(sent) - i + 1):
                        self._add_to_ngcorpus(
                            self.ngcorpus, sent[j : j + i], 1
                        )

    def get_count(
        self,
        ngram: Union[str, List[str]],
        corpus: Optional[TCounter[Optional[str]]] = None,
    ) -> int:
        r"""Get the count of an n-gram in the corpus.

        Parameters
        ----------
        ngram : str or List[str]
            The n-gram to retrieve the count of from the n-gram corpus
        corpus : Counter[str] or None
            The corpus

        Returns
        -------
        int
            The n-gram count

        Examples
        --------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> ngcorp = NGramCorpus(Corpus(tqbf))
        >>> ngcorp.get_count('the')
        2
        >>> ngcorp.get_count('fox')
        1


        .. versionadded:: 0.3.0

        """
        if not corpus:
            corpus = self.ngcorpus

        # if ngram is empty, we're at our leaf node and should return the
        # value in None
        if not ngram:
            return corpus[None]

        # support strings or lists/tuples by splitting strings
        if isinstance(ngram, str):
            ngram = ngram.split()

        # if ngram is not empty, check whether the next element is in the
        # corpus; if so, recurse--if not, return 0
        if ngram[0] in corpus:
            return self.get_count(
                ngram[1:],
                cast(Optional[TCounter[Optional[str]]], corpus[ngram[0]]),
            )
        return 0

    def _add_to_ngcorpus(
        self, corpus: Any, words: List[str], count: int
    ) -> None:
        """Build up a corpus entry recursively.

        Parameters
        ----------
        corpus : Corpus or counter
            The corpus
        words : [str]
            Words to add to the corpus
        count : int
            Count of words


        .. versionadded:: 0.3.0

        """
        if words[0] not in corpus:
            corpus[words[0]] = Counter()

        if len(words) == 1:
            corpus[words[0]][None] += count
        else:
            self._add_to_ngcorpus(corpus[words[0]], words[1:], count)

    def gng_importer(self, corpus_file: str) -> None:
        """Fill in self.ngcorpus from a Google NGram corpus file.

        Parameters
        ----------
        corpus_file : str
            The filename of the Google NGram file from which to initialize the
            n-gram corpus


        .. versionadded:: 0.3.0

        """
        with c_open(corpus_file, 'r', encoding='utf-8') as gng:
            for line in gng:
                line_parts = line.rstrip().split('\t')
                words = line_parts[0].split()

                self._add_to_ngcorpus(self.ngcorpus, words, int(line_parts[2]))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
