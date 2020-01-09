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

"""abydos.tests.distance.test_distance_ms_contingency.

This module contains unit tests for abydos.distance.MSContingency
"""

import unittest

from abydos.distance import MSContingency


class MSContingencyTestCases(unittest.TestCase):
    """Test MSContingency functions.

    abydos.distance.MSContingency
    """

    cmp = MSContingency()
    cmp_no_d = MSContingency(alphabet=0)
    cmp_4q1 = MSContingency(qval=1, alphabet=4)

    def test_ms_contingency_sim(self):
        """Test abydos.distance.MSContingency.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.49546153904804724)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.8142722325)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.8142722325)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.8142722325)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.8142722325)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.890704164
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.183772234
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.183772234
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.183772234
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.183772234
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.2782336187
        )

    def test_ms_contingency_dist(self):
        """Test abydos.distance.MSContingency.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5045384609519528)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.1857277675)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.1857277675)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.1857277675)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.1857277675)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.109295836
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.816227766
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.816227766
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.816227766
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.816227766
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.7217663813
        )

    def test_ms_contingency_corr(self):
        """Test abydos.distance.MSContingency.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), -1.0)
        self.assertEqual(self.cmp.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.009076921903905553)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.628544465)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.628544465)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.628544465)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.628544465)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.781408328
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.632455532
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.632455532
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.632455532
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.632455532
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.4435327626
        )

        self.assertEqual(self.cmp_4q1.corr('ab', 'ac'), 0.0)


if __name__ == '__main__':
    unittest.main()
