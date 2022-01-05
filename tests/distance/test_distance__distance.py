# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance__distance.

This module contains unit tests for abydos.distance._Distance
"""

import unittest

from abydos.distance import Dice, Levenshtein


class DistanceTestCases(unittest.TestCase):
    """Test _Distance base class.

    abydos.distance._Distance.sim, .dist, & .dist_abs
    """

    lev = Levenshtein()
    dice = Dice()

    def test_sim(self):
        """Test abydos.distance._Distance.sim."""
        self.assertEqual(
            self.lev.sim('Niall', 'Nigel'),
            1.0 - self.lev.dist('Niall', 'Nigel'),
        )
        self.assertEqual(
            self.dice.dist('Niall', 'Nigel'),
            1.0 - self.dice.sim('Niall', 'Nigel'),
        )

    def test_dist(self):
        """Test abydos.distance._Distance.dist."""
        self.assertEqual(
            1.0 - self.lev.sim('Niall', 'Nigel'),
            self.lev.dist('Niall', 'Nigel'),
        )
        self.assertEqual(
            1.0 - self.dice.dist('Niall', 'Nigel'),
            self.dice.sim('Niall', 'Nigel'),
        )

    def test_dist_abs(self):
        """Test abydos.distance._Distance.dist_abs."""
        self.assertEqual(
            self.dice.dist('Niall', 'Nigel'),
            self.dice.dist_abs('Niall', 'Nigel'),
        )


if __name__ == '__main__':
    unittest.main()
