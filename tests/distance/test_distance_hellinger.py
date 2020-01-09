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

"""abydos.tests.distance.test_distance_hellinger.

This module contains unit tests for abydos.distance.Hellinger
"""

import unittest

from abydos.distance import Hellinger


class HellingerTestCases(unittest.TestCase):
    """Test Hellinger functions.

    abydos.distance.Hellinger
    """

    cmp = Hellinger()

    def test_hellinger_dist(self):
        """Test abydos.distance.Hellinger.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.8164965809)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.8164965809)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.8164965809)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.8164965809)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.7071067812
        )

    def test_hellinger_sim(self):
        """Test abydos.distance.Hellinger.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.1835034191)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.1835034191)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.1835034191)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.1835034191)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.2928932188
        )

    def test_hellinger_dist_abs(self):
        """Test abydos.distance.Hellinger.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 2.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 2.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 2.8284271247461903)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 2.8284271247461903)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 4.47213595499958)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 3.4641016151
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 3.4641016151
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 3.4641016151
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 3.4641016151
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 3.7416573868
        )


if __name__ == '__main__':
    unittest.main()
