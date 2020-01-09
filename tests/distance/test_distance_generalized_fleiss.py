# -*- coding: utf-8 -*-

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

"""abydos.tests.distance.test_distance_generalized_fleiss.

This module contains unit tests for abydos.distance.GeneralizedFleiss
"""

import unittest

from abydos.distance import GeneralizedFleiss


class GeneralizedFleissTestCases(unittest.TestCase):
    """Test GeneralizedFleiss functions.

    abydos.distance.GeneralizedFleiss
    """

    cmp = GeneralizedFleiss(marginals='a')
    cmp_no_d = GeneralizedFleiss(alphabet=0)
    cmp_b = GeneralizedFleiss(marginals='b')
    cmp_c = GeneralizedFleiss(marginals='c')
    cmp_prop = GeneralizedFleiss(proportional=True)
    cmp_quad = GeneralizedFleiss(mean_func='quadratic')
    cmp_hero = GeneralizedFleiss(mean_func='heronian')
    cmp_ag = GeneralizedFleiss(mean_func='ag')
    cmp_gh = GeneralizedFleiss(mean_func='gh')
    cmp_agh = GeneralizedFleiss(mean_func='agh')

    def test_generalized_fleiss_sim(self):
        """Test abydos.distance.GeneralizedFleiss.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5)
        self.assertEqual(self.cmp.sim('a', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7480719794)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7480719794)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.8310964723
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.25)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.25)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.3356164384
        )

        # marginals b
        self.assertEqual(self.cmp_b.sim('abc', 'abc'), 0.5051280702677116)
        self.assertEqual(self.cmp_b.sim('abcd', 'efgh'), 0.4999588047443752)

        self.assertAlmostEqual(
            self.cmp_b.sim('Nigel', 'Niall'), 0.5038260754642173
        )
        self.assertAlmostEqual(
            self.cmp_b.sim('Niall', 'Nigel'), 0.5038260754642173
        )
        self.assertAlmostEqual(
            self.cmp_b.sim('Colin', 'Coiln'), 0.5038260754642173
        )
        self.assertAlmostEqual(
            self.cmp_b.sim('Coiln', 'Colin'), 0.5038260754642173
        )
        self.assertAlmostEqual(
            self.cmp_b.sim('ATCAACGAGT', 'AACGATTAG'), 0.5089871192422611
        )

        # marginals c
        self.assertEqual(self.cmp_c.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_c.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(
            self.cmp_c.sim('Nigel', 'Niall'), 0.7480719794344473
        )
        self.assertAlmostEqual(
            self.cmp_c.sim('Niall', 'Nigel'), 0.7480719794344473
        )
        self.assertAlmostEqual(
            self.cmp_c.sim('Colin', 'Coiln'), 0.7480719794344473
        )
        self.assertAlmostEqual(
            self.cmp_c.sim('Coiln', 'Colin'), 0.7480719794344473
        )
        self.assertAlmostEqual(
            self.cmp_c.sim('ATCAACGAGT', 'AACGATTAG'), 0.8310760896330953
        )

        # proportional
        self.assertEqual(self.cmp_prop.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_prop.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(
            self.cmp_prop.sim('Nigel', 'Niall'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_prop.sim('Niall', 'Nigel'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_prop.sim('Colin', 'Coiln'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_prop.sim('Coiln', 'Colin'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_prop.sim('ATCAACGAGT', 'AACGATTAG'), 0.8310964723
        )

        # quadratic mean
        self.assertEqual(self.cmp_quad.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_quad.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(
            self.cmp_quad.sim('Nigel', 'Niall'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_quad.sim('Niall', 'Nigel'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_quad.sim('Colin', 'Coiln'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_quad.sim('Coiln', 'Colin'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_quad.sim('ATCAACGAGT', 'AACGATTAG'), 0.8307317829209393
        )

        # heronian mean
        self.assertEqual(self.cmp_hero.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_hero.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(
            self.cmp_hero.sim('Nigel', 'Niall'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_hero.sim('Niall', 'Nigel'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_hero.sim('Colin', 'Coiln'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_hero.sim('Coiln', 'Colin'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_hero.sim('ATCAACGAGT', 'AACGATTAG'), 0.8312183486929234
        )

        # ag mean
        self.assertEqual(self.cmp_ag.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_ag.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(self.cmp_ag.sim('Nigel', 'Niall'), 0.7480719794)
        self.assertAlmostEqual(self.cmp_ag.sim('Niall', 'Nigel'), 0.7480719794)
        self.assertAlmostEqual(self.cmp_ag.sim('Colin', 'Coiln'), 0.7480719794)
        self.assertAlmostEqual(self.cmp_ag.sim('Coiln', 'Colin'), 0.7480719794)
        self.assertAlmostEqual(
            self.cmp_ag.sim('ATCAACGAGT', 'AACGATTAG'), 0.8312793457877081
        )

        # gh mean
        self.assertEqual(self.cmp_gh.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_gh.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(self.cmp_gh.sim('Nigel', 'Niall'), 0.7480719794)
        self.assertAlmostEqual(self.cmp_gh.sim('Niall', 'Nigel'), 0.7480719794)
        self.assertAlmostEqual(self.cmp_gh.sim('Colin', 'Coiln'), 0.7480719794)
        self.assertAlmostEqual(self.cmp_gh.sim('Coiln', 'Colin'), 0.7480719794)
        self.assertAlmostEqual(
            self.cmp_gh.sim('ATCAACGAGT', 'AACGATTAG'), 0.8316454969290444
        )

        # agh mean
        self.assertEqual(self.cmp_agh.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_agh.sim('abcd', 'efgh'), 0.496790757381258)

        self.assertAlmostEqual(
            self.cmp_agh.sim('Nigel', 'Niall'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_agh.sim('Niall', 'Nigel'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_agh.sim('Colin', 'Coiln'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_agh.sim('Coiln', 'Colin'), 0.7480719794
        )
        self.assertAlmostEqual(
            self.cmp_agh.sim('ATCAACGAGT', 'AACGATTAG'), 0.8314623707995847
        )

    def test_generalized_fleiss_dist(self):
        """Test abydos.distance.GeneralizedFleiss.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.5)
        self.assertEqual(self.cmp.dist('a', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.503209242618742)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2519280206)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2519280206)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.1689035277
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 0.5)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.5)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.dist('Nigel', 'Niall'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Niall', 'Nigel'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Colin', 'Coiln'), 0.75)
        self.assertAlmostEqual(self.cmp_no_d.dist('Coiln', 'Colin'), 0.75)
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.6643835616
        )

    def test_generalized_fleiss_corr(self):
        """Test abydos.distance.GeneralizedFleiss.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.0)
        self.assertEqual(self.cmp.corr('a', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), -0.006418485237483954)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.4961439589)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.6621929447
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.corr('Nigel', 'Niall'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Niall', 'Nigel'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Colin', 'Coiln'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.corr('Coiln', 'Colin'), -0.5)
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), -0.3287671233
        )


if __name__ == '__main__':
    unittest.main()
