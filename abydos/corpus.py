# -*- coding: utf-8 -*-
"""abydos.corpus

The corpus class is a container for linguistic corpora and includes various
functions for corpus statistics, language modeling, etc.

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals

class Corpus(object):
    """The Corpus class

    Internally, this is a list of lists or lists. The corpus itself is a list
    of documents. Each document is an ordered list of sentences in those
    documents. And each sentence is an ordered list of words that make up that
    sentence.
    """
    def __init__(self, corpus_text='', doc_split='\n', sent_split='.',
                 filter_chars='', stop_words=[]):
        """Corpus initializer

        corpus_text -- The corpus text as a single string
        doc_split -- a character used to split corpus_text into documents
        sent_split -- a character used to split documents into sentences
        filter_chars -- A list of characters (as a string, tuple, set, or list)
            to filter out of the corpus text
        stop_words -- A list of words (as a tuple, set, or list) to filter out
            of the corpus text

        When importing a corpus, newlines divide sentences and other whitespace
        divides words.
        """
        self.corpus = []

        for document in corpus_text.split(doc_split):
            doc = []
            for sentence in [s.split() for s in document.split(sent_split)]:
                for sw in set(stop_words):
                    while sw in sentence:
                        sentence.remove(sw)
                for char in set(filter_chars):
                    sentence = [w.replace(char, '') for w in sentence]
                if sentence:
                    doc.append(sentence)
            if doc:
                self.corpus.append(doc)
