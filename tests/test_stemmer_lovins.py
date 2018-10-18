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

"""abydos.tests.test_stemmer_lovins.

This module contains unit tests for abydos.stemmer.lovins
"""

from __future__ import unicode_literals

import codecs
import os
import unittest

from abydos.stemmer.lovins import lovins

TESTDIR = os.path.dirname(__file__)


class LovinsTestCases(unittest.TestCase):
    """Test Lovins functions.

    abydos.stemmer.lovins
    """

    def test_lovins(self):
        """Test abydos.stemmer.lovins."""
        # base case
        self.assertEqual(lovins(''), '')

        # test cases from Lovins' "Development of a Stemming Algorithm":
        # http://www.mt-archive.info/MT-1968-Lovins.pdf
        self.assertEqual(lovins('magnesia'), 'magnes')
        self.assertEqual(lovins('magnesite'), 'magnes')
        self.assertEqual(lovins('magnesian'), 'magnes')
        self.assertEqual(lovins('magnesium'), 'magnes')
        self.assertEqual(lovins('magnet'), 'magnet')
        self.assertEqual(lovins('magnetic'), 'magnet')
        self.assertEqual(lovins('magneto'), 'magnet')
        self.assertEqual(lovins('magnetically'), 'magnet')
        self.assertEqual(lovins('magnetism'), 'magnet')
        self.assertEqual(lovins('magnetite'), 'magnet')
        self.assertEqual(lovins('magnetitic'), 'magnet')
        self.assertEqual(lovins('magnetizable'), 'magnet')
        self.assertEqual(lovins('magnetization'), 'magnet')
        self.assertEqual(lovins('magnetize'), 'magnet')
        self.assertEqual(lovins('magnetometer'), 'magnetometer')
        self.assertEqual(lovins('magnetometric'), 'magnetometer')
        self.assertEqual(lovins('magnetometry'), 'magnetometer')
        self.assertEqual(lovins('magnetomotive'), 'magnetomot')
        self.assertEqual(lovins('magnetron'), 'magnetron')
        self.assertEqual(lovins('metal'), 'metal')
        self.assertEqual(lovins('metall'), 'metal')
        self.assertEqual(lovins('metallically'), 'metal')
        self.assertEqual(lovins('metalliferous'), 'metallifer')
        self.assertEqual(lovins('metallize'), 'metal')
        self.assertEqual(lovins('metallurgical'), 'metallurg')
        self.assertEqual(lovins('metallurgy'), 'metallurg')
        self.assertEqual(lovins('induction'), 'induc')
        self.assertEqual(lovins('inductance'), 'induc')
        self.assertEqual(lovins('induced'), 'induc')
        self.assertEqual(lovins('angular'), 'angl')
        self.assertEqual(lovins('angle'), 'angl')

        # missed branch test cases
        self.assertEqual(lovins('feminism'), 'fem')

    def test_lovins_snowball(self):
        """Test abydos.stemmer.lovins (Snowball testset).

        These test cases are from
        https://github.com/snowballstem/snowball-data/tree/master/lovins
        """
        #  Snowball Lovins test set
        with codecs.open(TESTDIR+'/corpora/snowball_lovins.csv',
                         encoding='utf-8') as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(lovins(word), stem.lower())


if __name__ == '__main__':
    unittest.main()
