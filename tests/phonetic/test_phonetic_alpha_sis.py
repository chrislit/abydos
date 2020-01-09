# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_alpha_sis.

This module contains unit tests for abydos.phonetic.AlphaSIS
"""

import unittest

from abydos.phonetic import AlphaSIS, alpha_sis


class AlphaSISTestCases(unittest.TestCase):
    """Test Alpha-SIS functions.

    test cases for abydos.phonetic.AlphaSIS
    """

    pa = AlphaSIS()

    def test_alpha_sis_encode(self):
        """Test abydos.phonetic.AlphaSIS."""
        self.assertEqual(self.pa.encode('')[0], '00000000000000')

        self.assertEqual(self.pa.encode('Rodgers')[0], '04740000000000')
        self.assertEqual(self.pa.encode('Rogers')[0], '04740000000000')
        self.assertEqual(self.pa.encode('Kant')[0], '07210000000000')
        self.assertEqual(self.pa.encode('Knuth')[0], '02100000000000')
        self.assertEqual(self.pa.encode('Harper')[0], '24940000000000')
        self.assertEqual(self.pa.encode('Collier')[0], '07540000000000')
        self.assertEqual(self.pa.encode('Schultz')[0], '06500000000000')
        self.assertEqual(self.pa.encode('Livingston')[0], '05827012000000')

        # tests of repeated letters
        self.assertEqual(self.pa.encode('Colllier')[0], '07554000000000')
        self.assertEqual(self.pa.encode('Collllier')[0], '07554000000000')
        self.assertEqual(self.pa.encode('Colllllier')[0], '07555400000000')
        self.assertEqual(self.pa.encode('Collllllier')[0], '07555400000000')
        self.assertEqual(self.pa.encode('Colalalier')[0], '07555400000000')

        # max_length bounds tests
        self.assertEqual(
            AlphaSIS(max_length=-1).encode('Niall')[0],
            '0250000000000000000000000000000000000000000000000000000000000000',
        )
        self.assertEqual(AlphaSIS(max_length=0).encode('Niall')[0], '0250')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Rogers')[0], 'RKR')
        self.assertEqual(self.pa.encode_alpha('Kant')[0], 'KNT')
        self.assertEqual(self.pa.encode_alpha('Knuth')[0], 'NT')
        self.assertEqual(self.pa.encode_alpha('Harper')[0], 'HRPR')

        # Test wrapper
        self.assertEqual(alpha_sis('Livingston')[0], '05827012000000')


if __name__ == '__main__':
    unittest.main()
