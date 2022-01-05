# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.compression.test_compression_arithmetic.

This module contains unit tests for abydos.compression.Arithmetic
"""

import unittest
from fractions import Fraction

from abydos.compression import Arithmetic

from .. import NIALL


class ArithmeticCoderTestCases(unittest.TestCase):
    """Test abydos.compression.Arithmetic.train & .Arithmetic.encode."""

    niall_probs = {
        'a': (Fraction(41, 57), Fraction(91, 114)),
        ' ': (Fraction(25, 114), Fraction(7, 19)),
        'c': (Fraction(97, 114), Fraction(50, 57)),
        'e': (Fraction(29, 57), Fraction(73, 114)),
        "'": (Fraction(56, 57), Fraction(113, 114)),
        'g': (Fraction(47, 57), Fraction(97, 114)),
        '\x00': (Fraction(113, 114), Fraction(1, 1)),
        'i': (Fraction(73, 114), Fraction(41, 57)),
        'M': (Fraction(17, 19), Fraction(52, 57)),
        'K': (Fraction(37, 38), Fraction(56, 57)),
        'j': (Fraction(50, 57), Fraction(17, 19)),
        '\xed': (Fraction(91, 114), Fraction(47, 57)),
        'l': (Fraction(0, 1), Fraction(25, 114)),
        'o': (Fraction(53, 57), Fraction(107, 114)),
        'N': (Fraction(7, 19), Fraction(29, 57)),
        '\xe9': (Fraction(52, 57), Fraction(35, 38)),
        '\xe1': (Fraction(35, 38), Fraction(53, 57)),
        'U': (Fraction(109, 114), Fraction(55, 57)),
        'O': (Fraction(55, 57), Fraction(37, 38)),
        'h': (Fraction(18, 19), Fraction(109, 114)),
        'n': (Fraction(107, 114), Fraction(18, 19)),
    }

    coder = Arithmetic()

    def test_arithmetic_train(self):
        """Test abydos.compression.Arithmetic.train."""
        self.coder.train('')
        self.assertEqual(self.coder.get_probs(), {'\x00': (0, 1)})
        self.coder.train(' '.join(NIALL))
        self.assertEqual(self.coder.get_probs(), self.niall_probs)
        self.coder.train(' '.join(sorted(NIALL)))
        self.assertEqual(self.coder.get_probs(), self.niall_probs)

        self.coder.train(' '.join(NIALL))
        niall_probs_new = self.coder.get_probs()
        self.coder.train(' '.join(sorted(NIALL)))
        self.assertEqual(niall_probs_new, self.coder.get_probs())

        self.coder.train('\x00'.join(NIALL))
        self.assertEqual(niall_probs_new, self.coder.get_probs())

    def test_arithmetic_encode(self):
        """Test abydos.compression.Arithmetic.encode."""
        self.coder.set_probs(self.niall_probs)
        self.assertEqual(self.coder.encode(''), (254, 8))
        self.assertEqual(self.coder.encode('a'), (3268, 12))
        self.assertEqual(self.coder.encode('Niall'), (3911665, 23))
        self.assertEqual(self.coder.encode('Ni\x00ll'), (1932751, 22))
        self.assertEqual(self.coder.encode('Niel'), (486801, 20))
        self.assertEqual(self.coder.encode('Mean'), (243067161, 28))
        self.assertEqual(
            self.coder.encode('Neil Noígíallach'), (2133315320471368785758, 72)
        )
        self.assertRaises(KeyError, self.coder.encode, 'NIALL')
        self.coder.set_probs({'\x00': (0, 1)})
        self.assertEqual(self.coder.encode(''), (1, 1))

    def test_arithmetic_decode(self):
        """Test abydos.compression.Arithmetic.decode."""
        self.coder.set_probs(self.niall_probs)
        self.assertEqual(self.coder.decode(254, 8), '')
        self.assertEqual(self.coder.decode(3268, 12), 'a')
        self.assertEqual(self.coder.decode(3911665, 23), 'Niall')
        self.assertEqual(self.coder.decode(1932751, 22), 'Ni ll')
        self.assertEqual(self.coder.decode(486801, 20), 'Niel')
        self.assertEqual(self.coder.decode(243067161, 28), 'Mean')
        self.assertEqual(
            self.coder.decode(2133315320471368785758, 72), 'Neil Noígíallach'
        )
        self.coder.set_probs({})
        self.assertEqual(self.coder.decode(0, 0), '')
        self.coder.set_probs({'\x00': (0, 1)})
        self.assertEqual(self.coder.decode(1, 1), '')


if __name__ == '__main__':
    unittest.main()
