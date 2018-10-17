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

"""abydos.tests.test_fingerprint_lightweight.

This module contains unit tests for abydos.fingerprint.lightweight
"""

from __future__ import unicode_literals

import unittest

from abydos.fingerprint.lightweight import count_fingerprint, \
    occurrence_fingerprint, occurrence_halved_fingerprint, position_fingerprint


class LightweightFingerprintsTestCases(unittest.TestCase):
    """Test Cisłak & Grabowski lightweight fingerprint functions.

    abydos.fingerprint.lightweight.occurrence_fingerprint,
    .occurrence_halved_fingerprint, .count_fingerprint, & .position_fingerprint
    """

    def test_occurrence_fingerprint(self):
        """Test abydos.fingerprint.lightweight.occurrence_fingerprint."""
        # Base case
        self.assertEqual(occurrence_fingerprint(''), 0)

        # https://arxiv.org/pdf/1711.08475.pdf
        self.assertEqual(occurrence_fingerprint('instance'),
                         0b1110111000010000)

        self.assertEqual(occurrence_fingerprint('inst'),
                         0b0100111000000000)
        self.assertEqual(occurrence_fingerprint('instance', 15),
                         0b111011100001000)
        self.assertEqual(occurrence_fingerprint('instance', 32),
                         0b11101110000100000000000000000000)
        self.assertEqual(occurrence_fingerprint('instance', 64),
                         0b11101110000100000000000000000000 << 32)

    def test_occurrence_halved_fingerprint(self):
        """Test abydos.fingerprint.lightweight.occurrence_halved_fingerprint."""  # noqa: E501
        # Base case
        self.assertEqual(occurrence_halved_fingerprint(''), 0)

        # https://arxiv.org/pdf/1711.08475.pdf
        self.assertEqual(occurrence_halved_fingerprint('instance'),
                         0b0110010010111000)

        self.assertEqual(occurrence_halved_fingerprint('inst'),
                         0b0001000010100100)
        self.assertEqual(occurrence_halved_fingerprint('instance', 15),
                         0b0110010010111000)
        self.assertEqual(occurrence_halved_fingerprint('instance', 32),
                         0b01100100101110000000000100000000)
        self.assertEqual(occurrence_halved_fingerprint('instance', 64),
                         0b01100100101110000000000100000000 << 32)

    def test_count_fingerprint(self):
        """Test abydos.fingerprint.lightweight.count_fingerprint."""
        # Base case
        self.assertEqual(count_fingerprint(''), 0)

        # https://arxiv.org/pdf/1711.08475.pdf
        self.assertEqual(count_fingerprint('instance'),
                         0b0101010001100100)

        self.assertEqual(count_fingerprint('inst'),
                         0b0001000001010100)
        self.assertEqual(count_fingerprint('instance', 15),
                         0b0101010001100100)
        self.assertEqual(count_fingerprint('instance', 32),
                         0b01010100011001000000000100000000)
        self.assertEqual(count_fingerprint('instance', 64),
                         0b01010100011001000000000100000000 << 32)

    def test_position_fingerprint(self):
        """Test abydos.fingerprint.lightweight.position_fingerprint."""
        # Base case
        self.assertEqual(position_fingerprint(''),
                         0b1111111111111111)

        # https://arxiv.org/pdf/1711.08475.pdf
        self.assertEqual(position_fingerprint('instance'),
                         0b1110111001110001)

        self.assertEqual(position_fingerprint('instance'),
                         0b1110111001110001)
        self.assertEqual(position_fingerprint('instance', 15),
                         0b111011100111000)
        self.assertEqual(position_fingerprint('instance', 32),
                         0b11101110011100000101011111111111)
        self.assertEqual(position_fingerprint('instance', 64),
                         0xee7057ffefffffff)


if __name__ == '__main__':
    unittest.main()
