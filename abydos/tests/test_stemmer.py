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
    _ends_in_cvc, porter, _sb_r1, _sb_r2, _sb_ends_in_short_syllable, \
    _sb_short_word, porter2, german
import os, codecs

TESTDIR = os.path.dirname(__file__)

class PorterTestCases(unittest.TestCase):
    """test cases for abydos.stemmer._m_degree, abydos.stemmer.porter
    """
    def test_m_degree(self):
        """test abydos.stemmer._m_degree
        """
        _vowels = set('aeiouy')
        # base case
        self.assertEqual(_m_degree('', _vowels), 0)

        # m==0
        self.assertEqual(_m_degree('tr', _vowels), 0)
        self.assertEqual(_m_degree('ee', _vowels), 0)
        self.assertEqual(_m_degree('tree', _vowels), 0)
        self.assertEqual(_m_degree('y', _vowels), 0)
        self.assertEqual(_m_degree('by', _vowels), 0)

        # m==1
        self.assertEqual(_m_degree('trouble', _vowels), 1)
        self.assertEqual(_m_degree('oats', _vowels), 1)
        self.assertEqual(_m_degree('trees', _vowels), 1)
        self.assertEqual(_m_degree('ivy', _vowels), 1)

        # m==2
        self.assertEqual(_m_degree('troubles', _vowels), 2)
        self.assertEqual(_m_degree('private', _vowels), 2)
        self.assertEqual(_m_degree('oaten', _vowels), 2)
        self.assertEqual(_m_degree('orrery', _vowels), 2)


    def test_has_vowel(self):
        """test abydos.stemmer._has_vowel
        """
        _vowels = set('aeiouy')
        # base case
        self.assertFalse(_sb_has_vowel('', _vowels))

        # False cases
        self.assertFalse(_sb_has_vowel('b', _vowels))
        self.assertFalse(_sb_has_vowel('c', _vowels))
        self.assertFalse(_sb_has_vowel('bc', _vowels))
        self.assertFalse(_sb_has_vowel('bcdfghjklmnpqrstvwxYz', _vowels))
        self.assertFalse(_sb_has_vowel('Y', _vowels))

        # True cases
        self.assertTrue(_sb_has_vowel('a', _vowels))
        self.assertTrue(_sb_has_vowel('e', _vowels))
        self.assertTrue(_sb_has_vowel('ae', _vowels))
        self.assertTrue(_sb_has_vowel('aeiouy', _vowels))
        self.assertTrue(_sb_has_vowel('y', _vowels))

        self.assertTrue(_sb_has_vowel('ade', _vowels))
        self.assertTrue(_sb_has_vowel('cad', _vowels))
        self.assertTrue(_sb_has_vowel('add', _vowels))
        self.assertTrue(_sb_has_vowel('phi', _vowels))
        self.assertTrue(_sb_has_vowel('pfy', _vowels))

        self.assertFalse(_sb_has_vowel('pfY', _vowels))


    def test_ends_in_doubled_cons(self):
        """test abydos.stemmer._ends_in_doubled_cons
        """
        _vowels = set('aeiouy')
        # base case
        self.assertFalse(_ends_in_doubled_cons('', _vowels))

        # False cases
        self.assertFalse(_ends_in_doubled_cons('b', _vowels))
        self.assertFalse(_ends_in_doubled_cons('c', _vowels))
        self.assertFalse(_ends_in_doubled_cons('bc', _vowels))
        self.assertFalse(_ends_in_doubled_cons('bcdfghjklmnpqrstvwxYz',
                                               _vowels))
        self.assertFalse(_ends_in_doubled_cons('Y', _vowels))
        self.assertFalse(_ends_in_doubled_cons('a', _vowels))
        self.assertFalse(_ends_in_doubled_cons('e', _vowels))
        self.assertFalse(_ends_in_doubled_cons('ae', _vowels))
        self.assertFalse(_ends_in_doubled_cons('aeiouy', _vowels))
        self.assertFalse(_ends_in_doubled_cons('y', _vowels))
        self.assertFalse(_ends_in_doubled_cons('ade', _vowels))
        self.assertFalse(_ends_in_doubled_cons('cad', _vowels))
        self.assertFalse(_ends_in_doubled_cons('phi', _vowels))
        self.assertFalse(_ends_in_doubled_cons('pfy', _vowels))
        self.assertFalse(_ends_in_doubled_cons('faddy', _vowels))
        self.assertFalse(_ends_in_doubled_cons('aiii', _vowels))
        self.assertFalse(_ends_in_doubled_cons('ayyy', _vowels))

        # True cases
        self.assertTrue(_ends_in_doubled_cons('add', _vowels))
        self.assertTrue(_ends_in_doubled_cons('fadd', _vowels))
        self.assertTrue(_ends_in_doubled_cons('fadddd', _vowels))
        self.assertTrue(_ends_in_doubled_cons('raYY', _vowels))
        self.assertTrue(_ends_in_doubled_cons('doll', _vowels))
        self.assertTrue(_ends_in_doubled_cons('parr', _vowels))
        self.assertTrue(_ends_in_doubled_cons('parrr', _vowels))
        self.assertTrue(_ends_in_doubled_cons('bacc', _vowels))


    def test_ends_in_cvc(self):
        """test abydos.stemmer._ends_in_cvc
        """
        _vowels = set('aeiouy')
        # base case
        self.assertFalse(_ends_in_cvc('', _vowels))

        # False cases
        self.assertFalse(_ends_in_cvc('b', _vowels))
        self.assertFalse(_ends_in_cvc('c', _vowels))
        self.assertFalse(_ends_in_cvc('bc', _vowels))
        self.assertFalse(_ends_in_cvc('bcdfghjklmnpqrstvwxYz', _vowels))
        self.assertFalse(_ends_in_cvc('YYY', _vowels))
        self.assertFalse(_ends_in_cvc('ddd', _vowels))
        self.assertFalse(_ends_in_cvc('faaf', _vowels))
        self.assertFalse(_ends_in_cvc('rare', _vowels))
        self.assertFalse(_ends_in_cvc('rhy', _vowels))

        # True cases
        self.assertTrue(_ends_in_cvc('dad', _vowels))
        self.assertTrue(_ends_in_cvc('phad', _vowels))
        self.assertTrue(_ends_in_cvc('faded', _vowels))
        self.assertTrue(_ends_in_cvc('maYor', _vowels))
        self.assertTrue(_ends_in_cvc('enlil', _vowels))
        self.assertTrue(_ends_in_cvc('parer', _vowels))
        self.assertTrue(_ends_in_cvc('padres', _vowels))
        self.assertTrue(_ends_in_cvc('bacyc', _vowels))

        # Special case for W, X, & Y
        self.assertFalse(_ends_in_cvc('craw', _vowels))
        self.assertFalse(_ends_in_cvc('max', _vowels))
        self.assertFalse(_ends_in_cvc('cray', _vowels))


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
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(porter(word), stem.lower())

    def test_sb_r1(self):
        """test abydos.stemmer._sb_r1
        """
        _vowels = set('aeiouy')
        # base case
        self.assertEqual(_sb_r1('', _vowels), 0)

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(_sb_r1('beautiful', _vowels), 5)
        self.assertEqual(_sb_r1('beauty', _vowels), 5)
        self.assertEqual(_sb_r1('beau', _vowels), 4)
        self.assertEqual(_sb_r1('animadversion', _vowels), 2)
        self.assertEqual(_sb_r1('sprinkled', _vowels), 5)
        self.assertEqual(_sb_r1('eucharist', _vowels), 3)

    def test_sb_r2(self):
        """test abydos.stemmer._sb_r2
        """
        _vowels = set('aeiouy')
        # base case
        self.assertEqual(_sb_r2('', _vowels), 0)

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(_sb_r2('beautiful', _vowels), 7)
        self.assertEqual(_sb_r2('beauty', _vowels), 6)
        self.assertEqual(_sb_r2('beau', _vowels), 4)
        self.assertEqual(_sb_r2('animadversion', _vowels), 4)
        self.assertEqual(_sb_r2('sprinkled', _vowels), 9)
        self.assertEqual(_sb_r2('eucharist', _vowels), 6)

    def test_sb_ends_in_short_syllable(self):
        """test abydos.stemmer._sb_ends_in_short_syllable
        """
        _vowels = set('aeiouy')
        _codanonvowels = set('bcdfghjklmnpqrstvz\'')
        # base case
        self.assertFalse(_sb_ends_in_short_syllable('', _vowels,
                                                    _codanonvowels))

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(_sb_ends_in_short_syllable('rap', _vowels,
                                                   _codanonvowels))
        self.assertTrue(_sb_ends_in_short_syllable('trap', _vowels,
                                                   _codanonvowels))
        self.assertTrue(_sb_ends_in_short_syllable('entrap', _vowels,
                                                   _codanonvowels))
        self.assertTrue(_sb_ends_in_short_syllable('ow', _vowels,
                                                   _codanonvowels))
        self.assertTrue(_sb_ends_in_short_syllable('on', _vowels,
                                                   _codanonvowels))
        self.assertTrue(_sb_ends_in_short_syllable('at', _vowels,
                                                   _codanonvowels))
        self.assertFalse(_sb_ends_in_short_syllable('uproot', _vowels,
                                                    _codanonvowels))
        self.assertFalse(_sb_ends_in_short_syllable('uproot', _vowels,
                                                    _codanonvowels))
        self.assertFalse(_sb_ends_in_short_syllable('bestow', _vowels,
                                                    _codanonvowels))
        self.assertFalse(_sb_ends_in_short_syllable('disturb', _vowels,
                                                    _codanonvowels))

    def test_sb_short_word(self):
        """test abydos.stemmer._sb_short_word
        """
        _vowels = set('aeiouy')
        _codanonvowels = set('bcdfghjklmnpqrstvz\'')
        # base case
        self.assertFalse(_sb_short_word('', _vowels, _codanonvowels))

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(_sb_short_word('bed', _vowels, _codanonvowels))
        self.assertTrue(_sb_short_word('shed', _vowels, _codanonvowels))
        self.assertTrue(_sb_short_word('shred', _vowels, _codanonvowels))
        self.assertFalse(_sb_short_word('bead', _vowels, _codanonvowels))
        self.assertFalse(_sb_short_word('embed', _vowels, _codanonvowels))
        self.assertFalse(_sb_short_word('beds', _vowels, _codanonvowels))


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


    def test_german_snowball(self):
        """test abydos.stemmer.german (Snowball testset)

        These test cases are from
        http://snowball.tartarus.org/algorithms/german/diffs.txt
        """
        #  Snowball Porter test set
        with codecs.open(TESTDIR+'/snowball_german.csv', 'r',
                         'utf-8') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(german(word), stem.lower())
