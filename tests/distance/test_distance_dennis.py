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

"""abydos.tests.distance.test_distance_dennis.

This module contains unit tests for abydos.distance.Dennis
"""

import unittest

from abydos.distance import Dennis


class DennisTestCases(unittest.TestCase):
    """Test Dennis functions.

    abydos.distance.Dennis
    """

    cmp = Dennis()
    cmp_no_d = Dennis(alphabet=0)

    def test_dennis_sim(self):
        """Test abydos.distance.Dennis.sim."""
        # Base cases
        self.assertAlmostEqual(self.cmp.sim('', ''), 0.3333333333333333)
        self.assertAlmostEqual(self.cmp.sim('a', ''), 0.3333333333333333)
        self.assertAlmostEqual(self.cmp.sim('', 'a'), 0.3333333333333333)
        self.assertAlmostEqual(self.cmp.sim('abc', ''), 0.3333333333333333)
        self.assertAlmostEqual(self.cmp.sim('', 'abc'), 0.3333333333333333)
        self.assertAlmostEqual(self.cmp.sim('abc', 'abc'), 0.9965986394557826)
        self.assertAlmostEqual(
            self.cmp.sim('abcd', 'efgh'), 0.32908163265306134
        )

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6615646259)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6615646259)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6615646259)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6615646259)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7693640991
        )

        # Tests with alphabet=0 (no d factor)
        self.assertAlmostEqual(self.cmp_no_d.sim('', ''), 0.3333333333333333)
        self.assertAlmostEqual(self.cmp_no_d.sim('a', ''), 0.3333333333333333)
        self.assertAlmostEqual(self.cmp_no_d.sim('', 'a'), 0.3333333333333333)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('abc', ''), 0.3333333333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('', 'abc'), 0.3333333333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('abc', 'abc'), 0.3333333333333333
        )
        self.assertAlmostEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.2222222222
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.2788497568
        )

    def test_dennis_dist(self):
        """Test abydos.distance.Dennis.dist."""
        # Base cases
        self.assertAlmostEqual(self.cmp.dist('', ''), 0.6666666666666667)
        self.assertAlmostEqual(self.cmp.dist('a', ''), 0.6666666666666667)
        self.assertAlmostEqual(self.cmp.dist('', 'a'), 0.6666666666666667)
        self.assertAlmostEqual(self.cmp.dist('abc', ''), 0.6666666666666667)
        self.assertAlmostEqual(self.cmp.dist('', 'abc'), 0.6666666666666667)
        self.assertAlmostEqual(
            self.cmp.dist('abc', 'abc'), 0.003401360544217358
        )
        self.assertAlmostEqual(
            self.cmp.dist('abcd', 'efgh'), 0.6709183673469387
        )

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3384353741)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3384353741)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.3384353741)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.3384353741)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2306359009
        )

        # Tests with alphabet=0 (no d factor)
        self.assertAlmostEqual(self.cmp_no_d.dist('', ''), 0.6666666666666667)
        self.assertAlmostEqual(self.cmp_no_d.dist('a', ''), 0.6666666666666667)
        self.assertAlmostEqual(self.cmp_no_d.dist('', 'a'), 0.6666666666666667)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('abc', ''), 0.6666666666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('', 'abc'), 0.6666666666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('abc', 'abc'), 0.6666666666666667
        )
        self.assertAlmostEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.7777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.7777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.7777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.7777777778
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.7211502432
        )

    def test_dennis_sim_score(self):
        """Test abydos.distance.Dennis.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertAlmostEqual(
            self.cmp.sim_score('abc', 'abc'), 27.85714285714286
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('abcd', 'efgh'), -0.17857142857142858
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 13.7857142857
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 13.7857142857
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 13.7857142857
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 13.7857142857
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 18.3132921606
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('abcd', 'efgh'), -1.5811388300841895
        )

        self.assertAlmostEqual(self.cmp_no_d.sim_score('Nigel', 'Niall'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Niall', 'Nigel'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Colin', 'Coiln'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim_score('Coiln', 'Colin'), -0.5)
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), -0.3057883149
        )

    def test_dennis_corr(self):
        """Test abydos.distance.Dennis.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertAlmostEqual(self.cmp.corr('abc', 'abc'), 0.994897959183674)
        self.assertAlmostEqual(
            self.cmp.corr('abcd', 'efgh'), -0.006377551020408
        )

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.4923469388)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.4923469388)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.4923469388)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.4923469388)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.6540461486
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -0.5)

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
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.0817253648
        )


if __name__ == '__main__':
    unittest.main()
