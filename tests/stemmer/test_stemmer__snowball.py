# -*- coding: utf-8 -*-

# Copyright 2014-2020 by Christopher C. Little.
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

This module contains unit tests for abydos.stemmer._Snowball
"""

import unittest

# noinspection PyProtectedMember
from abydos.stemmer._snowball import _Snowball


class SnowballTestCases(unittest.TestCase):
    """Test _Snowball functions.

    abydos.stemmer._Snowball
    """

    stmr = _Snowball()
    stmr._vowels = set('aeiouy')  # noqa: SF01
    stmr._codanonvowels = set("bcdfghjklmnpqrstvz'")  # noqa: SF01

    def test_has_vowel(self):
        """Test abydos.stemmer._Snowball._has_vowel."""
        # base case
        self.assertFalse(self.stmr._sb_has_vowel(''))  # noqa: SF01

        # False cases
        self.assertFalse(self.stmr._sb_has_vowel('b'))  # noqa: SF01
        self.assertFalse(self.stmr._sb_has_vowel('c'))  # noqa: SF01
        self.assertFalse(self.stmr._sb_has_vowel('bc'))  # noqa: SF01
        self.assertFalse(
            self.stmr._sb_has_vowel('bcdfghjklmnpqrstvwxYz')  # noqa: SF01
        )
        self.assertFalse(self.stmr._sb_has_vowel('Y'))  # noqa: SF01

        # True cases
        self.assertTrue(self.stmr._sb_has_vowel('a'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_has_vowel('e'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_has_vowel('ae'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_has_vowel('aeiouy'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_has_vowel('y'))  # noqa: SF01

        self.assertTrue(self.stmr._sb_has_vowel('ade'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_has_vowel('cad'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_has_vowel('add'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_has_vowel('phi'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_has_vowel('pfy'))  # noqa: SF01

        self.assertFalse(self.stmr._sb_has_vowel('pfY'))  # noqa: SF01

    def test_sb_r1(self):
        """Test abydos.stemmer._Snowball._sb_r1."""
        # base case
        self.assertEqual(self.stmr._sb_r1(''), 0)  # noqa: SF01

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(self.stmr._sb_r1('beautiful'), 5)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r1('beauty'), 5)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r1('beau'), 4)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r1('animadversion'), 2)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r1('sprinkled'), 5)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r1('eucharist'), 3)  # noqa: SF01

        self.assertEqual(
            self.stmr._sb_r1('eucharist', r1_prefixes={'ist'}), 3  # noqa: SF01
        )
        self.assertEqual(
            self.stmr._sb_r1('ist', r1_prefixes={'ist'}), 3  # noqa: SF01
        )

    def test_sb_r2(self):
        """Test abydos.stemmer._Snowball._sb_r2."""
        # base case
        self.assertEqual(self.stmr._sb_r2(''), 0)  # noqa: SF01

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(self.stmr._sb_r2('beautiful'), 7)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r2('beauty'), 6)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r2('beau'), 4)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r2('animadversion'), 4)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r2('sprinkled'), 9)  # noqa: SF01
        self.assertEqual(self.stmr._sb_r2('eucharist'), 6)  # noqa: SF01

    def test_sb_ends_in_short_syllable(self):
        """Test abydos.stemmer._Snowball._sb_ends_in_short_syllable."""
        # base case
        self.assertFalse(
            self.stmr._sb_ends_in_short_syllable('')  # noqa: SF01
        )

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(
            self.stmr._sb_ends_in_short_syllable('rap')  # noqa: SF01
        )
        self.assertTrue(
            self.stmr._sb_ends_in_short_syllable('trap')  # noqa: SF01
        )
        self.assertTrue(
            self.stmr._sb_ends_in_short_syllable('entrap')  # noqa: SF01
        )
        self.assertTrue(
            self.stmr._sb_ends_in_short_syllable('ow')  # noqa: SF01
        )
        self.assertTrue(
            self.stmr._sb_ends_in_short_syllable('on')  # noqa: SF01
        )
        self.assertTrue(
            self.stmr._sb_ends_in_short_syllable('at')  # noqa: SF01
        )
        self.assertFalse(
            self.stmr._sb_ends_in_short_syllable('uproot')  # noqa: SF01
        )
        self.assertFalse(
            self.stmr._sb_ends_in_short_syllable('uproot')  # noqa: SF01
        )
        self.assertFalse(
            self.stmr._sb_ends_in_short_syllable('bestow')  # noqa: SF01
        )
        self.assertFalse(
            self.stmr._sb_ends_in_short_syllable('disturb')  # noqa: SF01
        )

        # missed branch test cases
        self.assertFalse(
            self.stmr._sb_ends_in_short_syllable('d')  # noqa: SF01
        )
        self.assertFalse(
            self.stmr._sb_ends_in_short_syllable('a')  # noqa: SF01
        )
        self.assertFalse(
            self.stmr._sb_ends_in_short_syllable('da')  # noqa: SF01
        )

    def test_sb_short_word(self):
        """Test abydos.stemmer._Snowball._sb_short_word."""
        # base case
        self.assertFalse(self.stmr._sb_short_word(''))  # noqa: SF01

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(self.stmr._sb_short_word('bed'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_short_word('shed'))  # noqa: SF01
        self.assertTrue(self.stmr._sb_short_word('shred'))  # noqa: SF01
        self.assertFalse(self.stmr._sb_short_word('bead'))  # noqa: SF01
        self.assertFalse(self.stmr._sb_short_word('embed'))  # noqa: SF01
        self.assertFalse(self.stmr._sb_short_word('beds'))  # noqa: SF01


if __name__ == '__main__':
    unittest.main()
