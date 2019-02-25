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

"""abydos.tests.distance.test_distance_fossum.

This module contains unit tests for abydos.distance.Fossum
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Fossum


class FossumTestCases(unittest.TestCase):
    """Test Fossum functions.

    abydos.distance.Fossum
    """

    cmp = Fossum()
    cmp_no_d = Fossum(alphabet=0)

    def test_fossum_sim(self):
        """Test abydos.distance.Fossum.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 600.25)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 7.84)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 136.1111111111)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 136.1111111111)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 136.1111111111)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 136.1111111111)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 301.1272727273
        )

    def test_fossum_dist(self):
        """Test abydos.distance.Fossum.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), -599.25)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), -6.84)

        self.assertAlmostEqual(
            self.cmp.dist('Nigel', 'Niall'), -135.1111111111
        )
        self.assertAlmostEqual(
            self.cmp.dist('Niall', 'Nigel'), -135.1111111111
        )
        self.assertAlmostEqual(
            self.cmp.dist('Colin', 'Coiln'), -135.1111111111
        )
        self.assertAlmostEqual(
            self.cmp.dist('Coiln', 'Colin'), -135.1111111111
        )
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), -300.1272727273
        )


if __name__ == '__main__':
    unittest.main()
