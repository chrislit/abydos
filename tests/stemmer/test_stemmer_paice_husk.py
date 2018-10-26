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

"""abydos.tests.stemmer.test_stemmer_paice_husk.

This module contains unit tests for abydos.stemmer._paice_husk
"""

from __future__ import unicode_literals

import unittest

from abydos.stemmer import paice_husk

from .. import _corpus_file


class PaiceHuskTestCases(unittest.TestCase):
    """Test Paice-Husk functions.

    abydos.stemmer._paice_husk.paice_husk
    """

    def test_paice_husk(self):
        """Test abydos.stemmer._paice_husk.paice_husk."""
        # base case
        self.assertEqual(paice_husk(''), '')

        # cases copied from
        # https://doi.org/10.1145/101306.101310
        self.assertEqual(paice_husk('maximum'), 'maxim')
        self.assertEqual(paice_husk('presumably'), 'presum')
        self.assertEqual(paice_husk('multiply'), 'multiply')
        self.assertEqual(paice_husk('provision'), 'provid')
        self.assertEqual(paice_husk('owed'), 'ow')
        self.assertEqual(paice_husk('owing'), 'ow')
        self.assertEqual(paice_husk('ear'), 'ear')
        self.assertEqual(paice_husk('saying'), 'say')
        self.assertEqual(paice_husk('crying'), 'cry')
        self.assertEqual(paice_husk('string'), 'string')
        self.assertEqual(paice_husk('meant'), 'meant')
        self.assertEqual(paice_husk('cement'), 'cem')

    def test_paice_husk_hopper_set(self):
        """Test abydos.stemmer._paice_husk.paice_husk (Hopper262 testset).

        Source:
        https://raw.githubusercontent.com/Hopper262/paice-husk-stemmer/master/wordlist.txt

        The only correction made from stemmed values in the Hopper262 set/
        implementations were:
         - ymca : ymc -> ymca
         - yttrium : yttr -> yttri
         - ywca : ywc -> ywca
        The Pascal reference implementation does not consider 'y' in initial
        position to be a vowel.
        """
        with open(_corpus_file('paicehusk.csv')) as hopper_ts:
            for hopper_line in hopper_ts:
                (word, stem) = hopper_line.strip().split(',')
                self.assertEqual(paice_husk(word), stem)


if __name__ == '__main__':
    unittest.main()
