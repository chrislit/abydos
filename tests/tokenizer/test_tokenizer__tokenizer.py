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

"""abydos.tests.tokenizer.test_tokenizer_tokenizer.

This module contains unit tests for abydos.tokenizer._Tokenizer
"""

import sys
import unittest
from collections import Counter
from math import log1p

from abydos.tokenizer import QGrams, QSkipgrams, _Tokenizer


class TokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer._Tokenizer."""

    def test__tokenizer(self):
        """Test abydos.tokenizer._Tokenizer."""
        self.assertEqual(
            _Tokenizer().tokenize('').get_counter(), Counter({'': 1})
        )
        self.assertEqual(
            _Tokenizer().tokenize('a').get_counter(), Counter({'a': 1})
        )

        self.assertEqual(
            _Tokenizer().tokenize('NELSON').get_counter(),
            Counter({'NELSON': 1}),
        )
        self.assertEqual(
            _Tokenizer().tokenize('NEILSEN').get_counter(),
            Counter({'NEILSEN': 1}),
        )
        self.assertEqual(_Tokenizer().tokenize('NEILSEN').count(), 1)
        self.assertEqual(_Tokenizer().tokenize('NEILSEN').count_unique(), 1)

        tweet = 'Good to be home for a night'
        self.assertEqual(
            _Tokenizer().tokenize(tweet).get_counter(),
            Counter({'Good to be home for a night': 1}),
        )

        nelson = QGrams().tokenize('NELSON')
        neilsen = QGrams().tokenize('NEILSEN')
        self.assertEqual(
            nelson.get_set(), {'$N', 'EL', 'LS', 'N#', 'NE', 'ON', 'SO'}
        )
        self.assertEqual(
            nelson.get_list(), ['$N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#']
        )
        if sys.version_info >= (3, 6):
            self.assertEqual(
                repr(nelson),
                "QGrams({'$N': 1, 'NE': 1, 'EL': 1, 'LS': 1, 'SO': 1, 'ON': 1, \
'N#': 1})",
            )
        self.assertEqual(
            nelson & neilsen, Counter({'$N': 1, 'NE': 1, 'LS': 1, 'N#': 1})
        )
        self.assertEqual(
            nelson + neilsen,
            Counter(
                {
                    '$N': 2,
                    'NE': 2,
                    'EL': 1,
                    'LS': 2,
                    'SO': 1,
                    'ON': 1,
                    'N#': 2,
                    'EI': 1,
                    'IL': 1,
                    'SE': 1,
                    'EN': 1,
                }
            ),
        )
        self.assertEqual(
            nelson - neilsen, Counter({'EL': 1, 'SO': 1, 'ON': 1})
        )

        nelsonnelson = QGrams(scaler='set').tokenize('NELSONNELSON')
        self.assertEqual(nelsonnelson.count(), 8)

        nelson_ssk = QSkipgrams(scaler='SSK').tokenize('NELSON')
        self.assertAlmostEqual(nelson_ssk.count(), 18.66784401)

        nelson_log = QSkipgrams(qval=3, scaler=log1p).tokenize('NELSON')
        gold_standard = Counter(
            {
                '$$N': 1.0986122886681096,
                '$$E': 0.6931471805599453,
                '$$L': 0.6931471805599453,
                '$$S': 0.6931471805599453,
                '$$O': 0.6931471805599453,
                '$$#': 1.0986122886681096,
                '$NE': 1.0986122886681096,
                '$NL': 1.0986122886681096,
                '$NS': 1.0986122886681096,
                '$NO': 1.0986122886681096,
                '$NN': 1.0986122886681096,
                '$N#': 2.1972245773362196,
                '$EL': 1.0986122886681096,
                '$ES': 1.0986122886681096,
                '$EO': 1.0986122886681096,
                '$EN': 1.0986122886681096,
                '$E#': 1.6094379124341003,
                '$LS': 1.0986122886681096,
                '$LO': 1.0986122886681096,
                '$LN': 1.0986122886681096,
                '$L#': 1.6094379124341003,
                '$SO': 1.0986122886681096,
                '$SN': 1.0986122886681096,
                '$S#': 1.6094379124341003,
                '$ON': 1.0986122886681096,
                '$O#': 1.6094379124341003,
                '$##': 1.0986122886681096,
                'NEL': 0.6931471805599453,
                'NES': 0.6931471805599453,
                'NEO': 0.6931471805599453,
                'NEN': 0.6931471805599453,
                'NE#': 1.0986122886681096,
                'NLS': 0.6931471805599453,
                'NLO': 0.6931471805599453,
                'NLN': 0.6931471805599453,
                'NL#': 1.0986122886681096,
                'NSO': 0.6931471805599453,
                'NSN': 0.6931471805599453,
                'NS#': 1.0986122886681096,
                'NON': 0.6931471805599453,
                'NO#': 1.0986122886681096,
                'NN#': 1.0986122886681096,
                'N##': 1.0986122886681096,
                'ELS': 0.6931471805599453,
                'ELO': 0.6931471805599453,
                'ELN': 0.6931471805599453,
                'EL#': 1.0986122886681096,
                'ESO': 0.6931471805599453,
                'ESN': 0.6931471805599453,
                'ES#': 1.0986122886681096,
                'EON': 0.6931471805599453,
                'EO#': 1.0986122886681096,
                'EN#': 1.0986122886681096,
                'E##': 0.6931471805599453,
                'LSO': 0.6931471805599453,
                'LSN': 0.6931471805599453,
                'LS#': 1.0986122886681096,
                'LON': 0.6931471805599453,
                'LO#': 1.0986122886681096,
                'LN#': 1.0986122886681096,
                'L##': 0.6931471805599453,
                'SON': 0.6931471805599453,
                'SO#': 1.0986122886681096,
                'SN#': 1.0986122886681096,
                'S##': 0.6931471805599453,
                'ON#': 1.0986122886681096,
                'O##': 0.6931471805599453,
            }
        )
        test_counter = nelson_log.get_counter()
        for key in test_counter:
            self.assertAlmostEqual(test_counter[key], gold_standard[key])

        nelson_entropy = QSkipgrams(scaler='entropy').tokenize('NELSON')
        self.assertAlmostEqual(nelson_entropy.count(), 4.6644977792)


if __name__ == '__main__':
    unittest.main()
