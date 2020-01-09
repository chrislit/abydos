# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.stemmer.test_stemmer_snowball_swedish.

This module contains unit tests for abydos.stemmer.SnowballSwedish
"""

import codecs
import unittest

from abydos.stemmer import SnowballSwedish, sb_swedish

from .. import _corpus_file


class SnowballSwedishTestCases(unittest.TestCase):
    """Test Snowball Swedish functions.

    abydos.stemmer.SnowballSwedish
    """

    stmr = SnowballSwedish()

    def test_snowball_swedish(self):
        """Test abydos.stemmer.SnowballSwedish (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/swedish/diffs.txt
        """
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        #  Snowball Swedish test set
        with codecs.open(
            _corpus_file('snowball_swedish.csv'), encoding='utf-8'
        ) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(self.stmr.stem(word), stem.lower())

        # Test wrapper
        self.assertEqual(sb_swedish('ackompanjerade'), 'ackompanjer')


if __name__ == '__main__':
    unittest.main()
