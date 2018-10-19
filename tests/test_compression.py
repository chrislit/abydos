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

"""abydos.tests.test_compression.

This module contains unit tests for abydos.compression
"""

from __future__ import unicode_literals

import unittest
from fractions import Fraction

from abydos.compression import arithmetic, bwt, rle

from . import NIALL


class ArithmeticCoderTestCases(unittest.TestCase):
    """Test abydos.compression.arithmetic.train & .arithmetic.encode."""

    niall_probs = {'a': (Fraction(41, 57), Fraction(91, 114)),
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
                   'n': (Fraction(107, 114), Fraction(18, 19))}

    def test_arithmetic_train(self):
        """Test abydos.compression.arithmetic.train."""
        self.assertEqual(arithmetic.train(''), {'\x00': (0, 1)})
        self.assertEqual(arithmetic.train(' '.join(NIALL)),
                         self.niall_probs)
        self.assertEqual(arithmetic.train(' '.join(sorted(NIALL))),
                         self.niall_probs)
        self.assertEqual(arithmetic.train(' '.join(NIALL)),
                         arithmetic.train(' '.join(sorted(NIALL))))
        self.assertEqual(arithmetic.train(' '.join(NIALL)),
                         arithmetic.train('\x00'.join(NIALL)))

    def test_arithmetic_encode(self):
        """Test abydos.compression.arithmetic.encode."""
        self.assertEqual(arithmetic.encode('', self.niall_probs), (254, 8))
        self.assertEqual(arithmetic.encode('a', self.niall_probs), (3268, 12))
        self.assertEqual(arithmetic.encode('Niall', self.niall_probs),
                         (3911665, 23))
        self.assertEqual(arithmetic.encode('Ni\x00ll', self.niall_probs),
                         (1932751, 22))
        self.assertEqual(arithmetic.encode('Niel', self.niall_probs),
                         (486801, 20))
        self.assertEqual(arithmetic.encode('Mean', self.niall_probs),
                         (243067161, 28))
        self.assertEqual(arithmetic.encode('Neil Noígíallach',
                                           self.niall_probs),
                         (2133315320471368785758, 72))
        self.assertRaises(KeyError, arithmetic.encode, 'NIALL',
                          self.niall_probs)
        self.assertEqual(arithmetic.encode('', {'\x00': (0, 1)}), (1, 1))

    def test_arithmetic_decode(self):
        """Test abydos.compression.arithmetic.decode."""
        self.assertEqual(arithmetic.decode(254, 8, self.niall_probs), '')
        self.assertEqual(arithmetic.decode(3268, 12, self.niall_probs), 'a')
        self.assertEqual(arithmetic.decode(3911665, 23, self.niall_probs),
                         'Niall')
        self.assertEqual(arithmetic.decode(1932751, 22, self.niall_probs),
                         'Ni ll')
        self.assertEqual(arithmetic.decode(486801, 20, self.niall_probs),
                         'Niel')
        self.assertEqual(arithmetic.decode(243067161, 28, self.niall_probs),
                         'Mean')
        self.assertEqual(arithmetic.decode(2133315320471368785758, 72,
                                           self.niall_probs),
                         'Neil Noígíallach')
        self.assertEqual(arithmetic.decode(0, 0, {}), '')
        self.assertEqual(arithmetic.decode(1, 1, {'\x00': (0, 1)}), '')


