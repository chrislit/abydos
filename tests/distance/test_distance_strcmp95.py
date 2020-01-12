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

"""abydos.tests.distance.test_distance_strcmp95.

This module contains unit tests for abydos.distance.Strcmp95
"""

import unittest

from abydos.distance import Strcmp95


class Strcmp95TestCases(unittest.TestCase):
    """Test Strcmp95 functions.

    abydos.distance.Strcmp95
    """

    cmp = Strcmp95()
    cmp_ls = Strcmp95(True)

    def test_strcmp95_sim(self):
        """Test abydos.distance.Strcmp95.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('MARTHA', ''), 0)
        self.assertEqual(self.cmp.sim('', 'MARTHA'), 0)
        self.assertEqual(self.cmp.sim('MARTHA', 'MARTHA'), 1)

        self.assertAlmostEqual(self.cmp.sim('MARTHA', 'MARHTA'), 0.96111111)
        self.assertAlmostEqual(self.cmp.sim('DWAYNE', 'DUANE'), 0.873)
        self.assertAlmostEqual(self.cmp.sim('DIXON', 'DICKSONX'), 0.839333333)

        self.assertAlmostEqual(self.cmp.sim('ABCD', 'EFGH'), 0.0)

        # long_strings = True
        self.assertAlmostEqual(
            self.cmp_ls.sim('DIXON', 'DICKSONX'), 0.85393939
        )
        self.assertAlmostEqual(self.cmp_ls.sim('DWAYNE', 'DUANE'), 0.89609090)
        self.assertAlmostEqual(self.cmp_ls.sim('MARTHA', 'MARHTA'), 0.97083333)

        # cover case where we don't boost, etc.
        self.assertAlmostEqual(self.cmp.sim('A', 'ABCDEFGHIJK'), 69 / 99)
        self.assertAlmostEqual(self.cmp_ls.sim('A', 'ABCDEFGHIJK'), 69 / 99)
        self.assertAlmostEqual(self.cmp.sim('d', 'abcdefgh'), 0.708333333)
        self.assertAlmostEqual(self.cmp_ls.sim('d', 'abcdefgh'), 0.708333333)
        self.assertAlmostEqual(self.cmp_ls.sim('1', 'abc1efgh'), 0.708333333)
        self.assertAlmostEqual(
            self.cmp_ls.sim('12hundredths', '12hundred'), 0.916666667
        )

    def test_strcmp95_dist(self):
        """Test abydos.distance.Strcmp95.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('MARTHA', ''), 1)
        self.assertEqual(self.cmp.dist('', 'MARTHA'), 1)
        self.assertEqual(self.cmp.dist('MARTHA', 'MARTHA'), 0)

        self.assertAlmostEqual(self.cmp.dist('MARTHA', 'MARHTA'), 0.03888888)
        self.assertAlmostEqual(self.cmp.dist('DWAYNE', 'DUANE'), 0.127)
        self.assertAlmostEqual(self.cmp.dist('DIXON', 'DICKSONX'), 0.160666666)

        self.assertAlmostEqual(self.cmp.dist('ABCD', 'EFGH'), 1.0)


if __name__ == '__main__':
    unittest.main()
