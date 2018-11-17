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

"""abydos.corpus._corpus.

The Corpus class is a container for linguistic corpora and includes various
functions for corpus statistics, language modeling, etc.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log10

__all__ = ['Corpus']


class Corpus(object):
    """Corpus class.

    Internally, this is a list of lists or lists. The corpus itself is a list
    of documents. Each document is an ordered list of sentences in those
    documents. And each sentence is an ordered list of words that make up that
    sentence.
    """

    def __init__(
        self,
        corpus_text='',
        doc_split='\n\n',
        sent_split='\n',
        filter_chars='',
        stop_words=None,
    ):
        r"""Initialize Corpus.

        By default, when importing a corpus:
            - two consecutive newlines divide documents
            - single newlines divide sentences
            - other whitespace divides words

        Parameters
        ----------
        corpus_text : str
            The corpus text as a single string
        doc_split : str
            A character or string used to split corpus_text into documents
        sent_split : str
            A character or string used to split documents into sentences
        filter_chars : list
            A list of characters (as a string, tuple, set, or list) to filter
            out of the corpus text
        stop_words : list
            A list of words (as a tuple, set, or list) to filter out of the
            corpus text

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)

        """
        self.corpus = []
        self.doc_split = doc_split
        self.sent_split = sent_split

        for document in corpus_text.split(doc_split):
            doc = []
            for sentence in (s.split() for s in document.split(sent_split)):
                if stop_words:
                    for word in set(stop_words):
                        while word in sentence:
                            sentence.remove(word)
                for char in set(filter_chars):
                    sentence = [word.replace(char, '') for word in sentence]
                if sentence:
                    doc.append(sentence)
            if doc:
                self.corpus.append(doc)

    def docs(self):
        r"""Return the docs in the corpus.

        Each list within a doc represents the sentences in that doc, each of
        which is in turn a list of words within that sentence.

        Returns
        -------
        [[[str]]]
            The docs in the corpus as a list of lists of lists of strs

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> corp.docs()
        [[['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
        'dog.'], ['And', 'then', 'it', 'slept.'], ['And', 'the', 'dog',
        'ran', 'off.']]]
        >>> len(corp.docs())
        1

        """
        return self.corpus

    def paras(self):
        r"""Return the paragraphs in the corpus.

        Each list within a paragraph represents the sentences in that doc, each
        of which is in turn a list of words within that sentence.
        This is identical to the docs() member function and exists only to
        mirror part of NLTK's API for corpora.

        Returns
        -------
        [[[str]]]
            The paragraphs in the corpus as a list of lists of lists of strs

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> corp.paras()
        [[['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
        'dog.'], ['And', 'then', 'it', 'slept.'], ['And', 'the', 'dog',
        'ran', 'off.']]]
        >>> len(corp.paras())
        1

        """
        return self.docs()

    def sents(self):
        r"""Return the sentences in the corpus.

        Each list within a sentence represents the words within that sentence.

        Returns
        -------
        [[str]]
            The sentences in the corpus as a list of lists of strs

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> corp.sents()
        [['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
        'dog.'], ['And', 'then', 'it', 'slept.'], ['And', 'the', 'dog',
        'ran', 'off.']]
        >>> len(corp.sents())
        3

        """
        return [words for sents in self.corpus for words in sents]

    def words(self):
        r"""Return the words in the corpus as a single list.

        Returns
        -------
        [str]
            The words in the corpus as a list of strs

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> corp.words()
        ['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
        'dog.', 'And', 'then', 'it', 'slept.', 'And', 'the', 'dog', 'ran',
        'off.']
        >>> len(corp.words())
        18

        """
        return [words for sents in self.sents() for words in sents]

    def docs_of_words(self):
        r"""Return the docs in the corpus, with sentences flattened.

        Each list within the corpus represents all the words of that document.
        Thus the sentence level of lists has been flattened.

        Returns
        -------
        [[str]]
            The docs in the corpus as a list of list of strs

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> corp.docs_of_words()
        [['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
        'dog.', 'And', 'then', 'it', 'slept.', 'And', 'the', 'dog', 'ran',
        'off.']]
        >>> len(corp.docs_of_words())
        1

        """
        return [
            [words for sents in doc for words in sents] for doc in self.corpus
        ]

    def raw(self):
        r"""Return the raw corpus.

        This is reconstructed by joining sub-components with the corpus' split
        characters

        Returns
        -------
        str
            The raw corpus

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> print(corp.raw())
        The quick brown fox jumped over the lazy dog.
        And then it slept.
        And the dog ran off.
        >>> len(corp.raw())
        85

        """
        doc_list = []
        for doc in self.corpus:
            sent_list = []
            for sent in doc:
                sent_list.append(' '.join(sent))
            doc_list.append(self.sent_split.join(sent_list))
            del sent_list
        return self.doc_split.join(doc_list)

    def idf(self, term, transform=None):
        r"""Calculate the Inverse Document Frequency of a term in the corpus.

        Parameters
        ----------
        term : str
            The term to calculate the IDF of
        transform : function
            A function to apply to each document term before checking for the
            presence of term

        Returns
        -------
        float
            The IDF

        Examples
        --------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n\n'
        >>> tqbf += 'And then it slept.\n\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> print(corp.docs())
        [[['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
        'dog.']],
        [['And', 'then', 'it', 'slept.']],
        [['And', 'the', 'dog', 'ran', 'off.']]]
        >>> round(corp.idf('dog'), 10)
        0.4771212547
        >>> round(corp.idf('the'), 10)
        0.1760912591

        """
        docs_with_term = 0
        docs = self.docs_of_words()
        for doc in docs:
            doc_set = set(doc)
            if transform:
                transformed_doc = []
                for word in doc_set:
                    transformed_doc.append(transform(word))
                doc_set = set(transformed_doc)

            if term in doc_set:
                docs_with_term += 1

        if docs_with_term == 0:
            return float('inf')

        return log10(len(docs) / docs_with_term)


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
