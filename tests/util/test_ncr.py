# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.util.test_ncr.

This module contains unit tests for abydos.util._ncr
"""

import unittest

from abydos.util._ncr import _ncr


class ProdTestCases(unittest.TestCase):
    """Test cases for abydos.util._ncr."""

    def test_ncr(self):
        """Test abydos.util._ncr."""
        self.assertEqual(_ncr(1, 0), 1)
        self.assertEqual(_ncr(5, 0), 1)

        self.assertEqual(_ncr(1, 2), 0)
        self.assertEqual(_ncr(1, 2), 0)

        self.assertEqual(_ncr(2, 2), 1)
        self.assertEqual(_ncr(10, 10), 1)

        self.assertEqual(_ncr(7, 2), 21)
        self.assertEqual(_ncr(7, 3), 35)
        self.assertEqual(_ncr(4, 3), 4)
        self.assertEqual(_ncr(5, 3), 10)
        self.assertEqual(_ncr(10, 2), 45)
        self.assertEqual(_ncr(100, 3), 161700)
        self.assertEqual(_ncr(80, 5), 24040016)

        # gamma variant
        self.assertAlmostEqual(_ncr(10, 2.5), 77.8023559942)
        self.assertAlmostEqual(_ncr(0, 2.5), 0.12732395447)
        self.assertAlmostEqual(_ncr(2.5, 2.5), 1)
        self.assertAlmostEqual(_ncr(2.5, 2.1), 1.7043970865)


if __name__ == '__main__':
    unittest.main()
