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

This module contains unit tests for abydos.distance._baystat
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance import dist_baystat, sim_baystat


class BaystatTestCases(unittest.TestCase):
    """Test Baystat functions.

    abydos.distance._baystat.sim_baystat & .dist_baystat
    """

    def test_sim_baystat(self):
        """Test abydos.distance._baystat.sim_baystat."""
        # Base cases
        self.assertEqual(sim_baystat('', ''), 1)
        self.assertEqual(sim_baystat('Colin', ''), 0)
        self.assertEqual(sim_baystat('Colin', 'Colin'), 1)

        # Examples given in the paper
        # https://www.statistik.bayern.de/medien/statistik/zensus/zusammenf__hrung_von_datenbest__nden_ohne_numerische_identifikatoren.pdf
        self.assertAlmostEqual(sim_baystat('DRAKOMENA', 'DRAOMINA'), 7 / 9)
        self.assertAlmostEqual(sim_baystat('RIEKI', 'RILKI'), 4 / 5)
        self.assertAlmostEqual(sim_baystat('ATANASSIONI', 'ATANASIOU'), 8 / 11)
        self.assertAlmostEqual(
            sim_baystat('LIESKOVSKY', 'LIESZKOVSZKY'), 10 / 12
        )
        self.assertAlmostEqual(sim_baystat('JEANETTE', 'JEANNETTE'), 8 / 9)
        self.assertAlmostEqual(sim_baystat('JOHANNES', 'JOHAN'), 0.625)
        self.assertAlmostEqual(sim_baystat('JOHANNES', 'HANS'), 0.375)
        self.assertAlmostEqual(sim_baystat('JOHANNES', 'HANNES'), 0.75)
        self.assertAlmostEqual(sim_baystat('ZIMMERMANN', 'SEMMERMANN'), 0.8)
        self.assertAlmostEqual(sim_baystat('ZIMMERMANN', 'ZIMMERER'), 0.6)
        self.assertAlmostEqual(sim_baystat('ZIMMERMANN', 'ZIMMER'), 0.6)

        # Tests to maximize coverage
        self.assertAlmostEqual(
            sim_baystat('ZIMMERMANN', 'SEMMERMANN', 2, 2, 2), 0.8
        )
        self.assertAlmostEqual(sim_baystat('ZIMMER', 'ZIMMERMANN'), 0.6)

    def test_dist_baystat(self):
        """Test abydos.distance._baystat.dist_baystat."""
        # Base cases
        self.assertEqual(dist_baystat('', ''), 0)
        self.assertEqual(dist_baystat('Colin', ''), 1)
        self.assertEqual(dist_baystat('Colin', 'Colin'), 0)

        # Examples given in the paper
        # https://www.statistik.bayern.de/medien/statistik/zensus/zusammenf__hrung_von_datenbest__nden_ohne_numerische_identifikatoren.pdf
        self.assertAlmostEqual(dist_baystat('DRAKOMENA', 'DRAOMINA'), 2 / 9)
        self.assertAlmostEqual(dist_baystat('RIEKI', 'RILKI'), 1 / 5)
        self.assertAlmostEqual(
            dist_baystat('ATANASSIONI', 'ATANASIOU'), 3 / 11
        )
        self.assertAlmostEqual(
            dist_baystat('LIESKOVSKY', 'LIESZKOVSZKY'), 2 / 12
        )
        self.assertAlmostEqual(dist_baystat('JEANETTE', 'JEANNETTE'), 1 / 9)
        self.assertAlmostEqual(dist_baystat('JOHANNES', 'JOHAN'), 0.375)
        self.assertAlmostEqual(dist_baystat('JOHANNES', 'HANS'), 0.625)
        self.assertAlmostEqual(dist_baystat('JOHANNES', 'HANNES'), 0.25)
        self.assertAlmostEqual(dist_baystat('ZIMMERMANN', 'SEMMERMANN'), 0.2)
        self.assertAlmostEqual(dist_baystat('ZIMMERMANN', 'ZIMMERER'), 0.4)
        self.assertAlmostEqual(dist_baystat('ZIMMERMANN', 'ZIMMER'), 0.4)


if __name__ == '__main__':
    unittest.main()
