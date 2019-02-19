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

"""abydos.tests.distance.test_distance_stuart_tau.

This module contains unit tests for abydos.distance.StuartTau
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import StuartTau


class StuartTauTestCases(unittest.TestCase):
    """Test StuartTau functions.

    abydos.distance.StuartTau
    """

    cmp = StuartTau()
    cmp_no_d = StuartTau(alphabet=1)

    def test_stuart_tau_sim(self):
        """Test abydos.distance.StuartTau.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.00510204081632653)
        self.assertEqual(self.cmp.sim('a', ''), 0.005076009995835068)
        self.assertEqual(self.cmp.sim('', 'a'), 0.005076009995835068)
        self.assertEqual(self.cmp.sim('abc', ''), 0.005049979175343606)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.005049979175343606)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.00510204081632653)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0049718867138692216)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0050239484)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0050239484)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0050239484)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0050239484)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0050109329
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 4.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), -2.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), -2.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -0.4)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), -0.1481481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), -0.1481481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), -0.1481481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), -0.1481481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0
        )


if __name__ == '__main__':
    unittest.main()
