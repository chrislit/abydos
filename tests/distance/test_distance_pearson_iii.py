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

"""abydos.tests.distance.test_distance_pearson_iii.

This module contains unit tests for abydos.distance.PearsonIII
"""

import unittest

from abydos.distance import PearsonIII


class PearsonIIITestCases(unittest.TestCase):
    """Test PearsonIII functions.

    abydos.distance.PearsonIII
    """

    cmp = PearsonIII()
    cmp_no_d = PearsonIII(alphabet=0)

    def test_pearson_iii_sim(self):
        """Test abydos.distance.PearsonIII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5178457652562063)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.5178457652562063)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.49856936111823147)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5125741446)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5125741446)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5125741446)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5125741446)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5145331766
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.7236067977499789)
        self.assertEqual(
            self.cmp_no_d.sim('abcd', 'efgh'), 0.33333333333333337
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.3787321875
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.3787321875
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.3787321875
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.3787321875
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.422279161
        )

    def test_pearson_iii_dist(self):
        """Test abydos.distance.PearsonIII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.4821542347437937)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.4821542347437937)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5014306388817685)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4874258554)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4874258554)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.4874258554)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.4874258554)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4854668234
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.27639320225002106)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.6666666666666666
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.6212678125
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.6212678125
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.6212678125
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.6212678125
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.577720839
        )

    def test_pearson_iii_corr(self):
        """Test abydos.distance.PearsonIII.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.03569153051241248)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 0.03569153051241248)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.0028612777635371113)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.0251482893)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.0290663533
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.4472135954999579)
        self.assertEqual(
            self.cmp_no_d.corr('abcd', 'efgh'), -0.3333333333333333
        )

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.242535625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.242535625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.242535625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.242535625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.155441678
        )


if __name__ == '__main__':
    unittest.main()
