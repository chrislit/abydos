# Copyright 2014-2022 by Christopher C. Little.
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

import unittest

from abydos.phonetic import RefinedSoundex


class RefinedSoundexTestCases(unittest.TestCase):
    """Test Refined Soundex functions.

    test cases for abydos.phonetic.RefinedSoundex
    """

    pa = RefinedSoundex()

    def test_refined_soundex(self):
        """Test abydos.phonetic.RefinedSoundex."""
        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(self.pa.encode('Braz'), 'B95')
        self.assertEqual(self.pa.encode('Broz'), 'B95')
        self.assertEqual(self.pa.encode('Caren'), 'C98')
        self.assertEqual(self.pa.encode('Caron'), 'C98')
        self.assertEqual(self.pa.encode('Carren'), 'C98')
        self.assertEqual(self.pa.encode('Charon'), 'C98')
        self.assertEqual(self.pa.encode('Corain'), 'C98')
        self.assertEqual(self.pa.encode('Coram'), 'C98')
        self.assertEqual(self.pa.encode('Corran'), 'C98')
        self.assertEqual(self.pa.encode('Corrin'), 'C98')
        self.assertEqual(self.pa.encode('Corwin'), 'C98')
        self.assertEqual(self.pa.encode('Curran'), 'C98')
        self.assertEqual(self.pa.encode('Curreen'), 'C98')
        self.assertEqual(self.pa.encode('Currin'), 'C98')
        self.assertEqual(self.pa.encode('Currom'), 'C98')
        self.assertEqual(self.pa.encode('Currum'), 'C98')
        self.assertEqual(self.pa.encode('Curwen'), 'C98')
        self.assertEqual(self.pa.encode('Hairs'), 'H93')
        self.assertEqual(self.pa.encode('Hark'), 'H93')
        self.assertEqual(self.pa.encode('Hars'), 'H93')
        self.assertEqual(self.pa.encode('Hayers'), 'H93')
        self.assertEqual(self.pa.encode('Heers'), 'H93')
        self.assertEqual(self.pa.encode('Hiers'), 'H93')
        self.assertEqual(self.pa.encode('Lambard'), 'L8196')
        self.assertEqual(self.pa.encode('Lambart'), 'L8196')
        self.assertEqual(self.pa.encode('Lambert'), 'L8196')
        self.assertEqual(self.pa.encode('Lambird'), 'L8196')
        self.assertEqual(self.pa.encode('Lampaert'), 'L8196')
        self.assertEqual(self.pa.encode('Lampard'), 'L8196')
        self.assertEqual(self.pa.encode('Lampart'), 'L8196')
        self.assertEqual(self.pa.encode('Lamperd'), 'L8196')
        self.assertEqual(self.pa.encode('Lampert'), 'L8196')
        self.assertEqual(self.pa.encode('Lamport'), 'L8196')
        self.assertEqual(self.pa.encode('Limbert'), 'L8196')
        self.assertEqual(self.pa.encode('Lombard'), 'L8196')
        self.assertEqual(self.pa.encode('Nolton'), 'N768')
        self.assertEqual(self.pa.encode('Noulton'), 'N768')

        # http://trimc-nlp.blogspot.com/2015/03/the-soundex-algorithm.html
        self.assertEqual(self.pa.encode('Craig'), 'C94')
        self.assertEqual(self.pa.encode('Crag'), 'C94')
        self.assertEqual(self.pa.encode('Crejg'), 'C94')
        self.assertEqual(self.pa.encode('Creig'), 'C94')
        self.assertEqual(self.pa.encode('Craigg'), 'C94')
        self.assertEqual(self.pa.encode('Craug'), 'C94')
        self.assertEqual(self.pa.encode('Craiggg'), 'C94')
        self.assertEqual(self.pa.encode('Creg'), 'C94')
        self.assertEqual(self.pa.encode('Cregg'), 'C94')
        self.assertEqual(self.pa.encode('Creag'), 'C94')
        self.assertEqual(self.pa.encode('Greg'), 'G94')
        self.assertEqual(self.pa.encode('Gregg'), 'G94')
        self.assertEqual(self.pa.encode('Graig'), 'G94')
        self.assertEqual(self.pa.encode('Greig'), 'G94')
        self.assertEqual(self.pa.encode('Greggg'), 'G94')
        self.assertEqual(self.pa.encode('Groeg'), 'G94')
        self.assertEqual(self.pa.encode('Graj'), 'G94')
        self.assertEqual(self.pa.encode('Grej'), 'G94')
        self.assertEqual(self.pa.encode('Grreg'), 'G94')
        self.assertEqual(self.pa.encode('Greag'), 'G94')
        self.assertEqual(self.pa.encode('Grig'), 'G94')
        self.assertEqual(self.pa.encode('Kregg'), 'K94')
        self.assertEqual(self.pa.encode('Kraig'), 'K94')
        self.assertEqual(self.pa.encode('Krag'), 'K94')
        self.assertEqual(self.pa.encode('Kreig'), 'K94')
        self.assertEqual(self.pa.encode('Krug'), 'K94')
        self.assertEqual(self.pa.encode('Kreg'), 'K94')
        self.assertEqual(self.pa.encode('Krieg'), 'K94')
        self.assertEqual(self.pa.encode('Krijg'), 'K94')

        # Apache Commons test cases
        # http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/RefinedSoundexTest.java?view=markup
        self.assertEqual(self.pa.encode('testing'), 'T3684')
        self.assertEqual(self.pa.encode('TESTING'), 'T3684')
        self.assertEqual(self.pa.encode('The'), 'T')
        self.assertEqual(self.pa.encode('quick'), 'Q3')
        self.assertEqual(self.pa.encode('brown'), 'B98')
        self.assertEqual(self.pa.encode('fox'), 'F5')
        self.assertEqual(self.pa.encode('jumped'), 'J816')
        self.assertEqual(self.pa.encode('over'), 'O29')
        self.assertEqual(self.pa.encode('the'), 'T')
        self.assertEqual(self.pa.encode('lazy'), 'L5')
        self.assertEqual(self.pa.encode('dogs'), 'D43')

        # Test with retain_vowels=True
        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        pa_vowels = RefinedSoundex(retain_vowels=True)
        self.assertEqual(pa_vowels.encode('Braz'), 'B905')
        self.assertEqual(pa_vowels.encode('Broz'), 'B905')
        self.assertEqual(pa_vowels.encode('Caren'), 'C0908')
        self.assertEqual(pa_vowels.encode('Caron'), 'C0908')
        self.assertEqual(pa_vowels.encode('Carren'), 'C0908')
        self.assertEqual(pa_vowels.encode('Charon'), 'C0908')
        self.assertEqual(pa_vowels.encode('Corain'), 'C0908')
        self.assertEqual(pa_vowels.encode('Coram'), 'C0908')
        self.assertEqual(pa_vowels.encode('Corran'), 'C0908')
        self.assertEqual(pa_vowels.encode('Corrin'), 'C0908')
        self.assertEqual(pa_vowels.encode('Corwin'), 'C0908')
        self.assertEqual(pa_vowels.encode('Curran'), 'C0908')
        self.assertEqual(pa_vowels.encode('Curreen'), 'C0908')
        self.assertEqual(pa_vowels.encode('Currin'), 'C0908')
        self.assertEqual(pa_vowels.encode('Currom'), 'C0908')
        self.assertEqual(pa_vowels.encode('Currum'), 'C0908')
        self.assertEqual(pa_vowels.encode('Curwen'), 'C0908')
        self.assertEqual(pa_vowels.encode('Hairs'), 'H093')
        self.assertEqual(pa_vowels.encode('Hark'), 'H093')
        self.assertEqual(pa_vowels.encode('Hars'), 'H093')
        self.assertEqual(pa_vowels.encode('Hayers'), 'H093')
        self.assertEqual(pa_vowels.encode('Heers'), 'H093')
        self.assertEqual(pa_vowels.encode('Hiers'), 'H093')
        self.assertEqual(pa_vowels.encode('Lambard'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lambart'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lambert'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lambird'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lampaert'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lampard'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lampart'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lamperd'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lampert'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lamport'), 'L081096')
        self.assertEqual(pa_vowels.encode('Limbert'), 'L081096')
        self.assertEqual(pa_vowels.encode('Lombard'), 'L081096')
        self.assertEqual(pa_vowels.encode('Nolton'), 'N07608')
        self.assertEqual(pa_vowels.encode('Noulton'), 'N07608')

        # http://trimc-nlp.blogspot.com/2015/03/the-soundex-algorithm.html
        self.assertEqual(pa_vowels.encode('Craig'), 'C904')
        self.assertEqual(pa_vowels.encode('Crag'), 'C904')
        self.assertEqual(pa_vowels.encode('Crejg'), 'C904')
        self.assertEqual(pa_vowels.encode('Creig'), 'C904')
        self.assertEqual(pa_vowels.encode('Craigg'), 'C904')
        self.assertEqual(pa_vowels.encode('Craug'), 'C904')
        self.assertEqual(pa_vowels.encode('Craiggg'), 'C904')
        self.assertEqual(pa_vowels.encode('Creg'), 'C904')
        self.assertEqual(pa_vowels.encode('Cregg'), 'C904')
        self.assertEqual(pa_vowels.encode('Creag'), 'C904')
        self.assertEqual(pa_vowels.encode('Greg'), 'G904')
        self.assertEqual(pa_vowels.encode('Gregg'), 'G904')
        self.assertEqual(pa_vowels.encode('Graig'), 'G904')
        self.assertEqual(pa_vowels.encode('Greig'), 'G904')
        self.assertEqual(pa_vowels.encode('Greggg'), 'G904')
        self.assertEqual(pa_vowels.encode('Groeg'), 'G904')
        self.assertEqual(pa_vowels.encode('Graj'), 'G904')
        self.assertEqual(pa_vowels.encode('Grej'), 'G904')
        self.assertEqual(pa_vowels.encode('Grreg'), 'G904')
        self.assertEqual(pa_vowels.encode('Greag'), 'G904')
        self.assertEqual(pa_vowels.encode('Grig'), 'G904')
        self.assertEqual(pa_vowels.encode('Kregg'), 'K904')
        self.assertEqual(pa_vowels.encode('Kraig'), 'K904')
        self.assertEqual(pa_vowels.encode('Krag'), 'K904')
        self.assertEqual(pa_vowels.encode('Kreig'), 'K904')
        self.assertEqual(pa_vowels.encode('Krug'), 'K904')
        self.assertEqual(pa_vowels.encode('Kreg'), 'K904')
        self.assertEqual(pa_vowels.encode('Krieg'), 'K904')
        self.assertEqual(pa_vowels.encode('Krijg'), 'K904')

        # Apache Commons test cases
        # http://svn.apache.org/viewvc/commons/proper/codec/trunk/src/test/java/org/apache/commons/codec/language/RefinedSoundexTest.java?view=markup
        self.assertEqual(pa_vowels.encode('testing'), 'T036084')
        self.assertEqual(pa_vowels.encode('TESTING'), 'T036084')
        self.assertEqual(pa_vowels.encode('The'), 'T0')
        self.assertEqual(pa_vowels.encode('quick'), 'Q03')
        self.assertEqual(pa_vowels.encode('brown'), 'B908')
        self.assertEqual(pa_vowels.encode('fox'), 'F05')
        self.assertEqual(pa_vowels.encode('jumped'), 'J08106')
        self.assertEqual(pa_vowels.encode('over'), 'O209')
        self.assertEqual(pa_vowels.encode('the'), 'T0')
        self.assertEqual(pa_vowels.encode('lazy'), 'L050')
        self.assertEqual(pa_vowels.encode('dogs'), 'D043')

        # length tests
        pa_40 = RefinedSoundex(max_length=4, zero_pad=True)
        self.assertEqual(pa_40.encode('testing'), 'T368')
        self.assertEqual(pa_40.encode('TESTING'), 'T368')
        self.assertEqual(pa_40.encode('The'), 'T000')
        self.assertEqual(pa_40.encode('quick'), 'Q300')
        self.assertEqual(pa_40.encode('brown'), 'B980')
        self.assertEqual(pa_40.encode('fox'), 'F500')
        self.assertEqual(pa_40.encode('jumped'), 'J816')
        self.assertEqual(pa_40.encode('over'), 'O290')
        self.assertEqual(pa_40.encode('the'), 'T000')
        self.assertEqual(pa_40.encode('lazy'), 'L500')
        self.assertEqual(pa_40.encode('dogs'), 'D430')
        pa_4 = RefinedSoundex(max_length=4)
        self.assertEqual(pa_4.encode('The'), 'T')
        self.assertEqual(pa_4.encode('quick'), 'Q3')
        self.assertEqual(pa_4.encode('brown'), 'B98')
        self.assertEqual(pa_4.encode('fox'), 'F5')
        self.assertEqual(pa_4.encode('jumped'), 'J816')
        self.assertEqual(pa_4.encode('over'), 'O29')
        self.assertEqual(pa_4.encode('the'), 'T')
        self.assertEqual(pa_4.encode('lazy'), 'L5')
        self.assertEqual(pa_4.encode('dogs'), 'D43')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Broz'), 'BRZ')
        self.assertEqual(self.pa.encode_alpha('Caren'), 'CRN')
        self.assertEqual(self.pa.encode_alpha('Hairs'), 'HRK')
        self.assertEqual(self.pa.encode_alpha('Lamperd'), 'LNPRT')


if __name__ == '__main__':
    unittest.main()
