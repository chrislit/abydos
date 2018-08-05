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

"""abydos.tests.test_phonetic.

This module contains unit tests for abydos.phonetic
"""

from __future__ import unicode_literals

import codecs
import math
import os
import random
import unittest

from abydos._bm import _bm_apply_rule_if_compat, _bm_expand_alternates, \
    _bm_language, _bm_normalize_lang_attrs, _bm_phonetic_number, \
    _bm_remove_dupes
from abydos._bmdata import L_ANY, L_CYRILLIC, L_CZECH, L_DUTCH, L_ENGLISH, \
    L_FRENCH, L_GERMAN, L_GREEK, L_GREEKLATIN, L_HEBREW, L_HUNGARIAN, \
    L_ITALIAN, L_LATVIAN, L_POLISH, L_PORTUGUESE, L_ROMANIAN, L_SPANISH, \
    L_TURKISH
from abydos.phonetic import alpha_sis, bmpm, caverphone, dm_soundex, \
    double_metaphone, fuzzy_soundex, koelner_phonetik, \
    koelner_phonetik_alpha, koelner_phonetik_num_to_alpha, lein, metaphone, \
    mra, nysiis, onca, phonem, phonet, phonex, phonix, refined_soundex, \
    roger_root,  russell_index, russell_index_alpha, \
    russell_index_num_to_alpha, sfinxbis, soundex, spfc, statistics_canada

from six import text_type

TESTDIR = os.path.dirname(__file__)

EXTREME_TEST = False  # Set to True to test EVERY single case (NB: takes hours)
ALLOW_RANDOM = True  # Set to False to skip all random tests

if not EXTREME_TEST and os.path.isfile(TESTDIR + '/EXTREME_TEST'):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True


def one_in(inverse_probability):
    """Return whether to run a test.

    Return True if:
        EXTREME_TEST is True
        OR
        (ALLOW_RANDOM is False
        AND
        random.random() * inverse_probability < 1
    Otherwise return False
    """
    if EXTREME_TEST:
        return True
    elif ALLOW_RANDOM and random.random() * inverse_probability < 1:
        return True
    else:
        return False


class RussellIndexTestCases(unittest.TestCase):
    """Test Russel Index functions.

    test cases for abydos.phonetic.russell_index,
    .russell_index_num_to_alpha, & .russell_index_alpha
    """

    def test_russel_index(self):
        """Test abydos.phonetic.russell_index."""
        self.assertTrue(math.isnan(russell_index('')))
        self.assertTrue(math.isnan(russell_index('H')))
        self.assertEqual(russell_index('Hoppa'), 12)
        self.assertEqual(russell_index('Hopley'), 125)
        self.assertEqual(russell_index('Highfield'), 1254)
        self.assertEqual(russell_index('Wright'), 814)
        self.assertEqual(russell_index('Carter'), 31848)
        self.assertEqual(russell_index('Hopf'), 12)
        self.assertEqual(russell_index('Hay'), 1)
        self.assertEqual(russell_index('Haas'), 1)
        self.assertEqual(russell_index('Meyers'), 618)
        self.assertEqual(russell_index('Myers'), 618)
        self.assertEqual(russell_index('Meyer'), 618)
        self.assertEqual(russell_index('Myer'), 618)
        self.assertEqual(russell_index('Mack'), 613)
        self.assertEqual(russell_index('Knack'), 3713)

    def test_russel_index_n2a(self):
        """Test abydos.phonetic.russell_index_num_to_alpha."""
        self.assertEqual(russell_index_num_to_alpha(0), '')
        self.assertEqual(russell_index_num_to_alpha(''), '')
        self.assertEqual(russell_index_num_to_alpha(float('NaN')), '')
        self.assertEqual(russell_index_num_to_alpha(123456789), 'ABCDLMNR')
        self.assertEqual(russell_index_num_to_alpha('0123456789'), 'ABCDLMNR')

    def test_russel_index_alpha(self):
        """Test abydos.phonetic.russell_index_alpha."""
        self.assertEqual(russell_index_alpha(''), '')
        self.assertEqual(russell_index_alpha('H'), '')
        self.assertEqual(russell_index_alpha('Hoppa'), 'AB')
        self.assertEqual(russell_index_alpha('Hopley'), 'ABL')
        self.assertEqual(russell_index_alpha('Highfield'), 'ABLD')
        self.assertEqual(russell_index_alpha('Wright'), 'RAD')
        self.assertEqual(russell_index_alpha('Carter'), 'CARDR')
        self.assertEqual(russell_index_alpha('Hopf'), 'AB')
        self.assertEqual(russell_index_alpha('Hay'), 'A')
        self.assertEqual(russell_index_alpha('Haas'), 'A')
        self.assertEqual(russell_index_alpha('Meyers'), 'MAR')
        self.assertEqual(russell_index_alpha('Myers'), 'MAR')
        self.assertEqual(russell_index_alpha('Meyer'), 'MAR')
        self.assertEqual(russell_index_alpha('Myer'), 'MAR')
        self.assertEqual(russell_index_alpha('Mack'), 'MAC')
        self.assertEqual(russell_index_alpha('Knack'), 'CNAC')


class SoundexTestCases(unittest.TestCase):
    """Test Soundex functions.

    test cases for abydos.phonetic.soundex, .refined_soundex,
    & .dm_soundex
    """

    def test_soundex(self):
        """Test abydos.phonetic.soundex."""
        self.assertEqual(soundex(''), '0000')

        # https://archive.org/stream/accessingindivid00moor#page/14/mode/2up
        self.assertEqual(soundex('Euler'), 'E460')
        self.assertEqual(soundex('Gauss'), 'G200')
        self.assertEqual(soundex('Hilbert'), 'H416')
        self.assertEqual(soundex('Knuth'), 'K530')
        self.assertEqual(soundex('Lloyd'), 'L300')
        self.assertEqual(soundex('Lukasieicz'), 'L222')
        self.assertEqual(soundex('Ellery'), 'E460')
        self.assertEqual(soundex('Ghosh'), 'G200')
        self.assertEqual(soundex('Heilbronn'), 'H416')
        self.assertEqual(soundex('Kant'), 'K530')
        self.assertEqual(soundex('Ladd'), 'L300')
        self.assertEqual(soundex('Lissajous'), 'L222')
        self.assertEqual(soundex('Rogers'), 'R262')
        self.assertEqual(soundex('Rodgers'), 'R326')
        self.assertNotEquals(soundex('Rogers'), soundex('Rodgers'))
        self.assertNotEquals(soundex('Sinclair'), soundex('St. Clair'))
        self.assertNotEquals(soundex('Tchebysheff'), soundex('Chebyshev'))

        # http://creativyst.com/Doc/Articles/SoundEx1/SoundEx1.htm#Related
        self.assertEqual(soundex('Htacky'), 'H320')
        self.assertEqual(soundex('Atacky'), 'A320')
        self.assertEqual(soundex('Schmit'), 'S530')
        self.assertEqual(soundex('Schneider'), 'S536')
        self.assertEqual(soundex('Pfister'), 'P236')
        self.assertEqual(soundex('Ashcroft'), 'A261')
        self.assertEqual(soundex('Asicroft'), 'A226')

        # https://en.wikipedia.org/wiki/Soundex
        self.assertEqual(soundex('Robert'), 'R163')
        self.assertEqual(soundex('Rupert'), 'R163')
        self.assertEqual(soundex('Rubin'), 'R150')
        self.assertEqual(soundex('Tymczak'), 'T522')

        # https://en.wikipedia.org/wiki/Daitch%E2%80%93Mokotoff_Soundex
        self.assertEqual(soundex('Peters'), 'P362')
        self.assertEqual(soundex('Peterson'), 'P362')
        self.assertEqual(soundex('Moskowitz'), 'M232')
        self.assertEqual(soundex('Moskovitz'), 'M213')
        self.assertEqual(soundex('Auerbach'), 'A612')
        self.assertEqual(soundex('Uhrbach'), 'U612')
        self.assertEqual(soundex('Jackson'), 'J250')
        self.assertEqual(soundex('Jackson-Jackson'), 'J252')

        # maxlength tests
        self.assertEqual(soundex('Lincoln', 10), 'L524500000')
        self.assertEqual(soundex('Lincoln', 5), 'L5245')
        self.assertEqual(soundex('Christopher', 6), 'C62316')

        # maxlength bounds tests
        self.assertEqual(soundex('Niall', maxlength=float('inf')),
                         'N4000000000000000000000000000000000000000000000000' +
                         '00000000000000')
        self.assertEqual(soundex('Niall', maxlength=None),
                         'N4000000000000000000000000000000000000000000000000' +
                         '00000000000000')
        self.assertEqual(soundex('Niall', maxlength=0), 'N400')

        # reverse tests
        self.assertEqual(soundex('Rubin', reverse=True), 'N160')
        self.assertEqual(soundex('Llyod', reverse=True), 'D400')
        self.assertEqual(soundex('Lincoln', reverse=True), 'N425')
        self.assertEqual(soundex('Knuth', reverse=True), 'H352')

        # zero_pad tests
        self.assertEqual(soundex('Niall', maxlength=float('inf'),
                                 zero_pad=False), 'N4')
        self.assertEqual(soundex('Niall', maxlength=None,
                                 zero_pad=False), 'N4')
        self.assertEqual(soundex('Niall', maxlength=0, zero_pad=False), 'N4')
        self.assertEqual(soundex('Niall', maxlength=0, zero_pad=True), 'N400')
        self.assertEqual(soundex('', maxlength=4, zero_pad=False), '0')
        self.assertEqual(soundex('', maxlength=4, zero_pad=True), '0000')

    def test_soundex_special(self):
        """Test abydos.phonetic.soundex (special census variant method)."""
        self.assertEqual(soundex('Ashcroft', var='special'), 'A226')
        self.assertEqual(soundex('Asicroft', var='special'), 'A226')
        self.assertEqual(soundex('AsWcroft', var='special'), 'A226')
        self.assertEqual(soundex('Rupert', var='special'), 'R163')
        self.assertEqual(soundex('Rubin', var='special'), 'R150')

    def test_refined_soundex(self):
        """Test abydos.phonetic.refined_soundex."""
        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(refined_soundex('Braz'), 'B1905')
        self.assertEqual(refined_soundex('Broz'), 'B1905')
        self.assertEqual(refined_soundex('Caren'), 'C30908')
        self.assertEqual(refined_soundex('Caron'), 'C30908')
        self.assertEqual(refined_soundex('Carren'), 'C30908')
        self.assertEqual(refined_soundex('Charon'), 'C30908')
        self.assertEqual(refined_soundex('Corain'), 'C30908')
        self.assertEqual(refined_soundex('Coram'), 'C30908')
        self.assertEqual(refined_soundex('Corran'), 'C30908')
        self.assertEqual(refined_soundex('Corrin'), 'C30908')
        self.assertEqual(refined_soundex('Corwin'), 'C30908')
        self.assertEqual(refined_soundex('Curran'), 'C30908')
        self.assertEqual(refined_soundex('Curreen'), 'C30908')
        self.assertEqual(refined_soundex('Currin'), 'C30908')
        self.assertEqual(refined_soundex('Currom'), 'C30908')
        self.assertEqual(refined_soundex('Currum'), 'C30908')
        self.assertEqual(refined_soundex('Curwen'), 'C30908')
        self.assertEqual(refined_soundex('Caren'), 'C30908')
        self.assertEqual(refined_soundex('Caren'), 'C30908')
        self.assertEqual(refined_soundex('Caren'), 'C30908')
        self.assertEqual(refined_soundex('Caren'), 'C30908')
        self.assertEqual(refined_soundex('Caren'), 'C30908')
        self.assertEqual(refined_soundex('Caren'), 'C30908')
        self.assertEqual(refined_soundex('Caren'), 'C30908')
        self.assertEqual(refined_soundex('Hairs'), 'H093')
        self.assertEqual(refined_soundex('Hark'), 'H093')
        self.assertEqual(refined_soundex('Hars'), 'H093')
        self.assertEqual(refined_soundex('Hayers'), 'H093')
        self.assertEqual(refined_soundex('Heers'), 'H093')
        self.assertEqual(refined_soundex('Hiers'), 'H093')
        self.assertEqual(refined_soundex('Lambard'), 'L7081096')
        self.assertEqual(refined_soundex('Lambart'), 'L7081096')
        self.assertEqual(refined_soundex('Lambert'), 'L7081096')
        self.assertEqual(refined_soundex('Lambird'), 'L7081096')
        self.assertEqual(refined_soundex('Lampaert'), 'L7081096')
        self.assertEqual(refined_soundex('Lampard'), 'L7081096')
        self.assertEqual(refined_soundex('Lampart'), 'L7081096')
        self.assertEqual(refined_soundex('Lamperd'), 'L7081096')
        self.assertEqual(refined_soundex('Lampert'), 'L7081096')
        self.assertEqual(refined_soundex('Lamport'), 'L7081096')
        self.assertEqual(refined_soundex('Limbert'), 'L7081096')
        self.assertEqual(refined_soundex('Lombard'), 'L7081096')
        self.assertEqual(refined_soundex('Nolton'), 'N807608')
        self.assertEqual(refined_soundex('Noulton'), 'N807608')

        # http://trimc-nlp.blogspot.com/2015/03/the-soundex-algorithm.html
        self.assertEqual(refined_soundex('Craig'), 'C3904')
        self.assertEqual(refined_soundex('Crag'), 'C3904')
        self.assertEqual(refined_soundex('Crejg'), 'C3904')
        self.assertEqual(refined_soundex('Creig'), 'C3904')
        self.assertEqual(refined_soundex('Craigg'), 'C3904')
        self.assertEqual(refined_soundex('Craug'), 'C3904')
        self.assertEqual(refined_soundex('Craiggg'), 'C3904')
        self.assertEqual(refined_soundex('Creg'), 'C3904')
        self.assertEqual(refined_soundex('Cregg'), 'C3904')
        self.assertEqual(refined_soundex('Creag'), 'C3904')
        self.assertEqual(refined_soundex('Greg'), 'G4904')
        self.assertEqual(refined_soundex('Gregg'), 'G4904')
        self.assertEqual(refined_soundex('Graig'), 'G4904')
        self.assertEqual(refined_soundex('Greig'), 'G4904')
        self.assertEqual(refined_soundex('Greggg'), 'G4904')
        self.assertEqual(refined_soundex('Groeg'), 'G4904')
        self.assertEqual(refined_soundex('Graj'), 'G4904')
        self.assertEqual(refined_soundex('Grej'), 'G4904')
        self.assertEqual(refined_soundex('Grreg'), 'G4904')
        self.assertEqual(refined_soundex('Greag'), 'G4904')
        self.assertEqual(refined_soundex('Grig'), 'G4904')
        self.assertEqual(refined_soundex('Kregg'), 'K3904')
        self.assertEqual(refined_soundex('Kraig'), 'K3904')
        self.assertEqual(refined_soundex('Krag'), 'K3904')
        self.assertEqual(refined_soundex('Kreig'), 'K3904')
        self.assertEqual(refined_soundex('Krug'), 'K3904')
        self.assertEqual(refined_soundex('Kreg'), 'K3904')
        self.assertEqual(refined_soundex('Krieg'), 'K3904')
        self.assertEqual(refined_soundex('Krijg'), 'K3904')

        # Apache Commons test cases
        # http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/RefinedSoundexTest.java?view=markup
        self.assertEqual(refined_soundex('testing'), 'T6036084')
        self.assertEqual(refined_soundex('TESTING'), 'T6036084')
        self.assertEqual(refined_soundex('The'), 'T60')
        self.assertEqual(refined_soundex('quick'), 'Q503')
        self.assertEqual(refined_soundex('brown'), 'B1908')
        self.assertEqual(refined_soundex('fox'), 'F205')
        self.assertEqual(refined_soundex('jumped'), 'J408106')
        self.assertEqual(refined_soundex('over'), 'O0209')
        self.assertEqual(refined_soundex('the'), 'T60')
        self.assertEqual(refined_soundex('lazy'), 'L7050')
        self.assertEqual(refined_soundex('dogs'), 'D6043')

    def test_dm_soundex(self):
        """Test abydos.phonetic.dm_soundex (Daitchh-Mokotoff Soundex)."""
        # D-M tests
        self.assertEqual(soundex('', var='dm'), {'000000'})
        self.assertEqual(dm_soundex(''), {'000000'})

        # http://www.avotaynu.com/soundex.htm
        self.assertEqual(soundex('Augsburg', var='dm'), {'054795'})
        self.assertEqual(dm_soundex('Augsburg'), {'054795'})
        self.assertEqual(soundex('Breuer', var='dm'), {'791900'})
        self.assertEqual(dm_soundex('Breuer'), {'791900'})
        self.assertEqual(soundex('Halberstadt', var='dm'),
                         {'587943', '587433'})
        self.assertEqual(dm_soundex('Halberstadt'), {'587943', '587433'})
        self.assertEqual(soundex('Mannheim', var='dm'), {'665600'})
        self.assertEqual(dm_soundex('Mannheim'), {'665600'})
        self.assertEqual(soundex('Chernowitz', var='dm'),
                         {'496740', '596740'})
        self.assertEqual(dm_soundex('Chernowitz'), {'496740', '596740'})
        self.assertEqual(soundex('Cherkassy', var='dm'),
                         {'495400', '595400'})
        self.assertEqual(dm_soundex('Cherkassy'), {'495400', '595400'})
        self.assertEqual(soundex('Kleinman', var='dm'), {'586660'})
        self.assertEqual(dm_soundex('Kleinman'), {'586660'})
        self.assertEqual(soundex('Berlin', var='dm'), {'798600'})
        self.assertEqual(dm_soundex('Berlin'), {'798600'})

        self.assertEqual(soundex('Ceniow', var='dm'),
                         {'467000', '567000'})
        self.assertEqual(dm_soundex('Ceniow'), {'467000', '567000'})
        self.assertEqual(soundex('Tsenyuv', var='dm'), {'467000'})
        self.assertEqual(dm_soundex('Tsenyuv'), {'467000'})
        self.assertEqual(soundex('Holubica', var='dm'),
                         {'587400', '587500'})
        self.assertEqual(dm_soundex('Holubica'), {'587400', '587500'})
        self.assertEqual(soundex('Golubitsa', var='dm'), {'587400'})
        self.assertEqual(dm_soundex('Golubitsa'), {'587400'})
        self.assertEqual(soundex('Przemysl', var='dm'),
                         {'746480', '794648'})
        self.assertEqual(dm_soundex('Przemysl'), {'746480', '794648'})
        self.assertEqual(soundex('Pshemeshil', var='dm'), {'746480'})
        self.assertEqual(dm_soundex('Pshemeshil'), {'746480'})
        self.assertEqual(soundex('Rosochowaciec', var='dm'),
                         {'944744', '945744', '944755', '944754', '944745',
                          '945745', '945754', '945755'})
        self.assertEqual(dm_soundex('Rosochowaciec'),
                         {'944744', '945744', '944755', '944754', '944745',
                          '945745', '945754', '945755'})
        self.assertEqual(soundex('Rosokhovatsets', var='dm'), {'945744'})
        self.assertEqual(dm_soundex('Rosokhovatsets'), {'945744'})

        # https://en.wikipedia.org/wiki/Daitch%E2%80%93Mokotoff_Soundex
        self.assertEqual(soundex('Peters', var='dm'),
                         {'739400', '734000'})
        self.assertEqual(dm_soundex('Peters'), {'739400', '734000'})
        self.assertEqual(soundex('Peterson', var='dm'),
                         {'739460', '734600'})
        self.assertEqual(dm_soundex('Peterson'), {'739460', '734600'})
        self.assertEqual(soundex('Moskowitz', var='dm'), {'645740'})
        self.assertEqual(dm_soundex('Moskowitz'), {'645740'})
        self.assertEqual(soundex('Moskovitz', var='dm'), {'645740'})
        self.assertEqual(dm_soundex('Moskovitz'), {'645740'})
        self.assertEqual(soundex('Auerbach', var='dm'),
                         {'097500', '097400'})
        self.assertEqual(dm_soundex('Auerbach'), {'097500', '097400'})
        self.assertEqual(soundex('Uhrbach', var='dm'),
                         {'097500', '097400'})
        self.assertEqual(dm_soundex('Uhrbach'), {'097500', '097400'})
        self.assertEqual(soundex('Jackson', var='dm'),
                         {'154600', '454600', '145460', '445460'})
        self.assertEqual(dm_soundex('Jackson'),
                         {'154600', '454600', '145460', '445460'})
        self.assertEqual(soundex('Jackson-Jackson', var='dm'),
                         {'154654', '454654', '145465', '445465',
                          '154645', '454645', '145464', '445464',
                          '154644', '454644'})
        self.assertEqual(dm_soundex('Jackson-Jackson'),
                         {'154654', '454654', '145465', '445465',
                          '154645', '454645', '145464', '445464',
                          '154644', '454644'})

        # http://www.jewishgen.org/infofiles/soundex.html
        self.assertEqual(soundex('OHRBACH', var='dm'),
                         {'097500', '097400'})
        self.assertEqual(dm_soundex('OHRBACH'), {'097500', '097400'})
        self.assertEqual(soundex('LIPSHITZ', var='dm'), {'874400'})
        self.assertEqual(dm_soundex('LIPSHITZ'), {'874400'})
        self.assertEqual(soundex('LIPPSZYC', var='dm'),
                         {'874400', '874500'})
        self.assertEqual(dm_soundex('LIPPSZYC'), {'874400', '874500'})
        self.assertEqual(soundex('LEWINSKY', var='dm'), {'876450'})
        self.assertEqual(dm_soundex('LEWINSKY'), {'876450'})
        self.assertEqual(soundex('LEVINSKI', var='dm'), {'876450'})
        self.assertEqual(dm_soundex('LEVINSKI'), {'876450'})
        self.assertEqual(soundex('SZLAMAWICZ', var='dm'), {'486740'})
        self.assertEqual(dm_soundex('SZLAMAWICZ'), {'486740'})
        self.assertEqual(soundex('SHLAMOVITZ', var='dm'), {'486740'})
        self.assertEqual(dm_soundex('SHLAMOVITZ'), {'486740'})

        # http://community.actian.com/wiki/OME_soundex_dm()
        self.assertEqual(soundex('Schwarzenegger', var='dm'),
                         {'479465', '474659'})
        self.assertEqual(dm_soundex('Schwarzenegger'),
                         {'479465', '474659'})
        self.assertEqual(soundex('Shwarzenegger', var='dm'),
                         {'479465', '474659'})
        self.assertEqual(dm_soundex('Shwarzenegger'),
                         {'479465', '474659'})
        self.assertEqual(soundex('Schwartsenegger', var='dm'),
                         {'479465'})
        self.assertEqual(dm_soundex('Schwartsenegger'), {'479465'})

        # reverse DM-Soundex
        self.assertEqual(soundex('Schwarzenegger', var='dm', reverse=True),
                         {'956497'})
        self.assertEqual(dm_soundex('Schwarzenegger', reverse=True),
                         {'956497'})

        # maxlength bounds tests
        self.assertEqual(dm_soundex('Niall', maxlength=float('inf')),
                         {'68'+'0'*62})
        self.assertEqual(dm_soundex('Niall', maxlength=None),
                         {'68'+'0'*62})
        self.assertEqual(dm_soundex('Niall', maxlength=0), {'680000'})

        # zero_pad tests
        self.assertEqual(dm_soundex('Niall', maxlength=float('inf'),
                                    zero_pad=False), {'68'})
        self.assertEqual(dm_soundex('Niall', maxlength=None, zero_pad=False),
                         {'68'})
        self.assertEqual(dm_soundex('Niall', maxlength=0, zero_pad=False),
                         {'68'})
        self.assertEqual(dm_soundex('Niall', maxlength=0, zero_pad=True),
                         {'680000'})
        self.assertEqual(dm_soundex('', maxlength=6, zero_pad=False),
                         {'0'})
        self.assertEqual(dm_soundex('', maxlength=6, zero_pad=True),
                         {'000000'})


class KoelnerPhonetikTestCases(unittest.TestCase):
    """Test Koelner Phonetic functions.

    test cases for abydos.phonetic.koelner_phonetik,
    .koelner_phonetik_num_to_alpha, & .koelner_phonetik_alpha
    """

    def test_koelner_phonetik(self):
        """Test abydos.phonetic.koelner_phonetik."""
        self.assertEqual(koelner_phonetik(''), '')

        # https://de.wikipedia.org/wiki/K%C3%B6lner_Phonetik
        self.assertEqual(koelner_phonetik('Müller-Lüdenscheidt'), '65752682')
        self.assertEqual(koelner_phonetik('Wikipedia'), '3412')
        self.assertEqual(koelner_phonetik('Breschnew'), '17863')

        # http://search.cpan.org/~maros/Text-Phonetic/lib/Text/Phonetic/Koeln.pm
        self.assertEqual(koelner_phonetik('Müller'), '657')
        self.assertEqual(koelner_phonetik('schmidt'), '862')
        self.assertEqual(koelner_phonetik('schneider'), '8627')
        self.assertEqual(koelner_phonetik('fischer'), '387')
        self.assertEqual(koelner_phonetik('weber'), '317')
        self.assertEqual(koelner_phonetik('meyer'), '67')
        self.assertEqual(koelner_phonetik('wagner'), '3467')
        self.assertEqual(koelner_phonetik('schulz'), '858')
        self.assertEqual(koelner_phonetik('becker'), '147')
        self.assertEqual(koelner_phonetik('hoffmann'), '0366')
        self.assertEqual(koelner_phonetik('schäfer'), '837')
        self.assertEqual(koelner_phonetik('cater'), '427')
        self.assertEqual(koelner_phonetik('axel'), '0485')

        # etc. (for code coverage)
        self.assertEqual(koelner_phonetik('Akxel'), '0485')
        self.assertEqual(koelner_phonetik('Adz'), '08')
        self.assertEqual(koelner_phonetik('Alpharades'), '053728')
        self.assertEqual(koelner_phonetik('Cent'), '862')
        self.assertEqual(koelner_phonetik('Acre'), '087')
        self.assertEqual(koelner_phonetik('H'), '')

    def test_koelner_phonetik_n2a(self):
        """Test abydos.phonetic.koelner_phonetik_num_to_alpha."""
        self.assertEqual(koelner_phonetik_num_to_alpha('0123456789'),
                         'APTFKLNRS')

    def test_koelner_phonetik_alpha(self):
        """Test abydos.phonetic.koelner_phonetik_alpha."""
        self.assertEqual(koelner_phonetik_alpha('Müller-Lüdenscheidt'),
                         'NLRLTNST')
        self.assertEqual(koelner_phonetik_alpha('Wikipedia'), 'FKPT')
        self.assertEqual(koelner_phonetik_alpha('Breschnew'), 'PRSNF')
        self.assertEqual(koelner_phonetik_alpha('Müller'), 'NLR')
        self.assertEqual(koelner_phonetik_alpha('schmidt'), 'SNT')
        self.assertEqual(koelner_phonetik_alpha('schneider'), 'SNTR')
        self.assertEqual(koelner_phonetik_alpha('fischer'), 'FSR')
        self.assertEqual(koelner_phonetik_alpha('weber'), 'FPR')
        self.assertEqual(koelner_phonetik_alpha('meyer'), 'NR')
        self.assertEqual(koelner_phonetik_alpha('wagner'), 'FKNR')
        self.assertEqual(koelner_phonetik_alpha('schulz'), 'SLS')
        self.assertEqual(koelner_phonetik_alpha('becker'), 'PKR')
        self.assertEqual(koelner_phonetik_alpha('hoffmann'), 'AFNN')
        self.assertEqual(koelner_phonetik_alpha('schäfer'), 'SFR')
        self.assertEqual(koelner_phonetik_alpha('cater'), 'KTR')
        self.assertEqual(koelner_phonetik_alpha('axel'), 'AKSL')


class NysiisTestCases(unittest.TestCase):
    """Test NYSIIS functions.

    test cases for abydos.phonetic.nysiis
    """

    def test_nysiis(self):
        """Test abydos.phonetic.nysiis."""
        self.assertEqual(nysiis(''), '')

        # http://coryodaniel.com/index.php/2009/12/30/ruby-nysiis-implementation/
        self.assertEqual(nysiis('O\'Daniel'), 'ODANAL')
        self.assertEqual(nysiis('O\'Donnel'), 'ODANAL')
        self.assertEqual(nysiis('Cory'), 'CARY')
        self.assertEqual(nysiis('Corey'), 'CARY')
        self.assertEqual(nysiis('Kory'), 'CARY')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(nysiis('Diggell'), 'DAGAL')
        self.assertEqual(nysiis('Dougal'), 'DAGAL')
        self.assertEqual(nysiis('Doughill'), 'DAGAL')
        self.assertEqual(nysiis('Dougill'), 'DAGAL')
        self.assertEqual(nysiis('Dowgill'), 'DAGAL')
        self.assertEqual(nysiis('Dugall'), 'DAGAL')
        self.assertEqual(nysiis('Dugall'), 'DAGAL')
        self.assertEqual(nysiis('Glinde'), 'GLAND')
        self.assertEqual(nysiis('Plumridge', maxlength=20), 'PLANRADG')
        self.assertEqual(nysiis('Chinnick'), 'CANAC')
        self.assertEqual(nysiis('Chinnock'), 'CANAC')
        self.assertEqual(nysiis('Chinnock'), 'CANAC')
        self.assertEqual(nysiis('Chomicki'), 'CANAC')
        self.assertEqual(nysiis('Chomicz'), 'CANAC')
        self.assertEqual(nysiis('Schimek'), 'SANAC')
        self.assertEqual(nysiis('Shimuk'), 'SANAC')
        self.assertEqual(nysiis('Simak'), 'SANAC')
        self.assertEqual(nysiis('Simek'), 'SANAC')
        self.assertEqual(nysiis('Simic'), 'SANAC')
        self.assertEqual(nysiis('Sinnock'), 'SANAC')
        self.assertEqual(nysiis('Sinnocke'), 'SANAC')
        self.assertEqual(nysiis('Sunnex'), 'SANAX')
        self.assertEqual(nysiis('Sunnucks'), 'SANAC')
        self.assertEqual(nysiis('Sunock'), 'SANAC')
        self.assertEqual(nysiis('Webberley', maxlength=20), 'WABARLY')
        self.assertEqual(nysiis('Wibberley', maxlength=20), 'WABARLY')

        # etc. (for code coverage)
        self.assertEqual(nysiis('Alpharades'), 'ALFARA')
        self.assertEqual(nysiis('Aschenputtel'), 'ASANPA')
        self.assertEqual(nysiis('Beverly'), 'BAFARL')
        self.assertEqual(nysiis('Hardt'), 'HARD')
        self.assertEqual(nysiis('acknowledge'), 'ACNALA')
        self.assertEqual(nysiis('MacNeill'), 'MCNAL')
        self.assertEqual(nysiis('MacNeill'), nysiis('McNeill'))
        self.assertEqual(nysiis('Knight'), 'NAGT')
        self.assertEqual(nysiis('Knight'), nysiis('Night'))
        self.assertEqual(nysiis('Pfarr'), 'FAR')
        self.assertEqual(nysiis('Phair'), 'FAR')
        self.assertEqual(nysiis('Phair'), nysiis('Pfarr'))
        self.assertEqual(nysiis('Cherokee'), 'CARACY')
        self.assertEqual(nysiis('Iraq'), 'IRAG')

        # maxlength bounds tests
        self.assertEqual(nysiis('Niall', maxlength=float('inf')), 'NAL')
        self.assertEqual(nysiis('Niall', maxlength=None), 'NAL')
        self.assertEqual(nysiis('Niall', maxlength=0), 'NAL')

    def test_modified_nysiis(self):
        """Test abydos.phonetic.nysiis (modified version)."""
        self.assertEqual(nysiis('', maxlength=float('inf'), modified=True), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        # Some of these were... wrong... and have been corrected
        self.assertEqual(nysiis('Daves', maxlength=8, modified=True), 'DAV')
        self.assertEqual(nysiis('Davies', maxlength=8, modified=True), 'DAVY')
        self.assertEqual(nysiis('Devies', maxlength=8, modified=True), 'DAFY')
        self.assertEqual(nysiis('Divish', maxlength=8, modified=True), 'DAVAS')
        self.assertEqual(nysiis('Dove', maxlength=8, modified=True), 'DAV')
        self.assertEqual(nysiis('Devese', maxlength=8, modified=True), 'DAFAS')
        self.assertEqual(nysiis('Devies', maxlength=8, modified=True), 'DAFY')
        self.assertEqual(nysiis('Devos', maxlength=8, modified=True), 'DAF')

        self.assertEqual(nysiis('Schmit', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Schmitt', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Schmitz', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Schmoutz', maxlength=8, modified=True),
                         'SNAT')
        self.assertEqual(nysiis('Schnitt', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smit', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smite', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smits', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smoot', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smuts', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Sneath', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smyth', maxlength=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smithy', maxlength=8, modified=True), 'SNATY')
        self.assertEqual(nysiis('Smithey', maxlength=8, modified=True),
                         'SNATY')

        # http://www.dropby.com/NYSIISTextStrings.html
        # Some of these have been altered since the above uses a different set
        # of modifications.
        self.assertEqual(nysiis('Edwards', maxlength=8, modified=True),
                         'EDWAD')
        self.assertEqual(nysiis('Perez', maxlength=8, modified=True), 'PAR')
        self.assertEqual(nysiis('Macintosh', maxlength=8, modified=True),
                         'MCANTAS')
        self.assertEqual(nysiis('Phillipson', maxlength=8, modified=True),
                         'FALAPSAN')
        self.assertEqual(nysiis('Haddix', maxlength=8, modified=True), 'HADAC')
        self.assertEqual(nysiis('Essex', maxlength=8, modified=True), 'ESAC')
        self.assertEqual(nysiis('Moye', maxlength=8, modified=True), 'MY')
        self.assertEqual(nysiis('McKee', maxlength=8, modified=True), 'MCY')
        self.assertEqual(nysiis('Mackie', maxlength=8, modified=True), 'MCY')
        self.assertEqual(nysiis('Heitschmidt', maxlength=8, modified=True),
                         'HATSNAD')
        self.assertEqual(nysiis('Bart', maxlength=8, modified=True), 'BAD')
        self.assertEqual(nysiis('Hurd', maxlength=8, modified=True), 'HAD')
        self.assertEqual(nysiis('Hunt', maxlength=8, modified=True), 'HAN')
        self.assertEqual(nysiis('Westerlund', maxlength=8, modified=True),
                         'WASTARLA')
        self.assertEqual(nysiis('Evers', maxlength=8, modified=True), 'EVAR')
        self.assertEqual(nysiis('Devito', maxlength=8, modified=True), 'DAFAT')
        self.assertEqual(nysiis('Rawson', maxlength=8, modified=True), 'RASAN')
        self.assertEqual(nysiis('Shoulders', maxlength=8, modified=True),
                         'SALDAR')
        self.assertEqual(nysiis('Leighton', maxlength=8, modified=True),
                         'LATAN')
        self.assertEqual(nysiis('Wooldridge', maxlength=8, modified=True),
                         'WALDRAG')
        self.assertEqual(nysiis('Oliphant', maxlength=8, modified=True),
                         'OLAFAN')
        self.assertEqual(nysiis('Hatchett', maxlength=8, modified=True),
                         'HATCAT')
        self.assertEqual(nysiis('McKnight', maxlength=8, modified=True),
                         'MCNAT')
        self.assertEqual(nysiis('Rickert', maxlength=8, modified=True),
                         'RACAD')
        self.assertEqual(nysiis('Bowman', maxlength=8, modified=True), 'BANAN')
        self.assertEqual(nysiis('Vasquez', maxlength=8, modified=True), 'VASG')
        self.assertEqual(nysiis('Bashaw', maxlength=8, modified=True), 'BAS')
        self.assertEqual(nysiis('Schoenhoeft', maxlength=8, modified=True),
                         'SANAFT')
        self.assertEqual(nysiis('Heywood', maxlength=8, modified=True), 'HAD')
        self.assertEqual(nysiis('Hayman', maxlength=8, modified=True), 'HANAN')
        self.assertEqual(nysiis('Seawright', maxlength=8, modified=True),
                         'SARAT')
        self.assertEqual(nysiis('Kratzer', maxlength=8, modified=True),
                         'CRATSAR')
        self.assertEqual(nysiis('Canaday', maxlength=8, modified=True),
                         'CANADY')
        self.assertEqual(nysiis('Crepeau', maxlength=8, modified=True), 'CRAP')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/nysiis.js
        self.assertEqual(nysiis('Andrew', maxlength=8, modified=True), 'ANDR')
        self.assertEqual(nysiis('Robertson', maxlength=8, modified=True),
                         'RABARTSA')
        self.assertEqual(nysiis('Nolan', maxlength=8, modified=True), 'NALAN')
        self.assertEqual(nysiis('Louis XVI', maxlength=8, modified=True),
                         'LASXV')
        self.assertEqual(nysiis('Case', maxlength=8, modified=True), 'CAS')
        self.assertEqual(nysiis('Mclaughlin', maxlength=8, modified=True),
                         'MCLAGLAN')
        self.assertEqual(nysiis('Awale', maxlength=8, modified=True), 'AL')
        self.assertEqual(nysiis('Aegir', maxlength=8, modified=True), 'AGAR')
        self.assertEqual(nysiis('Lundgren', maxlength=8, modified=True),
                         'LANGRAN')
        self.assertEqual(nysiis('Philbert', maxlength=8, modified=True),
                         'FALBAD')
        self.assertEqual(nysiis('Harry', maxlength=8, modified=True), 'HARY')
        self.assertEqual(nysiis('Mackenzie', maxlength=8, modified=True),
                         'MCANSY')

        # maxlength bounds tests
        self.assertEqual(nysiis('Niall', maxlength=float('inf'),
                                modified=True), 'NAL')
        self.assertEqual(nysiis('Niall', maxlength=None, modified=True), 'NAL')
        self.assertEqual(nysiis('Niall', maxlength=0, modified=True), 'NAL')


class MraTestCases(unittest.TestCase):
    """Test MRA functions.

    test cases for abydos.phonetic.mra
    """

    def test_mra(self):
        """Test abydos.phonetic.mra."""
        self.assertEqual(mra(''), '')

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEqual(mra('Byrne'), 'BYRN')
        self.assertEqual(mra('Boern'), 'BRN')
        self.assertEqual(mra('Smith'), 'SMTH')
        self.assertEqual(mra('Smyth'), 'SMYTH')
        self.assertEqual(mra('Catherine'), 'CTHRN')
        self.assertEqual(mra('Kathryn'), 'KTHRYN')


class MetaphoneTestCases(unittest.TestCase):
    """Test Metaphone functions.

    test cases for abydos.phonetic.metaphone
    """

    def test_metaphone(self):
        """Test abydos.phonetic.metaphone."""
        self.assertEqual(metaphone(''), '')
        self.assertEqual(metaphone('...'), '')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(metaphone('Fishpool', 4), 'FXPL')
        self.assertEqual(metaphone('Fishpoole', 4), 'FXPL')
        self.assertEqual(metaphone('Gellately', 4), 'JLTL')
        self.assertEqual(metaphone('Gelletly', 4), 'JLTL')
        self.assertEqual(metaphone('Lowers', 4), 'LWRS')
        self.assertEqual(metaphone('Lowerson', 4), 'LWRS')
        self.assertEqual(metaphone('Mallabar', 4), 'MLBR')
        self.assertEqual(metaphone('Melbert', 4), 'MLBR')
        self.assertEqual(metaphone('Melbourn', 4), 'MLBR')
        self.assertEqual(metaphone('Melbourne', 4), 'MLBR')
        self.assertEqual(metaphone('Melburg', 4), 'MLBR')
        self.assertEqual(metaphone('Melbury', 4), 'MLBR')
        self.assertEqual(metaphone('Milberry', 4), 'MLBR')
        self.assertEqual(metaphone('Milborn', 4), 'MLBR')
        self.assertEqual(metaphone('Milbourn', 4), 'MLBR')
        self.assertEqual(metaphone('Milbourne', 4), 'MLBR')
        self.assertEqual(metaphone('Milburn', 4), 'MLBR')
        self.assertEqual(metaphone('Milburne', 4), 'MLBR')
        self.assertEqual(metaphone('Millberg', 4), 'MLBR')
        self.assertEqual(metaphone('Mulberry', 4), 'MLBR')
        self.assertEqual(metaphone('Mulbery', 4), 'MLBR')
        self.assertEqual(metaphone('Mulbry', 4), 'MLBR')
        self.assertEqual(metaphone('Saipy', 4), 'SP')
        self.assertEqual(metaphone('Sapey', 4), 'SP')
        self.assertEqual(metaphone('Sapp', 4), 'SP')
        self.assertEqual(metaphone('Sappy', 4), 'SP')
        self.assertEqual(metaphone('Sepey', 4), 'SP')
        self.assertEqual(metaphone('Seppey', 4), 'SP')
        self.assertEqual(metaphone('Sopp', 4), 'SP')
        self.assertEqual(metaphone('Zoppie', 4), 'SP')
        self.assertEqual(metaphone('Zoppo', 4), 'SP')
        self.assertEqual(metaphone('Zupa', 4), 'SP')
        self.assertEqual(metaphone('Zupo', 4), 'SP')
        self.assertEqual(metaphone('Zuppa', 4), 'SP')

        # assorted tests to complete code coverage
        self.assertEqual(metaphone('Xavier'), 'SFR')
        self.assertEqual(metaphone('Acacia'), 'AKX')
        self.assertEqual(metaphone('Schuler'), 'SKLR')
        self.assertEqual(metaphone('Sign'), 'SN')
        self.assertEqual(metaphone('Signed'), 'SNT')
        self.assertEqual(metaphone('Horatio'), 'HRX')
        self.assertEqual(metaphone('Ignatio'), 'IKNX')
        self.assertEqual(metaphone('Lucretia'), 'LKRX')

        # assorted tests to complete branch coverage
        self.assertEqual(metaphone('Lamb'), 'LM')
        self.assertEqual(metaphone('science'), 'SNS')

        # maxlength bounds tests
        self.assertEqual(metaphone('Niall', maxlength=float('inf')), 'NL')
        self.assertEqual(metaphone('Niall', maxlength=None), 'NL')
        self.assertEqual(metaphone('Niall', maxlength=0), 'NL')


class DoubleMetaphoneTestCases(unittest.TestCase):
    """Test Double Metaphone functions.

    test cases for abydos.phonetic.double_metaphone

    These test cases are copied from two sources:
    https://github.com/oubiwann/metaphone/blob/master/metaphone/tests/test_metaphone.py
    and
    http://swoodbridge.com/DoubleMetaPhone/surnames.txt

    Most test cases other than those in test_surnames and test_surnames4 come
    from the former and are under the following license:

        Copyright (c) 2007 Andrew Collins, Chris Leong
        Copyright (c) 2009 Matthew Somerville
        Copyright (c) 2010 Maximillian Dornseif, Richard Barran
        Copyright (c) 2012 Duncan McGreggor
        All rights reserved.

         * Redistribution and use in source and binary forms, with or without
            modification, are permitted provided that the following conditions
            are met:

         * Redistributions of source code must retain the above copyright
             notice, this list of conditions and the following disclaimer.

         * Redistributions in binary form must reproduce the above copyright
            notice, this list of conditions and the following disclaimer in
            the documentation and/or other materials provided with the
            distribution.

        Neither the name "Metaphone" nor the names of its contributors may be
        used to endorse or promote products derived from this software without
        specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
        "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
        LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
        A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
        HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
        SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
        LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
        DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
        THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    test_surname and test_surname4 come from a set of tests for a PHP port
    of Double Metaphone that is Copyright 2001, Stephen Woodbridge and
    identified as 'freely distributable'
    """

    def test_double_metaphone(self):
        """Test abydos.phonetic.double_metaphone."""
        # base case
        self.assertEqual(double_metaphone(''), ('', ''))

        # single result
        self.assertEqual(double_metaphone('aubrey'), ('APR', ''))

        # double result
        self.assertEqual(double_metaphone('richard'), ('RXRT', 'RKRT'))

        # general word list
        self.assertEqual(double_metaphone('Jose'), ('HS', ''))
        self.assertEqual(double_metaphone('cambrillo'), ('KMPRL', 'KMPR'))
        self.assertEqual(double_metaphone('otto'), ('AT', ''))
        self.assertEqual(double_metaphone('aubrey'), ('APR', ''))
        self.assertEqual(double_metaphone('maurice'), ('MRS', ''))
        self.assertEqual(double_metaphone('auto'), ('AT', ''))
        self.assertEqual(double_metaphone('maisey'), ('MS', ''))
        self.assertEqual(double_metaphone('catherine'), ('K0RN', 'KTRN'))
        self.assertEqual(double_metaphone('geoff'), ('JF', 'KF'))
        self.assertEqual(double_metaphone('Chile'), ('XL', ''))
        self.assertEqual(double_metaphone('katherine'), ('K0RN', 'KTRN'))
        self.assertEqual(double_metaphone('steven'), ('STFN', ''))
        self.assertEqual(double_metaphone('zhang'), ('JNK', ''))
        self.assertEqual(double_metaphone('bob'), ('PP', ''))
        self.assertEqual(double_metaphone('ray'), ('R', ''))
        self.assertEqual(double_metaphone('Tux'), ('TKS', ''))
        self.assertEqual(double_metaphone('bryan'), ('PRN', ''))
        self.assertEqual(double_metaphone('bryce'), ('PRS', ''))
        self.assertEqual(double_metaphone('Rapelje'), ('RPL', ''))
        self.assertEqual(double_metaphone('richard'), ('RXRT', 'RKRT'))
        self.assertEqual(double_metaphone('solilijs'), ('SLLS', ''))
        self.assertEqual(double_metaphone('Dallas'), ('TLS', ''))
        self.assertEqual(double_metaphone('Schwein'), ('XN', 'XFN'))
        self.assertEqual(double_metaphone('dave'), ('TF', ''))
        self.assertEqual(double_metaphone('eric'), ('ARK', ''))
        self.assertEqual(double_metaphone('Parachute'), ('PRKT', ''))
        self.assertEqual(double_metaphone('brian'), ('PRN', ''))
        self.assertEqual(double_metaphone('randy'), ('RNT', ''))
        self.assertEqual(double_metaphone('Through'), ('0R', 'TR'))
        self.assertEqual(double_metaphone('Nowhere'), ('NR', ''))
        self.assertEqual(double_metaphone('heidi'), ('HT', ''))
        self.assertEqual(double_metaphone('Arnow'), ('ARN', 'ARNF'))
        self.assertEqual(double_metaphone('Thumbail'), ('0MPL', 'TMPL'))

        # homophones
        self.assertEqual(double_metaphone('tolled'), double_metaphone('told'))
        self.assertEqual(double_metaphone('katherine'),
                         double_metaphone('catherine'))
        self.assertEqual(double_metaphone('brian'), double_metaphone('bryan'))

        # similar names
        self.assertEqual(double_metaphone('Bartoš'), ('PRT', ''))
        self.assertEqual(double_metaphone('Bartosz'), ('PRTS', 'PRTX'))
        self.assertEqual(double_metaphone('Bartosch'), ('PRTX', ''))
        self.assertEqual(double_metaphone('Bartos'), ('PRTS', ''))
        self.assertEqual(list(set(double_metaphone('Jablonski'))
                              .intersection(double_metaphone('Yablonsky'))),
                         ['APLNSK'])
        self.assertEqual(list(set(double_metaphone('Smith'))
                              .intersection(double_metaphone('Schmidt'))),
                         ['XMT'])

        # non-English Unicode
        self.assertEqual(double_metaphone('andestādītu'), ('ANTSTTT', ''))

        # c-cedilla
        self.assertEqual(double_metaphone('français'), ('FRNS', 'FRNSS'))
        self.assertEqual(double_metaphone('garçon'), ('KRSN', ''))
        self.assertEqual(double_metaphone('leçon'), ('LSN', ''))

        # German words
        self.assertEqual(double_metaphone('ach'), ('AK', ''))
        self.assertEqual(double_metaphone('bacher'), ('PKR', ''))
        self.assertEqual(double_metaphone('macher'), ('MKR', ''))

        # Italian words
        self.assertEqual(double_metaphone('bacci'), ('PX', ''))
        self.assertEqual(double_metaphone('bertucci'), ('PRTX', ''))
        self.assertEqual(double_metaphone('bellocchio'), ('PLX', ''))
        self.assertEqual(double_metaphone('bacchus'), ('PKS', ''))
        self.assertEqual(double_metaphone('focaccia'), ('FKX', ''))
        self.assertEqual(double_metaphone('chianti'), ('KNT', ''))
        self.assertEqual(double_metaphone('tagliaro'), ('TKLR', 'TLR'))
        self.assertEqual(double_metaphone('biaggi'), ('PJ', 'PK'))

        # Spanish words
        self.assertEqual(double_metaphone('bajador'), ('PJTR', 'PHTR'))
        self.assertEqual(double_metaphone('cabrillo'), ('KPRL', 'KPR'))
        self.assertEqual(double_metaphone('gallegos'), ('KLKS', 'KKS'))
        self.assertEqual(double_metaphone('San Jacinto'), ('SNHSNT', ''))

        # French words
        self.assertEqual(double_metaphone('rogier'), ('RJ', 'RJR'))
        self.assertEqual(double_metaphone('breaux'), ('PR', ''))

        # Slavic words
        self.assertEqual(double_metaphone('Wewski'), ('ASK', 'FFSK'))

        # Chinese words
        self.assertEqual(double_metaphone('zhao'), ('J', ''))

        # Dutch-origin words
        self.assertEqual(double_metaphone('school'), ('SKL', ''))
        self.assertEqual(double_metaphone('schooner'), ('SKNR', ''))
        self.assertEqual(double_metaphone('schermerhorn'),
                         ('XRMRRN', 'SKRMRRN'))
        self.assertEqual(double_metaphone('schenker'), ('XNKR', 'SKNKR'))

        # <ch> words
        self.assertEqual(double_metaphone('Charac'), ('KRK', ''))
        self.assertEqual(double_metaphone('Charis'), ('KRS', ''))
        self.assertEqual(double_metaphone('chord'), ('KRT', ''))
        self.assertEqual(double_metaphone('Chym'), ('KM', ''))
        self.assertEqual(double_metaphone('Chia'), ('K', ''))
        self.assertEqual(double_metaphone('chem'), ('KM', ''))
        self.assertEqual(double_metaphone('chore'), ('XR', ''))
        self.assertEqual(double_metaphone('orchestra'), ('ARKSTR', ''))
        self.assertEqual(double_metaphone('architect'), ('ARKTKT', ''))
        self.assertEqual(double_metaphone('orchid'), ('ARKT', ''))

        # <cc> words
        self.assertEqual(double_metaphone('accident'), ('AKSTNT', ''))
        self.assertEqual(double_metaphone('accede'), ('AKST', ''))
        self.assertEqual(double_metaphone('succeed'), ('SKST', ''))

        # <mc> words
        self.assertEqual(double_metaphone('mac caffrey'), ('MKFR', ''))
        self.assertEqual(double_metaphone('mac gregor'), ('MKRKR', ''))
        self.assertEqual(double_metaphone('mc crae'), ('MKR', ''))
        self.assertEqual(double_metaphone('mcclain'), ('MKLN', ''))

        # <gh> words
        self.assertEqual(double_metaphone('laugh'), ('LF', ''))
        self.assertEqual(double_metaphone('cough'), ('KF', ''))
        self.assertEqual(double_metaphone('rough'), ('RF', ''))

        # <g__> words
        self.assertEqual(double_metaphone('gya'), ('K', 'J'))
        self.assertEqual(double_metaphone('ges'), ('KS', 'JS'))
        self.assertEqual(double_metaphone('gep'), ('KP', 'JP'))
        self.assertEqual(double_metaphone('geb'), ('KP', 'JP'))
        self.assertEqual(double_metaphone('gel'), ('KL', 'JL'))
        self.assertEqual(double_metaphone('gey'), ('K', 'J'))
        self.assertEqual(double_metaphone('gib'), ('KP', 'JP'))
        self.assertEqual(double_metaphone('gil'), ('KL', 'JL'))
        self.assertEqual(double_metaphone('gin'), ('KN', 'JN'))
        self.assertEqual(double_metaphone('gie'), ('K', 'J'))
        self.assertEqual(double_metaphone('gei'), ('K', 'J'))
        self.assertEqual(double_metaphone('ger'), ('KR', 'JR'))
        self.assertEqual(double_metaphone('danger'), ('TNJR', 'TNKR'))
        self.assertEqual(double_metaphone('manager'), ('MNKR', 'MNJR'))
        self.assertEqual(double_metaphone('dowager'), ('TKR', 'TJR'))

        # <pb> words
        self.assertEqual(double_metaphone('Campbell'), ('KMPL', ''))
        self.assertEqual(double_metaphone('raspberry'), ('RSPR', ''))

        # <th> words
        self.assertEqual(double_metaphone('Thomas'), ('TMS', ''))
        self.assertEqual(double_metaphone('Thames'), ('TMS', ''))

        # etc. (for code coverage)
        self.assertEqual(double_metaphone('Xavier'), ('SF', 'SFR'))
        self.assertEqual(double_metaphone('Michael'), ('MKL', 'MXL'))
        self.assertEqual(double_metaphone('Ignacio'), ('AKNS', 'ANX'))
        self.assertEqual(double_metaphone('Ajjam'), ('AJM', ''))
        self.assertEqual(double_metaphone('Akkad'), ('AKT', ''))
        self.assertEqual(double_metaphone('Año'), ('AN', ''))
        self.assertEqual(double_metaphone('Año'), double_metaphone('Anno'))
        self.assertEqual(double_metaphone('Caucasian'), ('KKSN', 'KKXN'))
        self.assertEqual(double_metaphone('Kaukasian'), ('KKSN', ''))
        self.assertEqual(double_metaphone('Zaqqum'), ('SKM', ''))
        self.assertEqual(double_metaphone('stevven'), ('STFN', ''))
        self.assertEqual(double_metaphone('Tuxx'), ('TKS', ''))
        self.assertEqual(double_metaphone('Ghiradelli'), ('JRTL', ''))
        self.assertEqual(double_metaphone('ghoul'), ('KL', ''))
        self.assertEqual(double_metaphone('hej'), ('HJ', 'H'))

        # maxlength bounds tests
        self.assertEqual(double_metaphone('Niall', maxlength=float('inf')),
                         ('NL', ''))
        self.assertEqual(double_metaphone('Niall', maxlength=None), ('NL', ''))
        self.assertEqual(double_metaphone('Niall', maxlength=0), ('NL', ''))

    def test_double_metaphone_surnames(self):
        """Test abydos.phonetic.double_metaphone (surname data)."""
        self.assertEqual(double_metaphone(''), ('', ''))
        self.assertEqual(double_metaphone('ALLERTON'), ('ALRTN', ''))
        self.assertEqual(double_metaphone('Acton'), ('AKTN', ''))
        self.assertEqual(double_metaphone('Adams'), ('ATMS', ''))
        self.assertEqual(double_metaphone('Aggar'), ('AKR', ''))
        self.assertEqual(double_metaphone('Ahl'), ('AL', ''))
        self.assertEqual(double_metaphone('Aiken'), ('AKN', ''))
        self.assertEqual(double_metaphone('Alan'), ('ALN', ''))
        self.assertEqual(double_metaphone('Alcock'), ('ALKK', ''))
        self.assertEqual(double_metaphone('Alden'), ('ALTN', ''))
        self.assertEqual(double_metaphone('Aldham'), ('ALTM', ''))
        self.assertEqual(double_metaphone('Allen'), ('ALN', ''))
        self.assertEqual(double_metaphone('Allerton'), ('ALRTN', ''))
        self.assertEqual(double_metaphone('Alsop'), ('ALSP', ''))
        self.assertEqual(double_metaphone('Alwein'), ('ALN', ''))
        self.assertEqual(double_metaphone('Ambler'), ('AMPLR', ''))
        self.assertEqual(double_metaphone('Andevill'), ('ANTFL', ''))
        self.assertEqual(double_metaphone('Andrews'), ('ANTRS', ''))
        self.assertEqual(double_metaphone('Andreyco'), ('ANTRK', ''))
        self.assertEqual(double_metaphone('Andriesse'), ('ANTRS', ''))
        self.assertEqual(double_metaphone('Angier'), ('ANJ', 'ANJR'))
        self.assertEqual(double_metaphone('Annabel'), ('ANPL', ''))
        self.assertEqual(double_metaphone('Anne'), ('AN', ''))
        self.assertEqual(double_metaphone('Anstye'), ('ANST', ''))
        self.assertEqual(double_metaphone('Appling'), ('APLNK', ''))
        self.assertEqual(double_metaphone('Apuke'), ('APK', ''))
        self.assertEqual(double_metaphone('Arnold'), ('ARNLT', ''))
        self.assertEqual(double_metaphone('Ashby'), ('AXP', ''))
        self.assertEqual(double_metaphone('Astwood'), ('ASTT', ''))
        self.assertEqual(double_metaphone('Atkinson'), ('ATKNSN', ''))
        self.assertEqual(double_metaphone('Audley'), ('ATL', ''))
        self.assertEqual(double_metaphone('Austin'), ('ASTN', ''))
        self.assertEqual(double_metaphone('Avenal'), ('AFNL', ''))
        self.assertEqual(double_metaphone('Ayer'), ('AR', ''))
        self.assertEqual(double_metaphone('Ayot'), ('AT', ''))
        self.assertEqual(double_metaphone('Babbitt'), ('PPT', ''))
        self.assertEqual(double_metaphone('Bachelor'), ('PXLR', 'PKLR'))
        self.assertEqual(double_metaphone('Bachelour'), ('PXLR', 'PKLR'))
        self.assertEqual(double_metaphone('Bailey'), ('PL', ''))
        self.assertEqual(double_metaphone('Baivel'), ('PFL', ''))
        self.assertEqual(double_metaphone('Baker'), ('PKR', ''))
        self.assertEqual(double_metaphone('Baldwin'), ('PLTN', ''))
        self.assertEqual(double_metaphone('Balsley'), ('PLSL', ''))
        self.assertEqual(double_metaphone('Barber'), ('PRPR', ''))
        self.assertEqual(double_metaphone('Barker'), ('PRKR', ''))
        self.assertEqual(double_metaphone('Barlow'), ('PRL', 'PRLF'))
        self.assertEqual(double_metaphone('Barnard'), ('PRNRT', ''))
        self.assertEqual(double_metaphone('Barnes'), ('PRNS', ''))
        self.assertEqual(double_metaphone('Barnsley'), ('PRNSL', ''))
        self.assertEqual(double_metaphone('Barouxis'), ('PRKSS', ''))
        self.assertEqual(double_metaphone('Bartlet'), ('PRTLT', ''))
        self.assertEqual(double_metaphone('Basley'), ('PSL', ''))
        self.assertEqual(double_metaphone('Basset'), ('PST', ''))
        self.assertEqual(double_metaphone('Bassett'), ('PST', ''))
        self.assertEqual(double_metaphone('Batchlor'), ('PXLR', ''))
        self.assertEqual(double_metaphone('Bates'), ('PTS', ''))
        self.assertEqual(double_metaphone('Batson'), ('PTSN', ''))
        self.assertEqual(double_metaphone('Bayes'), ('PS', ''))
        self.assertEqual(double_metaphone('Bayley'), ('PL', ''))
        self.assertEqual(double_metaphone('Beale'), ('PL', ''))
        self.assertEqual(double_metaphone('Beauchamp'), ('PXMP', 'PKMP'))
        self.assertEqual(double_metaphone('Beauclerc'), ('PKLRK', ''))
        self.assertEqual(double_metaphone('Beech'), ('PK', ''))
        self.assertEqual(double_metaphone('Beers'), ('PRS', ''))
        self.assertEqual(double_metaphone('Beke'), ('PK', ''))
        self.assertEqual(double_metaphone('Belcher'), ('PLXR', 'PLKR'))
        self.assertEqual(double_metaphone('Benjamin'), ('PNJMN', ''))
        self.assertEqual(double_metaphone('Benningham'), ('PNNKM', ''))
        self.assertEqual(double_metaphone('Bereford'), ('PRFRT', ''))
        self.assertEqual(double_metaphone('Bergen'), ('PRJN', 'PRKN'))
        self.assertEqual(double_metaphone('Berkeley'), ('PRKL', ''))
        self.assertEqual(double_metaphone('Berry'), ('PR', ''))
        self.assertEqual(double_metaphone('Besse'), ('PS', ''))
        self.assertEqual(double_metaphone('Bessey'), ('PS', ''))
        self.assertEqual(double_metaphone('Bessiles'), ('PSLS', ''))
        self.assertEqual(double_metaphone('Bigelow'), ('PJL', 'PKLF'))
        self.assertEqual(double_metaphone('Bigg'), ('PK', ''))
        self.assertEqual(double_metaphone('Bigod'), ('PKT', ''))
        self.assertEqual(double_metaphone('Billings'), ('PLNKS', ''))
        self.assertEqual(double_metaphone('Bimper'), ('PMPR', ''))
        self.assertEqual(double_metaphone('Binker'), ('PNKR', ''))
        self.assertEqual(double_metaphone('Birdsill'), ('PRTSL', ''))
        self.assertEqual(double_metaphone('Bishop'), ('PXP', ''))
        self.assertEqual(double_metaphone('Black'), ('PLK', ''))
        self.assertEqual(double_metaphone('Blagge'), ('PLK', ''))
        self.assertEqual(double_metaphone('Blake'), ('PLK', ''))
        self.assertEqual(double_metaphone('Blanck'), ('PLNK', ''))
        self.assertEqual(double_metaphone('Bledsoe'), ('PLTS', ''))
        self.assertEqual(double_metaphone('Blennerhasset'), ('PLNRST', ''))
        self.assertEqual(double_metaphone('Blessing'), ('PLSNK', ''))
        self.assertEqual(double_metaphone('Blewett'), ('PLT', ''))
        self.assertEqual(double_metaphone('Bloctgoed'), ('PLKTKT', ''))
        self.assertEqual(double_metaphone('Bloetgoet'), ('PLTKT', ''))
        self.assertEqual(double_metaphone('Bloodgood'), ('PLTKT', ''))
        self.assertEqual(double_metaphone('Blossom'), ('PLSM', ''))
        self.assertEqual(double_metaphone('Blount'), ('PLNT', ''))
        self.assertEqual(double_metaphone('Bodine'), ('PTN', ''))
        self.assertEqual(double_metaphone('Bodman'), ('PTMN', ''))
        self.assertEqual(double_metaphone('BonCoeur'), ('PNKR', ''))
        self.assertEqual(double_metaphone('Bond'), ('PNT', ''))
        self.assertEqual(double_metaphone('Boscawen'), ('PSKN', ''))
        self.assertEqual(double_metaphone('Bosworth'), ('PSR0', 'PSRT'))
        self.assertEqual(double_metaphone('Bouchier'), ('PX', 'PKR'))
        self.assertEqual(double_metaphone('Bowne'), ('PN', ''))
        self.assertEqual(double_metaphone('Bradbury'), ('PRTPR', ''))
        self.assertEqual(double_metaphone('Bradder'), ('PRTR', ''))
        self.assertEqual(double_metaphone('Bradford'), ('PRTFRT', ''))
        self.assertEqual(double_metaphone('Bradstreet'), ('PRTSTRT', ''))
        self.assertEqual(double_metaphone('Braham'), ('PRHM', ''))
        self.assertEqual(double_metaphone('Brailsford'), ('PRLSFRT', ''))
        self.assertEqual(double_metaphone('Brainard'), ('PRNRT', ''))
        self.assertEqual(double_metaphone('Brandish'), ('PRNTX', ''))
        self.assertEqual(double_metaphone('Braun'), ('PRN', ''))
        self.assertEqual(double_metaphone('Brecc'), ('PRK', ''))
        self.assertEqual(double_metaphone('Brent'), ('PRNT', ''))
        self.assertEqual(double_metaphone('Brenton'), ('PRNTN', ''))
        self.assertEqual(double_metaphone('Briggs'), ('PRKS', ''))
        self.assertEqual(double_metaphone('Brigham'), ('PRM', ''))
        self.assertEqual(double_metaphone('Brobst'), ('PRPST', ''))
        self.assertEqual(double_metaphone('Brome'), ('PRM', ''))
        self.assertEqual(double_metaphone('Bronson'), ('PRNSN', ''))
        self.assertEqual(double_metaphone('Brooks'), ('PRKS', ''))
        self.assertEqual(double_metaphone('Brouillard'), ('PRLRT', ''))
        self.assertEqual(double_metaphone('Brown'), ('PRN', ''))
        self.assertEqual(double_metaphone('Browne'), ('PRN', ''))
        self.assertEqual(double_metaphone('Brownell'), ('PRNL', ''))
        self.assertEqual(double_metaphone('Bruley'), ('PRL', ''))
        self.assertEqual(double_metaphone('Bryant'), ('PRNT', ''))
        self.assertEqual(double_metaphone('Brzozowski'),
                         ('PRSSSK', 'PRTSTSFSK'))
        self.assertEqual(double_metaphone('Buide'), ('PT', ''))
        self.assertEqual(double_metaphone('Bulmer'), ('PLMR', ''))
        self.assertEqual(double_metaphone('Bunker'), ('PNKR', ''))
        self.assertEqual(double_metaphone('Burden'), ('PRTN', ''))
        self.assertEqual(double_metaphone('Burge'), ('PRJ', 'PRK'))
        self.assertEqual(double_metaphone('Burgoyne'), ('PRKN', ''))
        self.assertEqual(double_metaphone('Burke'), ('PRK', ''))
        self.assertEqual(double_metaphone('Burnett'), ('PRNT', ''))
        self.assertEqual(double_metaphone('Burpee'), ('PRP', ''))
        self.assertEqual(double_metaphone('Bursley'), ('PRSL', ''))
        self.assertEqual(double_metaphone('Burton'), ('PRTN', ''))
        self.assertEqual(double_metaphone('Bushnell'), ('PXNL', ''))
        self.assertEqual(double_metaphone('Buss'), ('PS', ''))
        self.assertEqual(double_metaphone('Buswell'), ('PSL', ''))
        self.assertEqual(double_metaphone('Butler'), ('PTLR', ''))
        self.assertEqual(double_metaphone('Calkin'), ('KLKN', ''))
        self.assertEqual(double_metaphone('Canada'), ('KNT', ''))
        self.assertEqual(double_metaphone('Canmore'), ('KNMR', ''))
        self.assertEqual(double_metaphone('Canney'), ('KN', ''))
        self.assertEqual(double_metaphone('Capet'), ('KPT', ''))
        self.assertEqual(double_metaphone('Card'), ('KRT', ''))
        self.assertEqual(double_metaphone('Carman'), ('KRMN', ''))
        self.assertEqual(double_metaphone('Carpenter'), ('KRPNTR', ''))
        self.assertEqual(double_metaphone('Cartwright'), ('KRTRT', ''))
        self.assertEqual(double_metaphone('Casey'), ('KS', ''))
        self.assertEqual(double_metaphone('Catterfield'), ('KTRFLT', ''))
        self.assertEqual(double_metaphone('Ceeley'), ('SL', ''))
        self.assertEqual(double_metaphone('Chambers'), ('XMPRS', ''))
        self.assertEqual(double_metaphone('Champion'), ('XMPN', ''))
        self.assertEqual(double_metaphone('Chapman'), ('XPMN', ''))
        self.assertEqual(double_metaphone('Chase'), ('XS', ''))
        self.assertEqual(double_metaphone('Cheney'), ('XN', ''))
        self.assertEqual(double_metaphone('Chetwynd'), ('XTNT', ''))
        self.assertEqual(double_metaphone('Chevalier'), ('XFL', 'XFLR'))
        self.assertEqual(double_metaphone('Chillingsworth'),
                         ('XLNKSR0', 'XLNKSRT'))
        self.assertEqual(double_metaphone('Christie'), ('KRST', ''))
        self.assertEqual(double_metaphone('Chubbuck'), ('XPK', ''))
        self.assertEqual(double_metaphone('Church'), ('XRX', 'XRK'))
        self.assertEqual(double_metaphone('Clark'), ('KLRK', ''))
        self.assertEqual(double_metaphone('Clarke'), ('KLRK', ''))
        self.assertEqual(double_metaphone('Cleare'), ('KLR', ''))
        self.assertEqual(double_metaphone('Clement'), ('KLMNT', ''))
        self.assertEqual(double_metaphone('Clerke'), ('KLRK', ''))
        self.assertEqual(double_metaphone('Clibben'), ('KLPN', ''))
        self.assertEqual(double_metaphone('Clifford'), ('KLFRT', ''))
        self.assertEqual(double_metaphone('Clivedon'), ('KLFTN', ''))
        self.assertEqual(double_metaphone('Close'), ('KLS', ''))
        self.assertEqual(double_metaphone('Clothilde'), ('KL0LT', 'KLTLT'))
        self.assertEqual(double_metaphone('Cobb'), ('KP', ''))
        self.assertEqual(double_metaphone('Coburn'), ('KPRN', ''))
        self.assertEqual(double_metaphone('Coburne'), ('KPRN', ''))
        self.assertEqual(double_metaphone('Cocke'), ('KK', ''))
        self.assertEqual(double_metaphone('Coffin'), ('KFN', ''))
        self.assertEqual(double_metaphone('Coffyn'), ('KFN', ''))
        self.assertEqual(double_metaphone('Colborne'), ('KLPRN', ''))
        self.assertEqual(double_metaphone('Colby'), ('KLP', ''))
        self.assertEqual(double_metaphone('Cole'), ('KL', ''))
        self.assertEqual(double_metaphone('Coleman'), ('KLMN', ''))
        self.assertEqual(double_metaphone('Collier'), ('KL', 'KLR'))
        self.assertEqual(double_metaphone('Compton'), ('KMPTN', ''))
        self.assertEqual(double_metaphone('Cone'), ('KN', ''))
        self.assertEqual(double_metaphone('Cook'), ('KK', ''))
        self.assertEqual(double_metaphone('Cooke'), ('KK', ''))
        self.assertEqual(double_metaphone('Cooper'), ('KPR', ''))
        self.assertEqual(double_metaphone('Copperthwaite'), ('KPR0T', 'KPRTT'))
        self.assertEqual(double_metaphone('Corbet'), ('KRPT', ''))
        self.assertEqual(double_metaphone('Corell'), ('KRL', ''))
        self.assertEqual(double_metaphone('Corey'), ('KR', ''))
        self.assertEqual(double_metaphone('Corlies'), ('KRLS', ''))
        self.assertEqual(double_metaphone('Corneliszen'), ('KRNLSN', 'KRNLXN'))
        self.assertEqual(double_metaphone('Cornelius'), ('KRNLS', ''))
        self.assertEqual(double_metaphone('Cornwallis'), ('KRNLS', ''))
        self.assertEqual(double_metaphone('Cosgrove'), ('KSKRF', ''))
        self.assertEqual(double_metaphone('Count of Brionne'), ('KNTFPRN', ''))
        self.assertEqual(double_metaphone('Covill'), ('KFL', ''))
        self.assertEqual(double_metaphone('Cowperthwaite'), ('KPR0T', 'KPRTT'))
        self.assertEqual(double_metaphone('Cowperwaite'), ('KPRT', ''))
        self.assertEqual(double_metaphone('Crane'), ('KRN', ''))
        self.assertEqual(double_metaphone('Creagmile'), ('KRKML', ''))
        self.assertEqual(double_metaphone('Crew'), ('KR', 'KRF'))
        self.assertEqual(double_metaphone('Crispin'), ('KRSPN', ''))
        self.assertEqual(double_metaphone('Crocker'), ('KRKR', ''))
        self.assertEqual(double_metaphone('Crockett'), ('KRKT', ''))
        self.assertEqual(double_metaphone('Crosby'), ('KRSP', ''))
        self.assertEqual(double_metaphone('Crump'), ('KRMP', ''))
        self.assertEqual(double_metaphone('Cunningham'), ('KNNKM', ''))
        self.assertEqual(double_metaphone('Curtis'), ('KRTS', ''))
        self.assertEqual(double_metaphone('Cutha'), ('K0', 'KT'))
        self.assertEqual(double_metaphone('Cutter'), ('KTR', ''))
        self.assertEqual(double_metaphone('D\'Aubigny'), ('TPN', 'TPKN'))
        self.assertEqual(double_metaphone('DAVIS'), ('TFS', ''))
        self.assertEqual(double_metaphone('Dabinott'), ('TPNT', ''))
        self.assertEqual(double_metaphone('Dacre'), ('TKR', ''))
        self.assertEqual(double_metaphone('Daggett'), ('TKT', ''))
        self.assertEqual(double_metaphone('Danvers'), ('TNFRS', ''))
        self.assertEqual(double_metaphone('Darcy'), ('TRS', ''))
        self.assertEqual(double_metaphone('Davis'), ('TFS', ''))
        self.assertEqual(double_metaphone('Dawn'), ('TN', ''))
        self.assertEqual(double_metaphone('Dawson'), ('TSN', ''))
        self.assertEqual(double_metaphone('Day'), ('T', ''))
        self.assertEqual(double_metaphone('Daye'), ('T', ''))
        self.assertEqual(double_metaphone('DeGrenier'), ('TKRN', 'TKRNR'))
        self.assertEqual(double_metaphone('Dean'), ('TN', ''))
        self.assertEqual(double_metaphone('Deekindaugh'), ('TKNT', ''))
        self.assertEqual(double_metaphone('Dennis'), ('TNS', ''))
        self.assertEqual(double_metaphone('Denny'), ('TN', ''))
        self.assertEqual(double_metaphone('Denton'), ('TNTN', ''))
        self.assertEqual(double_metaphone('Desborough'), ('TSPRF', ''))
        self.assertEqual(double_metaphone('Despenser'), ('TSPNSR', ''))
        self.assertEqual(double_metaphone('Deverill'), ('TFRL', ''))
        self.assertEqual(double_metaphone('Devine'), ('TFN', ''))
        self.assertEqual(double_metaphone('Dexter'), ('TKSTR', ''))
        self.assertEqual(double_metaphone('Dillaway'), ('TL', ''))
        self.assertEqual(double_metaphone('Dimmick'), ('TMK', ''))
        self.assertEqual(double_metaphone('Dinan'), ('TNN', ''))
        self.assertEqual(double_metaphone('Dix'), ('TKS', ''))
        self.assertEqual(double_metaphone('Doggett'), ('TKT', ''))
        self.assertEqual(double_metaphone('Donahue'), ('TNH', ''))
        self.assertEqual(double_metaphone('Dorfman'), ('TRFMN', ''))
        self.assertEqual(double_metaphone('Dorris'), ('TRS', ''))
        self.assertEqual(double_metaphone('Dow'), ('T', 'TF'))
        self.assertEqual(double_metaphone('Downey'), ('TN', ''))
        self.assertEqual(double_metaphone('Downing'), ('TNNK', ''))
        self.assertEqual(double_metaphone('Dowsett'), ('TST', ''))
        self.assertEqual(double_metaphone('Duck?'), ('TK', ''))
        self.assertEqual(double_metaphone('Dudley'), ('TTL', ''))
        self.assertEqual(double_metaphone('Duffy'), ('TF', ''))
        self.assertEqual(double_metaphone('Dunn'), ('TN', ''))
        self.assertEqual(double_metaphone('Dunsterville'), ('TNSTRFL', ''))
        self.assertEqual(double_metaphone('Durrant'), ('TRNT', ''))
        self.assertEqual(double_metaphone('Durrin'), ('TRN', ''))
        self.assertEqual(double_metaphone('Dustin'), ('TSTN', ''))
        self.assertEqual(double_metaphone('Duston'), ('TSTN', ''))
        self.assertEqual(double_metaphone('Eames'), ('AMS', ''))
        self.assertEqual(double_metaphone('Early'), ('ARL', ''))
        self.assertEqual(double_metaphone('Easty'), ('AST', ''))
        self.assertEqual(double_metaphone('Ebbett'), ('APT', ''))
        self.assertEqual(double_metaphone('Eberbach'), ('APRPK', ''))
        self.assertEqual(double_metaphone('Eberhard'), ('APRRT', ''))
        self.assertEqual(double_metaphone('Eddy'), ('AT', ''))
        self.assertEqual(double_metaphone('Edenden'), ('ATNTN', ''))
        self.assertEqual(double_metaphone('Edwards'), ('ATRTS', ''))
        self.assertEqual(double_metaphone('Eglinton'), ('AKLNTN', 'ALNTN'))
        self.assertEqual(double_metaphone('Eliot'), ('ALT', ''))
        self.assertEqual(double_metaphone('Elizabeth'), ('ALSP0', 'ALSPT'))
        self.assertEqual(double_metaphone('Ellis'), ('ALS', ''))
        self.assertEqual(double_metaphone('Ellison'), ('ALSN', ''))
        self.assertEqual(double_metaphone('Ellot'), ('ALT', ''))
        self.assertEqual(double_metaphone('Elny'), ('ALN', ''))
        self.assertEqual(double_metaphone('Elsner'), ('ALSNR', ''))
        self.assertEqual(double_metaphone('Emerson'), ('AMRSN', ''))
        self.assertEqual(double_metaphone('Empson'), ('AMPSN', ''))
        self.assertEqual(double_metaphone('Est'), ('AST', ''))
        self.assertEqual(double_metaphone('Estabrook'), ('ASTPRK', ''))
        self.assertEqual(double_metaphone('Estes'), ('ASTS', ''))
        self.assertEqual(double_metaphone('Estey'), ('AST', ''))
        self.assertEqual(double_metaphone('Evans'), ('AFNS', ''))
        self.assertEqual(double_metaphone('Fallowell'), ('FLL', ''))
        self.assertEqual(double_metaphone('Farnsworth'), ('FRNSR0', 'FRNSRT'))
        self.assertEqual(double_metaphone('Feake'), ('FK', ''))
        self.assertEqual(double_metaphone('Feke'), ('FK', ''))
        self.assertEqual(double_metaphone('Fellows'), ('FLS', ''))
        self.assertEqual(double_metaphone('Fettiplace'), ('FTPLS', ''))
        self.assertEqual(double_metaphone('Finney'), ('FN', ''))
        self.assertEqual(double_metaphone('Fischer'), ('FXR', 'FSKR'))
        self.assertEqual(double_metaphone('Fisher'), ('FXR', ''))
        self.assertEqual(double_metaphone('Fisk'), ('FSK', ''))
        self.assertEqual(double_metaphone('Fiske'), ('FSK', ''))
        self.assertEqual(double_metaphone('Fletcher'), ('FLXR', ''))
        self.assertEqual(double_metaphone('Folger'), ('FLKR', 'FLJR'))
        self.assertEqual(double_metaphone('Foliot'), ('FLT', ''))
        self.assertEqual(double_metaphone('Folyot'), ('FLT', ''))
        self.assertEqual(double_metaphone('Fones'), ('FNS', ''))
        self.assertEqual(double_metaphone('Fordham'), ('FRTM', ''))
        self.assertEqual(double_metaphone('Forstner'), ('FRSTNR', ''))
        self.assertEqual(double_metaphone('Fosten'), ('FSTN', ''))
        self.assertEqual(double_metaphone('Foster'), ('FSTR', ''))
        self.assertEqual(double_metaphone('Foulke'), ('FLK', ''))
        self.assertEqual(double_metaphone('Fowler'), ('FLR', ''))
        self.assertEqual(double_metaphone('Foxwell'), ('FKSL', ''))
        self.assertEqual(double_metaphone('Fraley'), ('FRL', ''))
        self.assertEqual(double_metaphone('Franceys'), ('FRNSS', ''))
        self.assertEqual(double_metaphone('Franke'), ('FRNK', ''))
        self.assertEqual(double_metaphone('Frascella'), ('FRSL', ''))
        self.assertEqual(double_metaphone('Frazer'), ('FRSR', ''))
        self.assertEqual(double_metaphone('Fredd'), ('FRT', ''))
        self.assertEqual(double_metaphone('Freeman'), ('FRMN', ''))
        self.assertEqual(double_metaphone('French'), ('FRNX', 'FRNK'))
        self.assertEqual(double_metaphone('Freville'), ('FRFL', ''))
        self.assertEqual(double_metaphone('Frey'), ('FR', ''))
        self.assertEqual(double_metaphone('Frick'), ('FRK', ''))
        self.assertEqual(double_metaphone('Frier'), ('FR', 'FRR'))
        self.assertEqual(double_metaphone('Froe'), ('FR', ''))
        self.assertEqual(double_metaphone('Frorer'), ('FRRR', ''))
        self.assertEqual(double_metaphone('Frost'), ('FRST', ''))
        self.assertEqual(double_metaphone('Frothingham'), ('FR0NKM', 'FRTNKM'))
        self.assertEqual(double_metaphone('Fry'), ('FR', ''))
        self.assertEqual(double_metaphone('Gaffney'), ('KFN', ''))
        self.assertEqual(double_metaphone('Gage'), ('KJ', 'KK'))
        self.assertEqual(double_metaphone('Gallion'), ('KLN', ''))
        self.assertEqual(double_metaphone('Gallishan'), ('KLXN', ''))
        self.assertEqual(double_metaphone('Gamble'), ('KMPL', ''))
        self.assertEqual(double_metaphone('Garbrand'), ('KRPRNT', ''))
        self.assertEqual(double_metaphone('Gardner'), ('KRTNR', ''))
        self.assertEqual(double_metaphone('Garrett'), ('KRT', ''))
        self.assertEqual(double_metaphone('Gassner'), ('KSNR', ''))
        self.assertEqual(double_metaphone('Gater'), ('KTR', ''))
        self.assertEqual(double_metaphone('Gaunt'), ('KNT', ''))
        self.assertEqual(double_metaphone('Gayer'), ('KR', ''))
        self.assertEqual(double_metaphone('Gerken'), ('KRKN', 'JRKN'))
        self.assertEqual(double_metaphone('Gerritsen'), ('KRTSN', 'JRTSN'))
        self.assertEqual(double_metaphone('Gibbs'), ('KPS', 'JPS'))
        self.assertEqual(double_metaphone('Giffard'), ('JFRT', 'KFRT'))
        self.assertEqual(double_metaphone('Gilbert'), ('KLPRT', 'JLPRT'))
        self.assertEqual(double_metaphone('Gill'), ('KL', 'JL'))
        self.assertEqual(double_metaphone('Gilman'), ('KLMN', 'JLMN'))
        self.assertEqual(double_metaphone('Glass'), ('KLS', ''))
        self.assertEqual(double_metaphone('GoddardGifford'), ('KTRJFRT', ''))
        self.assertEqual(double_metaphone('Godfrey'), ('KTFR', ''))
        self.assertEqual(double_metaphone('Godwin'), ('KTN', ''))
        self.assertEqual(double_metaphone('Goodale'), ('KTL', ''))
        self.assertEqual(double_metaphone('Goodnow'), ('KTN', 'KTNF'))
        self.assertEqual(double_metaphone('Gorham'), ('KRM', ''))
        self.assertEqual(double_metaphone('Goseline'), ('KSLN', ''))
        self.assertEqual(double_metaphone('Gott'), ('KT', ''))
        self.assertEqual(double_metaphone('Gould'), ('KLT', ''))
        self.assertEqual(double_metaphone('Grafton'), ('KRFTN', ''))
        self.assertEqual(double_metaphone('Grant'), ('KRNT', ''))
        self.assertEqual(double_metaphone('Gray'), ('KR', ''))
        self.assertEqual(double_metaphone('Green'), ('KRN', ''))
        self.assertEqual(double_metaphone('Griffin'), ('KRFN', ''))
        self.assertEqual(double_metaphone('Grill'), ('KRL', ''))
        self.assertEqual(double_metaphone('Grim'), ('KRM', ''))
        self.assertEqual(double_metaphone('Grisgonelle'), ('KRSKNL', ''))
        self.assertEqual(double_metaphone('Gross'), ('KRS', ''))
        self.assertEqual(double_metaphone('Guba'), ('KP', ''))
        self.assertEqual(double_metaphone('Gybbes'), ('KPS', 'JPS'))
        self.assertEqual(double_metaphone('Haburne'), ('HPRN', ''))
        self.assertEqual(double_metaphone('Hackburne'), ('HKPRN', ''))
        self.assertEqual(double_metaphone('Haddon?'), ('HTN', ''))
        self.assertEqual(double_metaphone('Haines'), ('HNS', ''))
        self.assertEqual(double_metaphone('Hale'), ('HL', ''))
        self.assertEqual(double_metaphone('Hall'), ('HL', ''))
        self.assertEqual(double_metaphone('Hallet'), ('HLT', ''))
        self.assertEqual(double_metaphone('Hallock'), ('HLK', ''))
        self.assertEqual(double_metaphone('Halstead'), ('HLSTT', ''))
        self.assertEqual(double_metaphone('Hammond'), ('HMNT', ''))
        self.assertEqual(double_metaphone('Hance'), ('HNS', ''))
        self.assertEqual(double_metaphone('Handy'), ('HNT', ''))
        self.assertEqual(double_metaphone('Hanson'), ('HNSN', ''))
        self.assertEqual(double_metaphone('Harasek'), ('HRSK', ''))
        self.assertEqual(double_metaphone('Harcourt'), ('HRKRT', ''))
        self.assertEqual(double_metaphone('Hardy'), ('HRT', ''))
        self.assertEqual(double_metaphone('Harlock'), ('HRLK', ''))
        self.assertEqual(double_metaphone('Harris'), ('HRS', ''))
        self.assertEqual(double_metaphone('Hartley'), ('HRTL', ''))
        self.assertEqual(double_metaphone('Harvey'), ('HRF', ''))
        self.assertEqual(double_metaphone('Harvie'), ('HRF', ''))
        self.assertEqual(double_metaphone('Harwood'), ('HRT', ''))
        self.assertEqual(double_metaphone('Hathaway'), ('H0', 'HT'))
        self.assertEqual(double_metaphone('Haukeness'), ('HKNS', ''))
        self.assertEqual(double_metaphone('Hawkes'), ('HKS', ''))
        self.assertEqual(double_metaphone('Hawkhurst'), ('HKRST', ''))
        self.assertEqual(double_metaphone('Hawkins'), ('HKNS', ''))
        self.assertEqual(double_metaphone('Hawley'), ('HL', ''))
        self.assertEqual(double_metaphone('Heald'), ('HLT', ''))
        self.assertEqual(double_metaphone('Helsdon'), ('HLSTN', ''))
        self.assertEqual(double_metaphone('Hemenway'), ('HMN', ''))
        self.assertEqual(double_metaphone('Hemmenway'), ('HMN', ''))
        self.assertEqual(double_metaphone('Henck'), ('HNK', ''))
        self.assertEqual(double_metaphone('Henderson'), ('HNTRSN', ''))
        self.assertEqual(double_metaphone('Hendricks'), ('HNTRKS', ''))
        self.assertEqual(double_metaphone('Hersey'), ('HRS', ''))
        self.assertEqual(double_metaphone('Hewes'), ('HS', ''))
        self.assertEqual(double_metaphone('Heyman'), ('HMN', ''))
        self.assertEqual(double_metaphone('Hicks'), ('HKS', ''))
        self.assertEqual(double_metaphone('Hidden'), ('HTN', ''))
        self.assertEqual(double_metaphone('Higgs'), ('HKS', ''))
        self.assertEqual(double_metaphone('Hill'), ('HL', ''))
        self.assertEqual(double_metaphone('Hills'), ('HLS', ''))
        self.assertEqual(double_metaphone('Hinckley'), ('HNKL', ''))
        self.assertEqual(double_metaphone('Hipwell'), ('HPL', ''))
        self.assertEqual(double_metaphone('Hobart'), ('HPRT', ''))
        self.assertEqual(double_metaphone('Hoben'), ('HPN', ''))
        self.assertEqual(double_metaphone('Hoffmann'), ('HFMN', ''))
        self.assertEqual(double_metaphone('Hogan'), ('HKN', ''))
        self.assertEqual(double_metaphone('Holmes'), ('HLMS', ''))
        self.assertEqual(double_metaphone('Hoo'), ('H', ''))
        self.assertEqual(double_metaphone('Hooker'), ('HKR', ''))
        self.assertEqual(double_metaphone('Hopcott'), ('HPKT', ''))
        self.assertEqual(double_metaphone('Hopkins'), ('HPKNS', ''))
        self.assertEqual(double_metaphone('Hopkinson'), ('HPKNSN', ''))
        self.assertEqual(double_metaphone('Hornsey'), ('HRNS', ''))
        self.assertEqual(double_metaphone('Houckgeest'), ('HKJST', 'HKKST'))
        self.assertEqual(double_metaphone('Hough'), ('H', ''))
        self.assertEqual(double_metaphone('Houstin'), ('HSTN', ''))
        self.assertEqual(double_metaphone('How'), ('H', 'HF'))
        self.assertEqual(double_metaphone('Howe'), ('H', ''))
        self.assertEqual(double_metaphone('Howland'), ('HLNT', ''))
        self.assertEqual(double_metaphone('Hubner'), ('HPNR', ''))
        self.assertEqual(double_metaphone('Hudnut'), ('HTNT', ''))
        self.assertEqual(double_metaphone('Hughes'), ('HS', ''))
        self.assertEqual(double_metaphone('Hull'), ('HL', ''))
        self.assertEqual(double_metaphone('Hulme'), ('HLM', ''))
        self.assertEqual(double_metaphone('Hume'), ('HM', ''))
        self.assertEqual(double_metaphone('Hundertumark'), ('HNTRTMRK', ''))
        self.assertEqual(double_metaphone('Hundley'), ('HNTL', ''))
        self.assertEqual(double_metaphone('Hungerford'),
                         ('HNKRFRT', 'HNJRFRT'))
        self.assertEqual(double_metaphone('Hunt'), ('HNT', ''))
        self.assertEqual(double_metaphone('Hurst'), ('HRST', ''))
        self.assertEqual(double_metaphone('Husbands'), ('HSPNTS', ''))
        self.assertEqual(double_metaphone('Hussey'), ('HS', ''))
        self.assertEqual(double_metaphone('Husted'), ('HSTT', ''))
        self.assertEqual(double_metaphone('Hutchins'), ('HXNS', ''))
        self.assertEqual(double_metaphone('Hutchinson'), ('HXNSN', ''))
        self.assertEqual(double_metaphone('Huttinger'), ('HTNKR', 'HTNJR'))
        self.assertEqual(double_metaphone('Huybertsen'), ('HPRTSN', ''))
        self.assertEqual(double_metaphone('Iddenden'), ('ATNTN', ''))
        self.assertEqual(double_metaphone('Ingraham'), ('ANKRHM', ''))
        self.assertEqual(double_metaphone('Ives'), ('AFS', ''))
        self.assertEqual(double_metaphone('Jackson'), ('JKSN', 'AKSN'))
        self.assertEqual(double_metaphone('Jacob'), ('JKP', 'AKP'))
        self.assertEqual(double_metaphone('Jans'), ('JNS', 'ANS'))
        self.assertEqual(double_metaphone('Jenkins'), ('JNKNS', 'ANKNS'))
        self.assertEqual(double_metaphone('Jewett'), ('JT', 'AT'))
        self.assertEqual(double_metaphone('Jewitt'), ('JT', 'AT'))
        self.assertEqual(double_metaphone('Johnson'), ('JNSN', 'ANSN'))
        self.assertEqual(double_metaphone('Jones'), ('JNS', 'ANS'))
        self.assertEqual(double_metaphone('Josephine'), ('JSFN', 'HSFN'))
        self.assertEqual(double_metaphone('Judd'), ('JT', 'AT'))
        self.assertEqual(double_metaphone('June'), ('JN', 'AN'))
        self.assertEqual(double_metaphone('Kamarowska'), ('KMRSK', ''))
        self.assertEqual(double_metaphone('Kay'), ('K', ''))
        self.assertEqual(double_metaphone('Kelley'), ('KL', ''))
        self.assertEqual(double_metaphone('Kelly'), ('KL', ''))
        self.assertEqual(double_metaphone('Keymber'), ('KMPR', ''))
        self.assertEqual(double_metaphone('Keynes'), ('KNS', ''))
        self.assertEqual(double_metaphone('Kilham'), ('KLM', ''))
        self.assertEqual(double_metaphone('Kim'), ('KM', ''))
        self.assertEqual(double_metaphone('Kimball'), ('KMPL', ''))
        self.assertEqual(double_metaphone('King'), ('KNK', ''))
        self.assertEqual(double_metaphone('Kinsey'), ('KNS', ''))
        self.assertEqual(double_metaphone('Kirk'), ('KRK', ''))
        self.assertEqual(double_metaphone('Kirton'), ('KRTN', ''))
        self.assertEqual(double_metaphone('Kistler'), ('KSTLR', ''))
        self.assertEqual(double_metaphone('Kitchen'), ('KXN', ''))
        self.assertEqual(double_metaphone('Kitson'), ('KTSN', ''))
        self.assertEqual(double_metaphone('Klett'), ('KLT', ''))
        self.assertEqual(double_metaphone('Kline'), ('KLN', ''))
        self.assertEqual(double_metaphone('Knapp'), ('NP', ''))
        self.assertEqual(double_metaphone('Knight'), ('NT', ''))
        self.assertEqual(double_metaphone('Knote'), ('NT', ''))
        self.assertEqual(double_metaphone('Knott'), ('NT', ''))
        self.assertEqual(double_metaphone('Knox'), ('NKS', ''))
        self.assertEqual(double_metaphone('Koeller'), ('KLR', ''))
        self.assertEqual(double_metaphone('La Pointe'), ('LPNT', ''))
        self.assertEqual(double_metaphone('LaPlante'), ('LPLNT', ''))
        self.assertEqual(double_metaphone('Laimbeer'), ('LMPR', ''))
        self.assertEqual(double_metaphone('Lamb'), ('LMP', ''))
        self.assertEqual(double_metaphone('Lambertson'), ('LMPRTSN', ''))
        self.assertEqual(double_metaphone('Lancto'), ('LNKT', ''))
        self.assertEqual(double_metaphone('Landry'), ('LNTR', ''))
        self.assertEqual(double_metaphone('Lane'), ('LN', ''))
        self.assertEqual(double_metaphone('Langendyck'), ('LNJNTK', 'LNKNTK'))
        self.assertEqual(double_metaphone('Langer'), ('LNKR', 'LNJR'))
        self.assertEqual(double_metaphone('Langford'), ('LNKFRT', ''))
        self.assertEqual(double_metaphone('Lantersee'), ('LNTRS', ''))
        self.assertEqual(double_metaphone('Laquer'), ('LKR', ''))
        self.assertEqual(double_metaphone('Larkin'), ('LRKN', ''))
        self.assertEqual(double_metaphone('Latham'), ('LTM', ''))
        self.assertEqual(double_metaphone('Lathrop'), ('L0RP', 'LTRP'))
        self.assertEqual(double_metaphone('Lauter'), ('LTR', ''))
        self.assertEqual(double_metaphone('Lawrence'), ('LRNS', ''))
        self.assertEqual(double_metaphone('Leach'), ('LK', ''))
        self.assertEqual(double_metaphone('Leager'), ('LKR', 'LJR'))
        self.assertEqual(double_metaphone('Learned'), ('LRNT', ''))
        self.assertEqual(double_metaphone('Leavitt'), ('LFT', ''))
        self.assertEqual(double_metaphone('Lee'), ('L', ''))
        self.assertEqual(double_metaphone('Leete'), ('LT', ''))
        self.assertEqual(double_metaphone('Leggett'), ('LKT', ''))
        self.assertEqual(double_metaphone('Leland'), ('LLNT', ''))
        self.assertEqual(double_metaphone('Leonard'), ('LNRT', ''))
        self.assertEqual(double_metaphone('Lester'), ('LSTR', ''))
        self.assertEqual(double_metaphone('Lestrange'), ('LSTRNJ', 'LSTRNK'))
        self.assertEqual(double_metaphone('Lethem'), ('L0M', 'LTM'))
        self.assertEqual(double_metaphone('Levine'), ('LFN', ''))
        self.assertEqual(double_metaphone('Lewes'), ('LS', ''))
        self.assertEqual(double_metaphone('Lewis'), ('LS', ''))
        self.assertEqual(double_metaphone('Lincoln'), ('LNKLN', ''))
        self.assertEqual(double_metaphone('Lindsey'), ('LNTS', ''))
        self.assertEqual(double_metaphone('Linher'), ('LNR', ''))
        self.assertEqual(double_metaphone('Lippet'), ('LPT', ''))
        self.assertEqual(double_metaphone('Lippincott'), ('LPNKT', ''))
        self.assertEqual(double_metaphone('Lockwood'), ('LKT', ''))
        self.assertEqual(double_metaphone('Loines'), ('LNS', ''))
        self.assertEqual(double_metaphone('Lombard'), ('LMPRT', ''))
        self.assertEqual(double_metaphone('Long'), ('LNK', ''))
        self.assertEqual(double_metaphone('Longespee'), ('LNJSP', 'LNKSP'))
        self.assertEqual(double_metaphone('Look'), ('LK', ''))
        self.assertEqual(double_metaphone('Lounsberry'), ('LNSPR', ''))
        self.assertEqual(double_metaphone('Lounsbury'), ('LNSPR', ''))
        self.assertEqual(double_metaphone('Louthe'), ('L0', 'LT'))
        self.assertEqual(double_metaphone('Loveyne'), ('LFN', ''))
        self.assertEqual(double_metaphone('Lowe'), ('L', ''))
        self.assertEqual(double_metaphone('Ludlam'), ('LTLM', ''))
        self.assertEqual(double_metaphone('Lumbard'), ('LMPRT', ''))
        self.assertEqual(double_metaphone('Lund'), ('LNT', ''))
        self.assertEqual(double_metaphone('Luno'), ('LN', ''))
        self.assertEqual(double_metaphone('Lutz'), ('LTS', ''))
        self.assertEqual(double_metaphone('Lydia'), ('LT', ''))
        self.assertEqual(double_metaphone('Lynne'), ('LN', ''))
        self.assertEqual(double_metaphone('Lyon'), ('LN', ''))
        self.assertEqual(double_metaphone('MacAlpin'), ('MKLPN', ''))
        self.assertEqual(double_metaphone('MacBricc'), ('MKPRK', ''))
        self.assertEqual(double_metaphone('MacCrinan'), ('MKRNN', ''))
        self.assertEqual(double_metaphone('MacKenneth'), ('MKN0', 'MKNT'))
        self.assertEqual(double_metaphone('MacMael nam Bo'), ('MKMLNMP', ''))
        self.assertEqual(double_metaphone('MacMurchada'), ('MKMRXT', 'MKMRKT'))
        self.assertEqual(double_metaphone('Macomber'), ('MKMPR', ''))
        self.assertEqual(double_metaphone('Macy'), ('MS', ''))
        self.assertEqual(double_metaphone('Magnus'), ('MNS', 'MKNS'))
        self.assertEqual(double_metaphone('Mahien'), ('MHN', ''))
        self.assertEqual(double_metaphone('Malmains'), ('MLMNS', ''))
        self.assertEqual(double_metaphone('Malory'), ('MLR', ''))
        self.assertEqual(double_metaphone('Mancinelli'), ('MNSNL', ''))
        self.assertEqual(double_metaphone('Mancini'), ('MNSN', ''))
        self.assertEqual(double_metaphone('Mann'), ('MN', ''))
        self.assertEqual(double_metaphone('Manning'), ('MNNK', ''))
        self.assertEqual(double_metaphone('Manter'), ('MNTR', ''))
        self.assertEqual(double_metaphone('Marion'), ('MRN', ''))
        self.assertEqual(double_metaphone('Marley'), ('MRL', ''))
        self.assertEqual(double_metaphone('Marmion'), ('MRMN', ''))
        self.assertEqual(double_metaphone('Marquart'), ('MRKRT', ''))
        self.assertEqual(double_metaphone('Marsh'), ('MRX', ''))
        self.assertEqual(double_metaphone('Marshal'), ('MRXL', ''))
        self.assertEqual(double_metaphone('Marshall'), ('MRXL', ''))
        self.assertEqual(double_metaphone('Martel'), ('MRTL', ''))
        self.assertEqual(double_metaphone('Martha'), ('MR0', 'MRT'))
        self.assertEqual(double_metaphone('Martin'), ('MRTN', ''))
        self.assertEqual(double_metaphone('Marturano'), ('MRTRN', ''))
        self.assertEqual(double_metaphone('Marvin'), ('MRFN', ''))
        self.assertEqual(double_metaphone('Mary'), ('MR', ''))
        self.assertEqual(double_metaphone('Mason'), ('MSN', ''))
        self.assertEqual(double_metaphone('Maxwell'), ('MKSL', ''))
        self.assertEqual(double_metaphone('Mayhew'), ('MH', 'MHF'))
        self.assertEqual(double_metaphone('McAllaster'), ('MKLSTR', ''))
        self.assertEqual(double_metaphone('McAllister'), ('MKLSTR', ''))
        self.assertEqual(double_metaphone('McConnell'), ('MKNL', ''))
        self.assertEqual(double_metaphone('McFarland'), ('MKFRLNT', ''))
        self.assertEqual(double_metaphone('McIlroy'), ('MSLR', ''))
        self.assertEqual(double_metaphone('McNair'), ('MKNR', ''))
        self.assertEqual(double_metaphone('McNair-Landry'), ('MKNRLNTR', ''))
        self.assertEqual(double_metaphone('McRaven'), ('MKRFN', ''))
        self.assertEqual(double_metaphone('Mead'), ('MT', ''))
        self.assertEqual(double_metaphone('Meade'), ('MT', ''))
        self.assertEqual(double_metaphone('Meck'), ('MK', ''))
        self.assertEqual(double_metaphone('Melton'), ('MLTN', ''))
        self.assertEqual(double_metaphone('Mendenhall'), ('MNTNL', ''))
        self.assertEqual(double_metaphone('Mering'), ('MRNK', ''))
        self.assertEqual(double_metaphone('Merrick'), ('MRK', ''))
        self.assertEqual(double_metaphone('Merry'), ('MR', ''))
        self.assertEqual(double_metaphone('Mighill'), ('ML', ''))
        self.assertEqual(double_metaphone('Miller'), ('MLR', ''))
        self.assertEqual(double_metaphone('Milton'), ('MLTN', ''))
        self.assertEqual(double_metaphone('Mohun'), ('MHN', ''))
        self.assertEqual(double_metaphone('Montague'), ('MNTK', ''))
        self.assertEqual(double_metaphone('Montboucher'), ('MNTPXR', 'MNTPKR'))
        self.assertEqual(double_metaphone('Moore'), ('MR', ''))
        self.assertEqual(double_metaphone('Morrel'), ('MRL', ''))
        self.assertEqual(double_metaphone('Morrill'), ('MRL', ''))
        self.assertEqual(double_metaphone('Morris'), ('MRS', ''))
        self.assertEqual(double_metaphone('Morton'), ('MRTN', ''))
        self.assertEqual(double_metaphone('Moton'), ('MTN', ''))
        self.assertEqual(double_metaphone('Muir'), ('MR', ''))
        self.assertEqual(double_metaphone('Mulferd'), ('MLFRT', ''))
        self.assertEqual(double_metaphone('Mullins'), ('MLNS', ''))
        self.assertEqual(double_metaphone('Mulso'), ('MLS', ''))
        self.assertEqual(double_metaphone('Munger'), ('MNKR', 'MNJR'))
        self.assertEqual(double_metaphone('Munt'), ('MNT', ''))
        self.assertEqual(double_metaphone('Murchad'), ('MRXT', 'MRKT'))
        self.assertEqual(double_metaphone('Murdock'), ('MRTK', ''))
        self.assertEqual(double_metaphone('Murray'), ('MR', ''))
        self.assertEqual(double_metaphone('Muskett'), ('MSKT', ''))
        self.assertEqual(double_metaphone('Myers'), ('MRS', ''))
        self.assertEqual(double_metaphone('Myrick'), ('MRK', ''))
        self.assertEqual(double_metaphone('NORRIS'), ('NRS', ''))
        self.assertEqual(double_metaphone('Nayle'), ('NL', ''))
        self.assertEqual(double_metaphone('Newcomb'), ('NKMP', ''))
        self.assertEqual(double_metaphone('Newcomb(e)'), ('NKMP', ''))
        self.assertEqual(double_metaphone('Newkirk'), ('NKRK', ''))
        self.assertEqual(double_metaphone('Newton'), ('NTN', ''))
        self.assertEqual(double_metaphone('Niles'), ('NLS', ''))
        self.assertEqual(double_metaphone('Noble'), ('NPL', ''))
        self.assertEqual(double_metaphone('Noel'), ('NL', ''))
        self.assertEqual(double_metaphone('Northend'), ('NR0NT', 'NRTNT'))
        self.assertEqual(double_metaphone('Norton'), ('NRTN', ''))
        self.assertEqual(double_metaphone('Nutter'), ('NTR', ''))
        self.assertEqual(double_metaphone('Odding'), ('ATNK', ''))
        self.assertEqual(double_metaphone('Odenbaugh'), ('ATNP', ''))
        self.assertEqual(double_metaphone('Ogborn'), ('AKPRN', ''))
        self.assertEqual(double_metaphone('Oppenheimer'), ('APNMR', ''))
        self.assertEqual(double_metaphone('Otis'), ('ATS', ''))
        self.assertEqual(double_metaphone('Oviatt'), ('AFT', ''))
        self.assertEqual(double_metaphone('PRUST?'), ('PRST', ''))
        self.assertEqual(double_metaphone('Paddock'), ('PTK', ''))
        self.assertEqual(double_metaphone('Page'), ('PJ', 'PK'))
        self.assertEqual(double_metaphone('Paine'), ('PN', ''))
        self.assertEqual(double_metaphone('Paist'), ('PST', ''))
        self.assertEqual(double_metaphone('Palmer'), ('PLMR', ''))
        self.assertEqual(double_metaphone('Park'), ('PRK', ''))
        self.assertEqual(double_metaphone('Parker'), ('PRKR', ''))
        self.assertEqual(double_metaphone('Parkhurst'), ('PRKRST', ''))
        self.assertEqual(double_metaphone('Parrat'), ('PRT', ''))
        self.assertEqual(double_metaphone('Parsons'), ('PRSNS', ''))
        self.assertEqual(double_metaphone('Partridge'), ('PRTRJ', ''))
        self.assertEqual(double_metaphone('Pashley'), ('PXL', ''))
        self.assertEqual(double_metaphone('Pasley'), ('PSL', ''))
        self.assertEqual(double_metaphone('Patrick'), ('PTRK', ''))
        self.assertEqual(double_metaphone('Pattee'), ('PT', ''))
        self.assertEqual(double_metaphone('Patten'), ('PTN', ''))
        self.assertEqual(double_metaphone('Pawley'), ('PL', ''))
        self.assertEqual(double_metaphone('Payne'), ('PN', ''))
        self.assertEqual(double_metaphone('Peabody'), ('PPT', ''))
        self.assertEqual(double_metaphone('Peake'), ('PK', ''))
        self.assertEqual(double_metaphone('Pearson'), ('PRSN', ''))
        self.assertEqual(double_metaphone('Peat'), ('PT', ''))
        self.assertEqual(double_metaphone('Pedersen'), ('PTRSN', ''))
        self.assertEqual(double_metaphone('Percy'), ('PRS', ''))
        self.assertEqual(double_metaphone('Perkins'), ('PRKNS', ''))
        self.assertEqual(double_metaphone('Perrine'), ('PRN', ''))
        self.assertEqual(double_metaphone('Perry'), ('PR', ''))
        self.assertEqual(double_metaphone('Peson'), ('PSN', ''))
        self.assertEqual(double_metaphone('Peterson'), ('PTRSN', ''))
        self.assertEqual(double_metaphone('Peyton'), ('PTN', ''))
        self.assertEqual(double_metaphone('Phinney'), ('FN', ''))
        self.assertEqual(double_metaphone('Pickard'), ('PKRT', ''))
        self.assertEqual(double_metaphone('Pierce'), ('PRS', ''))
        self.assertEqual(double_metaphone('Pierrepont'), ('PRPNT', ''))
        self.assertEqual(double_metaphone('Pike'), ('PK', ''))
        self.assertEqual(double_metaphone('Pinkham'), ('PNKM', ''))
        self.assertEqual(double_metaphone('Pitman'), ('PTMN', ''))
        self.assertEqual(double_metaphone('Pitt'), ('PT', ''))
        self.assertEqual(double_metaphone('Pitts'), ('PTS', ''))
        self.assertEqual(double_metaphone('Plantagenet'),
                         ('PLNTJNT', 'PLNTKNT'))
        self.assertEqual(double_metaphone('Platt'), ('PLT', ''))
        self.assertEqual(double_metaphone('Platts'), ('PLTS', ''))
        self.assertEqual(double_metaphone('Pleis'), ('PLS', ''))
        self.assertEqual(double_metaphone('Pleiss'), ('PLS', ''))
        self.assertEqual(double_metaphone('Plisko'), ('PLSK', ''))
        self.assertEqual(double_metaphone('Pliskovitch'), ('PLSKFX', ''))
        self.assertEqual(double_metaphone('Plum'), ('PLM', ''))
        self.assertEqual(double_metaphone('Plume'), ('PLM', ''))
        self.assertEqual(double_metaphone('Poitou'), ('PT', ''))
        self.assertEqual(double_metaphone('Pomeroy'), ('PMR', ''))
        self.assertEqual(double_metaphone('Poretiers'), ('PRTRS', ''))
        self.assertEqual(double_metaphone('Pote'), ('PT', ''))
        self.assertEqual(double_metaphone('Potter'), ('PTR', ''))
        self.assertEqual(double_metaphone('Potts'), ('PTS', ''))
        self.assertEqual(double_metaphone('Powell'), ('PL', ''))
        self.assertEqual(double_metaphone('Pratt'), ('PRT', ''))
        self.assertEqual(double_metaphone('Presbury'), ('PRSPR', ''))
        self.assertEqual(double_metaphone('Priest'), ('PRST', ''))
        self.assertEqual(double_metaphone('Prindle'), ('PRNTL', ''))
        self.assertEqual(double_metaphone('Prior'), ('PRR', ''))
        self.assertEqual(double_metaphone('Profumo'), ('PRFM', ''))
        self.assertEqual(double_metaphone('Purdy'), ('PRT', ''))
        self.assertEqual(double_metaphone('Purefoy'), ('PRF', ''))
        self.assertEqual(double_metaphone('Pury'), ('PR', ''))
        self.assertEqual(double_metaphone('Quinter'), ('KNTR', ''))
        self.assertEqual(double_metaphone('Rachel'), ('RXL', 'RKL'))
        self.assertEqual(double_metaphone('Rand'), ('RNT', ''))
        self.assertEqual(double_metaphone('Rankin'), ('RNKN', ''))
        self.assertEqual(double_metaphone('Ravenscroft'), ('RFNSKFT', ''))
        self.assertEqual(double_metaphone('Raynsford'), ('RNSFRT', ''))
        self.assertEqual(double_metaphone('Reakirt'), ('RKRT', ''))
        self.assertEqual(double_metaphone('Reaves'), ('RFS', ''))
        self.assertEqual(double_metaphone('Reeves'), ('RFS', ''))
        self.assertEqual(double_metaphone('Reichert'), ('RXRT', 'RKRT'))
        self.assertEqual(double_metaphone('Remmele'), ('RML', ''))
        self.assertEqual(double_metaphone('Reynolds'), ('RNLTS', ''))
        self.assertEqual(double_metaphone('Rhodes'), ('RTS', ''))
        self.assertEqual(double_metaphone('Richards'), ('RXRTS', 'RKRTS'))
        self.assertEqual(double_metaphone('Richardson'), ('RXRTSN', 'RKRTSN'))
        self.assertEqual(double_metaphone('Ring'), ('RNK', ''))
        self.assertEqual(double_metaphone('Roberts'), ('RPRTS', ''))
        self.assertEqual(double_metaphone('Robertson'), ('RPRTSN', ''))
        self.assertEqual(double_metaphone('Robson'), ('RPSN', ''))
        self.assertEqual(double_metaphone('Rodie'), ('RT', ''))
        self.assertEqual(double_metaphone('Rody'), ('RT', ''))
        self.assertEqual(double_metaphone('Rogers'), ('RKRS', 'RJRS'))
        self.assertEqual(double_metaphone('Ross'), ('RS', ''))
        self.assertEqual(double_metaphone('Rosslevin'), ('RSLFN', ''))
        self.assertEqual(double_metaphone('Rowland'), ('RLNT', ''))
        self.assertEqual(double_metaphone('Ruehl'), ('RL', ''))
        self.assertEqual(double_metaphone('Russell'), ('RSL', ''))
        self.assertEqual(double_metaphone('Ruth'), ('R0', 'RT'))
        self.assertEqual(double_metaphone('Ryan'), ('RN', ''))
        self.assertEqual(double_metaphone('Rysse'), ('RS', ''))
        self.assertEqual(double_metaphone('Sadler'), ('STLR', ''))
        self.assertEqual(double_metaphone('Salmon'), ('SLMN', ''))
        self.assertEqual(double_metaphone('Salter'), ('SLTR', ''))
        self.assertEqual(double_metaphone('Salvatore'), ('SLFTR', ''))
        self.assertEqual(double_metaphone('Sanders'), ('SNTRS', ''))
        self.assertEqual(double_metaphone('Sands'), ('SNTS', ''))
        self.assertEqual(double_metaphone('Sanford'), ('SNFRT', ''))
        self.assertEqual(double_metaphone('Sanger'), ('SNKR', 'SNJR'))
        self.assertEqual(double_metaphone('Sargent'), ('SRJNT', 'SRKNT'))
        self.assertEqual(double_metaphone('Saunders'), ('SNTRS', ''))
        self.assertEqual(double_metaphone('Schilling'), ('XLNK', ''))
        self.assertEqual(double_metaphone('Schlegel'), ('XLKL', 'SLKL'))
        self.assertEqual(double_metaphone('Scott'), ('SKT', ''))
        self.assertEqual(double_metaphone('Sears'), ('SRS', ''))
        self.assertEqual(double_metaphone('Segersall'), ('SJRSL', 'SKRSL'))
        self.assertEqual(double_metaphone('Senecal'), ('SNKL', ''))
        self.assertEqual(double_metaphone('Sergeaux'), ('SRJ', 'SRK'))
        self.assertEqual(double_metaphone('Severance'), ('SFRNS', ''))
        self.assertEqual(double_metaphone('Sharp'), ('XRP', ''))
        self.assertEqual(double_metaphone('Sharpe'), ('XRP', ''))
        self.assertEqual(double_metaphone('Sharply'), ('XRPL', ''))
        self.assertEqual(double_metaphone('Shatswell'), ('XTSL', ''))
        self.assertEqual(double_metaphone('Shattack'), ('XTK', ''))
        self.assertEqual(double_metaphone('Shattock'), ('XTK', ''))
        self.assertEqual(double_metaphone('Shattuck'), ('XTK', ''))
        self.assertEqual(double_metaphone('Shaw'), ('X', 'XF'))
        self.assertEqual(double_metaphone('Sheldon'), ('XLTN', ''))
        self.assertEqual(double_metaphone('Sherman'), ('XRMN', ''))
        self.assertEqual(double_metaphone('Shinn'), ('XN', ''))
        self.assertEqual(double_metaphone('Shirford'), ('XRFRT', ''))
        self.assertEqual(double_metaphone('Shirley'), ('XRL', ''))
        self.assertEqual(double_metaphone('Shively'), ('XFL', ''))
        self.assertEqual(double_metaphone('Shoemaker'), ('XMKR', ''))
        self.assertEqual(double_metaphone('Short'), ('XRT', ''))
        self.assertEqual(double_metaphone('Shotwell'), ('XTL', ''))
        self.assertEqual(double_metaphone('Shute'), ('XT', ''))
        self.assertEqual(double_metaphone('Sibley'), ('SPL', ''))
        self.assertEqual(double_metaphone('Silver'), ('SLFR', ''))
        self.assertEqual(double_metaphone('Simes'), ('SMS', ''))
        self.assertEqual(double_metaphone('Sinken'), ('SNKN', ''))
        self.assertEqual(double_metaphone('Sinn'), ('SN', ''))
        self.assertEqual(double_metaphone('Skelton'), ('SKLTN', ''))
        self.assertEqual(double_metaphone('Skiffe'), ('SKF', ''))
        self.assertEqual(double_metaphone('Skotkonung'), ('SKTKNNK', ''))
        self.assertEqual(double_metaphone('Slade'), ('SLT', 'XLT'))
        self.assertEqual(double_metaphone('Slye'), ('SL', 'XL'))
        self.assertEqual(double_metaphone('Smedley'), ('SMTL', 'XMTL'))
        self.assertEqual(double_metaphone('Smith'), ('SM0', 'XMT'))
        self.assertEqual(double_metaphone('Snow'), ('SN', 'XNF'))
        self.assertEqual(double_metaphone('Soole'), ('SL', ''))
        self.assertEqual(double_metaphone('Soule'), ('SL', ''))
        self.assertEqual(double_metaphone('Southworth'), ('S0R0', 'STRT'))
        self.assertEqual(double_metaphone('Sowles'), ('SLS', ''))
        self.assertEqual(double_metaphone('Spalding'), ('SPLTNK', ''))
        self.assertEqual(double_metaphone('Spark'), ('SPRK', ''))
        self.assertEqual(double_metaphone('Spencer'), ('SPNSR', ''))
        self.assertEqual(double_metaphone('Sperry'), ('SPR', ''))
        self.assertEqual(double_metaphone('Spofford'), ('SPFRT', ''))
        self.assertEqual(double_metaphone('Spooner'), ('SPNR', ''))
        self.assertEqual(double_metaphone('Sprague'), ('SPRK', ''))
        self.assertEqual(double_metaphone('Springer'), ('SPRNKR', 'SPRNJR'))
        self.assertEqual(double_metaphone('St. Clair'), ('STKLR', ''))
        self.assertEqual(double_metaphone('St. Claire'), ('STKLR', ''))
        self.assertEqual(double_metaphone('St. Leger'), ('STLJR', 'STLKR'))
        self.assertEqual(double_metaphone('St. Omer'), ('STMR', ''))
        self.assertEqual(double_metaphone('Stafferton'), ('STFRTN', ''))
        self.assertEqual(double_metaphone('Stafford'), ('STFRT', ''))
        self.assertEqual(double_metaphone('Stalham'), ('STLM', ''))
        self.assertEqual(double_metaphone('Stanford'), ('STNFRT', ''))
        self.assertEqual(double_metaphone('Stanton'), ('STNTN', ''))
        self.assertEqual(double_metaphone('Star'), ('STR', ''))
        self.assertEqual(double_metaphone('Starbuck'), ('STRPK', ''))
        self.assertEqual(double_metaphone('Starkey'), ('STRK', ''))
        self.assertEqual(double_metaphone('Starkweather'),
                         ('STRK0R', 'STRKTR'))
        self.assertEqual(double_metaphone('Stearns'), ('STRNS', ''))
        self.assertEqual(double_metaphone('Stebbins'), ('STPNS', ''))
        self.assertEqual(double_metaphone('Steele'), ('STL', ''))
        self.assertEqual(double_metaphone('Stephenson'), ('STFNSN', ''))
        self.assertEqual(double_metaphone('Stevens'), ('STFNS', ''))
        self.assertEqual(double_metaphone('Stoddard'), ('STTRT', ''))
        self.assertEqual(double_metaphone('Stodder'), ('STTR', ''))
        self.assertEqual(double_metaphone('Stone'), ('STN', ''))
        self.assertEqual(double_metaphone('Storey'), ('STR', ''))
        self.assertEqual(double_metaphone('Storrada'), ('STRT', ''))
        self.assertEqual(double_metaphone('Story'), ('STR', ''))
        self.assertEqual(double_metaphone('Stoughton'), ('STFTN', ''))
        self.assertEqual(double_metaphone('Stout'), ('STT', ''))
        self.assertEqual(double_metaphone('Stow'), ('ST', 'STF'))
        self.assertEqual(double_metaphone('Strong'), ('STRNK', ''))
        self.assertEqual(double_metaphone('Strutt'), ('STRT', ''))
        self.assertEqual(double_metaphone('Stryker'), ('STRKR', ''))
        self.assertEqual(double_metaphone('Stuckeley'), ('STKL', ''))
        self.assertEqual(double_metaphone('Sturges'), ('STRJS', 'STRKS'))
        self.assertEqual(double_metaphone('Sturgess'), ('STRJS', 'STRKS'))
        self.assertEqual(double_metaphone('Sturgis'), ('STRJS', 'STRKS'))
        self.assertEqual(double_metaphone('Suevain'), ('SFN', ''))
        self.assertEqual(double_metaphone('Sulyard'), ('SLRT', ''))
        self.assertEqual(double_metaphone('Sutton'), ('STN', ''))
        self.assertEqual(double_metaphone('Swain'), ('SN', 'XN'))
        self.assertEqual(double_metaphone('Swayne'), ('SN', 'XN'))
        self.assertEqual(double_metaphone('Swayze'), ('SS', 'XTS'))
        self.assertEqual(double_metaphone('Swift'), ('SFT', 'XFT'))
        self.assertEqual(double_metaphone('Taber'), ('TPR', ''))
        self.assertEqual(double_metaphone('Talcott'), ('TLKT', ''))
        self.assertEqual(double_metaphone('Tarne'), ('TRN', ''))
        self.assertEqual(double_metaphone('Tatum'), ('TTM', ''))
        self.assertEqual(double_metaphone('Taverner'), ('TFRNR', ''))
        self.assertEqual(double_metaphone('Taylor'), ('TLR', ''))
        self.assertEqual(double_metaphone('Tenney'), ('TN', ''))
        self.assertEqual(double_metaphone('Thayer'), ('0R', 'TR'))
        self.assertEqual(double_metaphone('Thember'), ('0MPR', 'TMPR'))
        self.assertEqual(double_metaphone('Thomas'), ('TMS', ''))
        self.assertEqual(double_metaphone('Thompson'), ('TMPSN', ''))
        self.assertEqual(double_metaphone('Thorne'), ('0RN', 'TRN'))
        self.assertEqual(double_metaphone('Thornycraft'),
                         ('0RNKRFT', 'TRNKRFT'))
        self.assertEqual(double_metaphone('Threlkeld'), ('0RLKLT', 'TRLKLT'))
        self.assertEqual(double_metaphone('Throckmorton'),
                         ('0RKMRTN', 'TRKMRTN'))
        self.assertEqual(double_metaphone('Thwaits'), ('0TS', 'TTS'))
        self.assertEqual(double_metaphone('Tibbetts'), ('TPTS', ''))
        self.assertEqual(double_metaphone('Tidd'), ('TT', ''))
        self.assertEqual(double_metaphone('Tierney'), ('TRN', ''))
        self.assertEqual(double_metaphone('Tilley'), ('TL', ''))
        self.assertEqual(double_metaphone('Tillieres'), ('TLRS', ''))
        self.assertEqual(double_metaphone('Tilly'), ('TL', ''))
        self.assertEqual(double_metaphone('Tisdale'), ('TSTL', ''))
        self.assertEqual(double_metaphone('Titus'), ('TTS', ''))
        self.assertEqual(double_metaphone('Tobey'), ('TP', ''))
        self.assertEqual(double_metaphone('Tooker'), ('TKR', ''))
        self.assertEqual(double_metaphone('Towle'), ('TL', ''))
        self.assertEqual(double_metaphone('Towne'), ('TN', ''))
        self.assertEqual(double_metaphone('Townsend'), ('TNSNT', ''))
        self.assertEqual(double_metaphone('Treadway'), ('TRT', ''))
        self.assertEqual(double_metaphone('Trelawney'), ('TRLN', ''))
        self.assertEqual(double_metaphone('Trinder'), ('TRNTR', ''))
        self.assertEqual(double_metaphone('Tripp'), ('TRP', ''))
        self.assertEqual(double_metaphone('Trippe'), ('TRP', ''))
        self.assertEqual(double_metaphone('Trott'), ('TRT', ''))
        self.assertEqual(double_metaphone('True'), ('TR', ''))
        self.assertEqual(double_metaphone('Trussebut'), ('TRSPT', ''))
        self.assertEqual(double_metaphone('Tucker'), ('TKR', ''))
        self.assertEqual(double_metaphone('Turgeon'), ('TRJN', 'TRKN'))
        self.assertEqual(double_metaphone('Turner'), ('TRNR', ''))
        self.assertEqual(double_metaphone('Tuttle'), ('TTL', ''))
        self.assertEqual(double_metaphone('Tyler'), ('TLR', ''))
        self.assertEqual(double_metaphone('Tylle'), ('TL', ''))
        self.assertEqual(double_metaphone('Tyrrel'), ('TRL', ''))
        self.assertEqual(double_metaphone('Ua Tuathail'), ('AT0L', 'ATTL'))
        self.assertEqual(double_metaphone('Ulrich'), ('ALRX', 'ALRK'))
        self.assertEqual(double_metaphone('Underhill'), ('ANTRL', ''))
        self.assertEqual(double_metaphone('Underwood'), ('ANTRT', ''))
        self.assertEqual(double_metaphone('Unknown'), ('ANKNN', ''))
        self.assertEqual(double_metaphone('Valentine'), ('FLNTN', ''))
        self.assertEqual(double_metaphone('Van Egmond'), ('FNKMNT', ''))
        self.assertEqual(double_metaphone('Van der Beek'), ('FNTRPK', ''))
        self.assertEqual(double_metaphone('Vaughan'), ('FKN', ''))
        self.assertEqual(double_metaphone('Vermenlen'), ('FRMNLN', ''))
        self.assertEqual(double_metaphone('Vincent'), ('FNSNT', ''))
        self.assertEqual(double_metaphone('Volentine'), ('FLNTN', ''))
        self.assertEqual(double_metaphone('Wagner'), ('AKNR', 'FKNR'))
        self.assertEqual(double_metaphone('Waite'), ('AT', 'FT'))
        self.assertEqual(double_metaphone('Walker'), ('ALKR', 'FLKR'))
        self.assertEqual(double_metaphone('Walter'), ('ALTR', 'FLTR'))
        self.assertEqual(double_metaphone('Wandell'), ('ANTL', 'FNTL'))
        self.assertEqual(double_metaphone('Wandesford'),
                         ('ANTSFRT', 'FNTSFRT'))
        self.assertEqual(double_metaphone('Warbleton'), ('ARPLTN', 'FRPLTN'))
        self.assertEqual(double_metaphone('Ward'), ('ART', 'FRT'))
        self.assertEqual(double_metaphone('Warde'), ('ART', 'FRT'))
        self.assertEqual(double_metaphone('Ware'), ('AR', 'FR'))
        self.assertEqual(double_metaphone('Wareham'), ('ARHM', 'FRHM'))
        self.assertEqual(double_metaphone('Warner'), ('ARNR', 'FRNR'))
        self.assertEqual(double_metaphone('Warren'), ('ARN', 'FRN'))
        self.assertEqual(double_metaphone('Washburne'), ('AXPRN', 'FXPRN'))
        self.assertEqual(double_metaphone('Waterbury'), ('ATRPR', 'FTRPR'))
        self.assertEqual(double_metaphone('Watson'), ('ATSN', 'FTSN'))
        self.assertEqual(double_metaphone('WatsonEllithorpe'),
                         ('ATSNL0RP', 'FTSNLTRP'))
        self.assertEqual(double_metaphone('Watts'), ('ATS', 'FTS'))
        self.assertEqual(double_metaphone('Wayne'), ('AN', 'FN'))
        self.assertEqual(double_metaphone('Webb'), ('AP', 'FP'))
        self.assertEqual(double_metaphone('Weber'), ('APR', 'FPR'))
        self.assertEqual(double_metaphone('Webster'), ('APSTR', 'FPSTR'))
        self.assertEqual(double_metaphone('Weed'), ('AT', 'FT'))
        self.assertEqual(double_metaphone('Weeks'), ('AKS', 'FKS'))
        self.assertEqual(double_metaphone('Wells'), ('ALS', 'FLS'))
        self.assertEqual(double_metaphone('Wenzell'), ('ANSL', 'FNTSL'))
        self.assertEqual(double_metaphone('West'), ('AST', 'FST'))
        self.assertEqual(double_metaphone('Westbury'), ('ASTPR', 'FSTPR'))
        self.assertEqual(double_metaphone('Whatlocke'), ('ATLK', ''))
        self.assertEqual(double_metaphone('Wheeler'), ('ALR', ''))
        self.assertEqual(double_metaphone('Whiston'), ('ASTN', ''))
        self.assertEqual(double_metaphone('White'), ('AT', ''))
        self.assertEqual(double_metaphone('Whitman'), ('ATMN', ''))
        self.assertEqual(double_metaphone('Whiton'), ('ATN', ''))
        self.assertEqual(double_metaphone('Whitson'), ('ATSN', ''))
        self.assertEqual(double_metaphone('Wickes'), ('AKS', 'FKS'))
        self.assertEqual(double_metaphone('Wilbur'), ('ALPR', 'FLPR'))
        self.assertEqual(double_metaphone('Wilcotes'), ('ALKTS', 'FLKTS'))
        self.assertEqual(double_metaphone('Wilkinson'), ('ALKNSN', 'FLKNSN'))
        self.assertEqual(double_metaphone('Willets'), ('ALTS', 'FLTS'))
        self.assertEqual(double_metaphone('Willett'), ('ALT', 'FLT'))
        self.assertEqual(double_metaphone('Willey'), ('AL', 'FL'))
        self.assertEqual(double_metaphone('Williams'), ('ALMS', 'FLMS'))
        self.assertEqual(double_metaphone('Williston'), ('ALSTN', 'FLSTN'))
        self.assertEqual(double_metaphone('Wilson'), ('ALSN', 'FLSN'))
        self.assertEqual(double_metaphone('Wimes'), ('AMS', 'FMS'))
        self.assertEqual(double_metaphone('Winch'), ('ANX', 'FNK'))
        self.assertEqual(double_metaphone('Winegar'), ('ANKR', 'FNKR'))
        self.assertEqual(double_metaphone('Wing'), ('ANK', 'FNK'))
        self.assertEqual(double_metaphone('Winsley'), ('ANSL', 'FNSL'))
        self.assertEqual(double_metaphone('Winslow'), ('ANSL', 'FNSLF'))
        self.assertEqual(double_metaphone('Winthrop'), ('AN0RP', 'FNTRP'))
        self.assertEqual(double_metaphone('Wise'), ('AS', 'FS'))
        self.assertEqual(double_metaphone('Wood'), ('AT', 'FT'))
        self.assertEqual(double_metaphone('Woodbridge'), ('ATPRJ', 'FTPRJ'))
        self.assertEqual(double_metaphone('Woodward'), ('ATRT', 'FTRT'))
        self.assertEqual(double_metaphone('Wooley'), ('AL', 'FL'))
        self.assertEqual(double_metaphone('Woolley'), ('AL', 'FL'))
        self.assertEqual(double_metaphone('Worth'), ('AR0', 'FRT'))
        self.assertEqual(double_metaphone('Worthen'), ('AR0N', 'FRTN'))
        self.assertEqual(double_metaphone('Worthley'), ('AR0L', 'FRTL'))
        self.assertEqual(double_metaphone('Wright'), ('RT', ''))
        self.assertEqual(double_metaphone('Wyer'), ('AR', 'FR'))
        self.assertEqual(double_metaphone('Wyere'), ('AR', 'FR'))
        self.assertEqual(double_metaphone('Wynkoop'), ('ANKP', 'FNKP'))
        self.assertEqual(double_metaphone('Yarnall'), ('ARNL', ''))
        self.assertEqual(double_metaphone('Yeoman'), ('AMN', ''))
        self.assertEqual(double_metaphone('Yorke'), ('ARK', ''))
        self.assertEqual(double_metaphone('Young'), ('ANK', ''))
        self.assertEqual(double_metaphone('ab Wennonwen'), ('APNNN', ''))
        self.assertEqual(double_metaphone('ap Llewellyn'), ('APLLN', ''))
        self.assertEqual(double_metaphone('ap Lorwerth'), ('APLRR0', 'APLRRT'))
        self.assertEqual(double_metaphone('d\'Angouleme'), ('TNKLM', ''))
        self.assertEqual(double_metaphone('de Audeham'), ('TTHM', ''))
        self.assertEqual(double_metaphone('de Bavant'), ('TPFNT', ''))
        self.assertEqual(double_metaphone('de Beauchamp'), ('TPXMP', 'TPKMP'))
        self.assertEqual(double_metaphone('de Beaumont'), ('TPMNT', ''))
        self.assertEqual(double_metaphone('de Bolbec'), ('TPLPK', ''))
        self.assertEqual(double_metaphone('de Braiose'), ('TPRS', ''))
        self.assertEqual(double_metaphone('de Braose'), ('TPRS', ''))
        self.assertEqual(double_metaphone('de Briwere'), ('TPRR', ''))
        self.assertEqual(double_metaphone('de Cantelou'), ('TKNTL', ''))
        self.assertEqual(double_metaphone('de Cherelton'),
                         ('TXRLTN', 'TKRLTN'))
        self.assertEqual(double_metaphone('de Cherleton'),
                         ('TXRLTN', 'TKRLTN'))
        self.assertEqual(double_metaphone('de Clare'), ('TKLR', ''))
        self.assertEqual(double_metaphone('de Claremont'), ('TKLRMNT', ''))
        self.assertEqual(double_metaphone('de Clifford'), ('TKLFRT', ''))
        self.assertEqual(double_metaphone('de Colville'), ('TKLFL', ''))
        self.assertEqual(double_metaphone('de Courtenay'), ('TKRTN', ''))
        self.assertEqual(double_metaphone('de Fauconberg'), ('TFKNPRK', ''))
        self.assertEqual(double_metaphone('de Forest'), ('TFRST', ''))
        self.assertEqual(double_metaphone('de Gai'), ('TK', ''))
        self.assertEqual(double_metaphone('de Grey'), ('TKR', ''))
        self.assertEqual(double_metaphone('de Guernons'), ('TKRNNS', ''))
        self.assertEqual(double_metaphone('de Haia'), ('T', ''))
        self.assertEqual(double_metaphone('de Harcourt'), ('TRKRT', ''))
        self.assertEqual(double_metaphone('de Hastings'), ('TSTNKS', ''))
        self.assertEqual(double_metaphone('de Hoke'), ('TK', ''))
        self.assertEqual(double_metaphone('de Hooch'), ('TK', ''))
        self.assertEqual(double_metaphone('de Hugelville'), ('TJLFL', 'TKLFL'))
        self.assertEqual(double_metaphone('de Huntingdon'), ('TNTNKTN', ''))
        self.assertEqual(double_metaphone('de Insula'), ('TNSL', ''))
        self.assertEqual(double_metaphone('de Keynes'), ('TKNS', ''))
        self.assertEqual(double_metaphone('de Lacy'), ('TLS', ''))
        self.assertEqual(double_metaphone('de Lexington'), ('TLKSNKTN', ''))
        self.assertEqual(double_metaphone('de Lusignan'), ('TLSNN', 'TLSKNN'))
        self.assertEqual(double_metaphone('de Manvers'), ('TMNFRS', ''))
        self.assertEqual(double_metaphone('de Montagu'), ('TMNTK', ''))
        self.assertEqual(double_metaphone('de Montault'), ('TMNTLT', ''))
        self.assertEqual(double_metaphone('de Montfort'), ('TMNTFRT', ''))
        self.assertEqual(double_metaphone('de Mortimer'), ('TMRTMR', ''))
        self.assertEqual(double_metaphone('de Morville'), ('TMRFL', ''))
        self.assertEqual(double_metaphone('de Morvois'), ('TMRF', 'TMRFS'))
        self.assertEqual(double_metaphone('de Neufmarche'),
                         ('TNFMRX', 'TNFMRK'))
        self.assertEqual(double_metaphone('de Odingsells'), ('TTNKSLS', ''))
        self.assertEqual(double_metaphone('de Odyngsells'), ('TTNKSLS', ''))
        self.assertEqual(double_metaphone('de Percy'), ('TPRS', ''))
        self.assertEqual(double_metaphone('de Pierrepont'), ('TPRPNT', ''))
        self.assertEqual(double_metaphone('de Plessetis'), ('TPLSTS', ''))
        self.assertEqual(double_metaphone('de Porhoet'), ('TPRT', ''))
        self.assertEqual(double_metaphone('de Prouz'), ('TPRS', ''))
        self.assertEqual(double_metaphone('de Quincy'), ('TKNS', ''))
        self.assertEqual(double_metaphone('de Ripellis'), ('TRPLS', ''))
        self.assertEqual(double_metaphone('de Ros'), ('TRS', ''))
        self.assertEqual(double_metaphone('de Salisbury'), ('TSLSPR', ''))
        self.assertEqual(double_metaphone('de Sanford'), ('TSNFRT', ''))
        self.assertEqual(double_metaphone('de Somery'), ('TSMR', ''))
        self.assertEqual(double_metaphone('de St. Hilary'), ('TSTLR', ''))
        self.assertEqual(double_metaphone('de St. Liz'), ('TSTLS', ''))
        self.assertEqual(double_metaphone('de Sutton'), ('TSTN', ''))
        self.assertEqual(double_metaphone('de Toeni'), ('TTN', ''))
        self.assertEqual(double_metaphone('de Tony'), ('TTN', ''))
        self.assertEqual(double_metaphone('de Umfreville'), ('TMFRFL', ''))
        self.assertEqual(double_metaphone('de Valognes'), ('TFLNS', 'TFLKNS'))
        self.assertEqual(double_metaphone('de Vaux'), ('TF', ''))
        self.assertEqual(double_metaphone('de Vere'), ('TFR', ''))
        self.assertEqual(double_metaphone('de Vermandois'),
                         ('TFRMNT', 'TFRMNTS'))
        self.assertEqual(double_metaphone('de Vernon'), ('TFRNN', ''))
        self.assertEqual(double_metaphone('de Vexin'), ('TFKSN', ''))
        self.assertEqual(double_metaphone('de Vitre'), ('TFTR', ''))
        self.assertEqual(double_metaphone('de Wandesford'), ('TNTSFRT', ''))
        self.assertEqual(double_metaphone('de Warenne'), ('TRN', ''))
        self.assertEqual(double_metaphone('de Westbury'), ('TSTPR', ''))
        self.assertEqual(double_metaphone('di Saluzzo'), ('TSLS', 'TSLTS'))
        self.assertEqual(double_metaphone('fitz Alan'), ('FTSLN', ''))
        self.assertEqual(double_metaphone('fitz Geoffrey'),
                         ('FTSJFR', 'FTSKFR'))
        self.assertEqual(double_metaphone('fitz Herbert'), ('FTSRPRT', ''))
        self.assertEqual(double_metaphone('fitz John'), ('FTSJN', ''))
        self.assertEqual(double_metaphone('fitz Patrick'), ('FTSPTRK', ''))
        self.assertEqual(double_metaphone('fitz Payn'), ('FTSPN', ''))
        self.assertEqual(double_metaphone('fitz Piers'), ('FTSPRS', ''))
        self.assertEqual(double_metaphone('fitz Randolph'), ('FTSRNTLF', ''))
        self.assertEqual(double_metaphone('fitz Richard'),
                         ('FTSRXRT', 'FTSRKRT'))
        self.assertEqual(double_metaphone('fitz Robert'), ('FTSRPRT', ''))
        self.assertEqual(double_metaphone('fitz Roy'), ('FTSR', ''))
        self.assertEqual(double_metaphone('fitz Scrob'), ('FTSSKP', ''))
        self.assertEqual(double_metaphone('fitz Walter'), ('FTSLTR', ''))
        self.assertEqual(double_metaphone('fitz Warin'), ('FTSRN', ''))
        self.assertEqual(double_metaphone('fitz Williams'), ('FTSLMS', ''))
        self.assertEqual(double_metaphone('la Zouche'), ('LSX', 'LSK'))
        self.assertEqual(double_metaphone('le Botiller'), ('LPTLR', ''))
        self.assertEqual(double_metaphone('le Despenser'), ('LTSPNSR', ''))
        self.assertEqual(double_metaphone('le deSpencer'), ('LTSPNSR', ''))
        self.assertEqual(double_metaphone('of Allendale'), ('AFLNTL', ''))
        self.assertEqual(double_metaphone('of Angouleme'), ('AFNKLM', ''))
        self.assertEqual(double_metaphone('of Anjou'), ('AFNJ', ''))
        self.assertEqual(double_metaphone('of Aquitaine'), ('AFKTN', ''))
        self.assertEqual(double_metaphone('of Aumale'), ('AFML', ''))
        self.assertEqual(double_metaphone('of Bavaria'), ('AFPFR', ''))
        self.assertEqual(double_metaphone('of Boulogne'), ('AFPLN', 'AFPLKN'))
        self.assertEqual(double_metaphone('of Brittany'), ('AFPRTN', ''))
        self.assertEqual(double_metaphone('of Brittary'), ('AFPRTR', ''))
        self.assertEqual(double_metaphone('of Castile'), ('AFKSTL', ''))
        self.assertEqual(double_metaphone('of Chester'), ('AFXSTR', 'AFKSTR'))
        self.assertEqual(double_metaphone('of Clermont'), ('AFKLRMNT', ''))
        self.assertEqual(double_metaphone('of Cologne'), ('AFKLN', 'AFKLKN'))
        self.assertEqual(double_metaphone('of Dinan'), ('AFTNN', ''))
        self.assertEqual(double_metaphone('of Dunbar'), ('AFTNPR', ''))
        self.assertEqual(double_metaphone('of England'), ('AFNKLNT', ''))
        self.assertEqual(double_metaphone('of Essex'), ('AFSKS', ''))
        self.assertEqual(double_metaphone('of Falaise'), ('AFFLS', ''))
        self.assertEqual(double_metaphone('of Flanders'), ('AFFLNTRS', ''))
        self.assertEqual(double_metaphone('of Galloway'), ('AFKL', ''))
        self.assertEqual(double_metaphone('of Germany'), ('AFKRMN', 'AFJRMN'))
        self.assertEqual(double_metaphone('of Gloucester'), ('AFKLSSTR', ''))
        self.assertEqual(double_metaphone('of Heristal'), ('AFRSTL', ''))
        self.assertEqual(double_metaphone('of Hungary'), ('AFNKR', ''))
        self.assertEqual(double_metaphone('of Huntington'), ('AFNTNKTN', ''))
        self.assertEqual(double_metaphone('of Kiev'), ('AFKF', ''))
        self.assertEqual(double_metaphone('of Kuno'), ('AFKN', ''))
        self.assertEqual(double_metaphone('of Landen'), ('AFLNTN', ''))
        self.assertEqual(double_metaphone('of Laon'), ('AFLN', ''))
        self.assertEqual(double_metaphone('of Leinster'), ('AFLNSTR', ''))
        self.assertEqual(double_metaphone('of Lens'), ('AFLNS', ''))
        self.assertEqual(double_metaphone('of Lorraine'), ('AFLRN', ''))
        self.assertEqual(double_metaphone('of Louvain'), ('AFLFN', ''))
        self.assertEqual(double_metaphone('of Mercia'), ('AFMRS', 'AFMRX'))
        self.assertEqual(double_metaphone('of Metz'), ('AFMTS', ''))
        self.assertEqual(double_metaphone('of Meulan'), ('AFMLN', ''))
        self.assertEqual(double_metaphone('of Nass'), ('AFNS', ''))
        self.assertEqual(double_metaphone('of Normandy'), ('AFNRMNT', ''))
        self.assertEqual(double_metaphone('of Ohningen'), ('AFNNJN', 'AFNNKN'))
        self.assertEqual(double_metaphone('of Orleans'), ('AFRLNS', ''))
        self.assertEqual(double_metaphone('of Poitou'), ('AFPT', ''))
        self.assertEqual(double_metaphone('of Polotzk'), ('AFPLTSK', ''))
        self.assertEqual(double_metaphone('of Provence'), ('AFPRFNS', ''))
        self.assertEqual(double_metaphone('of Ringelheim'),
                         ('AFRNJLM', 'AFRNKLM'))
        self.assertEqual(double_metaphone('of Salisbury'), ('AFSLSPR', ''))
        self.assertEqual(double_metaphone('of Saxony'), ('AFSKSN', ''))
        self.assertEqual(double_metaphone('of Scotland'), ('AFSKTLNT', ''))
        self.assertEqual(double_metaphone('of Senlis'), ('AFSNLS', ''))
        self.assertEqual(double_metaphone('of Stafford'), ('AFSTFRT', ''))
        self.assertEqual(double_metaphone('of Swabia'), ('AFSP', ''))
        self.assertEqual(double_metaphone('of Tongres'), ('AFTNKRS', ''))
        self.assertEqual(double_metaphone('of the Tributes'),
                         ('AF0TRPTS', 'AFTTRPTS'))
        self.assertEqual(double_metaphone('unknown'), ('ANKNN', ''))
        self.assertEqual(double_metaphone('van der Gouda'), ('FNTRKT', ''))
        self.assertEqual(double_metaphone('von Adenbaugh'), ('FNTNP', ''))
        self.assertEqual(double_metaphone('ARCHITure'), ('ARKTR', ''))
        self.assertEqual(double_metaphone('Arnoff'), ('ARNF', ''))
        self.assertEqual(double_metaphone('Arnow'), ('ARN', 'ARNF'))
        self.assertEqual(double_metaphone('DANGER'), ('TNJR', 'TNKR'))
        self.assertEqual(double_metaphone('Jankelowicz'), ('JNKLTS', 'ANKLFX'))
        self.assertEqual(double_metaphone('MANGER'), ('MNJR', 'MNKR'))
        self.assertEqual(double_metaphone('McClellan'), ('MKLLN', ''))
        self.assertEqual(double_metaphone('McHugh'), ('MK', ''))
        self.assertEqual(double_metaphone('McLaughlin'), ('MKLFLN', ''))
        self.assertEqual(double_metaphone('ORCHEStra'), ('ARKSTR', ''))
        self.assertEqual(double_metaphone('ORCHID'), ('ARKT', ''))
        self.assertEqual(double_metaphone('Pierce'), ('PRS', ''))
        self.assertEqual(double_metaphone('RANGER'), ('RNJR', 'RNKR'))
        self.assertEqual(double_metaphone('Schlesinger'), ('XLSNKR', 'SLSNJR'))
        self.assertEqual(double_metaphone('Uomo'), ('AM', ''))
        self.assertEqual(double_metaphone('Vasserman'), ('FSRMN', ''))
        self.assertEqual(double_metaphone('Wasserman'), ('ASRMN', 'FSRMN'))
        self.assertEqual(double_metaphone('Womo'), ('AM', 'FM'))
        self.assertEqual(double_metaphone('Yankelovich'), ('ANKLFX', 'ANKLFK'))
        self.assertEqual(double_metaphone('accede'), ('AKST', ''))
        self.assertEqual(double_metaphone('accident'), ('AKSTNT', ''))
        self.assertEqual(double_metaphone('adelsheim'), ('ATLSM', ''))
        self.assertEqual(double_metaphone('aged'), ('AJT', 'AKT'))
        self.assertEqual(double_metaphone('ageless'), ('AJLS', 'AKLS'))
        self.assertEqual(double_metaphone('agency'), ('AJNS', 'AKNS'))
        self.assertEqual(double_metaphone('aghast'), ('AKST', ''))
        self.assertEqual(double_metaphone('agio'), ('AJ', 'AK'))
        self.assertEqual(double_metaphone('agrimony'), ('AKRMN', ''))
        self.assertEqual(double_metaphone('album'), ('ALPM', ''))
        self.assertEqual(double_metaphone('alcmene'), ('ALKMN', ''))
        self.assertEqual(double_metaphone('alehouse'), ('ALHS', ''))
        self.assertEqual(double_metaphone('antique'), ('ANTK', ''))
        self.assertEqual(double_metaphone('artois'), ('ART', 'ARTS'))
        self.assertEqual(double_metaphone('automation'), ('ATMXN', ''))
        self.assertEqual(double_metaphone('bacchus'), ('PKS', ''))
        self.assertEqual(double_metaphone('bacci'), ('PX', ''))
        self.assertEqual(double_metaphone('bajador'), ('PJTR', 'PHTR'))
        self.assertEqual(double_metaphone('bellocchio'), ('PLX', ''))
        self.assertEqual(double_metaphone('bertucci'), ('PRTX', ''))
        self.assertEqual(double_metaphone('biaggi'), ('PJ', 'PK'))
        self.assertEqual(double_metaphone('bough'), ('P', ''))
        self.assertEqual(double_metaphone('breaux'), ('PR', ''))
        self.assertEqual(double_metaphone('broughton'), ('PRTN', ''))
        self.assertEqual(double_metaphone('cabrillo'), ('KPRL', 'KPR'))
        self.assertEqual(double_metaphone('caesar'), ('SSR', ''))
        self.assertEqual(double_metaphone('cagney'), ('KKN', ''))
        self.assertEqual(double_metaphone('campbell'), ('KMPL', ''))
        self.assertEqual(double_metaphone('carlisle'), ('KRLL', ''))
        self.assertEqual(double_metaphone('carlysle'), ('KRLL', ''))
        self.assertEqual(double_metaphone('chemistry'), ('KMSTR', ''))
        self.assertEqual(double_metaphone('chianti'), ('KNT', ''))
        self.assertEqual(double_metaphone('chorus'), ('KRS', ''))
        self.assertEqual(double_metaphone('cough'), ('KF', ''))
        self.assertEqual(double_metaphone('czerny'), ('SRN', 'XRN'))
        self.assertEqual(double_metaphone('deffenbacher'), ('TFNPKR', ''))
        self.assertEqual(double_metaphone('dumb'), ('TM', ''))
        self.assertEqual(double_metaphone('edgar'), ('ATKR', ''))
        self.assertEqual(double_metaphone('edge'), ('AJ', ''))
        self.assertEqual(double_metaphone('filipowicz'), ('FLPTS', 'FLPFX'))
        self.assertEqual(double_metaphone('focaccia'), ('FKX', ''))
        self.assertEqual(double_metaphone('gallegos'), ('KLKS', 'KKS'))
        self.assertEqual(double_metaphone('gambrelli'), ('KMPRL', ''))
        self.assertEqual(double_metaphone('geithain'), ('K0N', 'JTN'))
        self.assertEqual(double_metaphone('ghiradelli'), ('JRTL', ''))
        self.assertEqual(double_metaphone('ghislane'), ('JLN', ''))
        self.assertEqual(double_metaphone('gough'), ('KF', ''))
        self.assertEqual(double_metaphone('hartheim'), ('HR0M', 'HRTM'))
        self.assertEqual(double_metaphone('heimsheim'), ('HMSM', ''))
        self.assertEqual(double_metaphone('hochmeier'), ('HKMR', ''))
        self.assertEqual(double_metaphone('hugh'), ('H', ''))
        self.assertEqual(double_metaphone('hunger'), ('HNKR', 'HNJR'))
        self.assertEqual(double_metaphone('hungry'), ('HNKR', ''))
        self.assertEqual(double_metaphone('island'), ('ALNT', ''))
        self.assertEqual(double_metaphone('isle'), ('AL', ''))
        self.assertEqual(double_metaphone('jose'), ('HS', ''))
        self.assertEqual(double_metaphone('laugh'), ('LF', ''))
        self.assertEqual(double_metaphone('mac caffrey'), ('MKFR', ''))
        self.assertEqual(double_metaphone('mac gregor'), ('MKRKR', ''))
        self.assertEqual(double_metaphone('pegnitz'), ('PNTS', 'PKNTS'))
        self.assertEqual(double_metaphone('piskowitz'), ('PSKTS', 'PSKFX'))
        self.assertEqual(double_metaphone('queen'), ('KN', ''))
        self.assertEqual(double_metaphone('raspberry'), ('RSPR', ''))
        self.assertEqual(double_metaphone('resnais'), ('RSN', 'RSNS'))
        self.assertEqual(double_metaphone('rogier'), ('RJ', 'RJR'))
        self.assertEqual(double_metaphone('rough'), ('RF', ''))
        self.assertEqual(double_metaphone('san jacinto'), ('SNHSNT', ''))
        self.assertEqual(double_metaphone('schenker'), ('XNKR', 'SKNKR'))
        self.assertEqual(double_metaphone('schermerhorn'),
                         ('XRMRRN', 'SKRMRRN'))
        self.assertEqual(double_metaphone('schmidt'), ('XMT', 'SMT'))
        self.assertEqual(double_metaphone('schneider'), ('XNTR', 'SNTR'))
        self.assertEqual(double_metaphone('school'), ('SKL', ''))
        self.assertEqual(double_metaphone('schooner'), ('SKNR', ''))
        self.assertEqual(double_metaphone('schrozberg'), ('XRSPRK', 'SRSPRK'))
        self.assertEqual(double_metaphone('schulman'), ('XLMN', ''))
        self.assertEqual(double_metaphone('schwabach'), ('XPK', 'XFPK'))
        self.assertEqual(double_metaphone('schwarzach'), ('XRSK', 'XFRTSK'))
        self.assertEqual(double_metaphone('smith'), ('SM0', 'XMT'))
        self.assertEqual(double_metaphone('snider'), ('SNTR', 'XNTR'))
        self.assertEqual(double_metaphone('succeed'), ('SKST', ''))
        self.assertEqual(double_metaphone('sugarcane'), ('XKRKN', 'SKRKN'))
        self.assertEqual(double_metaphone('svobodka'), ('SFPTK', ''))
        self.assertEqual(double_metaphone('tagliaro'), ('TKLR', 'TLR'))
        self.assertEqual(double_metaphone('thames'), ('TMS', ''))
        self.assertEqual(double_metaphone('theilheim'), ('0LM', 'TLM'))
        self.assertEqual(double_metaphone('thomas'), ('TMS', ''))
        self.assertEqual(double_metaphone('thumb'), ('0M', 'TM'))
        self.assertEqual(double_metaphone('tichner'), ('TXNR', 'TKNR'))
        self.assertEqual(double_metaphone('tough'), ('TF', ''))
        self.assertEqual(double_metaphone('umbrella'), ('AMPRL', ''))
        self.assertEqual(double_metaphone('vilshofen'), ('FLXFN', ''))
        self.assertEqual(double_metaphone('von schuller'), ('FNXLR', ''))
        self.assertEqual(double_metaphone('wachtler'), ('AKTLR', 'FKTLR'))
        self.assertEqual(double_metaphone('wechsler'), ('AKSLR', 'FKSLR'))
        self.assertEqual(double_metaphone('weikersheim'), ('AKRSM', 'FKRSM'))
        self.assertEqual(double_metaphone('zhao'), ('J', ''))

    def test_double_metaphone_surnames4(self):
        """Test abydos.phonetic.double_metaphone (surname data, 4-letter)."""
        self.assertEqual(double_metaphone('', 4), ('', ''))
        self.assertEqual(double_metaphone('ALLERTON', 4), ('ALRT', ''))
        self.assertEqual(double_metaphone('Acton', 4), ('AKTN', ''))
        self.assertEqual(double_metaphone('Adams', 4), ('ATMS', ''))
        self.assertEqual(double_metaphone('Aggar', 4), ('AKR', ''))
        self.assertEqual(double_metaphone('Ahl', 4), ('AL', ''))
        self.assertEqual(double_metaphone('Aiken', 4), ('AKN', ''))
        self.assertEqual(double_metaphone('Alan', 4), ('ALN', ''))
        self.assertEqual(double_metaphone('Alcock', 4), ('ALKK', ''))
        self.assertEqual(double_metaphone('Alden', 4), ('ALTN', ''))
        self.assertEqual(double_metaphone('Aldham', 4), ('ALTM', ''))
        self.assertEqual(double_metaphone('Allen', 4), ('ALN', ''))
        self.assertEqual(double_metaphone('Allerton', 4), ('ALRT', ''))
        self.assertEqual(double_metaphone('Alsop', 4), ('ALSP', ''))
        self.assertEqual(double_metaphone('Alwein', 4), ('ALN', ''))
        self.assertEqual(double_metaphone('Ambler', 4), ('AMPL', ''))
        self.assertEqual(double_metaphone('Andevill', 4), ('ANTF', ''))
        self.assertEqual(double_metaphone('Andrews', 4), ('ANTR', ''))
        self.assertEqual(double_metaphone('Andreyco', 4), ('ANTR', ''))
        self.assertEqual(double_metaphone('Andriesse', 4), ('ANTR', ''))
        self.assertEqual(double_metaphone('Angier', 4), ('ANJ', 'ANJR'))
        self.assertEqual(double_metaphone('Annabel', 4), ('ANPL', ''))
        self.assertEqual(double_metaphone('Anne', 4), ('AN', ''))
        self.assertEqual(double_metaphone('Anstye', 4), ('ANST', ''))
        self.assertEqual(double_metaphone('Appling', 4), ('APLN', ''))
        self.assertEqual(double_metaphone('Apuke', 4), ('APK', ''))
        self.assertEqual(double_metaphone('Arnold', 4), ('ARNL', ''))
        self.assertEqual(double_metaphone('Ashby', 4), ('AXP', ''))
        self.assertEqual(double_metaphone('Astwood', 4), ('ASTT', ''))
        self.assertEqual(double_metaphone('Atkinson', 4), ('ATKN', ''))
        self.assertEqual(double_metaphone('Audley', 4), ('ATL', ''))
        self.assertEqual(double_metaphone('Austin', 4), ('ASTN', ''))
        self.assertEqual(double_metaphone('Avenal', 4), ('AFNL', ''))
        self.assertEqual(double_metaphone('Ayer', 4), ('AR', ''))
        self.assertEqual(double_metaphone('Ayot', 4), ('AT', ''))
        self.assertEqual(double_metaphone('Babbitt', 4), ('PPT', ''))
        self.assertEqual(double_metaphone('Bachelor', 4), ('PXLR', 'PKLR'))
        self.assertEqual(double_metaphone('Bachelour', 4), ('PXLR', 'PKLR'))
        self.assertEqual(double_metaphone('Bailey', 4), ('PL', ''))
        self.assertEqual(double_metaphone('Baivel', 4), ('PFL', ''))
        self.assertEqual(double_metaphone('Baker', 4), ('PKR', ''))
        self.assertEqual(double_metaphone('Baldwin', 4), ('PLTN', ''))
        self.assertEqual(double_metaphone('Balsley', 4), ('PLSL', ''))
        self.assertEqual(double_metaphone('Barber', 4), ('PRPR', ''))
        self.assertEqual(double_metaphone('Barker', 4), ('PRKR', ''))
        self.assertEqual(double_metaphone('Barlow', 4), ('PRL', 'PRLF'))
        self.assertEqual(double_metaphone('Barnard', 4), ('PRNR', ''))
        self.assertEqual(double_metaphone('Barnes', 4), ('PRNS', ''))
        self.assertEqual(double_metaphone('Barnsley', 4), ('PRNS', ''))
        self.assertEqual(double_metaphone('Barouxis', 4), ('PRKS', ''))
        self.assertEqual(double_metaphone('Bartlet', 4), ('PRTL', ''))
        self.assertEqual(double_metaphone('Basley', 4), ('PSL', ''))
        self.assertEqual(double_metaphone('Basset', 4), ('PST', ''))
        self.assertEqual(double_metaphone('Bassett', 4), ('PST', ''))
        self.assertEqual(double_metaphone('Batchlor', 4), ('PXLR', ''))
        self.assertEqual(double_metaphone('Bates', 4), ('PTS', ''))
        self.assertEqual(double_metaphone('Batson', 4), ('PTSN', ''))
        self.assertEqual(double_metaphone('Bayes', 4), ('PS', ''))
        self.assertEqual(double_metaphone('Bayley', 4), ('PL', ''))
        self.assertEqual(double_metaphone('Beale', 4), ('PL', ''))
        self.assertEqual(double_metaphone('Beauchamp', 4), ('PXMP', 'PKMP'))
        self.assertEqual(double_metaphone('Beauclerc', 4), ('PKLR', ''))
        self.assertEqual(double_metaphone('Beech', 4), ('PK', ''))
        self.assertEqual(double_metaphone('Beers', 4), ('PRS', ''))
        self.assertEqual(double_metaphone('Beke', 4), ('PK', ''))
        self.assertEqual(double_metaphone('Belcher', 4), ('PLXR', 'PLKR'))
        self.assertEqual(double_metaphone('Benjamin', 4), ('PNJM', ''))
        self.assertEqual(double_metaphone('Benningham', 4), ('PNNK', ''))
        self.assertEqual(double_metaphone('Bereford', 4), ('PRFR', ''))
        self.assertEqual(double_metaphone('Bergen', 4), ('PRJN', 'PRKN'))
        self.assertEqual(double_metaphone('Berkeley', 4), ('PRKL', ''))
        self.assertEqual(double_metaphone('Berry', 4), ('PR', ''))
        self.assertEqual(double_metaphone('Besse', 4), ('PS', ''))
        self.assertEqual(double_metaphone('Bessey', 4), ('PS', ''))
        self.assertEqual(double_metaphone('Bessiles', 4), ('PSLS', ''))
        self.assertEqual(double_metaphone('Bigelow', 4), ('PJL', 'PKLF'))
        self.assertEqual(double_metaphone('Bigg', 4), ('PK', ''))
        self.assertEqual(double_metaphone('Bigod', 4), ('PKT', ''))
        self.assertEqual(double_metaphone('Billings', 4), ('PLNK', ''))
        self.assertEqual(double_metaphone('Bimper', 4), ('PMPR', ''))
        self.assertEqual(double_metaphone('Binker', 4), ('PNKR', ''))
        self.assertEqual(double_metaphone('Birdsill', 4), ('PRTS', ''))
        self.assertEqual(double_metaphone('Bishop', 4), ('PXP', ''))
        self.assertEqual(double_metaphone('Black', 4), ('PLK', ''))
        self.assertEqual(double_metaphone('Blagge', 4), ('PLK', ''))
        self.assertEqual(double_metaphone('Blake', 4), ('PLK', ''))
        self.assertEqual(double_metaphone('Blanck', 4), ('PLNK', ''))
        self.assertEqual(double_metaphone('Bledsoe', 4), ('PLTS', ''))
        self.assertEqual(double_metaphone('Blennerhasset', 4), ('PLNR', ''))
        self.assertEqual(double_metaphone('Blessing', 4), ('PLSN', ''))
        self.assertEqual(double_metaphone('Blewett', 4), ('PLT', ''))
        self.assertEqual(double_metaphone('Bloctgoed', 4), ('PLKT', ''))
        self.assertEqual(double_metaphone('Bloetgoet', 4), ('PLTK', ''))
        self.assertEqual(double_metaphone('Bloodgood', 4), ('PLTK', ''))
        self.assertEqual(double_metaphone('Blossom', 4), ('PLSM', ''))
        self.assertEqual(double_metaphone('Blount', 4), ('PLNT', ''))
        self.assertEqual(double_metaphone('Bodine', 4), ('PTN', ''))
        self.assertEqual(double_metaphone('Bodman', 4), ('PTMN', ''))
        self.assertEqual(double_metaphone('BonCoeur', 4), ('PNKR', ''))
        self.assertEqual(double_metaphone('Bond', 4), ('PNT', ''))
        self.assertEqual(double_metaphone('Boscawen', 4), ('PSKN', ''))
        self.assertEqual(double_metaphone('Bosworth', 4), ('PSR0', 'PSRT'))
        self.assertEqual(double_metaphone('Bouchier', 4), ('PX', 'PKR'))
        self.assertEqual(double_metaphone('Bowne', 4), ('PN', ''))
        self.assertEqual(double_metaphone('Bradbury', 4), ('PRTP', ''))
        self.assertEqual(double_metaphone('Bradder', 4), ('PRTR', ''))
        self.assertEqual(double_metaphone('Bradford', 4), ('PRTF', ''))
        self.assertEqual(double_metaphone('Bradstreet', 4), ('PRTS', ''))
        self.assertEqual(double_metaphone('Braham', 4), ('PRHM', ''))
        self.assertEqual(double_metaphone('Brailsford', 4), ('PRLS', ''))
        self.assertEqual(double_metaphone('Brainard', 4), ('PRNR', ''))
        self.assertEqual(double_metaphone('Brandish', 4), ('PRNT', ''))
        self.assertEqual(double_metaphone('Braun', 4), ('PRN', ''))
        self.assertEqual(double_metaphone('Brecc', 4), ('PRK', ''))
        self.assertEqual(double_metaphone('Brent', 4), ('PRNT', ''))
        self.assertEqual(double_metaphone('Brenton', 4), ('PRNT', ''))
        self.assertEqual(double_metaphone('Briggs', 4), ('PRKS', ''))
        self.assertEqual(double_metaphone('Brigham', 4), ('PRM', ''))
        self.assertEqual(double_metaphone('Brobst', 4), ('PRPS', ''))
        self.assertEqual(double_metaphone('Brome', 4), ('PRM', ''))
        self.assertEqual(double_metaphone('Bronson', 4), ('PRNS', ''))
        self.assertEqual(double_metaphone('Brooks', 4), ('PRKS', ''))
        self.assertEqual(double_metaphone('Brouillard', 4), ('PRLR', ''))
        self.assertEqual(double_metaphone('Brown', 4), ('PRN', ''))
        self.assertEqual(double_metaphone('Browne', 4), ('PRN', ''))
        self.assertEqual(double_metaphone('Brownell', 4), ('PRNL', ''))
        self.assertEqual(double_metaphone('Bruley', 4), ('PRL', ''))
        self.assertEqual(double_metaphone('Bryant', 4), ('PRNT', ''))
        self.assertEqual(double_metaphone('Brzozowski', 4), ('PRSS', 'PRTS'))
        self.assertEqual(double_metaphone('Buide', 4), ('PT', ''))
        self.assertEqual(double_metaphone('Bulmer', 4), ('PLMR', ''))
        self.assertEqual(double_metaphone('Bunker', 4), ('PNKR', ''))
        self.assertEqual(double_metaphone('Burden', 4), ('PRTN', ''))
        self.assertEqual(double_metaphone('Burge', 4), ('PRJ', 'PRK'))
        self.assertEqual(double_metaphone('Burgoyne', 4), ('PRKN', ''))
        self.assertEqual(double_metaphone('Burke', 4), ('PRK', ''))
        self.assertEqual(double_metaphone('Burnett', 4), ('PRNT', ''))
        self.assertEqual(double_metaphone('Burpee', 4), ('PRP', ''))
        self.assertEqual(double_metaphone('Bursley', 4), ('PRSL', ''))
        self.assertEqual(double_metaphone('Burton', 4), ('PRTN', ''))
        self.assertEqual(double_metaphone('Bushnell', 4), ('PXNL', ''))
        self.assertEqual(double_metaphone('Buss', 4), ('PS', ''))
        self.assertEqual(double_metaphone('Buswell', 4), ('PSL', ''))
        self.assertEqual(double_metaphone('Butler', 4), ('PTLR', ''))
        self.assertEqual(double_metaphone('Calkin', 4), ('KLKN', ''))
        self.assertEqual(double_metaphone('Canada', 4), ('KNT', ''))
        self.assertEqual(double_metaphone('Canmore', 4), ('KNMR', ''))
        self.assertEqual(double_metaphone('Canney', 4), ('KN', ''))
        self.assertEqual(double_metaphone('Capet', 4), ('KPT', ''))
        self.assertEqual(double_metaphone('Card', 4), ('KRT', ''))
        self.assertEqual(double_metaphone('Carman', 4), ('KRMN', ''))
        self.assertEqual(double_metaphone('Carpenter', 4), ('KRPN', ''))
        self.assertEqual(double_metaphone('Cartwright', 4), ('KRTR', ''))
        self.assertEqual(double_metaphone('Casey', 4), ('KS', ''))
        self.assertEqual(double_metaphone('Catterfield', 4), ('KTRF', ''))
        self.assertEqual(double_metaphone('Ceeley', 4), ('SL', ''))
        self.assertEqual(double_metaphone('Chambers', 4), ('XMPR', ''))
        self.assertEqual(double_metaphone('Champion', 4), ('XMPN', ''))
        self.assertEqual(double_metaphone('Chapman', 4), ('XPMN', ''))
        self.assertEqual(double_metaphone('Chase', 4), ('XS', ''))
        self.assertEqual(double_metaphone('Cheney', 4), ('XN', ''))
        self.assertEqual(double_metaphone('Chetwynd', 4), ('XTNT', ''))
        self.assertEqual(double_metaphone('Chevalier', 4), ('XFL', 'XFLR'))
        self.assertEqual(double_metaphone('Chillingsworth', 4), ('XLNK', ''))
        self.assertEqual(double_metaphone('Christie', 4), ('KRST', ''))
        self.assertEqual(double_metaphone('Chubbuck', 4), ('XPK', ''))
        self.assertEqual(double_metaphone('Church', 4), ('XRX', 'XRK'))
        self.assertEqual(double_metaphone('Clark', 4), ('KLRK', ''))
        self.assertEqual(double_metaphone('Clarke', 4), ('KLRK', ''))
        self.assertEqual(double_metaphone('Cleare', 4), ('KLR', ''))
        self.assertEqual(double_metaphone('Clement', 4), ('KLMN', ''))
        self.assertEqual(double_metaphone('Clerke', 4), ('KLRK', ''))
        self.assertEqual(double_metaphone('Clibben', 4), ('KLPN', ''))
        self.assertEqual(double_metaphone('Clifford', 4), ('KLFR', ''))
        self.assertEqual(double_metaphone('Clivedon', 4), ('KLFT', ''))
        self.assertEqual(double_metaphone('Close', 4), ('KLS', ''))
        self.assertEqual(double_metaphone('Clothilde', 4), ('KL0L', 'KLTL'))
        self.assertEqual(double_metaphone('Cobb', 4), ('KP', ''))
        self.assertEqual(double_metaphone('Coburn', 4), ('KPRN', ''))
        self.assertEqual(double_metaphone('Coburne', 4), ('KPRN', ''))
        self.assertEqual(double_metaphone('Cocke', 4), ('KK', ''))
        self.assertEqual(double_metaphone('Coffin', 4), ('KFN', ''))
        self.assertEqual(double_metaphone('Coffyn', 4), ('KFN', ''))
        self.assertEqual(double_metaphone('Colborne', 4), ('KLPR', ''))
        self.assertEqual(double_metaphone('Colby', 4), ('KLP', ''))
        self.assertEqual(double_metaphone('Cole', 4), ('KL', ''))
        self.assertEqual(double_metaphone('Coleman', 4), ('KLMN', ''))
        self.assertEqual(double_metaphone('Collier', 4), ('KL', 'KLR'))
        self.assertEqual(double_metaphone('Compton', 4), ('KMPT', ''))
        self.assertEqual(double_metaphone('Cone', 4), ('KN', ''))
        self.assertEqual(double_metaphone('Cook', 4), ('KK', ''))
        self.assertEqual(double_metaphone('Cooke', 4), ('KK', ''))
        self.assertEqual(double_metaphone('Cooper', 4), ('KPR', ''))
        self.assertEqual(double_metaphone('Copperthwaite', 4),
                         ('KPR0', 'KPRT'))
        self.assertEqual(double_metaphone('Corbet', 4), ('KRPT', ''))
        self.assertEqual(double_metaphone('Corell', 4), ('KRL', ''))
        self.assertEqual(double_metaphone('Corey', 4), ('KR', ''))
        self.assertEqual(double_metaphone('Corlies', 4), ('KRLS', ''))
        self.assertEqual(double_metaphone('Corneliszen', 4), ('KRNL', ''))
        self.assertEqual(double_metaphone('Cornelius', 4), ('KRNL', ''))
        self.assertEqual(double_metaphone('Cornwallis', 4), ('KRNL', ''))
        self.assertEqual(double_metaphone('Cosgrove', 4), ('KSKR', ''))
        self.assertEqual(double_metaphone('Count of Brionne', 4), ('KNTF', ''))
        self.assertEqual(double_metaphone('Covill', 4), ('KFL', ''))
        self.assertEqual(double_metaphone('Cowperthwaite', 4),
                         ('KPR0', 'KPRT'))
        self.assertEqual(double_metaphone('Cowperwaite', 4), ('KPRT', ''))
        self.assertEqual(double_metaphone('Crane', 4), ('KRN', ''))
        self.assertEqual(double_metaphone('Creagmile', 4), ('KRKM', ''))
        self.assertEqual(double_metaphone('Crew', 4), ('KR', 'KRF'))
        self.assertEqual(double_metaphone('Crispin', 4), ('KRSP', ''))
        self.assertEqual(double_metaphone('Crocker', 4), ('KRKR', ''))
        self.assertEqual(double_metaphone('Crockett', 4), ('KRKT', ''))
        self.assertEqual(double_metaphone('Crosby', 4), ('KRSP', ''))
        self.assertEqual(double_metaphone('Crump', 4), ('KRMP', ''))
        self.assertEqual(double_metaphone('Cunningham', 4), ('KNNK', ''))
        self.assertEqual(double_metaphone('Curtis', 4), ('KRTS', ''))
        self.assertEqual(double_metaphone('Cutha', 4), ('K0', 'KT'))
        self.assertEqual(double_metaphone('Cutter', 4), ('KTR', ''))
        self.assertEqual(double_metaphone('D\'Aubigny', 4), ('TPN', 'TPKN'))
        self.assertEqual(double_metaphone('DAVIS', 4), ('TFS', ''))
        self.assertEqual(double_metaphone('Dabinott', 4), ('TPNT', ''))
        self.assertEqual(double_metaphone('Dacre', 4), ('TKR', ''))
        self.assertEqual(double_metaphone('Daggett', 4), ('TKT', ''))
        self.assertEqual(double_metaphone('Danvers', 4), ('TNFR', ''))
        self.assertEqual(double_metaphone('Darcy', 4), ('TRS', ''))
        self.assertEqual(double_metaphone('Davis', 4), ('TFS', ''))
        self.assertEqual(double_metaphone('Dawn', 4), ('TN', ''))
        self.assertEqual(double_metaphone('Dawson', 4), ('TSN', ''))
        self.assertEqual(double_metaphone('Day', 4), ('T', ''))
        self.assertEqual(double_metaphone('Daye', 4), ('T', ''))
        self.assertEqual(double_metaphone('DeGrenier', 4), ('TKRN', ''))
        self.assertEqual(double_metaphone('Dean', 4), ('TN', ''))
        self.assertEqual(double_metaphone('Deekindaugh', 4), ('TKNT', ''))
        self.assertEqual(double_metaphone('Dennis', 4), ('TNS', ''))
        self.assertEqual(double_metaphone('Denny', 4), ('TN', ''))
        self.assertEqual(double_metaphone('Denton', 4), ('TNTN', ''))
        self.assertEqual(double_metaphone('Desborough', 4), ('TSPR', ''))
        self.assertEqual(double_metaphone('Despenser', 4), ('TSPN', ''))
        self.assertEqual(double_metaphone('Deverill', 4), ('TFRL', ''))
        self.assertEqual(double_metaphone('Devine', 4), ('TFN', ''))
        self.assertEqual(double_metaphone('Dexter', 4), ('TKST', ''))
        self.assertEqual(double_metaphone('Dillaway', 4), ('TL', ''))
        self.assertEqual(double_metaphone('Dimmick', 4), ('TMK', ''))
        self.assertEqual(double_metaphone('Dinan', 4), ('TNN', ''))
        self.assertEqual(double_metaphone('Dix', 4), ('TKS', ''))
        self.assertEqual(double_metaphone('Doggett', 4), ('TKT', ''))
        self.assertEqual(double_metaphone('Donahue', 4), ('TNH', ''))
        self.assertEqual(double_metaphone('Dorfman', 4), ('TRFM', ''))
        self.assertEqual(double_metaphone('Dorris', 4), ('TRS', ''))
        self.assertEqual(double_metaphone('Dow', 4), ('T', 'TF'))
        self.assertEqual(double_metaphone('Downey', 4), ('TN', ''))
        self.assertEqual(double_metaphone('Downing', 4), ('TNNK', ''))
        self.assertEqual(double_metaphone('Dowsett', 4), ('TST', ''))
        self.assertEqual(double_metaphone('Duck?', 4), ('TK', ''))
        self.assertEqual(double_metaphone('Dudley', 4), ('TTL', ''))
        self.assertEqual(double_metaphone('Duffy', 4), ('TF', ''))
        self.assertEqual(double_metaphone('Dunn', 4), ('TN', ''))
        self.assertEqual(double_metaphone('Dunsterville', 4), ('TNST', ''))
        self.assertEqual(double_metaphone('Durrant', 4), ('TRNT', ''))
        self.assertEqual(double_metaphone('Durrin', 4), ('TRN', ''))
        self.assertEqual(double_metaphone('Dustin', 4), ('TSTN', ''))
        self.assertEqual(double_metaphone('Duston', 4), ('TSTN', ''))
        self.assertEqual(double_metaphone('Eames', 4), ('AMS', ''))
        self.assertEqual(double_metaphone('Early', 4), ('ARL', ''))
        self.assertEqual(double_metaphone('Easty', 4), ('AST', ''))
        self.assertEqual(double_metaphone('Ebbett', 4), ('APT', ''))
        self.assertEqual(double_metaphone('Eberbach', 4), ('APRP', ''))
        self.assertEqual(double_metaphone('Eberhard', 4), ('APRR', ''))
        self.assertEqual(double_metaphone('Eddy', 4), ('AT', ''))
        self.assertEqual(double_metaphone('Edenden', 4), ('ATNT', ''))
        self.assertEqual(double_metaphone('Edwards', 4), ('ATRT', ''))
        self.assertEqual(double_metaphone('Eglinton', 4), ('AKLN', 'ALNT'))
        self.assertEqual(double_metaphone('Eliot', 4), ('ALT', ''))
        self.assertEqual(double_metaphone('Elizabeth', 4), ('ALSP', ''))
        self.assertEqual(double_metaphone('Ellis', 4), ('ALS', ''))
        self.assertEqual(double_metaphone('Ellison', 4), ('ALSN', ''))
        self.assertEqual(double_metaphone('Ellot', 4), ('ALT', ''))
        self.assertEqual(double_metaphone('Elny', 4), ('ALN', ''))
        self.assertEqual(double_metaphone('Elsner', 4), ('ALSN', ''))
        self.assertEqual(double_metaphone('Emerson', 4), ('AMRS', ''))
        self.assertEqual(double_metaphone('Empson', 4), ('AMPS', ''))
        self.assertEqual(double_metaphone('Est', 4), ('AST', ''))
        self.assertEqual(double_metaphone('Estabrook', 4), ('ASTP', ''))
        self.assertEqual(double_metaphone('Estes', 4), ('ASTS', ''))
        self.assertEqual(double_metaphone('Estey', 4), ('AST', ''))
        self.assertEqual(double_metaphone('Evans', 4), ('AFNS', ''))
        self.assertEqual(double_metaphone('Fallowell', 4), ('FLL', ''))
        self.assertEqual(double_metaphone('Farnsworth', 4), ('FRNS', ''))
        self.assertEqual(double_metaphone('Feake', 4), ('FK', ''))
        self.assertEqual(double_metaphone('Feke', 4), ('FK', ''))
        self.assertEqual(double_metaphone('Fellows', 4), ('FLS', ''))
        self.assertEqual(double_metaphone('Fettiplace', 4), ('FTPL', ''))
        self.assertEqual(double_metaphone('Finney', 4), ('FN', ''))
        self.assertEqual(double_metaphone('Fischer', 4), ('FXR', 'FSKR'))
        self.assertEqual(double_metaphone('Fisher', 4), ('FXR', ''))
        self.assertEqual(double_metaphone('Fisk', 4), ('FSK', ''))
        self.assertEqual(double_metaphone('Fiske', 4), ('FSK', ''))
        self.assertEqual(double_metaphone('Fletcher', 4), ('FLXR', ''))
        self.assertEqual(double_metaphone('Folger', 4), ('FLKR', 'FLJR'))
        self.assertEqual(double_metaphone('Foliot', 4), ('FLT', ''))
        self.assertEqual(double_metaphone('Folyot', 4), ('FLT', ''))
        self.assertEqual(double_metaphone('Fones', 4), ('FNS', ''))
        self.assertEqual(double_metaphone('Fordham', 4), ('FRTM', ''))
        self.assertEqual(double_metaphone('Forstner', 4), ('FRST', ''))
        self.assertEqual(double_metaphone('Fosten', 4), ('FSTN', ''))
        self.assertEqual(double_metaphone('Foster', 4), ('FSTR', ''))
        self.assertEqual(double_metaphone('Foulke', 4), ('FLK', ''))
        self.assertEqual(double_metaphone('Fowler', 4), ('FLR', ''))
        self.assertEqual(double_metaphone('Foxwell', 4), ('FKSL', ''))
        self.assertEqual(double_metaphone('Fraley', 4), ('FRL', ''))
        self.assertEqual(double_metaphone('Franceys', 4), ('FRNS', ''))
        self.assertEqual(double_metaphone('Franke', 4), ('FRNK', ''))
        self.assertEqual(double_metaphone('Frascella', 4), ('FRSL', ''))
        self.assertEqual(double_metaphone('Frazer', 4), ('FRSR', ''))
        self.assertEqual(double_metaphone('Fredd', 4), ('FRT', ''))
        self.assertEqual(double_metaphone('Freeman', 4), ('FRMN', ''))
        self.assertEqual(double_metaphone('French', 4), ('FRNX', 'FRNK'))
        self.assertEqual(double_metaphone('Freville', 4), ('FRFL', ''))
        self.assertEqual(double_metaphone('Frey', 4), ('FR', ''))
        self.assertEqual(double_metaphone('Frick', 4), ('FRK', ''))
        self.assertEqual(double_metaphone('Frier', 4), ('FR', 'FRR'))
        self.assertEqual(double_metaphone('Froe', 4), ('FR', ''))
        self.assertEqual(double_metaphone('Frorer', 4), ('FRRR', ''))
        self.assertEqual(double_metaphone('Frost', 4), ('FRST', ''))
        self.assertEqual(double_metaphone('Frothingham', 4), ('FR0N', 'FRTN'))
        self.assertEqual(double_metaphone('Fry', 4), ('FR', ''))
        self.assertEqual(double_metaphone('Gaffney', 4), ('KFN', ''))
        self.assertEqual(double_metaphone('Gage', 4), ('KJ', 'KK'))
        self.assertEqual(double_metaphone('Gallion', 4), ('KLN', ''))
        self.assertEqual(double_metaphone('Gallishan', 4), ('KLXN', ''))
        self.assertEqual(double_metaphone('Gamble', 4), ('KMPL', ''))
        self.assertEqual(double_metaphone('Garbrand', 4), ('KRPR', ''))
        self.assertEqual(double_metaphone('Gardner', 4), ('KRTN', ''))
        self.assertEqual(double_metaphone('Garrett', 4), ('KRT', ''))
        self.assertEqual(double_metaphone('Gassner', 4), ('KSNR', ''))
        self.assertEqual(double_metaphone('Gater', 4), ('KTR', ''))
        self.assertEqual(double_metaphone('Gaunt', 4), ('KNT', ''))
        self.assertEqual(double_metaphone('Gayer', 4), ('KR', ''))
        self.assertEqual(double_metaphone('Gerken', 4), ('KRKN', 'JRKN'))
        self.assertEqual(double_metaphone('Gerritsen', 4), ('KRTS', 'JRTS'))
        self.assertEqual(double_metaphone('Gibbs', 4), ('KPS', 'JPS'))
        self.assertEqual(double_metaphone('Giffard', 4), ('JFRT', 'KFRT'))
        self.assertEqual(double_metaphone('Gilbert', 4), ('KLPR', 'JLPR'))
        self.assertEqual(double_metaphone('Gill', 4), ('KL', 'JL'))
        self.assertEqual(double_metaphone('Gilman', 4), ('KLMN', 'JLMN'))
        self.assertEqual(double_metaphone('Glass', 4), ('KLS', ''))
        self.assertEqual(double_metaphone('GoddardGifford', 4), ('KTRJ', ''))
        self.assertEqual(double_metaphone('Godfrey', 4), ('KTFR', ''))
        self.assertEqual(double_metaphone('Godwin', 4), ('KTN', ''))
        self.assertEqual(double_metaphone('Goodale', 4), ('KTL', ''))
        self.assertEqual(double_metaphone('Goodnow', 4), ('KTN', 'KTNF'))
        self.assertEqual(double_metaphone('Gorham', 4), ('KRM', ''))
        self.assertEqual(double_metaphone('Goseline', 4), ('KSLN', ''))
        self.assertEqual(double_metaphone('Gott', 4), ('KT', ''))
        self.assertEqual(double_metaphone('Gould', 4), ('KLT', ''))
        self.assertEqual(double_metaphone('Grafton', 4), ('KRFT', ''))
        self.assertEqual(double_metaphone('Grant', 4), ('KRNT', ''))
        self.assertEqual(double_metaphone('Gray', 4), ('KR', ''))
        self.assertEqual(double_metaphone('Green', 4), ('KRN', ''))
        self.assertEqual(double_metaphone('Griffin', 4), ('KRFN', ''))
        self.assertEqual(double_metaphone('Grill', 4), ('KRL', ''))
        self.assertEqual(double_metaphone('Grim', 4), ('KRM', ''))
        self.assertEqual(double_metaphone('Grisgonelle', 4), ('KRSK', ''))
        self.assertEqual(double_metaphone('Gross', 4), ('KRS', ''))
        self.assertEqual(double_metaphone('Guba', 4), ('KP', ''))
        self.assertEqual(double_metaphone('Gybbes', 4), ('KPS', 'JPS'))
        self.assertEqual(double_metaphone('Haburne', 4), ('HPRN', ''))
        self.assertEqual(double_metaphone('Hackburne', 4), ('HKPR', ''))
        self.assertEqual(double_metaphone('Haddon?', 4), ('HTN', ''))
        self.assertEqual(double_metaphone('Haines', 4), ('HNS', ''))
        self.assertEqual(double_metaphone('Hale', 4), ('HL', ''))
        self.assertEqual(double_metaphone('Hall', 4), ('HL', ''))
        self.assertEqual(double_metaphone('Hallet', 4), ('HLT', ''))
        self.assertEqual(double_metaphone('Hallock', 4), ('HLK', ''))
        self.assertEqual(double_metaphone('Halstead', 4), ('HLST', ''))
        self.assertEqual(double_metaphone('Hammond', 4), ('HMNT', ''))
        self.assertEqual(double_metaphone('Hance', 4), ('HNS', ''))
        self.assertEqual(double_metaphone('Handy', 4), ('HNT', ''))
        self.assertEqual(double_metaphone('Hanson', 4), ('HNSN', ''))
        self.assertEqual(double_metaphone('Harasek', 4), ('HRSK', ''))
        self.assertEqual(double_metaphone('Harcourt', 4), ('HRKR', ''))
        self.assertEqual(double_metaphone('Hardy', 4), ('HRT', ''))
        self.assertEqual(double_metaphone('Harlock', 4), ('HRLK', ''))
        self.assertEqual(double_metaphone('Harris', 4), ('HRS', ''))
        self.assertEqual(double_metaphone('Hartley', 4), ('HRTL', ''))
        self.assertEqual(double_metaphone('Harvey', 4), ('HRF', ''))
        self.assertEqual(double_metaphone('Harvie', 4), ('HRF', ''))
        self.assertEqual(double_metaphone('Harwood', 4), ('HRT', ''))
        self.assertEqual(double_metaphone('Hathaway', 4), ('H0', 'HT'))
        self.assertEqual(double_metaphone('Haukeness', 4), ('HKNS', ''))
        self.assertEqual(double_metaphone('Hawkes', 4), ('HKS', ''))
        self.assertEqual(double_metaphone('Hawkhurst', 4), ('HKRS', ''))
        self.assertEqual(double_metaphone('Hawkins', 4), ('HKNS', ''))
        self.assertEqual(double_metaphone('Hawley', 4), ('HL', ''))
        self.assertEqual(double_metaphone('Heald', 4), ('HLT', ''))
        self.assertEqual(double_metaphone('Helsdon', 4), ('HLST', ''))
        self.assertEqual(double_metaphone('Hemenway', 4), ('HMN', ''))
        self.assertEqual(double_metaphone('Hemmenway', 4), ('HMN', ''))
        self.assertEqual(double_metaphone('Henck', 4), ('HNK', ''))
        self.assertEqual(double_metaphone('Henderson', 4), ('HNTR', ''))
        self.assertEqual(double_metaphone('Hendricks', 4), ('HNTR', ''))
        self.assertEqual(double_metaphone('Hersey', 4), ('HRS', ''))
        self.assertEqual(double_metaphone('Hewes', 4), ('HS', ''))
        self.assertEqual(double_metaphone('Heyman', 4), ('HMN', ''))
        self.assertEqual(double_metaphone('Hicks', 4), ('HKS', ''))
        self.assertEqual(double_metaphone('Hidden', 4), ('HTN', ''))
        self.assertEqual(double_metaphone('Higgs', 4), ('HKS', ''))
        self.assertEqual(double_metaphone('Hill', 4), ('HL', ''))
        self.assertEqual(double_metaphone('Hills', 4), ('HLS', ''))
        self.assertEqual(double_metaphone('Hinckley', 4), ('HNKL', ''))
        self.assertEqual(double_metaphone('Hipwell', 4), ('HPL', ''))
        self.assertEqual(double_metaphone('Hobart', 4), ('HPRT', ''))
        self.assertEqual(double_metaphone('Hoben', 4), ('HPN', ''))
        self.assertEqual(double_metaphone('Hoffmann', 4), ('HFMN', ''))
        self.assertEqual(double_metaphone('Hogan', 4), ('HKN', ''))
        self.assertEqual(double_metaphone('Holmes', 4), ('HLMS', ''))
        self.assertEqual(double_metaphone('Hoo', 4), ('H', ''))
        self.assertEqual(double_metaphone('Hooker', 4), ('HKR', ''))
        self.assertEqual(double_metaphone('Hopcott', 4), ('HPKT', ''))
        self.assertEqual(double_metaphone('Hopkins', 4), ('HPKN', ''))
        self.assertEqual(double_metaphone('Hopkinson', 4), ('HPKN', ''))
        self.assertEqual(double_metaphone('Hornsey', 4), ('HRNS', ''))
        self.assertEqual(double_metaphone('Houckgeest', 4), ('HKJS', 'HKKS'))
        self.assertEqual(double_metaphone('Hough', 4), ('H', ''))
        self.assertEqual(double_metaphone('Houstin', 4), ('HSTN', ''))
        self.assertEqual(double_metaphone('How', 4), ('H', 'HF'))
        self.assertEqual(double_metaphone('Howe', 4), ('H', ''))
        self.assertEqual(double_metaphone('Howland', 4), ('HLNT', ''))
        self.assertEqual(double_metaphone('Hubner', 4), ('HPNR', ''))
        self.assertEqual(double_metaphone('Hudnut', 4), ('HTNT', ''))
        self.assertEqual(double_metaphone('Hughes', 4), ('HS', ''))
        self.assertEqual(double_metaphone('Hull', 4), ('HL', ''))
        self.assertEqual(double_metaphone('Hulme', 4), ('HLM', ''))
        self.assertEqual(double_metaphone('Hume', 4), ('HM', ''))
        self.assertEqual(double_metaphone('Hundertumark', 4), ('HNTR', ''))
        self.assertEqual(double_metaphone('Hundley', 4), ('HNTL', ''))
        self.assertEqual(double_metaphone('Hungerford', 4), ('HNKR', 'HNJR'))
        self.assertEqual(double_metaphone('Hunt', 4), ('HNT', ''))
        self.assertEqual(double_metaphone('Hurst', 4), ('HRST', ''))
        self.assertEqual(double_metaphone('Husbands', 4), ('HSPN', ''))
        self.assertEqual(double_metaphone('Hussey', 4), ('HS', ''))
        self.assertEqual(double_metaphone('Husted', 4), ('HSTT', ''))
        self.assertEqual(double_metaphone('Hutchins', 4), ('HXNS', ''))
        self.assertEqual(double_metaphone('Hutchinson', 4), ('HXNS', ''))
        self.assertEqual(double_metaphone('Huttinger', 4), ('HTNK', 'HTNJ'))
        self.assertEqual(double_metaphone('Huybertsen', 4), ('HPRT', ''))
        self.assertEqual(double_metaphone('Iddenden', 4), ('ATNT', ''))
        self.assertEqual(double_metaphone('Ingraham', 4), ('ANKR', ''))
        self.assertEqual(double_metaphone('Ives', 4), ('AFS', ''))
        self.assertEqual(double_metaphone('Jackson', 4), ('JKSN', 'AKSN'))
        self.assertEqual(double_metaphone('Jacob', 4), ('JKP', 'AKP'))
        self.assertEqual(double_metaphone('Jans', 4), ('JNS', 'ANS'))
        self.assertEqual(double_metaphone('Jenkins', 4), ('JNKN', 'ANKN'))
        self.assertEqual(double_metaphone('Jewett', 4), ('JT', 'AT'))
        self.assertEqual(double_metaphone('Jewitt', 4), ('JT', 'AT'))
        self.assertEqual(double_metaphone('Johnson', 4), ('JNSN', 'ANSN'))
        self.assertEqual(double_metaphone('Jones', 4), ('JNS', 'ANS'))
        self.assertEqual(double_metaphone('Josephine', 4), ('JSFN', 'HSFN'))
        self.assertEqual(double_metaphone('Judd', 4), ('JT', 'AT'))
        self.assertEqual(double_metaphone('June', 4), ('JN', 'AN'))
        self.assertEqual(double_metaphone('Kamarowska', 4), ('KMRS', ''))
        self.assertEqual(double_metaphone('Kay', 4), ('K', ''))
        self.assertEqual(double_metaphone('Kelley', 4), ('KL', ''))
        self.assertEqual(double_metaphone('Kelly', 4), ('KL', ''))
        self.assertEqual(double_metaphone('Keymber', 4), ('KMPR', ''))
        self.assertEqual(double_metaphone('Keynes', 4), ('KNS', ''))
        self.assertEqual(double_metaphone('Kilham', 4), ('KLM', ''))
        self.assertEqual(double_metaphone('Kim', 4), ('KM', ''))
        self.assertEqual(double_metaphone('Kimball', 4), ('KMPL', ''))
        self.assertEqual(double_metaphone('King', 4), ('KNK', ''))
        self.assertEqual(double_metaphone('Kinsey', 4), ('KNS', ''))
        self.assertEqual(double_metaphone('Kirk', 4), ('KRK', ''))
        self.assertEqual(double_metaphone('Kirton', 4), ('KRTN', ''))
        self.assertEqual(double_metaphone('Kistler', 4), ('KSTL', ''))
        self.assertEqual(double_metaphone('Kitchen', 4), ('KXN', ''))
        self.assertEqual(double_metaphone('Kitson', 4), ('KTSN', ''))
        self.assertEqual(double_metaphone('Klett', 4), ('KLT', ''))
        self.assertEqual(double_metaphone('Kline', 4), ('KLN', ''))
        self.assertEqual(double_metaphone('Knapp', 4), ('NP', ''))
        self.assertEqual(double_metaphone('Knight', 4), ('NT', ''))
        self.assertEqual(double_metaphone('Knote', 4), ('NT', ''))
        self.assertEqual(double_metaphone('Knott', 4), ('NT', ''))
        self.assertEqual(double_metaphone('Knox', 4), ('NKS', ''))
        self.assertEqual(double_metaphone('Koeller', 4), ('KLR', ''))
        self.assertEqual(double_metaphone('La Pointe', 4), ('LPNT', ''))
        self.assertEqual(double_metaphone('LaPlante', 4), ('LPLN', ''))
        self.assertEqual(double_metaphone('Laimbeer', 4), ('LMPR', ''))
        self.assertEqual(double_metaphone('Lamb', 4), ('LMP', ''))
        self.assertEqual(double_metaphone('Lambertson', 4), ('LMPR', ''))
        self.assertEqual(double_metaphone('Lancto', 4), ('LNKT', ''))
        self.assertEqual(double_metaphone('Landry', 4), ('LNTR', ''))
        self.assertEqual(double_metaphone('Lane', 4), ('LN', ''))
        self.assertEqual(double_metaphone('Langendyck', 4), ('LNJN', 'LNKN'))
        self.assertEqual(double_metaphone('Langer', 4), ('LNKR', 'LNJR'))
        self.assertEqual(double_metaphone('Langford', 4), ('LNKF', ''))
        self.assertEqual(double_metaphone('Lantersee', 4), ('LNTR', ''))
        self.assertEqual(double_metaphone('Laquer', 4), ('LKR', ''))
        self.assertEqual(double_metaphone('Larkin', 4), ('LRKN', ''))
        self.assertEqual(double_metaphone('Latham', 4), ('LTM', ''))
        self.assertEqual(double_metaphone('Lathrop', 4), ('L0RP', 'LTRP'))
        self.assertEqual(double_metaphone('Lauter', 4), ('LTR', ''))
        self.assertEqual(double_metaphone('Lawrence', 4), ('LRNS', ''))
        self.assertEqual(double_metaphone('Leach', 4), ('LK', ''))
        self.assertEqual(double_metaphone('Leager', 4), ('LKR', 'LJR'))
        self.assertEqual(double_metaphone('Learned', 4), ('LRNT', ''))
        self.assertEqual(double_metaphone('Leavitt', 4), ('LFT', ''))
        self.assertEqual(double_metaphone('Lee', 4), ('L', ''))
        self.assertEqual(double_metaphone('Leete', 4), ('LT', ''))
        self.assertEqual(double_metaphone('Leggett', 4), ('LKT', ''))
        self.assertEqual(double_metaphone('Leland', 4), ('LLNT', ''))
        self.assertEqual(double_metaphone('Leonard', 4), ('LNRT', ''))
        self.assertEqual(double_metaphone('Lester', 4), ('LSTR', ''))
        self.assertEqual(double_metaphone('Lestrange', 4), ('LSTR', ''))
        self.assertEqual(double_metaphone('Lethem', 4), ('L0M', 'LTM'))
        self.assertEqual(double_metaphone('Levine', 4), ('LFN', ''))
        self.assertEqual(double_metaphone('Lewes', 4), ('LS', ''))
        self.assertEqual(double_metaphone('Lewis', 4), ('LS', ''))
        self.assertEqual(double_metaphone('Lincoln', 4), ('LNKL', ''))
        self.assertEqual(double_metaphone('Lindsey', 4), ('LNTS', ''))
        self.assertEqual(double_metaphone('Linher', 4), ('LNR', ''))
        self.assertEqual(double_metaphone('Lippet', 4), ('LPT', ''))
        self.assertEqual(double_metaphone('Lippincott', 4), ('LPNK', ''))
        self.assertEqual(double_metaphone('Lockwood', 4), ('LKT', ''))
        self.assertEqual(double_metaphone('Loines', 4), ('LNS', ''))
        self.assertEqual(double_metaphone('Lombard', 4), ('LMPR', ''))
        self.assertEqual(double_metaphone('Long', 4), ('LNK', ''))
        self.assertEqual(double_metaphone('Longespee', 4), ('LNJS', 'LNKS'))
        self.assertEqual(double_metaphone('Look', 4), ('LK', ''))
        self.assertEqual(double_metaphone('Lounsberry', 4), ('LNSP', ''))
        self.assertEqual(double_metaphone('Lounsbury', 4), ('LNSP', ''))
        self.assertEqual(double_metaphone('Louthe', 4), ('L0', 'LT'))
        self.assertEqual(double_metaphone('Loveyne', 4), ('LFN', ''))
        self.assertEqual(double_metaphone('Lowe', 4), ('L', ''))
        self.assertEqual(double_metaphone('Ludlam', 4), ('LTLM', ''))
        self.assertEqual(double_metaphone('Lumbard', 4), ('LMPR', ''))
        self.assertEqual(double_metaphone('Lund', 4), ('LNT', ''))
        self.assertEqual(double_metaphone('Luno', 4), ('LN', ''))
        self.assertEqual(double_metaphone('Lutz', 4), ('LTS', ''))
        self.assertEqual(double_metaphone('Lydia', 4), ('LT', ''))
        self.assertEqual(double_metaphone('Lynne', 4), ('LN', ''))
        self.assertEqual(double_metaphone('Lyon', 4), ('LN', ''))
        self.assertEqual(double_metaphone('MacAlpin', 4), ('MKLP', ''))
        self.assertEqual(double_metaphone('MacBricc', 4), ('MKPR', ''))
        self.assertEqual(double_metaphone('MacCrinan', 4), ('MKRN', ''))
        self.assertEqual(double_metaphone('MacKenneth', 4), ('MKN0', 'MKNT'))
        self.assertEqual(double_metaphone('MacMael nam Bo', 4), ('MKML', ''))
        self.assertEqual(double_metaphone('MacMurchada', 4), ('MKMR', ''))
        self.assertEqual(double_metaphone('Macomber', 4), ('MKMP', ''))
        self.assertEqual(double_metaphone('Macy', 4), ('MS', ''))
        self.assertEqual(double_metaphone('Magnus', 4), ('MNS', 'MKNS'))
        self.assertEqual(double_metaphone('Mahien', 4), ('MHN', ''))
        self.assertEqual(double_metaphone('Malmains', 4), ('MLMN', ''))
        self.assertEqual(double_metaphone('Malory', 4), ('MLR', ''))
        self.assertEqual(double_metaphone('Mancinelli', 4), ('MNSN', ''))
        self.assertEqual(double_metaphone('Mancini', 4), ('MNSN', ''))
        self.assertEqual(double_metaphone('Mann', 4), ('MN', ''))
        self.assertEqual(double_metaphone('Manning', 4), ('MNNK', ''))
        self.assertEqual(double_metaphone('Manter', 4), ('MNTR', ''))
        self.assertEqual(double_metaphone('Marion', 4), ('MRN', ''))
        self.assertEqual(double_metaphone('Marley', 4), ('MRL', ''))
        self.assertEqual(double_metaphone('Marmion', 4), ('MRMN', ''))
        self.assertEqual(double_metaphone('Marquart', 4), ('MRKR', ''))
        self.assertEqual(double_metaphone('Marsh', 4), ('MRX', ''))
        self.assertEqual(double_metaphone('Marshal', 4), ('MRXL', ''))
        self.assertEqual(double_metaphone('Marshall', 4), ('MRXL', ''))
        self.assertEqual(double_metaphone('Martel', 4), ('MRTL', ''))
        self.assertEqual(double_metaphone('Martha', 4), ('MR0', 'MRT'))
        self.assertEqual(double_metaphone('Martin', 4), ('MRTN', ''))
        self.assertEqual(double_metaphone('Marturano', 4), ('MRTR', ''))
        self.assertEqual(double_metaphone('Marvin', 4), ('MRFN', ''))
        self.assertEqual(double_metaphone('Mary', 4), ('MR', ''))
        self.assertEqual(double_metaphone('Mason', 4), ('MSN', ''))
        self.assertEqual(double_metaphone('Maxwell', 4), ('MKSL', ''))
        self.assertEqual(double_metaphone('Mayhew', 4), ('MH', 'MHF'))
        self.assertEqual(double_metaphone('McAllaster', 4), ('MKLS', ''))
        self.assertEqual(double_metaphone('McAllister', 4), ('MKLS', ''))
        self.assertEqual(double_metaphone('McConnell', 4), ('MKNL', ''))
        self.assertEqual(double_metaphone('McFarland', 4), ('MKFR', ''))
        self.assertEqual(double_metaphone('McIlroy', 4), ('MSLR', ''))
        self.assertEqual(double_metaphone('McNair', 4), ('MKNR', ''))
        self.assertEqual(double_metaphone('McNair-Landry', 4), ('MKNR', ''))
        self.assertEqual(double_metaphone('McRaven', 4), ('MKRF', ''))
        self.assertEqual(double_metaphone('Mead', 4), ('MT', ''))
        self.assertEqual(double_metaphone('Meade', 4), ('MT', ''))
        self.assertEqual(double_metaphone('Meck', 4), ('MK', ''))
        self.assertEqual(double_metaphone('Melton', 4), ('MLTN', ''))
        self.assertEqual(double_metaphone('Mendenhall', 4), ('MNTN', ''))
        self.assertEqual(double_metaphone('Mering', 4), ('MRNK', ''))
        self.assertEqual(double_metaphone('Merrick', 4), ('MRK', ''))
        self.assertEqual(double_metaphone('Merry', 4), ('MR', ''))
        self.assertEqual(double_metaphone('Mighill', 4), ('ML', ''))
        self.assertEqual(double_metaphone('Miller', 4), ('MLR', ''))
        self.assertEqual(double_metaphone('Milton', 4), ('MLTN', ''))
        self.assertEqual(double_metaphone('Mohun', 4), ('MHN', ''))
        self.assertEqual(double_metaphone('Montague', 4), ('MNTK', ''))
        self.assertEqual(double_metaphone('Montboucher', 4), ('MNTP', ''))
        self.assertEqual(double_metaphone('Moore', 4), ('MR', ''))
        self.assertEqual(double_metaphone('Morrel', 4), ('MRL', ''))
        self.assertEqual(double_metaphone('Morrill', 4), ('MRL', ''))
        self.assertEqual(double_metaphone('Morris', 4), ('MRS', ''))
        self.assertEqual(double_metaphone('Morton', 4), ('MRTN', ''))
        self.assertEqual(double_metaphone('Moton', 4), ('MTN', ''))
        self.assertEqual(double_metaphone('Muir', 4), ('MR', ''))
        self.assertEqual(double_metaphone('Mulferd', 4), ('MLFR', ''))
        self.assertEqual(double_metaphone('Mullins', 4), ('MLNS', ''))
        self.assertEqual(double_metaphone('Mulso', 4), ('MLS', ''))
        self.assertEqual(double_metaphone('Munger', 4), ('MNKR', 'MNJR'))
        self.assertEqual(double_metaphone('Munt', 4), ('MNT', ''))
        self.assertEqual(double_metaphone('Murchad', 4), ('MRXT', 'MRKT'))
        self.assertEqual(double_metaphone('Murdock', 4), ('MRTK', ''))
        self.assertEqual(double_metaphone('Murray', 4), ('MR', ''))
        self.assertEqual(double_metaphone('Muskett', 4), ('MSKT', ''))
        self.assertEqual(double_metaphone('Myers', 4), ('MRS', ''))
        self.assertEqual(double_metaphone('Myrick', 4), ('MRK', ''))
        self.assertEqual(double_metaphone('NORRIS', 4), ('NRS', ''))
        self.assertEqual(double_metaphone('Nayle', 4), ('NL', ''))
        self.assertEqual(double_metaphone('Newcomb', 4), ('NKMP', ''))
        self.assertEqual(double_metaphone('Newcomb(e)', 4), ('NKMP', ''))
        self.assertEqual(double_metaphone('Newkirk', 4), ('NKRK', ''))
        self.assertEqual(double_metaphone('Newton', 4), ('NTN', ''))
        self.assertEqual(double_metaphone('Niles', 4), ('NLS', ''))
        self.assertEqual(double_metaphone('Noble', 4), ('NPL', ''))
        self.assertEqual(double_metaphone('Noel', 4), ('NL', ''))
        self.assertEqual(double_metaphone('Northend', 4), ('NR0N', 'NRTN'))
        self.assertEqual(double_metaphone('Norton', 4), ('NRTN', ''))
        self.assertEqual(double_metaphone('Nutter', 4), ('NTR', ''))
        self.assertEqual(double_metaphone('Odding', 4), ('ATNK', ''))
        self.assertEqual(double_metaphone('Odenbaugh', 4), ('ATNP', ''))
        self.assertEqual(double_metaphone('Ogborn', 4), ('AKPR', ''))
        self.assertEqual(double_metaphone('Oppenheimer', 4), ('APNM', ''))
        self.assertEqual(double_metaphone('Otis', 4), ('ATS', ''))
        self.assertEqual(double_metaphone('Oviatt', 4), ('AFT', ''))
        self.assertEqual(double_metaphone('PRUST?', 4), ('PRST', ''))
        self.assertEqual(double_metaphone('Paddock', 4), ('PTK', ''))
        self.assertEqual(double_metaphone('Page', 4), ('PJ', 'PK'))
        self.assertEqual(double_metaphone('Paine', 4), ('PN', ''))
        self.assertEqual(double_metaphone('Paist', 4), ('PST', ''))
        self.assertEqual(double_metaphone('Palmer', 4), ('PLMR', ''))
        self.assertEqual(double_metaphone('Park', 4), ('PRK', ''))
        self.assertEqual(double_metaphone('Parker', 4), ('PRKR', ''))
        self.assertEqual(double_metaphone('Parkhurst', 4), ('PRKR', ''))
        self.assertEqual(double_metaphone('Parrat', 4), ('PRT', ''))
        self.assertEqual(double_metaphone('Parsons', 4), ('PRSN', ''))
        self.assertEqual(double_metaphone('Partridge', 4), ('PRTR', ''))
        self.assertEqual(double_metaphone('Pashley', 4), ('PXL', ''))
        self.assertEqual(double_metaphone('Pasley', 4), ('PSL', ''))
        self.assertEqual(double_metaphone('Patrick', 4), ('PTRK', ''))
        self.assertEqual(double_metaphone('Pattee', 4), ('PT', ''))
        self.assertEqual(double_metaphone('Patten', 4), ('PTN', ''))
        self.assertEqual(double_metaphone('Pawley', 4), ('PL', ''))
        self.assertEqual(double_metaphone('Payne', 4), ('PN', ''))
        self.assertEqual(double_metaphone('Peabody', 4), ('PPT', ''))
        self.assertEqual(double_metaphone('Peake', 4), ('PK', ''))
        self.assertEqual(double_metaphone('Pearson', 4), ('PRSN', ''))
        self.assertEqual(double_metaphone('Peat', 4), ('PT', ''))
        self.assertEqual(double_metaphone('Pedersen', 4), ('PTRS', ''))
        self.assertEqual(double_metaphone('Percy', 4), ('PRS', ''))
        self.assertEqual(double_metaphone('Perkins', 4), ('PRKN', ''))
        self.assertEqual(double_metaphone('Perrine', 4), ('PRN', ''))
        self.assertEqual(double_metaphone('Perry', 4), ('PR', ''))
        self.assertEqual(double_metaphone('Peson', 4), ('PSN', ''))
        self.assertEqual(double_metaphone('Peterson', 4), ('PTRS', ''))
        self.assertEqual(double_metaphone('Peyton', 4), ('PTN', ''))
        self.assertEqual(double_metaphone('Phinney', 4), ('FN', ''))
        self.assertEqual(double_metaphone('Pickard', 4), ('PKRT', ''))
        self.assertEqual(double_metaphone('Pierce', 4), ('PRS', ''))
        self.assertEqual(double_metaphone('Pierrepont', 4), ('PRPN', ''))
        self.assertEqual(double_metaphone('Pike', 4), ('PK', ''))
        self.assertEqual(double_metaphone('Pinkham', 4), ('PNKM', ''))
        self.assertEqual(double_metaphone('Pitman', 4), ('PTMN', ''))
        self.assertEqual(double_metaphone('Pitt', 4), ('PT', ''))
        self.assertEqual(double_metaphone('Pitts', 4), ('PTS', ''))
        self.assertEqual(double_metaphone('Plantagenet', 4), ('PLNT', ''))
        self.assertEqual(double_metaphone('Platt', 4), ('PLT', ''))
        self.assertEqual(double_metaphone('Platts', 4), ('PLTS', ''))
        self.assertEqual(double_metaphone('Pleis', 4), ('PLS', ''))
        self.assertEqual(double_metaphone('Pleiss', 4), ('PLS', ''))
        self.assertEqual(double_metaphone('Plisko', 4), ('PLSK', ''))
        self.assertEqual(double_metaphone('Pliskovitch', 4), ('PLSK', ''))
        self.assertEqual(double_metaphone('Plum', 4), ('PLM', ''))
        self.assertEqual(double_metaphone('Plume', 4), ('PLM', ''))
        self.assertEqual(double_metaphone('Poitou', 4), ('PT', ''))
        self.assertEqual(double_metaphone('Pomeroy', 4), ('PMR', ''))
        self.assertEqual(double_metaphone('Poretiers', 4), ('PRTR', ''))
        self.assertEqual(double_metaphone('Pote', 4), ('PT', ''))
        self.assertEqual(double_metaphone('Potter', 4), ('PTR', ''))
        self.assertEqual(double_metaphone('Potts', 4), ('PTS', ''))
        self.assertEqual(double_metaphone('Powell', 4), ('PL', ''))
        self.assertEqual(double_metaphone('Pratt', 4), ('PRT', ''))
        self.assertEqual(double_metaphone('Presbury', 4), ('PRSP', ''))
        self.assertEqual(double_metaphone('Priest', 4), ('PRST', ''))
        self.assertEqual(double_metaphone('Prindle', 4), ('PRNT', ''))
        self.assertEqual(double_metaphone('Prior', 4), ('PRR', ''))
        self.assertEqual(double_metaphone('Profumo', 4), ('PRFM', ''))
        self.assertEqual(double_metaphone('Purdy', 4), ('PRT', ''))
        self.assertEqual(double_metaphone('Purefoy', 4), ('PRF', ''))
        self.assertEqual(double_metaphone('Pury', 4), ('PR', ''))
        self.assertEqual(double_metaphone('Quinter', 4), ('KNTR', ''))
        self.assertEqual(double_metaphone('Rachel', 4), ('RXL', 'RKL'))
        self.assertEqual(double_metaphone('Rand', 4), ('RNT', ''))
        self.assertEqual(double_metaphone('Rankin', 4), ('RNKN', ''))
        self.assertEqual(double_metaphone('Ravenscroft', 4), ('RFNS', ''))
        self.assertEqual(double_metaphone('Raynsford', 4), ('RNSF', ''))
        self.assertEqual(double_metaphone('Reakirt', 4), ('RKRT', ''))
        self.assertEqual(double_metaphone('Reaves', 4), ('RFS', ''))
        self.assertEqual(double_metaphone('Reeves', 4), ('RFS', ''))
        self.assertEqual(double_metaphone('Reichert', 4), ('RXRT', 'RKRT'))
        self.assertEqual(double_metaphone('Remmele', 4), ('RML', ''))
        self.assertEqual(double_metaphone('Reynolds', 4), ('RNLT', ''))
        self.assertEqual(double_metaphone('Rhodes', 4), ('RTS', ''))
        self.assertEqual(double_metaphone('Richards', 4), ('RXRT', 'RKRT'))
        self.assertEqual(double_metaphone('Richardson', 4), ('RXRT', 'RKRT'))
        self.assertEqual(double_metaphone('Ring', 4), ('RNK', ''))
        self.assertEqual(double_metaphone('Roberts', 4), ('RPRT', ''))
        self.assertEqual(double_metaphone('Robertson', 4), ('RPRT', ''))
        self.assertEqual(double_metaphone('Robson', 4), ('RPSN', ''))
        self.assertEqual(double_metaphone('Rodie', 4), ('RT', ''))
        self.assertEqual(double_metaphone('Rody', 4), ('RT', ''))
        self.assertEqual(double_metaphone('Rogers', 4), ('RKRS', 'RJRS'))
        self.assertEqual(double_metaphone('Ross', 4), ('RS', ''))
        self.assertEqual(double_metaphone('Rosslevin', 4), ('RSLF', ''))
        self.assertEqual(double_metaphone('Rowland', 4), ('RLNT', ''))
        self.assertEqual(double_metaphone('Ruehl', 4), ('RL', ''))
        self.assertEqual(double_metaphone('Russell', 4), ('RSL', ''))
        self.assertEqual(double_metaphone('Ruth', 4), ('R0', 'RT'))
        self.assertEqual(double_metaphone('Ryan', 4), ('RN', ''))
        self.assertEqual(double_metaphone('Rysse', 4), ('RS', ''))
        self.assertEqual(double_metaphone('Sadler', 4), ('STLR', ''))
        self.assertEqual(double_metaphone('Salmon', 4), ('SLMN', ''))
        self.assertEqual(double_metaphone('Salter', 4), ('SLTR', ''))
        self.assertEqual(double_metaphone('Salvatore', 4), ('SLFT', ''))
        self.assertEqual(double_metaphone('Sanders', 4), ('SNTR', ''))
        self.assertEqual(double_metaphone('Sands', 4), ('SNTS', ''))
        self.assertEqual(double_metaphone('Sanford', 4), ('SNFR', ''))
        self.assertEqual(double_metaphone('Sanger', 4), ('SNKR', 'SNJR'))
        self.assertEqual(double_metaphone('Sargent', 4), ('SRJN', 'SRKN'))
        self.assertEqual(double_metaphone('Saunders', 4), ('SNTR', ''))
        self.assertEqual(double_metaphone('Schilling', 4), ('XLNK', ''))
        self.assertEqual(double_metaphone('Schlegel', 4), ('XLKL', 'SLKL'))
        self.assertEqual(double_metaphone('Scott', 4), ('SKT', ''))
        self.assertEqual(double_metaphone('Sears', 4), ('SRS', ''))
        self.assertEqual(double_metaphone('Segersall', 4), ('SJRS', 'SKRS'))
        self.assertEqual(double_metaphone('Senecal', 4), ('SNKL', ''))
        self.assertEqual(double_metaphone('Sergeaux', 4), ('SRJ', 'SRK'))
        self.assertEqual(double_metaphone('Severance', 4), ('SFRN', ''))
        self.assertEqual(double_metaphone('Sharp', 4), ('XRP', ''))
        self.assertEqual(double_metaphone('Sharpe', 4), ('XRP', ''))
        self.assertEqual(double_metaphone('Sharply', 4), ('XRPL', ''))
        self.assertEqual(double_metaphone('Shatswell', 4), ('XTSL', ''))
        self.assertEqual(double_metaphone('Shattack', 4), ('XTK', ''))
        self.assertEqual(double_metaphone('Shattock', 4), ('XTK', ''))
        self.assertEqual(double_metaphone('Shattuck', 4), ('XTK', ''))
        self.assertEqual(double_metaphone('Shaw', 4), ('X', 'XF'))
        self.assertEqual(double_metaphone('Sheldon', 4), ('XLTN', ''))
        self.assertEqual(double_metaphone('Sherman', 4), ('XRMN', ''))
        self.assertEqual(double_metaphone('Shinn', 4), ('XN', ''))
        self.assertEqual(double_metaphone('Shirford', 4), ('XRFR', ''))
        self.assertEqual(double_metaphone('Shirley', 4), ('XRL', ''))
        self.assertEqual(double_metaphone('Shively', 4), ('XFL', ''))
        self.assertEqual(double_metaphone('Shoemaker', 4), ('XMKR', ''))
        self.assertEqual(double_metaphone('Short', 4), ('XRT', ''))
        self.assertEqual(double_metaphone('Shotwell', 4), ('XTL', ''))
        self.assertEqual(double_metaphone('Shute', 4), ('XT', ''))
        self.assertEqual(double_metaphone('Sibley', 4), ('SPL', ''))
        self.assertEqual(double_metaphone('Silver', 4), ('SLFR', ''))
        self.assertEqual(double_metaphone('Simes', 4), ('SMS', ''))
        self.assertEqual(double_metaphone('Sinken', 4), ('SNKN', ''))
        self.assertEqual(double_metaphone('Sinn', 4), ('SN', ''))
        self.assertEqual(double_metaphone('Skelton', 4), ('SKLT', ''))
        self.assertEqual(double_metaphone('Skiffe', 4), ('SKF', ''))
        self.assertEqual(double_metaphone('Skotkonung', 4), ('SKTK', ''))
        self.assertEqual(double_metaphone('Slade', 4), ('SLT', 'XLT'))
        self.assertEqual(double_metaphone('Slye', 4), ('SL', 'XL'))
        self.assertEqual(double_metaphone('Smedley', 4), ('SMTL', 'XMTL'))
        self.assertEqual(double_metaphone('Smith', 4), ('SM0', 'XMT'))
        self.assertEqual(double_metaphone('Snow', 4), ('SN', 'XNF'))
        self.assertEqual(double_metaphone('Soole', 4), ('SL', ''))
        self.assertEqual(double_metaphone('Soule', 4), ('SL', ''))
        self.assertEqual(double_metaphone('Southworth', 4), ('S0R0', 'STRT'))
        self.assertEqual(double_metaphone('Sowles', 4), ('SLS', ''))
        self.assertEqual(double_metaphone('Spalding', 4), ('SPLT', ''))
        self.assertEqual(double_metaphone('Spark', 4), ('SPRK', ''))
        self.assertEqual(double_metaphone('Spencer', 4), ('SPNS', ''))
        self.assertEqual(double_metaphone('Sperry', 4), ('SPR', ''))
        self.assertEqual(double_metaphone('Spofford', 4), ('SPFR', ''))
        self.assertEqual(double_metaphone('Spooner', 4), ('SPNR', ''))
        self.assertEqual(double_metaphone('Sprague', 4), ('SPRK', ''))
        self.assertEqual(double_metaphone('Springer', 4), ('SPRN', ''))
        self.assertEqual(double_metaphone('St. Clair', 4), ('STKL', ''))
        self.assertEqual(double_metaphone('St. Claire', 4), ('STKL', ''))
        self.assertEqual(double_metaphone('St. Leger', 4), ('STLJ', 'STLK'))
        self.assertEqual(double_metaphone('St. Omer', 4), ('STMR', ''))
        self.assertEqual(double_metaphone('Stafferton', 4), ('STFR', ''))
        self.assertEqual(double_metaphone('Stafford', 4), ('STFR', ''))
        self.assertEqual(double_metaphone('Stalham', 4), ('STLM', ''))
        self.assertEqual(double_metaphone('Stanford', 4), ('STNF', ''))
        self.assertEqual(double_metaphone('Stanton', 4), ('STNT', ''))
        self.assertEqual(double_metaphone('Star', 4), ('STR', ''))
        self.assertEqual(double_metaphone('Starbuck', 4), ('STRP', ''))
        self.assertEqual(double_metaphone('Starkey', 4), ('STRK', ''))
        self.assertEqual(double_metaphone('Starkweather', 4), ('STRK', ''))
        self.assertEqual(double_metaphone('Stearns', 4), ('STRN', ''))
        self.assertEqual(double_metaphone('Stebbins', 4), ('STPN', ''))
        self.assertEqual(double_metaphone('Steele', 4), ('STL', ''))
        self.assertEqual(double_metaphone('Stephenson', 4), ('STFN', ''))
        self.assertEqual(double_metaphone('Stevens', 4), ('STFN', ''))
        self.assertEqual(double_metaphone('Stoddard', 4), ('STTR', ''))
        self.assertEqual(double_metaphone('Stodder', 4), ('STTR', ''))
        self.assertEqual(double_metaphone('Stone', 4), ('STN', ''))
        self.assertEqual(double_metaphone('Storey', 4), ('STR', ''))
        self.assertEqual(double_metaphone('Storrada', 4), ('STRT', ''))
        self.assertEqual(double_metaphone('Story', 4), ('STR', ''))
        self.assertEqual(double_metaphone('Stoughton', 4), ('STFT', ''))
        self.assertEqual(double_metaphone('Stout', 4), ('STT', ''))
        self.assertEqual(double_metaphone('Stow', 4), ('ST', 'STF'))
        self.assertEqual(double_metaphone('Strong', 4), ('STRN', ''))
        self.assertEqual(double_metaphone('Strutt', 4), ('STRT', ''))
        self.assertEqual(double_metaphone('Stryker', 4), ('STRK', ''))
        self.assertEqual(double_metaphone('Stuckeley', 4), ('STKL', ''))
        self.assertEqual(double_metaphone('Sturges', 4), ('STRJ', 'STRK'))
        self.assertEqual(double_metaphone('Sturgess', 4), ('STRJ', 'STRK'))
        self.assertEqual(double_metaphone('Sturgis', 4), ('STRJ', 'STRK'))
        self.assertEqual(double_metaphone('Suevain', 4), ('SFN', ''))
        self.assertEqual(double_metaphone('Sulyard', 4), ('SLRT', ''))
        self.assertEqual(double_metaphone('Sutton', 4), ('STN', ''))
        self.assertEqual(double_metaphone('Swain', 4), ('SN', 'XN'))
        self.assertEqual(double_metaphone('Swayne', 4), ('SN', 'XN'))
        self.assertEqual(double_metaphone('Swayze', 4), ('SS', 'XTS'))
        self.assertEqual(double_metaphone('Swift', 4), ('SFT', 'XFT'))
        self.assertEqual(double_metaphone('Taber', 4), ('TPR', ''))
        self.assertEqual(double_metaphone('Talcott', 4), ('TLKT', ''))
        self.assertEqual(double_metaphone('Tarne', 4), ('TRN', ''))
        self.assertEqual(double_metaphone('Tatum', 4), ('TTM', ''))
        self.assertEqual(double_metaphone('Taverner', 4), ('TFRN', ''))
        self.assertEqual(double_metaphone('Taylor', 4), ('TLR', ''))
        self.assertEqual(double_metaphone('Tenney', 4), ('TN', ''))
        self.assertEqual(double_metaphone('Thayer', 4), ('0R', 'TR'))
        self.assertEqual(double_metaphone('Thember', 4), ('0MPR', 'TMPR'))
        self.assertEqual(double_metaphone('Thomas', 4), ('TMS', ''))
        self.assertEqual(double_metaphone('Thompson', 4), ('TMPS', ''))
        self.assertEqual(double_metaphone('Thorne', 4), ('0RN', 'TRN'))
        self.assertEqual(double_metaphone('Thornycraft', 4), ('0RNK', 'TRNK'))
        self.assertEqual(double_metaphone('Threlkeld', 4), ('0RLK', 'TRLK'))
        self.assertEqual(double_metaphone('Throckmorton', 4), ('0RKM', 'TRKM'))
        self.assertEqual(double_metaphone('Thwaits', 4), ('0TS', 'TTS'))
        self.assertEqual(double_metaphone('Tibbetts', 4), ('TPTS', ''))
        self.assertEqual(double_metaphone('Tidd', 4), ('TT', ''))
        self.assertEqual(double_metaphone('Tierney', 4), ('TRN', ''))
        self.assertEqual(double_metaphone('Tilley', 4), ('TL', ''))
        self.assertEqual(double_metaphone('Tillieres', 4), ('TLRS', ''))
        self.assertEqual(double_metaphone('Tilly', 4), ('TL', ''))
        self.assertEqual(double_metaphone('Tisdale', 4), ('TSTL', ''))
        self.assertEqual(double_metaphone('Titus', 4), ('TTS', ''))
        self.assertEqual(double_metaphone('Tobey', 4), ('TP', ''))
        self.assertEqual(double_metaphone('Tooker', 4), ('TKR', ''))
        self.assertEqual(double_metaphone('Towle', 4), ('TL', ''))
        self.assertEqual(double_metaphone('Towne', 4), ('TN', ''))
        self.assertEqual(double_metaphone('Townsend', 4), ('TNSN', ''))
        self.assertEqual(double_metaphone('Treadway', 4), ('TRT', ''))
        self.assertEqual(double_metaphone('Trelawney', 4), ('TRLN', ''))
        self.assertEqual(double_metaphone('Trinder', 4), ('TRNT', ''))
        self.assertEqual(double_metaphone('Tripp', 4), ('TRP', ''))
        self.assertEqual(double_metaphone('Trippe', 4), ('TRP', ''))
        self.assertEqual(double_metaphone('Trott', 4), ('TRT', ''))
        self.assertEqual(double_metaphone('True', 4), ('TR', ''))
        self.assertEqual(double_metaphone('Trussebut', 4), ('TRSP', ''))
        self.assertEqual(double_metaphone('Tucker', 4), ('TKR', ''))
        self.assertEqual(double_metaphone('Turgeon', 4), ('TRJN', 'TRKN'))
        self.assertEqual(double_metaphone('Turner', 4), ('TRNR', ''))
        self.assertEqual(double_metaphone('Tuttle', 4), ('TTL', ''))
        self.assertEqual(double_metaphone('Tyler', 4), ('TLR', ''))
        self.assertEqual(double_metaphone('Tylle', 4), ('TL', ''))
        self.assertEqual(double_metaphone('Tyrrel', 4), ('TRL', ''))
        self.assertEqual(double_metaphone('Ua Tuathail', 4), ('AT0L', 'ATTL'))
        self.assertEqual(double_metaphone('Ulrich', 4), ('ALRX', 'ALRK'))
        self.assertEqual(double_metaphone('Underhill', 4), ('ANTR', ''))
        self.assertEqual(double_metaphone('Underwood', 4), ('ANTR', ''))
        self.assertEqual(double_metaphone('Unknown', 4), ('ANKN', ''))
        self.assertEqual(double_metaphone('Valentine', 4), ('FLNT', ''))
        self.assertEqual(double_metaphone('Van Egmond', 4), ('FNKM', ''))
        self.assertEqual(double_metaphone('Van der Beek', 4), ('FNTR', ''))
        self.assertEqual(double_metaphone('Vaughan', 4), ('FKN', ''))
        self.assertEqual(double_metaphone('Vermenlen', 4), ('FRMN', ''))
        self.assertEqual(double_metaphone('Vincent', 4), ('FNSN', ''))
        self.assertEqual(double_metaphone('Volentine', 4), ('FLNT', ''))
        self.assertEqual(double_metaphone('Wagner', 4), ('AKNR', 'FKNR'))
        self.assertEqual(double_metaphone('Waite', 4), ('AT', 'FT'))
        self.assertEqual(double_metaphone('Walker', 4), ('ALKR', 'FLKR'))
        self.assertEqual(double_metaphone('Walter', 4), ('ALTR', 'FLTR'))
        self.assertEqual(double_metaphone('Wandell', 4), ('ANTL', 'FNTL'))
        self.assertEqual(double_metaphone('Wandesford', 4), ('ANTS', 'FNTS'))
        self.assertEqual(double_metaphone('Warbleton', 4), ('ARPL', 'FRPL'))
        self.assertEqual(double_metaphone('Ward', 4), ('ART', 'FRT'))
        self.assertEqual(double_metaphone('Warde', 4), ('ART', 'FRT'))
        self.assertEqual(double_metaphone('Ware', 4), ('AR', 'FR'))
        self.assertEqual(double_metaphone('Wareham', 4), ('ARHM', 'FRHM'))
        self.assertEqual(double_metaphone('Warner', 4), ('ARNR', 'FRNR'))
        self.assertEqual(double_metaphone('Warren', 4), ('ARN', 'FRN'))
        self.assertEqual(double_metaphone('Washburne', 4), ('AXPR', 'FXPR'))
        self.assertEqual(double_metaphone('Waterbury', 4), ('ATRP', 'FTRP'))
        self.assertEqual(double_metaphone('Watson', 4), ('ATSN', 'FTSN'))
        self.assertEqual(double_metaphone('WatsonEllithorpe', 4),
                         ('ATSN', 'FTSN'))
        self.assertEqual(double_metaphone('Watts', 4), ('ATS', 'FTS'))
        self.assertEqual(double_metaphone('Wayne', 4), ('AN', 'FN'))
        self.assertEqual(double_metaphone('Webb', 4), ('AP', 'FP'))
        self.assertEqual(double_metaphone('Weber', 4), ('APR', 'FPR'))
        self.assertEqual(double_metaphone('Webster', 4), ('APST', 'FPST'))
        self.assertEqual(double_metaphone('Weed', 4), ('AT', 'FT'))
        self.assertEqual(double_metaphone('Weeks', 4), ('AKS', 'FKS'))
        self.assertEqual(double_metaphone('Wells', 4), ('ALS', 'FLS'))
        self.assertEqual(double_metaphone('Wenzell', 4), ('ANSL', 'FNTS'))
        self.assertEqual(double_metaphone('West', 4), ('AST', 'FST'))
        self.assertEqual(double_metaphone('Westbury', 4), ('ASTP', 'FSTP'))
        self.assertEqual(double_metaphone('Whatlocke', 4), ('ATLK', ''))
        self.assertEqual(double_metaphone('Wheeler', 4), ('ALR', ''))
        self.assertEqual(double_metaphone('Whiston', 4), ('ASTN', ''))
        self.assertEqual(double_metaphone('White', 4), ('AT', ''))
        self.assertEqual(double_metaphone('Whitman', 4), ('ATMN', ''))
        self.assertEqual(double_metaphone('Whiton', 4), ('ATN', ''))
        self.assertEqual(double_metaphone('Whitson', 4), ('ATSN', ''))
        self.assertEqual(double_metaphone('Wickes', 4), ('AKS', 'FKS'))
        self.assertEqual(double_metaphone('Wilbur', 4), ('ALPR', 'FLPR'))
        self.assertEqual(double_metaphone('Wilcotes', 4), ('ALKT', 'FLKT'))
        self.assertEqual(double_metaphone('Wilkinson', 4), ('ALKN', 'FLKN'))
        self.assertEqual(double_metaphone('Willets', 4), ('ALTS', 'FLTS'))
        self.assertEqual(double_metaphone('Willett', 4), ('ALT', 'FLT'))
        self.assertEqual(double_metaphone('Willey', 4), ('AL', 'FL'))
        self.assertEqual(double_metaphone('Williams', 4), ('ALMS', 'FLMS'))
        self.assertEqual(double_metaphone('Williston', 4), ('ALST', 'FLST'))
        self.assertEqual(double_metaphone('Wilson', 4), ('ALSN', 'FLSN'))
        self.assertEqual(double_metaphone('Wimes', 4), ('AMS', 'FMS'))
        self.assertEqual(double_metaphone('Winch', 4), ('ANX', 'FNK'))
        self.assertEqual(double_metaphone('Winegar', 4), ('ANKR', 'FNKR'))
        self.assertEqual(double_metaphone('Wing', 4), ('ANK', 'FNK'))
        self.assertEqual(double_metaphone('Winsley', 4), ('ANSL', 'FNSL'))
        self.assertEqual(double_metaphone('Winslow', 4), ('ANSL', 'FNSL'))
        self.assertEqual(double_metaphone('Winthrop', 4), ('AN0R', 'FNTR'))
        self.assertEqual(double_metaphone('Wise', 4), ('AS', 'FS'))
        self.assertEqual(double_metaphone('Wood', 4), ('AT', 'FT'))
        self.assertEqual(double_metaphone('Woodbridge', 4), ('ATPR', 'FTPR'))
        self.assertEqual(double_metaphone('Woodward', 4), ('ATRT', 'FTRT'))
        self.assertEqual(double_metaphone('Wooley', 4), ('AL', 'FL'))
        self.assertEqual(double_metaphone('Woolley', 4), ('AL', 'FL'))
        self.assertEqual(double_metaphone('Worth', 4), ('AR0', 'FRT'))
        self.assertEqual(double_metaphone('Worthen', 4), ('AR0N', 'FRTN'))
        self.assertEqual(double_metaphone('Worthley', 4), ('AR0L', 'FRTL'))
        self.assertEqual(double_metaphone('Wright', 4), ('RT', ''))
        self.assertEqual(double_metaphone('Wyer', 4), ('AR', 'FR'))
        self.assertEqual(double_metaphone('Wyere', 4), ('AR', 'FR'))
        self.assertEqual(double_metaphone('Wynkoop', 4), ('ANKP', 'FNKP'))
        self.assertEqual(double_metaphone('Yarnall', 4), ('ARNL', ''))
        self.assertEqual(double_metaphone('Yeoman', 4), ('AMN', ''))
        self.assertEqual(double_metaphone('Yorke', 4), ('ARK', ''))
        self.assertEqual(double_metaphone('Young', 4), ('ANK', ''))
        self.assertEqual(double_metaphone('ab Wennonwen', 4), ('APNN', ''))
        self.assertEqual(double_metaphone('ap Llewellyn', 4), ('APLL', ''))
        self.assertEqual(double_metaphone('ap Lorwerth', 4), ('APLR', ''))
        self.assertEqual(double_metaphone('d\'Angouleme', 4), ('TNKL', ''))
        self.assertEqual(double_metaphone('de Audeham', 4), ('TTHM', ''))
        self.assertEqual(double_metaphone('de Bavant', 4), ('TPFN', ''))
        self.assertEqual(double_metaphone('de Beauchamp', 4), ('TPXM', 'TPKM'))
        self.assertEqual(double_metaphone('de Beaumont', 4), ('TPMN', ''))
        self.assertEqual(double_metaphone('de Bolbec', 4), ('TPLP', ''))
        self.assertEqual(double_metaphone('de Braiose', 4), ('TPRS', ''))
        self.assertEqual(double_metaphone('de Braose', 4), ('TPRS', ''))
        self.assertEqual(double_metaphone('de Briwere', 4), ('TPRR', ''))
        self.assertEqual(double_metaphone('de Cantelou', 4), ('TKNT', ''))
        self.assertEqual(double_metaphone('de Cherelton', 4), ('TXRL', 'TKRL'))
        self.assertEqual(double_metaphone('de Cherleton', 4), ('TXRL', 'TKRL'))
        self.assertEqual(double_metaphone('de Clare', 4), ('TKLR', ''))
        self.assertEqual(double_metaphone('de Claremont', 4), ('TKLR', ''))
        self.assertEqual(double_metaphone('de Clifford', 4), ('TKLF', ''))
        self.assertEqual(double_metaphone('de Colville', 4), ('TKLF', ''))
        self.assertEqual(double_metaphone('de Courtenay', 4), ('TKRT', ''))
        self.assertEqual(double_metaphone('de Fauconberg', 4), ('TFKN', ''))
        self.assertEqual(double_metaphone('de Forest', 4), ('TFRS', ''))
        self.assertEqual(double_metaphone('de Gai', 4), ('TK', ''))
        self.assertEqual(double_metaphone('de Grey', 4), ('TKR', ''))
        self.assertEqual(double_metaphone('de Guernons', 4), ('TKRN', ''))
        self.assertEqual(double_metaphone('de Haia', 4), ('T', ''))
        self.assertEqual(double_metaphone('de Harcourt', 4), ('TRKR', ''))
        self.assertEqual(double_metaphone('de Hastings', 4), ('TSTN', ''))
        self.assertEqual(double_metaphone('de Hoke', 4), ('TK', ''))
        self.assertEqual(double_metaphone('de Hooch', 4), ('TK', ''))
        self.assertEqual(double_metaphone('de Hugelville', 4),
                         ('TJLF', 'TKLF'))
        self.assertEqual(double_metaphone('de Huntingdon', 4), ('TNTN', ''))
        self.assertEqual(double_metaphone('de Insula', 4), ('TNSL', ''))
        self.assertEqual(double_metaphone('de Keynes', 4), ('TKNS', ''))
        self.assertEqual(double_metaphone('de Lacy', 4), ('TLS', ''))
        self.assertEqual(double_metaphone('de Lexington', 4), ('TLKS', ''))
        self.assertEqual(double_metaphone('de Lusignan', 4), ('TLSN', 'TLSK'))
        self.assertEqual(double_metaphone('de Manvers', 4), ('TMNF', ''))
        self.assertEqual(double_metaphone('de Montagu', 4), ('TMNT', ''))
        self.assertEqual(double_metaphone('de Montault', 4), ('TMNT', ''))
        self.assertEqual(double_metaphone('de Montfort', 4), ('TMNT', ''))
        self.assertEqual(double_metaphone('de Mortimer', 4), ('TMRT', ''))
        self.assertEqual(double_metaphone('de Morville', 4), ('TMRF', ''))
        self.assertEqual(double_metaphone('de Morvois', 4), ('TMRF', ''))
        self.assertEqual(double_metaphone('de Neufmarche', 4), ('TNFM', ''))
        self.assertEqual(double_metaphone('de Odingsells', 4), ('TTNK', ''))
        self.assertEqual(double_metaphone('de Odyngsells', 4), ('TTNK', ''))
        self.assertEqual(double_metaphone('de Percy', 4), ('TPRS', ''))
        self.assertEqual(double_metaphone('de Pierrepont', 4), ('TPRP', ''))
        self.assertEqual(double_metaphone('de Plessetis', 4), ('TPLS', ''))
        self.assertEqual(double_metaphone('de Porhoet', 4), ('TPRT', ''))
        self.assertEqual(double_metaphone('de Prouz', 4), ('TPRS', ''))
        self.assertEqual(double_metaphone('de Quincy', 4), ('TKNS', ''))
        self.assertEqual(double_metaphone('de Ripellis', 4), ('TRPL', ''))
        self.assertEqual(double_metaphone('de Ros', 4), ('TRS', ''))
        self.assertEqual(double_metaphone('de Salisbury', 4), ('TSLS', ''))
        self.assertEqual(double_metaphone('de Sanford', 4), ('TSNF', ''))
        self.assertEqual(double_metaphone('de Somery', 4), ('TSMR', ''))
        self.assertEqual(double_metaphone('de St. Hilary', 4), ('TSTL', ''))
        self.assertEqual(double_metaphone('de St. Liz', 4), ('TSTL', ''))
        self.assertEqual(double_metaphone('de Sutton', 4), ('TSTN', ''))
        self.assertEqual(double_metaphone('de Toeni', 4), ('TTN', ''))
        self.assertEqual(double_metaphone('de Tony', 4), ('TTN', ''))
        self.assertEqual(double_metaphone('de Umfreville', 4), ('TMFR', ''))
        self.assertEqual(double_metaphone('de Valognes', 4), ('TFLN', 'TFLK'))
        self.assertEqual(double_metaphone('de Vaux', 4), ('TF', ''))
        self.assertEqual(double_metaphone('de Vere', 4), ('TFR', ''))
        self.assertEqual(double_metaphone('de Vermandois', 4), ('TFRM', ''))
        self.assertEqual(double_metaphone('de Vernon', 4), ('TFRN', ''))
        self.assertEqual(double_metaphone('de Vexin', 4), ('TFKS', ''))
        self.assertEqual(double_metaphone('de Vitre', 4), ('TFTR', ''))
        self.assertEqual(double_metaphone('de Wandesford', 4), ('TNTS', ''))
        self.assertEqual(double_metaphone('de Warenne', 4), ('TRN', ''))
        self.assertEqual(double_metaphone('de Westbury', 4), ('TSTP', ''))
        self.assertEqual(double_metaphone('di Saluzzo', 4), ('TSLS', 'TSLT'))
        self.assertEqual(double_metaphone('fitz Alan', 4), ('FTSL', ''))
        self.assertEqual(double_metaphone('fitz Geoffrey', 4),
                         ('FTSJ', 'FTSK'))
        self.assertEqual(double_metaphone('fitz Herbert', 4), ('FTSR', ''))
        self.assertEqual(double_metaphone('fitz John', 4), ('FTSJ', ''))
        self.assertEqual(double_metaphone('fitz Patrick', 4), ('FTSP', ''))
        self.assertEqual(double_metaphone('fitz Payn', 4), ('FTSP', ''))
        self.assertEqual(double_metaphone('fitz Piers', 4), ('FTSP', ''))
        self.assertEqual(double_metaphone('fitz Randolph', 4), ('FTSR', ''))
        self.assertEqual(double_metaphone('fitz Richard', 4), ('FTSR', ''))
        self.assertEqual(double_metaphone('fitz Robert', 4), ('FTSR', ''))
        self.assertEqual(double_metaphone('fitz Roy', 4), ('FTSR', ''))
        self.assertEqual(double_metaphone('fitz Scrob', 4), ('FTSS', ''))
        self.assertEqual(double_metaphone('fitz Walter', 4), ('FTSL', ''))
        self.assertEqual(double_metaphone('fitz Warin', 4), ('FTSR', ''))
        self.assertEqual(double_metaphone('fitz Williams', 4), ('FTSL', ''))
        self.assertEqual(double_metaphone('la Zouche', 4), ('LSX', 'LSK'))
        self.assertEqual(double_metaphone('le Botiller', 4), ('LPTL', ''))
        self.assertEqual(double_metaphone('le Despenser', 4), ('LTSP', ''))
        self.assertEqual(double_metaphone('le deSpencer', 4), ('LTSP', ''))
        self.assertEqual(double_metaphone('of Allendale', 4), ('AFLN', ''))
        self.assertEqual(double_metaphone('of Angouleme', 4), ('AFNK', ''))
        self.assertEqual(double_metaphone('of Anjou', 4), ('AFNJ', ''))
        self.assertEqual(double_metaphone('of Aquitaine', 4), ('AFKT', ''))
        self.assertEqual(double_metaphone('of Aumale', 4), ('AFML', ''))
        self.assertEqual(double_metaphone('of Bavaria', 4), ('AFPF', ''))
        self.assertEqual(double_metaphone('of Boulogne', 4), ('AFPL', ''))
        self.assertEqual(double_metaphone('of Brittany', 4), ('AFPR', ''))
        self.assertEqual(double_metaphone('of Brittary', 4), ('AFPR', ''))
        self.assertEqual(double_metaphone('of Castile', 4), ('AFKS', ''))
        self.assertEqual(double_metaphone('of Chester', 4), ('AFXS', 'AFKS'))
        self.assertEqual(double_metaphone('of Clermont', 4), ('AFKL', ''))
        self.assertEqual(double_metaphone('of Cologne', 4), ('AFKL', ''))
        self.assertEqual(double_metaphone('of Dinan', 4), ('AFTN', ''))
        self.assertEqual(double_metaphone('of Dunbar', 4), ('AFTN', ''))
        self.assertEqual(double_metaphone('of England', 4), ('AFNK', ''))
        self.assertEqual(double_metaphone('of Essex', 4), ('AFSK', ''))
        self.assertEqual(double_metaphone('of Falaise', 4), ('AFFL', ''))
        self.assertEqual(double_metaphone('of Flanders', 4), ('AFFL', ''))
        self.assertEqual(double_metaphone('of Galloway', 4), ('AFKL', ''))
        self.assertEqual(double_metaphone('of Germany', 4), ('AFKR', 'AFJR'))
        self.assertEqual(double_metaphone('of Gloucester', 4), ('AFKL', ''))
        self.assertEqual(double_metaphone('of Heristal', 4), ('AFRS', ''))
        self.assertEqual(double_metaphone('of Hungary', 4), ('AFNK', ''))
        self.assertEqual(double_metaphone('of Huntington', 4), ('AFNT', ''))
        self.assertEqual(double_metaphone('of Kiev', 4), ('AFKF', ''))
        self.assertEqual(double_metaphone('of Kuno', 4), ('AFKN', ''))
        self.assertEqual(double_metaphone('of Landen', 4), ('AFLN', ''))
        self.assertEqual(double_metaphone('of Laon', 4), ('AFLN', ''))
        self.assertEqual(double_metaphone('of Leinster', 4), ('AFLN', ''))
        self.assertEqual(double_metaphone('of Lens', 4), ('AFLN', ''))
        self.assertEqual(double_metaphone('of Lorraine', 4), ('AFLR', ''))
        self.assertEqual(double_metaphone('of Louvain', 4), ('AFLF', ''))
        self.assertEqual(double_metaphone('of Mercia', 4), ('AFMR', ''))
        self.assertEqual(double_metaphone('of Metz', 4), ('AFMT', ''))
        self.assertEqual(double_metaphone('of Meulan', 4), ('AFML', ''))
        self.assertEqual(double_metaphone('of Nass', 4), ('AFNS', ''))
        self.assertEqual(double_metaphone('of Normandy', 4), ('AFNR', ''))
        self.assertEqual(double_metaphone('of Ohningen', 4), ('AFNN', ''))
        self.assertEqual(double_metaphone('of Orleans', 4), ('AFRL', ''))
        self.assertEqual(double_metaphone('of Poitou', 4), ('AFPT', ''))
        self.assertEqual(double_metaphone('of Polotzk', 4), ('AFPL', ''))
        self.assertEqual(double_metaphone('of Provence', 4), ('AFPR', ''))
        self.assertEqual(double_metaphone('of Ringelheim', 4), ('AFRN', ''))
        self.assertEqual(double_metaphone('of Salisbury', 4), ('AFSL', ''))
        self.assertEqual(double_metaphone('of Saxony', 4), ('AFSK', ''))
        self.assertEqual(double_metaphone('of Scotland', 4), ('AFSK', ''))
        self.assertEqual(double_metaphone('of Senlis', 4), ('AFSN', ''))
        self.assertEqual(double_metaphone('of Stafford', 4), ('AFST', ''))
        self.assertEqual(double_metaphone('of Swabia', 4), ('AFSP', ''))
        self.assertEqual(double_metaphone('of Tongres', 4), ('AFTN', ''))
        self.assertEqual(double_metaphone('of the Tributes', 4),
                         ('AF0T', 'AFTT'))
        self.assertEqual(double_metaphone('unknown', 4), ('ANKN', ''))
        self.assertEqual(double_metaphone('van der Gouda', 4), ('FNTR', ''))
        self.assertEqual(double_metaphone('von Adenbaugh', 4), ('FNTN', ''))
        self.assertEqual(double_metaphone('ARCHITure', 4), ('ARKT', ''))
        self.assertEqual(double_metaphone('Arnoff', 4), ('ARNF', ''))
        self.assertEqual(double_metaphone('Arnow', 4), ('ARN', 'ARNF'))
        self.assertEqual(double_metaphone('DANGER', 4), ('TNJR', 'TNKR'))
        self.assertEqual(double_metaphone('Jankelowicz', 4), ('JNKL', 'ANKL'))
        self.assertEqual(double_metaphone('MANGER', 4), ('MNJR', 'MNKR'))
        self.assertEqual(double_metaphone('McClellan', 4), ('MKLL', ''))
        self.assertEqual(double_metaphone('McHugh', 4), ('MK', ''))
        self.assertEqual(double_metaphone('McLaughlin', 4), ('MKLF', ''))
        self.assertEqual(double_metaphone('ORCHEStra', 4), ('ARKS', ''))
        self.assertEqual(double_metaphone('ORCHID', 4), ('ARKT', ''))
        self.assertEqual(double_metaphone('Pierce', 4), ('PRS', ''))
        self.assertEqual(double_metaphone('RANGER', 4), ('RNJR', 'RNKR'))
        self.assertEqual(double_metaphone('Schlesinger', 4), ('XLSN', 'SLSN'))
        self.assertEqual(double_metaphone('Uomo', 4), ('AM', ''))
        self.assertEqual(double_metaphone('Vasserman', 4), ('FSRM', ''))
        self.assertEqual(double_metaphone('Wasserman', 4), ('ASRM', 'FSRM'))
        self.assertEqual(double_metaphone('Womo', 4), ('AM', 'FM'))
        self.assertEqual(double_metaphone('Yankelovich', 4), ('ANKL', ''))
        self.assertEqual(double_metaphone('accede', 4), ('AKST', ''))
        self.assertEqual(double_metaphone('accident', 4), ('AKST', ''))
        self.assertEqual(double_metaphone('adelsheim', 4), ('ATLS', ''))
        self.assertEqual(double_metaphone('aged', 4), ('AJT', 'AKT'))
        self.assertEqual(double_metaphone('ageless', 4), ('AJLS', 'AKLS'))
        self.assertEqual(double_metaphone('agency', 4), ('AJNS', 'AKNS'))
        self.assertEqual(double_metaphone('aghast', 4), ('AKST', ''))
        self.assertEqual(double_metaphone('agio', 4), ('AJ', 'AK'))
        self.assertEqual(double_metaphone('agrimony', 4), ('AKRM', ''))
        self.assertEqual(double_metaphone('album', 4), ('ALPM', ''))
        self.assertEqual(double_metaphone('alcmene', 4), ('ALKM', ''))
        self.assertEqual(double_metaphone('alehouse', 4), ('ALHS', ''))
        self.assertEqual(double_metaphone('antique', 4), ('ANTK', ''))
        self.assertEqual(double_metaphone('artois', 4), ('ART', 'ARTS'))
        self.assertEqual(double_metaphone('automation', 4), ('ATMX', ''))
        self.assertEqual(double_metaphone('bacchus', 4), ('PKS', ''))
        self.assertEqual(double_metaphone('bacci', 4), ('PX', ''))
        self.assertEqual(double_metaphone('bajador', 4), ('PJTR', 'PHTR'))
        self.assertEqual(double_metaphone('bellocchio', 4), ('PLX', ''))
        self.assertEqual(double_metaphone('bertucci', 4), ('PRTX', ''))
        self.assertEqual(double_metaphone('biaggi', 4), ('PJ', 'PK'))
        self.assertEqual(double_metaphone('bough', 4), ('P', ''))
        self.assertEqual(double_metaphone('breaux', 4), ('PR', ''))
        self.assertEqual(double_metaphone('broughton', 4), ('PRTN', ''))
        self.assertEqual(double_metaphone('cabrillo', 4), ('KPRL', 'KPR'))
        self.assertEqual(double_metaphone('caesar', 4), ('SSR', ''))
        self.assertEqual(double_metaphone('cagney', 4), ('KKN', ''))
        self.assertEqual(double_metaphone('campbell', 4), ('KMPL', ''))
        self.assertEqual(double_metaphone('carlisle', 4), ('KRLL', ''))
        self.assertEqual(double_metaphone('carlysle', 4), ('KRLL', ''))
        self.assertEqual(double_metaphone('chemistry', 4), ('KMST', ''))
        self.assertEqual(double_metaphone('chianti', 4), ('KNT', ''))
        self.assertEqual(double_metaphone('chorus', 4), ('KRS', ''))
        self.assertEqual(double_metaphone('cough', 4), ('KF', ''))
        self.assertEqual(double_metaphone('czerny', 4), ('SRN', 'XRN'))
        self.assertEqual(double_metaphone('deffenbacher', 4), ('TFNP', ''))
        self.assertEqual(double_metaphone('dumb', 4), ('TM', ''))
        self.assertEqual(double_metaphone('edgar', 4), ('ATKR', ''))
        self.assertEqual(double_metaphone('edge', 4), ('AJ', ''))
        self.assertEqual(double_metaphone('filipowicz', 4), ('FLPT', 'FLPF'))
        self.assertEqual(double_metaphone('focaccia', 4), ('FKX', ''))
        self.assertEqual(double_metaphone('gallegos', 4), ('KLKS', 'KKS'))
        self.assertEqual(double_metaphone('gambrelli', 4), ('KMPR', ''))
        self.assertEqual(double_metaphone('geithain', 4), ('K0N', 'JTN'))
        self.assertEqual(double_metaphone('ghiradelli', 4), ('JRTL', ''))
        self.assertEqual(double_metaphone('ghislane', 4), ('JLN', ''))
        self.assertEqual(double_metaphone('gough', 4), ('KF', ''))
        self.assertEqual(double_metaphone('hartheim', 4), ('HR0M', 'HRTM'))
        self.assertEqual(double_metaphone('heimsheim', 4), ('HMSM', ''))
        self.assertEqual(double_metaphone('hochmeier', 4), ('HKMR', ''))
        self.assertEqual(double_metaphone('hugh', 4), ('H', ''))
        self.assertEqual(double_metaphone('hunger', 4), ('HNKR', 'HNJR'))
        self.assertEqual(double_metaphone('hungry', 4), ('HNKR', ''))
        self.assertEqual(double_metaphone('island', 4), ('ALNT', ''))
        self.assertEqual(double_metaphone('isle', 4), ('AL', ''))
        self.assertEqual(double_metaphone('jose', 4), ('HS', ''))
        self.assertEqual(double_metaphone('laugh', 4), ('LF', ''))
        self.assertEqual(double_metaphone('mac caffrey', 4), ('MKFR', ''))
        self.assertEqual(double_metaphone('mac gregor', 4), ('MKRK', ''))
        self.assertEqual(double_metaphone('pegnitz', 4), ('PNTS', 'PKNT'))
        self.assertEqual(double_metaphone('piskowitz', 4), ('PSKT', 'PSKF'))
        self.assertEqual(double_metaphone('queen', 4), ('KN', ''))
        self.assertEqual(double_metaphone('raspberry', 4), ('RSPR', ''))
        self.assertEqual(double_metaphone('resnais', 4), ('RSN', 'RSNS'))
        self.assertEqual(double_metaphone('rogier', 4), ('RJ', 'RJR'))
        self.assertEqual(double_metaphone('rough', 4), ('RF', ''))
        self.assertEqual(double_metaphone('san jacinto', 4), ('SNHS', ''))
        self.assertEqual(double_metaphone('schenker', 4), ('XNKR', 'SKNK'))
        self.assertEqual(double_metaphone('schermerhorn', 4), ('XRMR', 'SKRM'))
        self.assertEqual(double_metaphone('schmidt', 4), ('XMT', 'SMT'))
        self.assertEqual(double_metaphone('schneider', 4), ('XNTR', 'SNTR'))
        self.assertEqual(double_metaphone('school', 4), ('SKL', ''))
        self.assertEqual(double_metaphone('schooner', 4), ('SKNR', ''))
        self.assertEqual(double_metaphone('schrozberg', 4), ('XRSP', 'SRSP'))
        self.assertEqual(double_metaphone('schulman', 4), ('XLMN', ''))
        self.assertEqual(double_metaphone('schwabach', 4), ('XPK', 'XFPK'))
        self.assertEqual(double_metaphone('schwarzach', 4), ('XRSK', 'XFRT'))
        self.assertEqual(double_metaphone('smith', 4), ('SM0', 'XMT'))
        self.assertEqual(double_metaphone('snider', 4), ('SNTR', 'XNTR'))
        self.assertEqual(double_metaphone('succeed', 4), ('SKST', ''))
        self.assertEqual(double_metaphone('sugarcane', 4), ('XKRK', 'SKRK'))
        self.assertEqual(double_metaphone('svobodka', 4), ('SFPT', ''))
        self.assertEqual(double_metaphone('tagliaro', 4), ('TKLR', 'TLR'))
        self.assertEqual(double_metaphone('thames', 4), ('TMS', ''))
        self.assertEqual(double_metaphone('theilheim', 4), ('0LM', 'TLM'))
        self.assertEqual(double_metaphone('thomas', 4), ('TMS', ''))
        self.assertEqual(double_metaphone('thumb', 4), ('0M', 'TM'))
        self.assertEqual(double_metaphone('tichner', 4), ('TXNR', 'TKNR'))
        self.assertEqual(double_metaphone('tough', 4), ('TF', ''))
        self.assertEqual(double_metaphone('umbrella', 4), ('AMPR', ''))
        self.assertEqual(double_metaphone('vilshofen', 4), ('FLXF', ''))
        self.assertEqual(double_metaphone('von schuller', 4), ('FNXL', ''))
        self.assertEqual(double_metaphone('wachtler', 4), ('AKTL', 'FKTL'))
        self.assertEqual(double_metaphone('wechsler', 4), ('AKSL', 'FKSL'))
        self.assertEqual(double_metaphone('weikersheim', 4), ('AKRS', 'FKRS'))
        self.assertEqual(double_metaphone('zhao', 4), ('J', ''))


class CaverphoneTestCases(unittest.TestCase):
    """Test Caverphone functions.

    test cases for abydos.phonetic.caverphone
    """

    def test_caverphone2(self):
        """Test abydos.phonetic.caverphone (Caverphone 2)."""
        self.assertEqual(caverphone(''), '1111111111')
        self.assertEqual(caverphone('', 2), '1111111111')
        self.assertEqual(caverphone('', version=2), '1111111111')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(caverphone('Henrichsen'), 'ANRKSN1111')
        self.assertEqual(caverphone('Henricsson'), 'ANRKSN1111')
        self.assertEqual(caverphone('Henriksson'), 'ANRKSN1111')
        self.assertEqual(caverphone('Hinrichsen'), 'ANRKSN1111')
        self.assertEqual(caverphone('Izchaki'), 'ASKKA11111')
        self.assertEqual(caverphone('Maclaverty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Mccleverty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Mcclifferty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Mclafferty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Mclaverty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Slocomb'), 'SLKM111111')
        self.assertEqual(caverphone('Slocombe'), 'SLKM111111')
        self.assertEqual(caverphone('Slocumb'), 'SLKM111111')
        self.assertEqual(caverphone('Whitlam'), 'WTLM111111')

        # http://caversham.otago.ac.nz/files/working/ctp150804.pdf
        self.assertEqual(caverphone('Stevenson'), 'STFNSN1111')
        self.assertEqual(caverphone('Peter'), 'PTA1111111')
        for word in ('Darda', 'Datha', 'Dedie', 'Deedee', 'Deerdre', 'Deidre',
                     'Deirdre', 'Detta', 'Didi', 'Didier', 'Dido', 'Dierdre',
                     'Dieter', 'Dita', 'Ditter', 'Dodi', 'Dodie', 'Dody',
                     'Doherty', 'Dorthea', 'Dorthy', 'Doti', 'Dotti', 'Dottie',
                     'Dotty', 'Doty', 'Doughty', 'Douty', 'Dowdell', 'Duthie',
                     'Tada', 'Taddeo', 'Tadeo', 'Tadio', 'Tati', 'Teador',
                     'Tedda', 'Tedder', 'Teddi', 'Teddie', 'Teddy', 'Tedi',
                     'Tedie', 'Teeter', 'Teodoor', 'Teodor', 'Terti', 'Theda',
                     'Theodor', 'Theodore', 'Theta', 'Thilda', 'Thordia',
                     'Tilda', 'Tildi', 'Tildie', 'Tildy', 'Tita', 'Tito',
                     'Tjader', 'Toddie', 'Toddy', 'Torto', 'Tuddor', 'Tudor',
                     'Turtle', 'Tuttle', 'Tutto'):
            self.assertEqual(caverphone(word), 'TTA1111111')
            self.assertEqual(caverphone(word, 2), 'TTA1111111')
            self.assertEqual(caverphone(word, version=2), 'TTA1111111')
        for word in ('Cailean', 'Calan', 'Calen', 'Callahan', 'Callan',
                     'Callean', 'Carleen', 'Carlen', 'Carlene', 'Carlin',
                     'Carline', 'Carlyn', 'Carlynn', 'Carlynne', 'Charlean',
                     'Charleen', 'Charlene', 'Charline', 'Cherlyn', 'Chirlin',
                     'Clein', 'Cleon', 'Cline', 'Cohleen', 'Colan', 'Coleen',
                     'Colene', 'Colin', 'Colleen', 'Collen', 'Collin',
                     'Colline', 'Colon', 'Cullan', 'Cullen', 'Cullin',
                     'Gaelan', 'Galan', 'Galen', 'Garlan', 'Garlen', 'Gaulin',
                     'Gayleen', 'Gaylene', 'Giliane', 'Gillan', 'Gillian',
                     'Glen', 'Glenn', 'Glyn', 'Glynn', 'Gollin', 'Gorlin',
                     'Kalin', 'Karlan', 'Karleen', 'Karlen', 'Karlene',
                     'Karlin', 'Karlyn', 'Kaylyn', 'Keelin', 'Kellen',
                     'Kellene', 'Kellyann', 'Kellyn', 'Khalin', 'Kilan',
                     'Kilian', 'Killen', 'Killian', 'Killion', 'Klein',
                     'Kleon', 'Kline', 'Koerlin', 'Kylen', 'Kylynn', 'Quillan',
                     'Quillon', 'Qulllon', 'Xylon'):
            self.assertEqual(caverphone(word), 'KLN1111111')
            self.assertEqual(caverphone(word, 2), 'KLN1111111')
            self.assertEqual(caverphone(word, version=2), 'KLN1111111')
        for word in ('Dan', 'Dane', 'Dann', 'Darn', 'Daune', 'Dawn', 'Ddene',
                     'Dean', 'Deane', 'Deanne', 'DeeAnn', 'Deeann', 'Deeanne',
                     'Deeyn', 'Den', 'Dene', 'Denn', 'Deonne', 'Diahann',
                     'Dian', 'Diane', 'Diann', 'Dianne', 'Diannne', 'Dine',
                     'Dion', 'Dione', 'Dionne', 'Doane', 'Doehne', 'Don',
                     'Donn', 'Doone', 'Dorn', 'Down', 'Downe', 'Duane', 'Dun',
                     'Dunn', 'Duyne', 'Dyan', 'Dyane', 'Dyann', 'Dyanne',
                     'Dyun', 'Tan', 'Tann', 'Teahan', 'Ten', 'Tenn', 'Terhune',
                     'Thain', 'Thaine', 'Thane', 'Thanh', 'Thayne', 'Theone',
                     'Thin', 'Thorn', 'Thorne', 'Thun', 'Thynne', 'Tien',
                     'Tine', 'Tjon', 'Town', 'Towne', 'Turne', 'Tyne'):
            self.assertEqual(caverphone(word), 'TN11111111')
            self.assertEqual(caverphone(word, 2), 'TN11111111')
            self.assertEqual(caverphone(word, version=2), 'TN11111111')

        # etc. (for code coverage)
        self.assertEqual(caverphone('enough'), 'ANF1111111')
        self.assertEqual(caverphone('trough'), 'TRF1111111')
        self.assertEqual(caverphone('gnu'), 'NA11111111')

    def test_caverphone2_php_testset(self):
        """Test abydos.phonetic.caverphone (PHP version testset)."""
        # https://raw.githubusercontent.com/kiphughes/caverphone/master/unit_tests.php
        with open(TESTDIR + '/corpora/php_caverphone.csv') as php_testset:
            for php_line in php_testset:
                (word, caver) = php_line.strip().split(',')
                self.assertEqual(caverphone(word), caver)

    def test_caverphone1(self):
        """Test abydos.phonetic.caverphone (Caverphone 1)."""
        self.assertEqual(caverphone('', 1), '111111')
        self.assertEqual(caverphone('', version=1), '111111')

        # http://caversham.otago.ac.nz/files/working/ctp060902.pdf
        self.assertEqual(caverphone('David', version=1), 'TFT111')
        self.assertEqual(caverphone('Whittle', version=1), 'WTL111')

    def test_caversham(self):
        """Test using Caversham test set (SoundEx, Metaphone, & Caverphone)."""
        with open(TESTDIR + '/corpora/variantNames.csv') as cav_testset:
            next(cav_testset)
            for cav_line in cav_testset:
                (name1, soundex1, metaphone1, caverphone1,
                 name2, soundex2, metaphone2, caverphone2,
                 soundex_same, metaphone_same, caverphone_same) = \
                 cav_line.strip().split(',')

                self.assertEqual(soundex(name1), soundex1)
                self.assertEqual(soundex(name2), soundex2)
                if soundex_same == '1':
                    self.assertEqual(soundex(name1), soundex(name2))
                else:
                    self.assertNotEqual(soundex(name1), soundex(name2))

                self.assertEqual(metaphone(name1), metaphone1)
                self.assertEqual(metaphone(name2), metaphone2)
                if metaphone_same == '1':
                    self.assertEqual(metaphone(name1), metaphone(name2))
                else:
                    self.assertNotEqual(metaphone(name1), metaphone(name2))

                self.assertEqual(caverphone(name1), caverphone1)
                self.assertEqual(caverphone(name2), caverphone2)
                if caverphone_same == '1':
                    self.assertEqual(caverphone(name1), caverphone(name2))
                else:
                    self.assertNotEqual(caverphone(name1), caverphone(name2))


class AlphaSisTestCases(unittest.TestCase):
    """Test Alpha-SIS functions.

    test cases for abydos.phonetic.alpha_sis
    """

    def test_alpha_sis(self):
        """Test abydos.phonetic.alpha_sis."""
        self.assertEqual(alpha_sis('')[0], '00000000000000')

        self.assertEqual(alpha_sis('Rodgers')[0], '04740000000000')
        self.assertEqual(alpha_sis('Rogers')[0], '04740000000000')
        self.assertEqual(alpha_sis('Kant')[0], '07210000000000')
        self.assertEqual(alpha_sis('Knuth')[0], '02100000000000')
        self.assertEqual(alpha_sis('Harper')[0], '24940000000000')
        self.assertEqual(alpha_sis('Collier')[0], '07540000000000')
        self.assertEqual(alpha_sis('Schultz')[0], '06500000000000')
        self.assertEqual(alpha_sis('Livingston')[0], '05827012000000')

        # tests of repeated letters
        self.assertEqual(alpha_sis('Colllier')[0], '07554000000000')
        self.assertEqual(alpha_sis('Collllier')[0], '07554000000000')
        self.assertEqual(alpha_sis('Colllllier')[0], '07555400000000')
        self.assertEqual(alpha_sis('Collllllier')[0], '07555400000000')
        self.assertEqual(alpha_sis('Colalalier')[0], '07555400000000')

        # maxlength bounds tests
        self.assertEqual(alpha_sis('Niall', maxlength=float('inf'))[0],
                         '02500000000000000000000000000000000000000000000000' +
                         '00000000000000')
        self.assertEqual(alpha_sis('Niall', maxlength=None)[0],
                         '02500000000000000000000000000000000000000000000000' +
                         '00000000000000')
        self.assertEqual(alpha_sis('Niall', maxlength=0)[0], '0250')


class FuzzySoundexTestCases(unittest.TestCase):
    """Test Fuzzy Soundex functions.

    test cases for abydos.phonetic.fuzzy_soundex
    """

    def test_fuzzy_soundex(self):
        """Test abydos.phonetic.fuzzy_soundex."""
        self.assertEqual(fuzzy_soundex(''), '00000')
        # http://wayback.archive.org/web/20100629121128/http://www.ir.iit.edu/publications/downloads/IEEESoundexV5.pdf
        self.assertEqual(fuzzy_soundex('Kristen'), 'K6935')
        self.assertEqual(fuzzy_soundex('Krissy'), 'K6900')
        self.assertEqual(fuzzy_soundex('Christen'), 'K6935')

        # http://books.google.com/books?id=LZrT6eWf9NMC&lpg=PA76&ots=Tex3FqNwGP&dq=%22phonix%20algorithm%22&pg=PA75#v=onepage&q=%22phonix%20algorithm%22&f=false
        self.assertEqual(fuzzy_soundex('peter', 4), 'P360')
        self.assertEqual(fuzzy_soundex('pete', 4), 'P300')
        self.assertEqual(fuzzy_soundex('pedro', 4), 'P360')
        self.assertEqual(fuzzy_soundex('stephen', 4), 'S315')
        self.assertEqual(fuzzy_soundex('steve', 4), 'S310')
        self.assertEqual(fuzzy_soundex('smith', 4), 'S530')
        self.assertEqual(fuzzy_soundex('smythe', 4), 'S530')
        self.assertEqual(fuzzy_soundex('gail', 4), 'G400')
        self.assertEqual(fuzzy_soundex('gayle', 4), 'G400')
        self.assertEqual(fuzzy_soundex('christine', 4), 'K693')
        self.assertEqual(fuzzy_soundex('christina', 4), 'K693')
        self.assertEqual(fuzzy_soundex('kristina', 4), 'K693')

        # etc. (for code coverage)
        self.assertEqual(fuzzy_soundex('Wight'), 'W3000')
        self.assertEqual(fuzzy_soundex('Hardt'), 'H6000')
        self.assertEqual(fuzzy_soundex('Knight'), 'N3000')
        self.assertEqual(fuzzy_soundex('Czech'), 'S7000')
        self.assertEqual(fuzzy_soundex('Tsech'), 'S7000')
        self.assertEqual(fuzzy_soundex('gnomic'), 'N5900')
        self.assertEqual(fuzzy_soundex('Wright'), 'R3000')
        self.assertEqual(fuzzy_soundex('Hrothgar'), 'R3760')
        self.assertEqual(fuzzy_soundex('Hwaet'), 'W3000')
        self.assertEqual(fuzzy_soundex('Grant'), 'G6300')
        self.assertEqual(fuzzy_soundex('Hart'), 'H6000')
        self.assertEqual(fuzzy_soundex('Hardt'), 'H6000')

        # maxlength bounds tests
        self.assertEqual(fuzzy_soundex('Niall', maxlength=float('inf')),
                         'N4000000000000000000000000000000000000000000000000' +
                         '00000000000000')
        self.assertEqual(fuzzy_soundex('Niall', maxlength=None),
                         'N4000000000000000000000000000000000000000000000000' +
                         '00000000000000')
        self.assertEqual(fuzzy_soundex('Niall', maxlength=0), 'N400')

        # zero_pad tests
        self.assertEqual(fuzzy_soundex('Niall', maxlength=float('inf'),
                                       zero_pad=False), 'N4')
        self.assertEqual(fuzzy_soundex('Niall', maxlength=None,
                                       zero_pad=False), 'N4')
        self.assertEqual(fuzzy_soundex('Niall', maxlength=0,
                                       zero_pad=False), 'N4')
        self.assertEqual(fuzzy_soundex('Niall', maxlength=0,
                                       zero_pad=True), 'N400')
        self.assertEqual(fuzzy_soundex('', maxlength=4, zero_pad=False), '0')
        self.assertEqual(fuzzy_soundex('', maxlength=4, zero_pad=True), '0000')


class PhonexTestCases(unittest.TestCase):
    """Test Phonex functions.

    test cases for abydos.phonetic.phonex
    """

    def test_phonex(self):
        """Test abydos.phonetic.phonex."""
        self.assertEqual(phonex(''), '0000')

        # http://homepages.cs.ncl.ac.uk/brian.randell/Genealogy/NameMatching.pdf
        self.assertEqual(phonex('Ewell'), 'A400')
        self.assertEqual(phonex('Filp'), 'F100')
        self.assertEqual(phonex('Heames'), 'A500')
        self.assertEqual(phonex('Kneves'), 'N100')
        self.assertEqual(phonex('River'), 'R160')
        self.assertEqual(phonex('Corley'), 'C400')
        self.assertEqual(phonex('Carton'), 'C350')
        self.assertEqual(phonex('Cachpole'), 'C214')

        self.assertEqual(phonex('Ewell'), phonex('Ule'))
        self.assertEqual(phonex('Filp'), phonex('Philp'))
        self.assertEqual(phonex('Yule'), phonex('Ewell'))
        self.assertEqual(phonex('Heames'), phonex('Eames'))
        self.assertEqual(phonex('Kneves'), phonex('Neves'))
        self.assertEqual(phonex('River'), phonex('Rivers'))
        self.assertEqual(phonex('Corley'), phonex('Coley'))
        self.assertEqual(phonex('Carton'), phonex('Carlton'))
        self.assertEqual(phonex('Cachpole'), phonex('Catchpole'))

        # etc. (for code coverage)
        self.assertEqual(phonex('Saxon'), 'S250')
        self.assertEqual(phonex('Wright'), 'R230')
        self.assertEqual(phonex('Ai'), 'A000')
        self.assertEqual(phonex('Barth'), 'B300')
        self.assertEqual(phonex('Perry'), 'B600')
        self.assertEqual(phonex('Garth'), 'G300')
        self.assertEqual(phonex('Jerry'), 'G600')
        self.assertEqual(phonex('Gerry'), 'G600')
        self.assertEqual(phonex('Camden'), 'C500')
        self.assertEqual(phonex('Ganges'), 'G500')
        self.assertEqual(phonex('A-1'), 'A000')

        # maxlength bounds tests
        self.assertEqual(phonex('Niall', maxlength=float('inf')),
                         'N4000000000000000000000000000000000000000000000000' +
                         '00000000000000')
        self.assertEqual(phonex('Niall', maxlength=None),
                         'N4000000000000000000000000000000000000000000000000' +
                         '00000000000000')
        self.assertEqual(phonex('Niall', maxlength=0), 'N400')

        # zero_pad tests
        self.assertEqual(phonex('Niall', maxlength=float('inf'),
                                zero_pad=False), 'N4')
        self.assertEqual(phonex('Niall', maxlength=None, zero_pad=False),
                         'N4')
        self.assertEqual(phonex('Niall', maxlength=0, zero_pad=False),
                         'N4')
        self.assertEqual(phonex('Niall', maxlength=0, zero_pad=True),
                         'N400')
        self.assertEqual(phonex('', maxlength=4, zero_pad=False), '0')
        self.assertEqual(phonex('', maxlength=4, zero_pad=True), '0000')


class PhonemTestCases(unittest.TestCase):
    """Test Phonem functions.

    test cases for abydos.phonetic.phonem
    """

    def test_phonem(self):
        """Test abydos.phonetic.phonem."""
        self.assertEqual(phonem(''), '')

        # http://phonetik.phil-fak.uni-koeln.de/fileadmin/home/ritters/Allgemeine_Dateien/Martin_Wilz.pdf
        self.assertEqual(phonem('müller'), 'MYLR')
        self.assertEqual(phonem('schmidt'), 'CMYD')
        self.assertEqual(phonem('schneider'), 'CNAYDR')
        self.assertEqual(phonem('fischer'), 'VYCR')
        self.assertEqual(phonem('weber'), 'VBR')
        self.assertEqual(phonem('meyer'), 'MAYR')
        self.assertEqual(phonem('wagner'), 'VACNR')
        self.assertEqual(phonem('schulz'), 'CULC')
        self.assertEqual(phonem('becker'), 'BCR')
        self.assertEqual(phonem('hoffmann'), 'OVMAN')
        self.assertEqual(phonem('schäfer'), 'CVR')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/008_phonem.t
        self.assertEqual(phonem('mair'), 'MAYR')
        self.assertEqual(phonem('bäker'), 'BCR')
        self.assertEqual(phonem('schaeffer'), 'CVR')
        self.assertEqual(phonem('computer'), 'COMBUDR')
        self.assertEqual(phonem('pfeifer'), 'VAYVR')
        self.assertEqual(phonem('pfeiffer'), 'VAYVR')


class PhonixTestCases(unittest.TestCase):
    """Test Phonix functions.

    test cases for abydos.phonetic.phonix
    """

    def test_phonix(self):
        """Test abydos.phonetic.phonix."""
        self.assertEqual(phonix(''), '0000')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/007_phonix.t
        self.assertEqual(phonix('Müller'), 'M400')
        self.assertEqual(phonix('schneider'), 'S530')
        self.assertEqual(phonix('fischer'), 'F800')
        self.assertEqual(phonix('weber'), 'W100')
        self.assertEqual(phonix('meyer'), 'M000')
        self.assertEqual(phonix('wagner'), 'W250')
        self.assertEqual(phonix('schulz'), 'S480')
        self.assertEqual(phonix('becker'), 'B200')
        self.assertEqual(phonix('hoffmann'), 'H755')
        self.assertEqual(phonix('schäfer'), 'S700')
        self.assertEqual(phonix('schmidt'), 'S530')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/007_phonix.t:
        # testcases from Wais Module
        self.assertEqual(phonix('computer'), 'K513')
        self.assertEqual(phonix('computers'), 'K513')
        self.assertEqual(phonix('computers', 5), 'K5138')
        self.assertEqual(phonix('pfeifer'), 'F700')
        self.assertEqual(phonix('pfeiffer'), 'F700')
        self.assertEqual(phonix('knight'), 'N300')
        self.assertEqual(phonix('night'), 'N300')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/007_phonix.t:
        # testcases from
        # http://www.cl.uni-heidelberg.de/~bormann/documents/phono/
        # They use a sliglty different algorithm (first char is not included in
        # num code here)
        self.assertEqual(phonix('wait'), 'W300')
        self.assertEqual(phonix('weight'), 'W300')
        self.assertEqual(phonix('gnome'), 'N500')
        self.assertEqual(phonix('noam'), 'N500')
        self.assertEqual(phonix('rees'), 'R800')
        self.assertEqual(phonix('reece'), 'R800')
        self.assertEqual(phonix('yaeger'), 'v200')

        # http://books.google.com/books?id=xtWPI7Is9wIC&lpg=PA29&ots=DXhaL7ZkvK&dq=phonix%20gadd&pg=PA29#v=onepage&q=phonix%20gadd&f=false
        self.assertEqual(phonix('alam'), 'v450')
        self.assertEqual(phonix('berkpakaian'), 'B212')
        self.assertEqual(phonix('capaian'), 'K150')

        # http://books.google.com/books?id=LZrT6eWf9NMC&lpg=PA76&ots=Tex3FqNwGP&dq=%22phonix%20algorithm%22&pg=PA75#v=onepage&q=%22phonix%20algorithm%22&f=false
        self.assertEqual(phonix('peter'), 'P300')
        self.assertEqual(phonix('pete'), 'P300')
        self.assertEqual(phonix('pedro'), 'P360')
        self.assertEqual(phonix('stephen'), 'S375')
        self.assertEqual(phonix('steve'), 'S370')
        self.assertEqual(phonix('smith'), 'S530')
        self.assertEqual(phonix('smythe'), 'S530')
        self.assertEqual(phonix('gail'), 'G400')
        self.assertEqual(phonix('gayle'), 'G400')
        self.assertEqual(phonix('christine'), 'K683')
        self.assertEqual(phonix('christina'), 'K683')
        self.assertEqual(phonix('kristina'), 'K683')

        # maxlength bounds tests
        self.assertEqual(phonix('Niall', maxlength=float('inf')), 'N4'+'0'*62)
        self.assertEqual(phonix('Niall', maxlength=None), 'N4'+'0'*62)
        self.assertEqual(phonix('Niall', maxlength=0), 'N400')

        # zero_pad tests
        self.assertEqual(phonix('Niall', maxlength=float('inf'),
                                zero_pad=False), 'N4')
        self.assertEqual(phonix('Niall', maxlength=None, zero_pad=False),
                         'N4')
        self.assertEqual(phonix('Niall', maxlength=0, zero_pad=False),
                         'N4')
        self.assertEqual(phonix('Niall', maxlength=0, zero_pad=True),
                         'N400')
        self.assertEqual(phonix('', maxlength=4, zero_pad=False), '0')
        self.assertEqual(phonix('', maxlength=4, zero_pad=True), '0000')


class SfinxBisTestCases(unittest.TestCase):
    """Test SfinxBis functions.

    test cases for abydos.phonetic.sfinxbis
    """

    def test_sfinxbis(self):
        """Test abydos.phonetic.sfinxbis."""
        self.assertEqual(sfinxbis(''), ('',))

        # http://www.swami.se/download/18.248ad5af12aa81365338000106/TestSfinx.txt
        # cases where the gold standard gave clearly wrong values have been
        # corrected below (marked with '# wrong'
        self.assertEqual(sfinxbis('af Sandeberg'), ('S53162',))
        self.assertEqual(sfinxbis('av Ekenstam'), ('$25835',))
        self.assertEqual(sfinxbis('Da Costa'), ('K83',))
        self.assertEqual(sfinxbis('Das Neves'), ('D8', 'N78'))
        self.assertEqual(sfinxbis('de Besche'), ('B8',))
        self.assertEqual(sfinxbis('de la Motte'), ('M3',))
        self.assertEqual(sfinxbis('de Las Heras'), ('H68',))  # wrong
        self.assertEqual(sfinxbis('de Los Santos'), ('S538',))
        self.assertEqual(sfinxbis('del Rosario'), ('R862',))
        self.assertEqual(sfinxbis('Den Boer'), ('B6',))
        self.assertEqual(sfinxbis('Der de Kazinczy'),
                         ('D6', 'K8528',))  # wrong
        self.assertEqual(sfinxbis('des Rieux'), ('R28',))
        self.assertEqual(sfinxbis('Di Luca'), ('L2',))
        self.assertEqual(sfinxbis('Do Rosario'), ('R862',))
        self.assertEqual(sfinxbis('Don Lind'), ('L53',))
        self.assertEqual(sfinxbis('Dos Santos'), ('S538',))
        self.assertEqual(sfinxbis('du Rietz'), ('R38',))
        self.assertEqual(sfinxbis('in de Betou'), ('B3',))
        self.assertEqual(sfinxbis('La Fleur'), ('F46',))
        self.assertEqual(sfinxbis('Le Grand'), ('G653',))
        self.assertEqual(sfinxbis('li Puma'), ('L', 'P5'))
        self.assertEqual(sfinxbis('lo Martire'), ('L', 'M636'))
        self.assertEqual(sfinxbis('mac Donald'), ('D543',))
        self.assertEqual(sfinxbis('mc Intosh'), ('$538',))
        self.assertEqual(sfinxbis('S:t Cyr'), ('S6',))
        self.assertEqual(sfinxbis('Van Doom'), ('D5',))
        self.assertEqual(sfinxbis('Van de Peppel'), ('P14',))
        self.assertEqual(sfinxbis('Van den Berg'), ('B62',))
        self.assertEqual(sfinxbis('Van Der Kwast'), ('K783',))
        self.assertEqual(sfinxbis('von Ahn'), ('$5',))
        self.assertEqual(sfinxbis('von Dem Knesebeck'), ('K5812',))
        self.assertEqual(sfinxbis('von Der Burg'), ('B62',))
        self.assertEqual(sfinxbis('D\'Angelo'), ('D524',))
        self.assertEqual(sfinxbis('O\'Conner'), ('$256',))
        self.assertEqual(sfinxbis('Los'), ('L8',))
        self.assertEqual(sfinxbis('Mac'), ('M2',))
        self.assertEqual(sfinxbis('Till'), ('T4',))
        self.assertEqual(sfinxbis('Van'), ('V5',))
        self.assertEqual(sfinxbis('Von'), ('V5',))
        self.assertEqual(sfinxbis('Bernadotte af Wisborg'), ('B6533', 'V8162'))
        self.assertEqual(sfinxbis('Hjort af Ornäs'), ('J63', '$658'))
        self.assertEqual(sfinxbis('Horn af Åminne'), ('H65', '$55'))
        self.assertEqual(sfinxbis('Horn av Åminne'), ('H65', '$55'))
        self.assertEqual(sfinxbis('Hård af Segerstad'), ('H63', 'S26833'))
        self.assertEqual(sfinxbis('Hård av Segerstad'), ('H63', 'S26833'))
        self.assertEqual(sfinxbis('Stael von Holstein'), ('S34', 'H48325'))
        self.assertEqual(sfinxbis('de Oliveira e Silva'), ('$4726', 'S47'))
        self.assertEqual(sfinxbis('de Alfaro y Gómez'), ('$476', 'G58'))
        self.assertEqual(sfinxbis('Arjaliès-de la Lande'), ('$6248', 'L53'))
        self.assertEqual(sfinxbis('Dominicus van den Bussche'),
                         ('D5528', 'B8'))
        self.assertEqual(sfinxbis('Edebol Eeg-Olofsson'),
                         ('$314', '$2', '$4785'))
        self.assertEqual(sfinxbis('Jonsson-Blomqvist'), ('J585', 'B452783'))
        self.assertEqual(sfinxbis('Kiviniemi Birgersson'), ('#755', 'B62685'))
        self.assertEqual(sfinxbis('Massena Serpa dos Santos'),
                         ('M85', 'S61', 'S538'))
        self.assertEqual(sfinxbis('S:t Clair Renard'), ('K426', 'R563'))
        self.assertEqual(sfinxbis('Skoog H Andersson'), ('S22', 'H', '$53685'))
        self.assertEqual(sfinxbis('von Post-Skagegård'), ('P83', 'S22263'))
        self.assertEqual(sfinxbis('von Zur-Mühlen'), ('S6', 'M45'))
        self.assertEqual(sfinxbis('Waltå O:son'), ('V43', '$85'))
        self.assertEqual(sfinxbis('Zardán Gómez de la Torre'),
                         ('S635', 'G58', 'T6'))
        self.assertEqual(sfinxbis('af Jochnick'), ('J252',))
        self.assertEqual(sfinxbis('af Ioscnick'), ('J8252',))
        self.assertEqual(sfinxbis('Aabakken'), ('$125',))
        self.assertEqual(sfinxbis('Åbacken'), ('$125',))
        self.assertEqual(sfinxbis('Ahlen'), ('$45',))
        self.assertEqual(sfinxbis('Aleen'), ('$45',))
        self.assertEqual(sfinxbis('Braunerhielm'), ('B656245',))
        self.assertEqual(sfinxbis('Branneerhielm'), ('B656245',))
        self.assertEqual(sfinxbis('Carlzon'), ('K6485',))
        self.assertEqual(sfinxbis('Karlsson'), ('K6485',))
        self.assertEqual(sfinxbis('Enochsson'), ('$5285',))
        self.assertEqual(sfinxbis('Ericsson'), ('$6285',))
        self.assertEqual(sfinxbis('Ericksson'), ('$6285',))
        self.assertEqual(sfinxbis('Erixson'), ('$6285',))
        self.assertEqual(sfinxbis('Filipsson'), ('F4185',))
        self.assertEqual(sfinxbis('Philipson'), ('F4185',))
        self.assertEqual(sfinxbis('Flycht'), ('F423',))
        self.assertEqual(sfinxbis('Flygt'), ('F423',))
        self.assertEqual(sfinxbis('Flykt'), ('F423',))
        self.assertEqual(sfinxbis('Fröijer'), ('F626',))
        self.assertEqual(sfinxbis('Fröjer'), ('F626',))
        self.assertEqual(sfinxbis('Gertner'), ('J6356',))
        self.assertEqual(sfinxbis('Hiertner'), ('J6356',))
        self.assertEqual(sfinxbis('Hirch'), ('H62',))
        self.assertEqual(sfinxbis('Hirsch'), ('H68',))
        self.assertEqual(sfinxbis('Haegermarck'), ('H26562',))
        self.assertEqual(sfinxbis('Hägermark'), ('H26562',))
        self.assertEqual(sfinxbis('Isaxon'), ('$8285',))
        self.assertEqual(sfinxbis('Isacsson'), ('$8285',))
        self.assertEqual(sfinxbis('Joachimsson'), ('J2585',))
        self.assertEqual(sfinxbis('Joakimson'), ('J2585',))
        self.assertEqual(sfinxbis('Kjell'), ('#4',))
        self.assertEqual(sfinxbis('Käll'), ('#4',))
        self.assertEqual(sfinxbis('Knapp'), ('K51',))
        self.assertEqual(sfinxbis('Krans'), ('K658',))
        self.assertEqual(sfinxbis('Krantz'), ('K6538',))
        self.assertEqual(sfinxbis('Kvist'), ('K783',))
        self.assertEqual(sfinxbis('Quist'), ('K783',))
        self.assertEqual(sfinxbis('Lidbeck'), ('L312',))
        self.assertEqual(sfinxbis('Lidbäck'), ('L312',))
        self.assertEqual(sfinxbis('Linnér'), ('L56',))
        self.assertEqual(sfinxbis('Linner'), ('L56',))
        self.assertEqual(sfinxbis('Lorenzsonn'), ('L6585',))
        self.assertEqual(sfinxbis('Lorentzon'), ('L65385',))
        self.assertEqual(sfinxbis('Lorenßon'), ('L6585',))
        self.assertEqual(sfinxbis('Lyxell'), ('L284',))
        self.assertEqual(sfinxbis('Lycksell'), ('L284',))
        self.assertEqual(sfinxbis('Marcström'), ('M628365',))
        self.assertEqual(sfinxbis('Markström'), ('M628365',))
        self.assertEqual(sfinxbis('Michaelsson'), ('M2485',))
        self.assertEqual(sfinxbis('Mikaelson'), ('M2485',))
        self.assertEqual(sfinxbis('Mörch'), ('M62',))
        self.assertEqual(sfinxbis('Mörck'), ('M62',))
        self.assertEqual(sfinxbis('Mörk'), ('M62',))
        self.assertEqual(sfinxbis('Mørk'), ('M62',))
        self.assertEqual(sfinxbis('Nääs'), ('N8',))
        self.assertEqual(sfinxbis('Naess'), ('N8',))
        self.assertEqual(sfinxbis('Nordstedt'), ('N63833',))
        self.assertEqual(sfinxbis('Oxenstierna'), ('$28583265',))
        self.assertEqual(sfinxbis('Palmçrañtz'), ('P4526538',))
        self.assertEqual(sfinxbis('Palmcrantz'), ('P4526538',))
        self.assertEqual(sfinxbis('Palmkrantz'), ('P4526538',))
        self.assertEqual(sfinxbis('Preuss'), ('P68',))
        self.assertEqual(sfinxbis('Preutz'), ('P638',))
        self.assertEqual(sfinxbis('Richardson'), ('R26385',))
        self.assertEqual(sfinxbis('Rikardson'), ('R26385',))
        self.assertEqual(sfinxbis('Ruuth'), ('R3',))
        self.assertEqual(sfinxbis('Ruth'), ('R3',))
        self.assertEqual(sfinxbis('Sæter'), ('S36',))
        self.assertEqual(sfinxbis('Zäter'), ('S36',))
        self.assertEqual(sfinxbis('Schedin'), ('#35',))
        self.assertEqual(sfinxbis('Sjödin'), ('#35',))
        self.assertEqual(sfinxbis('Siöö'), ('#',))
        self.assertEqual(sfinxbis('Sjöh'), ('#',))
        self.assertEqual(sfinxbis('Svedberg'), ('S73162',))
        self.assertEqual(sfinxbis('Zwedberg'), ('S73162',))
        self.assertEqual(sfinxbis('Tjäder'), ('#36',))
        self.assertEqual(sfinxbis('þornquist'), ('T652783',))
        self.assertEqual(sfinxbis('Thörnqvist'), ('T652783',))
        self.assertEqual(sfinxbis('Törnkvist'), ('T652783',))
        self.assertEqual(sfinxbis('Wichman'), ('V255',))
        self.assertEqual(sfinxbis('Wickman'), ('V255',))
        self.assertEqual(sfinxbis('Wictorin'), ('V2365',))
        self.assertEqual(sfinxbis('Wictorsson'), ('V23685',))
        self.assertEqual(sfinxbis('Viktorson'), ('V23685',))
        self.assertEqual(sfinxbis('Zachrisson'), ('S2685',))
        self.assertEqual(sfinxbis('Zakrison'), ('S2685',))
        self.assertEqual(sfinxbis('Övragård'), ('$76263',))
        self.assertEqual(sfinxbis('Öfvragårdh'), ('$76263',))
        self.assertEqual(sfinxbis('Bogdanovic'), ('B23572',))
        self.assertEqual(sfinxbis('Bogdanovitch'), ('B235732',))
        self.assertEqual(sfinxbis('Dieterich'), ('D362',))
        self.assertEqual(sfinxbis('Eichorn'), ('$265',))
        self.assertEqual(sfinxbis('Friedrich'), ('F6362',))
        self.assertEqual(sfinxbis('Grantcharova'), ('G653267',))
        self.assertEqual(sfinxbis('Ilichev'), ('$427',))
        self.assertEqual(sfinxbis('Ivankovic'), ('$75272',))
        self.assertEqual(sfinxbis('Ivangurich'), ('$75262',))
        self.assertEqual(sfinxbis('Kinch'), ('#52',))
        self.assertEqual(sfinxbis('Kirchmann'), ('#6255',))
        self.assertEqual(sfinxbis('Machado'), ('M23',))
        self.assertEqual(sfinxbis('Reich'), ('R2',))
        self.assertEqual(sfinxbis('Roche'), ('R2',))
        self.assertEqual(sfinxbis('Rubaszkin'), ('R1825',))
        self.assertEqual(sfinxbis('Rubaschkin'), ('R1825',))
        self.assertEqual(sfinxbis('Sanchez'), ('S528',))
        self.assertEqual(sfinxbis('Walukiewicz'), ('V42728',))
        self.assertEqual(sfinxbis('Valukievitch'), ('V42732',))
        self.assertEqual(sfinxbis('K'), ('K',))
        self.assertEqual(sfinxbis('2010'), ('',))
        self.assertEqual(sfinxbis('cese'), ('S8',))

        # a few maxlength tests
        self.assertEqual(sfinxbis('Kiviniemi Birgersson', 3), ('#75', 'B62'))
        self.assertEqual(sfinxbis('Eichorn', 4), ('$265',))
        self.assertEqual(sfinxbis('Friedrich', 4), ('F636',))
        self.assertEqual(sfinxbis('Grantcharova', 4), ('G653',))
        self.assertEqual(sfinxbis('Ilichev', 4), ('$427',))
        self.assertEqual(sfinxbis('Ivankovic', 4), ('$752',))
        self.assertEqual(sfinxbis('Ivangurich', 4), ('$752',))
        self.assertEqual(sfinxbis('Kinch', 4), ('#52',))
        self.assertEqual(sfinxbis('Kirchmann', 4), ('#625',))
        self.assertEqual(sfinxbis('Machado', 4), ('M23',))
        self.assertEqual(sfinxbis('Reich', 4), ('R2',))
        self.assertEqual(sfinxbis('Roche', 4), ('R2',))
        self.assertEqual(sfinxbis('Rubaszkin', 4), ('R182',))
        self.assertEqual(sfinxbis('Rubaschkin', 4), ('R182',))
        self.assertEqual(sfinxbis('Sanchez', 4), ('S528',))
        self.assertEqual(sfinxbis('Walukiewicz', 4), ('V427',))
        self.assertEqual(sfinxbis('Valukievitch', 4), ('V427',))
        self.assertEqual(sfinxbis('K', 4), ('K',))
        self.assertEqual(sfinxbis('2010', 4), ('',))
        self.assertEqual(sfinxbis('cese', 4), ('S8',))

        # etc. (for code coverage)
        self.assertEqual(sfinxbis('chans'), ('#58',))
        self.assertEqual(sfinxbis('ljud'), ('J3',))
        self.assertEqual(sfinxbis('qi'), ('K',))
        self.assertEqual(sfinxbis('xavier'), ('S76',))
        self.assertEqual(sfinxbis('skjul'), ('#4',))
        self.assertEqual(sfinxbis('schul'), ('#4',))
        self.assertEqual(sfinxbis('skil'), ('#4',))

        # maxlength bounds tests
        self.assertEqual(sfinxbis('Niall', maxlength=float('inf')), ('N4',))
        self.assertEqual(sfinxbis('Niall', maxlength=None), ('N4',))
        self.assertEqual(sfinxbis('Niall', maxlength=0), ('N4',))


class PhonetTestCases(unittest.TestCase):
    """Test Phonet functions.

    test cases for abydos.phonetic.phonet
    """

    def test_phonet_german(self):
        """Test abydos.phonetic.phonet (German)."""
        self.assertEqual(phonet(''), '')
        self.assertEqual(phonet('', trace=True), '')

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

        self.assertEqual(phonet('', 2, trace=True), '')
        self.assertEqual(phonet('Zedlitz', 2, trace=True), 'ZETLIZ')
        self.assertEqual(phonet('Bremerhaven', 2, trace=True), 'BRENAFN')
        self.assertEqual(phonet('Schönberg', 2, trace=True), 'ZÖNBAK')
        self.assertEqual(phonet('Hamburger Hafen', 2, trace=True),
                         'ANBURKA AFN')
        self.assertEqual(phonet('Ziegler', 2, trace=True), 'ZIKLA')
        self.assertEqual(phonet('Scherer', 2, trace=True), 'ZERA')
        self.assertEqual(phonet('Jansen', 2, trace=True), 'IANZN')
        self.assertEqual(phonet('Eberhardt', 2, trace=True), 'EBART')
        self.assertEqual(phonet('Gottschalk', 2, trace=True), 'KUZALK')
        self.assertEqual(phonet('Brückmann', 2, trace=True), 'BRIKNAN')
        self.assertEqual(phonet('Blechschmidt', 2, trace=True), 'BLEKZNIT')
        self.assertEqual(phonet('Kolodziej', 2, trace=True), 'KULUTZI')
        self.assertEqual(phonet('Krauße', 2, trace=True), 'KRAUZE')

        # etc. (for code coverage)
        self.assertEqual(phonet('Jesper', 1, trace=True), 'IESPA')
        self.assertEqual(phonet('Glacéhandschuh', 1), 'GLAZANSHU')
        self.assertEqual(phonet('Blechschmidt', 1, trace=True), 'BLECHSHMIT')
        self.assertEqual(phonet('Burgdorf', 1), 'BURKDORF')
        self.assertEqual(phonet('Holzschuh', 1), 'HOLSHU')
        self.assertEqual(phonet('Aachen', 1, trace=True), 'ACHN')
        self.assertEqual(phonet('Abendspaziergang', 1), 'ABENTSPAZIRGANK')

    def test_phonet_nolang(self):
        """Test abydos.phonetic.phonet (no language)."""
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

        self.assertEqual(phonet('', 2, 'none', True), '')
        self.assertEqual(phonet('Zedlitz', 2, 'none', True), 'ZEDLITZ')
        self.assertEqual(phonet('Bremerhaven', 2, 'none', True), 'BREMERHAVEN')
        self.assertEqual(phonet('Schönberg', 2, 'none', True), 'SCHOENBERG')
        self.assertEqual(phonet('Brückmann', 2, 'none', True), 'BRUECKMAN')
        self.assertEqual(phonet('Krauße', 2, 'none', True), 'KRAUSE')

    def test_phonet_nachnamen(self):
        """Test abydos.phonetic.phonet (Nachnamen set)."""
        if not ALLOW_RANDOM:
            return
        with codecs.open(TESTDIR + '/corpora/nachnamen.csv',
                         encoding='utf-8') as nachnamen_testset:
            for nn_line in nachnamen_testset:
                if nn_line[0] != '#':
                    nn_line = nn_line.strip().split(',')
                    # This test set is very large (~10000 entries)
                    # so let's just randomly select about 100 for testing
                    if len(nn_line) >= 3 and one_in(100):
                        (term, ph1, ph2) = nn_line
                        self.assertEqual(phonet(term, 1), ph1)
                        self.assertEqual(phonet(term, 2), ph2)

    def test_phonet_ngerman(self):
        """Test abydos.phonetic.phonet (ngerman set)."""
        if not ALLOW_RANDOM:
            return
        with codecs.open(TESTDIR + '/corpora/ngerman.csv',
                         encoding='utf-8') as ngerman_testset:
            for ng_line in ngerman_testset:
                if ng_line[0] != '#':
                    ng_line = ng_line.strip().split(',')
                    # This test set is very large (~3000000 entries)
                    # so let's just randomly select about 30 for testing
                    if len(ng_line) >= 3 and one_in(10000):
                        (term, ph1, ph2) = ng_line
                        self.assertEqual(phonet(term, 1), ph1)
                        self.assertEqual(phonet(term, 2), ph2)


class SPFCTestCases(unittest.TestCase):
    """Test SPFC functions.

    test cases for abydos.phonetic.spfc
    """

    def test_spfc(self):
        """Test abydos.phonetic.spfc."""
        self.assertEqual(spfc(''), '')

        # https://archive.org/stream/accessingindivid00moor#page/19/mode/1up
        self.assertEqual(spfc(('J', 'KUHNS')), '16760')
        self.assertEqual(spfc(('G', 'ALTSHULER')), '35797')
        self.assertEqual(spfc('J KUHNS'), '16760')
        self.assertEqual(spfc('G ALTSHULER'), '35797')
        self.assertEqual(spfc('J. KUHNS'), '16760')
        self.assertEqual(spfc('G. ALTSHULER'), '35797')
        self.assertEqual(spfc('J. Kuhns'), '16760')
        self.assertEqual(spfc('G. Altshuler'), '35797')
        self.assertEqual(spfc('T. Vines'), '16760')
        self.assertEqual(spfc('J. Butler'), '35779')
        self.assertNotEqual(spfc('J. Kuhns'), spfc('J. Kuntz'))
        self.assertEqual(spfc('Jon Kuhns'), '16760')
        self.assertEqual(spfc('James Kuhns'), '16760')

        self.assertRaises(AttributeError, spfc, ('J', 'A', 'Kuhns'))
        self.assertRaises(AttributeError, spfc, 'JKuhns')
        self.assertRaises(AttributeError, spfc, 5)

        # etc. (for code coverage)
        self.assertEqual(spfc('James Goldstein'), '78795')
        self.assertEqual(spfc('James Hansen'), '58760')
        self.assertEqual(spfc('James Hester'), '59700')
        self.assertEqual(spfc('James Bardot'), '31745')
        self.assertEqual(spfc('James Windsor'), '29765')
        self.assertEqual(spfc('James Wenders'), '27760')
        self.assertEqual(spfc('James Ventor'), '17760')
        self.assertEqual(spfc('þ þ'), '00')


class StatisticsCanadaTestCases(unittest.TestCase):
    """Test Statistics Canada functions.

    test cases for abydos.phonetic.statistics_canada
    """

    def test_statistics_canada(self):
        """Test abydos.phonetic.statistics_canada."""
        self.assertEqual(statistics_canada(''), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        self.assertEqual(statistics_canada('Daves'), 'DVS')
        self.assertEqual(statistics_canada('Davies'), 'DVS')
        self.assertEqual(statistics_canada('Devese'), 'DVS')
        self.assertEqual(statistics_canada('Devies'), 'DVS')
        self.assertEqual(statistics_canada('Devos'), 'DVS')

        self.assertEqual(statistics_canada('Smathers'), 'SMTH')
        self.assertEqual(statistics_canada('Smithart'), 'SMTH')
        self.assertEqual(statistics_canada('Smithbower'), 'SMTH')
        self.assertEqual(statistics_canada('Smitherman'), 'SMTH')
        self.assertEqual(statistics_canada('Smithey'), 'SMTH')
        self.assertEqual(statistics_canada('Smithgall'), 'SMTH')
        self.assertEqual(statistics_canada('Smithingall'), 'SMTH')
        self.assertEqual(statistics_canada('Smithmyer'), 'SMTH')
        self.assertEqual(statistics_canada('Smithpeter'), 'SMTH')
        self.assertEqual(statistics_canada('Smithson'), 'SMTH')
        self.assertEqual(statistics_canada('Smithy'), 'SMTH')
        self.assertEqual(statistics_canada('Smotherman'), 'SMTH')
        self.assertEqual(statistics_canada('Smothers'), 'SMTH')
        self.assertEqual(statistics_canada('Smyth'), 'SMTH')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/statcan.js
        self.assertEqual(statistics_canada('Guillaume'), 'GLM')
        self.assertEqual(statistics_canada('Arlène'), 'ARLN')
        self.assertEqual(statistics_canada('Lüdenscheidt'), 'LDNS')


class LeinTestCases(unittest.TestCase):
    """Test Lein functions.

    test cases for abydos.phonetic.lein
    """

    def test_lein(self):
        """Test abydos.phonetic.lein."""
        self.assertEqual(lein(''), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        self.assertEqual(lein('Dubose'), 'D450')
        self.assertEqual(lein('Dubs'), 'D450')
        self.assertEqual(lein('Dubbs'), 'D450')
        self.assertEqual(lein('Doviak'), 'D450')
        self.assertEqual(lein('Dubke'), 'D450')
        self.assertEqual(lein('Dubus'), 'D450')
        self.assertEqual(lein('Dubois'), 'D450')
        self.assertEqual(lein('Duboise'), 'D450')
        self.assertEqual(lein('Doubek'), 'D450')
        self.assertEqual(lein('Defigh'), 'D450')
        self.assertEqual(lein('Defazio'), 'D450')
        self.assertEqual(lein('Debaca'), 'D450')
        self.assertEqual(lein('Dabbs'), 'D450')
        self.assertEqual(lein('Davies'), 'D450')
        self.assertEqual(lein('Dubukey'), 'D450')
        self.assertEqual(lein('Debus'), 'D450')
        self.assertEqual(lein('Debose'), 'D450')
        self.assertEqual(lein('Daves'), 'D450')
        self.assertEqual(lein('Dipiazza'), 'D450')
        self.assertEqual(lein('Dobbs'), 'D450')
        self.assertEqual(lein('Dobak'), 'D450')
        self.assertEqual(lein('Dobis'), 'D450')
        self.assertEqual(lein('Dobish'), 'D450')
        self.assertEqual(lein('Doepke'), 'D450')
        self.assertEqual(lein('Divish'), 'D450')
        self.assertEqual(lein('Dobosh'), 'D450')
        self.assertEqual(lein('Dupois'), 'D450')
        self.assertEqual(lein('Dufek'), 'D450')
        self.assertEqual(lein('Duffek'), 'D450')
        self.assertEqual(lein('Dupuis'), 'D450')
        self.assertEqual(lein('Dupas'), 'D450')
        self.assertEqual(lein('Devese'), 'D450')
        self.assertEqual(lein('Devos'), 'D450')
        self.assertEqual(lein('Deveaux'), 'D450')
        self.assertEqual(lein('Devies'), 'D450')

        self.assertEqual(lein('Sand'), 'S210')
        self.assertEqual(lein('Sandau'), 'S210')
        self.assertEqual(lein('Sande'), 'S210')
        self.assertEqual(lein('Sandia'), 'S210')
        self.assertEqual(lein('Sando'), 'S210')
        self.assertEqual(lein('Sandoe'), 'S210')
        self.assertEqual(lein('Sandy'), 'S210')
        self.assertEqual(lein('Santee'), 'S210')
        self.assertEqual(lein('Santi'), 'S210')
        self.assertEqual(lein('Santo'), 'S210')
        self.assertEqual(lein('Send'), 'S210')
        self.assertEqual(lein('Sennet'), 'S210')
        self.assertEqual(lein('Shemoit'), 'S210')
        self.assertEqual(lein('Shenot'), 'S210')
        self.assertEqual(lein('Shumate'), 'S210')
        self.assertEqual(lein('Simmet'), 'S210')
        self.assertEqual(lein('Simot'), 'S210')
        self.assertEqual(lein('Sineath'), 'S210')
        self.assertEqual(lein('Sinnott'), 'S210')
        self.assertEqual(lein('Sintay'), 'S210')
        self.assertEqual(lein('Smead'), 'S210')
        self.assertEqual(lein('Smeda'), 'S210')
        self.assertEqual(lein('Smit'), 'S210')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/lein.js
        self.assertEqual(lein('Guillaume'), 'G320')
        self.assertEqual(lein('Arlène'), 'A332')
        self.assertEqual(lein('Lüdenscheidt'), 'L125')


class RogerRootTestCases(unittest.TestCase):
    """Test Roger Root functions.

    test cases for abydos.phonetic.roger_root
    """

    def test_roger_root(self):
        """Test abydos.phonetic.roger_root."""
        self.assertEqual(roger_root(''), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        self.assertEqual(roger_root('BROWNER'), '09424')
        self.assertEqual(roger_root('STANLEY'), '00125')
        self.assertEqual(roger_root('CHALMAN'), '06532')
        self.assertEqual(roger_root('CHING'), '06270')
        self.assertEqual(roger_root('ANDERSON'), '12140')
        self.assertEqual(roger_root('OVERSTREET'), '18401')
        self.assertEqual(roger_root('HECKEL'), '27500')
        self.assertEqual(roger_root('WYSZYNSKI'), '40207')
        self.assertEqual(roger_root('WHITTED'), '41100')
        self.assertEqual(roger_root('ONGOQO'), '12770')  # PDF had a typo?
        self.assertEqual(roger_root('JOHNSON'), '32020')
        self.assertEqual(roger_root('WILLIAMS'), '45300')
        self.assertEqual(roger_root('SMITH'), '00310')
        self.assertEqual(roger_root('JONES'), '32000')
        self.assertEqual(roger_root('BROWN'), '09420')
        self.assertEqual(roger_root('DAVIS'), '01800')
        self.assertEqual(roger_root('JACKSON'), '37020')
        self.assertEqual(roger_root('WILSON'), '45020')
        self.assertEqual(roger_root('LEE'), '05000')
        self.assertEqual(roger_root('THOMAS'), '01300')

        self.assertEqual(roger_root('Defouw'), '01800')
        self.assertEqual(roger_root('Dauphi'), '01800')
        self.assertEqual(roger_root('Defazio'), '01800')
        self.assertEqual(roger_root('Defay'), '01800')
        self.assertEqual(roger_root('Davy'), '01800')
        self.assertEqual(roger_root('Defee'), '01800')
        self.assertEqual(roger_root('Dayhoff'), '01800')
        self.assertEqual(roger_root('Davie'), '01800')
        self.assertEqual(roger_root('Davey'), '01800')
        self.assertEqual(roger_root('Davies'), '01800')
        self.assertEqual(roger_root('Daves'), '01800')
        self.assertEqual(roger_root('Deife'), '01800')
        self.assertEqual(roger_root('Dehoff'), '01800')
        self.assertEqual(roger_root('Devese'), '01800')
        self.assertEqual(roger_root('Devoe'), '01800')
        self.assertEqual(roger_root('Devee'), '01800')
        self.assertEqual(roger_root('Devies'), '01800')
        self.assertEqual(roger_root('Devos'), '01800')
        self.assertEqual(roger_root('Dafoe'), '01800')
        self.assertEqual(roger_root('Dove'), '01800')
        self.assertEqual(roger_root('Duff'), '01800')
        self.assertEqual(roger_root('Duffey'), '01800')
        self.assertEqual(roger_root('Duffie'), '01800')
        self.assertEqual(roger_root('Duffy'), '01800')
        self.assertEqual(roger_root('Duyava'), '01800')
        self.assertEqual(roger_root('Tafoya'), '01800')
        self.assertEqual(roger_root('Tevis'), '01800')
        self.assertEqual(roger_root('Tiffee'), '01800')
        self.assertEqual(roger_root('Tivis'), '01800')
        self.assertEqual(roger_root('Thevis'), '01800')
        self.assertEqual(roger_root('Tovey'), '01800')
        self.assertEqual(roger_root('Toeves'), '01800')
        self.assertEqual(roger_root('Tuffs'), '01800')

        self.assertEqual(roger_root('Samotid'), '00311')
        self.assertEqual(roger_root('Simmet'), '00310')
        self.assertEqual(roger_root('Simot'), '00310')
        self.assertEqual(roger_root('Smead'), '00310')
        self.assertEqual(roger_root('Smeda'), '00310')
        self.assertEqual(roger_root('Smit'), '00310')
        self.assertEqual(roger_root('Smite'), '00310')
        self.assertEqual(roger_root('Smithe'), '00310')
        self.assertEqual(roger_root('Smithey'), '00310')
        self.assertEqual(roger_root('Smithson'), '00310')
        self.assertEqual(roger_root('Smithy'), '00310')
        self.assertEqual(roger_root('Smoot'), '00310')
        self.assertEqual(roger_root('Smyth'), '00310')
        self.assertEqual(roger_root('Szmodis'), '00310')
        self.assertEqual(roger_root('Zemaitis'), '00310')
        self.assertEqual(roger_root('Zmuda'), '00310')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/roger-root.js
        self.assertEqual(roger_root('Guillaume'), '07530')
        self.assertEqual(roger_root('Arlène'), '14520')
        self.assertEqual(roger_root('Lüdenscheidt'), '05126')


class ONCATestCases(unittest.TestCase):
    """Test ONCA functions.

    test cases for abydos.phonetic.onca
    """

    def test_onca(self):
        """Test abydos.phonetic.onca."""
        # https://nces.ed.gov/FCSM/pdf/RLT97.pdf
        self.assertEqual(onca('HALL'), 'H400')
        self.assertEqual(onca('SMITH'), 'S530')

        # http://nchod.uhce.ox.ac.uk/NCHOD%20Oxford%20E5%20Report%201st%20Feb_VerAM2.pdf
        self.assertEqual(onca('HAWTON'), 'H350')
        self.assertEqual(onca('HORTON'), 'H635')
        self.assertEqual(onca('HOUGHTON'), 'H235')


class BeiderMorseTestCases(unittest.TestCase):
    """Test BMPM functions.

    test cases for abydos.phonetic.bmpm and abydos.bm.*
    """

    def test_bmpm(self):
        """Test abydos.phonetic.bmpm.

        Most test cases from:
        http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/bm/

        As a rule, the test cases are copied from the above code, but the
        resultant values are not. This is largely because this Python port
        follows the PHP reference implementation much more closely than the
        Java port in Apache Commons Codec does. As a result, these tests have
        been conformed to the output produced by the PHP implementation,
        particularly in terms of formatting and ordering.
        """
        # base cases
        self.assertEqual(bmpm(''), '')

        for langs in ('', 1, 'spanish', 'english,italian', 3):
            for name_mode in ('gen', 'ash', 'sep'):
                for match_mode in ('approx', 'exact'):
                    for concat in (False, True):
                        if (isinstance(langs, text_type) and
                            ((name_mode == 'ash' and 'italian' in langs) or
                             (name_mode == 'sep' and 'english' in langs))):
                            self.assertRaises(ValueError, bmpm, '', langs,
                                              name_mode, match_mode, concat)
                        else:
                            self.assertEqual(bmpm('', langs, name_mode,
                                                  match_mode, concat), '')

        # testSolrGENERIC
        # concat is true, ruleType is EXACT
        self.assertEqual(bmpm('Angelo', '', 'gen', 'exact', True),
                         'angelo anxelo anhelo anjelo anZelo andZelo')
        self.assertEqual(bmpm('D\'Angelo', '', 'gen', 'exact', True),
                         'angelo anxelo anhelo anjelo anZelo andZelo dangelo' +
                         ' danxelo danhelo danjelo danZelo dandZelo')
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'gen',
                              'exact', True),
                         'angelo anxelo andZelo')
        self.assertEqual(bmpm('1234', '', 'gen', 'exact', True), '')

        # concat is false, ruleType is EXACT
        self.assertEqual(bmpm('Angelo', '', 'gen', 'exact', False),
                         'angelo anxelo anhelo anjelo anZelo andZelo')
        self.assertEqual(bmpm('D\'Angelo', '', 'gen', 'exact', False),
                         'angelo anxelo anhelo anjelo anZelo andZelo dangelo' +
                         ' danxelo danhelo danjelo danZelo dandZelo')
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'gen',
                              'exact', False),
                         'angelo anxelo andZelo')
        self.assertEqual(bmpm('1234', '', 'gen', 'exact', False), '')

        # concat is true, ruleType is APPROX
        self.assertEqual(bmpm('Angelo', '', 'gen', 'approx', True),
                         'angilo angYlo agilo ongilo ongYlo ogilo Yngilo' +
                         ' YngYlo anxilo onxilo anilo onilo aniilo oniilo' +
                         ' anzilo onzilo')
        self.assertEqual(bmpm('D\'Angelo', '', 'gen', 'approx', True),
                         'angilo angYlo agilo ongilo ongYlo ogilo Yngilo' +
                         ' YngYlo anxilo onxilo anilo onilo aniilo oniilo' +
                         ' anzilo onzilo dangilo dangYlo dagilo dongilo' +
                         ' dongYlo dogilo dYngilo dYngYlo danxilo donxilo' +
                         ' danilo donilo daniilo doniilo danzilo donzilo')
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'gen',
                              'approx', True),
                         'angilo ongilo anxilo onxilo anzilo onzilo')
        self.assertEqual(bmpm('1234', '', 'gen', 'approx', True), '')

        # concat is false, ruleType is APPROX
        self.assertEqual(bmpm('Angelo', '', 'gen', 'approx', False),
                         'angilo angYlo agilo ongilo ongYlo ogilo Yngilo' +
                         ' YngYlo anxilo onxilo anilo onilo aniilo oniilo' +
                         ' anzilo onzilo')
        self.assertEqual(bmpm('D\'Angelo', '', 'gen', 'approx', False),
                         'angilo angYlo agilo ongilo ongYlo ogilo Yngilo' +
                         ' YngYlo anxilo onxilo anilo onilo aniilo oniilo' +
                         ' anzilo onzilo dangilo dangYlo dagilo dongilo' +
                         ' dongYlo dogilo dYngilo dYngYlo danxilo donxilo' +
                         ' danilo donilo daniilo doniilo danzilo donzilo')
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'gen',
                              'approx', False),
                         'angilo ongilo anxilo onxilo anzilo onzilo')
        self.assertEqual(bmpm('1234', '', 'gen', 'approx', False), '')

        # testSolrASHKENAZI
        # concat is true, ruleType is EXACT
        self.assertEqual(bmpm('Angelo', '', 'ash', 'exact', True),
                         'angelo andZelo anhelo anxelo')
        self.assertEqual(bmpm('D\'Angelo', '', 'ash', 'exact', True),
                         'dangelo dandZelo danhelo danxelo')
        self.assertRaises(ValueError, bmpm, 'Angelo', 'italian,greek,spanish',
                          'ash', 'exact', True)
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'ash',
                              'exact', True, True), 'anxelo angelo')
        self.assertEqual(bmpm('1234', '', 'ash', 'exact', True), '')

        # concat is false, ruleType is EXACT
        self.assertEqual(bmpm('Angelo', '', 'ash', 'exact', False),
                         'angelo andZelo anhelo anxelo')
        self.assertEqual(bmpm('D\'Angelo', '', 'ash', 'exact', False),
                         'dangelo dandZelo danhelo danxelo')
        self.assertRaises(ValueError, bmpm, 'Angelo', 'italian,greek,spanish',
                          'ash', 'exact', False)
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'ash',
                              'exact', False, True), 'anxelo angelo')
        self.assertEqual(bmpm('1234', '', 'ash', 'exact', False), '')

        # concat is true, ruleType is APPROX
        self.assertEqual(bmpm('Angelo', '', 'ash', 'approx', True),
                         'angilo angYlo ongilo ongYlo Yngilo YngYlo anzilo' +
                         ' onzilo anilo onilo anxilo onxilo')
        self.assertEqual(bmpm('D\'Angelo', '', 'ash', 'approx', True),
                         'dangilo dangYlo dongilo dongYlo dYngilo dYngYlo' +
                         ' danzilo donzilo danilo donilo danxilo donxilo')
        self.assertRaises(ValueError, bmpm, 'Angelo', 'italian,greek,spanish',
                          'ash', 'approx', True)
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'ash',
                              'approx', True, True),
                         'anxYlo anxilo onxYlo onxilo angYlo angilo ongYlo' +
                         ' ongilo')
        self.assertEqual(bmpm('1234', '', 'ash', 'approx', True), '')

        # concat is false, ruleType is APPROX
        self.assertEqual(bmpm('Angelo', '', 'ash', 'approx', False),
                         'angilo angYlo ongilo ongYlo Yngilo YngYlo anzilo' +
                         ' onzilo anilo onilo anxilo onxilo')
        self.assertEqual(bmpm('D\'Angelo', '', 'ash', 'approx', False),
                         'dangilo dangYlo dongilo dongYlo dYngilo dYngYlo' +
                         ' danzilo donzilo danilo donilo danxilo donxilo')
        self.assertRaises(ValueError, bmpm, 'Angelo', 'italian,greek,spanish',
                          'ash', 'approx', False)
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'ash',
                              'approx', False, True),
                         'anxYlo anxilo onxYlo onxilo angYlo angilo ongYlo' +
                         ' ongilo')
        self.assertEqual(bmpm('1234', '', 'ash', 'approx', False), '')

        # testSolrSEPHARDIC
        # concat is true, ruleType is EXACT
        self.assertEqual(bmpm('Angelo', '', 'sep', 'exact', True),
                         'anZelo andZelo anxelo')
        self.assertEqual(bmpm('D\'Angelo', '', 'sep', 'exact', True),
                         'anZelo andZelo anxelo')
        self.assertRaises(ValueError, bmpm, 'Angelo', 'italian,greek,spanish',
                          'sep', 'exact', True)
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'sep',
                              'exact', True, True),
                         'andZelo anxelo')
        self.assertEqual(bmpm('1234', '', 'sep', 'exact', True), '')

        # concat is false, ruleType is EXACT
        self.assertEqual(bmpm('Angelo', '', 'sep', 'exact', False),
                         'anZelo andZelo anxelo')
        self.assertEqual(bmpm('D\'Angelo', '', 'sep', 'exact', False),
                         'anZelo andZelo anxelo')
        self.assertRaises(ValueError, bmpm, 'Angelo', 'italian,greek,spanish',
                          'sep', 'exact', False)
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'sep',
                              'exact', False, True), 'andZelo anxelo')
        self.assertEqual(bmpm('1234', '', 'sep', 'exact', False), '')

        # concat is true, ruleType is APPROX
        self.assertEqual(bmpm('Angelo', '', 'sep', 'approx', True),
                         'anzila anzilu nzila nzilu anhila anhilu nhila nhilu')
        self.assertEqual(bmpm('D\'Angelo', '', 'sep', 'approx', True),
                         'anzila anzilu nzila nzilu anhila anhilu nhila nhilu')
        self.assertRaises(ValueError, bmpm, 'Angelo', 'italian,greek,spanish',
                          'sep', 'approx', True)
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'sep',
                              'approx', True, True),
                         'anzila anzilu nzila nzilu anhila anhilu nhila nhilu')
        self.assertEqual(bmpm('1234', '', 'sep', 'approx', True), '')

        # concat is false, ruleType is APPROX
        self.assertEqual(bmpm('Angelo', '', 'sep', 'approx', False),
                         'anzila anzilu nzila nzilu anhila anhilu nhila nhilu')
        self.assertEqual(bmpm('D\'Angelo', '', 'sep', 'approx', False),
                         'anzila anzilu nzila nzilu anhila anhilu nhila nhilu')
        self.assertRaises(ValueError, bmpm, 'Angelo', 'italian,greek,spanish',
                          'sep', 'approx', False)
        self.assertEqual(bmpm('Angelo', 'italian,greek,spanish', 'sep',
                              'approx', False, True),
                         'anzila anzilu nzila nzilu anhila anhilu nhila nhilu')
        self.assertEqual(bmpm('1234', '', 'sep', 'approx', False), '')

        # testCompatibilityWithOriginalVersion
        self.assertEqual(bmpm('abram', '', 'gen', 'approx', False),
                         'abram abrom avram avrom obram obrom ovram ovrom' +
                         ' Ybram Ybrom abran abron obran obron')
        self.assertEqual(bmpm('Bendzin', '', 'gen', 'approx', False),
                         'binzn bindzn vindzn bintsn vintsn')
        self.assertEqual(bmpm('abram', '', 'ash', 'approx', False),
                         'abram abrom avram avrom obram obrom ovram ovrom' +
                         ' Ybram Ybrom ombram ombrom imbram imbrom')
        self.assertEqual(bmpm('Halpern', '', 'ash', 'approx', False),
                         'alpirn alpYrn olpirn olpYrn Ylpirn YlpYrn xalpirn' +
                         ' xolpirn')

        # PhoneticEngineTest
        self.assertEqual(bmpm('Renault', '', 'gen', 'approx', True),
                         'rinolt rino rinDlt rinalt rinult rinD rina rinu')
        self.assertEqual(bmpm('Renault', '', 'ash', 'approx', True),
                         'rinDlt rinalt rinult rYnDlt rYnalt rYnult rinolt')
        self.assertEqual(bmpm('Renault', '', 'sep', 'approx', True),
                         'rinDlt')
        self.assertEqual(bmpm('SntJohn-Smith', '', 'gen', 'exact', True),
                         'sntjonsmit')
        self.assertEqual(bmpm('d\'ortley', '', 'gen', 'exact', True),
                         'ortlaj ortlej dortlaj dortlej')
        self.assertEqual(bmpm('van helsing', '', 'gen', 'exact', False),
                         'helSink helsink helzink xelsink elSink elsink' +
                         ' vanhelsink vanhelzink vanjelsink fanhelsink' +
                         ' fanhelzink banhelsink')

    def test_bmpm_misc(self):
        """Test abydos.phonetic.bmpm (miscellaneous tests).

        The purpose of this test set is to achieve higher code coverage
        and to hit some of the test cases noted in the BMPM reference code.
        """
        # test of Ashkenazi with discardable prefix
        self.assertEqual(bmpm('bar Hayim', name_mode='ash'), 'Dm xDm')

        # tests of concat behavior
        self.assertEqual(bmpm('Rodham Clinton', concat=False),
                         'rodam rodom rYdam rYdom rodan rodon rodxam rodxom' +
                         ' rodxan rodxon rudam rudom klinton klnton klintun' +
                         ' klntun tzlinton tzlnton tzlintun tzlntun zlinton' +
                         ' zlnton')
        self.assertEqual(bmpm('Rodham Clinton', concat=True),
                         'rodamklinton rodomklinton rodamklnton rodomklnton' +
                         ' rodamklintun rodomklintun rodamklntun rodomklntun' +
                         ' rodamtzlinton rodomtzlinton rodamtzlnton' +
                         ' rodomtzlnton rodamtzlintun rodomtzlintun' +
                         ' rodamtzlntun rodomtzlntun rodamzlinton' +
                         ' rodomzlinton rodamzlnton rodomzlnton rodanklinton' +
                         ' rodonklinton rodanklnton rodonklnton' +
                         ' rodxamklinton rodxomklinton rodxamklnton' +
                         ' rodxomklnton rodxanklinton rodxonklinton' +
                         ' rodxanklnton rodxonklnton rudamklinton' +
                         ' rudomklinton rudamklnton rudomklnton rudamklintun' +
                         ' rudomklintun rudamklntun rudomklntun' +
                         ' rudamtzlinton rudomtzlinton rudamtzlnton' +
                         ' rudomtzlnton rudamtzlintun rudomtzlintun' +
                         ' rudamtzlntun rudomtzlntun')

        # tests of name_mode values
        self.assertEqual(bmpm('bar Hayim', name_mode='ash'), 'Dm xDm')
        self.assertEqual(bmpm('bar Hayim', name_mode='ashkenazi'), 'Dm xDm')
        self.assertEqual(bmpm('bar Hayim', name_mode='Ashkenazi'), 'Dm xDm')
        self.assertEqual(bmpm('bar Hayim', name_mode='gen', concat=True),
                         'barDm borDm bYrDm varDm vorDm barDn borDn barxDm' +
                         ' borxDm varxDm vorxDm barxDn borxDn')
        self.assertEqual(bmpm('bar Hayim', name_mode='general', concat=True),
                         'barDm borDm bYrDm varDm vorDm barDn borDn barxDm' +
                         ' borxDm varxDm vorxDm barxDn borxDn')
        self.assertEqual(bmpm('bar Hayim', name_mode='Mizrahi', concat=True),
                         'barDm borDm bYrDm varDm vorDm barDn borDn barxDm' +
                         ' borxDm varxDm vorxDm barxDn borxDn')
        self.assertEqual(bmpm('bar Hayim', name_mode='mizrahi', concat=True),
                         'barDm borDm bYrDm varDm vorDm barDn borDn barxDm' +
                         ' borxDm varxDm vorxDm barxDn borxDn')
        self.assertEqual(bmpm('bar Hayim', name_mode='miz', concat=True),
                         'barDm borDm bYrDm varDm vorDm barDn borDn barxDm' +
                         ' borxDm varxDm vorxDm barxDn borxDn')

        # test that out-of-range langauge_arg results in L_ANY
        self.assertEqual(bmpm('Rodham Clinton', language_arg=2**32),
                         'rodam rodom rYdam rYdom rodan rodon rodxam rodxom' +
                         ' rodxan rodxon rudam rudom klinton klnton klintun' +
                         ' klntun tzlinton tzlnton tzlintun tzlntun zlinton' +
                         ' zlnton')
        self.assertEqual(bmpm('Rodham Clinton', language_arg=-4),
                         'rodam rodom rYdam rYdom rodan rodon rodxam rodxom' +
                         ' rodxan rodxon rudam rudom klinton klnton klintun' +
                         ' klntun tzlinton tzlnton tzlintun tzlntun zlinton' +
                         ' zlnton')

        # etc. (for code coverage)
        self.assertEqual(bmpm('van Damme', name_mode='sep'), 'dami mi dam m')

    def test_bmpm_nachnamen(self):
        """Test abydos.phonetic.bmpm (Nachnamen set)."""
        if not ALLOW_RANDOM:
            return
        with codecs.open(TESTDIR + '/corpora/nachnamen.bm.csv',
                         encoding='utf-8') as nachnamen_testset:
            next(nachnamen_testset)
            for nn_line in nachnamen_testset:
                nn_line = nn_line.strip().split(',')
                # This test set is very large (~10000 entries)
                # so let's just randomly select about 20 for testing
                if nn_line[0] != '#' and one_in(500):
                    self.assertEqual(bmpm(nn_line[0], language_arg='german'),
                                     nn_line[1])
                    self.assertEqual(bmpm(nn_line[0]), nn_line[2])

    def test_bmpm_nachnamen_cc(self):
        """Test abydos.phonetic.bmpm (Nachnamen set, corner cases)."""
        with codecs.open(TESTDIR + '/corpora/nachnamen.bm.cc.csv',
                         encoding='utf-8') as nachnamen_testset:
            next(nachnamen_testset)
            for nn_line in nachnamen_testset:
                nn_line = nn_line.strip().split(',')
                # This test set is very large (~10000 entries)
                # so let's just randomly select about 20 for testing
                if nn_line[0] != '#':
                    self.assertEqual(bmpm(nn_line[0], language_arg='german'),
                                     nn_line[1])
                    self.assertEqual(bmpm(nn_line[0]), nn_line[2])

    def test_bmpm_uscensus2000(self):
        """Test abydos.phonetic.bmpm (US Census 2000 set)."""
        if not ALLOW_RANDOM:
            return
        with open(TESTDIR + '/corpora/uscensus2000.bm.csv') as uscensus_ts:
            next(uscensus_ts)
            for cen_line in uscensus_ts:
                cen_line = cen_line.strip().split(',')
                # This test set is very large (~150000 entries)
                # so let's just randomly select about 20 for testing
                if cen_line[0] != '#' and one_in(7500):
                    self.assertEqual(bmpm(cen_line[0], match_mode='approx',
                                          name_mode='gen'), cen_line[1])
                    self.assertEqual(bmpm(cen_line[0], match_mode='approx',
                                          name_mode='ash'), cen_line[2])
                    self.assertEqual(bmpm(cen_line[0], match_mode='approx',
                                          name_mode='sep'), cen_line[3])
                    self.assertEqual(bmpm(cen_line[0], match_mode='exact',
                                          name_mode='gen'), cen_line[4])
                    self.assertEqual(bmpm(cen_line[0], match_mode='exact',
                                          name_mode='ash'), cen_line[5])
                    self.assertEqual(bmpm(cen_line[0], match_mode='exact',
                                          name_mode='sep'), cen_line[6])

    def test_bmpm_uscensus2000_cc(self):
        """Test abydos.phonetic.bmpm (US Census 2000 set, corner cases)."""
        with open(TESTDIR + '/corpora/uscensus2000.bm.cc.csv') as uscensus_ts:
            next(uscensus_ts)
            for cen_line in uscensus_ts:
                cen_line = cen_line.strip().split(',')
                # This test set is very large (~150000 entries)
                # so let's just randomly select about 20 for testing
                if cen_line[0] != '#' and one_in(10):
                    self.assertEqual(bmpm(cen_line[0], match_mode='approx',
                                          name_mode='gen'), cen_line[1])
                    self.assertEqual(bmpm(cen_line[0], match_mode='approx',
                                          name_mode='ash'), cen_line[2])
                    self.assertEqual(bmpm(cen_line[0], match_mode='approx',
                                          name_mode='sep'), cen_line[3])
                    self.assertEqual(bmpm(cen_line[0], match_mode='exact',
                                          name_mode='gen'), cen_line[4])
                    self.assertEqual(bmpm(cen_line[0], match_mode='exact',
                                          name_mode='ash'), cen_line[5])
                    self.assertEqual(bmpm(cen_line[0], match_mode='exact',
                                          name_mode='sep'), cen_line[6])

    def test_bm_phonetic_number(self):
        """Test abydos.bm._bm_phonetic_number."""
        self.assertEqual(_bm_phonetic_number(''), '')
        self.assertEqual(_bm_phonetic_number('abcd'), 'abcd')
        self.assertEqual(_bm_phonetic_number('abcd[123]'), 'abcd')
        self.assertEqual(_bm_phonetic_number('abcd[123'), 'abcd')
        self.assertEqual(_bm_phonetic_number('abcd['), 'abcd')
        self.assertEqual(_bm_phonetic_number('abcd[[[123]]]'), 'abcd')

    def test_bm_apply_rule_if_compat(self):
        """Test abydos.bm._bm_apply_rule_if_compat."""
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def', 4), 'abcdef')
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def[6]', 4),
                         'abcdef[4]')
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def[4]', 4),
                         'abcdef[4]')
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def[0]', 4), None)
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def[8]', 4), None)
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def', 1), 'abcdef')
        self.assertEqual(_bm_apply_rule_if_compat('abc', 'def[4]', 1),
                         'abcdef[4]')

    def test_bm_language(self):
        """Test abydos.bm._bm_language.

        Most test cases from:
        http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/bm/LanguageGuessingTest.java?view=markup
        """
        self.assertEqual(_bm_language('Renault', 'gen'), L_FRENCH)
        self.assertEqual(_bm_language('Mickiewicz', 'gen'), L_POLISH)
        self.assertEqual(_bm_language('Thompson', 'gen') & L_ENGLISH,
                         L_ENGLISH)
        self.assertEqual(_bm_language('Nuñez', 'gen'), L_SPANISH)
        self.assertEqual(_bm_language('Carvalho', 'gen'), L_PORTUGUESE)
        self.assertEqual(_bm_language('Čapek', 'gen'), L_CZECH | L_LATVIAN)
        self.assertEqual(_bm_language('Sjneijder', 'gen'), L_DUTCH)
        self.assertEqual(_bm_language('Klausewitz', 'gen'), L_GERMAN)
        self.assertEqual(_bm_language('Küçük', 'gen'), L_TURKISH)
        self.assertEqual(_bm_language('Giacometti', 'gen'), L_ITALIAN)
        self.assertEqual(_bm_language('Nagy', 'gen'), L_HUNGARIAN)
        self.assertEqual(_bm_language('Ceauşescu', 'gen'), L_ROMANIAN)
        self.assertEqual(_bm_language('Angelopoulos', 'gen'), L_GREEKLATIN)
        self.assertEqual(_bm_language('Αγγελόπουλος', 'gen'), L_GREEK)
        self.assertEqual(_bm_language('Пушкин', 'gen'), L_CYRILLIC)
        self.assertEqual(_bm_language('כהן', 'gen'), L_HEBREW)
        self.assertEqual(_bm_language('ácz', 'gen'), L_ANY)
        self.assertEqual(_bm_language('átz', 'gen'), L_ANY)

    def test_bm_expand_alternates(self):
        """Test abydos.bm._bm_expand_alternates."""
        self.assertEqual(_bm_expand_alternates(''), '')
        self.assertEqual(_bm_expand_alternates('aa'), 'aa')
        self.assertEqual(_bm_expand_alternates('aa|bb'), 'aa|bb')
        self.assertEqual(_bm_expand_alternates('aa|aa'), 'aa|aa')

        self.assertEqual(_bm_expand_alternates('(aa)(bb)'), 'aabb')
        self.assertEqual(_bm_expand_alternates('(aa)(bb[0])'), '')
        self.assertEqual(_bm_expand_alternates('(aa)(bb[4])'), 'aabb[4]')
        self.assertEqual(_bm_expand_alternates('(aa[0])(bb)'), '')
        self.assertEqual(_bm_expand_alternates('(aa[4])(bb)'), 'aabb[4]')

        self.assertEqual(_bm_expand_alternates('(a|b|c)(a|b|c)'),
                         'aa|ab|ac|ba|bb|bc|ca|cb|cc')
        self.assertEqual(_bm_expand_alternates('(a[1]|b[2])(c|d)'),
                         'ac[1]|ad[1]|bc[2]|bd[2]')
        self.assertEqual(_bm_expand_alternates('(a[1]|b[2])(c[4]|d)'),
                         'ad[1]|bd[2]')

    def test_bm_remove_dupes(self):
        """Test abydos.bm._bm_remove_dupes."""
        self.assertEqual(_bm_remove_dupes(''), '')
        self.assertEqual(_bm_remove_dupes('aa'), 'aa')
        self.assertEqual(_bm_remove_dupes('aa|bb'), 'aa|bb')
        self.assertEqual(_bm_remove_dupes('aa|aa'), 'aa')
        self.assertEqual(_bm_remove_dupes('aa|aa|aa|bb|aa'), 'aa|bb')
        self.assertEqual(_bm_remove_dupes('bb|aa|bb|aa|bb'), 'bb|aa')

    def test_bm_normalize_lang_attrs(self):
        """Test abydos.bm._bm_normalize_language_attributes."""
        self.assertEqual(_bm_normalize_lang_attrs('', False), '')
        self.assertEqual(_bm_normalize_lang_attrs('', True), '')

        self.assertRaises(ValueError, _bm_normalize_lang_attrs, 'a[1', False)
        self.assertRaises(ValueError, _bm_normalize_lang_attrs, 'a[1', True)

        self.assertEqual(_bm_normalize_lang_attrs('abc', False), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[0]', False), '[0]')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2]', False), 'abc[2]')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2][4]', False), '[0]')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2][6]', False),
                         'abc[2]')
        self.assertEqual(_bm_normalize_lang_attrs('ab[2]c[4]', False), '[0]')
        self.assertEqual(_bm_normalize_lang_attrs('ab[2]c[6]', False),
                         'abc[2]')

        self.assertEqual(_bm_normalize_lang_attrs('abc', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[0]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2][4]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('abc[2][6]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('ab[2]c[4]', True), 'abc')
        self.assertEqual(_bm_normalize_lang_attrs('ab[2]c[6]', True), 'abc')


if __name__ == '__main__':
    unittest.main()
