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

"""abydos.tests.distance.test_distance__token_distance.

This module contains unit tests for abydos.distance._TokenDistance
"""

import unittest
from collections import Counter

from abydos.distance import (
    AverageLinkage,
    DamerauLevenshtein,
    Jaccard,
    JaroWinkler,
    SokalMichener,
)
from abydos.stats import ConfusionTable
from abydos.tokenizer import (
    CharacterTokenizer,
    QSkipgrams,
    WhitespaceTokenizer,
)


class TokenDistanceTestCases(unittest.TestCase):
    """Test _TokenDistance functions.

    abydos.distance._TokenDistance
    """

    cmp_j_crisp = Jaccard(intersection_type='crisp')
    cmp_j_soft = Jaccard(intersection_type='soft')
    cmp_j_fuzzy = Jaccard(
        intersection_type='fuzzy', metric=DamerauLevenshtein(), threshold=0.4
    )
    cmp_j_linkage = Jaccard(intersection_type='linkage')

    def test_crisp_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim (crisp)."""
        # Base cases
        self.assertEqual(self.cmp_j_crisp.sim('', ''), 1.0)
        self.assertEqual(self.cmp_j_crisp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_j_crisp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_j_crisp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_j_crisp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_j_crisp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_j_crisp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('Nigel', 'Niall'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('Niall', 'Nigel'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('Colin', 'Coiln'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('Coiln', 'Colin'), 0.3333333333
        )
        self.assertAlmostEqual(
            self.cmp_j_crisp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

    def test_soft_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim (soft)."""
        # Base cases
        self.assertEqual(self.cmp_j_soft.sim('', ''), 1.0)
        self.assertEqual(self.cmp_j_soft.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_j_soft.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_j_soft.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_j_soft.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_j_soft.sim('abc', 'abc'), 1.0)
        self.assertAlmostEqual(self.cmp_j_soft.sim('abcd', 'efgh'), 0.11111111)

        self.assertAlmostEqual(self.cmp_j_soft.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp_j_soft.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp_j_soft.sim('Colin', 'Coiln'), 0.6)
        self.assertAlmostEqual(self.cmp_j_soft.sim('Coiln', 'Colin'), 0.6)
        self.assertAlmostEqual(
            self.cmp_j_soft.sim('ATCAACGAGT', 'AACGATTAG'), 0.68
        )

        self.assertAlmostEqual(
            Jaccard(
                intersection_type='soft', tokenizer=WhitespaceTokenizer()
            ).sim('junior system analyst', 'systems analyst'),
            0.6190476190476191,
        )
        self.assertAlmostEqual(
            Jaccard(
                intersection_type='soft', tokenizer=WhitespaceTokenizer()
            ).sim('systems analyst', 'junior system analyst'),
            0.6190476190476191,
        )

        with self.assertRaises(TypeError):
            Jaccard(
                intersection_type='soft',
                metric=JaroWinkler(),
                tokenizer=WhitespaceTokenizer(),
            ).sim('junior system analyst', 'systems analyst')

    def test_fuzzy_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim (fuzzy)."""
        # Base cases
        self.assertEqual(self.cmp_j_fuzzy.sim('', ''), 1.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_j_fuzzy.sim('abc', 'abc'), 1.0)
        self.assertAlmostEqual(
            self.cmp_j_fuzzy.sim('abcd', 'efgh'), 0.1111111111111111
        )

        self.assertAlmostEqual(self.cmp_j_fuzzy.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp_j_fuzzy.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp_j_fuzzy.sim('Colin', 'Coiln'), 0.6)
        self.assertAlmostEqual(self.cmp_j_fuzzy.sim('Coiln', 'Colin'), 0.6)
        self.assertAlmostEqual(
            self.cmp_j_fuzzy.sim('ATCAACGAGT', 'AACGATTAG'), 0.68
        )
        self.assertEqual(sum(self.cmp_j_fuzzy._union().values()), 11.0)

        self.assertAlmostEqual(
            Jaccard(intersection_type='fuzzy').sim('synonym', 'antonym'),
            0.3333333333333333,
        )

    def test_linkage_jaccard_sim(self):
        """Test abydos.distance.Jaccard.sim (group linkage)."""
        # Base cases
        self.assertEqual(self.cmp_j_linkage.sim('', ''), 1.0)
        self.assertEqual(self.cmp_j_linkage.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_j_linkage.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_j_linkage.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_j_linkage.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_j_linkage.sim('abc', 'abc'), 1.0)
        self.assertAlmostEqual(
            self.cmp_j_linkage.sim('abcd', 'efgh'), 0.1111111111111111
        )

        self.assertAlmostEqual(self.cmp_j_linkage.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp_j_linkage.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp_j_linkage.sim('Colin', 'Coiln'), 0.6)
        self.assertAlmostEqual(self.cmp_j_linkage.sim('Coiln', 'Colin'), 0.6)
        self.assertAlmostEqual(
            self.cmp_j_linkage.sim('ATCAACGAGT', 'AACGATTAG'), 0.68
        )

        self.assertAlmostEqual(
            Jaccard(
                intersection_type='linkage',
                metric=JaroWinkler(),
                threshold=0.2,
            ).sim('synonym', 'antonym'),
            0.6,
        )

    def test_token_distance(self):
        """Test abydos.distance._TokenDistance members."""
        self.assertAlmostEqual(
            Jaccard(intersection_type='soft', alphabet=24).sim(
                'ATCAACGAGT', 'AACGATTAG'
            ),
            0.68,
        )
        self.assertAlmostEqual(
            Jaccard(qval=1, alphabet='CGAT').sim('ATCAACGAGT', 'AACGATTAG'),
            0.9,
        )
        self.assertAlmostEqual(
            Jaccard(tokenizer=QSkipgrams(qval=3), alphabet='CGAT').sim(
                'ATCAACGAGT', 'AACGATTAG'
            ),
            0.6372795969773299,
        )
        self.assertAlmostEqual(
            Jaccard(alphabet=None).sim('synonym', 'antonym'),
            0.3333333333333333,
        )
        self.assertAlmostEqual(
            Jaccard(tokenizer=QSkipgrams(qval=3)).sim('synonym', 'antonym'),
            0.34146341463414637,
        )

        src_ctr = Counter({'a': 5, 'b': 2, 'c': 10})
        tar_ctr = Counter({'a': 2, 'c': 1, 'd': 3, 'e': 12})
        self.assertAlmostEqual(Jaccard().sim(src_ctr, tar_ctr), 0.09375)

        self.assertAlmostEqual(
            SokalMichener(normalizer='proportional').sim('synonym', 'antonym'),
            0.984777917351113,
        )
        self.assertAlmostEqual(
            SokalMichener(normalizer='log').sim('synonym', 'antonym'),
            1.2385752469545532,
        )
        self.assertAlmostEqual(
            SokalMichener(normalizer='exp', alphabet=0).sim(
                'synonym', 'antonym'
            ),
            3.221246147982545e18,
        )
        self.assertAlmostEqual(
            SokalMichener(normalizer='laplace').sim('synonym', 'antonym'),
            0.98856416772554,
        )
        self.assertAlmostEqual(
            SokalMichener(normalizer='inverse').sim('synonym', 'antonym'),
            197.95790155440417,
        )
        self.assertAlmostEqual(
            SokalMichener(normalizer='complement').sim('synonym', 'antonym'),
            1.0204081632653061,
        )
        self.assertAlmostEqual(
            SokalMichener(normalizer='base case').sim('synonym', 'antonym'),
            0.9897959183673469,
        )
        self.assertAlmostEqual(
            SokalMichener().sim('synonym', 'antonym'), 0.9897959183673469
        )

        sm = SokalMichener()
        sm._tokenize('synonym', 'antonym')  # noqa: SF01

        self.assertEqual(
            sm._get_tokens(),  # noqa: SF01
            (
                Counter(
                    {
                        '$s': 1,
                        'sy': 1,
                        'yn': 1,
                        'no': 1,
                        'on': 1,
                        'ny': 1,
                        'ym': 1,
                        'm#': 1,
                    }
                ),
                Counter(
                    {
                        '$a': 1,
                        'an': 1,
                        'nt': 1,
                        'to': 1,
                        'on': 1,
                        'ny': 1,
                        'ym': 1,
                        'm#': 1,
                    }
                ),
            ),
        )
        self.assertEqual(sm._src_card(), 8)  # noqa: SF01
        self.assertEqual(sm._tar_card(), 8)  # noqa: SF01
        self.assertEqual(
            sm._symmetric_difference(),  # noqa: SF01
            Counter(
                {
                    '$s': 1,
                    'sy': 1,
                    'yn': 1,
                    'no': 1,
                    '$a': 1,
                    'an': 1,
                    'nt': 1,
                    'to': 1,
                }
            ),
        )
        self.assertEqual(sm._symmetric_difference_card(), 8)  # noqa: SF01
        self.assertEqual(sm._total_complement_card(), 772)  # noqa: SF01
        self.assertEqual(sm._population_card(), 788)  # noqa: SF01
        self.assertEqual(
            sm._union(),  # noqa: SF01
            Counter(
                {
                    '$s': 1,
                    'sy': 1,
                    'yn': 1,
                    'no': 1,
                    'on': 1,
                    'ny': 1,
                    'ym': 1,
                    'm#': 1,
                    '$a': 1,
                    'an': 1,
                    'nt': 1,
                    'to': 1,
                }
            ),
        )
        self.assertEqual(sm._union_card(), 12)  # noqa: SF01
        self.assertEqual(
            sm._difference(),  # noqa: SF01
            Counter(
                {
                    '$s': 1,
                    'sy': 1,
                    'yn': 1,
                    'no': 1,
                    'on': 0,
                    'ny': 0,
                    'ym': 0,
                    'm#': 0,
                    '$a': -1,
                    'an': -1,
                    'nt': -1,
                    'to': -1,
                }
            ),
        )
        self.assertEqual(
            sm._intersection(),  # noqa: SF01
            Counter({'on': 1, 'ny': 1, 'ym': 1, 'm#': 1}),
        )
        self.assertEqual(
            sm._get_confusion_table(),  # noqa: SF01
            ConfusionTable(tp=4, tn=772, fp=4, fn=4),
        )

        sm = SokalMichener(
            alphabet=Counter({'C': 20, 'G': 20, 'A': 20, 'T': 20}), qval=1
        )
        sm._tokenize('ATCAACGAGT', 'AACGATTAG')  # noqa: SF01
        self.assertEqual(sm._total_complement_card(), 61)  # noqa: SF01

        self.assertAlmostEqual(
            self.cmp_j_linkage.sim('abandonned', 'abandoned'),
            0.9090909090909091,
        )
        self.assertAlmostEqual(
            self.cmp_j_linkage.sim('abundacies', 'abundances'),
            0.6923076923076923,
        )

        # Some additional constructors needed to complete test coverage
        self.assertAlmostEqual(
            Jaccard(alphabet=None, qval=range(2, 4)).sim('abc', 'abcd'),
            0.42857142857142855,
        )
        self.assertAlmostEqual(
            AverageLinkage(qval=range(2, 4)).sim('abc', 'abcd'),
            0.22558922558922556,
        )
        self.assertAlmostEqual(
            Jaccard(alphabet='abcdefghijklmnop', qval=range(2, 4)).sim(
                'abc', 'abcd'
            ),
            0.42857142857142855,
        )
        self.assertAlmostEqual(
            Jaccard(
                alphabet='abcdefghijklmnop', tokenizer=WhitespaceTokenizer()
            ).sim('abc', 'abcd'),
            0.0,
        )
        self.assertAlmostEqual(
            Jaccard(alphabet=list('abcdefghijklmnop')).sim('abc', 'abcd'), 0.5
        )
        self.assertAlmostEqual(
            Jaccard(tokenizer=CharacterTokenizer()).sim('abc', 'abcd'), 0.75
        )

        cmp_j_soft = Jaccard(intersection_type='soft')
        self.assertEqual(cmp_j_soft._src_card(), 0)  # noqa: SF01
        self.assertEqual(cmp_j_soft._tar_card(), 0)  # noqa: SF01
        self.assertEqual(cmp_j_soft._src_only(), Counter())  # noqa: SF01
        self.assertEqual(cmp_j_soft._tar_only(), Counter())  # noqa: SF01
        self.assertEqual(cmp_j_soft._total(), Counter())  # noqa: SF01
        self.assertEqual(cmp_j_soft._union(), Counter())  # noqa: SF01
        self.assertEqual(cmp_j_soft._difference(), Counter())  # noqa: SF01
        cmp_j_soft.sim('abcd', 'abcde')
        self.assertEqual(cmp_j_soft._src_card(), 5)  # noqa: SF01
        self.assertEqual(cmp_j_soft._tar_card(), 6)  # noqa: SF01
        self.assertEqual(
            cmp_j_soft._src_only(), Counter({'#': 0.5})  # noqa: SF01
        )
        self.assertEqual(
            cmp_j_soft._tar_only(), Counter({'e#': 1, 'e': 0.5})  # noqa: SF01
        )
        self.assertEqual(
            cmp_j_soft._total(),  # noqa: SF01
            Counter(
                {
                    'e#': 1,
                    'e': 0.5,
                    '#': 0.5,
                    '$a': 2,
                    'ab': 2,
                    'bc': 2,
                    'cd': 2,
                    'd': 1.0,
                }
            ),
        )
        self.assertEqual(
            cmp_j_soft._union(),  # noqa: SF01
            Counter(
                {
                    'e#': 1,
                    'e': 0.5,
                    '#': 0.5,
                    '$a': 1,
                    'ab': 1,
                    'bc': 1,
                    'cd': 1,
                    'd': 0.5,
                }
            ),
        )
        self.assertEqual(
            cmp_j_soft._difference(),  # noqa: SF01
            Counter({'#': 0.5, 'e#': -1, 'e': -0.5}),
        )


if __name__ == '__main__':
    unittest.main()
