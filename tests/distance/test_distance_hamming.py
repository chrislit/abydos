# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_hamming.

This module contains unit tests for abydos.distance.Hamming
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Hamming, dist_hamming, hamming, sim_hamming


class HammingTestCases(unittest.TestCase):
    """Test Hamming functions.

    abydos.distance.Hamming
    """

    cmp = Hamming()

    def test_hamming_dist_abs(self):
        """Test abydos.distance.Hamming.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', '', False), 0)

        self.assertEqual(self.cmp.dist_abs('a', ''), 1)
        self.assertEqual(self.cmp.dist_abs('a', 'a'), 0)
        self.assertEqual(self.cmp.dist_abs('a', 'a', False), 0)
        self.assertEqual(self.cmp.dist_abs('a', 'b'), 1)
        self.assertEqual(self.cmp.dist_abs('a', 'b', False), 1)
        self.assertEqual(self.cmp.dist_abs('abc', 'cba'), 2)
        self.assertEqual(self.cmp.dist_abs('abc', 'cba', False), 2)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 3)
        self.assertEqual(self.cmp.dist_abs('bb', 'cbab'), 3)

        # test exception
        self.assertRaises(ValueError, self.cmp.dist_abs, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertEqual(self.cmp.dist_abs('karolin', 'kathrin'), 3)
        self.assertEqual(self.cmp.dist_abs('karolin', 'kerstin'), 3)
        self.assertEqual(self.cmp.dist_abs('1011101', '1001001'), 2)
        self.assertEqual(self.cmp.dist_abs('2173896', '2233796'), 3)

        # Test wrapper
        self.assertEqual(hamming('abc', 'cba', False), 2)

    def test_hamming_dist(self):
        """Test abydos.distance.Hamming.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('', '', False), 0)

        self.assertEqual(self.cmp.dist('a', ''), 1)
        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('a', 'a', False), 0)
        self.assertEqual(self.cmp.dist('a', 'b'), 1)
        self.assertEqual(self.cmp.dist('a', 'b', False), 1)
        self.assertAlmostEqual(self.cmp.dist('abc', 'cba'), 2 / 3)
        self.assertAlmostEqual(self.cmp.dist('abc', 'cba', False), 2 / 3)
        self.assertEqual(self.cmp.dist('abc', ''), 1)
        self.assertAlmostEqual(self.cmp.dist('bb', 'cbab'), 3 / 4)

        # test exception
        self.assertRaises(ValueError, self.cmp.dist, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertAlmostEqual(self.cmp.dist('karolin', 'kathrin'), 3 / 7)
        self.assertAlmostEqual(self.cmp.dist('karolin', 'kerstin'), 3 / 7)
        self.assertAlmostEqual(self.cmp.dist('1011101', '1001001'), 2 / 7)
        self.assertAlmostEqual(self.cmp.dist('2173896', '2233796'), 3 / 7)

        # Test wrapper
        self.assertAlmostEqual(dist_hamming('abc', 'cba'), 2 / 3)

    def test_hamming_sim(self):
        """Test abydos.distance.Hamming.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('', '', False), 1)

        self.assertEqual(self.cmp.sim('a', ''), 0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('a', 'a', False), 1)
        self.assertEqual(self.cmp.sim('a', 'b'), 0)
        self.assertEqual(self.cmp.sim('a', 'b', False), 0)
        self.assertAlmostEqual(self.cmp.sim('abc', 'cba'), 1 / 3)
        self.assertAlmostEqual(self.cmp.sim('abc', 'cba', False), 1 / 3)
        self.assertEqual(self.cmp.sim('abc', ''), 0)
        self.assertAlmostEqual(self.cmp.sim('bb', 'cbab'), 1 / 4)

        # test exception
        self.assertRaises(ValueError, self.cmp.sim, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertAlmostEqual(self.cmp.sim('karolin', 'kathrin'), 4 / 7)
        self.assertAlmostEqual(self.cmp.sim('karolin', 'kerstin'), 4 / 7)
        self.assertAlmostEqual(self.cmp.sim('1011101', '1001001'), 5 / 7)
        self.assertAlmostEqual(self.cmp.sim('2173896', '2233796'), 4 / 7)

        # Test wrapper
        self.assertAlmostEqual(sim_hamming('abc', 'cba'), 1 / 3)


if __name__ == '__main__':
    unittest.main()
