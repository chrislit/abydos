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

"""abydos.tests.test_stemmer.

This module contains unit tests for abydos.stemmer
"""

from __future__ import unicode_literals

import codecs
import os
import unittest

from abydos.stemmer import _ends_in_cvc, _ends_in_doubled_cons, _m_degree, \
    _sb_ends_in_short_syllable, _sb_has_vowel, _sb_r1, _sb_r2, \
    _sb_short_word, caumanns, clef_german, clef_german_plus, clef_swedish, \
    lovins, paice_husk, porter, porter2, sb_danish, sb_dutch, sb_german, \
    sb_norwegian, sb_swedish, uealite

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
                         encoding='utf-8') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(lovins(word), stem.lower())


class PorterTestCases(unittest.TestCase):
    """Test Porter functions.

    abydos.stemmer._m_degree, abydos.stemmer.porter,
    abydos.stemmer._sb_has_vowel, abydos.stemmer._ends_in_doubled_cons,
    & abydos.stemmer._ends_in_cvc
    """

    def test_m_degree(self):
        """Test abydos.stemmer._m_degree."""
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
        """Test abydos.stemmer._has_vowel."""
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
        """Test abydos.stemmer._ends_in_doubled_cons."""
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
        """Test abydos.stemmer._ends_in_cvc."""
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
        """Test abydos.stemmer.porter."""
        # base case
        self.assertEqual(porter(''), '')

        # simple cases
        self.assertEqual(porter('c'), 'c')
        self.assertEqual(porter('da'), 'da')
        self.assertEqual(porter('ad'), 'ad')
        self.assertEqual(porter('sing'), 'sing')
        self.assertEqual(porter('singing'), 'sing')

        # missed branch test cases
        self.assertEqual(porter('capitalism'), 'capit')
        self.assertEqual(porter('fatalism'), 'fatal')
        self.assertEqual(porter('stional'), 'stional')
        self.assertEqual(porter('palism'), 'palism')
        self.assertEqual(porter('sization'), 'sizat')
        self.assertEqual(porter('licated'), 'licat')
        self.assertEqual(porter('lical'), 'lical')

    def test_porter_early_english(self):
        """Test abydos.stemmer.porter (early English)."""
        # base case
        self.assertEqual(porter('', early_english=True), '')

        # simple cases (no different from regular stemmer)
        self.assertEqual(porter('c', early_english=True), 'c')
        self.assertEqual(porter('da', early_english=True), 'da')
        self.assertEqual(porter('ad', early_english=True), 'ad')
        self.assertEqual(porter('sing', early_english=True), 'sing')
        self.assertEqual(porter('singing', early_english=True), 'sing')

        # make
        self.assertEqual(porter('make', early_english=True), 'make')
        self.assertEqual(porter('makes', early_english=True), 'make')
        self.assertEqual(porter('maketh', early_english=True), 'make')
        self.assertEqual(porter('makest', early_english=True), 'make')

        # say
        self.assertEqual(porter('say', early_english=True), 'sai')
        self.assertEqual(porter('says', early_english=True), 'sai')
        self.assertEqual(porter('sayeth', early_english=True), 'sai')
        self.assertEqual(porter('sayest', early_english=True), 'sai')

        # missed branch test cases
        self.assertEqual(porter('best', early_english=True), 'best')
        self.assertEqual(porter('meth', early_english=True), 'meth')

    def test_porter_snowball(self):
        """Test abydos.stemmer.porter (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/porter/diffs.txt
        """
        #  Snowball Porter test set
        with open(TESTDIR+'/corpora/snowball_porter.csv') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(porter(word), stem.lower())


