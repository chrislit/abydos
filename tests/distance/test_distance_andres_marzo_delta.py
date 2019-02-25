# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_andres_marzo_delta.

This module contains unit tests for abydos.distance.AndresMarzoDelta
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import AndresMarzoDelta


class AndresMarzoDeltaTestCases(unittest.TestCase):
    """Test AndresMarzoDelta functions.

    abydos.distance.AndresMarzoDelta
    """

    cmp = AndresMarzoDelta()
    cmp_no_d = AndresMarzoDelta(alphabet=0)

    def test_andres_marzo_delta_sim(self):
        """Test abydos.distance.AndresMarzoDelta.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9987244897959184)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9987244897959184)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9974489795918368)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9974489795918368)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9872448979591837)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9923469388)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9923469388)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9923469388)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9923469388)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9911172173
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5025641703
        )

    def test_andres_marzo_delta_corr(self):
        """Test abydos.distance.AndresMarzoDelta.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.9974489795918368)
        self.assertEqual(self.cmp.corr('', 'a'), 0.9974489795918368)
        self.assertEqual(self.cmp.corr('abc', ''), 0.9948979591836735)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.9948979591836735)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), 0.9744897959183674)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.9846938776)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.9846938776)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.9846938776)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.9846938776)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.9822344347
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), 0.0051283407
        )


if __name__ == '__main__':
    unittest.main()
