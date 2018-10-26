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

"""abydos.tests.phonetic.test_phonetic_soundex.

This module contains unit tests for abydos.phonetic._soundex
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic import (
    fuzzy_soundex,
    lein,
    phonex,
    phonix,
    pshp_soundex_first,
    pshp_soundex_last,
    refined_soundex,
    soundex,
)


class SoundexTestCases(unittest.TestCase):
    """Test Soundex functions.

    test cases for abydos.phonetic._soundex.soundex, .refined_soundex
    """

    def test_soundex(self):
        """Test abydos.phonetic._soundex.soundex."""
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

        # max_length tests
        self.assertEqual(soundex('Lincoln', 10), 'L524500000')
        self.assertEqual(soundex('Lincoln', 5), 'L5245')
        self.assertEqual(soundex('Christopher', 6), 'C62316')

        # max_length bounds tests
        self.assertEqual(
            soundex('Niall', max_length=-1),
            'N4000000000000000000000000000000000000000000000000'
            + '00000000000000',
        )
        self.assertEqual(soundex('Niall', max_length=0), 'N400')

        # reverse tests
        self.assertEqual(soundex('Rubin', reverse=True), 'N160')
        self.assertEqual(soundex('Llyod', reverse=True), 'D400')
        self.assertEqual(soundex('Lincoln', reverse=True), 'N425')
        self.assertEqual(soundex('Knuth', reverse=True), 'H352')

        # zero_pad tests
        self.assertEqual(soundex('Niall', max_length=-1, zero_pad=False), 'N4')
        self.assertEqual(soundex('Niall', max_length=0, zero_pad=False), 'N4')
        self.assertEqual(soundex('Niall', max_length=0, zero_pad=True), 'N400')
        self.assertEqual(soundex('', max_length=4, zero_pad=False), '0')
        self.assertEqual(soundex('', max_length=4, zero_pad=True), '0000')

    def test_soundex_special(self):
        """Test abydos.phonetic._soundex.soundex (special 1880-1910 variant method)."""  # noqa: E501
        self.assertEqual(soundex('Ashcroft', var='special'), 'A226')
        self.assertEqual(soundex('Asicroft', var='special'), 'A226')
        self.assertEqual(soundex('AsWcroft', var='special'), 'A226')
        self.assertEqual(soundex('Rupert', var='special'), 'R163')
        self.assertEqual(soundex('Rubin', var='special'), 'R150')

    def test_soundex_census(self):
        """Test abydos.phonetic._soundex.soundex (Census variant method)."""
        self.assertEqual(soundex('Vandeusen', var='Census'), ('V532', 'D250'))
        self.assertEqual(soundex('van Deusen', var='Census'), ('V532', 'D250'))
        self.assertEqual(soundex('McDonald', var='Census'), 'M235')
        self.assertEqual(soundex('la Cruz', var='Census'), ('L262', 'C620'))
        self.assertEqual(soundex('vanDamme', var='Census'), ('V535', 'D500'))

    def test_refined_soundex(self):
        """Test abydos.phonetic._soundex.refined_soundex."""
        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(refined_soundex('Braz'), 'B195')
        self.assertEqual(refined_soundex('Broz'), 'B195')
        self.assertEqual(refined_soundex('Caren'), 'C398')
        self.assertEqual(refined_soundex('Caron'), 'C398')
        self.assertEqual(refined_soundex('Carren'), 'C398')
        self.assertEqual(refined_soundex('Charon'), 'C398')
        self.assertEqual(refined_soundex('Corain'), 'C398')
        self.assertEqual(refined_soundex('Coram'), 'C398')
        self.assertEqual(refined_soundex('Corran'), 'C398')
        self.assertEqual(refined_soundex('Corrin'), 'C398')
        self.assertEqual(refined_soundex('Corwin'), 'C398')
        self.assertEqual(refined_soundex('Curran'), 'C398')
        self.assertEqual(refined_soundex('Curreen'), 'C398')
        self.assertEqual(refined_soundex('Currin'), 'C398')
        self.assertEqual(refined_soundex('Currom'), 'C398')
        self.assertEqual(refined_soundex('Currum'), 'C398')
        self.assertEqual(refined_soundex('Curwen'), 'C398')
        self.assertEqual(refined_soundex('Caren'), 'C398')
        self.assertEqual(refined_soundex('Caren'), 'C398')
        self.assertEqual(refined_soundex('Caren'), 'C398')
        self.assertEqual(refined_soundex('Caren'), 'C398')
        self.assertEqual(refined_soundex('Caren'), 'C398')
        self.assertEqual(refined_soundex('Caren'), 'C398')
        self.assertEqual(refined_soundex('Caren'), 'C398')
        self.assertEqual(refined_soundex('Hairs'), 'H93')
        self.assertEqual(refined_soundex('Hark'), 'H93')
        self.assertEqual(refined_soundex('Hars'), 'H93')
        self.assertEqual(refined_soundex('Hayers'), 'H93')
        self.assertEqual(refined_soundex('Heers'), 'H93')
        self.assertEqual(refined_soundex('Hiers'), 'H93')
        self.assertEqual(refined_soundex('Lambard'), 'L78196')
        self.assertEqual(refined_soundex('Lambart'), 'L78196')
        self.assertEqual(refined_soundex('Lambert'), 'L78196')
        self.assertEqual(refined_soundex('Lambird'), 'L78196')
        self.assertEqual(refined_soundex('Lampaert'), 'L78196')
        self.assertEqual(refined_soundex('Lampard'), 'L78196')
        self.assertEqual(refined_soundex('Lampart'), 'L78196')
        self.assertEqual(refined_soundex('Lamperd'), 'L78196')
        self.assertEqual(refined_soundex('Lampert'), 'L78196')
        self.assertEqual(refined_soundex('Lamport'), 'L78196')
        self.assertEqual(refined_soundex('Limbert'), 'L78196')
        self.assertEqual(refined_soundex('Lombard'), 'L78196')
        self.assertEqual(refined_soundex('Nolton'), 'N8768')
        self.assertEqual(refined_soundex('Noulton'), 'N8768')

        # http://trimc-nlp.blogspot.com/2015/03/the-soundex-algorithm.html
        self.assertEqual(refined_soundex('Craig'), 'C394')
        self.assertEqual(refined_soundex('Crag'), 'C394')
        self.assertEqual(refined_soundex('Crejg'), 'C394')
        self.assertEqual(refined_soundex('Creig'), 'C394')
        self.assertEqual(refined_soundex('Craigg'), 'C394')
        self.assertEqual(refined_soundex('Craug'), 'C394')
        self.assertEqual(refined_soundex('Craiggg'), 'C394')
        self.assertEqual(refined_soundex('Creg'), 'C394')
        self.assertEqual(refined_soundex('Cregg'), 'C394')
        self.assertEqual(refined_soundex('Creag'), 'C394')
        self.assertEqual(refined_soundex('Greg'), 'G494')
        self.assertEqual(refined_soundex('Gregg'), 'G494')
        self.assertEqual(refined_soundex('Graig'), 'G494')
        self.assertEqual(refined_soundex('Greig'), 'G494')
        self.assertEqual(refined_soundex('Greggg'), 'G494')
        self.assertEqual(refined_soundex('Groeg'), 'G494')
        self.assertEqual(refined_soundex('Graj'), 'G494')
        self.assertEqual(refined_soundex('Grej'), 'G494')
        self.assertEqual(refined_soundex('Grreg'), 'G494')
        self.assertEqual(refined_soundex('Greag'), 'G494')
        self.assertEqual(refined_soundex('Grig'), 'G494')
        self.assertEqual(refined_soundex('Kregg'), 'K394')
        self.assertEqual(refined_soundex('Kraig'), 'K394')
        self.assertEqual(refined_soundex('Krag'), 'K394')
        self.assertEqual(refined_soundex('Kreig'), 'K394')
        self.assertEqual(refined_soundex('Krug'), 'K394')
        self.assertEqual(refined_soundex('Kreg'), 'K394')
        self.assertEqual(refined_soundex('Krieg'), 'K394')
        self.assertEqual(refined_soundex('Krijg'), 'K394')

        # Apache Commons test cases
        # http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/RefinedSoundexTest.java?view=markup
        self.assertEqual(refined_soundex('testing'), 'T63684')
        self.assertEqual(refined_soundex('TESTING'), 'T63684')
        self.assertEqual(refined_soundex('The'), 'T6')
        self.assertEqual(refined_soundex('quick'), 'Q53')
        self.assertEqual(refined_soundex('brown'), 'B198')
        self.assertEqual(refined_soundex('fox'), 'F25')
        self.assertEqual(refined_soundex('jumped'), 'J4816')
        self.assertEqual(refined_soundex('over'), 'O29')
        self.assertEqual(refined_soundex('the'), 'T6')
        self.assertEqual(refined_soundex('lazy'), 'L75')
        self.assertEqual(refined_soundex('dogs'), 'D643')

        # Test with retain_vowels=True
        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(refined_soundex('Braz', retain_vowels=True), 'B1905')
        self.assertEqual(refined_soundex('Broz', retain_vowels=True), 'B1905')
        self.assertEqual(
            refined_soundex('Caren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Caron', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Carren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Charon', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Corain', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Coram', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Corran', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Corrin', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Corwin', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Curran', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Curreen', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Currin', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Currom', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Currum', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Curwen', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Caren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Caren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Caren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Caren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Caren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Caren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            refined_soundex('Caren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(refined_soundex('Hairs', retain_vowels=True), 'H093')
        self.assertEqual(refined_soundex('Hark', retain_vowels=True), 'H093')
        self.assertEqual(refined_soundex('Hars', retain_vowels=True), 'H093')
        self.assertEqual(refined_soundex('Hayers', retain_vowels=True), 'H093')
        self.assertEqual(refined_soundex('Heers', retain_vowels=True), 'H093')
        self.assertEqual(refined_soundex('Hiers', retain_vowels=True), 'H093')
        self.assertEqual(
            refined_soundex('Lambard', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lambart', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lambert', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lambird', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lampaert', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lampard', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lampart', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lamperd', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lampert', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lamport', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Limbert', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Lombard', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            refined_soundex('Nolton', retain_vowels=True), 'N807608'
        )
        self.assertEqual(
            refined_soundex('Noulton', retain_vowels=True), 'N807608'
        )

        # http://trimc-nlp.blogspot.com/2015/03/the-soundex-algorithm.html
        self.assertEqual(refined_soundex('Craig', retain_vowels=True), 'C3904')
        self.assertEqual(refined_soundex('Crag', retain_vowels=True), 'C3904')
        self.assertEqual(refined_soundex('Crejg', retain_vowels=True), 'C3904')
        self.assertEqual(refined_soundex('Creig', retain_vowels=True), 'C3904')
        self.assertEqual(
            refined_soundex('Craigg', retain_vowels=True), 'C3904'
        )
        self.assertEqual(refined_soundex('Craug', retain_vowels=True), 'C3904')
        self.assertEqual(
            refined_soundex('Craiggg', retain_vowels=True), 'C3904'
        )
        self.assertEqual(refined_soundex('Creg', retain_vowels=True), 'C3904')
        self.assertEqual(refined_soundex('Cregg', retain_vowels=True), 'C3904')
        self.assertEqual(refined_soundex('Creag', retain_vowels=True), 'C3904')
        self.assertEqual(refined_soundex('Greg', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Gregg', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Graig', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Greig', retain_vowels=True), 'G4904')
        self.assertEqual(
            refined_soundex('Greggg', retain_vowels=True), 'G4904'
        )
        self.assertEqual(refined_soundex('Groeg', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Graj', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Grej', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Grreg', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Greag', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Grig', retain_vowels=True), 'G4904')
        self.assertEqual(refined_soundex('Kregg', retain_vowels=True), 'K3904')
        self.assertEqual(refined_soundex('Kraig', retain_vowels=True), 'K3904')
        self.assertEqual(refined_soundex('Krag', retain_vowels=True), 'K3904')
        self.assertEqual(refined_soundex('Kreig', retain_vowels=True), 'K3904')
        self.assertEqual(refined_soundex('Krug', retain_vowels=True), 'K3904')
        self.assertEqual(refined_soundex('Kreg', retain_vowels=True), 'K3904')
        self.assertEqual(refined_soundex('Krieg', retain_vowels=True), 'K3904')
        self.assertEqual(refined_soundex('Krijg', retain_vowels=True), 'K3904')

        # Apache Commons test cases
        # http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/RefinedSoundexTest.java?view=markup
        self.assertEqual(
            refined_soundex('testing', retain_vowels=True), 'T6036084'
        )
        self.assertEqual(
            refined_soundex('TESTING', retain_vowels=True), 'T6036084'
        )
        self.assertEqual(refined_soundex('The', retain_vowels=True), 'T60')
        self.assertEqual(refined_soundex('quick', retain_vowels=True), 'Q503')
        self.assertEqual(refined_soundex('brown', retain_vowels=True), 'B1908')
        self.assertEqual(refined_soundex('fox', retain_vowels=True), 'F205')
        self.assertEqual(
            refined_soundex('jumped', retain_vowels=True), 'J408106'
        )
        self.assertEqual(refined_soundex('over', retain_vowels=True), 'O0209')
        self.assertEqual(refined_soundex('the', retain_vowels=True), 'T60')
        self.assertEqual(refined_soundex('lazy', retain_vowels=True), 'L7050')
        self.assertEqual(refined_soundex('dogs', retain_vowels=True), 'D6043')

        # length tests
        self.assertEqual(
            refined_soundex('testing', max_length=4, zero_pad=True), 'T636'
        )
        self.assertEqual(
            refined_soundex('TESTING', max_length=4, zero_pad=True), 'T636'
        )
        self.assertEqual(
            refined_soundex('The', max_length=4, zero_pad=True), 'T600'
        )
        self.assertEqual(
            refined_soundex('quick', max_length=4, zero_pad=True), 'Q530'
        )
        self.assertEqual(
            refined_soundex('brown', max_length=4, zero_pad=True), 'B198'
        )
        self.assertEqual(
            refined_soundex('fox', max_length=4, zero_pad=True), 'F250'
        )
        self.assertEqual(
            refined_soundex('jumped', max_length=4, zero_pad=True), 'J481'
        )
        self.assertEqual(
            refined_soundex('over', max_length=4, zero_pad=True), 'O290'
        )
        self.assertEqual(
            refined_soundex('the', max_length=4, zero_pad=True), 'T600'
        )
        self.assertEqual(
            refined_soundex('lazy', max_length=4, zero_pad=True), 'L750'
        )
        self.assertEqual(
            refined_soundex('dogs', max_length=4, zero_pad=True), 'D643'
        )
        self.assertEqual(refined_soundex('The', max_length=4), 'T6')
        self.assertEqual(refined_soundex('quick', max_length=4), 'Q53')
        self.assertEqual(refined_soundex('brown', max_length=4), 'B198')
        self.assertEqual(refined_soundex('fox', max_length=4), 'F25')
        self.assertEqual(refined_soundex('jumped', max_length=4), 'J481')
        self.assertEqual(refined_soundex('over', max_length=4), 'O29')
        self.assertEqual(refined_soundex('the', max_length=4), 'T6')
        self.assertEqual(refined_soundex('lazy', max_length=4), 'L75')
        self.assertEqual(refined_soundex('dogs', max_length=4), 'D643')


class FuzzySoundexTestCases(unittest.TestCase):
    """Test Fuzzy Soundex functions.

    test cases for abydos.phonetic._soundex.fuzzy_soundex
    """

    def test_fuzzy_soundex(self):
        """Test abydos.phonetic._soundex.fuzzy_soundex."""
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

        # max_length bounds tests
        self.assertEqual(
            fuzzy_soundex('Niall', max_length=-1),
            'N4000000000000000000000000000000000000000000000000'
            + '00000000000000',
        )
        self.assertEqual(fuzzy_soundex('Niall', max_length=0), 'N400')

        # zero_pad tests
        self.assertEqual(
            fuzzy_soundex('Niall', max_length=-1, zero_pad=False), 'N4'
        )
        self.assertEqual(
            fuzzy_soundex('Niall', max_length=0, zero_pad=False), 'N4'
        )
        self.assertEqual(
            fuzzy_soundex('Niall', max_length=0, zero_pad=True), 'N400'
        )
        self.assertEqual(fuzzy_soundex('', max_length=4, zero_pad=False), '0')
        self.assertEqual(
            fuzzy_soundex('', max_length=4, zero_pad=True), '0000'
        )


class PhonexTestCases(unittest.TestCase):
    """Test Phonex functions.

    test cases for abydos.phonetic._soundex.phonex
    """

    def test_phonex(self):
        """Test abydos.phonetic._soundex.phonex."""
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

        # max_length bounds tests
        self.assertEqual(
            phonex('Niall', max_length=-1),
            'N4000000000000000000000000000000000000000000000000'
            + '00000000000000',
        )
        self.assertEqual(phonex('Niall', max_length=0), 'N400')

        # zero_pad tests
        self.assertEqual(phonex('Niall', max_length=0, zero_pad=False), 'N4')
        self.assertEqual(phonex('Niall', max_length=0, zero_pad=False), 'N4')
        self.assertEqual(phonex('Niall', max_length=0, zero_pad=True), 'N400')
        self.assertEqual(phonex('', max_length=4, zero_pad=False), '0')
        self.assertEqual(phonex('', max_length=4, zero_pad=True), '0000')


class PhonixTestCases(unittest.TestCase):
    """Test Phonix functions.

    test cases for abydos.phonetic._soundex.phonix
    """

    def test_phonix(self):
        """Test abydos.phonetic._soundex.phonix."""
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

        # max_length bounds tests
        self.assertEqual(phonix('Niall', max_length=-1), 'N4' + '0' * 62)
        self.assertEqual(phonix('Niall', max_length=0), 'N400')

        # zero_pad tests
        self.assertEqual(phonix('Niall', max_length=-1, zero_pad=False), 'N4')
        self.assertEqual(phonix('Niall', max_length=0, zero_pad=False), 'N4')
        self.assertEqual(phonix('Niall', max_length=0, zero_pad=True), 'N400')
        self.assertEqual(phonix('', max_length=4, zero_pad=False), '0')
        self.assertEqual(phonix('', max_length=4, zero_pad=True), '0000')


class LeinTestCases(unittest.TestCase):
    """Test Lein functions.

    test cases for abydos.phonetic._soundex.lein
    """

    def test_lein(self):
        """Test abydos.phonetic._soundex.lein."""
        self.assertEqual(lein(''), '0000')

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

        # Coverage
        self.assertEqual(lein('Lüdenscheidt', zero_pad=False), 'L125')
        self.assertEqual(lein('Smith', zero_pad=False), 'S21')


class PSHPSoundexTestCases(unittest.TestCase):
    """Test PSHP Soundex functions.

    test cases for abydos.phonetic._soundex.pshp_soundex_last &
    .pshp_soundex_first
    """

    def test_pshp_soundex_last(self):
        """Test abydos.phonetic._soundex.pshp_soundex_last."""
        # Base case
        self.assertEqual(pshp_soundex_last(''), '0000')

        self.assertEqual(pshp_soundex_last('JAMES'), 'J500')
        self.assertEqual(pshp_soundex_last('JOHN'), 'J500')
        self.assertEqual(pshp_soundex_last('PAT'), 'P300')
        self.assertEqual(pshp_soundex_last('PETER'), 'P350')

        self.assertEqual(pshp_soundex_last('Smith'), 'S530')
        self.assertEqual(pshp_soundex_last('van Damme'), 'D500')
        self.assertEqual(pshp_soundex_last('MacNeil'), 'M400')
        self.assertEqual(pshp_soundex_last('McNeil'), 'M400')
        self.assertEqual(pshp_soundex_last('Edwards'), 'A353')
        self.assertEqual(pshp_soundex_last('Gin'), 'J500')
        self.assertEqual(pshp_soundex_last('Cillian'), 'S450')
        self.assertEqual(pshp_soundex_last('Christopher'), 'K523')
        self.assertEqual(pshp_soundex_last('Carme'), 'K500')
        self.assertEqual(pshp_soundex_last('Knight'), 'N230')
        self.assertEqual(pshp_soundex_last('Phillip'), 'F410')
        self.assertEqual(pshp_soundex_last('Wein'), 'V500')
        self.assertEqual(pshp_soundex_last('Wagner', german=True), 'V255')
        self.assertEqual(pshp_soundex_last('Pence'), 'P500')
        self.assertEqual(pshp_soundex_last('Less'), 'L000')
        self.assertEqual(pshp_soundex_last('Simpson'), 'S525')
        self.assertEqual(pshp_soundex_last('Samson'), 'S250')
        self.assertEqual(pshp_soundex_last('Lang'), 'L500')
        self.assertEqual(pshp_soundex_last('Hagan'), 'H500')
        self.assertEqual(pshp_soundex_last('Cartes', german=True), 'K500')
        self.assertEqual(pshp_soundex_last('Kats', german=True), 'K000')
        self.assertEqual(pshp_soundex_last('Schultze', german=True), 'S400')
        self.assertEqual(pshp_soundex_last('Alze', german=True), 'A400')
        self.assertEqual(pshp_soundex_last('Galz', german=True), 'G400')
        self.assertEqual(pshp_soundex_last('Alte', german=True), 'A400')
        self.assertEqual(pshp_soundex_last('Alte', max_length=-1), 'A43')
        self.assertEqual(
            pshp_soundex_last('Altemaier', max_length=-1), 'A4355'
        )

    def test_pshp_soundex_first(self):
        """Test abydos.phonetic._soundex.pshp_soundex_first."""
        # Base case
        self.assertEqual(pshp_soundex_first(''), '0000')

        # Examples given in defining paper (Hershberg, et al. 1976)
        self.assertEqual(pshp_soundex_first('JAMES'), 'J700')
        self.assertEqual(pshp_soundex_first('JOHN'), 'J500')
        self.assertEqual(pshp_soundex_first('PAT'), 'P700')
        self.assertEqual(pshp_soundex_first('PETER'), 'P300')

        # Additions for coverage
        self.assertEqual(pshp_soundex_first('Giles'), 'J400')
        self.assertEqual(pshp_soundex_first('Cy'), 'S000')
        self.assertEqual(pshp_soundex_first('Chris'), 'K500')
        self.assertEqual(pshp_soundex_first('Caleb'), 'K400')
        self.assertEqual(pshp_soundex_first('Knabe'), 'N100')
        self.assertEqual(pshp_soundex_first('Phil'), 'F400')
        self.assertEqual(pshp_soundex_first('Wieland'), 'V400')
        self.assertEqual(pshp_soundex_first('Wayne', german=True), 'V500')
        self.assertEqual(
            pshp_soundex_first('Christopher', max_length=-1), 'K5'
        )
        self.assertEqual(
            pshp_soundex_first('Asdaananndsjsjasd', max_length=-1), 'A23553223'
        )
        self.assertEqual(pshp_soundex_first('Asdaananndsjsjasd'), 'A235')


if __name__ == '__main__':
    unittest.main()
