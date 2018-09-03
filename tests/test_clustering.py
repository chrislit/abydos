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

"""abydos.tests.test_clustering.

This module contains unit tests for abydos.clustering
"""

from __future__ import unicode_literals

import unittest

import abydos.stats as stats
from abydos.clustering import mean_pairwise_similarity


NIALL = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel', 'Nele',
         'Nigelli', 'Nel', 'Kneale', 'Uí Néill', 'O\'Neill', 'MacNeil',
         'MacNele', 'Niall Noígíallach')

NIALL_1WORD = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel',
               'Nele', 'Nigelli', 'Nel', 'Kneale', 'O\'Neill', 'MacNeil',
               'MacNele')


class MPSTestCases(unittest.TestCase):
    """Test mean pairwise similarity functions.

    abydos.clustering.mean_pairwise_similarity
    """

    def test_mean_pairwise_similarity(self):
        """Test abydos.clustering.mean_pairwise_similarity."""
        self.assertEqual(mean_pairwise_similarity(NIALL), 0.29362587170180671)
        self.assertEqual(mean_pairwise_similarity(NIALL, symmetric=True),
                         0.2936258717018066)
        self.assertEqual(mean_pairwise_similarity(NIALL,
                                                  mean_func=stats.hmean),
                         0.29362587170180671)
        self.assertEqual(mean_pairwise_similarity(NIALL, mean_func=stats.hmean,
                                                  symmetric=True),
                         0.2936258717018066)
        self.assertEqual(mean_pairwise_similarity(NIALL,
                                                  mean_func=stats.gmean),
                         0.33747245800668441)
        self.assertEqual(mean_pairwise_similarity(NIALL, mean_func=stats.gmean,
                                                  symmetric=True),
                         0.33747245800668441)
        self.assertEqual(mean_pairwise_similarity(NIALL,
                                                  mean_func=stats.amean),
                         0.38009278711484601)
        self.assertEqual(mean_pairwise_similarity(NIALL, mean_func=stats.amean,
                                                  symmetric=True),
                         0.38009278711484623)

        self.assertEqual(mean_pairwise_similarity(NIALL_1WORD),
                         mean_pairwise_similarity(' '.join(NIALL_1WORD)))
        self.assertEqual(mean_pairwise_similarity(NIALL_1WORD, symmetric=True),
                         mean_pairwise_similarity(' '.join(NIALL_1WORD),
                                                  symmetric=True))
        self.assertEqual(mean_pairwise_similarity(NIALL_1WORD,
                                                  mean_func=stats.gmean),
                         mean_pairwise_similarity(' '.join(NIALL_1WORD),
                                                  mean_func=stats.gmean))
        self.assertEqual(mean_pairwise_similarity(NIALL_1WORD,
                                                  mean_func=stats.amean),
                         mean_pairwise_similarity(' '.join(NIALL_1WORD),
                                                  mean_func=stats.amean))

        self.assertRaises(ValueError, mean_pairwise_similarity, ['a b c'])
        self.assertRaises(ValueError, mean_pairwise_similarity, 'abc')
        self.assertRaises(ValueError, mean_pairwise_similarity, 0)
        self.assertRaises(ValueError, mean_pairwise_similarity, NIALL,
                          mean_func='imaginary')

        self.assertEqual(mean_pairwise_similarity(NIALL),
                         mean_pairwise_similarity(tuple(NIALL)))
        self.assertEqual(mean_pairwise_similarity(NIALL),
                         mean_pairwise_similarity(list(NIALL)))
        self.assertAlmostEqual(mean_pairwise_similarity(NIALL),
                               mean_pairwise_similarity(sorted(NIALL)))
        self.assertAlmostEqual(mean_pairwise_similarity(NIALL),
                               mean_pairwise_similarity(set(NIALL)))


if __name__ == '__main__':
    unittest.main()
