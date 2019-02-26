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

"""abydos.tests.distance.test_distance_pearson_ii.

This module contains unit tests for abydos.distance.PearsonII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import PearsonII


class PearsonIITestCases(unittest.TestCase):
    """Test PearsonII functions.

    abydos.distance.PearsonII
    """

    cmp = PearsonII()
    cmp_no_d = PearsonII(alphabet=0)

    def test_pearson_ii_sim(self):
        """Test abydos.distance.PearsonII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.7071067811865476)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.006418353030552324)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4444480535)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4444480535)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4444480535)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4444480535)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5525391276
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.7071067811865476)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.4472135955
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.4472135955
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.4472135955
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.4472135955
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.3136250241
        )

    def test_pearson_ii_dist(self):
        """Test abydos.distance.PearsonII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.2928932188134524)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.9935816469694477)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5555519465)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5555519465)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5555519465)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5555519465)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4474608724
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), float('nan'))
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.2928932188134524
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.5527864045
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.5527864045
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.5527864045
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.5527864045
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.6863749759
        )


if __name__ == '__main__':
    unittest.main()
