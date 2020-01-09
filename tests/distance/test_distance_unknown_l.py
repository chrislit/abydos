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

"""abydos.tests.distance.test_distance_unknown_l.

This module contains unit tests for abydos.distance.UnknownL
"""

import unittest

from abydos.distance import UnknownL


class UnknownLTestCases(unittest.TestCase):
    """Test UnknownL functions.

    abydos.distance.UnknownL
    """

    cmp = UnknownL()
    cmp_no_d = UnknownL(alphabet=0)

    def test_unknown_l_sim(self):
        """Test abydos.distance.UnknownL.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9872448979591837)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9923469388)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9923469388)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9923469388)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9923469388)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9923371648
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
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5384615385
        )

    def test_unknown_l_dist(self):
        """Test abydos.distance.UnknownL.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.012755102040816313)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0076530612)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0076530612)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0076530612)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0076530612)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0076628352
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
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.4615384615
        )


if __name__ == '__main__':
    unittest.main()
