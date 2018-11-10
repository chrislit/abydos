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

"""abydos.tests.distance.test_distance_seqalign.

This module contains unit tests for abydos.distance._seqalign
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import (
    NeedlemanWunsch,
    gotoh,
    needleman_wunsch,
    smith_waterman,
)

from six.moves import range

from .. import NIALL


def _sim_wikipedia(src, tar):
    """Return a similarity score for two DNA base pairs.

    Values copied from:
    https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm

    Args:
        src (str): Source string for comparison
        tar (str): Target string for comparison

    Returns:
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

    Args:
        src (str): Source string for comparison
        tar (str): Target string for comparison

    Returns:
        int: nw similarity

    """
    return 2 * int(src is tar) - 1


class MatrixSimTestCases(unittest.TestCase):
    """Test matrix similarity functions.

    abydos.distance._seqalign.sim_matrix
    """

    def test_sim_matrix(self):
        """Test abydos.distance._seqalign.sim_matrix."""
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

    abydos.distance._seqalign.needleman_wunsch
    """

    def test_needleman_wunsch(self):
        """Test abydos.distance._seqalign.needleman_wunsch."""
        self.assertEqual(needleman_wunsch('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(needleman_wunsch('GATTACA', 'GCATGCU', 1, _sim_nw), 0)
        self.assertEqual(
            needleman_wunsch('AGACTAGTTAC', 'CGAGACGT', 5, _sim_wikipedia), 16
        )

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        self.assertEqual(
            needleman_wunsch('CGATATCAG', 'TGACGSTGC', 5, _sim_nw), -5
        )
        self.assertEqual(
            needleman_wunsch('AGACTAGTTAC', 'TGACGSTGC', 5, _sim_nw), -7
        )
        self.assertEqual(
            needleman_wunsch('AGACTAGTTAC', 'CGAGACGT', 5, _sim_nw), -15
        )

    def test_needleman_wunsch_nialls(self):
        """Test abydos.distance._seqalign.needleman_wunsch (Nialls set)."""
        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=2, skew=2)
        nw_vals = (5, 0, -2, 3, 1, 1, -2, -2, -1, -3, -3, -5, -3, -7, -7, -19)
        for i in range(len(NIALL)):
            self.assertEqual(
                needleman_wunsch(NIALL[0], NIALL[i], 2, _sim_nw), nw_vals[i]
            )


class SmithWatermanTestCases(unittest.TestCase):
    """Test Smith-Waterman functions.

    abydos.distance._seqalign.smith_waterman
    """

    def test_smith_waterman(self):
        """Test abydos.distance._seqalign.smith_waterman."""
        self.assertEqual(smith_waterman('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(smith_waterman('GATTACA', 'GCATGCU', 1, _sim_nw), 0)
        self.assertEqual(
            smith_waterman('AGACTAGTTAC', 'CGAGACGT', 5, _sim_wikipedia), 26
        )

        self.assertEqual(
            smith_waterman('CGATATCAG', 'TGACGSTGC', 5, _sim_nw), 0
        )
        self.assertEqual(
            smith_waterman('AGACTAGTTAC', 'TGACGSTGC', 5, _sim_nw), 1
        )
        self.assertEqual(
            smith_waterman('AGACTAGTTAC', 'CGAGACGT', 5, _sim_nw), 0
        )

    def test_smith_waterman_nialls(self):
        """Test abydos.distance._seqalign.smith_waterman (Nialls set)."""
        sw_vals = (5, 1, 1, 3, 2, 1, 1, 0, 0, 1, 1, 2, 2, 1, 0, 0)
        for i in range(len(NIALL)):
            self.assertEqual(
                smith_waterman(NIALL[0], NIALL[i], 2, _sim_nw), sw_vals[i]
            )


class GotohTestCases(unittest.TestCase):
    """Test Gotoh functions.

    abydos.distance._seqalign.gotoh
    """

    def test_gotoh(self):
        """Test abydos.distance._seqalign.gotoh."""
        self.assertEqual(gotoh('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(gotoh('GATTACA', 'GCATGCU', 1, 1, _sim_nw), 0)
        self.assertGreaterEqual(
            gotoh('GATTACA', 'GCATGCU', 1, 0.5, _sim_nw),
            needleman_wunsch('GATTACA', 'GCATGCU', 1, _sim_nw),
        )
        self.assertEqual(
            gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 5, _sim_wikipedia), 16
        )
        self.assertGreaterEqual(
            gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 2, _sim_wikipedia),
            needleman_wunsch('AGACTAGTTAC', 'CGAGACGT', 5, _sim_wikipedia),
        )

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        self.assertEqual(gotoh('CGATATCAG', 'TGACGSTGC', 5, 5, _sim_nw), -5)
        self.assertGreaterEqual(
            gotoh('CGATATCAG', 'TGACGSTGC', 5, 2, _sim_nw),
            needleman_wunsch('CGATATCAG', 'TGACGSTGC', 5, _sim_nw),
        )
        self.assertEqual(gotoh('AGACTAGTTAC', 'TGACGSTGC', 5, 5, _sim_nw), -7)
        self.assertGreaterEqual(
            gotoh('AGACTAGTTAC', 'TGACGSTGC', 5, 2, _sim_nw),
            needleman_wunsch('AGACTAGTTAC', 'TGACGSTGC', 5, _sim_nw),
        )
        self.assertEqual(gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 5, _sim_nw), -15)
        self.assertGreaterEqual(
            gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 2, _sim_nw),
            needleman_wunsch('AGACTAGTTAC', 'CGAGACGT', 5, _sim_nw),
        )

    def test_gotoh_nialls(self):
        """Test abydos.distance._seqalign.gotoh (Nialls set)."""
        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=2, skew=2)
        nw_vals = (5, 0, -2, 3, 1, 1, -2, -2, -1, -3, -3, -5, -3, -7, -7, -19)
        for i in range(len(NIALL)):
            self.assertEqual(
                gotoh(NIALL[0], NIALL[i], 2, 2, _sim_nw), nw_vals[i]
            )
        nw_vals2 = (5, 0, -2, 3, 1, 1, -2, -2, -1, -2, -3, -3, -2, -6, -6, -8)
        for i in range(len(NIALL)):
            self.assertEqual(
                gotoh(NIALL[0], NIALL[i], 2, 1, _sim_nw), nw_vals2[i]
            )
            self.assertGreaterEqual(
                gotoh(NIALL[0], NIALL[i], 2, 0.5, _sim_nw),
                needleman_wunsch(NIALL[0], NIALL[i], 2, _sim_nw),
            )


if __name__ == '__main__':
    unittest.main()
