# -*- coding: utf-8 -*-
"""abydos.tests.test_corpus

This module contains unit tests for abydos.corpus

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
import unittest
from abydos.corpus import Corpus

class CorpusTestCases(unittest.TestCase):
    """test cases for abydos.corpus
    """
    def test_corpus(self):
        """test abydos.corpus.Corpus
        """
        # base cases
        self.assertEqual(Corpus().corpus, [])
        self.assertEqual(Corpus('').corpus, [])
        self.assertEqual(Corpus(' ').corpus, [])
        self.assertEqual(Corpus('\n').corpus, [])
        self.assertEqual(Corpus(' \n').corpus, [])
        self.assertEqual(Corpus(' \n ').corpus, [])

        # one sentence
        self.assertEqual(Corpus('a').corpus, [['a']])
        self.assertEqual(Corpus('ab ab').corpus, [['ab', 'ab']])
        self.assertEqual(Corpus('abc def ghi').corpus, [['abc', 'def', 'ghi']])

        # multiple sentences
        self.assertEqual(Corpus('abc\ndef ghi').corpus,
                         [['abc'], ['def', 'ghi']])
        self.assertEqual(Corpus('abc\ndef ghi\n').corpus,
                         [['abc'], ['def', 'ghi']])
        self.assertEqual(Corpus('\nabc\r\ndef ghi\n').corpus,
                         [['abc'], ['def', 'ghi']])

        # sentence(s) with ignorables
        self.assertEqual(Corpus('abc. d-ef ghi.', '.-').corpus,
                         [['abc', 'def', 'ghi']])
        self.assertEqual(Corpus('abc.\nd-ef ghi.\n', '.-').corpus,
                         [['abc'], ['def', 'ghi']])
        self.assertEqual(Corpus('\nabc\r\ndef ghi\na b c d e f g.\n',
                                '.-').corpus,
                         [['abc'], ['def', 'ghi'],
                          ['a', 'b', 'c', 'd', 'e', 'f', 'g']])

if __name__ == '__main__':
    unittest.main()
