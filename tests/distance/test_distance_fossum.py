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

"""abydos.tests.distance.test_distance_fossum.

This module contains unit tests for abydos.distance.Fossum
"""

import unittest

from abydos.distance import Fossum


class FossumTestCases(unittest.TestCase):
    """Test Fossum functions.

    abydos.distance.Fossum
    """

    cmp = Fossum()
    cmp_no_d = Fossum(alphabet=0)

    def test_fossum_sim(self):
        """Test abydos.distance.Fossum.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.2222222222222222)
        self.assertEqual(self.cmp.sim('', 'a'), 0.2222222222222222)
        self.assertEqual(self.cmp.sim('abc', ''), 0.08163265306122448)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.08163265306122448)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.01234567901234568)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.2066115702)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.2066115702)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.2066115702)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.2066115702)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4215419501
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.2222222222222222)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.2222222222222222)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.08163265306122448)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.08163265306122448)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(
            self.cmp_no_d.sim('abcd', 'efgh'), 0.02469135802469136
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.3099173554
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.3099173554
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.3099173554
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.3099173554
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5365079365
        )

    def test_fossum_dist(self):
        """Test abydos.distance.Fossum.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.7777777777777778)
        self.assertEqual(self.cmp.dist('', 'a'), 0.7777777777777778)
        self.assertEqual(self.cmp.dist('abc', ''), 0.9183673469387755)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.9183673469387755)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.9876543209876543)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.7933884298)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.7933884298)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.7933884298)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.7933884298)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5784580499
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.7777777777777778)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.7777777777777778)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.9183673469387755)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.9183673469387755)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.9753086419753086
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.6900826446
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.6900826446
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.6900826446
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.6900826446
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.4634920635
        )

    def test_fossum_sim_score(self):
        """Test abydos.distance.Fossum.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 196.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 98.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 98.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 49.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 49.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 600.25)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 7.84)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 136.1111111111
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 136.1111111111
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 136.1111111111
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 136.1111111111
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 301.1272727273
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.25)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.25)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.25)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.25)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 3.0625)
        self.assertEqual(self.cmp_no_d.sim_score('abcd', 'efgh'), 0.1)

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), 1.5625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), 1.5625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), 1.5625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), 1.5625
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), 5.3772727273
        )


if __name__ == '__main__':
    unittest.main()
