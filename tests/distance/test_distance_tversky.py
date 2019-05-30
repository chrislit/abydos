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

from abydos.distance import Tversky, dist_tversky, sim_tversky
from abydos.tokenizer import QGrams, WhitespaceTokenizer

from .. import NONQ_FROM, NONQ_TO


class TverskyIndexTestCases(unittest.TestCase):
    """Test Tversky functions.

    abydos.distance.Tversky
    """

    cmp = Tversky()
    cmp_q2 = Tversky(tokenizer=QGrams(2))
    cmp_ws = Tversky(tokenizer=WhitespaceTokenizer())

    def test_tversky_sim(self):
        """Test abydos.distance.Tversky.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen'), 4 / 11)

        self.assertEqual(self.cmp_q2.sim('', ''), 1)
        self.assertEqual(self.cmp_q2.sim('nelson', ''), 0)
        self.assertEqual(self.cmp_q2.sim('', 'neilsen'), 0)
        self.assertAlmostEqual(self.cmp_q2.sim('nelson', 'neilsen'), 4 / 11)

        # test valid alpha & beta
        self.assertRaises(
            ValueError, Tversky(alpha=-1.0, beta=-1.0).sim, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, Tversky(alpha=-1.0, beta=0.0).sim, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, Tversky(alpha=0.0, beta=-1.0).sim, 'abcd', 'dcba'
        )

        # test empty QGrams
        self.assertAlmostEqual(
            Tversky(tokenizer=QGrams(7, start_stop='')).sim(
                'nelson', 'neilsen'
            ),
            0.0,
        )

        # test unequal alpha & beta
        self.assertAlmostEqual(
            Tversky(alpha=2.0, beta=1.0, tokenizer=QGrams(2)).sim(
                'niall', 'neal'
            ),
            3 / 11,
        )
        self.assertAlmostEqual(
            Tversky(alpha=1.0, beta=2.0, tokenizer=QGrams(2)).sim(
                'niall', 'neal'
            ),
            3 / 10,
        )
        self.assertAlmostEqual(
            Tversky(alpha=2.0, beta=2.0, tokenizer=QGrams(2)).sim(
                'niall', 'neal'
            ),
            3 / 13,
        )

        # test bias parameter
        self.assertAlmostEqual(
            Tversky(alpha=1.0, beta=1.0, bias=0.5, tokenizer=QGrams(2)).sim(
                'niall', 'neal'
            ),
            7 / 11,
        )
        self.assertAlmostEqual(
            Tversky(alpha=2.0, beta=1.0, bias=0.5, tokenizer=QGrams(2)).sim(
                'niall', 'neal'
            ),
            7 / 9,
        )
        self.assertAlmostEqual(
            Tversky(alpha=1.0, beta=2.0, bias=0.5, tokenizer=QGrams(2)).sim(
                'niall', 'neal'
            ),
            7 / 15,
        )
        self.assertAlmostEqual(
            Tversky(alpha=2.0, beta=2.0, bias=0.5, tokenizer=QGrams(2)).sim(
                'niall', 'neal'
            ),
            7 / 11,
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
            4 / 11,
        )

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.sim('', ''), 1)
        self.assertEqual(self.cmp_ws.sim('the quick', ''), 0)
        self.assertEqual(self.cmp_ws.sim('', 'the quick'), 0)
        self.assertAlmostEqual(self.cmp_ws.sim(NONQ_FROM, NONQ_TO), 1 / 3)
        self.assertAlmostEqual(self.cmp_ws.sim(NONQ_TO, NONQ_FROM), 1 / 3)

        # Test wrapper
        self.assertAlmostEqual(sim_tversky('nelson', 'neilsen'), 4 / 11)

    def test_tversky_dist(self):
        """Test abydos.distance.Tversky.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen'), 7 / 11)

        self.assertEqual(self.cmp_q2.dist('', ''), 0)
        self.assertEqual(self.cmp_q2.dist('nelson', ''), 1)
        self.assertEqual(self.cmp_q2.dist('', 'neilsen'), 1)
        self.assertAlmostEqual(self.cmp_q2.dist('nelson', 'neilsen'), 7 / 11)

        # test valid alpha & beta
        self.assertRaises(
            ValueError, Tversky(alpha=-1.0, beta=-1.0).dist, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, Tversky(alpha=-1.0, beta=0.0).dist, 'abcd', 'dcba'
        )
        self.assertRaises(
            ValueError, Tversky(alpha=0.0, beta=-1.0).dist, 'abcd', 'dcba'
        )

        # test empty QGrams
        self.assertAlmostEqual(
            Tversky(tokenizer=QGrams(7, start_stop='')).dist(
                'nelson', 'neilsen'
            ),
            1.0,
        )

        # test unequal alpha & beta
        self.assertAlmostEqual(
            Tversky(alpha=2.0, beta=1.0, tokenizer=QGrams(2)).dist(
                'niall', 'neal'
            ),
            8 / 11,
        )
        self.assertAlmostEqual(
            Tversky(alpha=1.0, beta=2.0, tokenizer=QGrams(2)).dist(
                'niall', 'neal'
            ),
            7 / 10,
        )
        self.assertAlmostEqual(
            Tversky(alpha=2.0, beta=2.0, tokenizer=QGrams(2)).dist(
                'niall', 'neal'
            ),
            10 / 13,
        )

        # test bias parameter
        self.assertAlmostEqual(
            Tversky(alpha=1.0, beta=1.0, bias=0.5, tokenizer=QGrams(2)).dist(
                'niall', 'neal'
            ),
            4 / 11,
        )
        self.assertAlmostEqual(
            Tversky(alpha=2.0, beta=1.0, bias=0.5, tokenizer=QGrams(2)).dist(
                'niall', 'neal'
            ),
            2 / 9,
        )
        self.assertAlmostEqual(
            Tversky(alpha=1.0, beta=2.0, bias=0.5, tokenizer=QGrams(2)).dist(
                'niall', 'neal'
            ),
            8 / 15,
        )
        self.assertAlmostEqual(
            Tversky(alpha=2.0, beta=2.0, bias=0.5, tokenizer=QGrams(2)).dist(
                'niall', 'neal'
            ),
            4 / 11,
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
            7 / 11,
        )

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.dist('', ''), 0)
        self.assertEqual(self.cmp_ws.dist('the quick', ''), 1)
        self.assertEqual(self.cmp_ws.dist('', 'the quick'), 1)
        self.assertAlmostEqual(self.cmp_ws.dist(NONQ_FROM, NONQ_TO), 2 / 3)
        self.assertAlmostEqual(self.cmp_ws.dist(NONQ_TO, NONQ_FROM), 2 / 3)

        # Test wrapper
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen'), 7 / 11)


if __name__ == '__main__':
    unittest.main()
