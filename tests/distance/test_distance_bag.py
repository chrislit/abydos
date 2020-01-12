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

"""abydos.tests.distance.test_distance_bag.

This module contains unit tests for abydos.distance.Bag
"""

import unittest

from abydos.distance import Bag
from abydos.tokenizer import SAPSTokenizer


class BagTestCases(unittest.TestCase):
    """Test bag similarity functions.

    abydos.distance.Bag
    """

    cmp = Bag()

    def test_bag_dist_abs(self):
        """Test abydos.distance.Bag.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', ''), 6)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen'), 7)
        self.assertEqual(self.cmp.dist_abs('ab', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('ab', 'c'), 2)
        self.assertEqual(self.cmp.dist_abs('nelson', 'neilsen'), 2)
        self.assertEqual(self.cmp.dist_abs('neilsen', 'nelson'), 2)
        self.assertEqual(self.cmp.dist_abs('niall', 'neal'), 2)
        self.assertEqual(self.cmp.dist_abs('aluminum', 'Catalan'), 5)
        self.assertEqual(self.cmp.dist_abs('abcdefg', 'hijklm'), 7)
        self.assertEqual(self.cmp.dist_abs('abcdefg', 'hijklmno'), 8)

    def test_bag_sim(self):
        """Test abydos.distance.Bag.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('nelson', ''), 0)
        self.assertEqual(self.cmp.sim('', 'neilsen'), 0)
        self.assertEqual(self.cmp.sim('ab', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('ab', 'c'), 0)
        self.assertAlmostEqual(self.cmp.sim('nelson', 'neilsen'), 5 / 7)
        self.assertAlmostEqual(self.cmp.sim('neilsen', 'nelson'), 5 / 7)
        self.assertAlmostEqual(self.cmp.sim('niall', 'neal'), 3 / 5)
        self.assertAlmostEqual(self.cmp.sim('aluminum', 'Catalan'), 3 / 8)
        self.assertEqual(self.cmp.sim('abcdefg', 'hijklm'), 0)
        self.assertEqual(self.cmp.sim('abcdefg', 'hijklmno'), 0)

        self.assertEqual(Bag(tokenizer=SAPSTokenizer()).sim('DNA', 'RNA'), 0.5)

    def test_bag_dist(self):
        """Test abydos.distance.Bag.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('nelson', ''), 1)
        self.assertEqual(self.cmp.dist('', 'neilsen'), 1)
        self.assertEqual(self.cmp.dist('ab', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('ab', 'c'), 1)
        self.assertAlmostEqual(self.cmp.dist('nelson', 'neilsen'), 2 / 7)
        self.assertAlmostEqual(self.cmp.dist('neilsen', 'nelson'), 2 / 7)
        self.assertAlmostEqual(self.cmp.dist('niall', 'neal'), 2 / 5)
        self.assertAlmostEqual(self.cmp.dist('aluminum', 'Catalan'), 5 / 8)
        self.assertEqual(self.cmp.dist('abcdefg', 'hijklm'), 1)
        self.assertEqual(self.cmp.dist('abcdefg', 'hijklmno'), 1)


if __name__ == '__main__':
    unittest.main()
