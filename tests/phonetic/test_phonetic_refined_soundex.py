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

"""abydos.tests.phonetic.test_phonetic_refined_soundex.

This module contains unit tests for abydos.phonetic.RefinedSoundex
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import RefinedSoundex, refined_soundex


class RefinedSoundexTestCases(unittest.TestCase):
    """Test Refined Soundex functions.

    test cases for abydos.phonetic.RefinedSoundex
    """

    pa = RefinedSoundex()

    def test_refined_soundex(self):
        """Test abydos.phonetic.RefinedSoundex."""
        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(self.pa.encode('Braz'), 'B195')
        self.assertEqual(self.pa.encode('Broz'), 'B195')
        self.assertEqual(self.pa.encode('Caren'), 'C398')
        self.assertEqual(self.pa.encode('Caron'), 'C398')
        self.assertEqual(self.pa.encode('Carren'), 'C398')
        self.assertEqual(self.pa.encode('Charon'), 'C398')
        self.assertEqual(self.pa.encode('Corain'), 'C398')
        self.assertEqual(self.pa.encode('Coram'), 'C398')
        self.assertEqual(self.pa.encode('Corran'), 'C398')
        self.assertEqual(self.pa.encode('Corrin'), 'C398')
        self.assertEqual(self.pa.encode('Corwin'), 'C398')
        self.assertEqual(self.pa.encode('Curran'), 'C398')
        self.assertEqual(self.pa.encode('Curreen'), 'C398')
        self.assertEqual(self.pa.encode('Currin'), 'C398')
        self.assertEqual(self.pa.encode('Currom'), 'C398')
        self.assertEqual(self.pa.encode('Currum'), 'C398')
        self.assertEqual(self.pa.encode('Curwen'), 'C398')
        self.assertEqual(self.pa.encode('Caren'), 'C398')
        self.assertEqual(self.pa.encode('Caren'), 'C398')
        self.assertEqual(self.pa.encode('Caren'), 'C398')
        self.assertEqual(self.pa.encode('Caren'), 'C398')
        self.assertEqual(self.pa.encode('Caren'), 'C398')
        self.assertEqual(self.pa.encode('Caren'), 'C398')
        self.assertEqual(self.pa.encode('Caren'), 'C398')
        self.assertEqual(self.pa.encode('Hairs'), 'H93')
        self.assertEqual(self.pa.encode('Hark'), 'H93')
        self.assertEqual(self.pa.encode('Hars'), 'H93')
        self.assertEqual(self.pa.encode('Hayers'), 'H93')
        self.assertEqual(self.pa.encode('Heers'), 'H93')
        self.assertEqual(self.pa.encode('Hiers'), 'H93')
        self.assertEqual(self.pa.encode('Lambard'), 'L78196')
        self.assertEqual(self.pa.encode('Lambart'), 'L78196')
        self.assertEqual(self.pa.encode('Lambert'), 'L78196')
        self.assertEqual(self.pa.encode('Lambird'), 'L78196')
        self.assertEqual(self.pa.encode('Lampaert'), 'L78196')
        self.assertEqual(self.pa.encode('Lampard'), 'L78196')
        self.assertEqual(self.pa.encode('Lampart'), 'L78196')
        self.assertEqual(self.pa.encode('Lamperd'), 'L78196')
        self.assertEqual(self.pa.encode('Lampert'), 'L78196')
        self.assertEqual(self.pa.encode('Lamport'), 'L78196')
        self.assertEqual(self.pa.encode('Limbert'), 'L78196')
        self.assertEqual(self.pa.encode('Lombard'), 'L78196')
        self.assertEqual(self.pa.encode('Nolton'), 'N8768')
        self.assertEqual(self.pa.encode('Noulton'), 'N8768')

        # http://trimc-nlp.blogspot.com/2015/03/the-soundex-algorithm.html
        self.assertEqual(self.pa.encode('Craig'), 'C394')
        self.assertEqual(self.pa.encode('Crag'), 'C394')
        self.assertEqual(self.pa.encode('Crejg'), 'C394')
        self.assertEqual(self.pa.encode('Creig'), 'C394')
        self.assertEqual(self.pa.encode('Craigg'), 'C394')
        self.assertEqual(self.pa.encode('Craug'), 'C394')
        self.assertEqual(self.pa.encode('Craiggg'), 'C394')
        self.assertEqual(self.pa.encode('Creg'), 'C394')
        self.assertEqual(self.pa.encode('Cregg'), 'C394')
        self.assertEqual(self.pa.encode('Creag'), 'C394')
        self.assertEqual(self.pa.encode('Greg'), 'G494')
        self.assertEqual(self.pa.encode('Gregg'), 'G494')
        self.assertEqual(self.pa.encode('Graig'), 'G494')
        self.assertEqual(self.pa.encode('Greig'), 'G494')
        self.assertEqual(self.pa.encode('Greggg'), 'G494')
        self.assertEqual(self.pa.encode('Groeg'), 'G494')
        self.assertEqual(self.pa.encode('Graj'), 'G494')
        self.assertEqual(self.pa.encode('Grej'), 'G494')
        self.assertEqual(self.pa.encode('Grreg'), 'G494')
        self.assertEqual(self.pa.encode('Greag'), 'G494')
        self.assertEqual(self.pa.encode('Grig'), 'G494')
        self.assertEqual(self.pa.encode('Kregg'), 'K394')
        self.assertEqual(self.pa.encode('Kraig'), 'K394')
        self.assertEqual(self.pa.encode('Krag'), 'K394')
        self.assertEqual(self.pa.encode('Kreig'), 'K394')
        self.assertEqual(self.pa.encode('Krug'), 'K394')
        self.assertEqual(self.pa.encode('Kreg'), 'K394')
        self.assertEqual(self.pa.encode('Krieg'), 'K394')
        self.assertEqual(self.pa.encode('Krijg'), 'K394')

        # Apache Commons test cases
        # http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/RefinedSoundexTest.java?view=markup
        self.assertEqual(self.pa.encode('testing'), 'T63684')
        self.assertEqual(self.pa.encode('TESTING'), 'T63684')
        self.assertEqual(self.pa.encode('The'), 'T6')
        self.assertEqual(self.pa.encode('quick'), 'Q53')
        self.assertEqual(self.pa.encode('brown'), 'B198')
        self.assertEqual(self.pa.encode('fox'), 'F25')
        self.assertEqual(self.pa.encode('jumped'), 'J4816')
        self.assertEqual(self.pa.encode('over'), 'O29')
        self.assertEqual(self.pa.encode('the'), 'T6')
        self.assertEqual(self.pa.encode('lazy'), 'L75')
        self.assertEqual(self.pa.encode('dogs'), 'D643')

        # Test with retain_vowels=True
        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(self.pa.encode('Braz', retain_vowels=True), 'B1905')
        self.assertEqual(self.pa.encode('Broz', retain_vowels=True), 'B1905')
        self.assertEqual(self.pa.encode('Caren', retain_vowels=True), 'C30908')
        self.assertEqual(self.pa.encode('Caron', retain_vowels=True), 'C30908')
        self.assertEqual(
            self.pa.encode('Carren', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Charon', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Corain', retain_vowels=True), 'C30908'
        )
        self.assertEqual(self.pa.encode('Coram', retain_vowels=True), 'C30908')
        self.assertEqual(
            self.pa.encode('Corran', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Corrin', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Corwin', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Curran', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Curreen', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Currin', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Currom', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Currum', retain_vowels=True), 'C30908'
        )
        self.assertEqual(
            self.pa.encode('Curwen', retain_vowels=True), 'C30908'
        )
        self.assertEqual(self.pa.encode('Caren', retain_vowels=True), 'C30908')
        self.assertEqual(self.pa.encode('Caren', retain_vowels=True), 'C30908')
        self.assertEqual(self.pa.encode('Caren', retain_vowels=True), 'C30908')
        self.assertEqual(self.pa.encode('Caren', retain_vowels=True), 'C30908')
        self.assertEqual(self.pa.encode('Caren', retain_vowels=True), 'C30908')
        self.assertEqual(self.pa.encode('Caren', retain_vowels=True), 'C30908')
        self.assertEqual(self.pa.encode('Caren', retain_vowels=True), 'C30908')
        self.assertEqual(self.pa.encode('Hairs', retain_vowels=True), 'H093')
        self.assertEqual(self.pa.encode('Hark', retain_vowels=True), 'H093')
        self.assertEqual(self.pa.encode('Hars', retain_vowels=True), 'H093')
        self.assertEqual(self.pa.encode('Hayers', retain_vowels=True), 'H093')
        self.assertEqual(self.pa.encode('Heers', retain_vowels=True), 'H093')
        self.assertEqual(self.pa.encode('Hiers', retain_vowels=True), 'H093')
        self.assertEqual(
            self.pa.encode('Lambard', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lambart', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lambert', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lambird', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lampaert', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lampard', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lampart', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lamperd', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lampert', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lamport', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Limbert', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Lombard', retain_vowels=True), 'L7081096'
        )
        self.assertEqual(
            self.pa.encode('Nolton', retain_vowels=True), 'N807608'
        )
        self.assertEqual(
            self.pa.encode('Noulton', retain_vowels=True), 'N807608'
        )

        # http://trimc-nlp.blogspot.com/2015/03/the-soundex-algorithm.html
        self.assertEqual(self.pa.encode('Craig', retain_vowels=True), 'C3904')
        self.assertEqual(self.pa.encode('Crag', retain_vowels=True), 'C3904')
        self.assertEqual(self.pa.encode('Crejg', retain_vowels=True), 'C3904')
        self.assertEqual(self.pa.encode('Creig', retain_vowels=True), 'C3904')
        self.assertEqual(self.pa.encode('Craigg', retain_vowels=True), 'C3904')
        self.assertEqual(self.pa.encode('Craug', retain_vowels=True), 'C3904')
        self.assertEqual(
            self.pa.encode('Craiggg', retain_vowels=True), 'C3904'
        )
        self.assertEqual(self.pa.encode('Creg', retain_vowels=True), 'C3904')
        self.assertEqual(self.pa.encode('Cregg', retain_vowels=True), 'C3904')
        self.assertEqual(self.pa.encode('Creag', retain_vowels=True), 'C3904')
        self.assertEqual(self.pa.encode('Greg', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Gregg', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Graig', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Greig', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Greggg', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Groeg', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Graj', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Grej', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Grreg', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Greag', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Grig', retain_vowels=True), 'G4904')
        self.assertEqual(self.pa.encode('Kregg', retain_vowels=True), 'K3904')
        self.assertEqual(self.pa.encode('Kraig', retain_vowels=True), 'K3904')
        self.assertEqual(self.pa.encode('Krag', retain_vowels=True), 'K3904')
        self.assertEqual(self.pa.encode('Kreig', retain_vowels=True), 'K3904')
        self.assertEqual(self.pa.encode('Krug', retain_vowels=True), 'K3904')
        self.assertEqual(self.pa.encode('Kreg', retain_vowels=True), 'K3904')
        self.assertEqual(self.pa.encode('Krieg', retain_vowels=True), 'K3904')
        self.assertEqual(self.pa.encode('Krijg', retain_vowels=True), 'K3904')

        # Apache Commons test cases
        # http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/RefinedSoundexTest.java?view=markup
        self.assertEqual(
            self.pa.encode('testing', retain_vowels=True), 'T6036084'
        )
        self.assertEqual(
            self.pa.encode('TESTING', retain_vowels=True), 'T6036084'
        )
        self.assertEqual(self.pa.encode('The', retain_vowels=True), 'T60')
        self.assertEqual(self.pa.encode('quick', retain_vowels=True), 'Q503')
        self.assertEqual(self.pa.encode('brown', retain_vowels=True), 'B1908')
        self.assertEqual(self.pa.encode('fox', retain_vowels=True), 'F205')
        self.assertEqual(
            self.pa.encode('jumped', retain_vowels=True), 'J408106'
        )
        self.assertEqual(self.pa.encode('over', retain_vowels=True), 'O0209')
        self.assertEqual(self.pa.encode('the', retain_vowels=True), 'T60')
        self.assertEqual(self.pa.encode('lazy', retain_vowels=True), 'L7050')
        self.assertEqual(self.pa.encode('dogs', retain_vowels=True), 'D6043')

        # length tests
        self.assertEqual(
            self.pa.encode('testing', max_length=4, zero_pad=True), 'T636'
        )
        self.assertEqual(
            self.pa.encode('TESTING', max_length=4, zero_pad=True), 'T636'
        )
        self.assertEqual(
            self.pa.encode('The', max_length=4, zero_pad=True), 'T600'
        )
        self.assertEqual(
            self.pa.encode('quick', max_length=4, zero_pad=True), 'Q530'
        )
        self.assertEqual(
            self.pa.encode('brown', max_length=4, zero_pad=True), 'B198'
        )
        self.assertEqual(
            self.pa.encode('fox', max_length=4, zero_pad=True), 'F250'
        )
        self.assertEqual(
            self.pa.encode('jumped', max_length=4, zero_pad=True), 'J481'
        )
        self.assertEqual(
            self.pa.encode('over', max_length=4, zero_pad=True), 'O290'
        )
        self.assertEqual(
            self.pa.encode('the', max_length=4, zero_pad=True), 'T600'
        )
        self.assertEqual(
            self.pa.encode('lazy', max_length=4, zero_pad=True), 'L750'
        )
        self.assertEqual(
            self.pa.encode('dogs', max_length=4, zero_pad=True), 'D643'
        )
        self.assertEqual(self.pa.encode('The', max_length=4), 'T6')
        self.assertEqual(self.pa.encode('quick', max_length=4), 'Q53')
        self.assertEqual(self.pa.encode('brown', max_length=4), 'B198')
        self.assertEqual(self.pa.encode('fox', max_length=4), 'F25')
        self.assertEqual(self.pa.encode('jumped', max_length=4), 'J481')
        self.assertEqual(self.pa.encode('over', max_length=4), 'O29')
        self.assertEqual(self.pa.encode('the', max_length=4), 'T6')
        self.assertEqual(self.pa.encode('lazy', max_length=4), 'L75')
        self.assertEqual(self.pa.encode('dogs', max_length=4), 'D643')

        # Test wrapper
        self.assertEqual(refined_soundex('Braz'), 'B195')


if __name__ == '__main__':
    unittest.main()
