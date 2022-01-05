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

"""abydos.tests.distance.test_distance_vps.

This module contains unit tests for abydos.distance.VPS
"""

import unittest

from abydos.distance import VPS


class VPSTestCases(unittest.TestCase):
    """Test VPS functions.

    abydos.distance.VPS
    """

    cmp = VPS()

    def test_vps_sim(self):
        """Test abydos.distance.VPS.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        # Testcases from paper
        self.assertEqual(
            self.cmp.sim('AINSCOMBE', 'ANSCOMB'), 0.5972222222222222
        )
        self.assertEqual(
            self.cmp.sim('AINSCOMBE', 'ANSCOMBE'), 0.7083333333333334
        )
        self.assertEqual(
            self.cmp.sim('AINSCOMBE', 'BRANSCOMB'), 0.5879629629629629
        )
        self.assertEqual(
            self.cmp.sim('AINSCOMBE', 'DASCOMBE'), 0.5925925925925926
        )
        self.assertEqual(self.cmp.sim('AINSCOMBE', 'DUNSCOMBE'), 0.75)
        self.assertEqual(
            self.cmp.sim('AINSCOMBE', 'HANSCOMB'), 0.6620370370370371
        )
        self.assertEqual(
            self.cmp.sim('AINSCOMBE', 'LIPSCOMBE'), 0.6666666666666666
        )
        self.assertEqual(
            self.cmp.sim('AINSCOMBE', 'LUSCOMBE'), 0.5555555555555556
        )
        self.assertEqual(self.cmp.sim('JULIA', 'JULIAN'), 0.8)
        self.assertEqual(self.cmp.sim('JULIA', 'JULIANA'), 0.7063492063492063)
        self.assertEqual(self.cmp.sim('JULIA', 'JULIANNA'), 0.6011904761904762)
        self.assertEqual(self.cmp.sim('JULIA', 'JULIE'), 0.75)
        self.assertEqual(self.cmp.sim('JULIA', 'JULIET'), 0.6)
        self.assertEqual(self.cmp.sim('JULIA', 'JULIUS'), 0.6333333333333333)
        self.assertEqual(self.cmp.sim('ROBBINS', 'ROBYNS'), 0.5238095238095238)


if __name__ == '__main__':
    unittest.main()
