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

"""abydos.tests.distance.test_distance_chebyshev.

This module contains unit tests for abydos.distance.Chebyshev
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Chebyshev, chebyshev
from abydos.tokenizer import QGrams

from .. import NONQ_FROM, NONQ_TO


class ChebyshevTestCases(unittest.TestCase):
    """Test Chebyshev functions.

    abydos.distance.Chebyshev
    """

    cmp = Chebyshev()

    def test_chebyshev_dist_abs(self):
        """Test abydos.distance.Chebyshev.dist_abs."""
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', ''), 1)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen'), 1)
        self.assertEqual(self.cmp.dist_abs('nelson', 'neilsen'), 1)

        self.assertEqual(self.cmp.dist_abs('', '', 2), 0)
        self.assertEqual(self.cmp.dist_abs('nelson', '', 2), 1)
        self.assertEqual(self.cmp.dist_abs('', 'neilsen', 2), 1)
        self.assertAlmostEqual(self.cmp.dist_abs('nelson', 'neilsen', 2), 1)

        # supplied q-gram tests
        self.assertEqual(self.cmp.dist_abs(QGrams(''), QGrams('')), 0)
        self.assertEqual(self.cmp.dist_abs(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(self.cmp.dist_abs(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            self.cmp.dist_abs(QGrams('nelson'), QGrams('neilsen')), 1
        )

        # non-q-gram tests
        self.assertEqual(self.cmp.dist_abs('', '', 0), 0)
        self.assertEqual(self.cmp.dist_abs('the quick', '', 0), 1)
        self.assertEqual(self.cmp.dist_abs('', 'the quick', 0), 1)
        self.assertAlmostEqual(self.cmp.dist_abs(NONQ_FROM, NONQ_TO, 0), 1)
        self.assertAlmostEqual(self.cmp.dist_abs(NONQ_TO, NONQ_FROM, 0), 1)

        # Test wrapper
        self.assertAlmostEqual(chebyshev('nelson', 'neilsen', 2), 1)


if __name__ == '__main__':
    unittest.main()
