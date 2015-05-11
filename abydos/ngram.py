# -*- coding: utf-8 -*-
"""abydos.ngram

The NGram class is a container for an n-gram corpus

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
from collections import Counter
from .corpus import Corpus


class NGramCorpus(object):
    """The NGramCorpus class

    Internally, this is a set of recursively embedded dicts, with n layers for
    a corpus of n-grams. E.g. for a trigram corpus, this will be a dict of
    dicts of dicts. More precisely, collections.Counter is used in place of
    dict, making multiset operations valid and allowing unattested n-grams to
    be queries.

    The key at each level is a word. The value at the most deeply embedded
    level is a numeric value representing the frequency of the trigram. E.g.
    the trigram frequency of 'colorless green ideas' would be the value of
    self.ngcorpus['colorless']['green']['ideas'].
    """
    ngcorpus = Counter()

    def __init__(self, corpus=None):
        """Corpus initializer

        corpus -- The Corpus from which to initialize the n-gram corpus. By
            default, this is None, which initializes an empty NGramCorpus. This
            can then be populated using NGramCorpus methods.
        """
        if corpus is None:
            return
        elif isinstance(corpus, Corpus):
            self.corpus_importer(corpus)
        else:
            raise TypeError('Corpus argument must be None or of type ' +
                            'abydos.Corpus. ' + str(type(corpus)) + ' found.')

    def corpus_importer(self, corpus):
        """Fill in self.ngcorpus from a Corpus argument

        corpus -- The Corpus from which to initialize the n-gram corpus
        """
        pass

    def gng_importer(self, corpus):
        """Fill in self.ngcorpus from a Google NGram corpus file

        corpus -- The Google NGram file from which to initialize the n-gram
            corpus
        """
        pass
