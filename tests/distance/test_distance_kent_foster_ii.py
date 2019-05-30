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

"""abydos.tests.distance.test_distance_kent_foster_ii.

This module contains unit tests for abydos.distance.KentFosterII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KentFosterII


class KentFosterIITestCases(unittest.TestCase):
    """Test KentFosterII functions.

    abydos.distance.KentFosterII
    """

    cmp = KentFosterII()
    cmp_no_d = KentFosterII(alphabet=0)

    def test_kent_foster_ii_sim(self):
        """Test abydos.distance.KentFosterII.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9968010236724241)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9980756895)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9980756895)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9980756895)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9980756895)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.9977888336
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.6666666666666667)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.6666666667
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.6756756757
        )

    def test_kent_foster_ii_dist(self):
        """Test abydos.distance.KentFosterII.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.003198976327575931)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.0019243105)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.0019243105)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.0019243105)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.0019243105)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.0022111664
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.33333333333333326
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.3243243243
        )

    def test_kent_foster_ii_sim_score(self):
        """Test abydos.distance.KentFosterII.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), -0.0031989763275758767
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), -0.0019243105
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), -0.0019243105
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), -0.0019243105
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), -0.0019243105
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), -0.0022111664
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim_score('abc', 'abc'), 0.0)
        self.assertEqual(
            self.cmp_no_d.sim_score('abcd', 'efgh'), -0.3333333333333333
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), -0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), -0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), -0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), -0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), -0.3243243243
        )


if __name__ == '__main__':
    unittest.main()
