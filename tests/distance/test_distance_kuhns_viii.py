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

"""abydos.tests.distance.test_distance_kuhns_viii.

This module contains unit tests for abydos.distance.KuhnsVIII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsVIII


class KuhnsVIIITestCases(unittest.TestCase):
    """Test KuhnsVIII functions.

    abydos.distance.KuhnsVIII
    """

    cmp = KuhnsVIII()
    cmp_no_d = KuhnsVIII(alphabet=1)

    def test_kuhns_viii_sim(self):
        """Test abydos.distance.KuhnsVIII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), -0.002551020408163265)
        self.assertEqual(self.cmp.sim('', 'a'), -0.002551020408163265)
        self.assertEqual(self.cmp.sim('abc', ''), -0.002551020408163265)
        self.assertEqual(self.cmp.sim('', 'abc'), -0.002551020408163265)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9974489795918368)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.0025510204081632655)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4974489796)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6641156463
        )

    def test_kuhns_viii_dist(self):
        """Test abydos.distance.KuhnsVIII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), 1.0025510204081634)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0025510204081634)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0025510204081634)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0025510204081634)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0025510204081632404)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0025510204081634)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5025510204)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5025510204)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5025510204)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5025510204)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3358843537
        )


if __name__ == '__main__':
    unittest.main()
