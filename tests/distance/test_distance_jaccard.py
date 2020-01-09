# Copyright 2014-2020 by Christopher C. Little.
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

import unittest
from math import log2

from abydos.distance import Jaccard, dist_jaccard, sim_jaccard, tanimoto
from abydos.tokenizer import QGrams, WhitespaceTokenizer

from .. import NONQ_FROM, NONQ_TO


class JaccardTestCases(unittest.TestCase):
    """Test Jaccard functions.

    abydos.distance.Jaccard
    """

    cmp = Jaccard()
    cmp_q2 = Jaccard(tokenizer=QGrams(2))
    cmp_ws = Jaccard(tokenizer=WhitespaceTokenizer())

    def test_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen'), 4 / 11)

        self.assertEqual(self.cmp_q2.sim('', ''), 1)
        self.assertEqual(self.cmp_q2.sim('nelson', ''), 0)
        self.assertEqual(self.cmp_q2.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp_q2.sim('nelson', 'neilsen'), 4 / 11)

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
            4 / 11,
        )

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.sim('', ''), 1)
        self.assertEqual(self.cmp_ws.sim('the quick', ''), 0)
        self.assertEqual(self.cmp_ws.sim('', 'the quick'), 0)
        self.assertAlmostEqual(self.cmp_ws.sim(NONQ_FROM, NONQ_TO), 1 / 3)
        self.assertAlmostEqual(self.cmp_ws.sim(NONQ_TO, NONQ_FROM), 1 / 3)

        # Test wrapper
        self.assertAlmostEqual(sim_jaccard('nelson', 'neilsen'), 4 / 11)

    def test_jaccard_dist(self):
        """Test abydos.distance.Jaccard.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen'), 7 / 11)

        self.assertEqual(self.cmp_q2.dist('', ''), 0)
        self.assertEqual(self.cmp_q2.dist('nelson', ''), 1)
        self.assertEqual(self.cmp_q2.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp_q2.dist('nelson', 'neilsen'), 7 / 11)

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
            7 / 11,
        )

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.dist('', ''), 0)
        self.assertEqual(self.cmp_ws.dist('the quick', ''), 1)
        self.assertEqual(self.cmp_ws.dist('', 'the quick'), 1)
        self.assertAlmostEqual(self.cmp_ws.dist(NONQ_FROM, NONQ_TO), 2 / 3)
        self.assertAlmostEqual(self.cmp_ws.dist(NONQ_TO, NONQ_FROM), 2 / 3)

        # Test wrapper
        self.assertAlmostEqual(dist_jaccard('nelson', 'neilsen'), 7 / 11)


class TanimotoTestCases(unittest.TestCase):
    """Test Tanimoto functions.

    abydos.distance.Jaccard.tanimoto_coeff
    """

    cmp = Jaccard()
    cmp_q2 = Jaccard(tokenizer=QGrams(2))
    cmp_ws = Jaccard(tokenizer=WhitespaceTokenizer())

    def test_jaccard_tanimoto_coeff(self):
        """Test abydos.distance.Jaccard.tanimoto_coeff."""
        self.assertEqual(self.cmp.tanimoto_coeff('', ''), 0)
        self.assertEqual(self.cmp.tanimoto_coeff('nelson', ''), float('-inf'))
        self.assertEqual(self.cmp.tanimoto_coeff('', 'neilsen'), float('-inf'))
        self.assertAlmostEqual(
            self.cmp.tanimoto_coeff('nelson', 'neilsen'), log2(4 / 11)
        )

        self.assertEqual(self.cmp_q2.tanimoto_coeff('', ''), 0)
        self.assertEqual(
            self.cmp_q2.tanimoto_coeff('nelson', ''), float('-inf')
        )
        self.assertEqual(
            self.cmp_q2.tanimoto_coeff('', 'neilsen'), float('-inf')
        )
        self.assertAlmostEqual(
            self.cmp_q2.tanimoto_coeff('nelson', 'neilsen'), log2(4 / 11),
        )

        # supplied q-gram tests
        self.assertEqual(
            self.cmp.tanimoto_coeff(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('').get_counter(),
            ),
            0,
        )
        self.assertEqual(
            self.cmp.tanimoto_coeff(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('').get_counter(),
            ),
            float('-inf'),
        )
        self.assertEqual(
            self.cmp.tanimoto_coeff(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            float('-inf'),
        )
        self.assertAlmostEqual(
            self.cmp.tanimoto_coeff(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            log2(4 / 11),
        )

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.tanimoto_coeff('', ''), 0)
        self.assertEqual(
            self.cmp_ws.tanimoto_coeff('the quick', ''), float('-inf')
        )
        self.assertEqual(
            self.cmp_ws.tanimoto_coeff('', 'the quick'), float('-inf')
        )
        self.assertAlmostEqual(
            self.cmp_ws.tanimoto_coeff(NONQ_FROM, NONQ_TO), log2(1 / 3)
        )
        self.assertAlmostEqual(
            self.cmp_ws.tanimoto_coeff(NONQ_TO, NONQ_FROM), log2(1 / 3)
        )

        # Test wrapper
        self.assertAlmostEqual(tanimoto('nelson', 'neilsen'), log2(4 / 11))


if __name__ == '__main__':
    unittest.main()
