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

"""abydos.tests.distance.test_distance_smith_waterman.

This module contains unit tests for abydos.distance.SmithWaterman
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import SmithWaterman, smith_waterman

from six.moves import range

from .test_distance_needleman_wunsch import _sim_nw, _sim_wikipedia
from .. import NIALL


class SmithWatermanTestCases(unittest.TestCase):
    """Test Smith-Waterman functions.

    abydos.distance.SmithWaterman
    """

    def test_smith_waterman_dist_abs(self):
        """Test abydos.distance.SmithWaterman.dist_abs."""
        self.assertEqual(SmithWaterman().dist_abs('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(
            SmithWaterman(1, _sim_nw).dist_abs('GATTACA', 'GCATGCU'), 0
        )
        self.assertEqual(
            SmithWaterman(5, _sim_wikipedia).dist_abs(
                'AGACTAGTTAC', 'CGAGACGT'
            ),
            26,
        )

        sw5 = SmithWaterman(5, _sim_nw)
        self.assertEqual(sw5.dist_abs('CGATATCAG', 'TGACGSTGC'), 0)
        self.assertEqual(sw5.dist_abs('AGACTAGTTAC', 'TGACGSTGC'), 1)
        self.assertEqual(sw5.dist_abs('AGACTAGTTAC', 'CGAGACGT'), 0)

        # Test wrapper
        self.assertEqual(
            smith_waterman('AGACTAGTTAC', 'CGAGACGT', 5, _sim_wikipedia), 26
        )

    def test_smith_waterman_dist_abs_nialls(self):
        """Test abydos.distance.SmithWaterman.dist_abs (Nialls set)."""
        sw_vals = (5, 1, 1, 3, 2, 1, 1, 0, 0, 1, 1, 2, 2, 1, 0, 0)
        sw2 = SmithWaterman(2, _sim_nw)
        for i in range(len(NIALL)):
            self.assertEqual(sw2.dist_abs(NIALL[0], NIALL[i]), sw_vals[i])


if __name__ == '__main__':
    unittest.main()
