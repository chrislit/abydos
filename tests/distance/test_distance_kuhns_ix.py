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

"""abydos.tests.distance.test_distance_kuhns_ix.

This module contains unit tests for abydos.distance.KuhnsIX
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsIX


class KuhnsIXTestCases(unittest.TestCase):
    """Test KuhnsIX functions.

    abydos.distance.KuhnsIX
    """

    cmp = KuhnsIX()
    cmp_no_d = KuhnsIX(alphabet=1)

    def test_kuhns_ix_sim(self):
        """Test abydos.distance.KuhnsIX.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0025641025641026)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.0025673940949935813)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.501285347)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.501285347)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.501285347)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.501285347)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6738954188
        )

    def test_kuhns_ix_dist(self):
        """Test abydos.distance.KuhnsIX.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), -0.002564102564102555)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0025673940949935)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.498714653)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.498714653)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.498714653)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.498714653)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3261045812
        )


if __name__ == '__main__':
    unittest.main()