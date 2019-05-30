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

"""abydos.tests.fingerprint.test_fingerprint_phonetic_fingerprint.

This module contains unit tests for abydos.fingerprint.Phonetic
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.fingerprint import Phonetic, phonetic_fingerprint
from abydos.phonetic import Phonet, Soundex


from .. import NIALL


class PhoneticTestCases(unittest.TestCase):
    """Test phonetic fingerprint functions.

    abydos.fingerprint.Phonetic
    """

    fp = Phonetic()
    fp_phonet = Phonetic(Phonet())
    fp_soundex = Phonetic(Soundex())
    soundex = Soundex()

    def test_phonetic_fingerprint(self):
        """Test abydos.fingerprint.Phonetic."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '')

        self.assertEqual(
            self.fp.fingerprint(' '.join(NIALL)), 'a anl mknl njl nklk nl'
        )
        self.assertEqual(
            self.fp_phonet.fingerprint(' '.join(NIALL)),
            'knile makneil maknele neil nel nele nial nigeli '
            + 'nigl nil noigialach oneil ui',
        )
        self.assertEqual(
            self.fp_soundex.fingerprint(' '.join(NIALL)),
            'k540 m254 n240 n242 n400 o540 u000',
        )

        # Test wrapper
        self.assertEqual(
            phonetic_fingerprint(' '.join(NIALL), self.soundex.encode),
            'k540 m254 n240 n242 n400 o540 u000',
        )


if __name__ == '__main__':
    unittest.main()
