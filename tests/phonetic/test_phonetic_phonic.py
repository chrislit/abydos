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

"""abydos.tests.phonetic.test_phonetic_phonic.

This module contains unit tests for abydos.phonetic.PHONIC
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import PHONIC


class PHONICTestCases(unittest.TestCase):
    """Test PHONIC functions.

    test cases for abydos.phonetic.PHONIC
    """

    pa = PHONIC()

    def test_phonic(self):
        """Test abydos.phonetic.PHONIC."""
        self.assertEqual(self.pa.encode(''), '0000')

        # test case from paper
        self.assertEqual(self.pa.encode('Phillips'), 'P8590')

        # coverage
        self.assertEqual(
            PHONIC(max_length=-1, zero_pad=False, extended=True).encode(
                'Phillips'
            ),
            '8590',
        )
        self.assertEqual(
            PHONIC(max_length=-1, zero_pad=False, extended=True).encode_alpha(
                'Phillips'
            ),
            'FLPS',
        )


if __name__ == '__main__':
    unittest.main()
