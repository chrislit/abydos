# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_eudex.

This module contains unit tests for abydos.phonetic.Eudex
"""

import unittest

from abydos.phonetic import Eudex


class EudexTestCases(unittest.TestCase):
    """Test eudex functions.

    test cases for abydos.phonetic.Eudex
    """

    pa = Eudex()

    def test_eudex(self):
        """Test abydos.phonetic.Eudex."""
        # base cases
        self.assertEqual(self.pa.encode(''), '18374686479671623680')
        self.assertEqual(self.pa.encode(' '), '18374686479671623680')

        # exact & mismatch cases from
        # https://github.com/ticki/eudex/blob/master/src/tests.rs
        self.assertEqual(self.pa.encode('JAva'), self.pa.encode('jAva'))
        self.assertEqual(
            self.pa.encode('co!mputer'), self.pa.encode('computer')
        )
        self.assertEqual(
            self.pa.encode('comp-uter'), self.pa.encode('computer')
        )
        self.assertEqual(
            self.pa.encode('comp@u#te?r'), self.pa.encode('computer')
        )
        self.assertEqual(self.pa.encode('lal'), self.pa.encode('lel'))
        self.assertEqual(self.pa.encode('rindom'), self.pa.encode('ryndom'))
        self.assertEqual(
            self.pa.encode('riiiindom'), self.pa.encode('ryyyyyndom')
        )
        self.assertEqual(
            self.pa.encode('riyiyiiindom'), self.pa.encode('ryyyyyndom')
        )
        self.assertEqual(
            self.pa.encode('triggered'), self.pa.encode('TRIGGERED')
        )
        self.assertEqual(self.pa.encode('repert'), self.pa.encode('ropert'))

        self.assertNotEqual(self.pa.encode('reddit'), self.pa.encode('eddit'))
        self.assertNotEqual(self.pa.encode('lol'), self.pa.encode('lulz'))
        self.assertNotEqual(self.pa.encode('ijava'), self.pa.encode('java'))
        self.assertNotEqual(self.pa.encode('jiva'), self.pa.encode('java'))
        self.assertNotEqual(self.pa.encode('jesus'), self.pa.encode('iesus'))
        self.assertNotEqual(self.pa.encode('aesus'), self.pa.encode('iesus'))
        self.assertNotEqual(self.pa.encode('iesus'), self.pa.encode('yesus'))
        self.assertNotEqual(self.pa.encode('rupirt'), self.pa.encode('ropert'))
        self.assertNotEqual(self.pa.encode('ripert'), self.pa.encode('ropyrt'))
        self.assertNotEqual(self.pa.encode('rrr'), self.pa.encode('rraaaa'))
        self.assertNotEqual(
            self.pa.encode('randomal'), self.pa.encode('randomai')
        )

        # manually checked against algorithm
        self.assertEqual(self.pa.encode('guillaume'), '288230383131034112')
        self.assertEqual(self.pa.encode('niall'), '648518346341351840')
        self.assertEqual(self.pa.encode('hello'), '144115188075896832')
        self.assertEqual(self.pa.encode('christopher'), '433648490138894409')
        self.assertEqual(self.pa.encode('colin'), '432345564238053650')


if __name__ == '__main__':
    unittest.main()
