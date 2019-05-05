# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.tokenizer.test_tokenizer_qgrams.

This module contains unit tests for abydos.tokenizer.QGrams
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.tokenizer import LegaliPyTokenizer

from six import PY2

from .. import _corpus_file


class LegaliPyTokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer.LegaliPyTokenizer."""

    def test_legalipy_tokenizer(self):
        """Test abydos.tokenizer.LegaliPyTokenizer."""
        if PY2:  # skip tests of SyllabiPy on Python 2.7
            return
        try:
            from syllabipy.legalipy import LegaliPy  # noqa: F401
        except ImportError:  # pragma: no cover
            return

        self.assertEqual(
            sorted(LegaliPyTokenizer().tokenize('').get_list()), []
        )
        self.assertEqual(
            sorted(LegaliPyTokenizer().tokenize('a').get_list()), ['a']
        )

        self.assertEqual(
            sorted(LegaliPyTokenizer().tokenize('nelson').get_list()),
            sorted(['n', 'els', 'on']),
        )
        self.assertEqual(
            sorted(LegaliPyTokenizer().tokenize('neilson').get_list()),
            sorted(['n', 'eils', 'on']),
        )

        tok = LegaliPyTokenizer()
        with open(_corpus_file('wikipediaCommonMisspellings.csv')) as corpus:
            text = ' '.join([_.split(',')[1] for _ in corpus.readlines()])
        tok.train_onsets(text)

        with open(_corpus_file('misspellings.csv')) as corpus:
            text = ' '.join([_.split(',')[1] for _ in corpus.readlines()])
        tok.train_onsets(text, append=True)

        self.assertEqual(
            sorted(tok.tokenize('nelson').get_list()), sorted(['nel', 'son'])
        )
        self.assertEqual(
            sorted(tok.tokenize('neilson').get_list()),
            sorted(['ne', 'il', 'son']),
        )
        self.assertEqual(
            sorted(tok.tokenize('peninsular').get_list()),
            sorted(['pe', 'nin', 'su', 'lar']),
        )
        self.assertEqual(
            sorted(tok.tokenize('spectacular').get_list()),
            sorted(['spec', 'ta', 'cu', 'lar']),
        )
        self.assertEqual(
            sorted(tok.tokenize('sufficiently').get_list()),
            sorted(['suf', 'fi', 'ci', 'ent', 'ly']),
        )
        self.assertEqual(
            sorted(tok.tokenize('yachting').get_list()),
            sorted(['y', 'ach', 'ting']),
        )
        self.assertEqual(
            sorted(tok.tokenize('caterpillars').get_list()),
            sorted(['ca', 'ter', 'pil', 'lars']),
        )


if __name__ == '__main__':
    unittest.main()
