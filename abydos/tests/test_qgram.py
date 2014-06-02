# -*- coding: utf-8 -*-
"""abydos.tests.test_util

This module contains unit tests for abydos.util

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
import unittest
from abydos.qgram import QGrams

class QgramTestCases(unittest.TestCase):
    """test cases for abydos.utils functions relating to q-grams
    """
    def test_qgrams(self):
        """test abydos.util.qgrams
        """
        self.assertEqual(sorted(QGrams('').elements()), [])
        self.assertEqual(sorted(QGrams('NELSON', 3).elements()),
                         sorted(['$$N', '$NE', 'NEL', 'ELS', 'LSO', 'SON',
                                 'ON#', 'N##']))
        self.assertEqual(sorted(QGrams('NELSON', 7).elements()), sorted([]))

        #http://www.sound-ex.com/alternative_qgram.htm
        self.assertEqual(sorted(QGrams('NELSON').elements()),
                          sorted(['$N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#']))
        self.assertEqual(sorted(QGrams('NEILSEN').elements()),
                          sorted(['$N', 'NE', 'EI', 'IL', 'LS', 'SE', 'EN',
                                  'N#']))
        self.assertEqual(sorted(QGrams('NELSON', start_stop='').elements()),
                          sorted(['NE', 'EL', 'LS', 'SO', 'ON']))
        self.assertEqual(sorted(QGrams('NEILSEN', start_stop='').elements()),
                          sorted(['NE', 'EI', 'IL', 'LS', 'SE', 'EN']))

    def test_qgram_intersections(self):
        """test abydos.util._qgrams_lists
        """
        self.assertEqual(sorted(QGrams('NELSON') & QGrams('')), [])
        self.assertEqual(sorted(QGrams('') & QGrams('NEILSEN')), [])
        self.assertEqual(sorted(QGrams('NELSON') & QGrams('NEILSEN')),
                         sorted(['$N', 'NE', 'LS', 'N#']))
        self.assertEqual(sorted(QGrams('NELSON') & QGrams('NOSLEN')),
                         sorted(['$N', 'N#']))
        self.assertEqual(sorted(QGrams('NAIL') & QGrams('LIAN')), [])

        self.assertEqual(sorted(QGrams('NELSON', start_stop='') &
                                QGrams('NEILSEN', start_stop='')),
                         sorted(['NE', 'LS']))
        self.assertEqual(sorted(QGrams('NELSON', start_stop='') &
                                QGrams('NOSLEN', start_stop='')), [])
        self.assertEqual(sorted(QGrams('NAIL', start_stop='') &
                                QGrams('LIAN', start_stop='')), [])

    def test_qgram_counts(self):
        """test abydos.util._qgrams_counts
        """
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
