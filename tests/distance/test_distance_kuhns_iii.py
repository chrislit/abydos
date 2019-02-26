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

"""abydos.tests.distance.test_distance_kuhns_iii.

This module contains unit tests for abydos.distance.KuhnsIII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsIII


class KuhnsIIITestCases(unittest.TestCase):
    """Test KuhnsIII functions.

    abydos.distance.KuhnsIII
    """

    cmp = KuhnsIII()
    cmp_no_d = KuhnsIII(alphabet=0)

    def test_kuhns_iii_sim(self):
        """Test abydos.distance.KuhnsIII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), -0.0012755102040816326)
        self.assertEqual(self.cmp.sim('', 'a'), -0.0012755102040816326)
        self.assertEqual(self.cmp.sim('abc', ''), -0.0012755102040816326)
        self.assertEqual(self.cmp.sim('', 'abc'), -0.0012755102040816326)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.0012795905310300703)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.3329065301)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.3329065301)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.3329065301)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.3329065301)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5014369573
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), -0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), -0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), -0.25)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), -0.25)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(
            self.cmp_no_d.sim('abcd', 'efgh'), -0.13333333333333333
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.2777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.2777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.2777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.2777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.6277173913
        )

    def test_kuhns_iii_dist(self):
        """Test abydos.distance.KuhnsIII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), 1.0012755102040816)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0012755102040816)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0012755102040816)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0012755102040816)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.00127959053103)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.6670934699)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.6670934699)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.6670934699)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.6670934699)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4985630427
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.25)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.25)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 1.1333333333333333
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.7222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.7222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.7222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.7222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.3722826087
        )


if __name__ == '__main__':
    unittest.main()
