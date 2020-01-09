# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_unigram_subtuple.

This module contains unit tests for abydos.distance.UnigramSubtuple
"""

import unittest

from abydos.distance import UnigramSubtuple


class UnigramSubtupleTestCases(unittest.TestCase):
    """Test UnigramSubtuple functions.

    abydos.distance.UnigramSubtuple
    """

    cmp = UnigramSubtuple()
    cmp_no_d = UnigramSubtuple(alphabet=0)

    def test_unigram_subtuple_sim(self):
        """Test abydos.distance.UnigramSubtuple.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.3557288160556184)
        self.assertEqual(self.cmp.sim('', 'a'), 0.3557288160556184)
        self.assertEqual(self.cmp.sim('abc', ''), 0.10825796687276863)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.10825796687276863)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6276193132)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6276193132)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6276193132)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6276193132)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7696362294
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.0)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.0)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.0
        )

    def test_unigram_subtuple_dist(self):
        """Test abydos.distance.UnigramSubtuple.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.6442711839443815)
        self.assertEqual(self.cmp.dist('', 'a'), 0.6442711839443815)
        self.assertEqual(self.cmp.dist('abc', ''), 0.8917420331272313)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.8917420331272313)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3723806868)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3723806868)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.3723806868)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.3723806868)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2303637706
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 1.0)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 1.0)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 1.0
        )

    def test_unigram_subtuple_sim_score(self):
        """Test abydos.distance.UnigramSubtuple.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.964750587602003)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.765430557931535)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.765430557931535)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.3365937758831885)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.3365937758831885)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 3.10918249812297)
        self.assertEqual(
            self.cmp.sim_score('abcd', 'efgh'), -0.461880260111438
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 2.2621288443
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 2.2621288443
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 2.2621288443
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 2.2621288443
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 3.3012550999
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim_score('', ''), -6.58)
        self.assertEqual(self.cmp_no_d.sim_score('a', ''), -6.848173581803079)
        self.assertEqual(self.cmp_no_d.sim_score('', 'a'), -6.848173581803079)
        self.assertEqual(
            self.cmp_no_d.sim_score('abc', ''), -7.317426209258153
        )
        self.assertEqual(
            self.cmp_no_d.sim_score('', 'abc'), -7.317426209258153
        )
        self.assertEqual(
            self.cmp_no_d.sim_score('abc', 'abc'), -4.544837487018372
        )
        self.assertEqual(
            self.cmp_no_d.sim_score('abcd', 'efgh'), -8.315721908477162
        )

        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Nigel', 'Niall'), -5.7513749089
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Niall', 'Nigel'), -5.7513749089
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Colin', 'Coiln'), -5.7513749089
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('Coiln', 'Colin'), -5.7513749089
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim_score('ATCAACGAGT', 'AACGATTAG'), -4.8615487946
        )


if __name__ == '__main__':
    unittest.main()
