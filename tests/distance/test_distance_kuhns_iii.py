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

"""abydos.tests.distance.test_distance_kuhns_iii.

This module contains unit tests for abydos.distance.KuhnsIII
"""

import unittest

from abydos.distance import KuhnsIII


class KuhnsIIITestCases(unittest.TestCase):
    """Test KuhnsIII functions.

    abydos.distance.KuhnsIII
    """

    cmp = KuhnsIII()
    cmp_no_d = KuhnsIII(alphabet=0)

    def test_kuhns_iii_sim(self):
        """Test abydos.distance.KuhnsIII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.25)
        self.assertEqual(self.cmp.sim('a', ''), 0.25)
        self.assertEqual(self.cmp.sim('', 'a'), 0.25)
        self.assertEqual(self.cmp.sim('abc', ''), 0.25)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.25)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9980818414322251)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.24760076775431863)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4971190781)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4971190781)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4971190781)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4971190781)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6199553626
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.25)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.25)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.25)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.25)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.25)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.25)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.125)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.125)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.125)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.125)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.1766304348
        )

    def test_kuhns_iii_dist(self):
        """Test abydos.distance.KuhnsIII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.75)
        self.assertEqual(self.cmp.dist('a', ''), 0.75)
        self.assertEqual(self.cmp.dist('', 'a'), 0.75)
        self.assertEqual(self.cmp.dist('abc', ''), 0.75)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.75)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0019181585677748858)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.7523992322456814)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5028809219)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5028809219)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5028809219)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5028809219)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3800446374
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.75)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.75)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.75)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.75)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.75)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.75)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.875)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.875)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.875)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.875)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.8233695652
        )

    def test_kuhns_iii_corr(self):
        """Test abydos.distance.KuhnsIII.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 0.9974424552429668)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.003198976327575176)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.3294921041)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.3294921041)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.3294921041)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.3294921041)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.4932738168
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.corr('abcd', 'efgh'), -0.3333333333333333
        )

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.097826087
        )


if __name__ == '__main__':
    unittest.main()
