# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_iterative_substring.

This module contains unit tests for abydos.distance.IterativeSubString
"""

import unittest

from abydos.distance import IterativeSubString


class IterativeSubStringTestCases(unittest.TestCase):
    """Test IterativeSubString functions.

    abydos.distance.IterativeSubString
    """

    cmp = IterativeSubString()
    cmp_norm = IterativeSubString(normalize_strings=True)

    def test_iterative_substring_sim(self):
        """Test abydos.distance.IterativeSubString.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.1)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.1)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.1)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.1)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6618421053
        )

    def test_iterative_substring_dist(self):
        """Test abydos.distance.IterativeSubString.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.9)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.9)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.9)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.9)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3381578947
        )

    def test_iterative_substring_corr(self):
        """Test abydos.distance.IterativeSubString.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), -1.0)
        self.assertEqual(self.cmp.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), -0.8)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), -0.8)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), -0.8)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), -0.8)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.3236842105
        )
        self.assertAlmostEqual(
            self.cmp_norm.corr('ATCAACGAGT', 'AACGATTAG'), 0.3236842105
        )
        self.assertAlmostEqual(
            self.cmp_norm.corr('ATC..AACGAGT', 'AA_CGAT_TAG'), 0.3236842105
        )


if __name__ == '__main__':
    unittest.main()
