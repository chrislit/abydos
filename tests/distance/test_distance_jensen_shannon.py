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

"""abydos.tests.distance.test_distance_jensen_shannon.

This module contains unit tests for abydos.distance.JensenShannon
"""

import unittest

from abydos.distance import JensenShannon


class JensenShannonTestCases(unittest.TestCase):
    """Test JensenShannon functions.

    abydos.distance.JensenShannon
    """

    cmp = JensenShannon()

    def test_jensen_shannon_dist(self):
        """Test abydos.distance.JensenShannon.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.332911546
        )

    def test_jensen_shannon_sim(self):
        """Test abydos.distance.JensenShannon.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.667088454
        )

    def test_jensen_shannon_dist_abs(self):
        """Test abydos.distance.JensenShannon.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 0.6931471805599453)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 0.6931471805599453)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 0.6931471805599453)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 0.6931471805599453)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 0.6931471805599453)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 0.3465735903
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 0.3465735903
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 0.3465735903
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 0.3465735903
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 0.2307566995
        )

        self.assertEqual(
            JensenShannon(intersection_type='soft', qval=2).dist_abs(
                'a', 'eh'
            ),
            0.6931471805599453,
        )


if __name__ == '__main__':
    unittest.main()
