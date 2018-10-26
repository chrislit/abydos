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

This module contains unit tests for abydos.phonetic._phonet
"""

from __future__ import unicode_literals

import codecs
import unittest

from abydos.phonetic import phonet

from .. import ALLOW_RANDOM, _corpus_file, _one_in


class PhonetTestCases(unittest.TestCase):
    """Test Phonet functions.

    test cases for abydos.phonetic._phonet.phonet
    """

    def test_phonet_german(self):
        """Test abydos.phonetic._phonet.phonet (German)."""
        self.assertEqual(phonet(''), '')

        # https://code.google.com/p/phonet4java/source/browse/trunk/src/test/java/com/googlecode/phonet4java/Phonet1Test.java
        self.assertEqual(phonet('', 1), '')
        self.assertEqual(phonet('Zedlitz', 1), 'ZETLIZ')
        self.assertEqual(phonet('Bremerhaven', 1), 'BREMAHAFN')
        self.assertEqual(phonet('Hamburger Hafen', 1), 'HAMBURGA HAFN')
        self.assertEqual(phonet('Jesper', 1), 'IESPA')
        self.assertEqual(phonet('elisabeth', 1), 'ELISABET')
        self.assertEqual(phonet('elisabet', 1), 'ELISABET')
        self.assertEqual(phonet('Ziegler', 1), 'ZIKLA')
        self.assertEqual(phonet('Scherer', 1), 'SHERA')
        self.assertEqual(phonet('Bartels', 1), 'BARTLS')
        self.assertEqual(phonet('Jansen', 1), 'IANSN')
        self.assertEqual(phonet('Sievers', 1), 'SIWAS')
        self.assertEqual(phonet('Michels', 1), 'MICHLS')
        self.assertEqual(phonet('Ewers', 1), 'EWERS')
        self.assertEqual(phonet('Evers', 1), 'EWERS')
        self.assertEqual(phonet('Wessels', 1), 'WESLS')
        self.assertEqual(phonet('Gottschalk', 1), 'GOSHALK')
        self.assertEqual(phonet('Brückmann', 1), 'BRÜKMAN')
        self.assertEqual(phonet('Blechschmidt', 1), 'BLECHSHMIT')
        self.assertEqual(phonet('Kolodziej', 1), 'KOLOTZI')
        self.assertEqual(phonet('Krauße', 1), 'KRAUSE')
        self.assertEqual(phonet('Cachel', 1), 'KESHL')

        self.assertEqual(phonet('', 2), '')
        self.assertEqual(phonet('Zedlitz', 2), 'ZETLIZ')
        self.assertEqual(phonet('Bremerhaven', 2), 'BRENAFN')
        self.assertEqual(phonet('Schönberg', 2), 'ZÖNBAK')
        self.assertEqual(phonet('Hamburger Hafen', 2), 'ANBURKA AFN')
        self.assertEqual(phonet('Ziegler', 2), 'ZIKLA')
        self.assertEqual(phonet('Scherer', 2), 'ZERA')
        self.assertEqual(phonet('Jansen', 2), 'IANZN')
        self.assertEqual(phonet('Eberhardt', 2), 'EBART')
        self.assertEqual(phonet('Gottschalk', 2), 'KUZALK')
        self.assertEqual(phonet('Brückmann', 2), 'BRIKNAN')
        self.assertEqual(phonet('Blechschmidt', 2), 'BLEKZNIT')
        self.assertEqual(phonet('Kolodziej', 2), 'KULUTZI')
        self.assertEqual(phonet('Krauße', 2), 'KRAUZE')

        # etc. (for code coverage)
        self.assertEqual(phonet('Jesper', 1), 'IESPA')
        self.assertEqual(phonet('Glacéhandschuh', 1), 'GLAZANSHU')
        self.assertEqual(phonet('Blechschmidt', 1), 'BLECHSHMIT')
        self.assertEqual(phonet('Burgdorf', 1), 'BURKDORF')
        self.assertEqual(phonet('Holzschuh', 1), 'HOLSHU')
        self.assertEqual(phonet('Aachen', 1), 'ACHN')
        self.assertEqual(phonet('Abendspaziergang', 1), 'ABENTSPAZIRGANK')

    def test_phonet_nolang(self):
        """Test abydos.phonetic._phonet.phonet (no language)."""
        self.assertEqual(phonet('', lang='none'), '')

        # https://code.google.com/p/phonet4java/source/browse/trunk/src/test/java/com/googlecode/phonet4java/Phonet1Test.java
        self.assertEqual(phonet('', 1, 'none'), '')
        self.assertEqual(phonet('Zedlitz', 1, 'none'), 'ZEDLITZ')
        self.assertEqual(phonet('Bremerhaven', 1, 'none'), 'BREMERHAVEN')
        self.assertEqual(phonet('Schönberg', 2, 'none'), 'SCHOENBERG')
        self.assertEqual(phonet('Brückmann', 1, 'none'), 'BRUECKMAN')
        self.assertEqual(phonet('Krauße', 1, 'none'), 'KRAUSE')

        self.assertEqual(phonet('', 2, 'none'), '')
        self.assertEqual(phonet('Zedlitz', 2, 'none'), 'ZEDLITZ')
        self.assertEqual(phonet('Bremerhaven', 2, 'none'), 'BREMERHAVEN')
        self.assertEqual(phonet('Schönberg', 2, 'none'), 'SCHOENBERG')
        self.assertEqual(phonet('Brückmann', 2, 'none'), 'BRUECKMAN')
        self.assertEqual(phonet('Krauße', 2, 'none'), 'KRAUSE')

    def test_phonet_nachnamen(self):
        """Test abydos.phonetic._phonet.phonet (Nachnamen set)."""
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
                        self.assertEqual(phonet(term, 1), ph1)
                        self.assertEqual(phonet(term, 2), ph2)

    def test_phonet_ngerman(self):
        """Test abydos.phonetic._phonet.phonet (ngerman set)."""
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
                        self.assertEqual(phonet(term, 1), ph1)
                        self.assertEqual(phonet(term, 2), ph2)


if __name__ == '__main__':
    unittest.main()
