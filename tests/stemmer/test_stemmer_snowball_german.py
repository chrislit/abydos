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

"""abydos.tests.stemmer.test_stemmer_snowball_german.

This module contains unit tests for abydos.stemmer.SnowballGerman
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import codecs
import unittest

from abydos.stemmer import SnowballGerman, sb_german

from .. import _corpus_file


class SnowballGermanTestCases(unittest.TestCase):
    """Test Snowball German functions.

    abydos.stemmer.SnowballGerman
    """

    stmr = SnowballGerman()
    stmr_av = SnowballGerman(alternate_vowels=True)

    def test_snowball_german(self):
        """Test abydos.stemmer.SnowballGerman (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/german/diffs.txt
        """
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        #  Snowball German test set
        with codecs.open(
            _corpus_file('snowball_german.csv'), encoding='utf-8'
        ) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(self.stmr.stem(word), stem.lower())

        # missed branch test cases
        self.assertEqual(self.stmr.stem('ikeit'), 'ikeit')

        # Test wrapper
        self.assertEqual(sb_german('dämmerung'), 'dammer')

    def test_sb_german_snowball_alt(self):
        """Test abydos.stemmer.SnowballGerman (alternate vowels)."""
        # base case
        self.assertEqual(self.stmr_av.stem(''), '')

        # dämmerung,dammer
        self.assertEqual(self.stmr_av.stem('dämmerung'), 'dammer')
        self.assertEqual(self.stmr_av.stem('daemmerung'), 'dammer')
        self.assertEqual(self.stmr.stem('dämmerung'), 'dammer')
        self.assertEqual(self.stmr.stem('daemmerung'), 'daemmer')

        # brötchen,brotch
        self.assertEqual(self.stmr_av.stem('brötchen'), 'brotch')
        self.assertEqual(self.stmr_av.stem('broetchen'), 'brotch')
        self.assertEqual(self.stmr.stem('brötchen'), 'brotch')
        self.assertEqual(self.stmr.stem('broetchen'), 'broetch')

        # büro,buro
        self.assertEqual(self.stmr_av.stem('büro'), 'buro')
        self.assertEqual(self.stmr_av.stem('buero'), 'buro')
        self.assertEqual(self.stmr.stem('büro'), 'buro')
        self.assertEqual(self.stmr.stem('buero'), 'buero')

        # häufen,hauf
        self.assertEqual(self.stmr_av.stem('häufen'), 'hauf')
        self.assertEqual(self.stmr_av.stem('haeufen'), 'hauf')
        self.assertEqual(self.stmr.stem('häufen'), 'hauf')
        self.assertEqual(self.stmr.stem('haeufen'), 'haeuf')

        # quelle,quell
        self.assertEqual(self.stmr_av.stem('qülle'), 'qull')
        self.assertEqual(self.stmr_av.stem('quelle'), 'quell')
        self.assertEqual(self.stmr.stem('qülle'), 'qull')
        self.assertEqual(self.stmr.stem('quelle'), 'quell')

        # feuer,feuer
        self.assertEqual(self.stmr_av.stem('feür'), 'feur')
        self.assertEqual(self.stmr_av.stem('feuer'), 'feu')
        self.assertEqual(self.stmr.stem('feür'), 'feur')
        self.assertEqual(self.stmr.stem('feuer'), 'feu')

        # über,uber
        self.assertEqual(self.stmr_av.stem('über'), 'uber')
        self.assertEqual(self.stmr_av.stem('ueber'), 'uber')
        self.assertEqual(self.stmr.stem('über'), 'uber')
        self.assertEqual(self.stmr.stem('ueber'), 'ueb')


if __name__ == '__main__':
    unittest.main()
