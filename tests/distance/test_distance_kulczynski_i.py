# -*- coding: utf-8 -*-

# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_kulczynski_i.

This module contains unit tests for abydos.distance.KulczynskiI
"""

import unittest

from abydos.distance import KulczynskiI


class KulczynskiITestCases(unittest.TestCase):
    """Test KulczynskiI functions.

    abydos.distance.KulczynskiI
    """

    cmp = KulczynskiI()

    def test_kulczynski_i_sim_score(self):
        """Test abydos.distance.KulczynskiI.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), float('inf'))
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 1.0
        )

    def test_kulczynski_i_dist(self):
        """Test abydos.distance.KulczynskiI.dist."""
        self.assertRaises(NotImplementedError, self.cmp.dist)

    def test_kulczynski_i_sim(self):
        """Test abydos.distance.KulczynskiI.sim."""
        self.assertRaises(NotImplementedError, self.cmp.sim)


if __name__ == '__main__':
    unittest.main()
