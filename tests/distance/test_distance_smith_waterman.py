# -*- coding: utf-8 -*-

# Copyright 2014-2020 by Christopher C. Little.
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

import unittest

from abydos.distance import SmithWaterman, smith_waterman

from six.moves import range

from .test_distance_needleman_wunsch import _sim_nw, _sim_wikipedia
from .. import NIALL


class SmithWatermanTestCases(unittest.TestCase):
    """Test Smith-Waterman functions.

    abydos.distance.SmithWaterman
    """

    def test_smith_waterman_sim_score(self):
        """Test abydos.distance.SmithWaterman.sim_score."""
        self.assertEqual(SmithWaterman().sim_score('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(
            SmithWaterman(1, _sim_nw).sim_score('GATTACA', 'GCATGCU'), 0
        )
        self.assertEqual(
            SmithWaterman(5, _sim_wikipedia).sim_score(
                'AGACTAGTTAC', 'CGAGACGT'
            ),
            26,
        )

        sw5 = SmithWaterman(5, _sim_nw)
        self.assertEqual(sw5.sim_score('CGATATCAG', 'TGACGSTGC'), 0)
        self.assertEqual(sw5.sim_score('AGACTAGTTAC', 'TGACGSTGC'), 1)
        self.assertEqual(sw5.sim_score('AGACTAGTTAC', 'CGAGACGT'), 0)

        # Test wrapper
        self.assertEqual(
            smith_waterman('AGACTAGTTAC', 'CGAGACGT', 5, _sim_wikipedia), 26
        )

    def test_smith_waterman_sim_score_nialls(self):
        """Test abydos.distance.SmithWaterman.sim_score (Nialls set)."""
        sw_vals = (5, 1, 1, 3, 2, 1, 1, 0, 0, 1, 1, 2, 2, 1, 0, 0)
        sw2 = SmithWaterman(2, _sim_nw)
        for i in range(len(NIALL)):
            self.assertEqual(sw2.sim_score(NIALL[0], NIALL[i]), sw_vals[i])

    def test_smith_waterman_sim(self):
        """Test abydos.distance.SmithWaterman.sim."""
        self.assertEqual(SmithWaterman().sim('', ''), 1.0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(
            SmithWaterman(1, _sim_nw).sim('GATTACA', 'GCATGCU'), 0
        )
        self.assertEqual(
            SmithWaterman(5, _sim_wikipedia).sim('AGACTAGTTAC', 'CGAGACGT'),
            0.3241905342349807,
        )

        sw5 = SmithWaterman(5, _sim_nw)
        self.assertEqual(sw5.sim('CGATATCAG', 'TGACGSTGC'), 0)
        self.assertEqual(
            sw5.sim('AGACTAGTTAC', 'TGACGSTGC'), 0.10050378152592121
        )
        self.assertEqual(sw5.sim('AGACTAGTTAC', 'CGAGACGT'), 0)


if __name__ == '__main__':
    unittest.main()
