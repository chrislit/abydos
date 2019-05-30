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

"""abydos.tests.distance.test_distance_average_linkage.

This module contains unit tests for abydos.distance.AverageLinkage
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import AverageLinkage, Prefix
from abydos.tokenizer import QGrams


class AverageLinkageTestCases(unittest.TestCase):
    """Test AverageLinkage functions.

    abydos.distance.AverageLinkage
    """

    cmp = AverageLinkage()
    cmp1 = AverageLinkage(tokenizer=QGrams(1))
    cmp_pfx = AverageLinkage(metric=Prefix())

    def test_average_linkage_dist(self):
        """Test abydos.distance.AverageLinkage.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.75)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.96)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.8611111111)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.8611111111)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.8333333333)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.8333333333)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.7545454545
        )

        self.assertEqual(self.cmp1.dist('aaa', 'aaa'), 0.0)
        self.assertAlmostEqual(self.cmp_pfx.dist('ababab', 'ab'), 0.714285714)


if __name__ == '__main__':
    unittest.main()
