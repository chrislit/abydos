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

"""abydos.tests.distance.test_distance_kuder_richardson.

This module contains unit tests for abydos.distance.KuderRichardson
"""

import unittest

from abydos.distance import KuderRichardson


class KuderRichardsonTestCases(unittest.TestCase):
    """Test KuderRichardson functions.

    abydos.distance.KuderRichardson
    """

    cmp = KuderRichardson()
    cmp_no_d = KuderRichardson(alphabet=0)

    def test_kuder_richardson_sim(self):
        """Test abydos.distance.KuderRichardson.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.4935400516795866)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.8316151203)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.8316151203)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.8316151203)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.8316151203)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.8983851254
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0102040816
        )

    def test_kuder_richardson_dist(self):
        """Test abydos.distance.KuderRichardson.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5064599483204134)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.1683848797)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.1683848797)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.1683848797)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.1683848797)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.1016148746
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.9897959184
        )

    def test_kuder_richardson_corr(self):
        """Test abydos.distance.KuderRichardson.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.012919896640826873)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.6632302405)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.6632302405)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.6632302405)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.6632302405)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.7967702508
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), float('-inf'))

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -2.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -2.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -2.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -2.0)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.9795918367
        )


if __name__ == '__main__':
    unittest.main()
