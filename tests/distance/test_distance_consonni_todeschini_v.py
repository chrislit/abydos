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

"""abydos.tests.distance.test_distance_consonni_todeschini_v.

This module contains unit tests for abydos.distance.ConsonniTodeschiniV
"""

import unittest

from abydos.distance import ConsonniTodeschiniV


class ConsonniTodeschiniVTestCases(unittest.TestCase):
    """Test ConsonniTodeschiniV functions.

    abydos.distance.ConsonniTodeschiniV
    """

    cmp = ConsonniTodeschiniV()
    cmp_no_d = ConsonniTodeschiniV(alphabet=0)

    def test_consonni_todeschini_v_sim(self):
        """Test abydos.distance.ConsonniTodeschiniV.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.8368594684755613)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.36359270242851005)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7281476435)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7281476435)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7281476435)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7281476435)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7523559381
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.1233121373
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.1233121373
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.1233121373
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.1233121373
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.1721709773
        )

    def test_consonni_todeschini_v_dist(self):
        """Test abydos.distance.ConsonniTodeschiniV.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.5)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.16314053152443875)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.63640729757149)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2718523565)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2718523565)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2718523565)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2718523565)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2476440619
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.8766878627
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.8766878627
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.8766878627
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.8766878627
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.8278290227
        )

    def test_consonni_todeschini_v_corr(self):
        """Test abydos.distance.ConsonniTodeschiniV.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 0.6737189369511224)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.2728145951429799)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.4562952871)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.4562952871)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.4562952871)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.4562952871)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.5047118763
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.7533757254
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.6556580454
        )


if __name__ == '__main__':
    unittest.main()
