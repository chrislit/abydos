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

This module contains unit tests for abydos.distance._typo
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
import unittest

from abydos.distance import dist_typo, sim_typo, typo


class TypoTestCases(unittest.TestCase):
    """Test Typo functions.

    abydos.distance._typo.typo, sim_typo & .dist_typo
    """

    def test_typo(self):
        """Test abydos.distance._typo.typo."""
        # Base cases
        self.assertEqual(typo('', ''), 0)
        self.assertEqual(typo('', 'typo'), 4)
        self.assertEqual(typo('typo', ''), 4)

        self.assertEqual(typo('asdf', 'zxcv'), 2)
        self.assertEqual(typo('asdf', 'ASDF'), 1)
        self.assertEqual(typo('asdf', 'qsdf'), 0.5)

        self.assertAlmostEqual(
            typo('asdf', 'asdt', metric='euclidean'), 0.70710677
        )
        self.assertAlmostEqual(typo('asdf', 'asdt', metric='manhattan'), 1)
        self.assertAlmostEqual(
            typo('asdf', 'asdt', metric='log-euclidean'), 0.4406868
        )
        self.assertAlmostEqual(
            typo('asdf', 'asdt', metric='log-manhattan'), 0.54930615
        )

        self.assertRaises(ValueError, typo, 'asdf', 'Ösdf')

    def test_sim_typo(self):
        """Test abydos.distance._typo.sim_typo."""
        # Base cases
        self.assertEqual(sim_typo('', ''), 1)
        self.assertEqual(sim_typo('', 'typo'), 0)
        self.assertEqual(sim_typo('typo', ''), 0)

        self.assertEqual(sim_typo('asdf', 'zxcv'), 0.5)
        self.assertEqual(sim_typo('asdf', 'ASDF'), 0.75)
        self.assertEqual(sim_typo('asdf', 'qsdf'), 0.875)

        self.assertAlmostEqual(
            sim_typo('asdf', 'asdt', metric='euclidean'), 1 - (0.70710677 / 4)
        )
        self.assertAlmostEqual(
            sim_typo('asdf', 'asdt', metric='manhattan'), 0.75
        )
        self.assertAlmostEqual(
            sim_typo('asdf', 'asdt', metric='log-euclidean'),
            1 - (0.4406868 / 4),
        )
        self.assertAlmostEqual(
            sim_typo('asdf', 'asdt', metric='log-manhattan'),
            1 - (0.54930615 / 4),
        )

    def test_dist_typo(self):
        """Test abydos.distance._typo.dist_typo."""
        # Base cases
        self.assertEqual(dist_typo('', ''), 0)
        self.assertEqual(dist_typo('', 'typo'), 1)
        self.assertEqual(dist_typo('typo', ''), 1)

        self.assertEqual(dist_typo('asdf', 'zxcv'), 0.5)
        self.assertEqual(dist_typo('asdf', 'ASDF'), 0.25)
        self.assertEqual(dist_typo('asdf', 'qsdf'), 0.125)

        self.assertAlmostEqual(
            dist_typo('asdf', 'asdt', metric='euclidean'), 0.70710677 / 4
        )
        self.assertAlmostEqual(
            dist_typo('asdf', 'asdt', metric='manhattan'), 0.25
        )
        self.assertAlmostEqual(
            dist_typo('asdf', 'asdt', metric='log-euclidean'), 0.4406868 / 4
        )
        self.assertAlmostEqual(
            dist_typo('asdf', 'asdt', metric='log-manhattan'), 0.54930615 / 4
        )


if __name__ == '__main__':
    unittest.main()