class Porter2TestCases(unittest.TestCase):
    """Test Porter2 functions.

    abydos.stemmer._sb_r1, abydos.stemmer._sb_r2,
    abydos.stemmer._sb_ends_in_short_syllable, abydos.stemmer._sb_short_word,
    & abydos.stemmer.porter2
    """

    def test_sb_r1(self):
        """Test abydos.stemmer._sb_r1."""
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
        """Test abydos.stemmer._sb_r2."""
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
        """Test abydos.stemmer._sb_ends_in_short_syllable."""
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

        # missed branch test cases
        self.assertFalse(_sb_ends_in_short_syllable('d', _vowels,
                                                    _codanonvowels))
        self.assertFalse(_sb_ends_in_short_syllable('a', _vowels,
                                                    _codanonvowels))

    def test_sb_short_word(self):
        """Test abydos.stemmer._sb_short_word."""
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
        """Test abydos.stemmer.porter2."""
        # base case
        self.assertEqual(porter2(''), '')

        # simple cases
        self.assertEqual(porter2('c'), 'c')
        self.assertEqual(porter2('da'), 'da')
        self.assertEqual(porter2('ad'), 'ad')
        self.assertEqual(porter2('sing'), 'sing')
        self.assertEqual(porter2('singing'), 'sing')

        # missed branch test cases
        self.assertEqual(porter2('capitalism'), 'capit')
        self.assertEqual(porter2('fatalism'), 'fatal')
        self.assertEqual(porter2('dog\'s'), 'dog')
        self.assertEqual(porter2('A\'s\''), 'a')
        self.assertEqual(porter2('agreedly'), 'agre')
        self.assertEqual(porter2('feedly'), 'feed')
        self.assertEqual(porter2('stional'), 'stional')
        self.assertEqual(porter2('palism'), 'palism')
        self.assertEqual(porter2('sization'), 'sizat')
        self.assertEqual(porter2('licated'), 'licat')
        self.assertEqual(porter2('lical'), 'lical')
        self.assertEqual(porter2('clessly'), 'clessli')
        self.assertEqual(porter2('tably'), 'tabli')
        self.assertEqual(porter2('sizer'), 'sizer')
        self.assertEqual(porter2('livity'), 'liviti')

    def test_porter2_early_english(self):
        """Test abydos.stemmer.porter2 (early English)."""
        # base case
        self.assertEqual(porter2('', early_english=True), '')

        # simple cases (no different from regular stemmer)
        self.assertEqual(porter2('c', early_english=True), 'c')
        self.assertEqual(porter2('da', early_english=True), 'da')
        self.assertEqual(porter2('ad', early_english=True), 'ad')
        self.assertEqual(porter2('sing', early_english=True), 'sing')
        self.assertEqual(porter2('singing', early_english=True), 'sing')

        # make
        self.assertEqual(porter2('make', early_english=True), 'make')
        self.assertEqual(porter2('makes', early_english=True), 'make')
        self.assertEqual(porter2('maketh', early_english=True), 'make')
        self.assertEqual(porter2('makest', early_english=True), 'make')

        # say
        self.assertEqual(porter2('say', early_english=True), 'say')
        self.assertEqual(porter2('says', early_english=True), 'say')
        self.assertEqual(porter2('sayeth', early_english=True), 'say')
        self.assertEqual(porter2('sayest', early_english=True), 'say')

        # missed branch test cases
        self.assertEqual(porter2('best', early_english=True), 'best')
        self.assertEqual(porter2('meth', early_english=True), 'meth')

    def test_porter2_snowball(self):
        """Test abydos.stemmer.porter2 (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/english/diffs.txt
        """
        #  Snowball Porter test set
        with open(TESTDIR+'/corpora/snowball_porter2.csv') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(porter2(word), stem.lower())


