# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_waahlin.

This module contains unit tests for abydos.phonetic.Waahlin
"""

import unittest

from abydos.phonetic import Soundex, Waahlin


class WaahlinTestCases(unittest.TestCase):
    """Test Wåhlin functions.

    test cases for abydos.phonetic.Waahlin
    """

    pa = Waahlin()
    pa_sdx = Waahlin(Soundex())

    def test_waahlin(self):
        """Test abydos.phonetic.Waahlin."""
        self.assertEqual(self.pa.encode(''), '')

        self.assertEqual(self.pa.encode('kjol'), '+OL')
        self.assertEqual(self.pa.encode('stråken'), 'STRÅ+EN')
        self.assertEqual(self.pa.encode('skytten'), '*YTTEN')
        self.assertEqual(self.pa.encode('ljuden'), 'JUDEN')
        self.assertEqual(self.pa.encode('högre'), 'HÖGRE')
        self.assertEqual(self.pa.encode('först'), 'FÖRST')
        self.assertEqual(self.pa.encode('hval'), 'VAL')
        self.assertEqual(self.pa.encode('hrothgar'), 'ROTHGAR')
        self.assertEqual(self.pa.encode('denna'), 'DENNA')
        self.assertEqual(self.pa.encode('djur'), 'JUR')
        self.assertEqual(self.pa.encode('hjärta'), 'JERTA')
        self.assertEqual(self.pa.encode('STIEN'), '*EN')
        self.assertEqual(self.pa.encode('SKJERN'), '*ERN')
        self.assertEqual(self.pa.encode('HIELPA'), 'JELPA')
        self.assertEqual(self.pa.encode('CEILA'), 'SEILA')
        self.assertEqual(self.pa.encode('GELD'), 'JELD')
        self.assertEqual(self.pa.encode('IERN'), 'JERN')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('kjol'), 'ÇOL')
        self.assertEqual(self.pa.encode_alpha('stråken'), 'STRÅÇEN')
        self.assertEqual(self.pa.encode_alpha('skytten'), 'ŠYTTEN')
        self.assertEqual(self.pa.encode_alpha('ljuden'), 'JUDEN')

    def test_waahlin_soundex(self):
        """Test abydos.phonetic.Waahlin with Soundex."""
        self.assertEqual(self.pa_sdx.encode(''), '')

        self.assertEqual(self.pa_sdx.encode('kjol'), '+O400')
        self.assertEqual(self.pa_sdx.encode('stråken'), 'ST625')
        self.assertEqual(self.pa_sdx.encode('skytten'), '*Y350')
        self.assertEqual(self.pa_sdx.encode('ljuden'), 'JU350')
        self.assertEqual(self.pa_sdx.encode('högre'), 'HO260')
        self.assertEqual(self.pa_sdx.encode('först'), 'FO623')
        self.assertEqual(self.pa_sdx.encode('hval'), 'VA400')
        self.assertEqual(self.pa_sdx.encode('hrothgar'), 'RO326')
        self.assertEqual(self.pa_sdx.encode('denna'), 'DE500')
        self.assertEqual(self.pa_sdx.encode('djur'), 'JU600')
        self.assertEqual(self.pa_sdx.encode('hjärta'), 'JA630')


if __name__ == '__main__':
    unittest.main()
