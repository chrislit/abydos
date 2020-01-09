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

"""abydos.tests.distance.test_distance_cohen_kappa.

This module contains unit tests for abydos.distance.CohenKappa
"""

import unittest

from abydos.distance import CohenKappa


class CohenKappaTestCases(unittest.TestCase):
    """Test CohenKappa functions.

    abydos.distance.CohenKappa
    """

    cmp = CohenKappa()
    cmp_no_d = CohenKappa(alphabet=0)

    def test_cohen_kappa_sim(self):
        """Test abydos.distance.CohenKappa.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9987228607918263)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9987228607918263)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9974424552429667)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9974424552429667)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.993581514762516)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9961439589)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9961439589)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9954751131
        )

        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

    def test_cohen_kappa_dist(self):
        """Test abydos.distance.CohenKappa.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0012771392081737387)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0012771392081737387)
        self.assertEqual(self.cmp.dist('abc', ''), 0.002557544757033292)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.002557544757033292)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.006418485237484006)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0038560411)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0038560411)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0045248869
        )

        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)


if __name__ == '__main__':
    unittest.main()
