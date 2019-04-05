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

"""abydos.tests.distance.test_distance_unknown_m.

This module contains unit tests for abydos.distance.UnknownM
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import UnknownM


class UnknownMTestCases(unittest.TestCase):
    """Test UnknownM functions.

    abydos.distance.UnknownM
    """

    cmp = UnknownM()
    cmp_no_d = UnknownM(alphabet=0)

    def test_unknown_m_sim(self):
        """Test abydos.distance.UnknownM.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.14599478380307845)
        self.assertEqual(self.cmp.sim('', 'a'), 0.14599478380307845)
        self.assertEqual(self.cmp.sim('abc', ''), 0.24935979408619846)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.24935979408619846)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.8743589743589744)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.3993581514762516)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6650599829)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6650599829)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6650599829)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6650599829)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7838816809
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.3)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.25)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.3073313411
        )

    def test_unknown_m_dist(self):
        """Test abydos.distance.UnknownM.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.8540052161969216)
        self.assertEqual(self.cmp.dist('', 'a'), 0.8540052161969216)
        self.assertEqual(self.cmp.dist('abc', ''), 0.7506402059138015)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.7506402059138015)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.12564102564102564)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.6006418485237484)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3349400171)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3349400171)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.3349400171)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.3349400171)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2161183191
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 0.7)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.75)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.6926686589
        )

    def test_unknown_m_sim_score(self):
        """Test abydos.distance.UnknownM.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 1.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.7080104323938431)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.7080104323938431)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.5012804118276031)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.5012804118276031)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), -0.7487179487179487)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), 0.2012836970474968
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), -0.3301199657
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), -0.3301199657
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), -0.3301199657
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), -0.3301199657
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), -0.5677633618
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim_score('abcd', 'efgh'), 0.4)

        self.assertAlmostEqual(self.cmp_no_d.sim_score('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.3853373178
        )


if __name__ == '__main__':
    unittest.main()
