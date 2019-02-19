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

"""abydos.tests.distance.test_distance_kuhns_vii.

This module contains unit tests for abydos.distance.KuhnsVII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsVII


class KuhnsVIITestCases(unittest.TestCase):
    """Test KuhnsVII functions.

    abydos.distance.KuhnsVII
    """

    cmp = KuhnsVII()

    def test_kuhns_vii_sim(self):
        """Test abydos.distance.KuhnsVII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9974489795918368)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.0025510204081632655)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4974489796)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6648698948
        )


if __name__ == '__main__':
    unittest.main()
