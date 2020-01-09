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

"""abydos.tests.distance.test_distance_needleman_wunsch.

This module contains unit tests for abydos.distance.NeedlemanWunsch
"""

import unittest

from abydos.distance import NeedlemanWunsch, needleman_wunsch

from six.moves import range

from .. import NIALL


def _sim_wikipedia(src, tar):
    """Return a similarity score for two DNA base pairs.

    Values copied from:
    https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm

    Parameters
    ----------
    src : str
        Source string for comparison
        tar : str
        Target string for comparison

    Returns
    -------
    int: similarity of two DNA base pairs

    """
    nw_matrix = {
        ('A', 'A'): 10,
        ('G', 'G'): 7,
        ('C', 'C'): 9,
        ('T', 'T'): 8,
        ('A', 'G'): -1,
        ('A', 'C'): -3,
        ('A', 'T'): -4,
        ('G', 'C'): -5,
        ('G', 'T'): -3,
        ('C', 'T'): 0,
    }
    return NeedlemanWunsch.sim_matrix(
        src, tar, nw_matrix, symmetric=True, alphabet='CGAT'
    )


def _sim_nw(src, tar):
    """Return 1 if src is tar, otherwise -1.

    Parameters
    ----------
    src : str
        Source string for comparison
        tar : str
        Target string for comparison

    Returns
    -------
    int: nw similarity

    """
    return 2 * int(src is tar) - 1


class MatrixSimTestCases(unittest.TestCase):
    """Test matrix similarity functions.

    abydos.distance.NeedlemanWunsch.sim_matrix
    """

    def test_sim_matrix(self):
        """Test abydos.distance.NeedlemanWunsch.sim_matrix."""
        self.assertEqual(NeedlemanWunsch.sim_matrix('', ''), 1)
        self.assertEqual(NeedlemanWunsch.sim_matrix('', 'a'), 0)
        self.assertEqual(NeedlemanWunsch.sim_matrix('a', ''), 0)
        self.assertEqual(NeedlemanWunsch.sim_matrix('a', 'a'), 1)
        self.assertEqual(NeedlemanWunsch.sim_matrix('abcd', 'abcd'), 1)
        self.assertEqual(NeedlemanWunsch.sim_matrix('abcd', 'dcba'), 0)
        self.assertEqual(NeedlemanWunsch.sim_matrix('abc', 'cba'), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(_sim_wikipedia('A', 'C'), -3)
        self.assertEqual(_sim_wikipedia('G', 'G'), 7)
        self.assertEqual(_sim_wikipedia('A', 'A'), 10)
        self.assertEqual(_sim_wikipedia('T', 'A'), -4)
        self.assertEqual(_sim_wikipedia('T', 'C'), 0)
        self.assertEqual(_sim_wikipedia('A', 'G'), -1)
        self.assertEqual(_sim_wikipedia('C', 'T'), 0)

        self.assertRaises(
            ValueError, NeedlemanWunsch.sim_matrix, 'abc', 'cba', alphabet='ab'
        )
        self.assertRaises(
            ValueError, NeedlemanWunsch.sim_matrix, 'abc', 'ba', alphabet='ab'
        )
        self.assertRaises(
            ValueError, NeedlemanWunsch.sim_matrix, 'ab', 'cba', alphabet='ab'
        )


class NeedlemanWunschTestCases(unittest.TestCase):
    """Test Needleman-Wunsch functions.

    abydos.distance.NeedlemanWunsch
    """

    def test_needleman_wunsch_sim_score(self):
        """Test abydos.distance.NeedlemanWunsch.sim_score."""
        self.assertEqual(NeedlemanWunsch().sim_score('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(
            NeedlemanWunsch(1, _sim_nw).sim_score('GATTACA', 'GCATGCU'), 0
        )
        self.assertEqual(
            NeedlemanWunsch(5, _sim_wikipedia).sim_score(
                'AGACTAGTTAC', 'CGAGACGT'
            ),
            16,
        )

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        nw5 = NeedlemanWunsch(5, _sim_nw)
        self.assertEqual(nw5.sim_score('CGATATCAG', 'TGACGSTGC'), -5)
        self.assertEqual(nw5.sim_score('AGACTAGTTAC', 'TGACGSTGC'), -7)
        self.assertEqual(nw5.sim_score('AGACTAGTTAC', 'CGAGACGT'), -15)

        # test wrapper
        self.assertEqual(
            needleman_wunsch('AGACTAGTTAC', 'CGAGACGT', 5, _sim_nw), -15
        )

    def test_needleman_wunsch_dist_abs_nialls(self):
        """Test abydos.distance.NeedlemanWunsch.dist_abs (Nialls set)."""
        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=2, skew=2)
        nw_vals = (5, 0, -2, 3, 1, 1, -2, -2, -1, -3, -3, -5, -3, -7, -7, -19)
        nw2 = NeedlemanWunsch(2, _sim_nw)
        for i in range(len(NIALL)):
            self.assertEqual(nw2.sim_score(NIALL[0], NIALL[i]), nw_vals[i])

    def test_needleman_wunsch_sim(self):
        """Test abydos.distance.NeedlemanWunsch.sim."""
        self.assertEqual(NeedlemanWunsch().sim('', ''), 1.0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(
            NeedlemanWunsch(1, _sim_nw).sim('GATTACA', 'GCATGCU'), 0
        )
        self.assertEqual(
            NeedlemanWunsch(5, _sim_wikipedia).sim('AGACTAGTTAC', 'CGAGACGT'),
            0.19950186722152657,
        )

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        nw5 = NeedlemanWunsch(5, _sim_nw)
        self.assertEqual(nw5.sim('CGATATCAG', 'TGACGSTGC'), 0)
        self.assertEqual(nw5.sim('AGACTAGTTAC', 'TGACGSTGC'), 0)
        self.assertEqual(nw5.sim('AGACTAGTTAC', 'CGAGACGT'), 0)


if __name__ == '__main__':
    unittest.main()
