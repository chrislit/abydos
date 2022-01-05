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

"""abydos.tests.distance.test_distance_warrens_iii.

This module contains unit tests for abydos.distance.WarrensIII
"""

import unittest

from abydos.distance import WarrensIII


class WarrensIIITestCases(unittest.TestCase):
    """Test WarrensIII functions.

    abydos.distance.WarrensIII
    """

    cmp = WarrensIII()
    cmp_no_d = WarrensIII(alphabet=0)
    cmp_2_1 = WarrensIII(alphabet=2, qval=1)

    def test_warrens_iii_sim(self):
        """Test abydos.distance.WarrensIII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9987228607918264)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9987228607918264)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9974424552429668)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9974424552429668)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.993581514762516)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9961439589)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9954751131
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0
        )

        self.assertEqual(self.cmp_2_1.sim('CG', 'GC'), 0.5)

    def test_warrens_iii_dist(self):
        """Test abydos.distance.WarrensIII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0012771392081736277)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0012771392081736277)
        self.assertEqual(self.cmp.dist('abc', ''), 0.002557544757033181)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.002557544757033181)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.006418485237484006)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0038560411)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0045248869
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.0
        )

    def test_warrens_iii_corr(self):
        """Test abydos.distance.WarrensIII.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.9974457215836526)
        self.assertEqual(self.cmp.corr('', 'a'), 0.9974457215836526)
        self.assertEqual(self.cmp.corr('abc', ''), 0.9948849104859335)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.9948849104859335)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), 0.9871630295250321)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.9922879177)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.9922879177)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.9922879177)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.9922879177)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.9909502262
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -1.0
        )


if __name__ == '__main__':
    unittest.main()
