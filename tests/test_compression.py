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

from abydos.compression import ac_decode, ac_encode, ac_train, \
    bwt_decode, bwt_encode, rle_decode, rle_encode
from abydos.util import Rational


class ArithmeticCoderTestCases(unittest.TestCase):
    """Test abydos.compression.ac_train & .ac_encode."""

    NIALL = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel',
             'Nele', 'Nigelli', 'Nel', 'Kneale', 'Uí Néill', 'O\'Neill',
             'MacNeil', 'MacNele', 'Niall Noígíallach')

    niall_probs = {'a': (Rational(41, 57), Rational(91, 114)),
                   ' ': (Rational(25, 114), Rational(7, 19)),
                   'c': (Rational(97, 114), Rational(50, 57)),
                   'e': (Rational(29, 57), Rational(73, 114)),
                   "'": (Rational(56, 57), Rational(113, 114)),
                   'g': (Rational(47, 57), Rational(97, 114)),
                   '\x00': (Rational(113, 114), Rational(1, 1)),
                   'i': (Rational(73, 114), Rational(41, 57)),
                   'M': (Rational(17, 19), Rational(52, 57)),
                   'K': (Rational(37, 38), Rational(56, 57)),
                   'j': (Rational(50, 57), Rational(17, 19)),
                   '\xed': (Rational(91, 114), Rational(47, 57)),
                   'l': (Rational(0, 1), Rational(25, 114)),
                   'o': (Rational(53, 57), Rational(107, 114)),
                   'N': (Rational(7, 19), Rational(29, 57)),
                   '\xe9': (Rational(52, 57), Rational(35, 38)),
                   '\xe1': (Rational(35, 38), Rational(53, 57)),
                   'U': (Rational(109, 114), Rational(55, 57)),
                   'O': (Rational(55, 57), Rational(37, 38)),
                   'h': (Rational(18, 19), Rational(109, 114)),
                   'n': (Rational(107, 114), Rational(18, 19))}

    def test_ac_train(self):
        """Test abydos.compression.ac_train."""
        self.assertEqual(ac_train(''), {'\x00': (0, 1)})
        self.assertEqual(ac_train(' '.join(self.NIALL)), self.niall_probs)
        self.assertEqual(ac_train(' '.join(sorted(self.NIALL))),
                         self.niall_probs)
        self.assertEqual(ac_train(' '.join(self.NIALL)),
                         ac_train(' '.join(sorted(self.NIALL))))
        self.assertEqual(ac_train(' '.join(self.NIALL)),
                         ac_train('\x00'.join(self.NIALL)))

    def test_ac_encode(self):
        """Test abydos.compression.ac_encode."""
        self.assertEqual(ac_encode('', self.niall_probs), (254, 8))
        self.assertEqual(ac_encode('a', self.niall_probs), (3268, 12))
        self.assertEqual(ac_encode('Niall', self.niall_probs), (3911665, 23))
        self.assertEqual(ac_encode('Ni\x00ll', self.niall_probs),
                         (1932751, 22))
        self.assertEqual(ac_encode('Niel', self.niall_probs), (486801, 20))
        self.assertEqual(ac_encode('Mean', self.niall_probs), (243067161, 28))
        self.assertEqual(ac_encode('Neil Noígíallach', self.niall_probs),
                         (2133315320471368785758, 72))
        self.assertRaises(KeyError, ac_encode, 'NIALL', self.niall_probs)
        self.assertEqual(ac_encode('', {'\x00': (0, 1)}), (1, 1))

    def test_ac_decode(self):
        """Test abydos.compression.ac_decode."""
        self.assertEqual(ac_decode(254, 8, self.niall_probs), '')
        self.assertEqual(ac_decode(3268, 12, self.niall_probs), 'a')
        self.assertEqual(ac_decode(3911665, 23, self.niall_probs), 'Niall')
        self.assertEqual(ac_decode(1932751, 22, self.niall_probs), 'Ni ll')
        self.assertEqual(ac_decode(486801, 20, self.niall_probs), 'Niel')
        self.assertEqual(ac_decode(243067161, 28, self.niall_probs), 'Mean')
        self.assertEqual(ac_decode(2133315320471368785758, 72,
                                   self.niall_probs), 'Neil Noígíallach')
        self.assertEqual(ac_decode(0, 0, {}), '')
        self.assertEqual(ac_decode(1, 1, {'\x00': (0, 1)}), '')


