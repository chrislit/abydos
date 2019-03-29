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

"""abydos.tests.distance.test_distance_peirce.

This module contains unit tests for abydos.distance.Peirce
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Peirce


class PeirceTestCases(unittest.TestCase):
    """Test Peirce functions.

    abydos.distance.Peirce
    """

    cmp = Peirce()
    cmp_no_d = Peirce(alphabet=0)

    def test_peirce_corr(self):
        """Test abydos.distance.Peirce.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), float('nan'))
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), float('nan'))
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.006418485237483954)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.4961439589)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.6324826532
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -0.5)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.3636363636
        )


if __name__ == '__main__':
    unittest.main()
