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

"""abydos.tests.distance.test_distance_jaccard.

This module contains unit tests for abydos.distance.Jaccard
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import math
import unittest

from abydos.distance import Jaccard, dist_jaccard, sim_jaccard, tanimoto
from abydos.tokenizer import QGrams

from .. import NONQ_FROM, NONQ_TO


class JaccardTestCases(unittest.TestCase):
    """Test Jaccard functions.

    abydos.distance.Jaccard
    """

    cmp = Jaccard()

    def test_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen'), 4 / 11)

        self.assertEqual(self.cmp.sim('', '', 2), 1)
        self.assertEqual(self.cmp.sim('nelson', '', 2), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen', 2), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen', 2), 4 / 11)

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
        self.assertAlmostEqual(sim_jaccard('nelson', 'neilsen'), 4 / 11)

    def test_jaccard_dist(self):
        """Test abydos.distance.Jaccard.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen'), 7 / 11)

        self.assertEqual(self.cmp.dist('', '', 2), 0)
        self.assertEqual(self.cmp.dist('nelson', '', 2), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen', 2), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen', 2), 7 / 11)

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
        self.assertAlmostEqual(dist_jaccard('nelson', 'neilsen'), 7 / 11)


class TanimotoTestCases(unittest.TestCase):
    """Test Tanimoto functions.

    abydos.distance.Jaccard.tanimoto_coeff
    """

    cmp = Jaccard()

    def test_jaccard_tanimoto_coeff(self):
        """Test abydos.distance.Jaccard.tanimoto_coeff."""
        self.assertEqual(self.cmp.tanimoto_coeff('', ''), 0)
        self.assertEqual(self.cmp.tanimoto_coeff('nelson', ''), float('-inf'))
        self.assertEqual(self.cmp.tanimoto_coeff('', 'neilsen'), float('-inf'))
        self.assertAlmostEqual(
            self.cmp.tanimoto_coeff('nelson', 'neilsen'), math.log(4 / 11, 2)
        )

        self.assertEqual(self.cmp.tanimoto_coeff('', '', 2), 0)
        self.assertEqual(
            self.cmp.tanimoto_coeff('nelson', '', 2), float('-inf')
        )
        self.assertEqual(
            self.cmp.tanimoto_coeff('', 'neilsen', 2), float('-inf')
        )
        self.assertAlmostEqual(
            self.cmp.tanimoto_coeff('nelson', 'neilsen', 2),
            math.log(4 / 11, 2),
        )

        # supplied q-gram tests
        self.assertEqual(self.cmp.tanimoto_coeff(QGrams(''), QGrams('')), 0)
        self.assertEqual(
            self.cmp.tanimoto_coeff(QGrams('nelson'), QGrams('')),
            float('-inf'),
        )
        self.assertEqual(
            self.cmp.tanimoto_coeff(QGrams(''), QGrams('neilsen')),
            float('-inf'),
        )
        self.assertAlmostEqual(
            self.cmp.tanimoto_coeff(QGrams('nelson'), QGrams('neilsen')),
            math.log(4 / 11, 2),
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.tanimoto_coeff('', '', 0), 0)
        self.assertEqual(
            self.cmp.tanimoto_coeff('the quick', '', 0), float('-inf')
        )
        self.assertEqual(
            self.cmp.tanimoto_coeff('', 'the quick', 0), float('-inf')
        )
        self.assertAlmostEqual(
            self.cmp.tanimoto_coeff(NONQ_FROM, NONQ_TO, 0), math.log(1 / 3, 2)
        )
        self.assertAlmostEqual(
            self.cmp.tanimoto_coeff(NONQ_TO, NONQ_FROM, 0), math.log(1 / 3, 2)
        )

        # Test wrapper
        self.assertAlmostEqual(
            tanimoto('nelson', 'neilsen'), math.log(4 / 11, 2)
        )


if __name__ == '__main__':
    unittest.main()
