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

"""abydos.tests.phonetic.test_phonetic_alpha_sis.

This module contains unit tests for abydos.phonetic._alpha_sis
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic import alpha_sis


class AlphaSisTestCases(unittest.TestCase):
    """Test Alpha-SIS functions.

    test cases for abydos.phonetic._alpha_sis
    """

    def test_alpha_sis(self):
        """Test abydos.phonetic._alpha_sis.alpha_sis."""
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

        # max_length bounds tests
        self.assertEqual(
            alpha_sis('Niall', max_length=-1)[0],
            '02500000000000000000000000000000000000000000000000'
            + '00000000000000',
        )
        self.assertEqual(alpha_sis('Niall', max_length=0)[0], '0250')


if __name__ == '__main__':
    unittest.main()
