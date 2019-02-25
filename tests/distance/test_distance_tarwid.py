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

"""abydos.tests.distance.test_distance_tarwid.

This module contains unit tests for abydos.distance.Tarwid
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Tarwid


class TarwidTestCases(unittest.TestCase):
    """Test Tarwid functions.

    abydos.distance.Tarwid
    """

    cmp = Tarwid()
    cmp_no_d = Tarwid(alphabet=0)

    def test_tarwid_sim(self):
        """Test abydos.distance.Tarwid.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9698492462)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9698492462)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9698492462)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9698492462)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9607002501
        )

    def test_tarwid_dist(self):
        """Test abydos.distance.Tarwid.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.010152284263959421)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0301507538)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0301507538)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0301507538)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0301507538)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0392997499
        )


if __name__ == '__main__':
    unittest.main()