class SnowballTestCases(unittest.TestCase):
    """Test Snowball functions.

    abydos.stemmer.sb_german, abydos.stemmer.sb_dutch,
    abydos.stemmer.sb_norwegian, abydos.stemmer.sb_swedish, &
    abydos.stemmer.sb_danish
    """

    def test_sb_german_snowball(self):
        """Test abydos.stemmer.sb_german (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/german/diffs.txt
        """
        # base case
        self.assertEqual(sb_german(''), '')

        #  Snowball German test set
        with codecs.open(TESTDIR+'/corpora/snowball_german.csv',
                         encoding='utf-8') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_german(word), stem.lower())

        # missed branch test cases
        self.assertEqual(sb_german('ikeit'), 'ikeit')

    def test_sb_german_snowball_alt(self):
        """Test abydos.stemmer.sb_german (alternate vowels)."""
        # base case
        self.assertEqual(sb_german('', alternate_vowels=True), '')

        # dämmerung,dammer
        self.assertEqual(sb_german('dämmerung', alternate_vowels=True),
                         'dammer')
        self.assertEqual(sb_german('daemmerung', alternate_vowels=True),
                         'dammer')
        self.assertEqual(sb_german('dämmerung'), 'dammer')
        self.assertEqual(sb_german('daemmerung'), 'daemmer')

        # brötchen,brotch
        self.assertEqual(sb_german('brötchen', alternate_vowels=True),
                         'brotch')
        self.assertEqual(sb_german('broetchen', alternate_vowels=True),
                         'brotch')
        self.assertEqual(sb_german('brötchen'), 'brotch')
        self.assertEqual(sb_german('broetchen'), 'broetch')

        # büro,buro
        self.assertEqual(sb_german('büro', alternate_vowels=True), 'buro')
        self.assertEqual(sb_german('buero', alternate_vowels=True), 'buro')
        self.assertEqual(sb_german('büro'), 'buro')
        self.assertEqual(sb_german('buero'), 'buero')

        # häufen,hauf
        self.assertEqual(sb_german('häufen', alternate_vowels=True), 'hauf')
        self.assertEqual(sb_german('haeufen', alternate_vowels=True), 'hauf')
        self.assertEqual(sb_german('häufen'), 'hauf')
        self.assertEqual(sb_german('haeufen'), 'haeuf')

        # quelle,quell
        self.assertEqual(sb_german('qülle', alternate_vowels=True), 'qull')
        self.assertEqual(sb_german('quelle', alternate_vowels=True), 'quell')
        self.assertEqual(sb_german('qülle'), 'qull')
        self.assertEqual(sb_german('quelle'), 'quell')

        # feuer,feuer
        self.assertEqual(sb_german('feür', alternate_vowels=True), 'feur')
        self.assertEqual(sb_german('feuer', alternate_vowels=True), 'feu')
        self.assertEqual(sb_german('feür'), 'feur')
        self.assertEqual(sb_german('feuer'), 'feu')

        # über,uber
        self.assertEqual(sb_german('über', alternate_vowels=True), 'uber')
        self.assertEqual(sb_german('ueber', alternate_vowels=True), 'uber')
        self.assertEqual(sb_german('über'), 'uber')
        self.assertEqual(sb_german('ueber'), 'ueb')

    def test_sb_dutch_snowball(self):
        """Test abydos.stemmer.sb_dutch (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/dutch/diffs.txt
        """
        # base case
        self.assertEqual(sb_dutch(''), '')

        #  Snowball Dutch test set
        with codecs.open(TESTDIR+'/corpora/snowball_dutch.csv',
                         encoding='utf-8') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_dutch(word), stem.lower())

        # missed branch test cases
        self.assertEqual(sb_dutch('zondulielijk'), 'zondulie')

    def test_sb_norwegian_snowball(self):
        """Test abydos.stemmer.sb_norwegian (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/norwegian/diffs.txt
        """
        # base case
        self.assertEqual(sb_norwegian(''), '')

        #  Snowball Norwegian test set
        with codecs.open(TESTDIR+'/corpora/snowball_norwegian.csv',
                         encoding='utf-8') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_norwegian(word), stem.lower())

    def test_sb_swedish_snowball(self):
        """Test abydos.stemmer.sb_swedish (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/swedish/diffs.txt
        """
        # base case
        self.assertEqual(sb_swedish(''), '')

        #  Snowball Swedish test set
        with codecs.open(TESTDIR+'/corpora/snowball_swedish.csv',
                         encoding='utf-8') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_swedish(word), stem.lower())

    def test_sb_danish_snowball(self):
        """Test abydos.stemmer.sb_danish (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/danish/diffs.txt
        """
        # base case
        self.assertEqual(sb_danish(''), '')

        #  Snowball Danish test set
        with codecs.open(TESTDIR+'/corpora/snowball_danish.csv',
                         encoding='utf-8') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_danish(word), stem.lower())


