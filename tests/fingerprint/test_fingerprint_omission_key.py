# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.fingerprint.test_fingerprint_omission_key.

This module contains unit tests for abydos.fingerprint.OmissionKey
"""

import unittest

from abydos.fingerprint import OmissionKey


class OmissionKeyTestCases(unittest.TestCase):
    """Test OmissionKey functions.

    abydos.fingerprint.OmissionKey
    """

    fp = OmissionKey()

    def test_omission_key(self):
        """Test abydos.fingerprint.OmissionKey."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '')

        # http://dl.acm.org/citation.cfm?id=358048
        self.assertEqual(self.fp.fingerprint('microelectronics'), 'MCLNTSRIOE')
        self.assertEqual(self.fp.fingerprint('circumstantial'), 'MCLNTSRIUA')
        self.assertEqual(self.fp.fingerprint('luminescent'), 'MCLNTSUIE')
        self.assertEqual(self.fp.fingerprint('multinucleate'), 'MCLNTUIEA')
        self.assertEqual(self.fp.fingerprint('multinucleon'), 'MCLNTUIEO')
        self.assertEqual(self.fp.fingerprint('cumulene'), 'MCLNUE')
        self.assertEqual(self.fp.fingerprint('luminance'), 'MCLNUIAE')
        self.assertEqual(self.fp.fingerprint('coelomic'), 'MCLOEI')
        self.assertEqual(self.fp.fingerprint('molecule'), 'MCLOEU')
        self.assertEqual(self.fp.fingerprint('cameral'), 'MCLRAE')
        self.assertEqual(self.fp.fingerprint('caramel'), 'MCLRAE')
        self.assertEqual(self.fp.fingerprint('maceral'), 'MCLRAE')
        self.assertEqual(self.fp.fingerprint('lacrimal'), 'MCLRAI')


if __name__ == '__main__':
    unittest.main()
