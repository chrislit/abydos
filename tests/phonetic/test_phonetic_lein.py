# -*- coding: utf-8 -*-

# Copyright 2014-2019 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_lein.

This module contains unit tests for abydos.phonetic.LEIN
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import LEIN, lein


class LeinTestCases(unittest.TestCase):
    """Test LEIN functions.

    test cases for abydos.phonetic.LEIN
    """

    pa = LEIN()
    pa_n0 = LEIN(zero_pad=False)

    def test_lein(self):
        """Test abydos.phonetic.LEIN."""
        self.assertEqual(self.pa.encode(''), '0000')

        # https://naldc.nal.usda.gov/download/27833/PDF
        self.assertEqual(self.pa.encode('Dubose'), 'D450')
        self.assertEqual(self.pa.encode('Dubs'), 'D450')
        self.assertEqual(self.pa.encode('Dubbs'), 'D450')
        self.assertEqual(self.pa.encode('Doviak'), 'D450')
        self.assertEqual(self.pa.encode('Dubke'), 'D450')
        self.assertEqual(self.pa.encode('Dubus'), 'D450')
        self.assertEqual(self.pa.encode('Dubois'), 'D450')
        self.assertEqual(self.pa.encode('Duboise'), 'D450')
        self.assertEqual(self.pa.encode('Doubek'), 'D450')
        self.assertEqual(self.pa.encode('Defigh'), 'D450')
        self.assertEqual(self.pa.encode('Defazio'), 'D450')
        self.assertEqual(self.pa.encode('Debaca'), 'D450')
        self.assertEqual(self.pa.encode('Dabbs'), 'D450')
        self.assertEqual(self.pa.encode('Davies'), 'D450')
        self.assertEqual(self.pa.encode('Dubukey'), 'D450')
        self.assertEqual(self.pa.encode('Debus'), 'D450')
        self.assertEqual(self.pa.encode('Debose'), 'D450')
        self.assertEqual(self.pa.encode('Daves'), 'D450')
        self.assertEqual(self.pa.encode('Dipiazza'), 'D450')
        self.assertEqual(self.pa.encode('Dobbs'), 'D450')
        self.assertEqual(self.pa.encode('Dobak'), 'D450')
        self.assertEqual(self.pa.encode('Dobis'), 'D450')
        self.assertEqual(self.pa.encode('Dobish'), 'D450')
        self.assertEqual(self.pa.encode('Doepke'), 'D450')
        self.assertEqual(self.pa.encode('Divish'), 'D450')
        self.assertEqual(self.pa.encode('Dobosh'), 'D450')
        self.assertEqual(self.pa.encode('Dupois'), 'D450')
        self.assertEqual(self.pa.encode('Dufek'), 'D450')
        self.assertEqual(self.pa.encode('Duffek'), 'D450')
        self.assertEqual(self.pa.encode('Dupuis'), 'D450')
        self.assertEqual(self.pa.encode('Dupas'), 'D450')
        self.assertEqual(self.pa.encode('Devese'), 'D450')
        self.assertEqual(self.pa.encode('Devos'), 'D450')
        self.assertEqual(self.pa.encode('Deveaux'), 'D450')
        self.assertEqual(self.pa.encode('Devies'), 'D450')

        self.assertEqual(self.pa.encode('Sand'), 'S210')
        self.assertEqual(self.pa.encode('Sandau'), 'S210')
        self.assertEqual(self.pa.encode('Sande'), 'S210')
        self.assertEqual(self.pa.encode('Sandia'), 'S210')
        self.assertEqual(self.pa.encode('Sando'), 'S210')
        self.assertEqual(self.pa.encode('Sandoe'), 'S210')
        self.assertEqual(self.pa.encode('Sandy'), 'S210')
        self.assertEqual(self.pa.encode('Santee'), 'S210')
        self.assertEqual(self.pa.encode('Santi'), 'S210')
        self.assertEqual(self.pa.encode('Santo'), 'S210')
        self.assertEqual(self.pa.encode('Send'), 'S210')
        self.assertEqual(self.pa.encode('Sennet'), 'S210')
        self.assertEqual(self.pa.encode('Shemoit'), 'S210')
        self.assertEqual(self.pa.encode('Shenot'), 'S210')
        self.assertEqual(self.pa.encode('Shumate'), 'S210')
        self.assertEqual(self.pa.encode('Simmet'), 'S210')
        self.assertEqual(self.pa.encode('Simot'), 'S210')
        self.assertEqual(self.pa.encode('Sineath'), 'S210')
        self.assertEqual(self.pa.encode('Sinnott'), 'S210')
        self.assertEqual(self.pa.encode('Sintay'), 'S210')
        self.assertEqual(self.pa.encode('Smead'), 'S210')
        self.assertEqual(self.pa.encode('Smeda'), 'S210')
        self.assertEqual(self.pa.encode('Smit'), 'S210')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/lein.js
        self.assertEqual(self.pa.encode('Guillaume'), 'G320')
        self.assertEqual(self.pa.encode('Arlène'), 'A332')
        self.assertEqual(self.pa.encode('Lüdenscheidt'), 'L125')

        # Coverage
        self.assertEqual(self.pa_n0.encode('Lüdenscheidt'), 'L125')
        self.assertEqual(self.pa_n0.encode('Smith'), 'S21')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Deveaux'), 'DPK')
        self.assertEqual(self.pa.encode_alpha('Devies'), 'DPK')
        self.assertEqual(self.pa.encode_alpha('Sand'), 'SNT')
        self.assertEqual(self.pa.encode_alpha('Sandau'), 'SNT')

        # Test wrapper
        self.assertEqual(lein('Dubose'), 'D450')


if __name__ == '__main__':
    unittest.main()