class CLEFTestCases(unittest.TestCase):
    """Test CLEF functions.

    abydos.stemmer.clef_german, abydos.stemmer.clef_german_plus, &
    abydos.stemmer.clef_swedish
    """

    def test_clef_german(self):
        """Test abydos.stemmer.clef_german."""
        # base case
        self.assertEqual(clef_german(''), '')

        # len <= 2
        self.assertEqual(clef_german('ä'), 'a')
        self.assertEqual(clef_german('er'), 'er')
        self.assertEqual(clef_german('es'), 'es')
        self.assertEqual(clef_german('äh'), 'ah')

        # len > 2
        self.assertEqual(clef_german('deinen'), 'dein')
        self.assertEqual(clef_german('können'), 'konn')
        self.assertEqual(clef_german('Damen'), 'dame')
        self.assertEqual(clef_german('kleines'), 'klein')
        self.assertEqual(clef_german('Namen'), 'name')
        self.assertEqual(clef_german('Äpfel'), 'apfel')
        self.assertEqual(clef_german('Jahre'), 'jahr')
        self.assertEqual(clef_german('Mannes'), 'mann')
        self.assertEqual(clef_german('Häuser'), 'haus')
        self.assertEqual(clef_german('Motoren'), 'motor')
        self.assertEqual(clef_german('kleine'), 'klein')
        self.assertEqual(clef_german('Pfingsten'), 'pfingst')
        self.assertEqual(clef_german('lautest'), 'lautest')
        self.assertEqual(clef_german('lauteste'), 'lautest')
        self.assertEqual(clef_german('lautere'), 'lauter')
        self.assertEqual(clef_german('lautste'), 'lautst')
        self.assertEqual(clef_german('kleinen'), 'klei')

    def test_clef_german_plus(self):
        """Test abydos.stemmer.clef_german_plus."""
        # base case
        self.assertEqual(clef_german_plus(''), '')

        # len <= 2
        self.assertEqual(clef_german_plus('ä'), 'a')
        self.assertEqual(clef_german_plus('er'), 'er')
        self.assertEqual(clef_german_plus('es'), 'es')
        self.assertEqual(clef_german_plus('äh'), 'ah')

        # len > 2
        self.assertEqual(clef_german_plus('deinen'), 'dein')
        self.assertEqual(clef_german_plus('können'), 'konn')
        self.assertEqual(clef_german_plus('Damen'), 'dam')
        self.assertEqual(clef_german_plus('kleines'), 'klein')
        self.assertEqual(clef_german_plus('Namen'), 'nam')
        self.assertEqual(clef_german_plus('Äpfel'), 'apfel')
        self.assertEqual(clef_german_plus('Jahre'), 'jahr')
        self.assertEqual(clef_german_plus('Mannes'), 'mann')
        self.assertEqual(clef_german_plus('Häuser'), 'haus')
        self.assertEqual(clef_german_plus('Motoren'), 'motor')
        self.assertEqual(clef_german_plus('kleine'), 'klein')
        self.assertEqual(clef_german_plus('Pfingsten'), 'pfing')
        self.assertEqual(clef_german_plus('lautest'), 'laut')
        self.assertEqual(clef_german_plus('lauteste'), 'laut')
        self.assertEqual(clef_german_plus('lautere'), 'laut')
        self.assertEqual(clef_german_plus('lautste'), 'laut')
        self.assertEqual(clef_german_plus('kleinen'), 'klein')
        self.assertEqual(clef_german_plus('Pfarrern'), 'pfarr')

    def test_clef_swedish(self):
        """Test abydos.stemmer.clef_swedish."""
        # base case
        self.assertEqual(clef_swedish(''), '')

        # unstemmed
        self.assertEqual(clef_swedish('konung'), 'konung')

        # len <= 3
        self.assertEqual(clef_swedish('km'), 'km')
        self.assertEqual(clef_swedish('ja'), 'ja')
        self.assertEqual(clef_swedish('de'), 'de')
        self.assertEqual(clef_swedish('in'), 'in')
        self.assertEqual(clef_swedish('a'), 'a')
        self.assertEqual(clef_swedish('mer'), 'mer')
        self.assertEqual(clef_swedish('s'), 's')
        self.assertEqual(clef_swedish('e'), 'e')
        self.assertEqual(clef_swedish('oss'), 'oss')
        self.assertEqual(clef_swedish('hos'), 'hos')

        # genitive
        self.assertEqual(clef_swedish('svenskars'), 'svensk')
        self.assertEqual(clef_swedish('stadens'), 'stad')
        self.assertEqual(clef_swedish('kommuns'), 'kommu')
        self.assertEqual(clef_swedish('aftonbladets'), 'aftonblad')

        # len > 7
        self.assertEqual(clef_swedish('fängelser'), 'fäng')
        self.assertEqual(clef_swedish('möjligheten'), 'möjlig')

        # len > 6
        self.assertEqual(clef_swedish('svenskar'), 'svensk')
        self.assertEqual(clef_swedish('myndigheterna'), 'myndighet')
        self.assertEqual(clef_swedish('avgörande'), 'avgör')
        self.assertEqual(clef_swedish('fängelse'), 'fäng')
        self.assertEqual(clef_swedish('viktigaste'), 'viktig')
        self.assertEqual(clef_swedish('kvinnorna'), 'kvinn')
        self.assertEqual(clef_swedish('åklagaren'), 'åklag')

        # len > 5
        self.assertEqual(clef_swedish('tidigare'), 'tidig')
        self.assertEqual(clef_swedish('senast'), 'sen')
        self.assertEqual(clef_swedish('möjlighet'), 'möjlig')

        # len > 4
        self.assertEqual(clef_swedish('svenskar'), 'svensk')
        self.assertEqual(clef_swedish('skriver'), 'skriv')
        self.assertEqual(clef_swedish('människor'), 'människ')
        self.assertEqual(clef_swedish('staden'), 'stad')
        self.assertEqual(clef_swedish('kunnat'), 'kunn')
        self.assertEqual(clef_swedish('samarbete'), 'samarbe')
        self.assertEqual(clef_swedish('aftonbladet'), 'aftonblad')

        # len > 3
        self.assertEqual(clef_swedish('allt'), 'all')
        self.assertEqual(clef_swedish('vilka'), 'vilk')
        self.assertEqual(clef_swedish('länge'), 'läng')
        self.assertEqual(clef_swedish('kommun'), 'kommu')


