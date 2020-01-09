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

"""abydos.tests.distance.test_distance_mutual_information.

This module contains unit tests for abydos.distance.MutualInformation
"""

import unittest

from abydos.distance import MutualInformation


class MutualInformationTestCases(unittest.TestCase):
    """Test MutualInformation functions.

    abydos.distance.MutualInformation
    """

    cmp = MutualInformation()
    cmp_no_d = MutualInformation(alphabet=0)

    def test_mutual_information_sim(self):
        """Test abydos.distance.MutualInformation.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.1752299652353853)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9284965499)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9284965499)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9284965499)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9284965499)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9481813127
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim('a', 'eh'), -0.9036774610288023
        )

    def test_mutual_information_dist(self):
        """Test abydos.distance.MutualInformation.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.8247700347646147)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0715034501)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0715034501)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0715034501)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0715034501)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0518186873
        )

    def test_mutual_information_sim_score(self):
        """Test abydos.distance.MutualInformation.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 7.527706972593264)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), -4.700439718141093
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 5.9908322396
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 5.9908322396
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 5.9908322396
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 5.9908322396
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 5.6279117576
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.sim_score('abcd', 'efgh'), -4.700439718141093
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), -0.4020984436
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), -0.4020984436
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), -0.4020984436
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), -0.4020984436
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), -0.1650592463
        )


if __name__ == '__main__':
    unittest.main()
