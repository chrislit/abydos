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

This module contains unit tests for abydos.stemmer._snowball
"""

from __future__ import unicode_literals

import codecs
import unittest

from abydos.stemmer import (
    Porter,
    porter,
    porter2,
    sb_danish,
    sb_dutch,
    sb_german,
    sb_norwegian,
    sb_swedish,
)

# noinspection PyProtectedMember
from abydos.stemmer._Snowball import _Snowball

from .. import _corpus_file


class PorterTestCases(unittest.TestCase):
    """Test Porter functions.

    abydos.stemmer._snowball.Porter._m_degree, .porter, ._has_vowel,
    ._ends_in_doubled_cons, & ._ends_in_cvc
    """

    def test_m_degree(self):
        """Test abydos.stemmer._snowball.Porter._m_degree."""
        stmr = Porter()
        stmr._vowels = set('aeiouy')  # noqa: SF01

        # base case
        self.assertEqual(stmr._m_degree(''), 0)  # noqa: SF01

        # m==0
        self.assertEqual(stmr._m_degree('tr'), 0)  # noqa: SF01
        self.assertEqual(stmr._m_degree('ee'), 0)  # noqa: SF01
        self.assertEqual(stmr._m_degree('tree'), 0)  # noqa: SF01
        self.assertEqual(stmr._m_degree('y'), 0)  # noqa: SF01
        self.assertEqual(stmr._m_degree('by'), 0)  # noqa: SF01

        # m==1
        self.assertEqual(stmr._m_degree('trouble'), 1)  # noqa: SF01
        self.assertEqual(stmr._m_degree('oats'), 1)  # noqa: SF01
        self.assertEqual(stmr._m_degree('trees'), 1)  # noqa: SF01
        self.assertEqual(stmr._m_degree('ivy'), 1)  # noqa: SF01

        # m==2
        self.assertEqual(stmr._m_degree('troubles'), 2)  # noqa: SF01
        self.assertEqual(stmr._m_degree('private'), 2)  # noqa: SF01
        self.assertEqual(stmr._m_degree('oaten'), 2)  # noqa: SF01
        self.assertEqual(stmr._m_degree('orrery'), 2)  # noqa: SF01

    def test_has_vowel(self):
        """Test abydos.stemmer._snowball.Porter._has_vowel."""
        stmr = Porter()
        stmr._vowels = set('aeiouy')  # noqa: SF01

        # base case
        self.assertFalse(stmr._has_vowel(''))  # noqa: SF01

        # False cases
        self.assertFalse(stmr._has_vowel('b'))  # noqa: SF01
        self.assertFalse(stmr._has_vowel('c'))  # noqa: SF01
        self.assertFalse(stmr._has_vowel('bc'))  # noqa: SF01
        self.assertFalse(
            stmr._has_vowel('bcdfghjklmnpqrstvwxYz')  # noqa: SF01
        )
        self.assertFalse(stmr._has_vowel('Y'))  # noqa: SF01

        # True cases
        self.assertTrue(stmr._has_vowel('a'))  # noqa: SF01
        self.assertTrue(stmr._has_vowel('e'))  # noqa: SF01
        self.assertTrue(stmr._has_vowel('ae'))  # noqa: SF01
        self.assertTrue(stmr._has_vowel('aeiouy'))  # noqa: SF01
        self.assertTrue(stmr._has_vowel('y'))  # noqa: SF01

        self.assertTrue(stmr._has_vowel('ade'))  # noqa: SF01
        self.assertTrue(stmr._has_vowel('cad'))  # noqa: SF01
        self.assertTrue(stmr._has_vowel('add'))  # noqa: SF01
        self.assertTrue(stmr._has_vowel('phi'))  # noqa: SF01
        self.assertTrue(stmr._has_vowel('pfy'))  # noqa: SF01

        self.assertFalse(stmr._has_vowel('pfY'))  # noqa: SF01

    def test_ends_in_doubled_cons(self):
        """Test abydos.stemmer._snowball.Porter._ends_in_doubled_cons."""
        stmr = Porter()
        stmr._vowels = set('aeiouy')  # noqa: SF01

        # base case
        self.assertFalse(stmr._ends_in_doubled_cons(''))  # noqa: SF01

        # False cases
        self.assertFalse(stmr._ends_in_doubled_cons('b'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('c'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('bc'))  # noqa: SF01
        self.assertFalse(
            stmr._ends_in_doubled_cons('bcdfghjklmnpqrstvwxYz')  # noqa: SF01
        )
        self.assertFalse(stmr._ends_in_doubled_cons('Y'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('a'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('e'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('ae'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('aeiouy'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('y'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('ade'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('cad'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('phi'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('pfy'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('faddy'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('aiii'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_doubled_cons('ayyy'))  # noqa: SF01

        # True cases
        self.assertTrue(stmr._ends_in_doubled_cons('add'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_doubled_cons('fadd'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_doubled_cons('fadddd'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_doubled_cons('raYY'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_doubled_cons('doll'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_doubled_cons('parr'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_doubled_cons('parrr'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_doubled_cons('bacc'))  # noqa: SF01

    def test_ends_in_cvc(self):
        """Test abydos.stemmer._snowball.Porter._ends_in_cvc."""
        stmr = Porter()
        stmr._vowels = set('aeiouy')  # noqa: SF01

        # base case
        self.assertFalse(stmr._ends_in_cvc(''))  # noqa: SF01

        # False cases
        self.assertFalse(stmr._ends_in_cvc('b'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_cvc('c'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_cvc('bc'))  # noqa: SF01
        self.assertFalse(
            stmr._ends_in_cvc('bcdfghjklmnpqrstvwxYz')  # noqa: SF01
        )
        self.assertFalse(stmr._ends_in_cvc('YYY'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_cvc('ddd'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_cvc('faaf'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_cvc('rare'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_cvc('rhy'))  # noqa: SF01

        # True cases
        self.assertTrue(stmr._ends_in_cvc('dad'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_cvc('phad'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_cvc('faded'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_cvc('maYor'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_cvc('enlil'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_cvc('parer'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_cvc('padres'))  # noqa: SF01
        self.assertTrue(stmr._ends_in_cvc('bacyc'))  # noqa: SF01

        # Special case for W, X, & Y
        self.assertFalse(stmr._ends_in_cvc('craw'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_cvc('max'))  # noqa: SF01
        self.assertFalse(stmr._ends_in_cvc('cray'))  # noqa: SF01

    def test_porter(self):
        """Test abydos.stemmer._snowball.porter."""
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
        """Test abydos.stemmer._snowball.porter (early English)."""
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
        """Test abydos.stemmer._snowball.porter (Snowball testset).

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

    abydos.stemmer._snowball.Snowball._sb_has_vowels, _sb_r1, ._sb_r2,
    ._sb_ends_in_short_syllable, ._sb_short_word, &
    abydos.stemmer._snowball.porter2
    """

    def test_has_vowel(self):
        """Test abydos.stemmer._snowball.Snowball._has_vowel."""
        stmr = _Snowball()
        stmr._vowels = set('aeiouy')  # noqa: SF01

        # base case
        self.assertFalse(stmr._sb_has_vowel(''))  # noqa: SF01

        # False cases
        self.assertFalse(stmr._sb_has_vowel('b'))  # noqa: SF01
        self.assertFalse(stmr._sb_has_vowel('c'))  # noqa: SF01
        self.assertFalse(stmr._sb_has_vowel('bc'))  # noqa: SF01
        self.assertFalse(
            stmr._sb_has_vowel('bcdfghjklmnpqrstvwxYz')  # noqa: SF01
        )
        self.assertFalse(stmr._sb_has_vowel('Y'))  # noqa: SF01

        # True cases
        self.assertTrue(stmr._sb_has_vowel('a'))  # noqa: SF01
        self.assertTrue(stmr._sb_has_vowel('e'))  # noqa: SF01
        self.assertTrue(stmr._sb_has_vowel('ae'))  # noqa: SF01
        self.assertTrue(stmr._sb_has_vowel('aeiouy'))  # noqa: SF01
        self.assertTrue(stmr._sb_has_vowel('y'))  # noqa: SF01

        self.assertTrue(stmr._sb_has_vowel('ade'))  # noqa: SF01
        self.assertTrue(stmr._sb_has_vowel('cad'))  # noqa: SF01
        self.assertTrue(stmr._sb_has_vowel('add'))  # noqa: SF01
        self.assertTrue(stmr._sb_has_vowel('phi'))  # noqa: SF01
        self.assertTrue(stmr._sb_has_vowel('pfy'))  # noqa: SF01

        self.assertFalse(stmr._sb_has_vowel('pfY'))  # noqa: SF01

    def test_sb_r1(self):
        """Test abydos.stemmer._snowball.Snowball._sb_r1."""
        stmr = _Snowball()
        stmr._vowels = set('aeiouy')  # noqa: SF01

        # base case
        self.assertEqual(stmr._sb_r1(''), 0)  # noqa: SF01

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(stmr._sb_r1('beautiful'), 5)  # noqa: SF01
        self.assertEqual(stmr._sb_r1('beauty'), 5)  # noqa: SF01
        self.assertEqual(stmr._sb_r1('beau'), 4)  # noqa: SF01
        self.assertEqual(stmr._sb_r1('animadversion'), 2)  # noqa: SF01
        self.assertEqual(stmr._sb_r1('sprinkled'), 5)  # noqa: SF01
        self.assertEqual(stmr._sb_r1('eucharist'), 3)  # noqa: SF01

    def test_sb_r2(self):
        """Test abydos.stemmer._snowball.Snowball._sb_r2."""
        stmr = _Snowball()
        stmr._vowels = set('aeiouy')  # noqa: SF01

        # base case
        self.assertEqual(stmr._sb_r2(''), 0)  # noqa: SF01

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(stmr._sb_r2('beautiful'), 7)  # noqa: SF01
        self.assertEqual(stmr._sb_r2('beauty'), 6)  # noqa: SF01
        self.assertEqual(stmr._sb_r2('beau'), 4)  # noqa: SF01
        self.assertEqual(stmr._sb_r2('animadversion'), 4)  # noqa: SF01
        self.assertEqual(stmr._sb_r2('sprinkled'), 9)  # noqa: SF01
        self.assertEqual(stmr._sb_r2('eucharist'), 6)  # noqa: SF01

    def test_sb_ends_in_short_syllable(self):
        """Test abydos.stemmer._snowball.Snowball._sb_ends_in_short_syllable."""  # noqa: E501
        stmr = _Snowball()
        stmr._vowels = set('aeiouy')  # noqa: SF01
        stmr._codanonvowels = set('bcdfghjklmnpqrstvz\'')  # noqa: SF01

        # base case
        self.assertFalse(stmr._sb_ends_in_short_syllable(''))  # noqa: SF01

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(stmr._sb_ends_in_short_syllable('rap'))  # noqa: SF01
        self.assertTrue(stmr._sb_ends_in_short_syllable('trap'))  # noqa: SF01
        self.assertTrue(
            stmr._sb_ends_in_short_syllable('entrap')  # noqa: SF01
        )
        self.assertTrue(stmr._sb_ends_in_short_syllable('ow'))  # noqa: SF01
        self.assertTrue(stmr._sb_ends_in_short_syllable('on'))  # noqa: SF01
        self.assertTrue(stmr._sb_ends_in_short_syllable('at'))  # noqa: SF01
        self.assertFalse(
            stmr._sb_ends_in_short_syllable('uproot')  # noqa: SF01
        )
        self.assertFalse(
            stmr._sb_ends_in_short_syllable('uproot')  # noqa: SF01
        )
        self.assertFalse(
            stmr._sb_ends_in_short_syllable('bestow')  # noqa: SF01
        )
        self.assertFalse(
            stmr._sb_ends_in_short_syllable('disturb')  # noqa: SF01
        )

        # missed branch test cases
        self.assertFalse(stmr._sb_ends_in_short_syllable('d'))  # noqa: SF01
        self.assertFalse(stmr._sb_ends_in_short_syllable('a'))  # noqa: SF01

    def test_sb_short_word(self):
        """Test abydos.stemmer._snowball.Snowball._sb_short_word."""
        stmr = _Snowball()
        stmr._vowels = set('aeiouy')  # noqa: SF01
        stmr._codanonvowels = set('bcdfghjklmnpqrstvz\'')  # noqa: SF01

        # base case
        self.assertFalse(stmr._sb_short_word(''))  # noqa: SF01

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(stmr._sb_short_word('bed'))  # noqa: SF01
        self.assertTrue(stmr._sb_short_word('shed'))  # noqa: SF01
        self.assertTrue(stmr._sb_short_word('shred'))  # noqa: SF01
        self.assertFalse(stmr._sb_short_word('bead'))  # noqa: SF01
        self.assertFalse(stmr._sb_short_word('embed'))  # noqa: SF01
        self.assertFalse(stmr._sb_short_word('beds'))  # noqa: SF01

    def test_porter2(self):
        """Test abydos.stemmer._snowball.porter2."""
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
        """Test abydos.stemmer._snowball.porter2 (early English)."""
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
        """Test abydos.stemmer._snowball.porter2 (Snowball testset).

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

    abydos.stemmer._snowball.sb_german, .sb_dutch, .sb_norwegian, .sb_swedish,
    & .sb_danish
    """

    def test_sb_german_snowball(self):
        """Test abydos.stemmer._snowball.sb_german (Snowball testset).

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
        """Test abydos.stemmer._snowball.sb_german (alternate vowels)."""
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
        """Test abydos.stemmer._snowball.sb_dutch (Snowball testset).

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
        """Test abydos.stemmer._snowball.sb_norwegian (Snowball testset).

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
        """Test abydos.stemmer._snowball.sb_swedish (Snowball testset).

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
        """Test abydos.stemmer._snowball.sb_danish (Snowball testset).

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
