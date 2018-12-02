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

"""abydos.tests.tokenizer.test_tokenizer_qgrams.

This module contains unit tests for abydos.tokenizer.QGrams
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.tokenizer import QGrams


class QGramsTestCases(unittest.TestCase):
    """Test abydos.tokenizer.QGrams."""

    def test_qgrams(self):
        """Test abydos.tokenizer.QGrams."""
        self.assertEqual(sorted(QGrams().tokenize('').get_list()), [])
        self.assertEqual(sorted(QGrams(2).tokenize('a').get_list()), [])
        self.assertEqual(sorted(QGrams(0).tokenize('NELSON').get_list()), [])
        self.assertEqual(sorted(QGrams(-1).tokenize('NELSON').get_list()), [])

        self.assertEqual(
            sorted(QGrams(3).tokenize('NELSON').get_list()),
            sorted(['$$N', '$NE', 'NEL', 'ELS', 'LSO', 'SON', 'ON#', 'N##']),
        )
        self.assertEqual(
            sorted(QGrams(7).tokenize('NELSON').get_list()), sorted([])
        )

        # http://www.sound-ex.com/alternative_qgram.htm
        self.assertEqual(
            sorted(QGrams().tokenize('NELSON').get_list()),
            sorted(['$N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#']),
        )
        self.assertEqual(
            sorted(QGrams().tokenize('NEILSEN').get_list()),
            sorted(['$N', 'NE', 'EI', 'IL', 'LS', 'SE', 'EN', 'N#']),
        )
        self.assertEqual(
            sorted(QGrams(start_stop='').tokenize('NELSON').get_list()),
            sorted(['NE', 'EL', 'LS', 'SO', 'ON']),
        )
        self.assertEqual(
            sorted(QGrams(start_stop='').tokenize('NEILSEN').get_list()),
            sorted(['NE', 'EI', 'IL', 'LS', 'SE', 'EN']),
        )

        # qval=(1,2)
        self.assertEqual(
            sorted(QGrams(qval=(1, 2)).tokenize('NELSON').get_list()),
            sorted(
                [
                    '$N',
                    'E',
                    'EL',
                    'L',
                    'LS',
                    'N',
                    'N',
                    'N#',
                    'NE',
                    'O',
                    'ON',
                    'S',
                    'SO',
                ]
            ),
        )
        self.assertEqual(
            sorted(QGrams(qval=(2, 1)).tokenize('NELSON').get_list()),
            sorted(
                [
                    '$N',
                    'E',
                    'EL',
                    'L',
                    'LS',
                    'N',
                    'N',
                    'N#',
                    'NE',
                    'O',
                    'ON',
                    'S',
                    'SO',
                ]
            ),
        )
        self.assertEqual(
            sorted(QGrams(qval=range(3)).tokenize('NELSON').get_list()),
            sorted(
                [
                    '$N',
                    'E',
                    'EL',
                    'L',
                    'LS',
                    'N',
                    'N',
                    'N#',
                    'NE',
                    'O',
                    'ON',
                    'S',
                    'SO',
                ]
            ),
        )
        self.assertEqual(QGrams(qval=(1, 2)).tokenize('NELSON').count(), 13)

        # skip=(1,2)
        self.assertEqual(
            sorted(QGrams(skip=(2, 1, 0)).tokenize('NELSON').get_list()),
            sorted(
                [
                    '$E',
                    '$L',
                    '$N',
                    'EL',
                    'EO',
                    'ES',
                    'LN',
                    'LO',
                    'LS',
                    'N',
                    'N',
                    'N#',
                    'NE',
                    'NL',
                    'NS',
                    'O',
                    'O#',
                    'ON',
                    'S#',
                    'SN',
                    'SO',
                ]
            ),
        )
        self.assertEqual(
            sorted(QGrams(skip=(2, 1, 0)).tokenize('NELSON').get_list()),
            sorted(
                [
                    '$E',
                    '$L',
                    '$N',
                    'EL',
                    'EO',
                    'ES',
                    'LN',
                    'LO',
                    'LS',
                    'N',
                    'N',
                    'N#',
                    'NE',
                    'NL',
                    'NS',
                    'O',
                    'O#',
                    'ON',
                    'S#',
                    'SN',
                    'SO',
                ]
            ),
        )
        self.assertEqual(
            sorted(QGrams(skip=range(3)).tokenize('NELSON').get_list()),
            sorted(
                [
                    '$E',
                    '$L',
                    '$N',
                    'EL',
                    'EO',
                    'ES',
                    'LN',
                    'LO',
                    'LS',
                    'N',
                    'N',
                    'N#',
                    'NE',
                    'NL',
                    'NS',
                    'O',
                    'O#',
                    'ON',
                    'S#',
                    'SN',
                    'SO',
                ]
            ),
        )
        self.assertEqual(QGrams(skip=(0, 1, 2)).tokenize('NELSON').count(), 21)

    def test_qgram_intersections(self):
        """Test abydos.tokenizer.QGrams intersections."""
        self.assertEqual(
            sorted(QGrams().tokenize('NELSON') & QGrams().tokenize('')), []
        )
        self.assertEqual(
            sorted(QGrams().tokenize('') & QGrams().tokenize('NEILSEN')), []
        )
        self.assertEqual(
            sorted(QGrams().tokenize('NELSON') & QGrams().tokenize('NEILSEN')),
            sorted(['$N', 'NE', 'LS', 'N#']),
        )
        self.assertEqual(
            sorted(QGrams().tokenize('NELSON') & QGrams().tokenize('NOSLEN')),
            sorted(['$N', 'N#']),
        )
        self.assertEqual(
            sorted(QGrams().tokenize('NAIL') & QGrams().tokenize('LIAN')), []
        )

        self.assertEqual(
            sorted(
                QGrams(start_stop='').tokenize('NELSON')
                & QGrams(start_stop='').tokenize('NEILSEN')
            ),
            sorted(['NE', 'LS']),
        )
        self.assertEqual(
            sorted(
                QGrams(start_stop='').tokenize('NELSON')
                & QGrams(start_stop='').tokenize('NOSLEN')
            ),
            [],
        )
        self.assertEqual(
            sorted(
                QGrams(start_stop='').tokenize('NAIL')
                & QGrams(start_stop='').tokenize('LIAN')
            ),
            [],
        )

    def test_qgram_counts(self):
        """Test abydos.tokenizer.QGrams counts."""
        self.assertEqual(QGrams().tokenize('').count(), 0)
        self.assertEqual(len(QGrams().tokenize('').get_list()), 0)

        self.assertEqual(QGrams().tokenize('NEILSEN').count(), 8)
        self.assertEqual(QGrams().tokenize('NELSON').count(), 7)
        self.assertEqual(QGrams(start_stop='').tokenize('NEILSEN').count(), 6)
        self.assertEqual(QGrams(start_stop='').tokenize('NELSON').count(), 5)

        self.assertEqual(len(QGrams().tokenize('NEILSEN').get_list()), 8)
        self.assertEqual(len(QGrams().tokenize('NELSON').get_list()), 7)
        self.assertEqual(
            len(QGrams(start_stop='').tokenize('NEILSEN').get_list()), 6
        )
        self.assertEqual(
            len(QGrams(start_stop='').tokenize('NELSON').get_list()), 5
        )


if __name__ == '__main__':
    unittest.main()
