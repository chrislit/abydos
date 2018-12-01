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

"""abydos.tests.distance.test_distance_minkowski.

This module contains unit tests for abydos.distance.Minkowski
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Minkowski, dist_minkowski, minkowski, sim_minkowski
from abydos.tokenizer import QGrams

from .. import NONQ_FROM, NONQ_TO


class MinkowskiTestCases(unittest.TestCase):
    """Test Minkowski functions.

    abydos.distance.Minkowski
    """

    cmp = Minkowski()
    cmp_q2 = Minkowski(tokenizer=QGrams(2))
    cmp_q1p0 = Minkowski(pval=0, tokenizer=QGrams(1))

    def test_minkowski_dist_abs(self):
        """Test abydos.distance.Minkowski.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', ''), 7)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen'), 8)
        self.assertAlmostEqual(self.cmp.dist_abs('nelson', 'neilsen'), 7)

        self.assertEqual(self.cmp_q2.dist_abs('', ''), 0)
        self.assertEqual(self.cmp_q2.dist_abs('nelson', ''), 7)
        self.assertEqual(self.cmp_q2.dist_abs('', 'neilsen'), 8)
        self.assertAlmostEqual(self.cmp_q2.dist_abs('nelson', 'neilsen'), 7)

        # supplied q-gram tests
        self.assertEqual(
            self.cmp.dist_abs(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('').get_counter(),
            ),
            0,
        )
        self.assertEqual(
            self.cmp.dist_abs(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('').get_counter(),
            ),
            7,
        )
        self.assertEqual(
            self.cmp.dist_abs(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            8,
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            7,
        )

        # test l_0 "norm"
        self.assertEqual(self.cmp_q1p0.dist_abs('', ''), 0)
        self.assertEqual(self.cmp_q1p0.dist_abs('a', ''), 1)
        self.assertEqual(self.cmp_q1p0.dist_abs('a', 'b'), 2)
        self.assertEqual(self.cmp_q1p0.dist_abs('ab', 'b'), 1)
        self.assertEqual(self.cmp_q1p0.dist_abs('aab', 'b'), 1)
        self.assertEqual(self.cmp_q1p0.dist_abs('', '', normalized=True), 0)
        self.assertEqual(self.cmp_q1p0.dist_abs('a', '', normalized=True), 1)
        self.assertEqual(self.cmp_q1p0.dist_abs('a', 'b', normalized=True), 1)
        self.assertEqual(
            self.cmp_q1p0.dist_abs('ab', 'b', normalized=True), 1 / 2
        )
        self.assertEqual(
            self.cmp_q1p0.dist_abs('aab', 'b', normalized=True), 1 / 2
        )
        self.assertEqual(
            self.cmp_q1p0.dist_abs('aaab', 'b', normalized=True), 1 / 2
        )
        self.assertEqual(
            self.cmp_q1p0.dist_abs('aaab', 'ab', normalized=True), 1 / 2
        )

        # test with alphabet
        self.assertEqual(
            Minkowski(tokenizer=QGrams(1), alphabet=26).dist_abs('ab', 'b'), 1
        )
        self.assertEqual(
            Minkowski(tokenizer=QGrams(1), alphabet=26).dist_abs(
                'ab', 'b', normalized=True
            ),
            1 / 26,
        )
        self.assertEqual(
            Minkowski(
                tokenizer=QGrams(1), alphabet='abcdefghijklmnopqrstuvwxyz'
            ).dist_abs('ab', 'b', normalized=True),
            1 / 26,
        )

        # Test wrapper
        self.assertAlmostEqual(minkowski('nelson', 'neilsen'), 7)

    def test_minkowski_sim(self):
        """Test abydos.distance.Minkowski.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen'), 8 / 15)

        self.assertEqual(self.cmp_q2.sim('', ''), 1)
        self.assertEqual(self.cmp_q2.sim('nelson', ''), 0)
        self.assertEqual(self.cmp_q2.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp_q2.sim('nelson', 'neilsen'), 8 / 15)

        # supplied q-gram tests
        self.assertEqual(
            self.cmp.sim(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('').get_counter(),
            ),
            1,
        )
        self.assertEqual(
            self.cmp.sim(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('').get_counter(),
            ),
            0,
        )
        self.assertEqual(
            self.cmp.sim(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            0,
        )
        self.assertAlmostEqual(
            self.cmp.sim(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            8 / 15,
        )

        # Test wrapper
        self.assertAlmostEqual(sim_minkowski('nelson', 'neilsen'), 8 / 15)

    def test_minkowski_dist(self):
        """Test abydos.distance.Minkowski.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen'), 7 / 15)

        self.assertEqual(self.cmp_q2.dist('', ''), 0)
        self.assertEqual(self.cmp_q2.dist('nelson', ''), 1)
        self.assertEqual(self.cmp_q2.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp_q2.dist('nelson', 'neilsen'), 7 / 15)

        # supplied q-gram tests
        self.assertEqual(
            self.cmp.dist(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('').get_counter(),
            ),
            0,
        )
        self.assertEqual(
            self.cmp.dist(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('').get_counter(),
            ),
            1,
        )
        self.assertEqual(
            self.cmp.dist(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            1,
        )
        self.assertAlmostEqual(
            self.cmp.dist(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            7 / 15,
        )

        # Test wrapper
        self.assertAlmostEqual(dist_minkowski('nelson', 'neilsen'), 7 / 15)


if __name__ == '__main__':
    unittest.main()
