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

"""abydos.tests.distance.test_distance_faith.

This module contains unit tests for abydos.distance.Faith
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Faith


class FaithTestCases(unittest.TestCase):
    """Test Faith functions.

    abydos.distance.Faith
    """

    cmp = Faith()

    def test_faith_sim(self):
        """Test abydos.distance.Faith.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5)
        self.assertEqual(self.cmp.sim('a', ''), 0.4987244897959184)
        self.assertEqual(self.cmp.sim('', 'a'), 0.4987244897959184)
        self.assertEqual(self.cmp.sim('abc', ''), 0.49744897959183676)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.49744897959183676)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 4.497448979591836)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.49362244897959184)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 3.4942602041)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 3.4942602041)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 3.4942602041)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 3.4942602041)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 7.4910714286
        )


if __name__ == '__main__':
    unittest.main()
