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

"""abydos.tests.distance.test_distance_basic.

This module contains unit tests for abydos.distance._basic
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance import (
    dist_ident,
    dist_length,
    dist_prefix,
    dist_suffix,
    sim_ident,
    sim_length,
    sim_prefix,
    sim_suffix,
)


class IdentityTestCases(unittest.TestCase):
    """Test identity similarity functions.

    abydos.distance._basic.sim_ident & .dist_ident
    """

    def test_sim_ident(self):
        """Test abydos.distance._basic.sim_ident."""
        self.assertEqual(sim_ident('', ''), 1)
        self.assertEqual(sim_ident('', 'a'), 0)
        self.assertEqual(sim_ident('a', ''), 0)
        self.assertEqual(sim_ident('a', 'a'), 1)
        self.assertEqual(sim_ident('abcd', 'abcd'), 1)
        self.assertEqual(sim_ident('abcd', 'dcba'), 0)
        self.assertEqual(sim_ident('abc', 'cba'), 0)

    def test_dist_ident(self):
        """Test abydos.distance._basic.dist_ident."""
        self.assertEqual(dist_ident('', ''), 0)
        self.assertEqual(dist_ident('', 'a'), 1)
        self.assertEqual(dist_ident('a', ''), 1)
        self.assertEqual(dist_ident('a', 'a'), 0)
        self.assertEqual(dist_ident('abcd', 'abcd'), 0)
        self.assertEqual(dist_ident('abcd', 'dcba'), 1)
        self.assertEqual(dist_ident('abc', 'cba'), 1)


class LengthTestCases(unittest.TestCase):
    """Test length similarity functions.

    abydos.distance._basic.sim_length & .dist_length
    """

    def test_sim_ident(self):
        """Test abydos.distance._basic.sim_length."""
        self.assertEqual(sim_length('', ''), 1)
        self.assertEqual(sim_length('', 'a'), 0)
        self.assertEqual(sim_length('a', ''), 0)
        self.assertEqual(sim_length('a', 'a'), 1)
        self.assertEqual(sim_length('abcd', 'abcd'), 1)
        self.assertEqual(sim_length('abcd', 'dcba'), 1)
        self.assertEqual(sim_length('abc', 'cba'), 1)
        self.assertEqual(sim_length('abc', 'dcba'), 0.75)
        self.assertEqual(sim_length('abcd', 'cba'), 0.75)
        self.assertEqual(sim_length('ab', 'dcba'), 0.5)
        self.assertEqual(sim_length('abcd', 'ba'), 0.5)

    def test_dist_ident(self):
        """Test abydos.distance._basic.dist_length."""
        self.assertEqual(dist_length('', ''), 0)
        self.assertEqual(dist_length('', 'a'), 1)
        self.assertEqual(dist_length('a', ''), 1)
        self.assertEqual(dist_length('a', 'a'), 0)
        self.assertEqual(dist_length('abcd', 'abcd'), 0)
        self.assertEqual(dist_length('abcd', 'dcba'), 0)
        self.assertEqual(dist_length('abc', 'cba'), 0)
        self.assertEqual(dist_length('abc', 'dcba'), 0.25)
        self.assertEqual(dist_length('abcd', 'cba'), 0.25)
        self.assertEqual(dist_length('ab', 'dcba'), 0.5)
        self.assertEqual(dist_length('abcd', 'ba'), 0.5)


class PrefixTestCases(unittest.TestCase):
    """Test prefix similarity functions.

    abydos.distance._basic.sim_prefix & .dist_prefix
    """

    def test_sim_prefix(self):
        """Test abydos.distance._basic.sim_prefix."""
        self.assertEqual(sim_prefix('', ''), 1)
        self.assertEqual(sim_prefix('a', ''), 0)
        self.assertEqual(sim_prefix('', 'a'), 0)
        self.assertEqual(sim_prefix('a', 'a'), 1)
        self.assertEqual(sim_prefix('ax', 'a'), 1)
        self.assertEqual(sim_prefix('axx', 'a'), 1)
        self.assertEqual(sim_prefix('ax', 'ay'), 1 / 2)
        self.assertEqual(sim_prefix('a', 'ay'), 1)
        self.assertEqual(sim_prefix('a', 'ayy'), 1)
        self.assertEqual(sim_prefix('ax', 'ay'), 1 / 2)
        self.assertEqual(sim_prefix('a', 'y'), 0)
        self.assertEqual(sim_prefix('y', 'a'), 0)
        self.assertEqual(sim_prefix('aaax', 'aaa'), 1)
        self.assertAlmostEqual(sim_prefix('axxx', 'aaa'), 1 / 3)
        self.assertEqual(sim_prefix('aaxx', 'aayy'), 1 / 2)
        self.assertEqual(sim_prefix('xxaa', 'yyaa'), 0)
        self.assertAlmostEqual(sim_prefix('aaxxx', 'aay'), 2 / 3)
        self.assertEqual(sim_prefix('aaxxxx', 'aayyy'), 2 / 5)
        self.assertEqual(sim_prefix('xa', 'a'), 0)
        self.assertEqual(sim_prefix('xxa', 'a'), 0)
        self.assertEqual(sim_prefix('xa', 'ya'), 0)
        self.assertEqual(sim_prefix('a', 'ya'), 0)
        self.assertEqual(sim_prefix('a', 'yya'), 0)
        self.assertEqual(sim_prefix('xa', 'ya'), 0)
        self.assertEqual(sim_prefix('xaaa', 'aaa'), 0)
        self.assertEqual(sim_prefix('xxxa', 'aaa'), 0)
        self.assertEqual(sim_prefix('xxxaa', 'yaa'), 0)
        self.assertEqual(sim_prefix('xxxxaa', 'yyyaa'), 0)

    def test_dist_prefix(self):
        """Test abydos.distance._basic.dist_prefix."""
        self.assertEqual(dist_prefix('', ''), 0)
        self.assertEqual(dist_prefix('a', ''), 1)
        self.assertEqual(dist_prefix('', 'a'), 1)
        self.assertEqual(dist_prefix('a', 'a'), 0)
        self.assertEqual(dist_prefix('ax', 'a'), 0)
        self.assertEqual(dist_prefix('axx', 'a'), 0)
        self.assertEqual(dist_prefix('ax', 'ay'), 1 / 2)
        self.assertEqual(dist_prefix('a', 'ay'), 0)
        self.assertEqual(dist_prefix('a', 'ayy'), 0)
        self.assertEqual(dist_prefix('ax', 'ay'), 1 / 2)
        self.assertEqual(dist_prefix('a', 'y'), 1)
        self.assertEqual(dist_prefix('y', 'a'), 1)
        self.assertEqual(dist_prefix('aaax', 'aaa'), 0)
        self.assertAlmostEqual(dist_prefix('axxx', 'aaa'), 2 / 3)
        self.assertEqual(dist_prefix('aaxx', 'aayy'), 1 / 2)
        self.assertEqual(dist_prefix('xxaa', 'yyaa'), 1)
        self.assertAlmostEqual(dist_prefix('aaxxx', 'aay'), 1 / 3)
        self.assertEqual(dist_prefix('aaxxxx', 'aayyy'), 3 / 5)
        self.assertEqual(dist_prefix('xa', 'a'), 1)
        self.assertEqual(dist_prefix('xxa', 'a'), 1)
        self.assertEqual(dist_prefix('xa', 'ya'), 1)
        self.assertEqual(dist_prefix('a', 'ya'), 1)
        self.assertEqual(dist_prefix('a', 'yya'), 1)
        self.assertEqual(dist_prefix('xa', 'ya'), 1)
        self.assertEqual(dist_prefix('xaaa', 'aaa'), 1)
        self.assertEqual(dist_prefix('xxxa', 'aaa'), 1)
        self.assertEqual(dist_prefix('xxxaa', 'yaa'), 1)
        self.assertEqual(dist_prefix('xxxxaa', 'yyyaa'), 1)


class SuffixTestCases(unittest.TestCase):
    """Test suffix similarity functions.

    abydos.distance._basic.sim_suffix & .dist_suffix
    """

    def test_sim_suffix(self):
        """Test abydos.distance._basic.sim_suffix."""
        self.assertEqual(sim_suffix('', ''), 1)
        self.assertEqual(sim_suffix('a', ''), 0)
        self.assertEqual(sim_suffix('', 'a'), 0)
        self.assertEqual(sim_suffix('a', 'a'), 1)
        self.assertEqual(sim_suffix('ax', 'a'), 0)
        self.assertEqual(sim_suffix('axx', 'a'), 0)
        self.assertEqual(sim_suffix('ax', 'ay'), 0)
        self.assertEqual(sim_suffix('a', 'ay'), 0)
        self.assertEqual(sim_suffix('a', 'ayy'), 0)
        self.assertEqual(sim_suffix('ax', 'ay'), 0)
        self.assertEqual(sim_suffix('a', 'y'), 0)
        self.assertEqual(sim_suffix('y', 'a'), 0)
        self.assertEqual(sim_suffix('aaax', 'aaa'), 0)
        self.assertEqual(sim_suffix('axxx', 'aaa'), 0)
        self.assertEqual(sim_suffix('aaxx', 'aayy'), 0)
        self.assertEqual(sim_suffix('xxaa', 'yyaa'), 1 / 2)
        self.assertEqual(sim_suffix('aaxxx', 'aay'), 0)
        self.assertEqual(sim_suffix('aaxxxx', 'aayyy'), 0)
        self.assertEqual(sim_suffix('xa', 'a'), 1)
        self.assertEqual(sim_suffix('xxa', 'a'), 1)
        self.assertEqual(sim_suffix('xa', 'ya'), 1 / 2)
        self.assertEqual(sim_suffix('a', 'ya'), 1)
        self.assertEqual(sim_suffix('a', 'yya'), 1)
        self.assertEqual(sim_suffix('xa', 'ya'), 1 / 2)
        self.assertEqual(sim_suffix('xaaa', 'aaa'), 1)
        self.assertAlmostEqual(sim_suffix('xxxa', 'aaa'), 1 / 3)
        self.assertAlmostEqual(sim_suffix('xxxaa', 'yaa'), 2 / 3)
        self.assertEqual(sim_suffix('xxxxaa', 'yyyaa'), 2 / 5)

    def test_dist_suffix(self):
        """Test abydos.distance._basic.dist_suffix."""
        self.assertEqual(dist_suffix('', ''), 0)
        self.assertEqual(dist_suffix('a', ''), 1)
        self.assertEqual(dist_suffix('', 'a'), 1)
        self.assertEqual(dist_suffix('a', 'a'), 0)
        self.assertEqual(dist_suffix('ax', 'a'), 1)
        self.assertEqual(dist_suffix('axx', 'a'), 1)
        self.assertEqual(dist_suffix('ax', 'ay'), 1)
        self.assertEqual(dist_suffix('a', 'ay'), 1)
        self.assertEqual(dist_suffix('a', 'ayy'), 1)
        self.assertEqual(dist_suffix('ax', 'ay'), 1)
        self.assertEqual(dist_suffix('a', 'y'), 1)
        self.assertEqual(dist_suffix('y', 'a'), 1)
        self.assertEqual(dist_suffix('aaax', 'aaa'), 1)
        self.assertEqual(dist_suffix('axxx', 'aaa'), 1)
        self.assertEqual(dist_suffix('aaxx', 'aayy'), 1)
        self.assertEqual(dist_suffix('xxaa', 'yyaa'), 1 / 2)
        self.assertEqual(dist_suffix('aaxxx', 'aay'), 1)
        self.assertEqual(dist_suffix('aaxxxx', 'aayyy'), 1)
        self.assertEqual(dist_suffix('xa', 'a'), 0)
        self.assertEqual(dist_suffix('xxa', 'a'), 0)
        self.assertEqual(dist_suffix('xa', 'ya'), 1 / 2)
        self.assertEqual(dist_suffix('a', 'ya'), 0)
        self.assertEqual(dist_suffix('a', 'yya'), 0)
        self.assertEqual(dist_suffix('xa', 'ya'), 1 / 2)
        self.assertEqual(dist_suffix('xaaa', 'aaa'), 0)
        self.assertAlmostEqual(dist_suffix('xxxa', 'aaa'), 2 / 3)
        self.assertAlmostEqual(dist_suffix('xxxaa', 'yaa'), 1 / 3)
        self.assertEqual(dist_suffix('xxxxaa', 'yyyaa'), 3 / 5)


if __name__ == '__main__':
    unittest.main()
