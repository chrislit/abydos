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
        pa_vowels = RefinedSoundex(retain_vowels=True)
        self.assertEqual(pa_vowels.encode('Braz'), 'B1905')
        self.assertEqual(pa_vowels.encode('Broz'), 'B1905')
        self.assertEqual(pa_vowels.encode('Caren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Caron'), 'C30908')
        self.assertEqual(pa_vowels.encode('Carren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Charon'), 'C30908')
        self.assertEqual(pa_vowels.encode('Corain'), 'C30908')
        self.assertEqual(pa_vowels.encode('Coram'), 'C30908')
        self.assertEqual(pa_vowels.encode('Corran'), 'C30908')
        self.assertEqual(pa_vowels.encode('Corrin'), 'C30908')
        self.assertEqual(pa_vowels.encode('Corwin'), 'C30908')
        self.assertEqual(pa_vowels.encode('Curran'), 'C30908')
        self.assertEqual(pa_vowels.encode('Curreen'), 'C30908')
        self.assertEqual(pa_vowels.encode('Currin'), 'C30908')
        self.assertEqual(pa_vowels.encode('Currom'), 'C30908')
        self.assertEqual(pa_vowels.encode('Currum'), 'C30908')
        self.assertEqual(pa_vowels.encode('Curwen'), 'C30908')
        self.assertEqual(pa_vowels.encode('Caren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Caren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Caren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Caren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Caren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Caren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Caren'), 'C30908')
        self.assertEqual(pa_vowels.encode('Hairs'), 'H093')
        self.assertEqual(pa_vowels.encode('Hark'), 'H093')
        self.assertEqual(pa_vowels.encode('Hars'), 'H093')
        self.assertEqual(pa_vowels.encode('Hayers'), 'H093')
        self.assertEqual(pa_vowels.encode('Heers'), 'H093')
        self.assertEqual(pa_vowels.encode('Hiers'), 'H093')
        self.assertEqual(pa_vowels.encode('Lambard'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lambart'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lambert'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lambird'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lampaert'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lampard'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lampart'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lamperd'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lampert'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lamport'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Limbert'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Lombard'), 'L7081096')
        self.assertEqual(pa_vowels.encode('Nolton'), 'N807608')
        self.assertEqual(pa_vowels.encode('Noulton'), 'N807608')

        # http://trimc-nlp.blogspot.com/2015/03/the-soundex-algorithm.html
        self.assertEqual(pa_vowels.encode('Craig'), 'C3904')
        self.assertEqual(pa_vowels.encode('Crag'), 'C3904')
        self.assertEqual(pa_vowels.encode('Crejg'), 'C3904')
        self.assertEqual(pa_vowels.encode('Creig'), 'C3904')
        self.assertEqual(pa_vowels.encode('Craigg'), 'C3904')
        self.assertEqual(pa_vowels.encode('Craug'), 'C3904')
        self.assertEqual(pa_vowels.encode('Craiggg'), 'C3904')
        self.assertEqual(pa_vowels.encode('Creg'), 'C3904')
        self.assertEqual(pa_vowels.encode('Cregg'), 'C3904')
        self.assertEqual(pa_vowels.encode('Creag'), 'C3904')
        self.assertEqual(pa_vowels.encode('Greg'), 'G4904')
        self.assertEqual(pa_vowels.encode('Gregg'), 'G4904')
        self.assertEqual(pa_vowels.encode('Graig'), 'G4904')
        self.assertEqual(pa_vowels.encode('Greig'), 'G4904')
        self.assertEqual(pa_vowels.encode('Greggg'), 'G4904')
        self.assertEqual(pa_vowels.encode('Groeg'), 'G4904')
        self.assertEqual(pa_vowels.encode('Graj'), 'G4904')
        self.assertEqual(pa_vowels.encode('Grej'), 'G4904')
        self.assertEqual(pa_vowels.encode('Grreg'), 'G4904')
        self.assertEqual(pa_vowels.encode('Greag'), 'G4904')
        self.assertEqual(pa_vowels.encode('Grig'), 'G4904')
        self.assertEqual(pa_vowels.encode('Kregg'), 'K3904')
        self.assertEqual(pa_vowels.encode('Kraig'), 'K3904')
        self.assertEqual(pa_vowels.encode('Krag'), 'K3904')
        self.assertEqual(pa_vowels.encode('Kreig'), 'K3904')
        self.assertEqual(pa_vowels.encode('Krug'), 'K3904')
        self.assertEqual(pa_vowels.encode('Kreg'), 'K3904')
        self.assertEqual(pa_vowels.encode('Krieg'), 'K3904')
        self.assertEqual(pa_vowels.encode('Krijg'), 'K3904')

        # Apache Commons test cases
        # http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/RefinedSoundexTest.java?view=markup
        self.assertEqual(pa_vowels.encode('testing'), 'T6036084')
        self.assertEqual(pa_vowels.encode('TESTING'), 'T6036084')
        self.assertEqual(pa_vowels.encode('The'), 'T60')
        self.assertEqual(pa_vowels.encode('quick'), 'Q503')
        self.assertEqual(pa_vowels.encode('brown'), 'B1908')
        self.assertEqual(pa_vowels.encode('fox'), 'F205')
        self.assertEqual(pa_vowels.encode('jumped'), 'J408106')
        self.assertEqual(pa_vowels.encode('over'), 'O0209')
        self.assertEqual(pa_vowels.encode('the'), 'T60')
        self.assertEqual(pa_vowels.encode('lazy'), 'L7050')
        self.assertEqual(pa_vowels.encode('dogs'), 'D6043')

        # length tests
        pa_40 = RefinedSoundex(max_length=4, zero_pad=True)
        self.assertEqual(pa_40.encode('testing'), 'T636')
        self.assertEqual(pa_40.encode('TESTING'), 'T636')
        self.assertEqual(pa_40.encode('The'), 'T600')
        self.assertEqual(pa_40.encode('quick'), 'Q530')
        self.assertEqual(pa_40.encode('brown'), 'B198')
        self.assertEqual(pa_40.encode('fox'), 'F250')
        self.assertEqual(pa_40.encode('jumped'), 'J481')
        self.assertEqual(pa_40.encode('over'), 'O290')
        self.assertEqual(pa_40.encode('the'), 'T600')
        self.assertEqual(pa_40.encode('lazy'), 'L750')
        self.assertEqual(pa_40.encode('dogs'), 'D643')
        pa_4 = RefinedSoundex(max_length=4)
        self.assertEqual(pa_4.encode('The'), 'T6')
        self.assertEqual(pa_4.encode('quick'), 'Q53')
        self.assertEqual(pa_4.encode('brown'), 'B198')
        self.assertEqual(pa_4.encode('fox'), 'F25')
        self.assertEqual(pa_4.encode('jumped'), 'J481')
        self.assertEqual(pa_4.encode('over'), 'O29')
        self.assertEqual(pa_4.encode('the'), 'T6')
        self.assertEqual(pa_4.encode('lazy'), 'L75')
        self.assertEqual(pa_4.encode('dogs'), 'D643')

        # Test wrapper
        self.assertEqual(refined_soundex('Braz'), 'B195')


if __name__ == '__main__':
    unittest.main()
