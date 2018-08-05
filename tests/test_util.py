# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tests.test_util.

This module contains unit tests for abydos.util
"""

import unittest

from abydos.util import prod

from six.moves import range


class ProdTestCases(unittest.TestCase):
    """Test cases for abydos.util.prod."""

    def test_prod(self):
        """Test abydos.util.prod."""
        self.assertEqual(prod([]), 1)
        self.assertEqual(prod(()), 1)
        self.assertEqual(prod({}), 1)

        self.assertEqual(prod([1, 1, 1, 1, 1]), 1)
        self.assertEqual(prod((1, 1, 1, 1, 1)), 1)
        self.assertEqual(prod({1, 1, 1, 1, 1}), 1)

        self.assertEqual(prod([2, 2, 2, 2, 2]), 32)
        self.assertEqual(prod((2, 2, 2, 2, 2)), 32)
        self.assertEqual(prod({2, 2, 2, 2, 2}), 2)

        self.assertEqual(prod([1, 2, 3, 4, 5]), 120)
        self.assertEqual(prod((1, 2, 3, 4, 5)), 120)
        self.assertEqual(prod({1, 2, 3, 4, 5}), 120)
        self.assertEqual(prod(range(1, 6)), 120)
        self.assertEqual(prod(list(range(1, 6))), 120)
        self.assertEqual(prod(tuple(range(1, 6))), 120)
        self.assertEqual(prod(set(range(1, 6))), 120)

        self.assertEqual(prod(range(6)), 0)
        self.assertEqual(prod(list(range(6))), 0)
        self.assertEqual(prod(tuple(range(6))), 0)
        self.assertEqual(prod(set(range(6))), 0)


if __name__ == '__main__':
    unittest.main()
