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

"""abydos.tests.compression.test_compression_arithmetic.

This module contains unit tests for abydos.compression._arithmetic
"""

from __future__ import unicode_literals

import unittest
from fractions import Fraction

from abydos.compression import ac_decode, ac_encode, ac_train

from .. import NIALL


class ArithmeticCoderTestCases(unittest.TestCase):
    """Test abydos.compression._arithmetic.train & ._arithmetic.encode."""

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

    def test_arithmetic_train(self):
        """Test abydos.compression._arithmetic.train."""
        self.assertEqual(ac_train(''), {'\x00': (0, 1)})
        self.assertEqual(ac_train(' '.join(NIALL)), self.niall_probs)
        self.assertEqual(ac_train(' '.join(sorted(NIALL))), self.niall_probs)
        self.assertEqual(
            ac_train(' '.join(NIALL)), ac_train(' '.join(sorted(NIALL)))
        )
        self.assertEqual(ac_train(' '.join(NIALL)), ac_train('\x00'.join(NIALL)))

    def test_arithmetic_encode(self):
        """Test abydos.compression._arithmetic.encode."""
        self.assertEqual(ac_encode('', self.niall_probs), (254, 8))
        self.assertEqual(ac_encode('a', self.niall_probs), (3268, 12))
        self.assertEqual(ac_encode('Niall', self.niall_probs), (3911665, 23))
        self.assertEqual(ac_encode('Ni\x00ll', self.niall_probs), (1932751, 22))
        self.assertEqual(ac_encode('Niel', self.niall_probs), (486801, 20))
        self.assertEqual(ac_encode('Mean', self.niall_probs), (243067161, 28))
        self.assertEqual(
            ac_encode('Neil Noígíallach', self.niall_probs),
            (2133315320471368785758, 72),
        )
        self.assertRaises(KeyError, ac_encode, 'NIALL', self.niall_probs)
        self.assertEqual(ac_encode('', {'\x00': (0, 1)}), (1, 1))

    def test_arithmetic_decode(self):
        """Test abydos.compression._arithmetic.decode."""
        self.assertEqual(ac_decode(254, 8, self.niall_probs), '')
        self.assertEqual(ac_decode(3268, 12, self.niall_probs), 'a')
        self.assertEqual(ac_decode(3911665, 23, self.niall_probs), 'Niall')
        self.assertEqual(ac_decode(1932751, 22, self.niall_probs), 'Ni ll')
        self.assertEqual(ac_decode(486801, 20, self.niall_probs), 'Niel')
        self.assertEqual(ac_decode(243067161, 28, self.niall_probs), 'Mean')
        self.assertEqual(
            ac_decode(2133315320471368785758, 72, self.niall_probs),
            'Neil Noígíallach',
        )
        self.assertEqual(ac_decode(0, 0, {}), '')
        self.assertEqual(ac_decode(1, 1, {'\x00': (0, 1)}), '')


if __name__ == '__main__':
    unittest.main()
