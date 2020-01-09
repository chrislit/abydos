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

import unittest

from abydos.tokenizer import NLTKTokenizer

try:
    from nltk import TweetTokenizer
except ImportError:  # pragma: no cover
    TweetTokenizer = None


class NLTKTokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer.NLTKTokenizer."""

    def test_nltk_tokenizer(self):
        """Test abydos.tokenizer.NLTKTokenizer."""
        if TweetTokenizer is None:  # pragma: no cover
            return

        tok = NLTKTokenizer(nltk_tokenizer=TweetTokenizer())

        self.assertEqual(sorted(tok.tokenize('').get_list()), [])
        self.assertEqual(sorted(tok.tokenize('a').get_list()), ['a'])

        self.assertEqual(
            sorted(tok.tokenize('NELSON').get_list()), sorted(['NELSON'])
        )
        self.assertEqual(
            sorted(tok.tokenize('NEILSEN').get_list()), sorted(['NEILSEN'])
        )

        tok = NLTKTokenizer(nltk_tokenizer=TweetTokenizer)
        tweet1 = 'Big night of basketball - @Warriors chasing 73 and a\
        farewell for an all-timer, @KobeBryant. NBA fans feeling like:'
        self.assertEqual(
            sorted(tok.tokenize(tweet1).get_list()),
            sorted(
                [
                    'Big',
                    'night',
                    'of',
                    'basketball',
                    '-',
                    '@Warriors',
                    'chasing',
                    '73',
                    'and',
                    'a',
                    'farewell',
                    'for',
                    'an',
                    'all-timer',
                    ',',
                    '@KobeBryant',
                    '.',
                    'NBA',
                    'fans',
                    'feeling',
                    'like',
                    ':',
                ]
            ),
        )

        tweet2 = 'Einstein was right! Congrats to @NSF and @LIGO on detecting\
        gravitational waves - a huge breakthrough in how we understand the\
        universe.'
        self.assertEqual(
            sorted(tok.tokenize(tweet2).get_list()),
            sorted(
                [
                    'Einstein',
                    'was',
                    'right',
                    '!',
                    'Congrats',
                    'to',
                    '@NSF',
                    'and',
                    '@LIGO',
                    'on',
                    'detecting',
                    'gravitational',
                    'waves',
                    '-',
                    'a',
                    'huge',
                    'breakthrough',
                    'in',
                    'how',
                    'we',
                    'understand',
                    'the',
                    'universe',
                    '.',
                ]
            ),
        )

        with self.assertRaises(TypeError):
            NLTKTokenizer(nltk_tokenizer='TweetTokenizer')


if __name__ == '__main__':
    unittest.main()
