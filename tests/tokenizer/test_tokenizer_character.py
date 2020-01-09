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

from abydos.tokenizer import CharacterTokenizer


class CharacterTokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer.CharacterTokenizer."""

    def test_character_tokenizer(self):
        """Test abydos.tokenizer.CharacterTokenizer."""
        self.assertEqual(
            sorted(CharacterTokenizer().tokenize('').get_list()), []
        )
        self.assertEqual(
            sorted(CharacterTokenizer().tokenize('a').get_list()), ['a']
        )

        self.assertEqual(
            sorted(CharacterTokenizer().tokenize('NELSON').get_list()),
            sorted(['N', 'E', 'L', 'S', 'O', 'N']),
        )

    def test_character_tokenizer_intersections(self):
        """Test abydos.tokenizer.CharacterTokenizer intersections."""
        self.assertEqual(
            sorted(
                CharacterTokenizer().tokenize('NELSON')
                & CharacterTokenizer().tokenize('')
            ),
            [],
        )
        self.assertEqual(
            sorted(
                CharacterTokenizer().tokenize('')
                & CharacterTokenizer().tokenize('NEILSEN')
            ),
            [],
        )
        self.assertEqual(
            sorted(
                CharacterTokenizer().tokenize('NELSON')
                & CharacterTokenizer().tokenize('NEILSEN')
            ),
            sorted(['N', 'E', 'L', 'S']),
        )
        self.assertEqual(
            sorted(
                CharacterTokenizer().tokenize('NAIL')
                & CharacterTokenizer().tokenize('LIAN')
            ),
            sorted(['N', 'A', 'I', 'L']),
        )

    def test_character_tokenizer_counts(self):
        """Test abydos.tokenizer.CharacterTokenizer counts."""
        self.assertEqual(CharacterTokenizer().tokenize('').count(), 0)
        self.assertEqual(len(CharacterTokenizer().tokenize('').get_list()), 0)

        self.assertEqual(CharacterTokenizer().tokenize('NEILSEN').count(), 7)
        self.assertEqual(CharacterTokenizer().tokenize('NELSON').count(), 6)

        self.assertEqual(
            len(CharacterTokenizer().tokenize('NEILSEN').get_list()), 7
        )
        self.assertEqual(
            len(CharacterTokenizer().tokenize('NELSON').get_list()), 6
        )


if __name__ == '__main__':
    unittest.main()
