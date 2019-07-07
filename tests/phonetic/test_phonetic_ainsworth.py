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

"""abydos.tests.phonetic.test_phonetic_ainsworth.

This module contains unit tests for abydos.phonetic.Ainsworth
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import Ainsworth


class AinsworthTestCases(unittest.TestCase):
    """Test Ainsworth functions.

    test cases for abydos.phonetic.Ainsworth
    """

    pa = Ainsworth()

    def test_ainsworth_encode(self):
        """Test abydos.phonetic.Ainsworth.encode"""
        self.assertEqual(self.pa.encode(''), '')

        self.assertEqual(self.pa.encode('a'), 'ə')
        self.assertEqual(self.pa.encode('I'), 'ɑi')
        self.assertEqual(self.pa.encode('there'), 'ðɛə')
        self.assertEqual(self.pa.encode('winning'), 'wɪnnɪŋg')
        self.assertEqual(self.pa.encode('Daniel'), 'dænɑiɛl')
        self.assertEqual(self.pa.encode('row'), 'rɑʊ')
        self.assertEqual(self.pa.encode('dole'), 'doəl')
        self.assertEqual(self.pa.encode('retired'), 'rɛtɜɛd')
        self.assertEqual(self.pa.encode('Ainsworth'), 'ɛiɪnswɜrð')
        self.assertEqual(self.pa.encode('snap'), 'snæp')
        self.assertEqual(self.pa.encode('spinned'), 'spɪnnɛd')
        self.assertEqual(self.pa.encode('zoo'), 'zu')
        self.assertEqual(self.pa.encode('ooze'), 'uz')
        self.assertEqual(self.pa.encode('parallelogram'), 'pɑɔlɛlogræm')


if __name__ == '__main__':
    unittest.main()
