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

"""abydos.tests.distance.test_distance_discounted_levenshtein.

This module contains unit tests for abydos.distance.DiscountedLevenshtein
"""

import unittest

from abydos.distance import DiscountedLevenshtein


class DiscountedLevenshteinTestCases(unittest.TestCase):
    """Test DiscountedLevenshtein functions.

    abydos.distance.DiscountedLevenshtein
    """

    cmp = DiscountedLevenshtein()
    cmp_coda = DiscountedLevenshtein(discount_from='coda')

    def test_discounted_levenshtein_aligmnent(self):
        """Test abydos.distance.DiscountedLevenshtein.alignment."""
        self.assertEqual(self.cmp.alignment('', ''), (0, '', ''))

        self.assertEqual(self.cmp.alignment('a', 'a'), (0.0, 'a', 'a'))
        self.assertEqual(self.cmp.alignment('ab', 'ab'), (0.0, 'ab', 'ab'))
        self.assertEqual(self.cmp.alignment('', 'a'), (1.0, '-', 'a'))
        self.assertEqual(
            self.cmp.alignment('', 'ab'), (1.845793595028118, '--', 'ab')
        )
        self.assertEqual(self.cmp.alignment('a', 'c'), (1.0, 'a', 'c'))

        self.assertEqual(self.cmp.alignment('abc', 'ac'), (1.0, 'abc', 'a-c'))
        self.assertEqual(
            self.cmp.alignment('abbc', 'ac'),
            (1.845793595028118, 'abbc', 'a--c'),
        )
        self.assertEqual(
            self.cmp.alignment('abbc', 'abc'),
            (0.8457935950281179, 'abbc', 'ab-c'),
        )

        self.assertEqual(
            DiscountedLevenshtein(mode='osa').alignment('Niall', 'Naill'),
            (0.8457935950281179, 'Niall', 'Naill'),
        )

        self.assertEqual(
            self.cmp.alignment('abcd', 'efgh'),
            (3.594032108779918, 'abcd', 'efgh'),
        )

        self.assertEqual(
            self.cmp.alignment('Nigel', 'Niall'),
            (1.5940321087799176, 'Nigel', 'Niall'),
        )
        self.assertEqual(
            self.cmp.alignment('Niall', 'Nigel'),
            (1.5940321087799176, 'Niall', 'Nigel'),
        )
        self.assertEqual(
            self.cmp.alignment('Colin', 'Coiln'),
            (1.5940321087799176, 'Coli-n', 'Co-iln'),
        )
        self.assertEqual(
            self.cmp.alignment('Coiln', 'Colin'),
            (1.5940321087799176, 'Coil-n', 'Co-lin'),
        )
        self.assertEqual(
            self.cmp.alignment('cccColin', 'Colin'),
            (2.594032108779918, 'cccColin', '---Colin'),
        )
        self.assertEqual(
            self.cmp.alignment('Colin', 'cccColin'),
            (2.594032108779918, '---Colin', 'cccColin'),
        )

    def test_discounted_levenshtein_dist_abs(self):
        """Test abydos.distance.DiscountedLevenshtein.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 2.845793595028118)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 2.845793595028118)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 3.594032108779918)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 1.5940321087799176
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 1.5940321087799176
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 1.5940321087799176
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 1.5940321087799176
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 3.480037325627888
        )

    def test_discounted_levenshtein_dist(self):
        """Test abydos.distance.DiscountedLevenshtein.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp.dist('Nigel', 'Niall'), 0.3729338516783247
        )
        self.assertAlmostEqual(
            self.cmp.dist('Niall', 'Nigel'), 0.3729338516783247
        )
        self.assertAlmostEqual(
            self.cmp.dist('Colin', 'Coiln'), 0.3729338516783247
        )
        self.assertAlmostEqual(
            self.cmp.dist('Coiln', 'Colin'), 0.3729338516783247
        )
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.49025364879218414
        )

        self.assertEqual(self.cmp_coda.dist('', ''), 0.0)
        self.assertEqual(self.cmp_coda.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_coda.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_coda.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_coda.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_coda.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_coda.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp_coda.dist('Nigel', 'Niall'), 0.43183503707707127
        )
        self.assertAlmostEqual(
            self.cmp_coda.dist('Niall', 'Nigel'), 0.43183503707707127
        )
        self.assertAlmostEqual(
            self.cmp_coda.dist('Colin', 'Coiln'), 0.43183503707707127
        )
        self.assertAlmostEqual(
            self.cmp_coda.dist('Coiln', 'Colin'), 0.43183503707707127
        )
        self.assertAlmostEqual(
            self.cmp_coda.dist('ATCAACGAGT', 'AACGATTAG'), 0.49025364879218414
        )

        # coverage additions
        self.assertAlmostEqual(
            DiscountedLevenshtein(discount_func='exp').dist('Nigel', 'Niall'),
            0.3776202500185377,
        )
        self.assertAlmostEqual(
            DiscountedLevenshtein(
                discount_func=lambda x: 1 / (x + 2) ** 0.3
            ).dist('Nigel', 'Niall'),
            0.3808786265263343,
        )
        self.assertAlmostEqual(
            self.cmp_coda.dist('da', 'dde'), 0.7027916583599728
        )
        self.assertAlmostEqual(
            self.cmp_coda.dist('d', 'dd'), 0.42289679751405895
        )
        self.assertAlmostEqual(
            DiscountedLevenshtein(discount_from='invalid value').dist(
                'Nigel', 'Niall'
            ),
            0.3729338516783247,
        )
        self.assertAlmostEqual(
            DiscountedLevenshtein(mode='osa').dist('Nigel', 'Ngiall'),
            0.4534644632194963,
        )


if __name__ == '__main__':
    unittest.main()
