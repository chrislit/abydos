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

"""abydos.tests.distance.test_distance_soft_cosine.

This module contains unit tests for abydos.distance.SoftCosine
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import SoftCosine


class SoftCosineTestCases(unittest.TestCase):
    """Test SoftCosine functions.

    abydos.distance.SoftCosine
    """

    cmp = SoftCosine()

    def test_soft_cosine_sim(self):
        """Test abydos.distance.SoftCosine.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.7428571428571427)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.898146239)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.898146239)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9375)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9375)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9731507012
        )

    def test_soft_cosine_dist(self):
        """Test abydos.distance.SoftCosine.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.25714285714285734)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.101853761)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.101853761)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0625)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0625)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0268492988
        )


if __name__ == '__main__':
    unittest.main()
