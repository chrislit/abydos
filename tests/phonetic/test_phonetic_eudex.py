# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

This module contains unit tests for abydos.phonetic.eudex
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.eudex import eudex


class EudexTestCases(unittest.TestCase):
    """Test eudex functions.

    test cases for abydos.phonetic.eudex.eudex
    """

    def test_eudex(self):
        """Test abydos.phonetic.eudex.eudex."""
        # base cases
        self.assertEqual(eudex(''), 18374686479671623680)
        self.assertEqual(eudex(' '), 18374686479671623680)

        # exact & mismatch cases from
        # https://github.com/ticki/eudex/blob/master/src/tests.rs
        self.assertEqual(eudex('JAva'), eudex('jAva'))
        self.assertEqual(eudex('co!mputer'), eudex('computer'))
        self.assertEqual(eudex('comp-uter'), eudex('computer'))
        self.assertEqual(eudex('comp@u#te?r'), eudex('computer'))
        self.assertEqual(eudex('lal'), eudex('lel'))
        self.assertEqual(eudex('rindom'), eudex('ryndom'))
        self.assertEqual(eudex('riiiindom'), eudex('ryyyyyndom'))
        self.assertEqual(eudex('riyiyiiindom'), eudex('ryyyyyndom'))
        self.assertEqual(eudex('triggered'), eudex('TRIGGERED'))
        self.assertEqual(eudex('repert'), eudex('ropert'))

        self.assertNotEqual(eudex('reddit'), eudex('eddit'))
        self.assertNotEqual(eudex('lol'), eudex('lulz'))
        self.assertNotEqual(eudex('ijava'), eudex('java'))
        self.assertNotEqual(eudex('jiva'), eudex('java'))
        self.assertNotEqual(eudex('jesus'), eudex('iesus'))
        self.assertNotEqual(eudex('aesus'), eudex('iesus'))
        self.assertNotEqual(eudex('iesus'), eudex('yesus'))
        self.assertNotEqual(eudex('rupirt'), eudex('ropert'))
        self.assertNotEqual(eudex('ripert'), eudex('ropyrt'))
        self.assertNotEqual(eudex('rrr'), eudex('rraaaa'))
        self.assertNotEqual(eudex('randomal'), eudex('randomai'))

        # manually checked against algorithm
        self.assertEqual(eudex('guillaume'), 288230383131034112)
        self.assertEqual(eudex('niall'), 648518346341351840)
        self.assertEqual(eudex('hello'), 144115188075896832)
        self.assertEqual(eudex('christopher'), 433648490138894409)
        self.assertEqual(eudex('colin'), 432345564238053650)


if __name__ == '__main__':
    unittest.main()
