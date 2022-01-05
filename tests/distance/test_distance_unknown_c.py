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

"""abydos.tests.distance.test_distance_unknown_c.

This module contains unit tests for abydos.distance.UnknownC
"""

import unittest

from abydos.distance import UnknownC


class UnknownCTestCases(unittest.TestCase):
    """Test UnknownC functions.

    abydos.distance.UnknownC
    """

    cmp = UnknownC()
    cmp_no_d = UnknownC(alphabet=0)

    def test_unknown_c_sim(self):
        """Test abydos.distance.UnknownC.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.1987163029525032)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.1666666667)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.1666666667)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.1666666667)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.1666666667)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.09577771
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.1926686589
        )

    def test_unknown_c_dist(self):
        """Test abydos.distance.UnknownC.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.8012836970474968)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.8333333333)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.8333333333)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.8333333333)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.8333333333)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.90422229
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.8333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.8333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.8333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.8333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.8073313411
        )


if __name__ == '__main__':
    unittest.main()
