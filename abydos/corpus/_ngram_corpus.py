# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from codecs import open as c_open
from collections import Counter
from math import log10

from six import text_type
from six.moves import range

from ._corpus import Corpus

__all__ = ['NGramCorpus']


class NGramCorpus(object):
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
    """

    def __init__(self, corpus=None):
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

        """
        self.ngcorpus = Counter()

        if corpus is None:
            return
        elif isinstance(corpus, Corpus):
            self.corpus_importer(corpus)
        else:
            raise TypeError(
                'Corpus argument must be None or of type abydos.Corpus. '
                + str(type(corpus))
                + ' found.'
            )

    def corpus_importer(self, corpus, n_val=1, bos='_START_', eos='_END_'):
        r"""Fill in self.ngcorpus from a Corpus argument.

        Parameters
        ----------
        corpus :Corpus
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

    def get_count(self, ngram, corpus=None):
        r"""Get the count of an n-gram in the corpus.

        Parameters
        ----------
        ngram : str
            The n-gram to retrieve the count of from the n-gram corpus
        corpus : Corpus
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
        >>> NGramCorpus(Corpus(tqbf)).get_count('the')
        2
        >>> NGramCorpus(Corpus(tqbf)).get_count('fox')
        1

        """
        if not corpus:
            corpus = self.ngcorpus

        # if ngram is empty, we're at our leaf node and should return the
        # value in None
        if not ngram:
            return corpus[None]

        # support strings or lists/tuples by splitting strings
        if isinstance(ngram, (text_type, str)):
            ngram = text_type(ngram).split()

        # if ngram is not empty, check whether the next element is in the
        # corpus; if so, recurse--if not, return 0
        if ngram[0] in corpus:
            return self.get_count(ngram[1:], corpus[ngram[0]])
        return 0

    def _add_to_ngcorpus(self, corpus, words, count):
        """Build up a corpus entry recursively.

        Parameters
        ----------
        corpus : Corpus
            The corpus
        words : [str]
            Words to add to the corpus
        count : int
            Count of words

        """
        if words[0] not in corpus:
            corpus[words[0]] = Counter()

        if len(words) == 1:
            corpus[words[0]][None] += count
        else:
            self._add_to_ngcorpus(corpus[words[0]], words[1:], count)

    def gng_importer(self, corpus_file):
        """Fill in self.ngcorpus from a Google NGram corpus file.

        Parameters
        ----------
        corpus_file : file
            The Google NGram file from which to initialize the n-gram corpus

        """
        with c_open(corpus_file, 'r', encoding='utf-8') as gng:
            for line in gng:
                line = line.rstrip().split('\t')
                words = line[0].split()

                self._add_to_ngcorpus(self.ngcorpus, words, int(line[2]))

    def tf(self, term):
        r"""Return term frequency.

        Parameters
        ----------
        term : str
            The term for which to calculate tf

        Returns
        -------
        float
            The term frequency (tf)

        Raises
        ------
        ValueError
            tf can only calculate the frequency of individual words

        Examples
        --------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> ngcorp = NGramCorpus(Corpus(tqbf))
        >>> NGramCorpus(Corpus(tqbf)).tf('the')
        1.3010299956639813
        >>> NGramCorpus(Corpus(tqbf)).tf('fox')
        1.0

        """
        if ' ' in term:
            raise ValueError(
                'tf can only calculate the term frequency of individual words'
            )
        tcount = self.get_count(term)
        if tcount == 0:
            return 0.0
        return 1 + log10(tcount)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
