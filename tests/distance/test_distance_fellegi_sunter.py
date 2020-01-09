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

"""abydos.tests.distance.test_distance_fellegi_sunter.

This module contains unit tests for abydos.distance.FellegiSunter
"""

import unittest

from abydos.distance import FellegiSunter


class FellegiSunterTestCases(unittest.TestCase):
    """Test FellegiSunter functions.

    abydos.distance.FellegiSunter
    """

    cmp = FellegiSunter()
    cmp_simp = FellegiSunter(simplified=True)

    def test_fellegi_sunter_sim(self):
        """Test abydos.distance.FellegiSunter.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.586895558534099)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.270318312)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.270318312)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.270318312)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.270318312)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.2814144756
        )

        # Simplified variant cases
        self.assertEqual(self.cmp_simp.sim('', ''), 0.0)
        self.assertEqual(self.cmp_simp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_simp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_simp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_simp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_simp.sim('abc', 'abc'), 0.9241962407465937)
        self.assertEqual(self.cmp_simp.sim('abcd', 'efgh'), 0.0)
        self.assertAlmostEqual(
            self.cmp_simp.sim('Nigel', 'Niall'), 0.2687639203842084
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim('Niall', 'Nigel'), 0.2687639203842084
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim('Colin', 'Coiln'), 0.2687639203842084
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim('Coiln', 'Colin'), 0.2687639203842084
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5959107950190301
        )

    def test_fellegi_sunter_dist(self):
        """Test abydos.distance.FellegiSunter.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.413104441465901)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.729681688)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.729681688)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.729681688)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.729681688)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.7185855244
        )

        # Simplified variant cases
        self.assertEqual(self.cmp_simp.dist('', ''), 1.0)
        self.assertEqual(self.cmp_simp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_simp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_simp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_simp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_simp.dist('abc', 'abc'), 0.07580375925340632)
        self.assertEqual(self.cmp_simp.dist('abcd', 'efgh'), 1.0)
        self.assertAlmostEqual(
            self.cmp_simp.dist('Nigel', 'Niall'), 0.7312360796157916
        )
        self.assertAlmostEqual(
            self.cmp_simp.dist('Niall', 'Nigel'), 0.7312360796157916
        )
        self.assertAlmostEqual(
            self.cmp_simp.dist('Colin', 'Coiln'), 0.7312360796157916
        )
        self.assertAlmostEqual(
            self.cmp_simp.dist('Coiln', 'Colin'), 0.7312360796157916
        )
        self.assertAlmostEqual(
            self.cmp_simp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4040892049809699
        )

    def test_fellegi_sunter_sim_score(self):
        """Test abydos.distance.FellegiSunter.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 1.760686675602297)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 1.3515915598
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 1.3515915598
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 1.3515915598
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 1.3515915598
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 2.8141447562
        )

        # Simplified variant cases
        self.assertEqual(self.cmp_simp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_simp.sim_score('a', ''), -0.6931471805599453)
        self.assertEqual(self.cmp_simp.sim_score('', 'a'), 0.0)
        self.assertEqual(
            self.cmp_simp.sim_score('abc', ''), -2.772588722239781
        )
        self.assertEqual(self.cmp_simp.sim_score('', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_simp.sim_score('abc', 'abc'), 5.545177444479562
        )
        self.assertEqual(
            self.cmp_simp.sim_score('abcd', 'efgh'), -4.023594781085251
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim_score('Nigel', 'Niall'), 2.6876392038420835
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim_score('Niall', 'Nigel'), 2.6876392038420835
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim_score('Colin', 'Coiln'), 2.6876392038420835
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim_score('Coiln', 'Colin'), 2.6876392038420835
        )
        self.assertAlmostEqual(
            self.cmp_simp.sim_score('ATCAACGAGT', 'AACGATTAG'),
            11.322305105361572,
        )


if __name__ == '__main__':
    unittest.main()
