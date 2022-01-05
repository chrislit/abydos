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

"""abydos.tests.fingerprint.test_fingerprint_occurrence_halved.

This module contains unit tests for abydos.fingerprint.OccurrenceHalved
"""

import unittest

from abydos.fingerprint import OccurrenceHalved


class OccurrenceHalvedFingerprintTestCases(unittest.TestCase):
    """Test Cisłak & Grabowski's occurrence halved fingerprint functions.

    abydos.fingerprint.OccurrenceHalved
    """

    fp = OccurrenceHalved()

    def test_occurrence_halved_fingerprint(self):
        """Test abydos.fingerprint.OccurrenceHalved."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '0' * 16)

        # https://arxiv.org/pdf/1711.08475.pdf
        self.assertEqual(self.fp.fingerprint('instance'), '0110010010111000')

        self.assertEqual(self.fp.fingerprint('inst'), '0001000010100100')
        self.assertEqual(
            OccurrenceHalved(15).fingerprint('instance'), '110010010111000'
        )
        self.assertEqual(
            OccurrenceHalved(32).fingerprint('instance'),
            '01100100101110000000000100000000',
        )
        self.assertEqual(
            OccurrenceHalved(64).fingerprint('instance'),
            f"01100100101110000000000100000000{'0' * 32}",
        )


if __name__ == '__main__':
    unittest.main()
