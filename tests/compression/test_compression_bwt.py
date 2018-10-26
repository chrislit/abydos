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

This module contains unit tests for abydos.compression._bwt
"""

from __future__ import unicode_literals

import unittest

from abydos.compression import bwt_decode, bwt_encode


class BWTTestCases(unittest.TestCase):
    """Test abydos.compression._bwt.bwt_encode and bwt_decode."""

    def test_bwt_encode(self):
        """Test abydos.compression._bwt.bwt_encode."""
        # Examples from Wikipedia entry on BWT
        self.assertEqual(bwt_encode(''), '\x00')
        self.assertEqual(bwt_encode('^BANANA', '|'), 'BNN^AA|A')
        self.assertEqual(
            bwt_encode('SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES', '|'),
            'TEXYDST.E.IXIXIXXSSMPPS.B..E.|.UESFXDIIOIIITS',
        )

        self.assertEqual(bwt_encode('aardvark', '$'), 'k$avrraad')

        self.assertRaises(ValueError, bwt_encode, 'ABC$', '$')
        self.assertRaises(ValueError, bwt_encode, 'ABC\0')

    def test_bwt_decode(self):
        """Test abydos.compression._bwt.bwt_decode."""
        self.assertEqual(bwt_decode(''), '')
        self.assertEqual(bwt_decode('\x00'), '')
        self.assertEqual(bwt_decode('BNN^AA|A', '|'), '^BANANA')
        self.assertEqual(
            bwt_decode('TEXYDST.E.IXIXIXXSSMPPS.B..E.|.' + 'UESFXDIIOIIITS', '|'),
            'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES',
        )

        self.assertEqual(bwt_decode('k$avrraad', '$'), 'aardvark')

        self.assertRaises(ValueError, bwt_decode, 'ABC', '$')
        self.assertRaises(ValueError, bwt_decode, 'ABC')

    def test_bwt_roundtripping(self):
        """Test abydos.compression._bwt.bwt_encode & .bwt_decode roundtripping."""  # noqa: E501
        for w in (
            '',
            'Banana',
            'The quick brown fox, etc.',
            'it is better a chylde unborne than untaught',
            'manners maketh man',
            'בְּרֵאשִׁית, בָּרָא אֱלֹהִים',
            'Ein Rückblick bietet sich folglich an.',
        ):
            self.assertEqual(bwt_decode(bwt_encode(w)), w)
            self.assertEqual(bwt_decode(bwt_encode(w, '$'), '$'), w)


if __name__ == '__main__':
    unittest.main()
