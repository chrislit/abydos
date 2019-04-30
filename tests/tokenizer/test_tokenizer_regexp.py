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

from abydos.tokenizer import RegexpTokenizer


class RegexpTokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer.RegexpTokenizer."""

    def test_regexp_tokenizer(self):
        """Test abydos.tokenizer.RegexpTokenizer."""
        self.assertEqual(sorted(RegexpTokenizer().tokenize('').get_list()), [])
        self.assertEqual(
            sorted(RegexpTokenizer().tokenize('a').get_list()), ['a']
        )

        self.assertEqual(
            sorted(RegexpTokenizer().tokenize('NELSON').get_list()),
            sorted(['NELSON']),
        )
        self.assertEqual(
            sorted(RegexpTokenizer().tokenize('NEILSEN').get_list()),
            sorted(['NEILSEN']),
        )

        tweet = "Looking forward to hearing your ideas about what we can\
        accomplish this year & beyond. I'll answer your questions on\
        #AskPOTUS at 12:30p ET."
        self.assertEqual(
            sorted(RegexpTokenizer().tokenize(tweet).get_list()),
            sorted(
                [
                    'Looking',
                    'forward',
                    'to',
                    'hearing',
                    'your',
                    'ideas',
                    'about',
                    'what',
                    'we',
                    'can',
                    'accomplish',
                    'this',
                    'year',
                    'beyond',
                    'I',
                    'll',
                    'answer',
                    'your',
                    'questions',
                    'on',
                    'AskPOTUS',
                    'at',
                    '12',
                    '30p',
                    'ET',
                ]
            ),
        )


if __name__ == '__main__':
    unittest.main()
