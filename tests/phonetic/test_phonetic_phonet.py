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

"""abydos.tests.phonetic.test_phonetic_phonet.

This module contains unit tests for abydos.phonetic.Phonet
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import codecs
import unittest

from abydos.phonetic import Phonet, phonet

from .. import ALLOW_RANDOM, _corpus_file, _one_in


class PhonetTestCases(unittest.TestCase):
    """Test Phonet functions.

    test cases for abydos.phonetic.Phonet
    """

    pa = Phonet()

    def test_phonet_german(self):
        """Test abydos.phonetic.Phonet (German)."""
        self.assertEqual(self.pa.encode(''), '')

        # https://code.google.com/p/phonet4java/source/browse/trunk/src/test/java/com/googlecode/phonet4java/Phonet1Test.java
        self.assertEqual(self.pa.encode('', 1), '')
        self.assertEqual(self.pa.encode('Zedlitz', 1), 'ZETLIZ')
        self.assertEqual(self.pa.encode('Bremerhaven', 1), 'BREMAHAFN')
        self.assertEqual(self.pa.encode('Hamburger Hafen', 1), 'HAMBURGA HAFN')
        self.assertEqual(self.pa.encode('Jesper', 1), 'IESPA')
        self.assertEqual(self.pa.encode('elisabeth', 1), 'ELISABET')
        self.assertEqual(self.pa.encode('elisabet', 1), 'ELISABET')
        self.assertEqual(self.pa.encode('Ziegler', 1), 'ZIKLA')
        self.assertEqual(self.pa.encode('Scherer', 1), 'SHERA')
        self.assertEqual(self.pa.encode('Bartels', 1), 'BARTLS')
        self.assertEqual(self.pa.encode('Jansen', 1), 'IANSN')
        self.assertEqual(self.pa.encode('Sievers', 1), 'SIWAS')
        self.assertEqual(self.pa.encode('Michels', 1), 'MICHLS')
        self.assertEqual(self.pa.encode('Ewers', 1), 'EWERS')
        self.assertEqual(self.pa.encode('Evers', 1), 'EWERS')
        self.assertEqual(self.pa.encode('Wessels', 1), 'WESLS')
        self.assertEqual(self.pa.encode('Gottschalk', 1), 'GOSHALK')
        self.assertEqual(self.pa.encode('Brückmann', 1), 'BRÜKMAN')
        self.assertEqual(self.pa.encode('Blechschmidt', 1), 'BLECHSHMIT')
        self.assertEqual(self.pa.encode('Kolodziej', 1), 'KOLOTZI')
        self.assertEqual(self.pa.encode('Krauße', 1), 'KRAUSE')
        self.assertEqual(self.pa.encode('Cachel', 1), 'KESHL')

        self.assertEqual(self.pa.encode('', 2), '')
        self.assertEqual(self.pa.encode('Zedlitz', 2), 'ZETLIZ')
        self.assertEqual(self.pa.encode('Bremerhaven', 2), 'BRENAFN')
        self.assertEqual(self.pa.encode('Schönberg', 2), 'ZÖNBAK')
        self.assertEqual(self.pa.encode('Hamburger Hafen', 2), 'ANBURKA AFN')
        self.assertEqual(self.pa.encode('Ziegler', 2), 'ZIKLA')
        self.assertEqual(self.pa.encode('Scherer', 2), 'ZERA')
        self.assertEqual(self.pa.encode('Jansen', 2), 'IANZN')
        self.assertEqual(self.pa.encode('Eberhardt', 2), 'EBART')
        self.assertEqual(self.pa.encode('Gottschalk', 2), 'KUZALK')
        self.assertEqual(self.pa.encode('Brückmann', 2), 'BRIKNAN')
        self.assertEqual(self.pa.encode('Blechschmidt', 2), 'BLEKZNIT')
        self.assertEqual(self.pa.encode('Kolodziej', 2), 'KULUTZI')
        self.assertEqual(self.pa.encode('Krauße', 2), 'KRAUZE')

        # etc. (for code coverage)
        self.assertEqual(self.pa.encode('Jesper', 1), 'IESPA')
        self.assertEqual(self.pa.encode('Glacéhandschuh', 1), 'GLAZANSHU')
        self.assertEqual(self.pa.encode('Blechschmidt', 1), 'BLECHSHMIT')
        self.assertEqual(self.pa.encode('Burgdorf', 1), 'BURKDORF')
        self.assertEqual(self.pa.encode('Holzschuh', 1), 'HOLSHU')
        self.assertEqual(self.pa.encode('Aachen', 1), 'ACHN')
        self.assertEqual(
            self.pa.encode('Abendspaziergang', 1), 'ABENTSPAZIRGANK'
        )

        # Test wrapper
        self.assertEqual(phonet('Bremerhaven', 1), 'BREMAHAFN')

    def test_phonet_nolang(self):
        """Test abydos.phonetic.Phonet (no language)."""
        self.assertEqual(self.pa.encode('', lang='none'), '')

        # https://code.google.com/p/phonet4java/source/browse/trunk/src/test/java/com/googlecode/phonet4java/Phonet1Test.java
        self.assertEqual(self.pa.encode('', 1, 'none'), '')
        self.assertEqual(self.pa.encode('Zedlitz', 1, 'none'), 'ZEDLITZ')
        self.assertEqual(
            self.pa.encode('Bremerhaven', 1, 'none'), 'BREMERHAVEN'
        )
        self.assertEqual(self.pa.encode('Schönberg', 2, 'none'), 'SCHOENBERG')
        self.assertEqual(self.pa.encode('Brückmann', 1, 'none'), 'BRUECKMAN')
        self.assertEqual(self.pa.encode('Krauße', 1, 'none'), 'KRAUSE')

        self.assertEqual(self.pa.encode('', 2, 'none'), '')
        self.assertEqual(self.pa.encode('Zedlitz', 2, 'none'), 'ZEDLITZ')
        self.assertEqual(
            self.pa.encode('Bremerhaven', 2, 'none'), 'BREMERHAVEN'
        )
        self.assertEqual(self.pa.encode('Schönberg', 2, 'none'), 'SCHOENBERG')
        self.assertEqual(self.pa.encode('Brückmann', 2, 'none'), 'BRUECKMAN')
        self.assertEqual(self.pa.encode('Krauße', 2, 'none'), 'KRAUSE')

        # Test wrapper
        self.assertEqual(phonet('Bremerhaven', 1, 'none'), 'BREMERHAVEN')

    def test_phonet_nachnamen(self):
        """Test abydos.phonetic.Phonet (Nachnamen set)."""
        if not ALLOW_RANDOM:
            return
        with codecs.open(
            _corpus_file('nachnamen.csv'), encoding='utf-8'
        ) as nachnamen_testset:
            for nn_line in nachnamen_testset:
                if nn_line[0] != '#':
                    nn_line = nn_line.strip().split(',')
                    # This test set is very large (~10000 entries)
                    # so let's just randomly select about 100 for testing
                    if len(nn_line) >= 3 and _one_in(100):
                        (term, ph1, ph2) = nn_line
                        self.assertEqual(self.pa.encode(term, 1), ph1)
                        self.assertEqual(self.pa.encode(term, 2), ph2)

    def test_phonet_ngerman(self):
        """Test abydos.phonetic.Phonet (ngerman set)."""
        if not ALLOW_RANDOM:
            return
        with codecs.open(
            _corpus_file('ngerman.csv'), encoding='utf-8'
        ) as ngerman_testset:
            for ng_line in ngerman_testset:
                if ng_line[0] != '#':
                    ng_line = ng_line.strip().split(',')
                    # This test set is very large (~3000000 entries)
                    # so let's just randomly select about 30 for testing
                    if len(ng_line) >= 3 and _one_in(10000):
                        (term, ph1, ph2) = ng_line
                        self.assertEqual(self.pa.encode(term, 1), ph1)
                        self.assertEqual(self.pa.encode(term, 2), ph2)


if __name__ == '__main__':
    unittest.main()
