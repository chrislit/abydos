# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_rouge_w.

This module contains unit tests for abydos.distance.RougeW
"""

import unittest

from abydos.distance import RougeW


class RougeWTestCases(unittest.TestCase):
    """Test RougeW functions.

    abydos.distance.RougeW
    """

    cmp = RougeW()
    cmp_cubed = RougeW(f_func=lambda x: x ** 3, f_inv=lambda x: x ** (1 / 3))

    def test_rouge_w_sim(self):
        """Test abydos.distance.RougeW.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4472135955)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4472135955)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4898979486)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4898979486)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.548566506
        )

        # Examples from paper
        self.assertEqual(round(self.cmp.sim('ABCDEFG', 'ABCDHIK'), 3), 0.571)
        self.assertEqual(round(self.cmp.sim('ABCDEFG', 'AHBKCID'), 3), 0.286)

        # Coverage
        self.assertAlmostEqual(
            self.cmp_cubed.sim('Nigel', 'Niall'), 0.4160167646
        )
        self.assertAlmostEqual(
            self.cmp_cubed.sim('Colin', 'Coiln'), 0.4308869380
        )
        self.assertAlmostEqual(
            self.cmp_cubed.sim('ATCAACGAGT', 'AACGATTAG'), 0.5125114739
        )

    def test_rouge_w_dist(self):
        """Test abydos.distance.RougeW.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5527864045)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5527864045)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5101020514)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5101020514)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.451433494
        )

    def test_rouge_w_wlcs(self):
        """Test abydos.distance.RougeW.wlcs."""
        self.assertEqual(self.cmp.wlcs('', ''), 0)
        self.assertEqual(self.cmp.wlcs('a', ''), 0)
        self.assertEqual(self.cmp.wlcs('', 'a'), 0)
        self.assertEqual(self.cmp.wlcs('abc', ''), 0)
        self.assertEqual(self.cmp.wlcs('', 'abc'), 0)
        self.assertEqual(self.cmp.wlcs('abc', 'abc'), 9)


if __name__ == '__main__':
    unittest.main()
