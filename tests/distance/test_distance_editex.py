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

"""abydos.tests.distance.test_distance_editex.

This module contains unit tests for abydos.distance.Editex
"""

import unittest

from abydos.distance import Editex, dist_editex, editex, sim_editex


class EditexTestCases(unittest.TestCase):
    """Test Editex functions.

    abydos.distance.Editex
    """

    cmp = Editex()
    cmp_local = Editex(local=True)
    cmp_taper = Editex(taper=True)

    def test_editex_dist_abs(self):
        """Test abydos.distance.Editex.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', ''), 12)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen'), 14)
        self.assertEqual(self.cmp.dist_abs('ab', 'a'), 2)
        self.assertEqual(self.cmp.dist_abs('ab', 'c'), 4)
        self.assertEqual(self.cmp.dist_abs('nelson', 'neilsen'), 2)
        self.assertEqual(self.cmp.dist_abs('neilsen', 'nelson'), 2)
        self.assertEqual(self.cmp.dist_abs('niall', 'neal'), 1)
        self.assertEqual(self.cmp.dist_abs('neal', 'niall'), 1)
        self.assertEqual(self.cmp.dist_abs('niall', 'nihal'), 2)
        self.assertEqual(self.cmp.dist_abs('nihal', 'niall'), 2)
        self.assertEqual(self.cmp.dist_abs('neal', 'nihl'), 3)
        self.assertEqual(self.cmp.dist_abs('nihl', 'neal'), 3)

        # Test tapering variant
        self.assertAlmostEqual(
            self.cmp_taper.dist_abs('nelson', 'neilsen'), 2.7142857143
        )

        # Test wrapper
        self.assertEqual(editex('niall', 'neal'), 1)

    def test_editex_dist_abs_local(self):
        """Test abydos.distance.Editex.dist_abs (local variant)."""
        self.assertEqual(self.cmp_local.dist_abs('', ''), 0)
        self.assertEqual(self.cmp_local.dist_abs('nelson', ''), 12)
        self.assertEqual(self.cmp_local.dist_abs('', 'neilsen'), 14)
        self.assertEqual(self.cmp_local.dist_abs('ab', 'a'), 2)
        self.assertEqual(self.cmp_local.dist_abs('ab', 'c'), 2)
        self.assertEqual(self.cmp_local.dist_abs('nelson', 'neilsen'), 2)
        self.assertEqual(self.cmp_local.dist_abs('neilsen', 'nelson'), 2)
        self.assertEqual(self.cmp_local.dist_abs('niall', 'neal'), 1)
        self.assertEqual(self.cmp_local.dist_abs('neal', 'niall'), 1)
        self.assertEqual(self.cmp_local.dist_abs('niall', 'nihal'), 2)
        self.assertEqual(self.cmp_local.dist_abs('nihal', 'niall'), 2)
        self.assertEqual(self.cmp_local.dist_abs('neal', 'nihl'), 3)
        self.assertEqual(self.cmp_local.dist_abs('nihl', 'neal'), 3)

        # Test wrapper
        self.assertEqual(editex('niall', 'neal', local=True), 1)

    def test_editex_sim(self):
        """Test abydos.distance.Editex.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertEqual(self.cmp.sim('ab', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('ab', 'c'), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen'), 12 / 14)
        self.assertAlmostEqual(self.cmp.sim('neilsen', 'nelson'), 12 / 14)
        self.assertEqual(self.cmp.sim('niall', 'neal'), 0.9)

        # Test wrapper
        self.assertEqual(sim_editex('niall', 'neal'), 0.9)

    def test_editex_dist(self):
        """Test abydos.distance.Editex.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertEqual(self.cmp.dist('ab', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('ab', 'c'), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen'), 2 / 14)
        self.assertAlmostEqual(self.cmp.dist('neilsen', 'nelson'), 2 / 14)
        self.assertEqual(self.cmp.dist('niall', 'neal'), 0.1)

        # Test tapering variant
        self.assertAlmostEqual(
            self.cmp_taper.dist('nelson', 'neilsen'), 0.123376623
        )

        # Test wrapper
        self.assertEqual(dist_editex('niall', 'neal'), 0.1)


if __name__ == '__main__':
    unittest.main()
