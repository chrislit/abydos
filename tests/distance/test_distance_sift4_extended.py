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

"""abydos.tests.distance.test_distance_sift4_extended.

This module contains unit tests for abydos.distance.Sift4Extended
"""

import unittest

from abydos.distance import Sift4Extended
from abydos.tokenizer import QGrams


class Sift4ExtendedTestCases(unittest.TestCase):
    """Test Sift4Extended functions.

    abydos.distance.Sift4Extended
    """

    ltamc = Sift4Extended.longer_transpositions_are_more_costly

    cmp = Sift4Extended()
    cmp_kwargs = Sift4Extended(
        tokenizer=QGrams(qval=2),
        token_matcher=Sift4Extended.sift4_token_matcher,
        matching_evaluator=Sift4Extended.sift4_matching_evaluator,
        local_length_evaluator=Sift4Extended.reward_length_evaluator,
        transposition_cost_evaluator=ltamc,
        transpositions_evaluator=lambda lcss, trans: lcss - trans,
    )
    cmp_kwargs2 = Sift4Extended(
        local_length_evaluator=Sift4Extended.reward_length_evaluator_exp
    )
    cmp_md = Sift4Extended(max_distance=3)

    def test_sift4_extended_dist_abs(self):
        """Test abydos.distance.Sift4Extended.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 3)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 3)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 4)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 2)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 2)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 1)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 1)
        self.assertAlmostEqual(self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 4)

        self.assertEqual(self.cmp_kwargs.dist_abs('', ''), 0)
        self.assertEqual(self.cmp_kwargs.dist_abs('a', ''), 2)
        self.assertEqual(self.cmp_kwargs.dist_abs('', 'a'), 2)
        self.assertEqual(self.cmp_kwargs.dist_abs('abc', ''), 4)
        self.assertEqual(self.cmp_kwargs.dist_abs('', 'abc'), 4)
        self.assertEqual(self.cmp_kwargs.dist_abs('abc', 'abc'), -1)
        self.assertEqual(self.cmp_kwargs.dist_abs('abcd', 'efgh'), -2)

        self.assertAlmostEqual(self.cmp_kwargs.dist_abs('Nigel', 'Niall'), 1)
        self.assertAlmostEqual(self.cmp_kwargs.dist_abs('Niall', 'Nigel'), 1)
        self.assertAlmostEqual(self.cmp_kwargs.dist_abs('Colin', 'Coiln'), 1)
        self.assertAlmostEqual(self.cmp_kwargs.dist_abs('Coiln', 'Colin'), 1)
        self.assertAlmostEqual(
            self.cmp_kwargs.dist_abs('ATCAACGAGT', 'AACGATTAG'), 2
        )

        self.assertEqual(self.cmp_kwargs2.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.cmp_kwargs2.dist_abs('abcd', 'efgh'), 8)

        self.assertAlmostEqual(self.cmp_kwargs2.dist_abs('Nigel', 'Niall'), 7)
        self.assertAlmostEqual(self.cmp_kwargs2.dist_abs('Niall', 'Nigel'), 7)
        self.assertAlmostEqual(self.cmp_kwargs2.dist_abs('Colin', 'Coiln'), 6)
        self.assertAlmostEqual(self.cmp_kwargs2.dist_abs('Coiln', 'Colin'), 6)
        self.assertAlmostEqual(
            self.cmp_kwargs2.dist_abs('ATCAACGAGT', 'AACGATTAG'), 25
        )

        # coverage completion
        self.assertAlmostEqual(
            self.cmp_kwargs.dist_abs('beaurocracy', 'bureaucracy'), 3
        )
        self.assertAlmostEqual(
            self.cmp_md.dist_abs('beaurocratically', 'bureaucracy'), 3
        )
        self.assertAlmostEqual(
            self.cmp_md.dist_abs('bureaucracy', 'bureaucracy'), 3
        )


if __name__ == '__main__':
    unittest.main()
