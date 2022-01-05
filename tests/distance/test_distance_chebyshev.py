# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_chebyshev.

This module contains unit tests for abydos.distance.Chebyshev
"""

import unittest

from abydos.distance import Chebyshev
from abydos.tokenizer import QGrams, WhitespaceTokenizer

from .. import NONQ_FROM, NONQ_TO


class ChebyshevTestCases(unittest.TestCase):
    """Test Chebyshev functions.

    abydos.distance.Chebyshev
    """

    cmp = Chebyshev()
    cmp_q2 = Chebyshev(tokenizer=QGrams(2))
    cmp_ws = Chebyshev(tokenizer=WhitespaceTokenizer())

    def test_chebyshev_dist_abs(self):
        """Test abydos.distance.Chebyshev.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', ''), 1)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen'), 1)
        self.assertEqual(self.cmp.dist_abs('nelson', 'neilsen'), 1)

        self.assertEqual(self.cmp_q2.dist_abs('', ''), 0)
        self.assertEqual(self.cmp_q2.dist_abs('nelson', ''), 1)
        self.assertEqual(self.cmp_q2.dist_abs('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp_q2.dist_abs('nelson', 'neilsen'), 1)

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
            1,
        )
        self.assertEqual(
            self.cmp.dist_abs(
                QGrams().tokenize('').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            1,
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs(
                QGrams().tokenize('nelson').get_counter(),
                QGrams().tokenize('neilsen').get_counter(),
            ),
            1,
        )

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.dist_abs('', ''), 0)
        self.assertEqual(self.cmp_ws.dist_abs('the quick', ''), 1)
        self.assertEqual(self.cmp_ws.dist_abs('', 'the quick'), 1)
        self.assertAlmostEqual(self.cmp_ws.dist_abs(NONQ_FROM, NONQ_TO), 1)
        self.assertAlmostEqual(self.cmp_ws.dist_abs(NONQ_TO, NONQ_FROM), 1)

    def test_chebyshev_dist(self):
        """Test abydos.distance.Chebyshev.dist."""
        self.assertRaises(NotImplementedError, self.cmp.dist)

    def test_chebyshev_sim(self):
        """Test abydos.distance.Chebyshev.sim."""
        self.assertRaises(NotImplementedError, self.cmp.sim)


if __name__ == '__main__':
    unittest.main()
