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

"""abydos.tests.distance.test_distance_manhattan.

This module contains unit tests for abydos.distance.Manhattan
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Manhattan, dist_manhattan, manhattan, sim_manhattan
from abydos.tokenizer import QGrams

from .. import NONQ_FROM, NONQ_TO


class ManhattanTestCases(unittest.TestCase):
    """Test Manhattan functions.

    abydos.distance.Manhattan
    """

    cmp = Manhattan()

    def test_manhattan_dist_abs(self):
        """Test abydos.distance.Manhattan.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', ''), 7)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen'), 8)
        self.assertAlmostEqual(self.cmp.dist_abs('nelson', 'neilsen'), 7)

        self.assertEqual(self.cmp.dist_abs('', '', 2), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', '', 2), 7)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen', 2), 8)
        self.assertAlmostEqual(self.cmp.dist_abs('nelson', 'neilsen', 2), 7)

        # supplied q-gram tests
        self.assertEqual(self.cmp.dist_abs(QGrams(''), QGrams('')), 0)
        self.assertEqual(self.cmp.dist_abs(QGrams('nelson'), QGrams('')), 7)
        self.assertEqual(self.cmp.dist_abs(QGrams(''), QGrams('neilsen')), 8)
        self.assertAlmostEqual(
            self.cmp.dist_abs(QGrams('nelson'), QGrams('neilsen')), 7
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.dist_abs('', '', 0), 0)
        self.assertEqual(self.cmp.dist_abs('the quick', '', 0), 2)
        self.assertEqual(self.cmp.dist_abs('', 'the quick', 0), 2)
        self.assertAlmostEqual(self.cmp.dist_abs(NONQ_FROM, NONQ_TO, 0), 8)
        self.assertAlmostEqual(self.cmp.dist_abs(NONQ_TO, NONQ_FROM, 0), 8)

        # Test wrapper
        self.assertAlmostEqual(manhattan('nelson', 'neilsen'), 7)

    def test_manhattan_sim(self):
        """Test abydos.distance.Manhattan.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen'), 8 / 15)

        self.assertEqual(self.cmp.sim('', '', 2), 1)
        self.assertEqual(self.cmp.sim('nelson', '', 2), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen', 2), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen', 2), 8 / 15)

        # supplied q-gram tests
        self.assertEqual(self.cmp.sim(QGrams(''), QGrams('')), 1)
        self.assertEqual(self.cmp.sim(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(self.cmp.sim(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(
            self.cmp.sim(QGrams('nelson'), QGrams('neilsen')), 8 / 15
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.sim('', '', 0), 1)
        self.assertEqual(self.cmp.sim('the quick', '', 0), 0)
        self.assertEqual(self.cmp.sim('', 'the quick', 0), 0)
        self.assertAlmostEqual(self.cmp.sim(NONQ_FROM, NONQ_TO, 0), 1 / 2)
        self.assertAlmostEqual(self.cmp.sim(NONQ_TO, NONQ_FROM, 0), 1 / 2)

        # Test wrapper
        self.assertAlmostEqual(sim_manhattan('nelson', 'neilsen'), 8 / 15)

    def test_manhattan_dist(self):
        """Test abydos.distance.Manhattan.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen'), 7 / 15)

        self.assertEqual(self.cmp.dist('', '', 2), 0)
        self.assertEqual(self.cmp.dist('nelson', '', 2), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen', 2), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen', 2), 7 / 15)

        # supplied q-gram tests
        self.assertEqual(self.cmp.dist(QGrams(''), QGrams('')), 0)
        self.assertEqual(self.cmp.dist(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(self.cmp.dist(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            self.cmp.dist(QGrams('nelson'), QGrams('neilsen')), 7 / 15
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.dist('', '', 0), 0)
        self.assertEqual(self.cmp.dist('the quick', '', 0), 1)
        self.assertEqual(self.cmp.dist('', 'the quick', 0), 1)
        self.assertAlmostEqual(self.cmp.dist(NONQ_FROM, NONQ_TO, 0), 1 / 2)
        self.assertAlmostEqual(self.cmp.dist(NONQ_TO, NONQ_FROM, 0), 1 / 2)

        # Test wrapper
        self.assertAlmostEqual(dist_manhattan('nelson', 'neilsen'), 7 / 15)


if __name__ == '__main__':
    unittest.main()
