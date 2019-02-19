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

"""abydos.tests.distance.test_distance_brainerd_robinson.

This module contains unit tests for abydos.distance.BrainerdRobinson
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import BrainerdRobinson


class BrainerdRobinsonTestCases(unittest.TestCase):
    """Test BrainerdRobinson functions.

    abydos.distance.BrainerdRobinson
    """

    cmp = BrainerdRobinson()

    def test_brainerd_robinson_sim(self):
        """Test abydos.distance.BrainerdRobinson.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 1.4210854715202004e-16)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6363636364
        )

    def test_brainerd_robinson_sim_abs(self):
        """Test abydos.distance.BrainerdRobinson.sim_abs."""
        # Base cases
        self.assertEqual(self.cmp.sim_abs('', ''), 200)
        self.assertEqual(self.cmp.sim_abs('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim_abs('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim_abs('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim_abs('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim_abs('abc', 'abc'), 200.0)
        self.assertEqual(
            self.cmp.sim_abs('abcd', 'efgh'), 2.842170943040401e-14
        )

        self.assertAlmostEqual(self.cmp.sim_abs('Nigel', 'Niall'), 100.0)
        self.assertAlmostEqual(self.cmp.sim_abs('Niall', 'Nigel'), 100.0)
        self.assertAlmostEqual(self.cmp.sim_abs('Colin', 'Coiln'), 100.0)
        self.assertAlmostEqual(self.cmp.sim_abs('Coiln', 'Colin'), 100.0)
        self.assertAlmostEqual(
            self.cmp.sim_abs('ATCAACGAGT', 'AACGATTAG'), 127.2727272727
        )


if __name__ == '__main__':
    unittest.main()
