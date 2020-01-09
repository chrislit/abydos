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

"""abydos.tests.distance.test_distance_hassanat.

This module contains unit tests for abydos.distance.Hassanat
"""

import unittest

from collections import Counter

from abydos.distance import Hassanat


class HassanatTestCases(unittest.TestCase):
    """Test Hassanat functions.

    abydos.distance.Hassanat
    """

    cmp = Hassanat()

    def test_hassanat_dist(self):
        """Test abydos.distance.Hassanat.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.3333333333)
        self.assertAlmostEqual(self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.25)

    def test_hassanat_sim(self):
        """Test abydos.distance.Hassanat.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.5)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6666666667)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6666666667)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6666666667)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6666666667)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.75)

    def test_hassanat_dist_abs(self):
        """Test abydos.distance.Hassanat.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 2.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 2.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 5.0)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 3.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 3.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 3.0)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 3.0)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 3.5
        )

        self.assertAlmostEqual(
            self.cmp.dist_abs(
                Counter({'a': -4, 'b': -2}), Counter({'a': -2, 'b': 4})
            ),
            0.8571428571428572,
        )


if __name__ == '__main__':
    unittest.main()
