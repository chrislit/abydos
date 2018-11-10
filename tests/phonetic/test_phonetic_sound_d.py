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

"""abydos.tests.phonetic.test_phonetic_sound_d.

This module contains unit tests for abydos.phonetic._sound_d
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import sound_d


class SoundDTestCases(unittest.TestCase):
    """Test class SoundD functions.

    test cases for abydos.phonetic._sound_d.sound_d
    """

    def test_sound_d(self):
        """Test abydos.phonetic._sound_d.sound_d."""
        # Base cases
        self.assertEqual(sound_d(''), '0000')
        self.assertEqual(sound_d('', max_length=6), '000000')

        self.assertEqual(sound_d('knight'), '5300')
        self.assertEqual(sound_d('accept'), '2130')
        self.assertEqual(sound_d('pneuma'), '5500')
        self.assertEqual(sound_d('ax'), '2000')
        self.assertEqual(sound_d('wherever'), '6160')
        self.assertEqual(sound_d('pox'), '1200')
        self.assertEqual(sound_d('anywhere'), '5600')
        self.assertEqual(sound_d('adenosine'), '3525')
        self.assertEqual(sound_d('judge'), '2200')
        self.assertEqual(sound_d('rough'), '6000')
        self.assertEqual(sound_d('x-ray'), '2600')
        self.assertEqual(sound_d('acetylcholine', max_length=-1), '234245')
        self.assertEqual(sound_d('rough', max_length=-1), '6')


if __name__ == '__main__':
    unittest.main()
