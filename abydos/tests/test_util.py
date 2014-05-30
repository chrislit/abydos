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
from abydos.util import qgrams, _qgram_lists, _qgram_counts


# pylint: disable=R0904
# pylint: disable=R0915
class QgramTestCases(unittest.TestCase):
    """test cases for abydos.utils functions relating to q-grams
    """
    def test_qgrams(self):
        """test abydos.util.qgrams
        """
        self.assertEqual(qgrams(''), [])
        self.assertEqual(qgrams('NELSON', 3), ['$$N', '$NE', 'NEL', 'ELS',
                                                'LSO', 'SON', 'ON#', 'N##'])
        self.assertEqual(qgrams('NELSON', 7), [])

        #http://www.sound-ex.com/alternative_qgram.htm
        self.assertEqual(qgrams('NELSON'),
                          ['$N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#'])
        self.assertEqual(qgrams('NEILSEN'),
                          ['$N', 'NE', 'EI', 'IL', 'LS', 'SE', 'EN', 'N#'])
        self.assertEqual(qgrams('NELSON', start_stop=''),
                          ['NE', 'EL', 'LS', 'SO', 'ON'])
        self.assertEqual(qgrams('NEILSEN', start_stop=''),
                          ['NE', 'EI', 'IL', 'LS', 'SE', 'EN'])

    def test_qgram_lists(self):
        """test abydos.util._qgrams_lists
        """
        self.assertEqual(_qgram_lists('NELSON', ''),
                          (['$N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#'], [], []))
        self.assertEqual(_qgram_lists('', 'NEILSEN'),
                          ([], ['$N', 'NE', 'EI', 'IL', 'LS',
                                'SE', 'EN', 'N#'], []))
        self.assertEqual(_qgram_lists('NELSON', 'NEILSEN'),
                          (['$N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#'],
                           ['$N', 'NE', 'EI', 'IL', 'LS', 'SE', 'EN', 'N#'],
                           ['$N', 'NE', 'LS', 'N#']))
        self.assertEqual(_qgram_lists('NELSON', 'NOSLEN'),
                          (['$N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#'],
                           ['$N', 'NO', 'OS', 'SL', 'LE', 'EN', 'N#'],
                           ['$N', 'N#']))
        self.assertEqual(_qgram_lists('NAIL', 'LIAN'),
                          (['$N', 'NA', 'AI', 'IL', 'L#'],
                           ['$L', 'LI', 'IA', 'AN', 'N#'],
                           []))

        self.assertEqual(_qgram_lists('NELSON', 'NEILSEN', start_stop=''),
                          (['NE', 'EL', 'LS', 'SO', 'ON'],
                           ['NE', 'EI', 'IL', 'LS', 'SE', 'EN'],
                           ['NE', 'LS']))
        self.assertEqual(_qgram_lists('NELSON', 'NOSLEN', start_stop=''),
                          (['NE', 'EL', 'LS', 'SO', 'ON'],
                           ['NO', 'OS', 'SL', 'LE', 'EN'],
                           []))
        self.assertEqual(_qgram_lists('NAIL', 'LIAN', start_stop=''),
                          (['NA', 'AI', 'IL'],
                           ['LI', 'IA', 'AN'],
                           []))

    def test_qgram_counts(self):
        """test abydos.util._qgrams_counts
        """
        self.assertEqual(_qgram_counts('NELSON', ''), (7, 0, 0))
        self.assertEqual(_qgram_counts('', 'NEILSEN'), (0, 8, 0))
        self.assertEqual(_qgram_counts('NELSON', 'NEILSEN'), (7, 8, 4))
        self.assertEqual(_qgram_counts('NELSON', 'NOSLEN'), (7, 7, 2))
        self.assertEqual(_qgram_counts('NAIL', 'LIAN'), (5, 5, 0))
        self.assertEqual(_qgram_counts('NELSON', 'NEILSEN', start_stop=''),
                          (5, 6, 2))
        self.assertEqual(_qgram_counts('NELSON', 'NOSLEN', start_stop=''),
                          (5, 5, 0))
        self.assertEqual(_qgram_counts('NAIL', 'LIAN', start_stop=''),
                          (3, 3, 0))


if __name__ == '__main__':
    unittest.main()
