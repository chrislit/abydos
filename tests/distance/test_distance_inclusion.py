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

"""abydos.tests.distance.test_distance_inclusion.

This module contains unit tests for abydos.distance.Inclusion
"""

import unittest

from abydos.distance import Inclusion


class InclusionTestCases(unittest.TestCase):
    """Test Inclusion functions.

    abydos.distance.Inclusion
    """

    cmp = Inclusion()

    def test_inclusion_dist(self):
        """Test abydos.distance.Inclusion.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('a', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        # Testcases from paper
        self.assertEqual(self.cmp.dist('ALINE', 'LINA'), 0.0)
        self.assertEqual(self.cmp.dist('ADELINE', 'LINA'), 0.0)
        self.assertEqual(self.cmp.dist('DIONNE', 'DONNE'), 0.0)
        self.assertEqual(self.cmp.dist('ANGELINE', 'ADELINE'), 1.0)
        self.assertEqual(self.cmp.dist('CASSEGRAIN', 'CASGRAIN'), 1.0)

        # coverage
        self.assertEqual(self.cmp.dist('abc', 'abcd'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'abc'), 0.0)


if __name__ == '__main__':
    unittest.main()
