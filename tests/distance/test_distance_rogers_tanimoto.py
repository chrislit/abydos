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

"""abydos.tests.distance.test_distance_rogers_tanimoto.

This module contains unit tests for abydos.distance.RogersTanimoto
"""

import unittest

from abydos.distance import RogersTanimoto


class RogersTanimotoTestCases(unittest.TestCase):
    """Test RogersTanimoto functions.

    abydos.distance.RogersTanimoto
    """

    cmp = RogersTanimoto()
    cmp_no_d = RogersTanimoto(alphabet=0)

    def test_rogers_tanimoto_sim(self):
        """Test abydos.distance.RogersTanimoto.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9748110831234257)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9848101266)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9848101266)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9848101266)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9848101266)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.982300885
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.2)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.3333333333
        )

    def test_rogers_tanimoto_dist(self):
        """Test abydos.distance.RogersTanimoto.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0050890585241730735)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0050890585241730735)
        self.assertEqual(self.cmp.dist('abc', ''), 0.010152284263959421)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.010152284263959421)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.02518891687657432)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0151898734)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0151898734)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0151898734)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0151898734)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.017699115
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.8)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.8)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.8)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.8)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.6666666667
        )


if __name__ == '__main__':
    unittest.main()
