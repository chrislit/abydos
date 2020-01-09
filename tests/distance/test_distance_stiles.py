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

"""abydos.tests.distance.test_distance_stiles.

This module contains unit tests for abydos.distance.Stiles
"""

import unittest

from abydos.distance import Stiles


class StilesTestCases(unittest.TestCase):
    """Test Stiles functions.

    abydos.distance.Stiles
    """

    cmp = Stiles()
    cmp_no_d = Stiles(alphabet=0)

    def test_stiles_sim(self):
        """Test abydos.distance.Stiles.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.760700314616495)
        self.assertEqual(self.cmp.sim('', 'a'), 0.760700314616495)
        self.assertEqual(self.cmp.sim('abc', ''), 0.7416916584588271)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.7416916584588271)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.4768516719017855)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5744293838)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5744293838)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5744293838)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5744293838)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5909028826
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('a', ''), 0.9511587063686434)
        self.assertAlmostEqual(self.cmp_no_d.sim('', 'a'), 0.9511587063686434)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('abc', ''), 0.9309340273884292
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('', 'abc'), 0.9309340273884292
        )
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('abcd', 'efgh'), 0.47481536969259386
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.5216609379
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.5216609379
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.5216609379
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.5216609379
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5532905837
        )

    def test_stiles_dist(self):
        """Test abydos.distance.Stiles.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.239299685383505)
        self.assertEqual(self.cmp.dist('', 'a'), 0.239299685383505)
        self.assertEqual(self.cmp.dist('abc', ''), 0.2583083415411729)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.2583083415411729)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.5231483280982145)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4255706162)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4255706162)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.4255706162)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.4255706162)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4090971174
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('a', ''), 0.048841293631356586
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('', 'a'), 0.048841293631356586
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('abc', ''), 0.06906597261157077
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('', 'abc'), 0.06906597261157077
        )
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('abcd', 'efgh'), 0.5251846303074061
        )

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.4783390621
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.4783390621
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.4783390621
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.4783390621
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.4467094163
        )

    def test_stiles_sim_score(self):
        """Test abydos.distance.Stiles.sim_score."""
        # Base cases
        self.assertAlmostEqual(self.cmp.sim_score('', ''), 16.292255897915638)
        self.assertAlmostEqual(self.cmp.sim_score('a', ''), 8.992335212208333)
        self.assertAlmostEqual(self.cmp.sim_score('', 'a'), 8.992335212208333)
        self.assertAlmostEqual(
            self.cmp.sim_score('abc', ''), 8.692417367356594
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('', 'abc'), 8.692417367356594
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('abc', 'abc'), 17.98245215160657
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('abcd', 'efgh'), -0.8426334527850912
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 2.7352860243
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 2.7352860243
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 2.7352860243
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 2.7352860243
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 3.4428002638
        )

        # Tests with alphabet=0 (no d factor)
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('', ''), 13.647817481888637
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('a', ''), 13.22184890168726
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('', 'a'), 13.22184890168726
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('abc', ''), 13.522878821349728
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('', 'abc'), 13.522878821349728
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('abc', 'abc'), 15.69019612345796
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('abcd', 'efgh'), -0.8061799153541304
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), 0.7043650362
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), 0.7043650362
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), 0.7043650362
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), 0.7043650362
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), 1.8208082871
        )

    def test_stiles_corr(self):
        """Test abydos.distance.Stiles.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 1.0)
        self.assertAlmostEqual(self.cmp.corr('a', ''), 0.5214006292329901)
        self.assertAlmostEqual(self.cmp.corr('', 'a'), 0.5214006292329901)
        self.assertAlmostEqual(self.cmp.corr('abc', ''), 0.48338331691765435)
        self.assertAlmostEqual(self.cmp.corr('', 'abc'), 0.48338331691765435)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertAlmostEqual(
            self.cmp.corr('abcd', 'efgh'), -0.046296656196428934
        )

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.1488587676)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.1488587676)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.1488587676)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.1488587676)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.1818057652
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.corr('a', ''), 0.9023174127372868)
        self.assertAlmostEqual(self.cmp_no_d.corr('', 'a'), 0.9023174127372868)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('abc', ''), 0.8618680547768583
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('', 'abc'), 0.8618680547768583
        )
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('abcd', 'efgh'), -0.05036926061481227
        )

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), 0.0433218759
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), 0.0433218759
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), 0.0433218759
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), 0.0433218759
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), 0.1065811673
        )


if __name__ == '__main__':
    unittest.main()
