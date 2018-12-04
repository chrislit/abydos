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

"""abydos.tests.fingerprint.test_fingerprint_position.

This module contains unit tests for abydos.fingerprint.Position
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.fingerprint import Position, position_fingerprint


class PositionFingerprintTestCases(unittest.TestCase):
    """Test Cisłak & Grabowski's position fingerprint functions.

    abydos.fingerprint.Position
    """

    fp = Position()

    def test_position_fingerprint(self):
        """Test abydos.fingerprint.Position."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), 0b1111111111111111)

        # https://arxiv.org/pdf/1711.08475.pdf
        self.assertEqual(self.fp.fingerprint('instance'), 0b1110111001110001)

        self.assertEqual(self.fp.fingerprint('instance'), 0b1110111001110001)
        self.assertEqual(
            Position(15).fingerprint('instance'), 0b111011100111000
        )
        self.assertEqual(
            Position(32).fingerprint('instance'),
            0b11101110011100000101011111111111,
        )
        self.assertEqual(
            Position(64).fingerprint('instance'), 0xEE7057FFEFFFFFFF
        )

        # Test wrapper
        self.assertEqual(
            position_fingerprint('instance', 32),
            0b11101110011100000101011111111111,
        )


if __name__ == '__main__':
    unittest.main()
