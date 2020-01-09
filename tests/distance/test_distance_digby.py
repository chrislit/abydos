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

"""abydos.tests.distance.test_distance_digby.

This module contains unit tests for abydos.distance.Digby
"""

import unittest

from abydos.distance import Digby


class DigbyTestCases(unittest.TestCase):
    """Test Digby functions.

    abydos.distance.Digby
    """

    cmp = Digby()
    cmp_no_d = Digby(alphabet=0)

    def test_digby_sim(self):
        """Test abydos.distance.Digby.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9847181266)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9847181266)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9847181266)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9847181266)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9898546788
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0
        )

    def test_digby_dist(self):
        """Test abydos.distance.Digby.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0152818734)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0152818734)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0152818734)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0152818734)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0101453212
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.0
        )

    def test_digby_corr(self):
        """Test abydos.distance.Digby.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), -1.0)
        self.assertEqual(self.cmp.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.9694362533)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.9694362533)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.9694362533)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.9694362533)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.9797093576
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -1.0
        )


if __name__ == '__main__':
    unittest.main()
