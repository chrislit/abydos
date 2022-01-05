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

"""abydos.tests.distance.test_distance_kent_foster_i.

This module contains unit tests for abydos.distance.KentFosterI
"""

import unittest

from abydos.distance import KentFosterI


class KentFosterITestCases(unittest.TestCase):
    """Test KentFosterI functions.

    abydos.distance.KentFosterI
    """

    cmp = KentFosterI()
    cmp_no_d = KentFosterI(alphabet=0)

    def test_kent_foster_i_sim(self):
        """Test abydos.distance.KentFosterI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.6666666666666667)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.8)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.8604651163
        )

    def test_kent_foster_i_dist(self):
        """Test abydos.distance.KentFosterI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.33333333333333326)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.1395348837
        )

    def test_kent_foster_i_sim_score(self):
        """Test abydos.distance.KentFosterI.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), -0.3333333333333333
        )

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), -0.2)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), -0.2)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), -0.2)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), -0.2)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), -0.1395348837
        )


if __name__ == '__main__':
    unittest.main()
