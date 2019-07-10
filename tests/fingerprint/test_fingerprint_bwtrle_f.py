# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.fingerprint.test_fingerprint_bwtrle_f.

This module contains unit tests for abydos.fingerprint.BWTRLE_F
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.fingerprint import BWTRLE_F


class BWTRLE_FTestCases(unittest.TestCase):
    """Test BWT+RLE fingerprint.

    abydos.fingerprint.BWTRLE_F
    """
    bwtrle = BWTRLE_F()

    bws = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'

    def test_consonant_bwtrle_f(self):
        """Test abydos.fingerprint.BWTRLE_F."""
        # Base case
        self.assertEqual(self.bwtrle.fingerprint(''), '\x00')

        self.assertEqual(self.bwtrle.fingerprint('banana'), 'annb\x00aa')
        self.assertEqual(
            self.bwtrle.fingerprint(self.bws), 'WWBWWB45WB\x003WB10WB'
        )
        self.assertEqual(self.bwtrle.fingerprint('Schifffahrt'), 't\x00fSfficahhr')


if __name__ == '__main__':
    unittest.main()
