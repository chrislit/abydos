# Copyright 2014-2020 by Christopher C. Little.
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

import unittest

from abydos.compression import Arithmetic
from abydos.distance import NCDarith

from .. import NIALL


class NCDarithTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.NCDarith
    """

    arith = Arithmetic(' '.join(NIALL))
    cmp = NCDarith()
    cmp_probs = NCDarith(arith.get_probs())

    def test_ncd_arith_dist(self):
        """Test abydos.distance.NCDarith.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp_probs.dist('', ''), 0)
        self.assertGreater(self.cmp.dist('a', ''), 0)
        self.assertGreater(self.cmp_probs.dist('a', ''), 0)
        self.assertGreater(self.cmp.dist('abcdefg', 'fg'), 0)

        self.assertAlmostEqual(
            self.cmp_probs.dist('Niall', 'Neil'), 0.608695652173913
        )
        self.assertAlmostEqual(
            self.cmp_probs.dist('Neil', 'Niall'), 0.608695652173913
        )
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Neil'), 0.6875)
        self.assertAlmostEqual(self.cmp.dist('Neil', 'Niall'), 0.6875)
        self.assertAlmostEqual(
            self.cmp_probs.dist('Njáll', 'Njall'), 0.714285714285714
        )
        self.assertAlmostEqual(
            self.cmp_probs.dist('Njall', 'Njáll'), 0.714285714285714
        )
        self.assertAlmostEqual(self.cmp.dist('Njáll', 'Njall'), 0.75)
        self.assertAlmostEqual(self.cmp.dist('Njall', 'Njáll'), 0.75)

    def test_ncd_arith_sim(self):
        """Test abydos.distance.NCDarith.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp_probs.sim('', ''), 1)
        self.assertLess(self.cmp.sim('a', ''), 1)
        self.assertLess(self.cmp_probs.sim('a', ''), 1)
        self.assertLess(self.cmp.sim('abcdefg', 'fg'), 1)

        self.assertAlmostEqual(
            self.cmp_probs.sim('Niall', 'Neil'), 0.3913043478260869
        )
        self.assertAlmostEqual(
            self.cmp_probs.sim('Neil', 'Niall'), 0.3913043478260869
        )
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Neil'), 0.3125)
        self.assertAlmostEqual(self.cmp.sim('Neil', 'Niall'), 0.3125)
        self.assertAlmostEqual(
            self.cmp_probs.sim('Njáll', 'Njall'), 0.285714285714285
        )
        self.assertAlmostEqual(
            self.cmp_probs.sim('Njall', 'Njáll'), 0.285714285714285
        )
        self.assertAlmostEqual(self.cmp.sim('Njáll', 'Njall'), 0.25)
        self.assertAlmostEqual(self.cmp.sim('Njall', 'Njáll'), 0.25)


if __name__ == '__main__':
    unittest.main()
