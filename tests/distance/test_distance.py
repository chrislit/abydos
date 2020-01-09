# -*- coding: utf-8 -*-

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

"""abydos.tests.distance.test_distance.

This module contains unit tests for abydos.distance
"""

import unittest

from abydos.distance import dist, sim
from abydos.distance import dist_levenshtein, sim_levenshtein


class SimDistTestCases(unittest.TestCase):
    """Test generic sim & dist functions.

    abydos.distance.sim & .dist
    """

    def test_sim(self):
        """Test abydos.distance.sim."""
        self.assertEqual(
            sim('Niall', 'Nigel'), sim_levenshtein('Niall', 'Nigel')
        )
        self.assertRaises(AttributeError, sim, 'abc', 'abc', 0)

    def test_dist(self):
        """Test abydos.distance.dist."""
        self.assertEqual(
            dist('Niall', 'Nigel'), dist_levenshtein('Niall', 'Nigel')
        )
        self.assertRaises(AttributeError, dist, 'abc', 'abc', 0)


if __name__ == '__main__':
    unittest.main()
