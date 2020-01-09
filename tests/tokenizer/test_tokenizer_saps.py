# -*- coding: utf-8 -*-

# Copyright 2019-2020 by Christopher C. Little.
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

import unittest

from abydos.tokenizer import SAPSTokenizer


class SAPSTokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer.SAPSTokenizer."""

    def test_saps_tokenizer(self):
        """Test abydos.tokenizer.SAPSTokenizer."""
        self.assertEqual(sorted(SAPSTokenizer().tokenize('').get_list()), [])
        self.assertEqual(
            sorted(SAPSTokenizer().tokenize('a').get_list()), ['a']
        )

        tok = SAPSTokenizer()

        self.assertEqual(
            sorted(tok.tokenize('nelson').get_list()), sorted(['nel', 'son'])
        )
        self.assertEqual(
            sorted(tok.tokenize('neilson').get_list()), sorted(['neil', 'son'])
        )
        self.assertEqual(
            sorted(tok.tokenize('peninsular').get_list()),
            sorted(['pe', 'nin', 'su', 'lar']),
        )
        self.assertEqual(
            sorted(tok.tokenize('spectacular').get_list()),
            sorted(['s', 'pec', 'ta', 'cu', 'lar']),
        )
        self.assertEqual(
            sorted(tok.tokenize('sufficiently').get_list()),
            sorted(['suf', 'fi', 'cien', 't', 'ly']),
        )
        self.assertEqual(
            sorted(tok.tokenize('yachting').get_list()),
            sorted(['yac', 'h', 'tin', 'g']),
        )
        self.assertEqual(
            sorted(tok.tokenize('caterpillars').get_list()),
            sorted(['ca', 'ter', 'pil', 'lar', 's']),
        )


if __name__ == '__main__':
    unittest.main()
