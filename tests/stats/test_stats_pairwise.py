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

"""abydos.tests.stats.test_stats_pairwise.

This module contains unit tests for abydos.stats pairwise functions
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import sim_jaccard
from abydos.stats import (
    amean,
    gmean,
    hmean,
    mean_pairwise_similarity,
    pairwise_similarity_statistics,
)

NIALL = (
    'Niall',
    'Neal',
    'Neil',
    'Njall',
    'Njáll',
    'Nigel',
    'Neel',
    'Nele',
    'Nigelli',
    'Nel',
    'Kneale',
    'Uí Néill',
    "O'Neill",
    'MacNeil',
    'MacNele',
    'Niall Noígíallach',
)

NIALL_1WORD = (
    'Niall',
    'Neal',
    'Neil',
    'Njall',
    'Njáll',
    'Nigel',
    'Neel',
    'Nele',
    'Nigelli',
    'Nel',
    'Kneale',
    "O'Neill",
    'MacNeil',
    'MacNele',
)


class MPSTestCases(unittest.TestCase):
    """Test mean pairwise similarity functions.

    abydos.stats.mean_pairwise_similarity
    """

    def test_mean_pairwise_similarity(self):
        """Test abydos.stats.mean_pairwise_similarity."""
        self.assertEqual(mean_pairwise_similarity(NIALL), 0.29362587170180671)
        self.assertEqual(
            mean_pairwise_similarity(NIALL, symmetric=True), 0.2936258717018066
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL, mean_func=hmean),
            0.29362587170180671,
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL, mean_func=hmean, symmetric=True),
            0.2936258717018066,
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL, mean_func=gmean),
            0.33747245800668441,
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL, mean_func=gmean, symmetric=True),
            0.33747245800668441,
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL, mean_func=amean),
            0.38009278711484601,
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL, mean_func=amean, symmetric=True),
            0.38009278711484623,
        )

        self.assertEqual(
            mean_pairwise_similarity(NIALL_1WORD),
            mean_pairwise_similarity(' '.join(NIALL_1WORD)),
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL_1WORD, symmetric=True),
            mean_pairwise_similarity(' '.join(NIALL_1WORD), symmetric=True),
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL_1WORD, mean_func=gmean),
            mean_pairwise_similarity(' '.join(NIALL_1WORD), mean_func=gmean),
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL_1WORD, mean_func=amean),
            mean_pairwise_similarity(' '.join(NIALL_1WORD), mean_func=amean),
        )

        self.assertRaises(ValueError, mean_pairwise_similarity, ['a b c'])
        self.assertRaises(ValueError, mean_pairwise_similarity, 'abc')
        self.assertRaises(ValueError, mean_pairwise_similarity, 0)
        self.assertRaises(
            ValueError, mean_pairwise_similarity, NIALL, mean_func='imaginary'
        )
        self.assertRaises(
            ValueError, mean_pairwise_similarity, NIALL, metric='imaginary'
        )

        self.assertEqual(
            mean_pairwise_similarity(NIALL),
            mean_pairwise_similarity(tuple(NIALL)),
        )
        self.assertEqual(
            mean_pairwise_similarity(NIALL),
            mean_pairwise_similarity(list(NIALL)),
        )
        self.assertAlmostEqual(
            mean_pairwise_similarity(NIALL),
            mean_pairwise_similarity(sorted(NIALL)),
        )
        self.assertAlmostEqual(
            mean_pairwise_similarity(NIALL),
            mean_pairwise_similarity(set(NIALL)),
        )


class PSSTestCases(unittest.TestCase):
    """Test pairwise similarity statistics functions.

    abydos.stats.pairwise_similarity_statistics
    """

    def test_pairwise_similarity_statistics(self):
        """Test abydos.stats.pairwise_similarity_statistics."""
        (pw_max, pw_min, pw_mean, pw_std) = pairwise_similarity_statistics(
            NIALL, NIALL
        )
        self.assertAlmostEqual(pw_max, 1.0)
        self.assertAlmostEqual(pw_min, 0.11764705882352944)
        self.assertAlmostEqual(pw_mean, 0.4188369879201684)
        self.assertAlmostEqual(pw_std, 0.2265099631340623)

        (pw_max, pw_min, pw_mean, pw_std) = pairwise_similarity_statistics(
            NIALL, ('Kneal',)
        )
        self.assertAlmostEqual(pw_max, 0.8333333333333334)
        self.assertAlmostEqual(pw_min, 0.11764705882352944)
        self.assertAlmostEqual(pw_mean, 0.30474877450980387)
        self.assertAlmostEqual(pw_std, 0.1842666797571549)

        # Test symmetric
        (pw_max, pw_min, pw_mean, pw_std) = pairwise_similarity_statistics(
            NIALL, NIALL, symmetric=True
        )
        self.assertAlmostEqual(pw_max, 1.0)
        self.assertAlmostEqual(pw_min, 0.11764705882352944)
        self.assertAlmostEqual(pw_mean, 0.4188369879201679)
        self.assertAlmostEqual(pw_std, 0.22650996313406255)

        (pw_max, pw_min, pw_mean, pw_std) = pairwise_similarity_statistics(
            NIALL, ('Kneal',), symmetric=True
        )
        self.assertAlmostEqual(pw_max, 0.8333333333333334)
        self.assertAlmostEqual(pw_min, 0.11764705882352944)
        self.assertAlmostEqual(pw_mean, 0.304748774509804)
        self.assertAlmostEqual(pw_std, 0.18426667975715486)

        # Test with splittable strings
        (pw_max, pw_min, pw_mean, pw_std) = pairwise_similarity_statistics(
            'The quick brown fox', 'jumped over the lazy dog.'
        )
        self.assertAlmostEqual(pw_max, 0.6666666666666667)
        self.assertAlmostEqual(pw_min, 0.0)
        self.assertAlmostEqual(pw_mean, 0.08499999999999999)
        self.assertAlmostEqual(pw_std, 0.16132265804901677)

        (pw_max, pw_min, pw_mean, pw_std) = pairwise_similarity_statistics(
            'The', 'jumped'
        )
        self.assertAlmostEqual(pw_max, 0.16666666666666663)
        self.assertAlmostEqual(pw_min, 0.16666666666666663)
        self.assertAlmostEqual(pw_mean, 0.16666666666666663)
        self.assertAlmostEqual(pw_std, 0.0)

        # Test with a set metric
        (pw_max, pw_min, pw_mean, pw_std) = pairwise_similarity_statistics(
            NIALL, NIALL, metric=sim_jaccard
        )
        self.assertAlmostEqual(pw_max, 1.0)
        self.assertAlmostEqual(pw_min, 0.0)
        self.assertAlmostEqual(pw_mean, 0.23226906681010506)
        self.assertAlmostEqual(pw_std, 0.24747101181262784)

        # Test using hmean'
        (pw_max, pw_min, pw_mean, pw_std) = pairwise_similarity_statistics(
            NIALL, NIALL, mean_func=hmean
        )
        self.assertAlmostEqual(pw_max, 1.0)
        self.assertAlmostEqual(pw_min, 0.11764705882352944)
        self.assertAlmostEqual(pw_mean, 0.30718771249150056)
        self.assertAlmostEqual(pw_std, 0.25253182790044676)

        # Test exceptions
        self.assertRaises(
            ValueError,
            pairwise_similarity_statistics,
            NIALL,
            NIALL,
            mean_func=None,
        )
        self.assertRaises(
            ValueError,
            pairwise_similarity_statistics,
            NIALL,
            NIALL,
            metric=None,
        )
        self.assertRaises(ValueError, pairwise_similarity_statistics, 5, NIALL)
        self.assertRaises(ValueError, pairwise_similarity_statistics, NIALL, 5)


if __name__ == '__main__':
    unittest.main()
