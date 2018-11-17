# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import RogerRoot, roger_root


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
        self.assertEqual(self.pa.encode('BROWNER', zero_pad=False), '09424')
        self.assertEqual(self.pa.encode('STANLEY', zero_pad=False), '00125')
        self.assertEqual(self.pa.encode('CHALMAN', zero_pad=False), '06532')
        self.assertEqual(self.pa.encode('CHING', zero_pad=False), '0627')
        self.assertEqual(self.pa.encode('ANDERSON', zero_pad=False), '12140')
        self.assertEqual(self.pa.encode('OVERSTREET, zero_pad=False'), '18401')
        self.assertEqual(self.pa.encode('HECKEL', zero_pad=False), '275')
        self.assertEqual(self.pa.encode('WYSZYNSKI', zero_pad=False), '40207')
        self.assertEqual(self.pa.encode('WHITTED', zero_pad=False), '411')
        self.assertEqual(self.pa.encode('ONGOQO', zero_pad=False), '1277')
        self.assertEqual(self.pa.encode('JOHNSON', zero_pad=False), '3202')
        self.assertEqual(self.pa.encode('WILLIAMS', zero_pad=False), '4530')
        self.assertEqual(self.pa.encode('SMITH', zero_pad=False), '0031')
        self.assertEqual(self.pa.encode('JONES', zero_pad=False), '320')
        self.assertEqual(self.pa.encode('BROWN', zero_pad=False), '0942')
        self.assertEqual(self.pa.encode('DAVIS', zero_pad=False), '0180')
        self.assertEqual(self.pa.encode('JACKSON', zero_pad=False), '3702')
        self.assertEqual(self.pa.encode('WILSON', zero_pad=False), '4502')
        self.assertEqual(self.pa.encode('LEE', zero_pad=False), '05')
        self.assertEqual(self.pa.encode('THOMAS', zero_pad=False), '0130')

        # Test wrapper
        self.assertEqual(roger_root('BROWNER'), '09424')


if __name__ == '__main__':
    unittest.main()
