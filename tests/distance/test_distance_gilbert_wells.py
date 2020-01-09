# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_gilbert_wells.

This module contains unit tests for abydos.distance.GilbertWells
"""

import unittest

from abydos.distance import GilbertWells


class GilbertWellsTestCases(unittest.TestCase):
    """Test GilbertWells functions.

    abydos.distance.GilbertWells
    """

    cmp = GilbertWells()
    cmp_no_d = GilbertWells(alphabet=0)

    def test_gilbert_wells_sim(self):
        """Test abydos.distance.GilbertWells.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.028716013247135602)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.3776594411)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.3776594411)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.3776594411)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.3776594411)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4950086952
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(
            self.cmp_no_d.sim('abcd', 'efgh'), 0.13486136169765683
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.0255856715
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.0255856715
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.0255856715
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.0255856715
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0153237873
        )

    def test_gilbert_wells_dist(self):
        """Test abydos.distance.GilbertWells.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.9712839867528644)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.6223405589)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.6223405589)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.6223405589)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.6223405589)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5049913048
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.8651386383023432
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.9744143285
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.9744143285
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.9744143285
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.9744143285
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.9846762127
        )

    def test_gilbert_wells_sim_score(self):
        """Test abydos.distance.GilbertWells.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 76.91383873217538)
        self.assertEqual(self.cmp.sim_score('a', ''), 40.179592442305186)
        self.assertEqual(self.cmp.sim_score('', 'a'), 40.179592442305186)
        self.assertEqual(self.cmp.sim_score('abc', ''), 39.4890060826051)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 39.4890060826051)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 49.00800898579118)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), 1.6845961909440712
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 25.6938443303
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 25.6938443303
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 25.6938443303
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 25.6938443303
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 55.2085412384
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), -36.04365338911715)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 70.9425768923849)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 70.9425768923849)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 71.63572407294485)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 71.63572407294485)
        self.assertEqual(
            self.cmp_no_d.sim_score('abc', 'abc'), 71.63572407294485
        )
        self.assertEqual(
            self.cmp_no_d.sim_score('abcd', 'efgh'), 9.690984737859244
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), 1.8432222004
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), 1.8432222004
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), 1.8432222004
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), 1.8432222004
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), 1.1132321566
        )


if __name__ == '__main__':
    unittest.main()
