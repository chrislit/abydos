# -*- coding: utf-8 -*-

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

"""abydos.tests.distance.test_distance_baulieu_iv.

This module contains unit tests for abydos.distance.BaulieuIV
"""

import unittest

from abydos.distance import BaulieuIV


class BaulieuIVTestCases(unittest.TestCase):
    """Test BaulieuIV functions.

    abydos.distance.BaulieuIV
    """

    cmp = BaulieuIV()
    cmp_no_d = BaulieuIV(alphabet=0)

    def test_baulieu_iv_dist(self):
        """Test abydos.distance.BaulieuIV.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.4999995930090347)
        self.assertEqual(self.cmp.dist('a', ''), 0.4999995950831843)
        self.assertEqual(self.cmp.dist('', 'a'), 0.4999995950831843)
        self.assertEqual(self.cmp.dist('abc', ''), 0.49999959715204023)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.49999959715204023)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.49999637435083444)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.4999996033268451)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4999972161)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4999972161)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.4999972161)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.4999972161)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4999941112
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5229924650732152)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5229924650732152)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5028740581341519)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5028740581341519)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.5)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.5001839397205857
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.5001682119
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.5001682119
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.5001682119
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.5001682119
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5000335167
        )

    def test_baulieu_iv_sim(self):
        """Test abydos.distance.BaulieuIV.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5000004069909654)
        self.assertEqual(self.cmp.sim('a', ''), 0.5000004049168156)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5000004049168156)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5000004028479598)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5000004028479598)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.5000036256491656)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.5000003966731549)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5000027839)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5000027839)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5000027839)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5000027839)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5000058888
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.4770075349267848)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.4770075349267848)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.49712594186584813)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.49712594186584813)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.4998160602794143)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.4998317881
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.4998317881
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.4998317881
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.4998317881
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.4999664833
        )

    def test_baulieu_iv_dist_abs(self):
        """Test abydos.distance.BaulieuIV.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), -1066.2460472130606)
        self.assertEqual(self.cmp.dist_abs('a', ''), -1060.8121333300487)
        self.assertEqual(self.cmp.dist_abs('', 'a'), -1060.8121333300487)
        self.assertEqual(self.cmp.dist_abs('abc', ''), -1055.3920882318764)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), -1055.3920882318764)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), -9498.574712454234)
        self.assertEqual(
            self.cmp.dist_abs('abcd', 'efgh'), -1039.2151656463932
        )

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), -7293.3912640224
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), -7293.3912640224
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), -7293.3912640224
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), -7293.3912640224
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), -15427.7573462754
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist_abs('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist_abs('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist_abs('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('Nigel', 'Niall'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('Niall', 'Nigel'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('Colin', 'Coiln'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('Coiln', 'Colin'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist_abs('ATCAACGAGT', 'AACGATTAG'), 0.5
        )


if __name__ == '__main__':
    unittest.main()
