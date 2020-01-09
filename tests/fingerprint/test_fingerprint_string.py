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

"""abydos.tests.fingerprint.test_fingerprint_string_fingerprint.

This module contains unit tests for abydos.fingerprint.String
"""

import unittest

from abydos.fingerprint import String, str_fingerprint

class StringTestCases(unittest.TestCase):
    """Test string fingerprint functions.

    abydos.fingerprint.String
    """

    fp = String()

    _testset = (
        'À noite, vovô Kowalsky vê o ímã cair no pé do pingüim \
queixoso e vovó põe açúcar no chá de tâmaras do jabuti feliz.',
    )
    _anssetw = (
        'a acucar cair cha de do e feliz ima jabuti kowalsky no noite \
o pe pinguim poe queixoso tamaras ve vovo',
    )

    def test_string_fingerprint(self):
        """Test abydos.fingerprint.String."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '')

        for i in range(len(self._testset)):
            self.assertEqual(
                self.fp.fingerprint(self._testset[i]), self._anssetw[i]
            )

        # Test wrapper
        self.assertEqual(str_fingerprint(self._testset[0]), self._anssetw[0])


if __name__ == '__main__':
    unittest.main()
