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

import unittest

from abydos.distance import Typo, dist_typo, sim_typo, typo


class TypoTestCases(unittest.TestCase):
    """Test Typo functions.

    abydos.distance.Typo
    """

    cmp = Typo()
    cmp_auto = Typo(layout='auto', failsafe=True)

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
            Typo(metric='euclidean').dist_abs('asdf', 'asdt'), 0.70710677
        )
        self.assertAlmostEqual(
            Typo(metric='manhattan').dist_abs('asdf', 'asdt'), 1
        )
        self.assertAlmostEqual(
            Typo(metric='log-euclidean').dist_abs('asdf', 'asdt'), 0.4406868
        )
        self.assertAlmostEqual(
            Typo(metric='log-manhattan').dist_abs('asdf', 'asdt'), 0.54930615
        )

        self.assertEqual(self.cmp_auto.dist_abs('Schluß', 'Schluss'), 3)
        self.assertAlmostEqual(
            self.cmp_auto.dist_abs('délicat', 'delicate'), 1.7071068
        )
        self.assertEqual(self.cmp_auto.dist_abs('비빔밥', 'Bibimbap'), 11)

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
            Typo(metric='euclidean').sim('asdf', 'asdt'), 1 - (0.70710677 / 4)
        )
        self.assertAlmostEqual(
            Typo(metric='manhattan').sim('asdf', 'asdt'), 0.75
        )
        self.assertAlmostEqual(
            Typo(metric='log-euclidean').sim('asdf', 'asdt'),
            1 - (0.4406868 / 4),
        )
        self.assertAlmostEqual(
            Typo(metric='log-manhattan').sim('asdf', 'asdt'),
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
            Typo(metric='euclidean').dist('asdf', 'asdt'), 0.70710677 / 4
        )
        self.assertAlmostEqual(
            Typo(metric='manhattan').dist('asdf', 'asdt'), 0.25
        )
        self.assertAlmostEqual(
            Typo(metric='log-euclidean').dist('asdf', 'asdt'), 0.4406868 / 4
        )
        self.assertAlmostEqual(
            Typo(metric='log-manhattan').dist('asdf', 'asdt'), 0.54930615 / 4
        )

        # Test wrapper
        self.assertAlmostEqual(
            dist_typo('asdf', 'asdt', metric='log-euclidean'), 0.4406868 / 4
        )


if __name__ == '__main__':
    unittest.main()
