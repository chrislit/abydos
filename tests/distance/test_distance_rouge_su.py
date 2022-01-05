# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_rouge_su.

This module contains unit tests for abydos.distance.RougeSU
"""

import unittest

from abydos.distance import RougeSU


class RougeSUTestCases(unittest.TestCase):
    """Test RougeSU functions.

    abydos.distance.RougeSU
    """

    cmp = RougeSU()

    def test_rouge_su_sim(self):
        """Test abydos.distance.RougeSU.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9333333333)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9333333333)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7840112202
        )

    def test_rouge_su_dist(self):
        """Test abydos.distance.RougeSU.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.6)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.6)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0666666667)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2159887798
        )


if __name__ == '__main__':
    unittest.main()
