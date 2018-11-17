# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_typo.

This module contains unit tests for abydos.distance.Typo
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Typo, dist_typo, sim_typo, typo


class TypoTestCases(unittest.TestCase):
    """Test Typo functions.

    abydos.distance.Typo
    """

    cmp = Typo()

    def test_typo_dist_abs(self):
        """Test abydos.distance.Typo.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', 'typo'), 4)
        self.assertEqual(self.cmp.dist_abs('typo', ''), 4)

        self.assertEqual(self.cmp.dist_abs('asdf', 'zxcv'), 2)
        self.assertEqual(self.cmp.dist_abs('asdf', 'ASDF'), 1)
        self.assertEqual(self.cmp.dist_abs('asdf', 'qsdf'), 0.5)

        self.assertAlmostEqual(
            self.cmp.dist_abs('asdf', 'asdt', metric='euclidean'), 0.70710677
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('asdf', 'asdt', metric='manhattan'), 1
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('asdf', 'asdt', metric='log-euclidean'),
            0.4406868,
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('asdf', 'asdt', metric='log-manhattan'),
            0.54930615,
        )

        self.assertRaises(ValueError, self.cmp.dist_abs, 'asdf', 'Ösdf')

        # Test wrapper
        self.assertAlmostEqual(
            typo('asdf', 'asdt', metric='log-euclidean'), 0.4406868
        )

    def test_typo_sim(self):
        """Test abydos.distance.Typo.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('', 'typo'), 0)
        self.assertEqual(self.cmp.sim('typo', ''), 0)

        self.assertEqual(self.cmp.sim('asdf', 'zxcv'), 0.5)
        self.assertEqual(self.cmp.sim('asdf', 'ASDF'), 0.75)
        self.assertEqual(self.cmp.sim('asdf', 'qsdf'), 0.875)

        self.assertAlmostEqual(
            self.cmp.sim('asdf', 'asdt', metric='euclidean'),
            1 - (0.70710677 / 4),
        )
        self.assertAlmostEqual(
            self.cmp.sim('asdf', 'asdt', metric='manhattan'), 0.75
        )
        self.assertAlmostEqual(
            self.cmp.sim('asdf', 'asdt', metric='log-euclidean'),
            1 - (0.4406868 / 4),
        )
        self.assertAlmostEqual(
            self.cmp.sim('asdf', 'asdt', metric='log-manhattan'),
            1 - (0.54930615 / 4),
        )

        # Test wrapper
        self.assertAlmostEqual(
            sim_typo('asdf', 'asdt', metric='log-euclidean'),
            1 - (0.4406868 / 4),
        )

    def test_typo_dist(self):
        """Test abydos.distance.Typo.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('', 'typo'), 1)
        self.assertEqual(self.cmp.dist('typo', ''), 1)

        self.assertEqual(self.cmp.dist('asdf', 'zxcv'), 0.5)
        self.assertEqual(self.cmp.dist('asdf', 'ASDF'), 0.25)
        self.assertEqual(self.cmp.dist('asdf', 'qsdf'), 0.125)

        self.assertAlmostEqual(
            self.cmp.dist('asdf', 'asdt', metric='euclidean'), 0.70710677 / 4
        )
        self.assertAlmostEqual(
            self.cmp.dist('asdf', 'asdt', metric='manhattan'), 0.25
        )
        self.assertAlmostEqual(
            self.cmp.dist('asdf', 'asdt', metric='log-euclidean'),
            0.4406868 / 4,
        )
        self.assertAlmostEqual(
            self.cmp.dist('asdf', 'asdt', metric='log-manhattan'),
            0.54930615 / 4,
        )

        # Test wrapper
        self.assertAlmostEqual(
            dist_typo('asdf', 'asdt', metric='log-euclidean'), 0.4406868 / 4
        )


if __name__ == '__main__':
    unittest.main()
