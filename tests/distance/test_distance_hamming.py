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

This module contains unit tests for abydos.distance._hamming
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import (
    dist_hamming,
    dist_mlipns,
    hamming,
    sim_hamming,
    sim_mlipns,
)


class HammingTestCases(unittest.TestCase):
    """Test Hamming functions.

    abydos.distance._hamming.hamming, .dist_hamming, & .sim_hamming
    """

    def test_hamming(self):
        """Test abydos.distance._hamming.hamming."""
        self.assertEqual(hamming('', ''), 0)
        self.assertEqual(hamming('', '', False), 0)

        self.assertEqual(hamming('a', ''), 1)
        self.assertEqual(hamming('a', 'a'), 0)
        self.assertEqual(hamming('a', 'a', False), 0)
        self.assertEqual(hamming('a', 'b'), 1)
        self.assertEqual(hamming('a', 'b', False), 1)
        self.assertEqual(hamming('abc', 'cba'), 2)
        self.assertEqual(hamming('abc', 'cba', False), 2)
        self.assertEqual(hamming('abc', ''), 3)
        self.assertEqual(hamming('bb', 'cbab'), 3)

        # test exception
        self.assertRaises(ValueError, hamming, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertEqual(hamming('karolin', 'kathrin'), 3)
        self.assertEqual(hamming('karolin', 'kerstin'), 3)
        self.assertEqual(hamming('1011101', '1001001'), 2)
        self.assertEqual(hamming('2173896', '2233796'), 3)

    def test_dist_hamming(self):
        """Test abydos.distance._hamming.dist_hamming."""
        self.assertEqual(dist_hamming('', ''), 0)
        self.assertEqual(dist_hamming('', '', False), 0)

        self.assertEqual(dist_hamming('a', ''), 1)
        self.assertEqual(dist_hamming('a', 'a'), 0)
        self.assertEqual(dist_hamming('a', 'a', False), 0)
        self.assertEqual(dist_hamming('a', 'b'), 1)
        self.assertEqual(dist_hamming('a', 'b', False), 1)
        self.assertAlmostEqual(dist_hamming('abc', 'cba'), 2 / 3)
        self.assertAlmostEqual(dist_hamming('abc', 'cba', False), 2 / 3)
        self.assertEqual(dist_hamming('abc', ''), 1)
        self.assertAlmostEqual(dist_hamming('bb', 'cbab'), 3 / 4)

        # test exception
        self.assertRaises(ValueError, dist_hamming, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertAlmostEqual(dist_hamming('karolin', 'kathrin'), 3 / 7)
        self.assertAlmostEqual(dist_hamming('karolin', 'kerstin'), 3 / 7)
        self.assertAlmostEqual(dist_hamming('1011101', '1001001'), 2 / 7)
        self.assertAlmostEqual(dist_hamming('2173896', '2233796'), 3 / 7)

    def test_sim_hamming(self):
        """Test abydos.distance._hamming.sim_hamming."""
        self.assertEqual(sim_hamming('', ''), 1)
        self.assertEqual(sim_hamming('', '', False), 1)

        self.assertEqual(sim_hamming('a', ''), 0)
        self.assertEqual(sim_hamming('a', 'a'), 1)
        self.assertEqual(sim_hamming('a', 'a', False), 1)
        self.assertEqual(sim_hamming('a', 'b'), 0)
        self.assertEqual(sim_hamming('a', 'b', False), 0)
        self.assertAlmostEqual(sim_hamming('abc', 'cba'), 1 / 3)
        self.assertAlmostEqual(sim_hamming('abc', 'cba', False), 1 / 3)
        self.assertEqual(sim_hamming('abc', ''), 0)
        self.assertAlmostEqual(sim_hamming('bb', 'cbab'), 1 / 4)

        # test exception
        self.assertRaises(ValueError, sim_hamming, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertAlmostEqual(sim_hamming('karolin', 'kathrin'), 4 / 7)
        self.assertAlmostEqual(sim_hamming('karolin', 'kerstin'), 4 / 7)
        self.assertAlmostEqual(sim_hamming('1011101', '1001001'), 5 / 7)
        self.assertAlmostEqual(sim_hamming('2173896', '2233796'), 4 / 7)


class MLIPNSTestCases(unittest.TestCase):
    """Test MLIPNS functions.

    abydos.distance._hamming.sim_mlipns & .dist_mlipns
    """

    def test_sim_mlipns(self):
        """Test abydos.distance._hamming.sim_mlipns."""
        self.assertEqual(sim_mlipns('', ''), 1)
        self.assertEqual(sim_mlipns('a', ''), 0)
        self.assertEqual(sim_mlipns('', 'a'), 0)
        self.assertEqual(sim_mlipns('a', 'a'), 1)
        self.assertEqual(sim_mlipns('ab', 'a'), 1)
        self.assertEqual(sim_mlipns('abc', 'abc'), 1)
        self.assertEqual(sim_mlipns('abc', 'abcde'), 1)
        self.assertEqual(sim_mlipns('abcg', 'abcdeg'), 1)
        self.assertEqual(sim_mlipns('abcg', 'abcdefg'), 0)
        self.assertEqual(sim_mlipns('Tomato', 'Tamato'), 1)
        self.assertEqual(sim_mlipns('ato', 'Tam'), 1)

    def test_dist_mlipns(self):
        """Test abydos.distance._hamming.dist_mlipns."""
        self.assertEqual(dist_mlipns('', ''), 0)
        self.assertEqual(dist_mlipns('a', ''), 1)
        self.assertEqual(dist_mlipns('', 'a'), 1)
        self.assertEqual(dist_mlipns('a', 'a'), 0)
        self.assertEqual(dist_mlipns('ab', 'a'), 0)
        self.assertEqual(dist_mlipns('abc', 'abc'), 0)
        self.assertEqual(dist_mlipns('abc', 'abcde'), 0)
        self.assertEqual(dist_mlipns('abcg', 'abcdeg'), 0)
        self.assertEqual(dist_mlipns('abcg', 'abcdefg'), 1)
        self.assertEqual(dist_mlipns('Tomato', 'Tamato'), 0)
        self.assertEqual(dist_mlipns('ato', 'Tam'), 0)


if __name__ == '__main__':
    unittest.main()
