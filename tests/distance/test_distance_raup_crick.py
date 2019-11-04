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

"""abydos.tests.distance.test_distance_raup_crick.

This module contains unit tests for abydos.distance.RaupCrick
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import RaupCrick


class RaupCrickTestCases(unittest.TestCase):
    """Test RaupCrick functions.

    abydos.distance.RaupCrick
    """

    cmp = RaupCrick()

    def test_inclusion_sim(self):
        """Test abydos.distance.RaupCrick.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0114358323)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0114358323)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0114358323)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0114358323)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0139593909
        )


if __name__ == '__main__':
    unittest.main()
