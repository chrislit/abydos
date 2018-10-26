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

"""abydos.tests.compression.test_compression_bwt.

This module contains unit tests for abydos.compression.bwt
"""

from __future__ import unicode_literals

import unittest

from abydos.compression.bwt import decode, encode


class BWTTestCases(unittest.TestCase):
    """Test abydos.compression.bwt.encode and .decode."""

    def test_bwt_encode(self):
        """Test abydos.compression.bwt.encode."""
        # Examples from Wikipedia entry on BWT
        self.assertEqual(encode(''), '\x00')
        self.assertEqual(encode('^BANANA', '|'), 'BNN^AA|A')
        self.assertEqual(
            encode('SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES', '|'),
            'TEXYDST.E.IXIXIXXSSMPPS.B..E.|.UESFXDIIOIIITS',
        )

        self.assertEqual(encode('aardvark', '$'), 'k$avrraad')

        self.assertRaises(ValueError, encode, 'ABC$', '$')
        self.assertRaises(ValueError, encode, 'ABC\0')

    def test_bwt_decode(self):
        """Test abydos.compression.bwt.decode."""
        self.assertEqual(decode(''), '')
        self.assertEqual(decode('\x00'), '')
        self.assertEqual(decode('BNN^AA|A', '|'), '^BANANA')
        self.assertEqual(
            decode('TEXYDST.E.IXIXIXXSSMPPS.B..E.|.' + 'UESFXDIIOIIITS', '|'),
            'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES',
        )

        self.assertEqual(decode('k$avrraad', '$'), 'aardvark')

        self.assertRaises(ValueError, decode, 'ABC', '$')
        self.assertRaises(ValueError, decode, 'ABC')

    def test_bwt_roundtripping(self):
        """Test abydos.compression.bwt.encode & .decode roundtripping."""
        for w in (
            '',
            'Banana',
            'The quick brown fox, etc.',
            'it is better a chylde unborne than untaught',
            'manners maketh man',
            'בְּרֵאשִׁית, בָּרָא אֱלֹהִים',
            'Ein Rückblick bietet sich folglich an.',
        ):
            self.assertEqual(decode(encode(w)), w)
            self.assertEqual(decode(encode(w, '$'), '$'), w)


if __name__ == '__main__':
    unittest.main()
