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

This module contains unit tests for abydos.compression.BWT
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.compression import BWT, bwt_decode, bwt_encode


class BWTTestCases(unittest.TestCase):
    """Test abydos.compression.BWT.encode and .decode."""

    coder = BWT()
    coder_pipe = BWT('|')
    coder_dollar = BWT('$')

    def test_bwt_encode(self):
        """Test abydos.compression.BWT.encode."""
        # Examples from Wikipedia entry on BWT
        self.assertEqual(self.coder.encode(''), '\x00')
        self.assertEqual(self.coder_pipe.encode('^BANANA'), 'BNN^AA|A')
        self.assertEqual(
            self.coder_pipe.encode(
                'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES'
            ),
            'TEXYDST.E.IXIXIXXSSMPPS.B..E.|.UESFXDIIOIIITS',
        )

        self.assertEqual(self.coder_dollar.encode('aardvark'), 'k$avrraad')

        self.assertRaises(ValueError, self.coder_dollar.encode, 'ABC$')
        self.assertRaises(ValueError, self.coder.encode, 'ABC\0')

        # Test wrapper
        self.assertEqual(bwt_encode('aardvark', '$'), 'k$avrraad')

    def test_bwt_decode(self):
        """Test abydos.compression.BWT.decode."""
        self.assertEqual(self.coder.decode(''), '')
        self.assertEqual(self.coder.decode('\x00'), '')
        self.assertEqual(self.coder_pipe.decode('BNN^AA|A'), '^BANANA')
        self.assertEqual(
            self.coder_pipe.decode(
                'TEXYDST.E.IXIXIXXSSMPPS.B..E.|.UESFXDIIOIIITS'
            ),
            'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES',
        )

        self.assertEqual(self.coder_dollar.decode('k$avrraad'), 'aardvark')

        self.assertRaises(ValueError, self.coder_dollar.decode, 'ABC')
        self.assertRaises(ValueError, self.coder.decode, 'ABC')

        # Test wrapper
        self.assertEqual(bwt_decode('BNN^AA|A', '|'), '^BANANA')

    def test_bwt_roundtripping(self):
        """Test abydos.compression.BWT.encode & .decode roundtripping."""
        for w in (
            '',
            'Banana',
            'The quick brown fox, etc.',
            'it is better a chylde unborne than untaught',
            'manners maketh man',
            'בְּרֵאשִׁית, בָּרָא אֱלֹהִים',
            'Ein Rückblick bietet sich folglich an.',
        ):
            self.assertEqual(self.coder.decode(self.coder.encode(w)), w)
            self.assertEqual(
                self.coder_dollar.decode(self.coder_dollar.encode(w)), w
            )


if __name__ == '__main__':
    unittest.main()
