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

"""abydos.tests.distance.test_distance_anderberg.

This module contains unit tests for abydos.distance.Anderberg
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Anderberg


class AnderbergTestCases(unittest.TestCase):
    """Test Anderberg functions.

    abydos.distance.Anderberg
    """

    cmp = Anderberg()

    def test_anderberg_sim(self):
        """Test abydos.distance.Anderberg.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.01020408163265306)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0089285714
        )

    def test_anderberg_sim_score(self):
        """Test abydos.distance.Anderberg.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 0.00510204081632653)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.0044642857
        )


if __name__ == '__main__':
    unittest.main()
