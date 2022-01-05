# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_roger_root.

This module contains unit tests for abydos.phonetic.RogerRoot
"""

import unittest

from abydos.phonetic import RogerRoot


class RogerRootTestCases(unittest.TestCase):
    """Test Roger Root functions.

    test cases for abydos.phonetic.RogerRoot
    """

    pa = RogerRoot()

    def test_roger_root(self):
        """Test abydos.phonetic.RogerRoot."""
        self.assertEqual(self.pa.encode(''), '00000')

        # https://naldc.nal.usda.gov/download/27833/PDF
        self.assertEqual(self.pa.encode('BROWNER'), '09424')
        self.assertEqual(self.pa.encode('STANLEY'), '00125')
        self.assertEqual(self.pa.encode('CHALMAN'), '06532')
        self.assertEqual(self.pa.encode('CHING'), '06270')
        self.assertEqual(self.pa.encode('ANDERSON'), '12140')
        self.assertEqual(self.pa.encode('OVERSTREET'), '18401')
        self.assertEqual(self.pa.encode('HECKEL'), '27500')
        self.assertEqual(self.pa.encode('WYSZYNSKI'), '40207')
        self.assertEqual(self.pa.encode('WHITTED'), '41100')
        self.assertEqual(self.pa.encode('ONGOQO'), '12770')  # PDF had a typo?
        self.assertEqual(self.pa.encode('JOHNSON'), '32020')
        self.assertEqual(self.pa.encode('WILLIAMS'), '45300')
        self.assertEqual(self.pa.encode('SMITH'), '00310')
        self.assertEqual(self.pa.encode('JONES'), '32000')
        self.assertEqual(self.pa.encode('BROWN'), '09420')
        self.assertEqual(self.pa.encode('DAVIS'), '01800')
        self.assertEqual(self.pa.encode('JACKSON'), '37020')
        self.assertEqual(self.pa.encode('WILSON'), '45020')
        self.assertEqual(self.pa.encode('LEE'), '05000')
        self.assertEqual(self.pa.encode('THOMAS'), '01300')

        self.assertEqual(self.pa.encode('Defouw'), '01800')
        self.assertEqual(self.pa.encode('Dauphi'), '01800')
        self.assertEqual(self.pa.encode('Defazio'), '01800')
        self.assertEqual(self.pa.encode('Defay'), '01800')
        self.assertEqual(self.pa.encode('Davy'), '01800')
        self.assertEqual(self.pa.encode('Defee'), '01800')
        self.assertEqual(self.pa.encode('Dayhoff'), '01800')
        self.assertEqual(self.pa.encode('Davie'), '01800')
        self.assertEqual(self.pa.encode('Davey'), '01800')
        self.assertEqual(self.pa.encode('Davies'), '01800')
        self.assertEqual(self.pa.encode('Daves'), '01800')
        self.assertEqual(self.pa.encode('Deife'), '01800')
        self.assertEqual(self.pa.encode('Dehoff'), '01800')
        self.assertEqual(self.pa.encode('Devese'), '01800')
        self.assertEqual(self.pa.encode('Devoe'), '01800')
        self.assertEqual(self.pa.encode('Devee'), '01800')
        self.assertEqual(self.pa.encode('Devies'), '01800')
        self.assertEqual(self.pa.encode('Devos'), '01800')
        self.assertEqual(self.pa.encode('Dafoe'), '01800')
        self.assertEqual(self.pa.encode('Dove'), '01800')
        self.assertEqual(self.pa.encode('Duff'), '01800')
        self.assertEqual(self.pa.encode('Duffey'), '01800')
        self.assertEqual(self.pa.encode('Duffie'), '01800')
        self.assertEqual(self.pa.encode('Duffy'), '01800')
        self.assertEqual(self.pa.encode('Duyava'), '01800')
        self.assertEqual(self.pa.encode('Tafoya'), '01800')
        self.assertEqual(self.pa.encode('Tevis'), '01800')
        self.assertEqual(self.pa.encode('Tiffee'), '01800')
        self.assertEqual(self.pa.encode('Tivis'), '01800')
        self.assertEqual(self.pa.encode('Thevis'), '01800')
        self.assertEqual(self.pa.encode('Tovey'), '01800')
        self.assertEqual(self.pa.encode('Toeves'), '01800')
        self.assertEqual(self.pa.encode('Tuffs'), '01800')

        self.assertEqual(self.pa.encode('Samotid'), '00311')
        self.assertEqual(self.pa.encode('Simmet'), '00310')
        self.assertEqual(self.pa.encode('Simot'), '00310')
        self.assertEqual(self.pa.encode('Smead'), '00310')
        self.assertEqual(self.pa.encode('Smeda'), '00310')
        self.assertEqual(self.pa.encode('Smit'), '00310')
        self.assertEqual(self.pa.encode('Smite'), '00310')
        self.assertEqual(self.pa.encode('Smithe'), '00310')
        self.assertEqual(self.pa.encode('Smithey'), '00310')
        self.assertEqual(self.pa.encode('Smithson'), '00310')
        self.assertEqual(self.pa.encode('Smithy'), '00310')
        self.assertEqual(self.pa.encode('Smoot'), '00310')
        self.assertEqual(self.pa.encode('Smyth'), '00310')
        self.assertEqual(self.pa.encode('Szmodis'), '00310')
        self.assertEqual(self.pa.encode('Zemaitis'), '00310')
        self.assertEqual(self.pa.encode('Zmuda'), '00310')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/roger-root.js
        self.assertEqual(self.pa.encode('Guillaume'), '07530')
        self.assertEqual(self.pa.encode('Arlène'), '14520')
        self.assertEqual(self.pa.encode('Lüdenscheidt'), '05126')

        # no zero_pad
        nzp = RogerRoot(zero_pad=False)
        self.assertEqual(nzp.encode('BROWNER'), '09424')
        self.assertEqual(nzp.encode('STANLEY'), '00125')
        self.assertEqual(nzp.encode('CHALMAN'), '06532')
        self.assertEqual(nzp.encode('CHING'), '0627')
        self.assertEqual(nzp.encode('ANDERSON'), '12140')
        self.assertEqual(nzp.encode('OVERSTREET'), '18401')
        self.assertEqual(nzp.encode('HECKEL'), '275')
        self.assertEqual(nzp.encode('WYSZYNSKI'), '40207')
        self.assertEqual(nzp.encode('WHITTED'), '411')
        self.assertEqual(nzp.encode('ONGOQO'), '1277')
        self.assertEqual(nzp.encode('JOHNSON'), '3202')
        self.assertEqual(nzp.encode('WILLIAMS'), '4530')
        self.assertEqual(nzp.encode('SMITH'), '0031')
        self.assertEqual(nzp.encode('JONES'), '320')
        self.assertEqual(nzp.encode('BROWN'), '0942')
        self.assertEqual(nzp.encode('DAVIS'), '0180')
        self.assertEqual(nzp.encode('JACKSON'), '3702')
        self.assertEqual(nzp.encode('WILSON'), '4502')
        self.assertEqual(nzp.encode('LEE'), '05')
        self.assertEqual(nzp.encode('THOMAS'), '0130')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('BROWNER'), 'PRNR')
        self.assertEqual(self.pa.encode_alpha('STANLEY'), 'STNL')
        self.assertEqual(self.pa.encode_alpha('CHALMAN'), 'JLMN')
        self.assertEqual(self.pa.encode_alpha('CHING'), 'JNK')


if __name__ == '__main__':
    unittest.main()
