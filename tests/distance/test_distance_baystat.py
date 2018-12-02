# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_baystat.

This module contains unit tests for abydos.distance.Baystat
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Baystat, dist_baystat, sim_baystat


class BaystatTestCases(unittest.TestCase):
    """Test Baystat functions.

    abydos.distance.Baystat
    """

    cmp = Baystat()

    def test_baystat_sim(self):
        """Test abydos.distance.Baystat.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('Colin', ''), 0)
        self.assertEqual(self.cmp.sim('Colin', 'Colin'), 1)

        # Examples given in the paper
        # https://www.statistik.bayern.de/medien/statistik/zensus/zusammenf__hrung_von_datenbest__nden_ohne_numerische_identifikatoren.pdf
        self.assertAlmostEqual(self.cmp.sim('DRAKOMENA', 'DRAOMINA'), 7 / 9)
        self.assertAlmostEqual(self.cmp.sim('RIEKI', 'RILKI'), 4 / 5)
        self.assertAlmostEqual(
            self.cmp.sim('ATANASSIONI', 'ATANASIOU'), 8 / 11
        )
        self.assertAlmostEqual(
            self.cmp.sim('LIESKOVSKY', 'LIESZKOVSZKY'), 10 / 12
        )
        self.assertAlmostEqual(self.cmp.sim('JEANETTE', 'JEANNETTE'), 8 / 9)
        self.assertAlmostEqual(self.cmp.sim('JOHANNES', 'JOHAN'), 0.625)
        self.assertAlmostEqual(self.cmp.sim('JOHANNES', 'HANS'), 0.375)
        self.assertAlmostEqual(self.cmp.sim('JOHANNES', 'HANNES'), 0.75)
        self.assertAlmostEqual(self.cmp.sim('ZIMMERMANN', 'SEMMERMANN'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('ZIMMERMANN', 'ZIMMERER'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('ZIMMERMANN', 'ZIMMER'), 0.6)

        # Tests to maximize coverage
        self.assertAlmostEqual(
            Baystat(2, 2, 2).sim('ZIMMERMANN', 'SEMMERMANN'), 0.8
        )
        self.assertAlmostEqual(self.cmp.sim('ZIMMER', 'ZIMMERMANN'), 0.6)

        # Test wrapper
        self.assertAlmostEqual(sim_baystat('ZIMMERMANN', 'SEMMERMANN'), 0.8)

    def test_baystat_dist(self):
        """Test abydos.distance.Baystat.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('Colin', ''), 1)
        self.assertEqual(self.cmp.dist('Colin', 'Colin'), 0)

        # Examples given in the paper
        # https://www.statistik.bayern.de/medien/statistik/zensus/zusammenf__hrung_von_datenbest__nden_ohne_numerische_identifikatoren.pdf
        self.assertAlmostEqual(self.cmp.dist('DRAKOMENA', 'DRAOMINA'), 2 / 9)
        self.assertAlmostEqual(self.cmp.dist('RIEKI', 'RILKI'), 1 / 5)
        self.assertAlmostEqual(
            self.cmp.dist('ATANASSIONI', 'ATANASIOU'), 3 / 11
        )
        self.assertAlmostEqual(
            self.cmp.dist('LIESKOVSKY', 'LIESZKOVSZKY'), 2 / 12
        )
        self.assertAlmostEqual(self.cmp.dist('JEANETTE', 'JEANNETTE'), 1 / 9)
        self.assertAlmostEqual(self.cmp.dist('JOHANNES', 'JOHAN'), 0.375)
        self.assertAlmostEqual(self.cmp.dist('JOHANNES', 'HANS'), 0.625)
        self.assertAlmostEqual(self.cmp.dist('JOHANNES', 'HANNES'), 0.25)
        self.assertAlmostEqual(self.cmp.dist('ZIMMERMANN', 'SEMMERMANN'), 0.2)
        self.assertAlmostEqual(self.cmp.dist('ZIMMERMANN', 'ZIMMERER'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('ZIMMERMANN', 'ZIMMER'), 0.4)

        # Test wrapper
        self.assertAlmostEqual(dist_baystat('ZIMMERMANN', 'SEMMERMANN'), 0.2)


if __name__ == '__main__':
    unittest.main()
