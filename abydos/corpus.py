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

    Internally, this is a list of lists. The corpus itself is an ordered list of
    sentences; each sentence is an ordered list of words that make up the
    sentence.
    """
    def __init__(self, corpus_text='', filter_chars='', stop_words=[]):
        """Corpus initializer

        corpus_text -- The corpus text as a single string
        filter_chars -- A list of characters (as a string, tuple, set, or list)
            to filter out of the corpus text
        stop_words -- A list of words (as a tuple, set, or list) to filter out
            of the corpus text

        When importing a corpus, newlines divide sentences and other whitespace
        divides words.
        """
        self.corpus = []

        for sentence in [s.split() for s in corpus_text.splitlines()]:
            for sw in set(stop_words):
                if sw in sentence:
                    sentence.remove(sw)
            for char in set(filter_chars):
                sentence = [w.replace(char, '') for w in sentence]
            self.corpus.append(sentence)

        while [] in self.corpus:
            self.corpus.remove([])
