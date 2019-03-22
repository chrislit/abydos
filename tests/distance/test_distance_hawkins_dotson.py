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

"""abydos.tests.distance.test_distance_hawkins_dotson.

This module contains unit tests for abydos.distance.HawkinsDotson
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import HawkinsDotson


class HawkinsDotsonTestCases(unittest.TestCase):
    """Test HawkinsDotson functions.

    abydos.distance.HawkinsDotson
    """

    cmp = HawkinsDotson()
    cmp_no_d = HawkinsDotson(alphabet=0)

    def test_hawkins_dotson_sim(self):
        """Test abydos.distance.HawkinsDotson.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.4987244897959184)
        self.assertEqual(self.cmp.sim('', 'a'), 0.4987244897959184)
        self.assertEqual(self.cmp.sim('abc', ''), 0.49744897959183676)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.49744897959183676)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.49362244897959184)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6628254375)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6628254375)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6628254375)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6628254375)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7454954955
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.1666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.25
        )

    def test_hawkins_dotson_dist(self):
        """Test abydos.distance.HawkinsDotson.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.5012755102040816)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5012755102040816)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5025510204081632)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5025510204081632)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5063775510204082)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3371745625)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3371745625)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.3371745625)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.3371745625)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2545045045
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.8333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.8333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.8333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.8333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.75
        )


if __name__ == '__main__':
    unittest.main()
