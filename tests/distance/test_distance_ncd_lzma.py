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

"""abydos.tests.distance.test_distance_ncd_lzma.

This module contains unit tests for abydos.distance.NCDlzma
"""

import unittest

from abydos.distance import NCDlzma, dist_ncd_lzma, sim_ncd_lzma

from six import PY3

try:
    import lzma
except ImportError:  # pragma: no cover
    # If the system lacks the lzma library, that's fine, but lzma compression
    # similarity won't be supported.
    lzma = None


class CompressionTestCases(unittest.TestCase):
    """Test compression distance functions.

    abydos.distance.NCDlzma
    """

    if lzma is not None:
        cmp = NCDlzma()

    def test_ncd_lzma_dist(self):
        """Test abydos.distance.NCDlzma.dist."""
        if lzma is not None:
            self.assertEqual(self.cmp.dist('', ''), 0)
            if PY3:
                self.assertAlmostEqual(self.cmp.dist('a', ''), 0.6086956521739)
                self.assertAlmostEqual(self.cmp.dist('abcdefg', 'fg'), 0.16)
            else:
                self.assertAlmostEqual(self.cmp.dist('a', ''), 0.5714285714286)
                self.assertAlmostEqual(
                    self.cmp.dist('abcdefg', 'fg'), 0.1739130434783
                )

            # Test wrapper
            if PY3:
                self.assertAlmostEqual(dist_ncd_lzma('abcdefg', 'fg'), 0.16)
            else:
                self.assertAlmostEqual(
                    dist_ncd_lzma('abcdefg', 'fg'), 0.1739130434783
                )

    def test_ncd_lzma_sim(self):
        """Test abydos.distance.NCDlzma.sim."""
        if lzma is not None:
            self.assertEqual(self.cmp.sim('', ''), 1)
            if PY3:
                self.assertAlmostEqual(self.cmp.sim('a', ''), 0.391304347826)
                self.assertAlmostEqual(self.cmp.sim('abcdefg', 'fg'), 0.84)
            else:
                self.assertAlmostEqual(self.cmp.sim('a', ''), 0.428571428571)
                self.assertAlmostEqual(
                    self.cmp.sim('abcdefg', 'fg'), 0.8260869565217
                )

            # Test wrapper
            if PY3:
                self.assertAlmostEqual(sim_ncd_lzma('abcdefg', 'fg'), 0.84)
            else:
                self.assertAlmostEqual(
                    sim_ncd_lzma('abcdefg', 'fg'), 0.8260869565217
                )


if __name__ == '__main__':
    unittest.main()
