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

"""abydos.tests.distance.test_distance_chord.

This module contains unit tests for abydos.distance.Chord
"""

import unittest

from abydos.distance import Chord


class ChordTestCases(unittest.TestCase):
    """Test Chord functions.

    abydos.distance.Chord
    """

    cmp = Chord()

    def test_chord_dist(self):
        """Test abydos.distance.Chord.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.707106781186547)
        self.assertEqual(self.cmp.dist('', 'a'), 0.707106781186547)
        self.assertEqual(self.cmp.dist('abc', ''), 0.707106781186547)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.707106781186547)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.7071067812)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.7071067812)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.7071067812)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.7071067812)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5766941889
        )

    def test_chord_sim(self):
        """Test abydos.distance.Chord.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.292893218813453)
        self.assertEqual(self.cmp.sim('', 'a'), 0.292893218813453)
        self.assertEqual(self.cmp.sim('abc', ''), 0.292893218813453)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.292893218813453)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.2928932188)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.2928932188)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.2928932188)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.2928932188)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4233058111
        )

    def test_chord_dist_abs(self):
        """Test abydos.distance.Chord.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 1.414213562373095)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 0.8155687433
        )


if __name__ == '__main__':
    unittest.main()
