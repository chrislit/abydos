# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_ncd_paq9a.

This module contains unit tests for abydos.distance.NCDpaq9a
"""

import unittest

from abydos.distance import NCDpaq9a

from six import PY2


class NCDpaq9aTestCases(unittest.TestCase):
    """Test NCDpaq9a functions.

    abydos.distance.NCDpaq9a
    """

    cmp = NCDpaq9a()

    def test_ncd_paq9a_dist(self):
        """Test abydos.distance.NCDpaq9a.dist."""
        if PY2:  # skip tests since paq9a isn't supported on Python 2.7
            return
        try:
            import paq  # noqa: F401
        except ImportError:  # pragma: no cover
            return

        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.2)
        self.assertEqual(self.cmp.dist('', 'a'), 0.2)
        self.assertEqual(self.cmp.dist('abc', ''), 0.42857142857142855)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.42857142857142855)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5555555556)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5555555556)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5555555556)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5555555556)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.6153846154
        )

    def test_ncd_paq9a_sim(self):
        """Test abydos.distance.NCDpaq9a.sim."""
        if PY2:  # skip tests since paq9a isn't supported on Python 2.7
            return

        try:
            import paq  # noqa: F401
        except ImportError:  # pragma: no cover
            return

        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.8)
        self.assertEqual(self.cmp.sim('', 'a'), 0.8)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5714285714285714)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5714285714285714)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.5)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4444444444)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4444444444)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4444444444)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4444444444)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.3846153846
        )


if __name__ == '__main__':
    unittest.main()
