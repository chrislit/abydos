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
    pa4 = Metaphone(4)

    def test_metaphone(self):
        """Test abydos.phonetic.Metaphone."""
        self.assertEqual(self.pa.encode(''), '')
        self.assertEqual(self.pa.encode('...'), '')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(self.pa4.encode('Fishpool'), 'FXPL')
        self.assertEqual(self.pa4.encode('Fishpoole'), 'FXPL')
        self.assertEqual(self.pa4.encode('Gellately'), 'JLTL')
        self.assertEqual(self.pa4.encode('Gelletly'), 'JLTL')
        self.assertEqual(self.pa4.encode('Lowers'), 'LWRS')
        self.assertEqual(self.pa4.encode('Lowerson'), 'LWRS')
        self.assertEqual(self.pa4.encode('Mallabar'), 'MLBR')
        self.assertEqual(self.pa4.encode('Melbert'), 'MLBR')
        self.assertEqual(self.pa4.encode('Melbourn'), 'MLBR')
        self.assertEqual(self.pa4.encode('Melbourne'), 'MLBR')
        self.assertEqual(self.pa4.encode('Melburg'), 'MLBR')
        self.assertEqual(self.pa4.encode('Melbury'), 'MLBR')
        self.assertEqual(self.pa4.encode('Milberry'), 'MLBR')
        self.assertEqual(self.pa4.encode('Milborn'), 'MLBR')
        self.assertEqual(self.pa4.encode('Milbourn'), 'MLBR')
        self.assertEqual(self.pa4.encode('Milbourne'), 'MLBR')
        self.assertEqual(self.pa4.encode('Milburn'), 'MLBR')
        self.assertEqual(self.pa4.encode('Milburne'), 'MLBR')
        self.assertEqual(self.pa4.encode('Millberg'), 'MLBR')
        self.assertEqual(self.pa4.encode('Mulberry'), 'MLBR')
        self.assertEqual(self.pa4.encode('Mulbery'), 'MLBR')
        self.assertEqual(self.pa4.encode('Mulbry'), 'MLBR')
        self.assertEqual(self.pa4.encode('Saipy'), 'SP')
        self.assertEqual(self.pa4.encode('Sapey'), 'SP')
        self.assertEqual(self.pa4.encode('Sapp'), 'SP')
        self.assertEqual(self.pa4.encode('Sappy'), 'SP')
        self.assertEqual(self.pa4.encode('Sepey'), 'SP')
        self.assertEqual(self.pa4.encode('Seppey'), 'SP')
        self.assertEqual(self.pa4.encode('Sopp'), 'SP')
        self.assertEqual(self.pa4.encode('Zoppie'), 'SP')
        self.assertEqual(self.pa4.encode('Zoppo'), 'SP')
        self.assertEqual(self.pa4.encode('Zupa'), 'SP')
        self.assertEqual(self.pa4.encode('Zupo'), 'SP')
        self.assertEqual(self.pa4.encode('Zuppa'), 'SP')

        # assorted tests to complete code coverage
        self.assertEqual(self.pa.encode('Xavier'), 'SFR')
        self.assertEqual(self.pa.encode('Acacia'), 'AKX')
        self.assertEqual(self.pa.encode('Schuler'), 'SKLR')
        self.assertEqual(self.pa.encode('Sign'), 'SN')
        self.assertEqual(self.pa.encode('Signed'), 'SNT')
        self.assertEqual(self.pa.encode('Horatio'), 'HRX')
        self.assertEqual(self.pa.encode('Ignatio'), 'IKNX')
        self.assertEqual(self.pa.encode('Lucretia'), 'LKRX')
        self.assertEqual(self.pa.encode('Wright'), 'RKT')
        self.assertEqual(self.pa.encode('White'), 'WT')
        self.assertEqual(self.pa.encode('Black'), 'BLK')
        self.assertEqual(self.pa.encode('Chance'), 'XNS')
        self.assertEqual(self.pa.encode('Dgengo'), 'JJNK')
        self.assertEqual(self.pa.encode('Ghost'), 'ST')
        self.assertEqual(self.pa.encode('Qing'), 'KNK')
        self.assertEqual(self.pa.encode('Asia'), 'AX')
        self.assertEqual(self.pa.encode('Ax'), 'AKS')
        self.assertEqual(self.pa.encode('Thegn'), '0N')
        self.assertEqual(self.pa.encode('acknowledged'), 'AKNLJT')
        self.assertEqual(self.pa.encode('awkward'), 'AKWRT')
        self.assertEqual(self.pa.encode('admitted'), 'ATMTT')
        self.assertEqual(self.pa.encode('dahl'), 'TL')
        self.assertEqual(self.pa.encode('autobiography'), 'ATBKRF')
        self.assertEqual(self.pa.encode('exaggerate'), 'EKSKRT')
        self.assertEqual(self.pa.encode('pitch'), 'PX')
        self.assertEqual(self.pa.encode('chracter'), 'KRKTR')

        # assorted tests to complete branch coverage
        self.assertEqual(self.pa.encode('Lamb'), 'LM')
        self.assertEqual(self.pa.encode('science'), 'SNS')

        # max_length bounds tests
        self.assertEqual(Metaphone(max_length=-1).encode('Niall'), 'NL')
        self.assertEqual(Metaphone(max_length=0).encode('Niall'), 'NL')

        # Test wrapper
        self.assertEqual(metaphone('Xavier'), 'SFR')


if __name__ == '__main__':
    unittest.main()
