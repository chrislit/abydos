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

"""abydos.tests.stemmer.test_stemmer_porter.

This module contains unit tests for abydos.stemmer.Porter
"""

import unittest

from abydos.stemmer import Porter, porter


from .. import _corpus_file


class PorterTestCases(unittest.TestCase):
    """Test Porter functions.

    abydos.stemmer.Porter
    """

    stmr = Porter()
    stmr._vowels = set('aeiouy')  # noqa: SF01
    stmr_ee = Porter(early_english=True)
    stmr_ee._vowels = set('aeiouy')  # noqa: SF01

    def test_m_degree(self):
        """Test abydos.stemmer.Porter._m_degree."""
        # base case
        self.assertEqual(self.stmr._m_degree(''), 0)  # noqa: SF01

        # m==0
        self.assertEqual(self.stmr._m_degree('tr'), 0)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('ee'), 0)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('tree'), 0)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('y'), 0)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('by'), 0)  # noqa: SF01

        # m==1
        self.assertEqual(self.stmr._m_degree('trouble'), 1)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('oats'), 1)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('trees'), 1)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('ivy'), 1)  # noqa: SF01

        # m==2
        self.assertEqual(self.stmr._m_degree('troubles'), 2)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('private'), 2)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('oaten'), 2)  # noqa: SF01
        self.assertEqual(self.stmr._m_degree('orrery'), 2)  # noqa: SF01

    def test_has_vowel(self):
        """Test abydos.stemmer.Porter._has_vowel."""
        # base case
        self.assertFalse(self.stmr._has_vowel(''))  # noqa: SF01

        # False cases
        self.assertFalse(self.stmr._has_vowel('b'))  # noqa: SF01
        self.assertFalse(self.stmr._has_vowel('c'))  # noqa: SF01
        self.assertFalse(self.stmr._has_vowel('bc'))  # noqa: SF01
        self.assertFalse(
            self.stmr._has_vowel('bcdfghjklmnpqrstvwxYz')  # noqa: SF01
        )
        self.assertFalse(self.stmr._has_vowel('Y'))  # noqa: SF01

        # True cases
        self.assertTrue(self.stmr._has_vowel('a'))  # noqa: SF01
        self.assertTrue(self.stmr._has_vowel('e'))  # noqa: SF01
        self.assertTrue(self.stmr._has_vowel('ae'))  # noqa: SF01
        self.assertTrue(self.stmr._has_vowel('aeiouy'))  # noqa: SF01
        self.assertTrue(self.stmr._has_vowel('y'))  # noqa: SF01

        self.assertTrue(self.stmr._has_vowel('ade'))  # noqa: SF01
        self.assertTrue(self.stmr._has_vowel('cad'))  # noqa: SF01
        self.assertTrue(self.stmr._has_vowel('add'))  # noqa: SF01
        self.assertTrue(self.stmr._has_vowel('phi'))  # noqa: SF01
        self.assertTrue(self.stmr._has_vowel('pfy'))  # noqa: SF01

        self.assertFalse(self.stmr._has_vowel('pfY'))  # noqa: SF01

    def test_ends_in_doubled_cons(self):
        """Test abydos.stemmer.Porter._ends_in_doubled_cons."""
        # base case
        self.assertFalse(self.stmr._ends_in_doubled_cons(''))  # noqa: SF01

        # False cases
        self.assertFalse(self.stmr._ends_in_doubled_cons('b'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('c'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('bc'))  # noqa: SF01
        self.assertFalse(
            self.stmr._ends_in_doubled_cons(  # noqa: SF01
                'bcdfghjklmnpqrstvwxYz'
            )
        )
        self.assertFalse(self.stmr._ends_in_doubled_cons('Y'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('a'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('e'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('ae'))  # noqa: SF01
        self.assertFalse(
            self.stmr._ends_in_doubled_cons('aeiouy')  # noqa: SF01
        )
        self.assertFalse(self.stmr._ends_in_doubled_cons('y'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('ade'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('cad'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('phi'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('pfy'))  # noqa: SF01
        self.assertFalse(
            self.stmr._ends_in_doubled_cons('faddy')  # noqa: SF01
        )
        self.assertFalse(self.stmr._ends_in_doubled_cons('aiii'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_doubled_cons('ayyy'))  # noqa: SF01

        # True cases
        self.assertTrue(self.stmr._ends_in_doubled_cons('add'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_doubled_cons('fadd'))  # noqa: SF01
        self.assertTrue(
            self.stmr._ends_in_doubled_cons('fadddd')  # noqa: SF01
        )
        self.assertTrue(self.stmr._ends_in_doubled_cons('raYY'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_doubled_cons('doll'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_doubled_cons('parr'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_doubled_cons('parrr'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_doubled_cons('bacc'))  # noqa: SF01

    def test_ends_in_cvc(self):
        """Test abydos.stemmer.Porter._ends_in_cvc."""
        # base case
        self.assertFalse(self.stmr._ends_in_cvc(''))  # noqa: SF01

        # False cases
        self.assertFalse(self.stmr._ends_in_cvc('b'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_cvc('c'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_cvc('bc'))  # noqa: SF01
        self.assertFalse(
            self.stmr._ends_in_cvc('bcdfghjklmnpqrstvwxYz')  # noqa: SF01
        )
        self.assertFalse(self.stmr._ends_in_cvc('YYY'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_cvc('ddd'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_cvc('faaf'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_cvc('rare'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_cvc('rhy'))  # noqa: SF01

        # True cases
        self.assertTrue(self.stmr._ends_in_cvc('dad'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_cvc('phad'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_cvc('faded'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_cvc('maYor'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_cvc('enlil'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_cvc('parer'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_cvc('padres'))  # noqa: SF01
        self.assertTrue(self.stmr._ends_in_cvc('bacyc'))  # noqa: SF01

        # Special case for W, X, & Y
        self.assertFalse(self.stmr._ends_in_cvc('craw'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_cvc('max'))  # noqa: SF01
        self.assertFalse(self.stmr._ends_in_cvc('cray'))  # noqa: SF01

    def test_porter(self):
        """Test abydos.stemmer.Porter."""
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        # simple cases
        self.assertEqual(self.stmr.stem('c'), 'c')
        self.assertEqual(self.stmr.stem('da'), 'da')
        self.assertEqual(self.stmr.stem('ad'), 'ad')
        self.assertEqual(self.stmr.stem('sing'), 'sing')
        self.assertEqual(self.stmr.stem('singing'), 'sing')

        # missed branch test cases
        self.assertEqual(self.stmr.stem('capitalism'), 'capit')
        self.assertEqual(self.stmr.stem('fatalism'), 'fatal')
        self.assertEqual(self.stmr.stem('stional'), 'stional')
        self.assertEqual(self.stmr.stem('palism'), 'palism')
        self.assertEqual(self.stmr.stem('sization'), 'sizat')
        self.assertEqual(self.stmr.stem('licated'), 'licat')
        self.assertEqual(self.stmr.stem('lical'), 'lical')

        # Test wrapper
        self.assertEqual(porter('singing'), 'sing')

    def test_porter_early_english(self):
        """Test abydos.stemmer.Porter (early English)."""
        # base case
        self.assertEqual(self.stmr_ee.stem(''), '')

        # simple cases (no different from regular stemmer)
        self.assertEqual(self.stmr_ee.stem('c'), 'c')
        self.assertEqual(self.stmr_ee.stem('da'), 'da')
        self.assertEqual(self.stmr_ee.stem('ad'), 'ad')
        self.assertEqual(self.stmr_ee.stem('sing'), 'sing')
        self.assertEqual(self.stmr_ee.stem('singing'), 'sing')

        # make
        self.assertEqual(self.stmr_ee.stem('make'), 'make')
        self.assertEqual(self.stmr_ee.stem('makes'), 'make')
        self.assertEqual(self.stmr_ee.stem('maketh'), 'make')
        self.assertEqual(self.stmr_ee.stem('makest'), 'make')

        # say
        self.assertEqual(self.stmr_ee.stem('say'), 'sai')
        self.assertEqual(self.stmr_ee.stem('says'), 'sai')
        self.assertEqual(self.stmr_ee.stem('sayeth'), 'sai')
        self.assertEqual(self.stmr_ee.stem('sayest'), 'sai')

        # missed branch test cases
        self.assertEqual(self.stmr_ee.stem('best'), 'best')
        self.assertEqual(self.stmr_ee.stem('meth'), 'meth')

    def test_porter_snowball(self):
        """Test abydos.stemmer.Porter (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/porter/diffs.txt
        """
        #  Snowball Porter test set
        with open(_corpus_file('snowball_porter.csv')) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(self.stmr.stem(word), stem.lower())


if __name__ == '__main__':
    unittest.main()
