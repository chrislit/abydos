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

"""abydos.tests.distance.test_distance_azzoo.

This module contains unit tests for abydos.distance.AZZOO
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import AZZOO


class AZZOOTestCases(unittest.TestCase):
    """Test AZZOO functions.

    abydos.distance.AZZOO
    """

    cmp = AZZOO()

    def test_azzoo_sim(self):
        """Test abydos.distance.AZZOO.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9809885931558935)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9886075949)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9886075949)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9886075949)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9886075949)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.986163522
        )

    def test_azzoo_sim_score(self):
        """Test abydos.distance.AZZOO.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 392.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 391.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 391.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 390.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 390.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 394.0)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 387.0)

        self.assertAlmostEqual(self.cmp.sim_score('Nigel', 'Niall'), 390.5)
        self.assertAlmostEqual(self.cmp.sim_score('Niall', 'Nigel'), 390.5)
        self.assertAlmostEqual(self.cmp.sim_score('Colin', 'Coiln'), 390.5)
        self.assertAlmostEqual(self.cmp.sim_score('Coiln', 'Colin'), 390.5)
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 392.0
        )


if __name__ == '__main__':
    unittest.main()
