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

"""abydos.tests.stemmer.test_stemmer_snowball.

This module contains unit tests for abydos.stemmer.snowball
"""

from __future__ import unicode_literals

import codecs
import unittest

from abydos.stemmer.snowball import (
    _ends_in_cvc,
    _ends_in_doubled_cons,
    _m_degree,
    _sb_ends_in_short_syllable,
    _sb_has_vowel,
    _sb_r1,
    _sb_r2,
    _sb_short_word,
    porter,
    porter2,
    sb_danish,
    sb_dutch,
    sb_german,
    sb_norwegian,
    sb_swedish,
)

from .. import _corpus_file


class PorterTestCases(unittest.TestCase):
    """Test Porter functions.

    abydos.stemmer.snowball._m_degree, .porter, ._sb_has_vowel,
    ._ends_in_doubled_cons, & ._ends_in_cvc
    """

    def test_m_degree(self):
        """Test abydos.stemmer.snowball._m_degree."""
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
        """Test abydos.stemmer.snowball._has_vowel."""
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
        """Test abydos.stemmer.snowball._ends_in_doubled_cons."""
        _vowels = set('aeiouy')
        # base case
        self.assertFalse(_ends_in_doubled_cons('', _vowels))

        # False cases
        self.assertFalse(_ends_in_doubled_cons('b', _vowels))
        self.assertFalse(_ends_in_doubled_cons('c', _vowels))
        self.assertFalse(_ends_in_doubled_cons('bc', _vowels))
        self.assertFalse(
            _ends_in_doubled_cons('bcdfghjklmnpqrstvwxYz', _vowels)
        )
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
        """Test abydos.stemmer.snowball._ends_in_cvc."""
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
        """Test abydos.stemmer.snowball.porter."""
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
        """Test abydos.stemmer.snowball.porter (early English)."""
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
        """Test abydos.stemmer.snowball.porter (Snowball testset).

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
                    self.assertEqual(porter(word), stem.lower())


class Porter2TestCases(unittest.TestCase):
    """Test Porter2 functions.

    abydos.stemmer.snowball._sb_r1, ._sb_r2, ._sb_ends_in_short_syllable,
    ._sb_short_word, & .porter2
    """

    def test_sb_r1(self):
        """Test abydos.stemmer.snowball._sb_r1."""
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
        """Test abydos.stemmer.snowball._sb_r2."""
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
        """Test abydos.stemmer.snowball._sb_ends_in_short_syllable."""
        _vowels = set('aeiouy')
        _codanonvowels = set('bcdfghjklmnpqrstvz\'')
        # base case
        self.assertFalse(
            _sb_ends_in_short_syllable('', _vowels, _codanonvowels)
        )

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(
            _sb_ends_in_short_syllable('rap', _vowels, _codanonvowels)
        )
        self.assertTrue(
            _sb_ends_in_short_syllable('trap', _vowels, _codanonvowels)
        )
        self.assertTrue(
            _sb_ends_in_short_syllable('entrap', _vowels, _codanonvowels)
        )
        self.assertTrue(
            _sb_ends_in_short_syllable('ow', _vowels, _codanonvowels)
        )
        self.assertTrue(
            _sb_ends_in_short_syllable('on', _vowels, _codanonvowels)
        )
        self.assertTrue(
            _sb_ends_in_short_syllable('at', _vowels, _codanonvowels)
        )
        self.assertFalse(
            _sb_ends_in_short_syllable('uproot', _vowels, _codanonvowels)
        )
        self.assertFalse(
            _sb_ends_in_short_syllable('uproot', _vowels, _codanonvowels)
        )
        self.assertFalse(
            _sb_ends_in_short_syllable('bestow', _vowels, _codanonvowels)
        )
        self.assertFalse(
            _sb_ends_in_short_syllable('disturb', _vowels, _codanonvowels)
        )

        # missed branch test cases
        self.assertFalse(
            _sb_ends_in_short_syllable('d', _vowels, _codanonvowels)
        )
        self.assertFalse(
            _sb_ends_in_short_syllable('a', _vowels, _codanonvowels)
        )

    def test_sb_short_word(self):
        """Test abydos.stemmer.snowball._sb_short_word."""
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
        """Test abydos.stemmer.snowball.porter2."""
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
        """Test abydos.stemmer.snowball.porter2 (early English)."""
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
        """Test abydos.stemmer.snowball.porter2 (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/english/diffs.txt
        """
        #  Snowball Porter test set
        with open(_corpus_file('snowball_porter2.csv')) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(porter2(word), stem.lower())


class SnowballTestCases(unittest.TestCase):
    """Test Snowball functions.

    abydos.stemmer.snowball.sb_german, .sb_dutch, .sb_norwegian, .sb_swedish, &
    .sb_danish
    """

    def test_sb_german_snowball(self):
        """Test abydos.stemmer.snowball.sb_german (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/german/diffs.txt
        """
        # base case
        self.assertEqual(sb_german(''), '')

        #  Snowball German test set
        with codecs.open(
            _corpus_file('snowball_german.csv'), encoding='utf-8'
        ) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_german(word), stem.lower())

        # missed branch test cases
        self.assertEqual(sb_german('ikeit'), 'ikeit')

    def test_sb_german_snowball_alt(self):
        """Test abydos.stemmer.snowball.sb_german (alternate vowels)."""
        # base case
        self.assertEqual(sb_german('', alternate_vowels=True), '')

        # dämmerung,dammer
        self.assertEqual(
            sb_german('dämmerung', alternate_vowels=True), 'dammer'
        )
        self.assertEqual(
            sb_german('daemmerung', alternate_vowels=True), 'dammer'
        )
        self.assertEqual(sb_german('dämmerung'), 'dammer')
        self.assertEqual(sb_german('daemmerung'), 'daemmer')

        # brötchen,brotch
        self.assertEqual(
            sb_german('brötchen', alternate_vowels=True), 'brotch'
        )
        self.assertEqual(
            sb_german('broetchen', alternate_vowels=True), 'brotch'
        )
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
        """Test abydos.stemmer.snowball.sb_dutch (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/dutch/diffs.txt
        """
        # base case
        self.assertEqual(sb_dutch(''), '')

        #  Snowball Dutch test set
        with codecs.open(
            _corpus_file('snowball_dutch.csv'), encoding='utf-8'
        ) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_dutch(word), stem.lower())

        # missed branch test cases
        self.assertEqual(sb_dutch('zondulielijk'), 'zondulie')

    def test_sb_norwegian_snowball(self):
        """Test abydos.stemmer.snowball.sb_norwegian (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/norwegian/diffs.txt
        """
        # base case
        self.assertEqual(sb_norwegian(''), '')

        #  Snowball Norwegian test set
        with codecs.open(
            _corpus_file('snowball_norwegian.csv'), encoding='utf-8'
        ) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_norwegian(word), stem.lower())

    def test_sb_swedish_snowball(self):
        """Test abydos.stemmer.snowball.sb_swedish (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/swedish/diffs.txt
        """
        # base case
        self.assertEqual(sb_swedish(''), '')

        #  Snowball Swedish test set
        with codecs.open(
            _corpus_file('snowball_swedish.csv'), encoding='utf-8'
        ) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_swedish(word), stem.lower())

    def test_sb_danish_snowball(self):
        """Test abydos.stemmer.snowball.sb_danish (Snowball testset).

        These test cases are from
        http://snowball.tartarus.org/algorithms/danish/diffs.txt
        """
        # base case
        self.assertEqual(sb_danish(''), '')

        #  Snowball Danish test set
        with codecs.open(
            _corpus_file('snowball_danish.csv'), encoding='utf-8'
        ) as snowball_ts:
            next(snowball_ts)
            for line in snowball_ts:
                if line[0] != '#':
                    line = line.strip().split(',')
                    word, stem = line[0], line[1]
                    self.assertEqual(sb_danish(word), stem.lower())


if __name__ == '__main__':
    unittest.main()
