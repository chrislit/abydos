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

"""abydos.tests.distance.test_distance_complete_linkage.

This module contains unit tests for abydos.distance.CompleteLinkage
"""

import unittest

from abydos.distance import CompleteLinkage, JaroWinkler
from abydos.tokenizer import QGrams


class CompleteLinkageTestCases(unittest.TestCase):
    """Test CompleteLinkage functions.

    abydos.distance.CompleteLinkage
    """

    cmp = CompleteLinkage()
    cmp_q4 = CompleteLinkage(tokenizer=QGrams(qval=4, start_stop=''))
    cmp_q4_jw = CompleteLinkage(
        tokenizer=QGrams(qval=4, start_stop=''), metric=JaroWinkler()
    )

    def test_complete_linkage_dist(self):
        """Test abydos.distance.CompleteLinkage.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 1.0)

        self.assertEqual(self.cmp_q4.dist('AAAT', 'AATT'), 0.25)
        self.assertAlmostEqual(
            self.cmp_q4_jw.dist('AAAT', 'AATT'), 0.133333333333
        )

    def test_complete_linkage_sim(self):
        """Test abydos.distance.CompleteLinkage.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0)

    def test_complete_linkage_dist_abs(self):
        """Test abydos.distance.CompleteLinkage.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), float('-inf'))
        self.assertEqual(self.cmp.dist_abs('a', ''), float('-inf'))
        self.assertEqual(self.cmp.dist_abs('', 'a'), float('-inf'))
        self.assertEqual(self.cmp.dist_abs('abc', ''), float('-inf'))
        self.assertEqual(self.cmp.dist_abs('', 'abc'), float('-inf'))
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 2)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 2)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 2)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 2)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 2)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 2)
        self.assertAlmostEqual(self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 2)


if __name__ == '__main__':
    unittest.main()
