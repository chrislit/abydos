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

"""abydos.tests.distance.test_distance_mutual_information.

This module contains unit tests for abydos.distance.MutualInformation
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import MutualInformation


class MutualInformationTestCases(unittest.TestCase):
    """Test MutualInformation functions.

    abydos.distance.MutualInformation
    """

    cmp = MutualInformation()
    cmp_no_d = MutualInformation(alphabet=1)

    def test_mutual_information_sim(self):
        """Test abydos.distance.MutualInformation.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 7.6147098441152075)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), float('nan'))

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 6.0297473434)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 6.0297473434)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 6.0297473434)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 6.0297473434)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 5.6407050526
        )

    def test_mutual_information_dist(self):
        """Test abydos.distance.MutualInformation.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), -6.6147098441152075)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), float('nan'))

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), -5.0297473434)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), -5.0297473434)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), -5.0297473434)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), -5.0297473434)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), -4.6407050526
        )


if __name__ == '__main__':
    unittest.main()
