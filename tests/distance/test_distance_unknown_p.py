# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_unknown_p.

This module contains unit tests for abydos.distance.UnknownP
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import UnknownP


class UnknownPTestCases(unittest.TestCase):
    """Test UnknownP functions.

    abydos.distance.UnknownP
    """

    cmp = UnknownP()
    cmp_no_d = UnknownP(alphabet=0)

    def test_unknown_p_sim(self):
        """Test abydos.distance.UnknownP.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.75)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.2958758548)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.2958758548)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.2958758548)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.2958758548)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5093099295
        )

    def test_unknown_p_dist(self):
        """Test abydos.distance.UnknownP.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.25)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.7041241452)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.7041241452)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.7041241452)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.7041241452)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4906900705
        )

    def test_unknown_p_sim_score(self):
        """Test abydos.distance.UnknownP.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 0.75)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), -0.22360679774997896
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 0.2958758548
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 0.2958758548
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 0.2958758548
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 0.2958758548
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.5093099295
        )


if __name__ == '__main__':
    unittest.main()
