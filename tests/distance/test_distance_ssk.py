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

"""abydos.tests.distance.test_distance_ssk.

This module contains unit tests for abydos.distance.SSK
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import SSK


class SSKTestCases(unittest.TestCase):
    """Test SSK functions.

    abydos.distance.SSK
    """

    cmp = SSK()
    cmp_05 = SSK(ssk_lambda=0.05)

    def test_saps_sim(self):
        """Test abydos.distance.SSK.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0666666667)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0666666667)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4333333333
        )

        # Examples from paper
        self.assertAlmostEqual(
            self.cmp.sim('cat', 'car'), 0.551724138
        )

    def test_saps_sim_score(self):
        """Test abydos.distance.SSK.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0)
        self.assertEqual(self.cmp.sim_score('a', ''), -3)
        self.assertEqual(self.cmp.sim_score('', 'a'), -3)
        self.assertEqual(self.cmp.sim_score('abc', ''), -7)
        self.assertEqual(self.cmp.sim_score('', 'abc'), -7)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 13)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), -7)

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 1)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 1)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 13
        )

        # Examples from paper
        self.assertEqual(self.cmp.sim_score('cat', 'car'), 16)


if __name__ == '__main__':
    unittest.main()