class CaumannsTestCases(unittest.TestCase):
    """Test Caumanns functions.

    abydos.stemmer.caumanns
    """

    def test_caumanns(self):
        """Test abydos.stemmer.caumanns."""
        # base case
        self.assertEqual(caumanns(''), '')

        # tests from Caumanns' description of the algorithm
        self.assertEqual(caumanns('singt'), 'sing')
        self.assertEqual(caumanns('singen'), 'sing')
        self.assertEqual(caumanns('beliebt'), 'belieb')
        self.assertEqual(caumanns('beliebtester'), 'belieb')
        self.assertEqual(caumanns('stören'), 'stor')
        self.assertEqual(caumanns('stöhnen'), 'stoh')
        self.assertEqual(caumanns('Kuß'), 'kuss')
        self.assertEqual(caumanns('Küsse'), 'kuss')
        self.assertEqual(caumanns('Verlierer'), 'verlier')
        self.assertEqual(caumanns('Verlies'), 'verlie')
        self.assertEqual(caumanns('Maus'), 'mau')
        self.assertEqual(caumanns('Mauer'), 'mau')
        self.assertEqual(caumanns('Störsender'), 'stor')

        # additional tests to achieve full coverage
        self.assertEqual(caumanns('Müllerinnen'), 'mullerin')
        self.assertEqual(caumanns('Matrix'), 'matrix')
        self.assertEqual(caumanns('Matrizen'), 'matrix')

    def test_caumanns_lucene(self):
        """Test abydos.stemmer.caumanns (Lucene tests).

        Based on tests from
        https://svn.apache.org/repos/asf/lucene.net/trunk/test/contrib/Analyzers/De/data.txt
        This is presumably Apache-licensed.
        """
        # German special characters are replaced:
        self.assertEqual(caumanns('häufig'), 'haufig')
        self.assertEqual(caumanns('üor'), 'uor')
        self.assertEqual(caumanns('björk'), 'bjork')

        # here the stemmer works okay, it maps related words to the same stem:
        self.assertEqual(caumanns('abschließen'), 'abschliess')
        self.assertEqual(caumanns('abschließender'), 'abschliess')
        self.assertEqual(caumanns('abschließendes'), 'abschliess')
        self.assertEqual(caumanns('abschließenden'), 'abschliess')

        self.assertEqual(caumanns('Tisch'), 'tisch')
        self.assertEqual(caumanns('Tische'), 'tisch')
        self.assertEqual(caumanns('Tischen'), 'tisch')
        self.assertEqual(caumanns('geheimtür'), 'geheimtur')

        self.assertEqual(caumanns('Haus'), 'hau')
        self.assertEqual(caumanns('Hauses'), 'hau')
        self.assertEqual(caumanns('Häuser'), 'hau')
        self.assertEqual(caumanns('Häusern'), 'hau')
        # here's a case where overstemming occurs, i.e. a word is
        # mapped to the same stem as unrelated words:
        self.assertEqual(caumanns('hauen'), 'hau')

        # here's a case where understemming occurs, i.e. two related words
        # are not mapped to the same stem. This is the case with basically
        # all irregular forms:
        self.assertEqual(caumanns('Drama'), 'drama')
        self.assertEqual(caumanns('Dramen'), 'dram')

        # replace "ß" with 'ss':
        self.assertEqual(caumanns('Ausmaß'), 'ausmass')

        # fake words to test if suffixes are cut off:
        self.assertEqual(caumanns('xxxxxe'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxs'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxn'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxt'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxem'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxer'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxnd'), 'xxxxx')
        # the suffixes are also removed when combined:
        self.assertEqual(caumanns('xxxxxetende'), 'xxxxx')

        # words that are shorter than four charcters are not changed:
        self.assertEqual(caumanns('xxe'), 'xxe')
        # -em and -er are not removed from words shorter than five characters:
        self.assertEqual(caumanns('xxem'), 'xxem')
        self.assertEqual(caumanns('xxer'), 'xxer')
        # -nd is not removed from words shorter than six characters:
        self.assertEqual(caumanns('xxxnd'), 'xxxnd')


