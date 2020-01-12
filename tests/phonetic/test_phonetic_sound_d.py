# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_sound_d.

This module contains unit tests for abydos.phonetic.SoundD
"""

import unittest

from abydos.phonetic import SoundD


class SoundDTestCases(unittest.TestCase):
    """Test class SoundD functions.

    test cases for abydos.phonetic.SoundD
    """

    pa = SoundD()

    def test_sound_d(self):
        """Test abydos.phonetic.SoundD."""
        # Base cases
        self.assertEqual(self.pa.encode(''), '0000')
        self.assertEqual(SoundD(max_length=6).encode(''), '000000')

        self.assertEqual(self.pa.encode('knight'), '5300')
        self.assertEqual(self.pa.encode('accept'), '2130')
        self.assertEqual(self.pa.encode('pneuma'), '5500')
        self.assertEqual(self.pa.encode('ax'), '2000')
        self.assertEqual(self.pa.encode('wherever'), '6160')
        self.assertEqual(self.pa.encode('pox'), '1200')
        self.assertEqual(self.pa.encode('anywhere'), '5600')
        self.assertEqual(self.pa.encode('adenosine'), '3525')
        self.assertEqual(self.pa.encode('judge'), '2200')
        self.assertEqual(self.pa.encode('rough'), '6000')
        self.assertEqual(self.pa.encode('x-ray'), '2600')
        self.assertEqual(
            SoundD(max_length=-1).encode('acetylcholine'), '234245'
        )
        self.assertEqual(SoundD(max_length=-1).encode('rough'), '6')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('pox'), 'PK')
        self.assertEqual(self.pa.encode_alpha('anywhere'), 'NR')
        self.assertEqual(self.pa.encode_alpha('adenosine'), 'TNKN')
        self.assertEqual(self.pa.encode_alpha('judge'), 'KK')


if __name__ == '__main__':
    unittest.main()