class BWTTestCases(unittest.TestCase):
    """Test abydos.compression.bwt and .bwt_decode."""

    def test_bwt(self):
        """Test abydos.compression.bwt_encode."""
        # Examples from Wikipedia entry on BWT
        self.assertEqual(bwt_encode(''), '\x00')
        self.assertEqual(bwt_encode('^BANANA', '|'), 'BNN^AA|A')
        self.assertEqual(bwt_encode('SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST' +
                                    '.BOXES', '|'),
                         'TEXYDST.E.IXIXIXXSSMPPS.B..E.|.UESFXDIIOIIITS')

        self.assertEqual(bwt_encode('aardvark', '$'), 'k$avrraad')

        self.assertRaises(ValueError, bwt_encode, 'ABC$', '$')
        self.assertRaises(ValueError, bwt_encode, 'ABC\0')

    def test_bwt_decode(self):
        """Test abydos.compression.bwt_decode."""
        self.assertEqual(bwt_decode(''), '')
        self.assertEqual(bwt_decode('\x00'), '')
        self.assertEqual(bwt_decode('BNN^AA|A', '|'), '^BANANA')
        self.assertEqual(bwt_decode('TEXYDST.E.IXIXIXXSSMPPS.B..E.|.' +
                                    'UESFXDIIOIIITS', '|'),
                         'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES')

        self.assertEqual(bwt_decode('k$avrraad', '$'), 'aardvark')

        self.assertRaises(ValueError, bwt_decode, 'ABC', '$')
        self.assertRaises(ValueError, bwt_decode, 'ABC')

    def test_bwt_roundtripping(self):
        """Test abydos.compression.bwt & .bwt_decode roundtripping."""
        for w in ('', 'Banana', 'The quick brown fox, etc.',
                  'it is better a chylde unborne than untaught',
                  'manners maketh man', 'בְּרֵאשִׁית, בָּרָא אֱלֹהִים',
                  'Ein Rückblick bietet sich folglich an.'):
            self.assertEqual(bwt_decode(bwt_encode(w)), w)
            self.assertEqual(bwt_decode(bwt_encode(w, '$'), '$'), w)


class RLETestCases(unittest.TestCase):
    """Test abydos.compression.rle_encode & .rle_decode."""

    bws = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'

    def test_rle_encode(self):
        """Test abydos.compression.rle_encode."""
        self.assertEqual(rle_encode('', False), '')
        self.assertEqual(rle_encode(''), '\x00')
        self.assertEqual(rle_encode('banana', False), 'banana')
        self.assertEqual(rle_encode('banana'), 'annb\x00aa')
        self.assertEqual(rle_encode(self.bws, False), '12WB12W3B24WB14W')
        self.assertEqual(rle_encode(self.bws), 'WWBWWB45WB\x003WB10WB')
        self.assertEqual(rle_encode('Schifffahrt', False), 'Schi3fahrt')

    def test_rle_decode(self):
        """Test abydos.compression.rle_decode."""
        self.assertEqual(rle_decode('', False), '')
        self.assertEqual(rle_decode('\x00'), '')
        self.assertEqual(rle_decode('banana', False), 'banana')
        self.assertEqual(rle_decode('annb\x00aa'), 'banana')
        self.assertEqual(rle_decode('12WB12W3B24WB14W', False), self.bws)
        self.assertEqual(rle_decode('12W1B12W3B24W1B14W', False), self.bws)
        self.assertEqual(rle_decode('WWBWWB45WB\x003WB10WB'), self.bws)
        self.assertEqual(rle_decode('Schi3fahrt', False), 'Schifffahrt')

    def test_rle_roundtripping(self):
        """Test abydos.compression.rle_encode & .rle_decode roundtripping."""
        self.assertEqual(rle_decode(rle_encode('', False), False), '')
        self.assertEqual(rle_decode(rle_encode('')), '')
        self.assertEqual(rle_decode(rle_encode('banana', False), False),
                         'banana')
        self.assertEqual(rle_decode(rle_encode('banana')), 'banana')
        self.assertEqual(rle_decode(rle_encode(self.bws, False), False),
                         self.bws)
        self.assertEqual(rle_decode(rle_encode(self.bws)), self.bws)
        self.assertEqual(rle_decode(rle_encode('Schifffahrt', False), False),
                         'Schifffahrt')
        self.assertEqual(rle_decode(rle_encode('Schifffahrt')), 'Schifffahrt')


if __name__ == '__main__':
    unittest.main()
