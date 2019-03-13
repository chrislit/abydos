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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

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
        with self.assertRaises(NotImplementedError):
            self.cmp.sim('a', 'a')

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
