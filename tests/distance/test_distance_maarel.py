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

"""abydos.tests.distance.test_distance_maarel.

This module contains unit tests for abydos.distance.Maarel
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Maarel


class MaarelTestCases(unittest.TestCase):
    """Test Maarel functions.

    abydos.distance.Maarel
    """

    cmp = Maarel()
    cmp_no_d = Maarel(alphabet=0)

    def test_maarel_sim(self):
        """Test abydos.distance.Maarel.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), -1.0)
        self.assertEqual(self.cmp.sim('', 'a'), -1.0)
        self.assertEqual(self.cmp.sim('abc', ''), -1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), -1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.3333333333
        )

    def test_maarel_dist(self):
        """Test abydos.distance.Maarel.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), 2.0)
        self.assertEqual(self.cmp.dist('', 'a'), 2.0)
        self.assertEqual(self.cmp.dist('abc', ''), 2.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 2.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.6666666667
        )


if __name__ == '__main__':
    unittest.main()
