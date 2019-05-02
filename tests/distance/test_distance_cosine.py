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

"""abydos.tests.distance.test_distance_cosine.

This module contains unit tests for abydos.distance.Cosine
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import math
import unittest

from abydos.distance import Cosine, dist_cosine, sim_cosine
from abydos.tokenizer import QGrams, QSkipgrams, WhitespaceTokenizer

from .. import NONQ_FROM, NONQ_TO


class CosineSimilarityTestCases(unittest.TestCase):
    """Test cosine similarity functions.

    abydos.distance.Cosine
    """

    cmp = Cosine()
    cmp_q2 = Cosine(tokenizer=QGrams(2))
    cmp_ws = Cosine(tokenizer=WhitespaceTokenizer())

    def test_cosine_sim(self):
        """Test abydos.distance.Cosine.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(
            self.cmp.sim('nelson', 'neilsen'), 4 / math.sqrt(7 * 8)
        )

        self.assertEqual(self.cmp_q2.sim('', ''), 1)
        self.assertEqual(self.cmp_q2.sim('nelson', ''), 0)
        self.assertEqual(self.cmp_q2.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(
            self.cmp_q2.sim('nelson', 'neilsen'), 4 / math.sqrt(7 * 8)
        )

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
            4 / math.sqrt(7 * 8),
        )

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.sim('', ''), 1)
        self.assertEqual(self.cmp_ws.sim('the quick', ''), 0)
        self.assertEqual(self.cmp_ws.sim('', 'the quick'), 0)
        self.assertAlmostEqual(
            self.cmp_ws.sim(NONQ_FROM, NONQ_TO), 4 / math.sqrt(9 * 7)
        )
        self.assertAlmostEqual(
            self.cmp_ws.sim(NONQ_TO, NONQ_FROM), 4 / math.sqrt(9 * 7)
        )

        self.assertEqual(self.cmp_q2.sim('eh', 'a'), 0.0)

        # Test wrapper
        self.assertAlmostEqual(
            sim_cosine('nelson', 'neilsen'), 4 / math.sqrt(7 * 8)
        )

    def test_cosine_dist(self):
        """Test abydos.distance.Cosine.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(
            self.cmp.dist('nelson', 'neilsen'), 1 - (4 / math.sqrt(7 * 8))
        )

        self.assertEqual(self.cmp_q2.dist('', ''), 0)
        self.assertEqual(self.cmp_q2.dist('nelson', ''), 1)
        self.assertEqual(self.cmp_q2.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(
            self.cmp_q2.dist('nelson', 'neilsen'), 1 - (4 / math.sqrt(7 * 8))
        )

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
            1 - (4 / math.sqrt(7 * 8)),
        )

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.dist('', ''), 0)
        self.assertEqual(self.cmp_ws.dist('the quick', ''), 1)
        self.assertEqual(self.cmp_ws.dist('', 'the quick'), 1)
        self.assertAlmostEqual(
            self.cmp_ws.dist(NONQ_FROM, NONQ_TO), 1 - 4 / math.sqrt(9 * 7)
        )
        self.assertAlmostEqual(
            self.cmp_ws.dist(NONQ_TO, NONQ_FROM), 1 - 4 / math.sqrt(9 * 7)
        )

        # Test wrapper
        self.assertAlmostEqual(
            dist_cosine('nelson', 'neilsen'), 1 - (4 / math.sqrt(7 * 8))
        )


if __name__ == '__main__':
    unittest.main()
