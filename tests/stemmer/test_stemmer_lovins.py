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

"""abydos.tests.stemmer.test_stemmer_lovins.

This module contains unit tests for abydos.stemmer.Lovins
"""

import codecs
import unittest

from abydos.stemmer import Lovins

from .. import _corpus_file


class LovinsTestCases(unittest.TestCase):
    """Test Lovins functions.

    abydos.stemmer.Lovins
    """

    stmr = Lovins()

    def test_lovins(self):
        """Test abydos.stemmer.Lovins."""
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        # test cases from Lovins' "Development of a Stemming Algorithm":
        # http://www.mt-archive.info/MT-1968-Lovins.pdf
        self.assertEqual(self.stmr.stem('magnesia'), 'magnes')
        self.assertEqual(self.stmr.stem('magnesite'), 'magnes')
        self.assertEqual(self.stmr.stem('magnesian'), 'magnes')
        self.assertEqual(self.stmr.stem('magnesium'), 'magnes')
        self.assertEqual(self.stmr.stem('magnet'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetic'), 'magnet')
        self.assertEqual(self.stmr.stem('magneto'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetically'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetism'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetite'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetitic'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetizable'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetization'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetize'), 'magnet')
        self.assertEqual(self.stmr.stem('magnetometer'), 'magnetometer')
        self.assertEqual(self.stmr.stem('magnetometric'), 'magnetometer')
        self.assertEqual(self.stmr.stem('magnetometry'), 'magnetometer')
        self.assertEqual(self.stmr.stem('magnetomotive'), 'magnetomot')
        self.assertEqual(self.stmr.stem('magnetron'), 'magnetron')
        self.assertEqual(self.stmr.stem('metal'), 'metal')
        self.assertEqual(self.stmr.stem('metall'), 'metal')
        self.assertEqual(self.stmr.stem('metallically'), 'metal')
        self.assertEqual(self.stmr.stem('metalliferous'), 'metallifer')
        self.assertEqual(self.stmr.stem('metallize'), 'metal')
        self.assertEqual(self.stmr.stem('metallurgical'), 'metallurg')
        self.assertEqual(self.stmr.stem('metallurgy'), 'metallurg')
        self.assertEqual(self.stmr.stem('induction'), 'induc')
        self.assertEqual(self.stmr.stem('inductance'), 'induc')
        self.assertEqual(self.stmr.stem('induced'), 'induc')
        self.assertEqual(self.stmr.stem('angular'), 'angl')
        self.assertEqual(self.stmr.stem('angle'), 'angl')

        # missed branch test cases
        self.assertEqual(self.stmr.stem('feminism'), 'fem')

    def test_lovins_snowball(self):
        """Test abydos.stemmer.Lovins (Snowball testset).

        These test cases are from
        https://github.com/snowballstem/snowball-data/tree/master/lovins
        """
        #  Snowball Lovins test set
        with codecs.open(
            _corpus_file('snowball_lovins.csv'), encoding='utf-8'
        ) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(self.stmr.stem(word), stem.lower())


if __name__ == '__main__':
    unittest.main()
