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

"""abydos.tests.distance.test_distance_consonni_todeschini_ii.

This module contains unit tests for abydos.distance.ConsonniTodeschiniII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ConsonniTodeschiniII


class ConsonniTodeschiniIITestCases(unittest.TestCase):
    """Test ConsonniTodeschiniII functions.

    abydos.distance.ConsonniTodeschiniII
    """

    cmp = ConsonniTodeschiniII()

    def test_consonni_todeschini_ii_sim(self):
        """Test abydos.distance.ConsonniTodeschiniII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.8351838558230296)
        self.assertEqual(self.cmp.sim('', 'a'), 0.8351838558230296)
        self.assertEqual(self.cmp.sim('abc', ''), 0.7585487129939101)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.7585487129939101)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.640262668568961)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7080704349)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7080704349)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7080704349)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7080704349)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6880377723
        )


if __name__ == '__main__':
    unittest.main()
