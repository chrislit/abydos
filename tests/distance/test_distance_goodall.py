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

"""abydos.tests.distance.test_distance_goodall.

This module contains unit tests for abydos.distance.Goodall
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Goodall


class GoodallTestCases(unittest.TestCase):
    """Test Goodall functions.

    abydos.distance.Goodall
    """

    cmp = Goodall()
    cmp_no_d = Goodall(alphabet=1)

    def test_goodall_sim(self):
        """Test abydos.distance.Goodall.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9678321591500222)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9678321591500222)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9544884026871964)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9544884026871964)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9279473952929225)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9442360891)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9442360891)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9442360891)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9442360891)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.939755208
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.391826552
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.391826552
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.391826552
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.391826552
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5
        )


if __name__ == '__main__':
    unittest.main()
