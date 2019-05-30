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

"""abydos.tests.fingerprint.test_fingerprint_count.

This module contains unit tests for abydos.fingerprint.Count
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.fingerprint import Count, count_fingerprint


class CountFingerprintTestCases(unittest.TestCase):
    """Test Cisłak & Grabowski's count fingerprint functions.

    abydos.fingerprint.Count
    """

    fp = Count()

    def test_count_fingerprint(self):
        """Test abydos.fingerprint.Count."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), 0)

        # https://arxiv.org/pdf/1711.08475.pdf
        self.assertEqual(self.fp.fingerprint('instance'), 0b0101010001100100)

        self.assertEqual(self.fp.fingerprint('inst'), 0b0001000001010100)
        self.assertEqual(Count(15).fingerprint('instance'), 0b0101010001100100)
        self.assertEqual(
            Count(32).fingerprint('instance'),
            0b01010100011001000000000100000000,
        )
        self.assertEqual(
            Count(64).fingerprint('instance'),
            0b01010100011001000000000100000000 << 32,
        )

        # Test wrapper
        self.assertEqual(
            count_fingerprint('instance', 32),
            0b01010100011001000000000100000000,
        )


if __name__ == '__main__':
    unittest.main()
