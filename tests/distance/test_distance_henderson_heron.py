# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_henderson_heron.

This module contains unit tests for abydos.distance.HendersonHeron
"""

import unittest

from abydos.distance import HendersonHeron


class HendersonHeronTestCases(unittest.TestCase):
    """Test HendersonHeron functions.

    abydos.distance.HendersonHeron
    """

    cmp = HendersonHeron()

    def test_henderson_heron_dist(self):
        """Test abydos.distance.HendersonHeron.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('a', 'a'), 3.258008184e-06)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertAlmostEqual(self.cmp.dist('abc', 'abc'), 6.40140979487e-11)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.9684367974410505)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 4.94203602e-06)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 4.94203602e-06)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 4.94203602e-06)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 4.94203602e-06)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 1.108779488e-12
        )


if __name__ == '__main__':
    unittest.main()
