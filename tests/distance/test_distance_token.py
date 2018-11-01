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

"""abydos.tests.distance.test_distance_token.

This module contains unit tests for abydos.distance._token
"""

from __future__ import division, unicode_literals

import math
import unittest

from abydos.distance import (
    bag,
    dist_bag,
    dist_cosine,
    dist_dice,
    dist_jaccard,
    dist_monge_elkan,
    dist_overlap,
    dist_tversky,
    sim_bag,
    sim_cosine,
    sim_dice,
    sim_jaccard,
    sim_monge_elkan,
    sim_overlap,
    sim_tversky,
    tanimoto,
)
from abydos.tokenizer import QGrams

from .. import NONQ_FROM, NONQ_TO


class TverskyIndexTestCases(unittest.TestCase):
    """Test Tversky functions.

    abydos.distance._token.sim_tversky & .dist_tversky
    """

    def test_sim_tversky(self):
        """Test abydos.distance._token.sim_tversky."""
        self.assertEqual(sim_tversky('', ''), 1)
        self.assertEqual(sim_tversky('nelson', ''), 0)
        self.assertEqual(sim_tversky('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_tversky('nelson', 'neilsen'), 4 / 11)

        self.assertEqual(sim_tversky('', '', 2), 1)
        self.assertEqual(sim_tversky('nelson', '', 2), 0)
        self.assertEqual(sim_tversky('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_tversky('nelson', 'neilsen', 2), 4 / 11)

        # test valid alpha & beta
        self.assertRaises(ValueError, sim_tversky, 'abcd', 'dcba', 2, -1, -1)
        self.assertRaises(ValueError, sim_tversky, 'abcd', 'dcba', 2, -1, 0)
        self.assertRaises(ValueError, sim_tversky, 'abcd', 'dcba', 2, 0, -1)

        # test empty QGrams
        self.assertAlmostEqual(sim_tversky('nelson', 'neilsen', 7), 0.0)

        # test unequal alpha & beta
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 2, 1), 3 / 11)
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 1, 2), 3 / 10)
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 2, 2), 3 / 13)

        # test bias parameter
        self.assertAlmostEqual(
            sim_tversky('niall', 'neal', 2, 1, 1, 0.5), 7 / 11
        )
        self.assertAlmostEqual(
            sim_tversky('niall', 'neal', 2, 2, 1, 0.5), 7 / 9
        )
        self.assertAlmostEqual(
            sim_tversky('niall', 'neal', 2, 1, 2, 0.5), 7 / 15
        )
        self.assertAlmostEqual(
            sim_tversky('niall', 'neal', 2, 2, 2, 0.5), 7 / 11
        )

        # supplied q-gram tests
        self.assertEqual(sim_tversky(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_tversky(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_tversky(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(
            sim_tversky(QGrams('nelson'), QGrams('neilsen')), 4 / 11
        )

        # non-q-gram tests
        self.assertEqual(sim_tversky('', '', 0), 1)
        self.assertEqual(sim_tversky('the quick', '', 0), 0)
        self.assertEqual(sim_tversky('', 'the quick', 0), 0)
        self.assertAlmostEqual(sim_tversky(NONQ_FROM, NONQ_TO, 0), 1 / 3)
        self.assertAlmostEqual(sim_tversky(NONQ_TO, NONQ_FROM, 0), 1 / 3)

    def test_dist_tversky(self):
        """Test abydos.distance._token.dist_tversky."""
        self.assertEqual(dist_tversky('', ''), 0)
        self.assertEqual(dist_tversky('nelson', ''), 1)
        self.assertEqual(dist_tversky('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen'), 7 / 11)

        self.assertEqual(dist_tversky('', '', 2), 0)
        self.assertEqual(dist_tversky('nelson', '', 2), 1)
        self.assertEqual(dist_tversky('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen', 2), 7 / 11)

        # test valid alpha & beta
        self.assertRaises(ValueError, dist_tversky, 'abcd', 'dcba', 2, -1, -1)
        self.assertRaises(ValueError, dist_tversky, 'abcd', 'dcba', 2, -1, 0)
        self.assertRaises(ValueError, dist_tversky, 'abcd', 'dcba', 2, 0, -1)

        # test empty QGrams
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen', 7), 1.0)

        # test unequal alpha & beta
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 2, 1), 8 / 11)
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 1, 2), 7 / 10)
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 2, 2), 10 / 13)

        # test bias parameter
        self.assertAlmostEqual(
            dist_tversky('niall', 'neal', 2, 1, 1, 0.5), 4 / 11
        )
        self.assertAlmostEqual(
            dist_tversky('niall', 'neal', 2, 2, 1, 0.5), 2 / 9
        )
        self.assertAlmostEqual(
            dist_tversky('niall', 'neal', 2, 1, 2, 0.5), 8 / 15
        )
        self.assertAlmostEqual(
            dist_tversky('niall', 'neal', 2, 2, 2, 0.5), 4 / 11
        )

        # supplied q-gram tests
        self.assertEqual(dist_tversky(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_tversky(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_tversky(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            dist_tversky(QGrams('nelson'), QGrams('neilsen')), 7 / 11
        )

        # non-q-gram tests
        self.assertEqual(dist_tversky('', '', 0), 0)
        self.assertEqual(dist_tversky('the quick', '', 0), 1)
        self.assertEqual(dist_tversky('', 'the quick', 0), 1)
        self.assertAlmostEqual(dist_tversky(NONQ_FROM, NONQ_TO, 0), 2 / 3)
        self.assertAlmostEqual(dist_tversky(NONQ_TO, NONQ_FROM, 0), 2 / 3)


class DiceTestCases(unittest.TestCase):
    """Test Dice functions.

    abydos.distance.token.sim_dice & .dist_dice
    """

    def test_sim_dice(self):
        """Test abydos.distance._token.sim_dice."""
        self.assertEqual(sim_dice('', ''), 1)
        self.assertEqual(sim_dice('nelson', ''), 0)
        self.assertEqual(sim_dice('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_dice('nelson', 'neilsen'), 8 / 15)

        self.assertEqual(sim_dice('', '', 2), 1)
        self.assertEqual(sim_dice('nelson', '', 2), 0)
        self.assertEqual(sim_dice('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_dice('nelson', 'neilsen', 2), 8 / 15)

        # supplied q-gram tests
        self.assertEqual(sim_dice(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_dice(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_dice(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(
            sim_dice(QGrams('nelson'), QGrams('neilsen')), 8 / 15
        )

        # non-q-gram tests
        self.assertEqual(sim_dice('', '', 0), 1)
        self.assertEqual(sim_dice('the quick', '', 0), 0)
        self.assertEqual(sim_dice('', 'the quick', 0), 0)
        self.assertAlmostEqual(sim_dice(NONQ_FROM, NONQ_TO, 0), 1 / 2)
        self.assertAlmostEqual(sim_dice(NONQ_TO, NONQ_FROM, 0), 1 / 2)

    def test_dist_dice(self):
        """Test abydos.distance._token.dist_dice."""
        self.assertEqual(dist_dice('', ''), 0)
        self.assertEqual(dist_dice('nelson', ''), 1)
        self.assertEqual(dist_dice('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_dice('nelson', 'neilsen'), 7 / 15)

        self.assertEqual(dist_dice('', '', 2), 0)
        self.assertEqual(dist_dice('nelson', '', 2), 1)
        self.assertEqual(dist_dice('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_dice('nelson', 'neilsen', 2), 7 / 15)

        # supplied q-gram tests
        self.assertEqual(dist_dice(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_dice(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_dice(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            dist_dice(QGrams('nelson'), QGrams('neilsen')), 7 / 15
        )

        # non-q-gram tests
        self.assertEqual(dist_dice('', '', 0), 0)
        self.assertEqual(dist_dice('the quick', '', 0), 1)
        self.assertEqual(dist_dice('', 'the quick', 0), 1)
        self.assertAlmostEqual(dist_dice(NONQ_FROM, NONQ_TO, 0), 1 / 2)
        self.assertAlmostEqual(dist_dice(NONQ_TO, NONQ_FROM, 0), 1 / 2)


class JaccardTestCases(unittest.TestCase):
    """Test Jaccard functions.

    abydos.distance._token.sim_jaccard & .dist_jaccard
    """

    def test_sim_jaccard(self):
        """Test abydos.distance._token.sim_jaccard."""
        self.assertEqual(sim_jaccard('', ''), 1)
        self.assertEqual(sim_jaccard('nelson', ''), 0)
        self.assertEqual(sim_jaccard('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_jaccard('nelson', 'neilsen'), 4 / 11)

        self.assertEqual(sim_jaccard('', '', 2), 1)
        self.assertEqual(sim_jaccard('nelson', '', 2), 0)
        self.assertEqual(sim_jaccard('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_jaccard('nelson', 'neilsen', 2), 4 / 11)

        # supplied q-gram tests
        self.assertEqual(sim_jaccard(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_jaccard(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_jaccard(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(
            sim_jaccard(QGrams('nelson'), QGrams('neilsen')), 4 / 11
        )

        # non-q-gram tests
        self.assertEqual(sim_jaccard('', '', 0), 1)
        self.assertEqual(sim_jaccard('the quick', '', 0), 0)
        self.assertEqual(sim_jaccard('', 'the quick', 0), 0)
        self.assertAlmostEqual(sim_jaccard(NONQ_FROM, NONQ_TO, 0), 1 / 3)
        self.assertAlmostEqual(sim_jaccard(NONQ_TO, NONQ_FROM, 0), 1 / 3)

    def test_dist_jaccard(self):
        """Test abydos.distance._token.dist_jaccard."""
        self.assertEqual(dist_jaccard('', ''), 0)
        self.assertEqual(dist_jaccard('nelson', ''), 1)
        self.assertEqual(dist_jaccard('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_jaccard('nelson', 'neilsen'), 7 / 11)

        self.assertEqual(dist_jaccard('', '', 2), 0)
        self.assertEqual(dist_jaccard('nelson', '', 2), 1)
        self.assertEqual(dist_jaccard('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_jaccard('nelson', 'neilsen', 2), 7 / 11)

        # supplied q-gram tests
        self.assertEqual(dist_jaccard(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_jaccard(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_jaccard(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            dist_jaccard(QGrams('nelson'), QGrams('neilsen')), 7 / 11
        )

        # non-q-gram tests
        self.assertEqual(dist_jaccard('', '', 0), 0)
        self.assertEqual(dist_jaccard('the quick', '', 0), 1)
        self.assertEqual(dist_jaccard('', 'the quick', 0), 1)
        self.assertAlmostEqual(dist_jaccard(NONQ_FROM, NONQ_TO, 0), 2 / 3)
        self.assertAlmostEqual(dist_jaccard(NONQ_TO, NONQ_FROM, 0), 2 / 3)


class OverlapTestCases(unittest.TestCase):
    """Test overlap functions.

    abydos.distance._token.sim_overlap & .dist_overlap
    """

    def test_sim_overlap(self):
        """Test abydos.distance._token.sim_overlap."""
        self.assertEqual(sim_overlap('', ''), 1)
        self.assertEqual(sim_overlap('nelson', ''), 0)
        self.assertEqual(sim_overlap('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_overlap('nelson', 'neilsen'), 4 / 7)

        self.assertEqual(sim_overlap('', '', 2), 1)
        self.assertEqual(sim_overlap('nelson', '', 2), 0)
        self.assertEqual(sim_overlap('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_overlap('nelson', 'neilsen', 2), 4 / 7)

        # supplied q-gram tests
        self.assertEqual(sim_overlap(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_overlap(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_overlap(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(
            sim_overlap(QGrams('nelson'), QGrams('neilsen')), 4 / 7
        )

        # non-q-gram tests
        self.assertEqual(sim_overlap('', '', 0), 1)
        self.assertEqual(sim_overlap('the quick', '', 0), 0)
        self.assertEqual(sim_overlap('', 'the quick', 0), 0)
        self.assertAlmostEqual(sim_overlap(NONQ_FROM, NONQ_TO, 0), 4 / 7)
        self.assertAlmostEqual(sim_overlap(NONQ_TO, NONQ_FROM, 0), 4 / 7)

    def test_dist_overlap(self):
        """Test abydos.distance._token.dist_overlap."""
        self.assertEqual(dist_overlap('', ''), 0)
        self.assertEqual(dist_overlap('nelson', ''), 1)
        self.assertEqual(dist_overlap('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_overlap('nelson', 'neilsen'), 3 / 7)

        self.assertEqual(dist_overlap('', '', 2), 0)
        self.assertEqual(dist_overlap('nelson', '', 2), 1)
        self.assertEqual(dist_overlap('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_overlap('nelson', 'neilsen', 2), 3 / 7)

        # supplied q-gram tests
        self.assertEqual(dist_overlap(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_overlap(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_overlap(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            dist_overlap(QGrams('nelson'), QGrams('neilsen')), 3 / 7
        )

        # non-q-gram tests
        self.assertEqual(dist_overlap('', '', 0), 0)
        self.assertEqual(dist_overlap('the quick', '', 0), 1)
        self.assertEqual(dist_overlap('', 'the quick', 0), 1)
        self.assertAlmostEqual(dist_overlap(NONQ_FROM, NONQ_TO, 0), 3 / 7)
        self.assertAlmostEqual(dist_overlap(NONQ_TO, NONQ_FROM, 0), 3 / 7)


class TanimotoTestCases(unittest.TestCase):
    """Test Tanimoto functions.

    abydos.distance._token.tanimoto
    """

    def test_tanimoto(self):
        """Test abydos.distance._token.tanimoto."""
        self.assertEqual(tanimoto('', ''), 0)
        self.assertEqual(tanimoto('nelson', ''), float('-inf'))
        self.assertEqual(tanimoto('', 'neilsen'), float('-inf'))
        self.assertAlmostEqual(
            tanimoto('nelson', 'neilsen'), math.log(4 / 11, 2)
        )

        self.assertEqual(tanimoto('', '', 2), 0)
        self.assertEqual(tanimoto('nelson', '', 2), float('-inf'))
        self.assertEqual(tanimoto('', 'neilsen', 2), float('-inf'))
        self.assertAlmostEqual(
            tanimoto('nelson', 'neilsen', 2), math.log(4 / 11, 2)
        )

        # supplied q-gram tests
        self.assertEqual(tanimoto(QGrams(''), QGrams('')), 0)
        self.assertEqual(tanimoto(QGrams('nelson'), QGrams('')), float('-inf'))
        self.assertEqual(
            tanimoto(QGrams(''), QGrams('neilsen')), float('-inf')
        )
        self.assertAlmostEqual(
            tanimoto(QGrams('nelson'), QGrams('neilsen')), math.log(4 / 11, 2)
        )

        # non-q-gram tests
        self.assertEqual(tanimoto('', '', 0), 0)
        self.assertEqual(tanimoto('the quick', '', 0), float('-inf'))
        self.assertEqual(tanimoto('', 'the quick', 0), float('-inf'))
        self.assertAlmostEqual(
            tanimoto(NONQ_FROM, NONQ_TO, 0), math.log(1 / 3, 2)
        )
        self.assertAlmostEqual(
            tanimoto(NONQ_TO, NONQ_FROM, 0), math.log(1 / 3, 2)
        )


class CosineSimilarityTestCases(unittest.TestCase):
    """Test cosine similarity functions.

    abydos.distance._token.sim_cosine & .dist_cosine
    """

    def test_sim_cosine(self):
        """Test abydos.distance._token.sim_cosine."""
        self.assertEqual(sim_cosine('', ''), 1)
        self.assertEqual(sim_cosine('nelson', ''), 0)
        self.assertEqual(sim_cosine('', 'neilsen'), 0)
        self.assertAlmostEqual(
            sim_cosine('nelson', 'neilsen'), 4 / math.sqrt(7 * 8)
        )

        self.assertEqual(sim_cosine('', '', 2), 1)
        self.assertEqual(sim_cosine('nelson', '', 2), 0)
        self.assertEqual(sim_cosine('', 'neilsen', 2), 0)
        self.assertAlmostEqual(
            sim_cosine('nelson', 'neilsen', 2), 4 / math.sqrt(7 * 8)
        )

        # supplied q-gram tests
        self.assertEqual(sim_cosine(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_cosine(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_cosine(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(
            sim_cosine(QGrams('nelson'), QGrams('neilsen')),
            4 / math.sqrt(7 * 8),
        )

        # non-q-gram tests
        self.assertEqual(sim_cosine('', '', 0), 1)
        self.assertEqual(sim_cosine('the quick', '', 0), 0)
        self.assertEqual(sim_cosine('', 'the quick', 0), 0)
        self.assertAlmostEqual(
            sim_cosine(NONQ_FROM, NONQ_TO, 0), 4 / math.sqrt(9 * 7)
        )
        self.assertAlmostEqual(
            sim_cosine(NONQ_TO, NONQ_FROM, 0), 4 / math.sqrt(9 * 7)
        )

    def test_dist_cosine(self):
        """Test abydos.distance._token.dist_cosine."""
        self.assertEqual(dist_cosine('', ''), 0)
        self.assertEqual(dist_cosine('nelson', ''), 1)
        self.assertEqual(dist_cosine('', 'neilsen'), 1)
        self.assertAlmostEqual(
            dist_cosine('nelson', 'neilsen'), 1 - (4 / math.sqrt(7 * 8))
        )

        self.assertEqual(dist_cosine('', '', 2), 0)
        self.assertEqual(dist_cosine('nelson', '', 2), 1)
        self.assertEqual(dist_cosine('', 'neilsen', 2), 1)
        self.assertAlmostEqual(
            dist_cosine('nelson', 'neilsen', 2), 1 - (4 / math.sqrt(7 * 8))
        )

        # supplied q-gram tests
        self.assertEqual(dist_cosine(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_cosine(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_cosine(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(
            dist_cosine(QGrams('nelson'), QGrams('neilsen')),
            1 - (4 / math.sqrt(7 * 8)),
        )

        # non-q-gram tests
        self.assertEqual(dist_cosine('', '', 0), 0)
        self.assertEqual(dist_cosine('the quick', '', 0), 1)
        self.assertEqual(dist_cosine('', 'the quick', 0), 1)
        self.assertAlmostEqual(
            dist_cosine(NONQ_FROM, NONQ_TO, 0), 1 - 4 / math.sqrt(9 * 7)
        )
        self.assertAlmostEqual(
            dist_cosine(NONQ_TO, NONQ_FROM, 0), 1 - 4 / math.sqrt(9 * 7)
        )


class MongeElkanTestCases(unittest.TestCase):
    """Test Monge-Elkan functions.

    abydos.distance._token.sim_monge_elkan & .dist_monge_elkan
    """

    def test_sim_monge_elkan(self):
        """Test abydos.distance._token.sim_monge_elkan."""
        self.assertEqual(sim_monge_elkan('', ''), 1)
        self.assertEqual(sim_monge_elkan('', 'a'), 0)
        self.assertEqual(sim_monge_elkan('a', 'a'), 1)

        self.assertEqual(sim_monge_elkan('Niall', 'Neal'), 3 / 4)
        self.assertEqual(sim_monge_elkan('Niall', 'Njall'), 5 / 6)
        self.assertEqual(sim_monge_elkan('Niall', 'Niel'), 3 / 4)
        self.assertEqual(sim_monge_elkan('Niall', 'Nigel'), 3 / 4)

        self.assertEqual(
            sim_monge_elkan('Niall', 'Neal', symmetric=True), 31 / 40
        )
        self.assertEqual(
            sim_monge_elkan('Niall', 'Njall', symmetric=True), 5 / 6
        )
        self.assertEqual(
            sim_monge_elkan('Niall', 'Niel', symmetric=True), 31 / 40
        )
        self.assertAlmostEqual(
            sim_monge_elkan('Niall', 'Nigel', symmetric=True), 17 / 24
        )

    def test_dist_monge_elkan(self):
        """Test abydos.distance._token.dist_monge_elkan."""
        self.assertEqual(dist_monge_elkan('', ''), 0)
        self.assertEqual(dist_monge_elkan('', 'a'), 1)

        self.assertEqual(dist_monge_elkan('Niall', 'Neal'), 1 / 4)
        self.assertAlmostEqual(dist_monge_elkan('Niall', 'Njall'), 1 / 6)
        self.assertEqual(dist_monge_elkan('Niall', 'Niel'), 1 / 4)
        self.assertEqual(dist_monge_elkan('Niall', 'Nigel'), 1 / 4)

        self.assertAlmostEqual(
            dist_monge_elkan('Niall', 'Neal', symmetric=True), 9 / 40
        )
        self.assertAlmostEqual(
            dist_monge_elkan('Niall', 'Njall', symmetric=True), 1 / 6
        )
        self.assertAlmostEqual(
            dist_monge_elkan('Niall', 'Niel', symmetric=True), 9 / 40
        )
        self.assertAlmostEqual(
            dist_monge_elkan('Niall', 'Nigel', symmetric=True), 7 / 24
        )


class BagTestCases(unittest.TestCase):
    """Test bag similarity functions.

    abydos.distance._token.bag, .sim_bag & .dist_bag
    """

    def test_bag(self):
        """Test abydos.distance._token.bag."""
        self.assertEqual(bag('', ''), 0)
        self.assertEqual(bag('nelson', ''), 6)
        self.assertEqual(bag('', 'neilsen'), 7)
        self.assertEqual(bag('ab', 'a'), 1)
        self.assertEqual(bag('ab', 'c'), 2)
        self.assertEqual(bag('nelson', 'neilsen'), 2)
        self.assertEqual(bag('neilsen', 'nelson'), 2)
        self.assertEqual(bag('niall', 'neal'), 2)
        self.assertEqual(bag('aluminum', 'Catalan'), 5)
        self.assertEqual(bag('abcdefg', 'hijklm'), 7)
        self.assertEqual(bag('abcdefg', 'hijklmno'), 8)

    def test_sim_bag(self):
        """Test abydos.distance._token.sim_bag."""
        self.assertEqual(sim_bag('', ''), 1)
        self.assertEqual(sim_bag('nelson', ''), 0)
        self.assertEqual(sim_bag('', 'neilsen'), 0)
        self.assertEqual(sim_bag('ab', 'a'), 0.5)
        self.assertEqual(sim_bag('ab', 'c'), 0)
        self.assertAlmostEqual(sim_bag('nelson', 'neilsen'), 5 / 7)
        self.assertAlmostEqual(sim_bag('neilsen', 'nelson'), 5 / 7)
        self.assertAlmostEqual(sim_bag('niall', 'neal'), 3 / 5)
        self.assertAlmostEqual(sim_bag('aluminum', 'Catalan'), 3 / 8)
        self.assertEqual(sim_bag('abcdefg', 'hijklm'), 0)
        self.assertEqual(sim_bag('abcdefg', 'hijklmno'), 0)

    def test_dist_bag(self):
        """Test abydos.distance._token.dist_bag."""
        self.assertEqual(dist_bag('', ''), 0)
        self.assertEqual(dist_bag('nelson', ''), 1)
        self.assertEqual(dist_bag('', 'neilsen'), 1)
        self.assertEqual(dist_bag('ab', 'a'), 0.5)
        self.assertEqual(dist_bag('ab', 'c'), 1)
        self.assertAlmostEqual(dist_bag('nelson', 'neilsen'), 2 / 7)
        self.assertAlmostEqual(dist_bag('neilsen', 'nelson'), 2 / 7)
        self.assertAlmostEqual(dist_bag('niall', 'neal'), 2 / 5)
        self.assertAlmostEqual(dist_bag('aluminum', 'Catalan'), 5 / 8)
        self.assertEqual(dist_bag('abcdefg', 'hijklm'), 1)
        self.assertEqual(dist_bag('abcdefg', 'hijklmno'), 1)


if __name__ == '__main__':
    unittest.main()
