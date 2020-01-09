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

"""abydos.tests.distance.test_distance_dice.

This module contains unit tests for abydos.distance.Dice
"""

import unittest

from abydos.distance import Dice, dist_dice, sim_dice
from abydos.tokenizer import QGrams, WhitespaceTokenizer

from .. import NONQ_FROM, NONQ_TO


class DiceTestCases(unittest.TestCase):
    """Test Dice functions.

    abydos.distance.Dice
    """

    cmp = Dice()
    cmp_q2 = Dice(tokenizer=QGrams(2))
    cmp_ws = Dice(tokenizer=WhitespaceTokenizer())

    def test_dice_sim(self):
        """Test abydos.distance.Dice.sim."""
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

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.sim('', ''), 1)
        self.assertEqual(self.cmp_ws.sim('the quick', ''), 0)
        self.assertEqual(self.cmp_ws.sim('', 'the quick'), 0)
        self.assertAlmostEqual(self.cmp_ws.sim(NONQ_FROM, NONQ_TO), 1 / 2)
        self.assertAlmostEqual(self.cmp_ws.sim(NONQ_TO, NONQ_FROM), 1 / 2)

        # Test wrapper
        self.assertAlmostEqual(sim_dice('nelson', 'neilsen'), 8 / 15)

    def test_dice_dist(self):
        """Test abydos.distance.Dice.dist."""
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

        # non-q-gram tests
        self.assertEqual(self.cmp_ws.dist('', ''), 0)
        self.assertEqual(self.cmp_ws.dist('the quick', ''), 1)
        self.assertEqual(self.cmp_ws.dist('', 'the quick'), 1)
        self.assertAlmostEqual(self.cmp_ws.dist(NONQ_FROM, NONQ_TO), 1 / 2)
        self.assertAlmostEqual(self.cmp_ws.dist(NONQ_TO, NONQ_FROM), 1 / 2)

        # Test wrapper
        self.assertAlmostEqual(dist_dice('nelson', 'neilsen'), 7 / 15)


if __name__ == '__main__':
    unittest.main()
