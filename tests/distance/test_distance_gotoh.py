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

from abydos.distance import (
    Gotoh,
    NeedlemanWunsch,
    gotoh,
)

from six.moves import range

from .test_distance_needleman_wunsch import _sim_nw, _sim_wikipedia
from .. import NIALL


class GotohTestCases(unittest.TestCase):
    """Test Gotoh functions.

    abydos.distance.Gotoh
    """
    cmp = Gotoh()
    nw = NeedlemanWunsch()

    def test_gotoh_dist_abs(self):
        """Test abydos.distance.Gotoh.dist_abs."""
        self.assertEqual(gotoh('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(self.cmp.dist_abs('GATTACA', 'GCATGCU', 1, 1, _sim_nw), 0)
        self.assertGreaterEqual(
            self.cmp.dist_abs('GATTACA', 'GCATGCU', 1, 0.5, _sim_nw),
            self.nw.dist_abs('GATTACA', 'GCATGCU', 1, _sim_nw),
        )
        self.assertEqual(
            self.cmp.dist_abs('AGACTAGTTAC', 'CGAGACGT', 5, 5, _sim_wikipedia), 16
        )
        self.assertGreaterEqual(
            self.cmp.dist_abs('AGACTAGTTAC', 'CGAGACGT', 5, 2, _sim_wikipedia),
            self.nw.dist_abs('AGACTAGTTAC', 'CGAGACGT', 5, _sim_wikipedia),
        )

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        self.assertEqual(self.cmp.dist_abs('CGATATCAG', 'TGACGSTGC', 5, 5, _sim_nw), -5)
        self.assertGreaterEqual(
            self.cmp.dist_abs('CGATATCAG', 'TGACGSTGC', 5, 2, _sim_nw),
            self.nw.dist_abs('CGATATCAG', 'TGACGSTGC', 5, _sim_nw),
        )
        self.assertEqual(gotoh('AGACTAGTTAC', 'TGACGSTGC', 5, 5, _sim_nw), -7)
        self.assertGreaterEqual(
            self.cmp.dist_abs('AGACTAGTTAC', 'TGACGSTGC', 5, 2, _sim_nw),
            self.nw.dist_abs('AGACTAGTTAC', 'TGACGSTGC', 5, _sim_nw),
        )
        self.assertEqual(self.cmp.dist_abs('AGACTAGTTAC', 'CGAGACGT', 5, 5, _sim_nw), -15)
        self.assertGreaterEqual(
            self.cmp.dist_abs('AGACTAGTTAC', 'CGAGACGT', 5, 2, _sim_nw),
            self.nw.dist_abs('AGACTAGTTAC', 'CGAGACGT', 5, _sim_nw),
        )

        # Test wrapper
        self.assertEqual(
            gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 5, _sim_wikipedia), 16
        )

    def test_gotoh_dist_abs_nialls(self):
        """Test abydos.distance._seqalign.gotoh (Nialls set)."""
        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=2, skew=2)
        nw_vals = (5, 0, -2, 3, 1, 1, -2, -2, -1, -3, -3, -5, -3, -7, -7, -19)
        for i in range(len(NIALL)):
            self.assertEqual(
                self.cmp.dist_abs(NIALL[0], NIALL[i], 2, 2, _sim_nw), nw_vals[i]
            )
        nw_vals2 = (5, 0, -2, 3, 1, 1, -2, -2, -1, -2, -3, -3, -2, -6, -6, -8)
        for i in range(len(NIALL)):
            self.assertEqual(
                self.cmp.dist_abs(NIALL[0], NIALL[i], 2, 1, _sim_nw), nw_vals2[i]
            )
            self.assertGreaterEqual(
                self.cmp.dist_abs(NIALL[0], NIALL[i], 2, 0.5, _sim_nw),
                self.nw.dist_abs(NIALL[0], NIALL[i], 2, _sim_nw),
            )


if __name__ == '__main__':
    unittest.main()
