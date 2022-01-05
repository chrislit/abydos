# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_ratcliff_obershelp.

This module contains unit tests for abydos.distance.RatcliffObershelp
"""

import unittest
from difflib import SequenceMatcher

from abydos.distance import RatcliffObershelp

from .. import _corpus_file


class RatcliffObershelpTestCases(unittest.TestCase):
    """Test Ratcliff-Obserhelp functions.

    abydos.distance.RatcliffObershelp
    """

    cmp = RatcliffObershelp()

    def test_ratcliff_obershelp_sim(self):
        """Test abydos.distance.RatcliffObershelp.sim."""
        # https://github.com/rockymadden/stringmetric/blob/master/core/src/test/scala/com/rockymadden/stringmetric/similarity/RatcliffObershelpMetricSpec.scala
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('abc', ''), 0)
        self.assertEqual(self.cmp.sim('', 'xyz'), 0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1)
        self.assertEqual(self.cmp.sim('123', '123'), 1)
        self.assertEqual(self.cmp.sim('abc', 'xyz'), 0)
        self.assertEqual(self.cmp.sim('123', '456'), 0)
        self.assertAlmostEqual(
            self.cmp.sim('aleksander', 'alexandre'), 0.7368421052631579
        )
        self.assertAlmostEqual(
            self.cmp.sim('alexandre', 'aleksander'), 0.7368421052631579
        )
        self.assertAlmostEqual(
            self.cmp.sim('pennsylvania', 'pencilvaneya'), 0.6666666666666666
        )
        self.assertAlmostEqual(
            self.cmp.sim('pencilvaneya', 'pennsylvania'), 0.6666666666666666
        )
        self.assertAlmostEqual(
            self.cmp.sim('abcefglmn', 'abefglmo'), 0.8235294117647058
        )
        self.assertAlmostEqual(
            self.cmp.sim('abefglmo', 'abcefglmn'), 0.8235294117647058
        )

        with open(_corpus_file('variantNames.csv')) as cav_testset:
            next(cav_testset)
            for line in cav_testset:
                line = line.strip().split(',')
                word1, word2 = line[0], line[4]
                self.assertAlmostEqual(
                    self.cmp.sim(word1, word2),
                    SequenceMatcher(None, word1, word2).ratio(),
                )

        with open(_corpus_file('wikipediaCommonMisspellings.csv')) as missp:
            next(missp)
            for line in missp:
                line = line.strip().upper()
                line = ''.join(
                    [
                        _
                        for _ in line.strip()
                        if _ in tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ,')
                    ]
                )
                word1, word2 = line.split(',')
                # print(word1, word2e)
                self.assertAlmostEqual(
                    self.cmp.sim(word1, word2),
                    SequenceMatcher(None, word1, word2).ratio(),
                )

    def test_ratcliff_obershelp_dist(self):
        """Test abydos.distance.RatcliffObershelp.dist."""
        # https://github.com/rockymadden/stringmetric/blob/master/core/src/test/scala/com/rockymadden/stringmetric/similarity/RatcliffObershelpMetricSpec.scala
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('abc', ''), 1)
        self.assertEqual(self.cmp.dist('', 'xyz'), 1)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist('123', '123'), 0)
        self.assertEqual(self.cmp.dist('abc', 'xyz'), 1)
        self.assertEqual(self.cmp.dist('123', '456'), 1)
        self.assertAlmostEqual(
            self.cmp.dist('aleksander', 'alexandre'), 0.2631578947368421
        )
        self.assertAlmostEqual(
            self.cmp.dist('alexandre', 'aleksander'), 0.2631578947368421
        )
        self.assertAlmostEqual(
            self.cmp.dist('pennsylvania', 'pencilvaneya'), 0.3333333333333333
        )
        self.assertAlmostEqual(
            self.cmp.dist('pencilvaneya', 'pennsylvania'), 0.3333333333333333
        )
        self.assertAlmostEqual(
            self.cmp.dist('abcefglmn', 'abefglmo'), 0.1764705882352941
        )
        self.assertAlmostEqual(
            self.cmp.dist('abefglmo', 'abcefglmn'), 0.1764705882352941
        )


if __name__ == '__main__':
    unittest.main()
