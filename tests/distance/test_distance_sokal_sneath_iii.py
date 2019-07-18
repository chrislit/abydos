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

"""abydos.tests.distance.test_distance_sokal_sneath_iii.

This module contains unit tests for abydos.distance.SokalSneathIII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import SokalSneathIII


class SokalSneathIIITestCases(unittest.TestCase):
    """Test SokalSneathIII functions.

    abydos.distance.SokalSneathIII
    """

    cmp = SokalSneathIII()

    def test_sokal_sneath_iii_sim_score(self):
        """Test abydos.distance.SokalSneathIII.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), float('inf'))
        self.assertEqual(self.cmp.sim_score('a', ''), 391.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 391.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 195.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 195.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), float('inf'))
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 77.4)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 129.6666666667
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 129.6666666667
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 129.6666666667
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 129.6666666667
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 111.0
        )
        self.assertEqual(
            self.cmp.sim_score('Kirisits', 'Kiritsis'), float('inf')
        )


    def test_sokal_sneath_iii_dist(self):
        """Test abydos.distance.SokalSneathIII.dist."""
        self.assertRaises(NotImplementedError, self.cmp.dist)

    def test_sokal_sneath_iii_sim(self):
        """Test abydos.distance.SokalSneathIII.sim."""
        self.assertRaises(NotImplementedError, self.cmp.sim)


if __name__ == '__main__':
    unittest.main()
