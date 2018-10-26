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

This module contains unit tests for abydos.phonetic._roger_root
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic import roger_root


class RogerRootTestCases(unittest.TestCase):
    """Test Roger Root functions.

    test cases for abydos.phonetic._roger_root.roger_root
    """

    def test_roger_root(self):
        """Test abydos.phonetic._roger_root.roger_root."""
        self.assertEqual(roger_root(''), '00000')

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

        # no zero_pad
        self.assertEqual(roger_root('BROWNER', zero_pad=False), '09424')
        self.assertEqual(roger_root('STANLEY', zero_pad=False), '00125')
        self.assertEqual(roger_root('CHALMAN', zero_pad=False), '06532')
        self.assertEqual(roger_root('CHING', zero_pad=False), '0627')
        self.assertEqual(roger_root('ANDERSON', zero_pad=False), '12140')
        self.assertEqual(roger_root('OVERSTREET, zero_pad=False'), '18401')
        self.assertEqual(roger_root('HECKEL', zero_pad=False), '275')
        self.assertEqual(roger_root('WYSZYNSKI', zero_pad=False), '40207')
        self.assertEqual(roger_root('WHITTED', zero_pad=False), '411')
        self.assertEqual(roger_root('ONGOQO', zero_pad=False), '1277')
        self.assertEqual(roger_root('JOHNSON', zero_pad=False), '3202')
        self.assertEqual(roger_root('WILLIAMS', zero_pad=False), '4530')
        self.assertEqual(roger_root('SMITH', zero_pad=False), '0031')
        self.assertEqual(roger_root('JONES', zero_pad=False), '320')
        self.assertEqual(roger_root('BROWN', zero_pad=False), '0942')
        self.assertEqual(roger_root('DAVIS', zero_pad=False), '0180')
        self.assertEqual(roger_root('JACKSON', zero_pad=False), '3702')
        self.assertEqual(roger_root('WILSON', zero_pad=False), '4502')
        self.assertEqual(roger_root('LEE', zero_pad=False), '05')
        self.assertEqual(roger_root('THOMAS', zero_pad=False), '0130')


if __name__ == '__main__':
    unittest.main()
