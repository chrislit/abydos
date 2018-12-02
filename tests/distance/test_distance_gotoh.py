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

"""abydos.tests.distance.test_distance_gotoh.

This module contains unit tests for abydos.distance.Gotoh
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Gotoh, NeedlemanWunsch, gotoh

from six.moves import range

from .test_distance_needleman_wunsch import _sim_nw, _sim_wikipedia
from .. import NIALL


class GotohTestCases(unittest.TestCase):
    """Test Gotoh functions.

    abydos.distance.Gotoh
    """

    def test_gotoh_dist_abs(self):
        """Test abydos.distance.Gotoh.dist_abs."""
        self.assertEqual(Gotoh().dist_abs('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(
            Gotoh(1, 1, _sim_nw).dist_abs('GATTACA', 'GCATGCU'), 0
        )
        self.assertGreaterEqual(
            Gotoh(1, 0.5, _sim_nw).dist_abs('GATTACA', 'GCATGCU'),
            NeedlemanWunsch(1, _sim_nw).dist_abs('GATTACA', 'GCATGCU'),
        )
        self.assertEqual(
            Gotoh(5, 5, _sim_wikipedia).dist_abs('AGACTAGTTAC', 'CGAGACGT'), 16
        )
        self.assertGreaterEqual(
            Gotoh(5, 2, _sim_wikipedia).dist_abs('AGACTAGTTAC', 'CGAGACGT'),
            NeedlemanWunsch(5, _sim_wikipedia).dist_abs(
                'AGACTAGTTAC', 'CGAGACGT'
            ),
        )

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        self.assertEqual(
            Gotoh(5, 5, _sim_nw).dist_abs('CGATATCAG', 'TGACGSTGC'), -5
        )
        self.assertGreaterEqual(
            Gotoh(5, 2, _sim_nw).dist_abs('CGATATCAG', 'TGACGSTGC'),
            NeedlemanWunsch(5, _sim_nw).dist_abs('CGATATCAG', 'TGACGSTGC'),
        )
        self.assertEqual(
            Gotoh(5, 5, _sim_nw).dist_abs('AGACTAGTTAC', 'TGACGSTGC'), -7
        )
        self.assertGreaterEqual(
            Gotoh(5, 2, _sim_nw).dist_abs('AGACTAGTTAC', 'TGACGSTGC'),
            NeedlemanWunsch(5, _sim_nw).dist_abs('AGACTAGTTAC', 'TGACGSTGC'),
        )
        self.assertEqual(
            Gotoh(5, 5, _sim_nw).dist_abs('AGACTAGTTAC', 'CGAGACGT'), -15
        )
        self.assertGreaterEqual(
            Gotoh(5, 2, _sim_nw).dist_abs('AGACTAGTTAC', 'CGAGACGT'),
            NeedlemanWunsch(5, _sim_nw).dist_abs('AGACTAGTTAC', 'CGAGACGT'),
        )

        # Test wrapper
        self.assertEqual(
            gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 5, _sim_wikipedia), 16
        )

    def test_gotoh_dist_abs_nialls(self):
        """Test abydos.distance.Gotoh.dist_abs (Nialls set)."""
        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=2, skew=2)
        nw_vals = (5, 0, -2, 3, 1, 1, -2, -2, -1, -3, -3, -5, -3, -7, -7, -19)
        g22 = Gotoh(2, 2, _sim_nw)
        for i in range(len(NIALL)):
            self.assertEqual(g22.dist_abs(NIALL[0], NIALL[i]), nw_vals[i])
        nw_vals2 = (5, 0, -2, 3, 1, 1, -2, -2, -1, -2, -3, -3, -2, -6, -6, -8)
        g21 = Gotoh(2, 1, _sim_nw)
        g205 = Gotoh(2, 0.5, _sim_nw)
        nw2 = NeedlemanWunsch(2, _sim_nw)
        for i in range(len(NIALL)):
            self.assertEqual(g21.dist_abs(NIALL[0], NIALL[i]), nw_vals2[i])
            self.assertGreaterEqual(
                g205.dist_abs(NIALL[0], NIALL[i]),
                nw2.dist_abs(NIALL[0], NIALL[i]),
            )


if __name__ == '__main__':
    unittest.main()
