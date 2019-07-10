# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.fingerprint.test_fingerprint_bwt_f.

This module contains unit tests for abydos.fingerprint.BWT_F
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.fingerprint import BWT_F


class BWT_FTestCases(unittest.TestCase):
    """Test BWT fingerprint.

    abydos.fingerprint.BWT_F
    """
    bwt = BWT_F()
    bwt_pipe = BWT_F('|')
    bwt_dollar = BWT_F('$')

    def test_consonant_bwt_f(self):
        """Test abydos.fingerprint.BWT_F."""
        # Examples from Wikipedia entry on BWT
        self.assertEqual(self.bwt.fingerprint(''), '\x00')
        self.assertEqual(self.bwt_pipe.fingerprint('^BANANA'), 'BNN^AA|A')
        self.assertEqual(
            self.bwt_pipe.fingerprint(
                'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES'
            ),
            'TEXYDST.E.IXIXIXXSSMPPS.B..E.|.UESFXDIIOIIITS',
        )

        self.assertEqual(self.bwt_dollar.fingerprint('aardvark'), 'k$avrraad')


if __name__ == '__main__':
    unittest.main()
