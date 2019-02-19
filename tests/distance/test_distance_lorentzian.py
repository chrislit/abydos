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

"""abydos.tests.distance.test_distance_lorentzian.

This module contains unit tests for abydos.distance.Lorentzian
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Lorentzian


class LorentzianTestCases(unittest.TestCase):
    """Test Lorentzian functions.

    abydos.distance.Lorentzian
    """

    cmp = Lorentzian()

    def test_lorentzian_dist_abs(self):
        """Test abydos.distance.Lorentzian.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1.3862943611198906)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1.3862943611198906)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 2.772588722239781)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 2.772588722239781)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 6.931471805599453)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 4.1588830834
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 4.1588830834
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 4.1588830834
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 4.1588830834
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 4.8520302639
        )


if __name__ == '__main__':
    unittest.main()
