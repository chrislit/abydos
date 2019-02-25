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

"""abydos.tests.distance.test_distance_consonni_todeschini_iii.

This module contains unit tests for abydos.distance.ConsonniTodeschiniIII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ConsonniTodeschiniIII


class ConsonniTodeschiniIIITestCases(unittest.TestCase):
    """Test ConsonniTodeschiniIII functions.

    abydos.distance.ConsonniTodeschiniIII
    """

    cmp = ConsonniTodeschiniIII()
    cmp_no_d = ConsonniTodeschiniIII(alphabet=1)

    def test_consonni_todeschini_iii_sim(self):
        """Test abydos.distance.ConsonniTodeschiniIII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.24145128700608987)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.2079748185)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.2079748185)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.2079748185)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.2079748185)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.3119622277
        )

    def test_consonni_todeschini_iii_dist(self):
        """Test abydos.distance.ConsonniTodeschiniIII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.7585487129939101)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.7920251815)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.7920251815)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.7920251815)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.7920251815)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.6880377723
        )


if __name__ == '__main__':
    unittest.main()