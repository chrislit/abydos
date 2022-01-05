# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_cao.

This module contains unit tests for abydos.distance.Cao
"""

import unittest

from abydos.distance import Cao


class CaoTestCases(unittest.TestCase):
    """Test Cao functions.

    abydos.distance.Cao
    """

    cmp = Cao()

    def test_cao_sim(self):
        """Test abydos.distance.Cao.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0)

    def test_cao_dist_abs(self):
        """Test abydos.distance.Cao.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertAlmostEqual(self.cmp.dist_abs('a', ''), 0.649453598585)
        self.assertAlmostEqual(self.cmp.dist_abs('', 'a'), 0.649453598585)
        self.assertEqual(self.cmp.dist_abs('a', 'a'), 0.0)
        self.assertAlmostEqual(self.cmp.dist_abs('abc', ''), 0.649453598585)
        self.assertAlmostEqual(self.cmp.dist_abs('', 'abc'), 0.649453598585)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('abcd', 'efgh'), 0.649453598585
        )

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 0.324726799
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 0.324726799
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 0.324726799
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 0.324726799
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 0.21648453286
        )


if __name__ == '__main__':
    unittest.main()