class UEALiteTestCases(unittest.TestCase):
    """Test UEA-lite functions.

    abydos.stemmer.uealite
    """

    def test_uealite(self):
        """Test abydos.stemmer.uealite."""
        # base case
        self.assertEqual(uealite(''), '')

        # test cases copied from Ruby port
        # https://github.com/ealdent/uea-stemmer/blob/master/test/uea_stemmer_test.rb
        # These are corrected to match the Java version's output.
        # stem base words to just the base word
        self.assertEqual(uealite('man'), 'man')
        self.assertEqual(uealite('happiness'), 'happiness')
        # stem theses as thesis but not bases as basis
        self.assertEqual(uealite('theses'), 'thesis')
        self.assertNotEqual(uealite('bases'), 'basis')
        # stem preterite words ending in -ed without the -ed
        self.assertEqual(uealite('ordained'), 'ordain')
        self.assertEqual(uealite('killed'), 'kill')
        self.assertEqual(uealite('liked'), 'lik')
        self.assertEqual(uealite('helped'), 'help')
        self.assertEqual(uealite('scarred'), 'scarre')
        self.assertEqual(uealite('invited'), 'invit')
        self.assertEqual(uealite('exited'), 'exit')
        self.assertEqual(uealite('debited'), 'debit')
        self.assertEqual(uealite('smited'), 'smit')
        # stem progressive verbs and gerunds without the -ing
        self.assertEqual(uealite('running'), 'run')
        self.assertEqual(uealite('settings'), 'set')
        self.assertEqual(uealite('timing'), 'time')
        self.assertEqual(uealite('dying'), 'dy')
        self.assertEqual(uealite('harping'), 'harp')
        self.assertEqual(uealite('charring'), 'char')
        # not stem false progressive verbs such as 'sing'
        self.assertEqual(uealite('ring'), 'ring')
        self.assertEqual(uealite('sing'), 'se')
        self.assertEqual(uealite('bring'), 'br')
        self.assertEqual(uealite('fling'), 'fle')
        # stem various plural nouns and 3rd-pres verbs without the -s/-es
        self.assertEqual(uealite('changes'), 'change')
        self.assertEqual(uealite('deaths'), 'death')
        self.assertEqual(uealite('shadows'), 'shadow')
        self.assertEqual(uealite('flies'), 'fly')
        self.assertEqual(uealite('things'), 'thing')
        self.assertEqual(uealite('nothings'), 'nothing')
        self.assertEqual(uealite('witches'), 'witch')
        self.assertEqual(uealite('makes'), 'mak')
        self.assertEqual(uealite('smokes'), 'smok')
        self.assertEqual(uealite('does'), 'do')
        # stem various words with -des suffix
        self.assertEqual(uealite('abodes'), 'abod')
        self.assertEqual(uealite('escapades'), 'escapad')
        self.assertEqual(uealite('crusades'), 'crusad')
        self.assertEqual(uealite('grades'), 'grad')
        # stem various words with -res suffix
        self.assertEqual(uealite('wires'), 'wir')
        self.assertEqual(uealite('acres'), 'acr')
        self.assertEqual(uealite('fires'), 'fir')
        self.assertEqual(uealite('cares'), 'car')
        # stem acronyms when pluralized otherwise they should be left alone
        self.assertEqual(uealite('USA'), 'USA')
        self.assertEqual(uealite('FLOSS'), 'FLOSS')
        self.assertEqual(uealite('MREs'), 'MRE')
        self.assertEqual(uealite('USAED'), 'USAED')

        # test cases copied from Ruby port
        # https://github.com/ealdent/uea-stemmer/blob/master/test/uea_stemmer_test.rb
        # stem base words to just the base word
        self.assertEqual(uealite('man', var='Adams'), 'man')
        self.assertEqual(uealite('happiness', var='Adams'), 'happiness')
        # stem theses as thesis but not bases as basis
        self.assertEqual(uealite('theses', var='Adams'), 'thesis')
        self.assertNotEqual(uealite('bases', var='Adams'), 'basis')
        # stem preterite words ending in -ed without the -ed
        self.assertEqual(uealite('ordained', var='Adams'), 'ordain')
        self.assertEqual(uealite('killed', var='Adams'), 'kill')
        self.assertEqual(uealite('liked', var='Adams'), 'like')
        self.assertEqual(uealite('helped', var='Adams'), 'help')
        # self.assertEqual(uealite('scarred', var='Adams'), 'scar')
        self.assertEqual(uealite('invited', var='Adams'), 'invite')
        self.assertEqual(uealite('exited', var='Adams'), 'exit')
        self.assertEqual(uealite('debited', var='Adams'), 'debit')
        self.assertEqual(uealite('smited', var='Adams'), 'smite')
        # stem progressive verbs and gerunds without the -ing
        self.assertEqual(uealite('running', var='Adams'), 'run')
        self.assertEqual(uealite('settings', var='Adams'), 'set')
        self.assertEqual(uealite('timing', var='Adams'), 'time')
        self.assertEqual(uealite('dying', var='Adams'), 'die')
        self.assertEqual(uealite('harping', var='Adams'), 'harp')
        self.assertEqual(uealite('charring', var='Adams'), 'char')
        # not stem false progressive verbs such as 'sing'
        self.assertEqual(uealite('ring', var='Adams'), 'ring')
        self.assertEqual(uealite('sing', var='Adams'), 'sing')
        self.assertEqual(uealite('ring', var='Adams'), 'ring')
        self.assertEqual(uealite('bring', var='Adams'), 'bring')
        self.assertEqual(uealite('fling', var='Adams'), 'fling')
        # stem various plural nouns and 3rd-pres verbs without the -s/-es
        self.assertEqual(uealite('changes', var='Adams'), 'change')
        self.assertEqual(uealite('deaths', var='Adams'), 'death')
        self.assertEqual(uealite('shadows', var='Adams'), 'shadow')
        self.assertEqual(uealite('flies', var='Adams'), 'fly')
        self.assertEqual(uealite('things', var='Adams'), 'thing')
        self.assertEqual(uealite('nothings', var='Adams'), 'nothing')
        self.assertEqual(uealite('witches', var='Adams'), 'witch')
        self.assertEqual(uealite('makes', var='Adams'), 'make')
        self.assertEqual(uealite('smokes', var='Adams'), 'smoke')
        self.assertEqual(uealite('does', var='Adams'), 'do')
        # stem various words with -des suffix
        self.assertEqual(uealite('abodes', var='Adams'), 'abode')
        self.assertEqual(uealite('escapades', var='Adams'), 'escapade')
        self.assertEqual(uealite('crusades', var='Adams'), 'crusade')
        self.assertEqual(uealite('grades', var='Adams'), 'grade')
        # stem various words with -res suffix
        self.assertEqual(uealite('wires', var='Adams'), 'wire')
        self.assertEqual(uealite('acres', var='Adams'), 'acre')
        self.assertEqual(uealite('fires', var='Adams'), 'fire')
        self.assertEqual(uealite('cares', var='Adams'), 'care')
        # stem acronyms when pluralized otherwise they should be left alone
        self.assertEqual(uealite('USA', var='Adams'), 'USA')
        self.assertEqual(uealite('FLOSS', var='Adams'), 'FLOSS')
        self.assertEqual(uealite('MREs', var='Adams'), 'MRE')
        self.assertEqual(uealite('USAED', var='Adams'), 'USAED')

    def test_uealite_wsj_set(self):
        """Test abydos.stemmer.uealite (WSJ testset)."""
        with open(TESTDIR + '/corpora/uea-lite_wsj.csv') as wsj_testset:
            for wsj_line in wsj_testset:
                (word, uea, rule) = wsj_line.strip().split(',')
                self.assertEqual(uealite(word, return_rule_no=True),
                                 (uea, float(rule)))


class PaiceHuskTestCases(unittest.TestCase):
    """Test Paice-Husk functions.

    abydos.stemmer.paice_husk
    """

    def test_paice_husk(self):
        """Test abydos.stemmer.paice_husk."""
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
        """Test abydos.stemmer.paice_husk (Hopper262 testset).

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
        with open(TESTDIR + '/corpora/paicehusk.csv') as hopper_testset:
            for hopper_line in hopper_testset:
                (word, stem) = hopper_line.strip().split(',')
                self.assertEqual(paice_husk(word), stem)


if __name__ == '__main__':
    unittest.main()
