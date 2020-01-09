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

"""abydos.tests.distance.test_distance_azzoo.

This module contains unit tests for abydos.distance.AZZOO
"""

import unittest

from abydos.distance import AZZOO


class AZZOOTestCases(unittest.TestCase):
    """Test AZZOO functions.

    abydos.distance.AZZOO
    """

    cmp = AZZOO()
    cmp_no_d = AZZOO(alphabet=0)

    def test_azzoo_sim(self):
        """Test abydos.distance.AZZOO.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9809885931558935)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9886075949)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9886075949)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9886075949)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9886075949)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.986163522
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.6363636364
        )

    def test_azzoo_sim_score(self):
        """Test abydos.distance.AZZOO.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 392.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 391.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 391.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 390.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 390.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 394.0)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 387.0)

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), 390.5)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), 390.5)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 390.5)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 390.5)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 392.0
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 4.0)
        self.assertEqual(self.cmp_no_d.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim_score('Nigel', 'Niall'), 3.0)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Niall', 'Nigel'), 3.0)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Colin', 'Coiln'), 3.0)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Coiln', 'Colin'), 3.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), 7.0
        )


if __name__ == '__main__':
    unittest.main()
