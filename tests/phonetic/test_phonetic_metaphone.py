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

"""abydos.tests.phonetic.test_phonetic_metaphone.

This module contains unit tests for abydos.phonetic.Metaphone
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import Metaphone, metaphone


class MetaphoneTestCases(unittest.TestCase):
    """Test Metaphone functions.

    test cases for abydos.phonetic.Metaphone
    """

    pa = Metaphone()

    def test_metaphone(self):
        """Test abydos.phonetic.Metaphone."""
        self.assertEqual(self.pa.encode(''), '')
        self.assertEqual(self.pa.encode('...'), '')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(self.pa.encode('Fishpool', 4), 'FXPL')
        self.assertEqual(self.pa.encode('Fishpoole', 4), 'FXPL')
        self.assertEqual(self.pa.encode('Gellately', 4), 'JLTL')
        self.assertEqual(self.pa.encode('Gelletly', 4), 'JLTL')
        self.assertEqual(self.pa.encode('Lowers', 4), 'LWRS')
        self.assertEqual(self.pa.encode('Lowerson', 4), 'LWRS')
        self.assertEqual(self.pa.encode('Mallabar', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Melbert', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Melbourn', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Melbourne', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Melburg', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Melbury', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Milberry', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Milborn', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Milbourn', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Milbourne', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Milburn', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Milburne', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Millberg', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Mulberry', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Mulbery', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Mulbry', 4), 'MLBR')
        self.assertEqual(self.pa.encode('Saipy', 4), 'SP')
        self.assertEqual(self.pa.encode('Sapey', 4), 'SP')
        self.assertEqual(self.pa.encode('Sapp', 4), 'SP')
        self.assertEqual(self.pa.encode('Sappy', 4), 'SP')
        self.assertEqual(self.pa.encode('Sepey', 4), 'SP')
        self.assertEqual(self.pa.encode('Seppey', 4), 'SP')
        self.assertEqual(self.pa.encode('Sopp', 4), 'SP')
        self.assertEqual(self.pa.encode('Zoppie', 4), 'SP')
        self.assertEqual(self.pa.encode('Zoppo', 4), 'SP')
        self.assertEqual(self.pa.encode('Zupa', 4), 'SP')
        self.assertEqual(self.pa.encode('Zupo', 4), 'SP')
        self.assertEqual(self.pa.encode('Zuppa', 4), 'SP')

        # assorted tests to complete code coverage
        self.assertEqual(self.pa.encode('Xavier'), 'SFR')
        self.assertEqual(self.pa.encode('Acacia'), 'AKX')
        self.assertEqual(self.pa.encode('Schuler'), 'SKLR')
        self.assertEqual(self.pa.encode('Sign'), 'SN')
        self.assertEqual(self.pa.encode('Signed'), 'SNT')
        self.assertEqual(self.pa.encode('Horatio'), 'HRX')
        self.assertEqual(self.pa.encode('Ignatio'), 'IKNX')
        self.assertEqual(self.pa.encode('Lucretia'), 'LKRX')

        # assorted tests to complete branch coverage
        self.assertEqual(self.pa.encode('Lamb'), 'LM')
        self.assertEqual(self.pa.encode('science'), 'SNS')

        # max_length bounds tests
        self.assertEqual(self.pa.encode('Niall', max_length=-1), 'NL')
        self.assertEqual(self.pa.encode('Niall', max_length=0), 'NL')

        # Test wrapper
        self.assertEqual(metaphone('Xavier'), 'SFR')


if __name__ == '__main__':
    unittest.main()
