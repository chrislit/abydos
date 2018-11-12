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

"""abydos.tests.distance.test_distance_tversky.

This module contains unit tests for abydos.distance.Tversky
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import (
    Tversky,
    dist_tversky,
    sim_tversky,
)
from abydos.tokenizer import QGrams

from .. import NONQ_FROM, NONQ_TO


class TverskyIndexTestCases(unittest.TestCase):
    """Test Tversky functions.

    abydos.distance.Tversky
    """
    cmp = Tversky()

    def test_tversky_sim(self):
        """Test abydos.distance.Tversky.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen'), 4 / 11)

        self.assertEqual(self.cmp.sim('', '', 2), 1)
        self.assertEqual(self.cmp.sim('nelson', '', 2), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen', 2), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen', 2), 4 / 11)

        # test valid alpha & beta
        self.assertRaises(ValueError, self.cmp.sim, 'abcd', 'dcba', 2, -1, -1)
        self.assertRaises(ValueError, self.cmp.sim, 'abcd', 'dcba', 2, -1, 0)
        self.assertRaises(ValueError, self.cmp.sim, 'abcd', 'dcba', 2, 0, -1)

        # test empty QGrams
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen', 7), 0.0)

        # test unequal alpha & beta
        self.assertAlmostEqual(self.cmp.sim('niall', 'neal', 2, 2, 1), 3 / 11)
        self.assertAlmostEqual(self.cmp.sim('niall', 'neal', 2, 1, 2), 3 / 10)
        self.assertAlmostEqual(self.cmp.sim('niall', 'neal', 2, 2, 2), 3 / 13)

        # test bias parameter
        self.assertAlmostEqual(
            self.cmp.sim('niall', 'neal', 2, 1, 1, 0.5), 7 / 11
        )
        self.assertAlmostEqual(
            self.cmp.sim('niall', 'neal', 2, 2, 1, 0.5), 7 / 9
        )
        self.assertAlmostEqual(
            self.cmp.sim('niall', 'neal', 2, 1, 2, 0.5), 7 / 15
        )
        self.assertAlmostEqual(
            self.cmp.sim('niall', 'neal', 2, 2, 2, 0.5), 7 / 11
        )

        # supplied q-gram tests
        self.assertEqual(self.cmp.sim(QGrams(''), QGrams('')), 1)
        self.assertEqual(self.cmp.sim(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(self.cmp.sim(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(
            self.cmp.sim(QGrams('nelson'), QGrams('neilsen')), 4 / 11
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.sim('', '', 0), 1)
        self.assertEqual(self.cmp.sim('the quick', '', 0), 0)
        self.assertEqual(self.cmp.sim('', 'the quick', 0), 0)
        self.assertAlmostEqual(self.cmp.sim(NONQ_FROM, NONQ_TO, 0), 1 / 3)
        self.assertAlmostEqual(self.cmp.sim(NONQ_TO, NONQ_FROM, 0), 1 / 3)

        # Test wrapper
        self.assertAlmostEqual(sim_tversky('nelson', 'neilsen'), 4 / 11)

    def test_tversky_dist(self):
        """Test abydos.distance.Tversky.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen'), 7 / 11)

        self.assertEqual(self.cmp.dist('', '', 2), 0)
        self.assertEqual(self.cmp.dist('nelson', '', 2), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen', 2), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen', 2), 7 / 11)

        # test valid alpha & beta
        self.assertRaises(ValueError, self.cmp.dist, 'abcd', 'dcba', 2, -1, -1)
        self.assertRaises(ValueError, self.cmp.dist, 'abcd', 'dcba', 2, -1, 0)
        self.assertRaises(ValueError, self.cmp.dist, 'abcd', 'dcba', 2, 0, -1)

        # test empty QGrams
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen', 7), 1.0)

        # test unequal alpha & beta
        self.assertAlmostEqual(self.cmp.dist('niall', 'neal', 2, 2, 1), 8 / 11)
        self.assertAlmostEqual(self.cmp.dist('niall', 'neal', 2, 1, 2), 7 / 10)
        self.assertAlmostEqual(self.cmp.dist('niall', 'neal', 2, 2, 2), 10 / 13)

        # test bias parameter
        self.assertAlmostEqual(
            self.cmp.dist('niall', 'neal', 2, 1, 1, 0.5), 4 / 11
        )
        self.assertAlmostEqual(
            self.cmp.dist('niall', 'neal', 2, 2, 1, 0.5), 2 / 9
        )
        self.assertAlmostEqual(
            self.cmp.dist('niall', 'neal', 2, 1, 2, 0.5), 8 / 15
        )
        self.assertAlmostEqual(
            self.cmp.dist('niall', 'neal', 2, 2, 2, 0.5), 4 / 11
        )

        # supplied q-gram tests
        self.assertEqual(self.cmp.dist(QGrams(''), QGrams('')), 0)
        self.assertEqual(self.cmp.dist(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(self.cmp.dist(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            self.cmp.dist(QGrams('nelson'), QGrams('neilsen')), 7 / 11
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.dist('', '', 0), 0)
        self.assertEqual(self.cmp.dist('the quick', '', 0), 1)
        self.assertEqual(self.cmp.dist('', 'the quick', 0), 1)
        self.assertAlmostEqual(self.cmp.dist(NONQ_FROM, NONQ_TO, 0), 2 / 3)
        self.assertAlmostEqual(self.cmp.dist(NONQ_TO, NONQ_FROM, 0), 2 / 3)

        # Test wrapper
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen'), 7 / 11)


if __name__ == '__main__':
    unittest.main()
