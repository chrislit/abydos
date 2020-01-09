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

from abydos.tokenizer import WordpunctTokenizer


class WordpunctTokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer.WordpunctTokenizer."""

    def test_wordpunct_tokenizer(self):
        """Test abydos.tokenizer.WordpunctTokenizer."""
        self.assertEqual(
            sorted(WordpunctTokenizer().tokenize('').get_list()), []
        )
        self.assertEqual(
            sorted(WordpunctTokenizer().tokenize('a').get_list()), ['a']
        )

        self.assertEqual(
            sorted(WordpunctTokenizer().tokenize('NELSON').get_list()),
            sorted(['NELSON']),
        )
        self.assertEqual(
            sorted(WordpunctTokenizer().tokenize('NEILSEN').get_list()),
            sorted(['NEILSEN']),
        )

        tweet = 'I got a chance to catch up with the @Space_Station crew\
        today. Nothing like a call to space on #AstronomyNight!'
        self.assertEqual(
            sorted(WordpunctTokenizer().tokenize(tweet).get_list()),
            sorted(
                [
                    'I',
                    'got',
                    'a',
                    'chance',
                    'to',
                    'catch',
                    'up',
                    'with',
                    'the',
                    '@',
                    'Space_Station',
                    'crew',
                    'today',
                    '.',
                    'Nothing',
                    'like',
                    'a',
                    'call',
                    'to',
                    'space',
                    'on',
                    '#',
                    'AstronomyNight',
                    '!',
                ]
            ),
        )


if __name__ == '__main__':
    unittest.main()
