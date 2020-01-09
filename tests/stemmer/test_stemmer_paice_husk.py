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

"""abydos.tests.stemmer.test_stemmer_paice_husk.

This module contains unit tests for abydos.stemmer.PaiceHusk
"""

import unittest

from abydos.stemmer import PaiceHusk, paice_husk

from .. import _corpus_file


class PaiceHuskTestCases(unittest.TestCase):
    """Test Paice-Husk functions.

    abydos.stemmer.PaiceHusk
    """

    stmr = PaiceHusk()

    def test_paice_husk(self):
        """Test abydos.stemmer.PaiceHusk."""
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        # cases copied from
        # https://doi.org/10.1145/101306.101310
        self.assertEqual(self.stmr.stem('maximum'), 'maxim')
        self.assertEqual(self.stmr.stem('presumably'), 'presum')
        self.assertEqual(self.stmr.stem('multiply'), 'multiply')
        self.assertEqual(self.stmr.stem('provision'), 'provid')
        self.assertEqual(self.stmr.stem('owed'), 'ow')
        self.assertEqual(self.stmr.stem('owing'), 'ow')
        self.assertEqual(self.stmr.stem('ear'), 'ear')
        self.assertEqual(self.stmr.stem('saying'), 'say')
        self.assertEqual(self.stmr.stem('crying'), 'cry')
        self.assertEqual(self.stmr.stem('string'), 'string')
        self.assertEqual(self.stmr.stem('meant'), 'meant')
        self.assertEqual(self.stmr.stem('cement'), 'cem')

        # Test wrapper
        self.assertEqual(paice_husk('maximum'), 'maxim')

    def test_paice_husk_hopper_set(self):
        """Test abydos.stemmer.PaiceHusk (Hopper262 testset).

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
                self.assertEqual(self.stmr.stem(word), stem)


if __name__ == '__main__':
    unittest.main()
