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

"""abydos.tests.distance.test_distance_unknown_i.

This module contains unit tests for abydos.distance.UnknownI
"""

import unittest

from abydos.distance import UnknownI


class UnknownITestCases(unittest.TestCase):
    """Test UnknownI functions.

    abydos.distance.UnknownI
    """

    cmp = UnknownI()

    def test_unknown_i_sim(self):
        """Test abydos.distance.UnknownI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5)
        self.assertEqual(self.cmp.sim('a', ''), 0.2)
        self.assertEqual(self.cmp.sim('', 'a'), 0.2)
        self.assertEqual(self.cmp.sim('abc', ''), 0.125)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.125)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.8333333333333334)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.023809523809523808)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.125)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.125)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.125)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.125)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.1428571429
        )

    def test_unknown_i_dist(self):
        """Test abydos.distance.UnknownI.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.5)
        self.assertEqual(self.cmp.dist('a', ''), 0.8)
        self.assertEqual(self.cmp.dist('', 'a'), 0.8)
        self.assertEqual(self.cmp.dist('abc', ''), 0.875)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.875)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.16666666666666663)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.9761904761904762)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.875)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.875)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.875)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.875)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.8571428571
        )


if __name__ == '__main__':
    unittest.main()
