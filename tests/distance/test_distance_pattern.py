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

"""abydos.tests.distance.test_distance_pattern.

This module contains unit tests for abydos.distance.Pattern
"""

import unittest

from abydos.distance import Pattern


class PatternTestCases(unittest.TestCase):
    """Test Pattern functions.

    abydos.distance.Pattern
    """

    cmp = Pattern()
    cmp_no_d = Pattern(alphabet=0)

    def test_pattern_dist(self):
        """Test abydos.distance.Pattern.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.0001626926280716368)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 5.85693e-05)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 5.85693e-05)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 5.85693e-05)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 5.85693e-05)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 7.80925e-05
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.2448979592
        )

    def test_pattern_sim(self):
        """Test abydos.distance.Pattern.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9998373073719283)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9999414307)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9999414307)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9999414307)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9999414307)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9999219075
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.5555555556
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.5555555556
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.5555555556
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.5555555556
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.7551020408
        )


if __name__ == '__main__':
    unittest.main()
