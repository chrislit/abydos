# -*- coding: utf-8 -*-
"""abydos.tests.test_stemmer

This module contains unit tests for abydos.stemmer

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
from abydos.stemmer import _m_degree, _sb_has_vowel, _ends_in_doubled_cons, \
    _ends_in_cvc, porter, _sb_r1, _sb_r2, _sb_short_syllable, \
    _sb_ends_in_short_syllable, _sb_short_word, porter2
import os

TESTDIR = os.path.dirname(__file__)

class PorterTestCases(unittest.TestCase):
    """test cases for abydos.stemmer._m_degree, abydos.stemmer.porter 
    """
    def test_m_degree(self):
        """test abydos.stemmer._m_degree
        """
        # base case
        self.assertEqual(_m_degree(''), 0)

        # m==0
        self.assertEqual(_m_degree('tr'), 0)
        self.assertEqual(_m_degree('ee'), 0)
        self.assertEqual(_m_degree('tree'), 0)
        self.assertEqual(_m_degree('y'), 0)
        self.assertEqual(_m_degree('by'), 0)

        # m==1
        self.assertEqual(_m_degree('trouble'), 1)
        self.assertEqual(_m_degree('oats'), 1)
        self.assertEqual(_m_degree('trees'), 1)
        self.assertEqual(_m_degree('ivy'), 1)

        # m==2
        self.assertEqual(_m_degree('troubles'), 2)
        self.assertEqual(_m_degree('private'), 2)
        self.assertEqual(_m_degree('oaten'), 2)
        self.assertEqual(_m_degree('orrery'), 2)


    def test_has_vowel(self):
        """test abydos.stemmer._has_vowel
        """
        # base case
        self.assertFalse(_sb_has_vowel(''))

        # False cases
        self.assertFalse(_sb_has_vowel('b'))
        self.assertFalse(_sb_has_vowel('c'))
        self.assertFalse(_sb_has_vowel('bc'))
        self.assertFalse(_sb_has_vowel('bcdfghjklmnpqrstvwxYz'))
        self.assertFalse(_sb_has_vowel('Y'))

        # True cases
        self.assertTrue(_sb_has_vowel('a'))
        self.assertTrue(_sb_has_vowel('e'))
        self.assertTrue(_sb_has_vowel('ae'))
        self.assertTrue(_sb_has_vowel('aeiouy'))
        self.assertTrue(_sb_has_vowel('y'))

        self.assertTrue(_sb_has_vowel('ade'))
        self.assertTrue(_sb_has_vowel('cad'))
        self.assertTrue(_sb_has_vowel('add'))
        self.assertTrue(_sb_has_vowel('phi'))
        self.assertTrue(_sb_has_vowel('pfy'))

        self.assertFalse(_sb_has_vowel('pfY'))


    def test_ends_in_doubled_cons(self):
        """test abydos.stemmer._ends_in_doubled_cons
        """
        # base case
        self.assertFalse(_ends_in_doubled_cons(''))

        # False cases
        self.assertFalse(_ends_in_doubled_cons('b'))
        self.assertFalse(_ends_in_doubled_cons('c'))
        self.assertFalse(_ends_in_doubled_cons('bc'))
        self.assertFalse(_ends_in_doubled_cons('bcdfghjklmnpqrstvwxYz'))
        self.assertFalse(_ends_in_doubled_cons('Y'))
        self.assertFalse(_ends_in_doubled_cons('a'))
        self.assertFalse(_ends_in_doubled_cons('e'))
        self.assertFalse(_ends_in_doubled_cons('ae'))
        self.assertFalse(_ends_in_doubled_cons('aeiouy'))
        self.assertFalse(_ends_in_doubled_cons('y'))
        self.assertFalse(_ends_in_doubled_cons('ade'))
        self.assertFalse(_ends_in_doubled_cons('cad'))
        self.assertFalse(_ends_in_doubled_cons('phi'))
        self.assertFalse(_ends_in_doubled_cons('pfy'))
        self.assertFalse(_ends_in_doubled_cons('faddy'))
        self.assertFalse(_ends_in_doubled_cons('aiii'))
        self.assertFalse(_ends_in_doubled_cons('ayyy'))

        # True cases
        self.assertTrue(_ends_in_doubled_cons('add'))
        self.assertTrue(_ends_in_doubled_cons('fadd'))
        self.assertTrue(_ends_in_doubled_cons('fadddd'))
        self.assertTrue(_ends_in_doubled_cons('raYY'))
        self.assertTrue(_ends_in_doubled_cons('doll'))
        self.assertTrue(_ends_in_doubled_cons('parr'))
        self.assertTrue(_ends_in_doubled_cons('parrr'))
        self.assertTrue(_ends_in_doubled_cons('bacc'))


    def test_ends_in_cvc(self):
        """test abydos.stemmer._ends_in_cvc
        """
        # base case
        self.assertFalse(_ends_in_cvc(''))

        # False cases
        self.assertFalse(_ends_in_cvc('b'))
        self.assertFalse(_ends_in_cvc('c'))
        self.assertFalse(_ends_in_cvc('bc'))
        self.assertFalse(_ends_in_cvc('bcdfghjklmnpqrstvwxYz'))
        self.assertFalse(_ends_in_cvc('YYY'))
        self.assertFalse(_ends_in_cvc('ddd'))
        self.assertFalse(_ends_in_cvc('faaf'))
        self.assertFalse(_ends_in_cvc('rare'))
        self.assertFalse(_ends_in_cvc('rhy'))

        # True cases
        self.assertTrue(_ends_in_cvc('dad'))
        self.assertTrue(_ends_in_cvc('phad'))
        self.assertTrue(_ends_in_cvc('faded'))
        self.assertTrue(_ends_in_cvc('maYor'))
        self.assertTrue(_ends_in_cvc('enlil'))
        self.assertTrue(_ends_in_cvc('parer'))
        self.assertTrue(_ends_in_cvc('padres'))
        self.assertTrue(_ends_in_cvc('bacyc'))

        # Special case for W, X, & Y
        self.assertFalse(_ends_in_cvc('craw'))
        self.assertFalse(_ends_in_cvc('max'))
        self.assertFalse(_ends_in_cvc('cray'))


    def test_porter(self):
        """test abydos.stemmer.porter
        """
        # base case
        self.assertEqual(porter(''), '')

        # simple cases
        self.assertEqual(porter('c'), 'c')
        self.assertEqual(porter('da'), 'da')
        self.assertEqual(porter('ad'), 'ad')
        self.assertEqual(porter('sing'), 'sing')
        self.assertEqual(porter('singing'), 'sing')


    def test_porter_snowball(self):
        """test abydos.stemmer.porter (Snowball testset)

        These test cases are from
        http://snowball.tartarus.org/algorithms/porter/diffs.txt
        """
        #  Snowball Porter test set
        with open(TESTDIR+'/snowball_porter.csv') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                line = line.strip().split(',')
                word, stem = line[0], line[1]
                self.assertEqual(porter(word), stem.lower())

    def test_sb_r1(self):
        """test abydos.stemmer._sb_r1
        """
        # base case
        self.assertEqual(_sb_r1(''), 0)

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(_sb_r1('beautiful'), 5)
        self.assertEqual(_sb_r1('beauty'), 5)
        self.assertEqual(_sb_r1('beau'), 4)
        self.assertEqual(_sb_r1('animadversion'), 2)
        self.assertEqual(_sb_r1('sprinkled'), 5)
        self.assertEqual(_sb_r1('eucharist'), 3)

    def test_sb_r2(self):
        """test abydos.stemmer._sb_r2
        """
        # base case
        self.assertEqual(_sb_r2(''), 0)

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(_sb_r2('beautiful'), 7)
        self.assertEqual(_sb_r2('beauty'), 6)
        self.assertEqual(_sb_r2('beau'), 4)
        self.assertEqual(_sb_r2('animadversion'), 4)
        self.assertEqual(_sb_r2('sprinkled'), 9)
        self.assertEqual(_sb_r2('eucharist'), 6)

    def test_sb_short_syllable(self):
        """test abydos.stemmer._sb_short_syllable
        """
        # base case
        self.assertFalse(_sb_short_syllable(''))

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(_sb_short_syllable('rap', 1))
        self.assertTrue(_sb_short_syllable('trap', 2))
        self.assertTrue(_sb_short_syllable('entrap', 4))
        self.assertTrue(_sb_short_syllable('ow'))
        self.assertTrue(_sb_short_syllable('on'))
        self.assertTrue(_sb_short_syllable('at'))
        self.assertFalse(_sb_short_syllable('uproot', 3))
        self.assertFalse(_sb_short_syllable('uproot', 4))
        self.assertFalse(_sb_short_syllable('bestow', 4))
        #self.assertFalse(_sb_short_syllable('disturb', 4))

    def test_sb_ends_in_short_syllable(self):
        """test abydos.stemmer._sb_ends_in_short_syllable
        """
        # base case
        self.assertFalse(_sb_ends_in_short_syllable(''))

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(_sb_ends_in_short_syllable('rap'))
        self.assertTrue(_sb_ends_in_short_syllable('trap'))
        self.assertTrue(_sb_ends_in_short_syllable('entrap'))
        self.assertTrue(_sb_ends_in_short_syllable('ow'))
        self.assertTrue(_sb_ends_in_short_syllable('on'))
        self.assertTrue(_sb_ends_in_short_syllable('at'))
        self.assertFalse(_sb_ends_in_short_syllable('uproot'))
        self.assertFalse(_sb_ends_in_short_syllable('uproot'))
        self.assertFalse(_sb_ends_in_short_syllable('bestow'))
        self.assertFalse(_sb_short_syllable('disturb'))

    def test_sb_short_word(self):
        """test abydos.stemmer._sb_short_word
        """
        # base case
        self.assertFalse(_sb_short_word(''))

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(_sb_short_word('bed'))
        self.assertTrue(_sb_short_word('shed'))
        self.assertTrue(_sb_short_word('shred'))
        self.assertFalse(_sb_short_word('bead'))
        self.assertFalse(_sb_short_word('embed'))
        self.assertFalse(_sb_short_word('beds'))


    def test_porter2(self):
        """test abydos.stemmer.porter2
        """
        # base case
        self.assertEqual(porter2(''), '')

        # simple cases
        self.assertEqual(porter2('c'), 'c')
        self.assertEqual(porter2('da'), 'da')
        self.assertEqual(porter2('ad'), 'ad')
        self.assertEqual(porter2('sing'), 'sing')
        self.assertEqual(porter2('singing'), 'sing')


    def test_porter2_snowball(self):
        """test abydos.stemmer.porter2 (Snowball testset)

        These test cases are from
        http://snowball.tartarus.org/algorithms/english/diffs.txt
        """
        #  Snowball Porter test set
        with open(TESTDIR+'/snowball_porter2.csv') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(porter2(word), stem.lower())
