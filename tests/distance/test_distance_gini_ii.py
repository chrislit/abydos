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

"""abydos.tests.distance.test_distance_gini_ii.

This module contains unit tests for abydos.distance.GiniII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import GiniII


class GiniIITestCases(unittest.TestCase):
    """Test GiniII functions.

    abydos.distance.GiniII
    """

    cmp = GiniII()
    cmp_no_d = GiniII(alphabet=0)

    def test_gini_ii_sim(self):
        """Test abydos.distance.GiniII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), 0.9987228607918263)
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), 0.998719590268886)
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9987064918137779)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -1.9993186235767724)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9987049082)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4935594778)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9987049082)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4935594778)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9986833103
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), float('nan'))

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

    def test_gini_ii_dist(self):
        """Test abydos.distance.GiniII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.496505552665505)
        self.assertEqual(self.cmp.dist('a', ''), 0.0012950931497246465)
        self.assertEqual(self.cmp.dist('', 'a'), 0.4971440967783952)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0012984095896947379)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.49778428543942865)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.001311692182679569)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.24312685823360403)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0013132978)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4958438698)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0013132978)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.4958438698)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0013351992
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), float('nan'))

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
