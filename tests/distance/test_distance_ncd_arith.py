# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_ncd_arith.

This module contains unit tests for abydos.distance.NCDarith
"""

from __future__ import division, unicode_literals

import unittest

from abydos.compression import Arithmetic
from abydos.distance import NCDarith, dist_ncd_arith, sim_ncd_arith

from .. import NIALL


class NCDarithTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.NCDarith
    """

    arith = Arithmetic(' '.join(NIALL))
    cmp = NCDarith()

    def test_dist_ncd_arith(self):
        """Test abydos.distance.NCDarith.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('', '', self.arith.get_probs()), 0)
        self.assertGreater(self.cmp.dist('a', ''), 0)
        self.assertGreater(self.cmp.dist('a', '', self.arith.get_probs()), 0)
        self.assertGreater(self.cmp.dist('abcdefg', 'fg'), 0)

        self.assertAlmostEqual(
            self.cmp.dist('Niall', 'Neil', self.arith.get_probs()),
            0.608695652173913,
        )
        self.assertAlmostEqual(
            self.cmp.dist('Neil', 'Niall', self.arith.get_probs()),
            0.608695652173913,
        )
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Neil'), 0.6875)
        self.assertAlmostEqual(self.cmp.dist('Neil', 'Niall'), 0.6875)
        self.assertAlmostEqual(
            self.cmp.dist('Njáll', 'Njall', self.arith.get_probs()),
            0.714285714285714,
        )
        self.assertAlmostEqual(
            self.cmp.dist('Njall', 'Njáll', self.arith.get_probs()),
            0.714285714285714,
        )
        self.assertAlmostEqual(self.cmp.dist('Njáll', 'Njall'), 0.75)
        self.assertAlmostEqual(self.cmp.dist('Njall', 'Njáll'), 0.75)

        # Test wrapper
        self.assertAlmostEqual(
            dist_ncd_arith('Niall', 'Neil', self.arith.get_probs()),
            0.608695652173913,
        )

    def test_sim_ncd_arith(self):
        """Test abydos.distance._compression.sim_ncd_arith."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('', '', self.arith.get_probs()), 1)
        self.assertLess(self.cmp.sim('a', ''), 1)
        self.assertLess(self.cmp.sim('a', '', self.arith.get_probs()), 1)
        self.assertLess(self.cmp.sim('abcdefg', 'fg'), 1)

        self.assertAlmostEqual(
            self.cmp.sim('Niall', 'Neil', self.arith.get_probs()),
            0.3913043478260869,
        )
        self.assertAlmostEqual(
            self.cmp.sim('Neil', 'Niall', self.arith.get_probs()),
            0.3913043478260869,
        )
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Neil'), 0.3125)
        self.assertAlmostEqual(self.cmp.sim('Neil', 'Niall'), 0.3125)
        self.assertAlmostEqual(
            self.cmp.sim('Njáll', 'Njall', self.arith.get_probs()),
            0.285714285714285,
        )
        self.assertAlmostEqual(
            self.cmp.sim('Njall', 'Njáll', self.arith.get_probs()),
            0.285714285714285,
        )
        self.assertAlmostEqual(self.cmp.sim('Njáll', 'Njall'), 0.25)
        self.assertAlmostEqual(self.cmp.sim('Njall', 'Njáll'), 0.25)

        # Test wrapper
        self.assertAlmostEqual(
            sim_ncd_arith('Niall', 'Neil', self.arith.get_probs()),
            0.3913043478260869,
        )


if __name__ == '__main__':
    unittest.main()
