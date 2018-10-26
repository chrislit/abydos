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

"""abydos.tests.tokenizer.test_tokenizer_qgram.

This module contains unit tests for abydos.tokenizer.qgram
"""

from __future__ import unicode_literals

import unittest

from abydos.tokenizer.qgram import QGrams


class QgramTestCases(unittest.TestCase):
    """Test abydos.tokenizer.qgram."""

    def test_qgrams(self):
        """Test abydos.tokenizer.qgram.QGrams."""
        self.assertEqual(sorted(QGrams('').elements()), [])
        self.assertEqual(sorted(QGrams('a', 2).elements()), [])
        self.assertEqual(sorted(QGrams('NELSON', 0).elements()), [])
        self.assertEqual(sorted(QGrams('NELSON', -1).elements()), [])

        self.assertEqual(
            sorted(QGrams('NELSON', 3).elements()),
            sorted(['$$N', '$NE', 'NEL', 'ELS', 'LSO', 'SON', 'ON#', 'N##']),
        )
        self.assertEqual(sorted(QGrams('NELSON', 7).elements()), sorted([]))

        # http://www.sound-ex.com/alternative_qgram.htm
        self.assertEqual(
            sorted(QGrams('NELSON').elements()),
            sorted(['$N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#']),
        )
        self.assertEqual(
            sorted(QGrams('NEILSEN').elements()),
            sorted(['$N', 'NE', 'EI', 'IL', 'LS', 'SE', 'EN', 'N#']),
        )
        self.assertEqual(
            sorted(QGrams('NELSON', start_stop='').elements()),
            sorted(['NE', 'EL', 'LS', 'SO', 'ON']),
        )
        self.assertEqual(
            sorted(QGrams('NEILSEN', start_stop='').elements()),
            sorted(['NE', 'EI', 'IL', 'LS', 'SE', 'EN']),
        )

        # qval=(1,2)
        self.assertEqual(
            sorted(QGrams('NELSON', qval=(1, 2)).elements()),
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
            sorted(QGrams('NELSON', qval=(2, 1)).elements()),
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
            sorted(QGrams('NELSON', qval=range(3)).elements()),
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
        self.assertEqual(QGrams('NELSON', qval=(1, 2)).count(), 13)

        # skip=(1,2)
        self.assertEqual(
            sorted(QGrams('NELSON', skip=(2, 1, 0)).elements()),
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
            sorted(QGrams('NELSON', skip=(2, 1, 0)).elements()),
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
            sorted(QGrams('NELSON', skip=range(3)).elements()),
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
        self.assertEqual(QGrams('NELSON', skip=(0, 1, 2)).count(), 21)

    def test_qgram_intersections(self):
        """Test abydos.tokenizer.qgram.QGrams intersections."""
        self.assertEqual(sorted(QGrams('NELSON') & QGrams('')), [])
        self.assertEqual(sorted(QGrams('') & QGrams('NEILSEN')), [])
        self.assertEqual(
            sorted(QGrams('NELSON') & QGrams('NEILSEN')),
            sorted(['$N', 'NE', 'LS', 'N#']),
        )
        self.assertEqual(
            sorted(QGrams('NELSON') & QGrams('NOSLEN')), sorted(['$N', 'N#'])
        )
        self.assertEqual(sorted(QGrams('NAIL') & QGrams('LIAN')), [])

        self.assertEqual(
            sorted(
                QGrams('NELSON', start_stop='')
                & QGrams('NEILSEN', start_stop='')
            ),
            sorted(['NE', 'LS']),
        )
        self.assertEqual(
            sorted(
                QGrams('NELSON', start_stop='')
                & QGrams('NOSLEN', start_stop='')
            ),
            [],
        )
        self.assertEqual(
            sorted(
                QGrams('NAIL', start_stop='') & QGrams('LIAN', start_stop='')
            ),
            [],
        )

    def test_qgram_counts(self):
        """Test abydos.tokenizer.qgram.QGrams counts."""
        self.assertEqual(QGrams('').count(), 0)
        self.assertEqual(len(QGrams('').ordered_list), 0)

        self.assertEqual(QGrams('NEILSEN').count(), 8)
        self.assertEqual(QGrams('NELSON').count(), 7)
        self.assertEqual(QGrams('NEILSEN', start_stop='').count(), 6)
        self.assertEqual(QGrams('NELSON', start_stop='').count(), 5)

        self.assertEqual(len(QGrams('NEILSEN').ordered_list), 8)
        self.assertEqual(len(QGrams('NELSON').ordered_list), 7)
        self.assertEqual(len(QGrams('NEILSEN', start_stop='').ordered_list), 6)
        self.assertEqual(len(QGrams('NELSON', start_stop='').ordered_list), 5)


if __name__ == '__main__':
    unittest.main()
