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

"""abydos.tests.distance.test_distance_lig3.

This module contains unit tests for abydos.distance.LIG3
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import LIG3


class LIG3TestCases(unittest.TestCase):
    """Test LIG3 functions.

    abydos.distance.LIG3
    """

    cmp = LIG3()

    def test_lig3_sim(self):
        """Test abydos.distance.LIG3.sim."""
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
        self.assertEqual(self.cmp.sim('Glavin', 'Glawyn'), 0.8)
        self.assertEqual(
            self.cmp.sim('Williams', 'Vylliems'), 0.7692307692307693
        )
        self.assertEqual(self.cmp.sim('Lewis', 'Louis'), 0.75)
        self.assertEqual(self.cmp.sim('Alex', 'Alexander'), 0.6153846153846154)
        self.assertEqual(self.cmp.sim('Wild', 'Wildsmith'), 0.6153846153846154)
        self.assertEqual(
            self.cmp.sim('Bram', 'Bramberley'), 0.5714285714285714
        )


if __name__ == '__main__':
    unittest.main()
