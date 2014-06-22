# -*- coding: utf-8 -*-
"""abydos.tests.test_phones

This module contains unit tests for abydos.phones

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
import unittest
from abydos.phones import ipa_to_features


class IpaFeaturesTestCases(unittest.TestCase):
    """test cases for abydos.phones.ipa_to_features
    """
    def test_ipa_to_features(self):
        """test abydos.phones.ipa_to_features
        """
        self.assertEqual(ipa_to_features('medçen'),
                         [24636469832361, 41129052826026, 29161217878698,
                          29164281833898, 41129052826026, 24763171367593])
        self.assertEqual(ipa_to_features('axtuŋ'),
                         [41129037162922, 29171793832362, 29161217895082,
                          41060262046122, 24773747305129])
        self.assertEqual(ipa_to_features('iç'),
                         [41128985717162, 29164281833898])
        self.assertEqual(ipa_to_features('bakofen'),
                         [29034516343466, 41129037162922, 29171793832618,
                          41060329154986, 29034516359594, 41129052826026,
                          24763171367593])
        self.assertEqual(ipa_to_features('dʒuŋel'),
                         [29164281817702, 41060262046122, 24773747305129,
                          41129052826026, 24763171367322])
        self.assertEqual(ipa_to_features('kvatʃ'),
                         [29171793832618, 29034516343210, 41129037162922,
                          29164281834086])
        self.assertEqual(ipa_to_features('nitʃe'),
                         [24763171367593, 41128985717162, 29164281834086,
                          41129052826026])
        self.assertEqual(ipa_to_features('klø'),
                         [29171793832618, 24763171367322, 41060333349290])
        self.assertEqual(ipa_to_features('kybax'),
                         [29171793832618, 41060266240426, 29034516343466,
                          41129037162922, 29171793832362])
        self.assertEqual(ipa_to_features('i@c'),
                         [41128985717162, -1, 29164281834154])

if __name__ == '__main__':
    unittest.main()
