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

"""abydos.tests.distance.test_distance_pearson_iii.

This module contains unit tests for abydos.distance.PearsonIII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import PearsonIII


class PearsonIIITestCases(unittest.TestCase):
    """Test PearsonIII functions.

    abydos.distance.PearsonIII
    """

    cmp = PearsonIII()
    cmp_no_d = PearsonIII(alphabet=0)

    def test_pearson_iii_sim(self):
        """Test abydos.distance.PearsonIII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.03569153051241248)
        self.assertEqual(
            self.cmp.sim('abcd', 'efgh'),
            (1.7520273272936104e-19 + 0.0028612777635371113j),
        )

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0251482893)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0290663533
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(
            self.cmp_no_d.sim('abcd', 'efgh'),
            (2.041077998578922e-17 + 0.3333333333333333j),
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), float('nan')
        )

    def test_pearson_iii_dist(self):
        """Test abydos.distance.PearsonIII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.9643084694875875)
        self.assertEqual(
            self.cmp.dist('abcd', 'efgh'), (1 - 0.0028612777635371113j)
        )

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.9748517107)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.9748517107)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.9748517107)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.9748517107)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.9709336467
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), float('nan'))
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), (1 - 0.3333333333333333j)
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), float('nan')
        )


if __name__ == '__main__':
    unittest.main()
