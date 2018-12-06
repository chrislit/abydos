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
    pa_1 = Phonet(1)
    pa_2 = Phonet(2)
    pa_1none = Phonet(1, 'none')
    pa_2none = Phonet(2, 'none')

    def test_phonet_german(self):
        """Test abydos.phonetic.Phonet (German)."""
        self.assertEqual(self.pa.encode(''), '')

        # https://code.google.com/p/phonet4java/source/browse/trunk/src/test/java/com/googlecode/phonet4java/Phonet1Test.java
        self.assertEqual(self.pa_1.encode(''), '')
        self.assertEqual(self.pa_1.encode('Zedlitz'), 'ZETLIZ')
        self.assertEqual(self.pa_1.encode('Bremerhaven'), 'BREMAHAFN')
        self.assertEqual(self.pa_1.encode('Hamburger Hafen'), 'HAMBURGA HAFN')
        self.assertEqual(self.pa_1.encode('Jesper'), 'IESPA')
        self.assertEqual(self.pa_1.encode('elisabeth'), 'ELISABET')
        self.assertEqual(self.pa_1.encode('elisabet'), 'ELISABET')
        self.assertEqual(self.pa_1.encode('Ziegler'), 'ZIKLA')
        self.assertEqual(self.pa_1.encode('Scherer'), 'SHERA')
        self.assertEqual(self.pa_1.encode('Bartels'), 'BARTLS')
        self.assertEqual(self.pa_1.encode('Jansen'), 'IANSN')
        self.assertEqual(self.pa_1.encode('Sievers'), 'SIWAS')
        self.assertEqual(self.pa_1.encode('Michels'), 'MICHLS')
        self.assertEqual(self.pa_1.encode('Ewers'), 'EWERS')
        self.assertEqual(self.pa_1.encode('Evers'), 'EWERS')
        self.assertEqual(self.pa_1.encode('Wessels'), 'WESLS')
        self.assertEqual(self.pa_1.encode('Gottschalk'), 'GOSHALK')
        self.assertEqual(self.pa_1.encode('Brückmann'), 'BRÜKMAN')
        self.assertEqual(self.pa_1.encode('Blechschmidt'), 'BLECHSHMIT')
        self.assertEqual(self.pa_1.encode('Kolodziej'), 'KOLOTZI')
        self.assertEqual(self.pa_1.encode('Krauße'), 'KRAUSE')
        self.assertEqual(self.pa_1.encode('Cachel'), 'KESHL')

        self.assertEqual(self.pa_2.encode(''), '')
        self.assertEqual(self.pa_2.encode('Zedlitz'), 'ZETLIZ')
        self.assertEqual(self.pa_2.encode('Bremerhaven'), 'BRENAFN')
        self.assertEqual(self.pa_2.encode('Schönberg'), 'ZÖNBAK')
        self.assertEqual(self.pa_2.encode('Hamburger Hafen'), 'ANBURKA AFN')
        self.assertEqual(self.pa_2.encode('Ziegler'), 'ZIKLA')
        self.assertEqual(self.pa_2.encode('Scherer'), 'ZERA')
        self.assertEqual(self.pa_2.encode('Jansen'), 'IANZN')
        self.assertEqual(self.pa_2.encode('Eberhardt'), 'EBART')
        self.assertEqual(self.pa_2.encode('Gottschalk'), 'KUZALK')
        self.assertEqual(self.pa_2.encode('Brückmann'), 'BRIKNAN')
        self.assertEqual(self.pa_2.encode('Blechschmidt'), 'BLEKZNIT')
        self.assertEqual(self.pa_2.encode('Kolodziej'), 'KULUTZI')
        self.assertEqual(self.pa_2.encode('Krauße'), 'KRAUZE')

        # etc. (for code coverage)
        self.assertEqual(self.pa_1.encode('Jesper'), 'IESPA')
        self.assertEqual(self.pa_1.encode('Glacéhandschuh'), 'GLAZANSHU')
        self.assertEqual(self.pa_1.encode('Blechschmidt'), 'BLECHSHMIT')
        self.assertEqual(self.pa_1.encode('Burgdorf'), 'BURKDORF')
        self.assertEqual(self.pa_1.encode('Holzschuh'), 'HOLSHU')
        self.assertEqual(self.pa_1.encode('Aachen'), 'ACHN')
        self.assertEqual(
            self.pa_1.encode('Abendspaziergang'), 'ABENTSPAZIRGANK'
        )

        # Test wrapper
        self.assertEqual(phonet('Bremerhaven', 1), 'BREMAHAFN')

    def test_phonet_nolang(self):
        """Test abydos.phonetic.Phonet (no language)."""
        self.assertEqual(Phonet(lang='none').encode(''), '')

        # https://code.google.com/p/phonet4java/source/browse/trunk/src/test/java/com/googlecode/phonet4java/Phonet1Test.java
        self.assertEqual(self.pa_1none.encode(''), '')
        self.assertEqual(self.pa_1none.encode('Zedlitz'), 'ZEDLITZ')
        self.assertEqual(self.pa_1none.encode('Bremerhaven'), 'BREMERHAVEN')
        self.assertEqual(self.pa_2none.encode('Schönberg'), 'SCHOENBERG')
        self.assertEqual(self.pa_1none.encode('Brückmann'), 'BRUECKMAN')
        self.assertEqual(self.pa_1none.encode('Krauße'), 'KRAUSE')

        self.assertEqual(self.pa_2none.encode(''), '')
        self.assertEqual(self.pa_2none.encode('Zedlitz'), 'ZEDLITZ')
        self.assertEqual(self.pa_2none.encode('Bremerhaven'), 'BREMERHAVEN')
        self.assertEqual(self.pa_2none.encode('Schönberg'), 'SCHOENBERG')
        self.assertEqual(self.pa_2none.encode('Brückmann'), 'BRUECKMAN')
        self.assertEqual(self.pa_2none.encode('Krauße'), 'KRAUSE')

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
                        self.assertEqual(self.pa_1.encode(term), ph1)
                        self.assertEqual(self.pa_2.encode(term), ph2)

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
                        self.assertEqual(self.pa_1.encode(term), ph1)
                        self.assertEqual(self.pa_2.encode(term), ph2)


if __name__ == '__main__':
    unittest.main()
