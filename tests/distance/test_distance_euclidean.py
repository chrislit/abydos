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

"""abydos.tests.distance.test_distance_euclidean.

This module contains unit tests for abydos.distance.Euclidean
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import (
    Euclidean,
    dist_euclidean,
    euclidean,
    sim_euclidean,
)
from abydos.tokenizer import QGrams

from .. import NONQ_FROM, NONQ_TO


class EuclideanTestCases(unittest.TestCase):
    """Test Euclidean functions.

    abydos.distance.Euclidean
    """
    cmp = Euclidean()

    def test_euclidean_dist_abs(self):
        """Test abydos.distance.Euclidean.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', ''), 7 ** 0.5)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen'), 8 ** 0.5)
        self.assertAlmostEqual(self.cmp.dist_abs('nelson', 'neilsen'), 7 ** 0.5)

        self.assertEqual(self.cmp.dist_abs('', '', 2), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', '', 2), 7 ** 0.5)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen', 2), 8 ** 0.5)
        self.assertAlmostEqual(self.cmp.dist_abs('nelson', 'neilsen', 2), 7 ** 0.5)

        # supplied q-gram tests
        self.assertEqual(self.cmp.dist_abs(QGrams(''), QGrams('')), 0)
        self.assertEqual(self.cmp.dist_abs(QGrams('nelson'), QGrams('')), 7 ** 0.5)
        self.assertEqual(self.cmp.dist_abs(QGrams(''), QGrams('neilsen')), 8 ** 0.5)
        self.assertAlmostEqual(
            self.cmp.dist_abs(QGrams('nelson'), QGrams('neilsen')), 7 ** 0.5
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.dist_abs('', '', 0), 0)
        self.assertEqual(self.cmp.dist_abs('the quick', '', 0), 2 ** 0.5)
        self.assertEqual(self.cmp.dist_abs('', 'the quick', 0), 2 ** 0.5)
        self.assertAlmostEqual(self.cmp.dist_abs(NONQ_FROM, NONQ_TO, 0), 8 ** 0.5)
        self.assertAlmostEqual(self.cmp.dist_abs(NONQ_TO, NONQ_FROM, 0), 8 ** 0.5)

        # Test wrapper
        self.assertAlmostEqual(euclidean('nelson', 'neilsen'), 7 ** 0.5)

    def test_euclidean_sim(self):
        """Test abydos.distance.Euclidean.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(
            self.cmp.sim('nelson', 'neilsen'), 1 - 7 ** 0.5 / 23 ** 0.5
        )

        self.assertEqual(self.cmp.sim('', '', 2), 1)
        self.assertEqual(self.cmp.sim('nelson', '', 2), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen', 2), 0)
        self.assertAlmostEqual(
            self.cmp.sim('nelson', 'neilsen', 2), 1 - 7 ** 0.5 / 23 ** 0.5
        )

        # supplied q-gram tests
        self.assertEqual(self.cmp.sim(QGrams(''), QGrams('')), 1)
        self.assertEqual(self.cmp.sim(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(self.cmp.sim(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(
            self.cmp.sim(QGrams('nelson'), QGrams('neilsen')),
            1 - 7 ** 0.5 / 23 ** 0.5,
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.sim('', '', 0), 1)
        self.assertEqual(self.cmp.sim('the quick', '', 0), 0)
        self.assertEqual(self.cmp.sim('', 'the quick', 0), 0)
        self.assertAlmostEqual(
            self.cmp.sim(NONQ_FROM, NONQ_TO, 0), 1 - 8 ** 0.5 / 24 ** 0.5
        )
        self.assertAlmostEqual(
            self.cmp.sim(NONQ_TO, NONQ_FROM, 0), 1 - 8 ** 0.5 / 24 ** 0.5
        )

        # Test wrapper
        self.assertAlmostEqual(
            sim_euclidean('nelson', 'neilsen'), 1 - 7 ** 0.5 / 23 ** 0.5
        )

    def test_euclidean_dist(self):
        """Test abydos.distance.Euclidean.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(
            self.cmp.dist('nelson', 'neilsen'), 7 ** 0.5 / 23 ** 0.5
        )

        self.assertEqual(self.cmp.dist('', '', 2), 0)
        self.assertEqual(self.cmp.dist('nelson', '', 2), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen', 2), 1)
        self.assertAlmostEqual(
            self.cmp.dist('nelson', 'neilsen', 2), 7 ** 0.5 / 23 ** 0.5
        )

        # supplied q-gram tests
        self.assertEqual(self.cmp.dist(QGrams(''), QGrams('')), 0)
        self.assertEqual(self.cmp.dist(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(self.cmp.dist(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            self.cmp.dist(QGrams('nelson'), QGrams('neilsen')),
            7 ** 0.5 / 23 ** 0.5,
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.dist('', '', 0), 0)
        self.assertEqual(self.cmp.dist('the quick', '', 0), 1)
        self.assertEqual(self.cmp.dist('', 'the quick', 0), 1)
        self.assertAlmostEqual(
            self.cmp.dist(NONQ_FROM, NONQ_TO, 0), 8 ** 0.5 / 24 ** 0.5
        )
        self.assertAlmostEqual(
            self.cmp.dist(NONQ_TO, NONQ_FROM, 0), 8 ** 0.5 / 24 ** 0.5
        )

        # Test wrapper
        self.assertAlmostEqual(
            dist_euclidean('nelson', 'neilsen'), 7 ** 0.5 / 23 ** 0.5
        )


if __name__ == '__main__':
    unittest.main()
