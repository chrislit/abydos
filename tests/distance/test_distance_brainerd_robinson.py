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
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6363636364
        )

    def test_brainerd_robinson_dist(self):
        """Test abydos.distance.BrainerdRobinson.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3636363636
        )

    def test_brainerd_robinson_sim_score(self):
        """Test abydos.distance.BrainerdRobinson.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 200.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 100.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 100.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 100.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 100.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 200.0)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), 100.0)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), 100.0)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 100.0)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 100.0)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 127.2727272727
        )


if __name__ == '__main__':
    unittest.main()
