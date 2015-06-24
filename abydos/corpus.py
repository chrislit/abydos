# -*- coding: utf-8 -*-

# Copyright 2014-2015 by Christopher C. Little.
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

"""abydos.corpus

The corpus class is a container for linguistic corpora and includes various
functions for corpus statistics, language modeling, etc.
"""

from __future__ import unicode_literals
from math import log10


class Corpus(object):
    """The Corpus class

    Internally, this is a list of lists or lists. The corpus itself is a list
    of documents. Each document is an ordered list of sentences in those
    documents. And each sentence is an ordered list of words that make up that
    sentence.
    """
    def __init__(self, corpus_text='', doc_split='\n\n', sent_split='\n',
                 filter_chars='', stop_words=None):
        """Corpus initializer

        By default, when importing a corpus:
            - two consecutive newlines divide documents
            - single newlines divide sentences
            - other whitespace divides words

        :param corpus_text: the corpus text as a single string
        :param doc_split: a character or string used to split corpus_text into
            documents
        :param sent_split: a character or string used to split documents into
            sentences
        :param filter_chars: A list of characters (as a string, tuple, set, or
            list) to filter out of the corpus text
        :param stop_words: A list of words (as a tuple, set, or list) to filter
            out of the corpus text
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
        """Get the docs in the corpus

        Each list within a doc represents the sentences in that doc, each of
        which is in turn a list of words within that sentence.

        :returns: the paragraphs in the corpus as a list of lists of lists
            of strs
        :rtype: list(list(list(str)))
        """
        return self.corpus

    def paras(self):
        """Get the paragraphs in the corpus

        Each list within a paragraph represents the sentences in that doc, each
        of which is in turn a list of words within that sentence.
        This is identical to the docs() member function and exists only to
        mirror part of NLTK's API for corpora.

        :returns: the paragraphs in the corpus as a list of lists of lists
            of strs
        :rtype: list(list(list(str)))
        """
        return self.docs()

    def sents(self):
        """Get the sentences in the corpus

        Each list within a sentence represents the words within that sentence.

        :returns: the sentences in the corpus as a list of lists of strs
        :rtype: list(list(str))
        """
        return [words for sents in self.corpus for words in sents]

    def words(self):
        """Get the words in the corpus as a single list

        :returns: the words in the corpus as a list of strs
        :rtype: list(str)
        """
        return [words for sents in self.sents() for words in sents]

    def docs_of_words(self):
        """Get the docs in the corpus, with sentences flattened

        Each list within the corpus represents all the words of that document.
        Thus the sentence level of lists has been flattened.

        :returns: the docs in the corpus as a list of list of strs
        :rtype: list(list(str))
        """
        return [[words for sents in doc for words in sents]
                for doc in self.corpus]

    def raw(self):
        """Get the raw corpus

        This is reconstructed by joining sub-components with the corpus' split
        characters

        :returns: the raw corpus
        :rtype: str
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
        """Calculates the Inverse Document Frequency (IDF) of a term in the
        corpus.

        :param term: the term to calculate the IDF of
        :param transform: a function to apply to each document term before
            checking for the presence of term
        :returns: the IDF
        :rtype: float
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

        return log10(len(docs)/docs_with_term)