class BWTTestCases(unittest.TestCase):
    """Test abydos.compression.bwt.encode and .decode."""

    def test_bwt_encode(self):
        """Test abydos.compression.bwt.encode."""
        # Examples from Wikipedia entry on BWT
        self.assertEqual(bwt.encode(''), '\x00')
        self.assertEqual(bwt.encode('^BANANA', '|'), 'BNN^AA|A')
        self.assertEqual(bwt.encode('SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST' +
                                    '.BOXES', '|'),
                         'TEXYDST.E.IXIXIXXSSMPPS.B..E.|.UESFXDIIOIIITS')

        self.assertEqual(bwt.encode('aardvark', '$'), 'k$avrraad')

        self.assertRaises(ValueError, bwt.encode, 'ABC$', '$')
        self.assertRaises(ValueError, bwt.encode, 'ABC\0')

    def test_bwt_decode(self):
        """Test abydos.compression.bwt.decode."""
        self.assertEqual(bwt.decode(''), '')
        self.assertEqual(bwt.decode('\x00'), '')
        self.assertEqual(bwt.decode('BNN^AA|A', '|'), '^BANANA')
        self.assertEqual(bwt.decode('TEXYDST.E.IXIXIXXSSMPPS.B..E.|.' +
                                    'UESFXDIIOIIITS', '|'),
                         'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES')

        self.assertEqual(bwt.decode('k$avrraad', '$'), 'aardvark')

        self.assertRaises(ValueError, bwt.decode, 'ABC', '$')
        self.assertRaises(ValueError, bwt.decode, 'ABC')

    def test_bwt_roundtripping(self):
        """Test abydos.compression.bwt.encode & .decode roundtripping."""
        for w in ('', 'Banana', 'The quick brown fox, etc.',
                  'it is better a chylde unborne than untaught',
                  'manners maketh man', 'בְּרֵאשִׁית, בָּרָא אֱלֹהִים',
                  'Ein Rückblick bietet sich folglich an.'):
            self.assertEqual(bwt.decode(bwt.encode(w)), w)
            self.assertEqual(bwt.decode(bwt.encode(w, '$'), '$'), w)


class RLETestCases(unittest.TestCase):
    """Test abydos.compression.rle.encode & .decode."""

    bws = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'

    def test_rle_encode(self):
        """Test abydos.compression.rle.encode."""
        self.assertEqual(rle.encode('', False), '')
        self.assertEqual(rle.encode(''), '\x00')
        self.assertEqual(rle.encode('banana', False), 'banana')
        self.assertEqual(rle.encode('banana'), 'annb\x00aa')
        self.assertEqual(rle.encode(self.bws, False), '12WB12W3B24WB14W')
        self.assertEqual(rle.encode(self.bws), 'WWBWWB45WB\x003WB10WB')
        self.assertEqual(rle.encode('Schifffahrt', False), 'Schi3fahrt')

    def test_rle_decode(self):
        """Test abydos.compression.rle.decode."""
        self.assertEqual(rle.decode('', False), '')
        self.assertEqual(rle.decode('\x00'), '')
        self.assertEqual(rle.decode('banana', False), 'banana')
        self.assertEqual(rle.decode('annb\x00aa'), 'banana')
        self.assertEqual(rle.decode('12WB12W3B24WB14W', False), self.bws)
        self.assertEqual(rle.decode('12W1B12W3B24W1B14W', False), self.bws)
        self.assertEqual(rle.decode('WWBWWB45WB\x003WB10WB'), self.bws)
        self.assertEqual(rle.decode('Schi3fahrt', False), 'Schifffahrt')

    def test_rle_roundtripping(self):
        """Test abydos.compression.rle.encode & .decode roundtripping."""
        self.assertEqual(rle.decode(rle.encode('', False), False), '')
        self.assertEqual(rle.decode(rle.encode('')), '')
        self.assertEqual(rle.decode(rle.encode('banana', False), False),
                         'banana')
        self.assertEqual(rle.decode(rle.encode('banana')), 'banana')
        self.assertEqual(rle.decode(rle.encode(self.bws, False), False),
                         self.bws)
        self.assertEqual(rle.decode(rle.encode(self.bws)), self.bws)
        self.assertEqual(rle.decode(rle.encode('Schifffahrt', False), False),
                         'Schifffahrt')
        self.assertEqual(rle.decode(rle.encode('Schifffahrt')), 'Schifffahrt')


if __name__ == '__main__':
    unittest.main()
