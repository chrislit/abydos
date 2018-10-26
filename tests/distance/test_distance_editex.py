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

"""abydos.tests.distance.test_distance_editex.

This module contains unit tests for abydos.distance.editex
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance.editex import dist_editex, editex, sim_editex


class EditexTestCases(unittest.TestCase):
    """Test Editex functions.

    abydos.distance.editex, .sim_editex & .dist_editex
    """

    def test_editex(self):
        """Test abydos.distance.editex.editex."""
        self.assertEqual(editex('', ''), 0)
        self.assertEqual(editex('nelson', ''), 12)
        self.assertEqual(editex('', 'neilsen'), 14)
        self.assertEqual(editex('ab', 'a'), 2)
        self.assertEqual(editex('ab', 'c'), 4)
        self.assertEqual(editex('nelson', 'neilsen'), 2)
        self.assertEqual(editex('neilsen', 'nelson'), 2)
        self.assertEqual(editex('niall', 'neal'), 1)
        self.assertEqual(editex('neal', 'niall'), 1)
        self.assertEqual(editex('niall', 'nihal'), 2)
        self.assertEqual(editex('nihal', 'niall'), 2)
        self.assertEqual(editex('neal', 'nihl'), 3)
        self.assertEqual(editex('nihl', 'neal'), 3)

    def test_editex_local(self):
        """Test abydos.distance.editex.editex (local variant)."""
        self.assertEqual(editex('', '', local=True), 0)
        self.assertEqual(editex('nelson', '', local=True), 12)
        self.assertEqual(editex('', 'neilsen', local=True), 14)
        self.assertEqual(editex('ab', 'a', local=True), 2)
        self.assertEqual(editex('ab', 'c', local=True), 2)
        self.assertEqual(editex('nelson', 'neilsen', local=True), 2)
        self.assertEqual(editex('neilsen', 'nelson', local=True), 2)
        self.assertEqual(editex('niall', 'neal', local=True), 1)
        self.assertEqual(editex('neal', 'niall', local=True), 1)
        self.assertEqual(editex('niall', 'nihal', local=True), 2)
        self.assertEqual(editex('nihal', 'niall', local=True), 2)
        self.assertEqual(editex('neal', 'nihl', local=True), 3)
        self.assertEqual(editex('nihl', 'neal', local=True), 3)

    def test_sim_editex(self):
        """Test abydos.distance.editex.sim_editex."""
        self.assertEqual(sim_editex('', ''), 1)
        self.assertEqual(sim_editex('nelson', ''), 0)
        self.assertEqual(sim_editex('', 'neilsen'), 0)
        self.assertEqual(sim_editex('ab', 'a'), 0.5)
        self.assertEqual(sim_editex('ab', 'c'), 0)
        self.assertAlmostEqual(sim_editex('nelson', 'neilsen'), 12 / 14)
        self.assertAlmostEqual(sim_editex('neilsen', 'nelson'), 12 / 14)
        self.assertEqual(sim_editex('niall', 'neal'), 0.9)

    def test_dist_editex(self):
        """Test abydos.distance.editex.dist_editex."""
        self.assertEqual(dist_editex('', ''), 0)
        self.assertEqual(dist_editex('nelson', ''), 1)
        self.assertEqual(dist_editex('', 'neilsen'), 1)
        self.assertEqual(dist_editex('ab', 'a'), 0.5)
        self.assertEqual(dist_editex('ab', 'c'), 1)
        self.assertAlmostEqual(dist_editex('nelson', 'neilsen'), 2 / 14)
        self.assertAlmostEqual(dist_editex('neilsen', 'nelson'), 2 / 14)
        self.assertEqual(dist_editex('niall', 'neal'), 0.1)


if __name__ == '__main__':
    unittest.main()
