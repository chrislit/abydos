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

r"""abydos.corpus.

The corpus package includes basic and n-gram corpus classes:

- :py:class:`Corpus`
- :py:class:`NGramCorpus`


As a quick example of :py:class:`.Corpus`:

>>> tqbf = 'The quick brown fox jumped over the lazy dog.\n\n'
>>> tqbf += 'And then it slept.\n\n And the dog ran off.'
>>> corp = Corpus(tqbf)
>>> corp.docs()
[[['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog.']],
[['And', 'then', 'it', 'slept.']], [['And', 'the', 'dog', 'ran', 'off.']]]
>>> round(corp.idf('dog'), 10)
0.4771212547
>>> round(corp.idf('the'), 10)
0.1760912591

Here, each sentence is a separate "document". We can retrieve IDF values from
the :py:class:`.Corpus`. The same :py:class:`.Corpus` can be used to initialize
an :py:class:`.NGramCorpus` and calculate TF values:

>>> ngcorp = NGramCorpus(corp)
>>> ngcorp.get_count('the')
2
>>> ngcorp.get_count('fox')
1
>>> ngcorp.tf('the')
1.3010299956639813
>>> ngcorp.tf('fox')
1.0

----

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._corpus import Corpus
from ._ngram_corpus import NGramCorpus

__all__ = ['Corpus', 'NGramCorpus']


if __name__ == '__main__':
    import doctest

    doctest.testmod()
