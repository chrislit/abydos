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

"""abydos.tests.distance.test_distance_kuhns_i.

This module contains unit tests for abydos.distance.KuhnsI
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsI


class KuhnsITestCases(unittest.TestCase):
    """Test KuhnsI functions.

    abydos.distance.KuhnsI
    """

    cmp = KuhnsI()
    cmp_no_d = KuhnsI(alphabet=0)

    def test_kuhns_i_sim(self):
        """Test abydos.distance.KuhnsI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.010152019991670138)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -8.134631403581842e-05)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0075359225)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0075359225)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0075359225)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0075359225)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0174992191
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -0.5)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), -0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), -0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), -0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), -0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), -0.1224489796
        )

    def test_kuhns_i_dist(self):
        """Test abydos.distance.KuhnsI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.9898479800083299)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.000081346314036)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.9924640775)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.9924640775)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.9924640775)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.9924640775)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.9825007809
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.5)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 1.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 1.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 1.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 1.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.1224489796
        )


if __name__ == '__main__':
    unittest.main()
