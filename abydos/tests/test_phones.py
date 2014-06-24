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
from abydos.phones import ipa_to_features, has_feature
from math import isnan


class IpaFeaturesTestCases(unittest.TestCase):
    """test cases for abydos.phones.ipa_to_features
    """
    def test_ipa_to_features(self):
        """test abydos.phones.ipa_to_features
        """
        self.assertEqual(ipa_to_features('medçen'),
                         [24652843543209, 41145158953386, 29367643892394,
                          29370440460714, 41145158953386, 24969597381289])
        self.assertEqual(ipa_to_features('axtuŋ'),
                         [41145143290282, 29394058586538, 29367643908778,
                          41076368173482, 24996012059305])
        self.assertEqual(ipa_to_features('iç'),
                         [41145091844522, 29370440460714])
        self.assertEqual(ipa_to_features('bakofen'),
                         [29050890054314, 41145143290282, 29394058586794,
                          41076435282346, 29050890070442, 41145158953386,
                          24969597381289])
        self.assertEqual(ipa_to_features('dʒuŋel'),
                         [29370440444518, 41076368173482, 24996012059305,
                          41145158953386, 24969597381018])
        self.assertEqual(ipa_to_features('kvatʃ'),
                         [29394058586794, 29050890054058, 41145143290282,
                          29370440460902])
        self.assertEqual(ipa_to_features('nitʃe'),
                         [24969597381289, 41145091844522, 29370440460902,
                          41145158953386])
        self.assertEqual(ipa_to_features('klø'),
                         [29394058586794, 24969597381018, 41076439476650])
        self.assertEqual(ipa_to_features('kybax'),
                         [29394058586794, 41076372367786, 29050890054314,
                          41145143290282, 29394058586538])
        self.assertEqual(ipa_to_features('i@c'),
                         [41145091844522, -1, 29370440460970])


class HasFeatureTestCases(unittest.TestCase):
    """test cases for abydos.phones.has_feature
    """
    def test_ipa_to_features(self):
        """test abydos.phones.has_feature
        """
        self.assertEqual(has_feature(ipa_to_features('medçen'), 'nasal'),
                         [1, -1, -1, -1, -1, 1])
        self.assertEqual(has_feature(ipa_to_features('nitʃe'), 'nasal'),
                         [1, -1, -1, -1])
        self.assertEqual(has_feature(ipa_to_features('nitʃe'), 'strident'),
                         [-1, -1, 1, -1])
        self.assertEqual(has_feature(ipa_to_features('nitʃe'), 'syllabic'),
                         [-1, 1, -1, 1])
        self.assertRaises(AttributeError, has_feature, ipa_to_features('nitʃe'),
                          'vocalic')
        self.assertEqual(has_feature(ipa_to_features('medçen'), 'nasal', True),
                         [1, 0, 0, 0, 0, 1])
        self.assertEqual(has_feature(ipa_to_features('nitʃe'), 'nasal', True),
                         [1, 0, 0, 0])
        self.assertEqual(has_feature(ipa_to_features('nitʃe'), 'strident',
                                     True), [0, 0, 1, 0])
        self.assertEqual(has_feature(ipa_to_features('nitʃe'), 'syllabic',
                                     True), [0, 1, 0, 1])
        self.assertRaises(AttributeError, has_feature, ipa_to_features('nitʃe'),
                          'vocalic', True)
        self.assertEqual(has_feature(ipa_to_features('løvenbroy'), 'ATR',),
                         [0, 1, 0, 1, 0, 0, 0, 1, 1])
        self.assertNotEqual(has_feature(ipa_to_features('i@c'), 'syllabic'),
                            [1, float('NaN'), -1])
        self.assertTrue(isnan(has_feature(ipa_to_features('i@c'),
                                              'syllabic')[1]))


if __name__ == '__main__':
    unittest.main()
