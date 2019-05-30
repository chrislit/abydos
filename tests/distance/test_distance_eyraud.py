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

"""abydos.tests.distance.test_distance_eyraud.

This module contains unit tests for abydos.distance.Eyraud
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Eyraud


class EyraudTestCases(unittest.TestCase):
    """Test Eyraud functions.

    abydos.distance.Eyraud
    """

    cmp = Eyraud()
    cmp_no_d = Eyraud(alphabet=0)

    def test_eyraud_sim(self):
        """Test abydos.distance.Eyraud.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertAlmostEqual(
            self.cmp.sim('abc', 'abc'), 1.2327416173570019e-06
        )
        self.assertAlmostEqual(
            self.cmp.sim('abcd', 'efgh'), 1.6478781097519779e-06
        )

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 1.5144e-06)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 1.5144e-06)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 1.5144e-06)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 1.5144e-06)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 1.565e-06
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.75)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.04)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.1018518519
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.1018518519
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.1018518519
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.1018518519
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.078030303
        )

    def test_eyraud_dist(self):
        """Test abydos.distance.Eyraud.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('abc', 'abc'), 0.9999987672583827)
        self.assertAlmostEqual(
            self.cmp.dist('abcd', 'efgh'), 0.9999983521218903
        )

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.9999984856)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.9999984856)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.9999984856)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.9999984856)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.999998435
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.25)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 0.96)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.8981481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.8981481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.8981481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.8981481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.921969697
        )

    def test_eyraud_sim_score(self):
        """Test abydos.distance.Eyraud.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertAlmostEqual(
            self.cmp.sim_score('abc', 'abc'), -1.2327416173570019e-06
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('abcd', 'efgh'), -1.6478781097519779e-06
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), -1.5144e-06
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), -1.5144e-06
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), -1.5144e-06
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), -1.5144e-06
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), -1.565e-06
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), -0.75)
        self.assertEqual(self.cmp_no_d.sim_score('abcd', 'efgh'), -0.04)

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), -0.1018518519
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), -0.1018518519
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), -0.1018518519
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), -0.1018518519
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), -0.078030303
        )


if __name__ == '__main__':
    unittest.main()
