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

"""abydos.tests.distance.test_distance_size.

This module contains unit tests for abydos.distance.Size
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Size


class SizeTestCases(unittest.TestCase):
    """Test Size functions.

    abydos.distance.Size
    """

    cmp = Size()
    cmp_no_d = Size(alphabet=1)

    def test_size_dist(self):
        """Test abydos.distance.Size.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 6.507705122865473e-06)
        self.assertEqual(self.cmp.dist('', 'a'), 6.507705122865473e-06)
        self.assertEqual(self.cmp.dist('abc', ''), 2.6030820491461892e-05)
        self.assertEqual(self.cmp.dist('', 'abc'), 2.6030820491461892e-05)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.0001626926280716368)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 5.85693e-05)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 5.85693e-05)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 5.85693e-05)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 5.85693e-05)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 7.97194e-05
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.4444444444
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.25
        )


if __name__ == '__main__':
    unittest.main()
