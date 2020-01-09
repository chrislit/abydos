# -*- coding: utf-8 -*-

# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.fingerprint.test_fingerprint_bwtrlef.

This module contains unit tests for abydos.fingerprint.BWTRLEF
"""

import unittest

from abydos.fingerprint import BWTRLEF


class BWTRLEFTestCases(unittest.TestCase):
    """Test BWT+RLE fingerprint.

    abydos.fingerprint.BWTRLEF
    """

    bwtrle = BWTRLEF()

    bws = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'

    def test_consonant_bwtrlef(self):
        """Test abydos.fingerprint.BWTRLEF."""
        # Base case
        self.assertEqual(self.bwtrle.fingerprint(''), '\x00')

        self.assertEqual(self.bwtrle.fingerprint('banana'), 'annb\x00aa')
        self.assertEqual(
            self.bwtrle.fingerprint(self.bws), 'WWBWWB45WB\x003WB10WB'
        )
        self.assertEqual(
            self.bwtrle.fingerprint('Schifffahrt'), 't\x00fSfficahhr'
        )


if __name__ == '__main__':
    unittest.main()
