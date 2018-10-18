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

"""abydos.tests.fuzz.test_phonetic.

This module contains fuzz tests for abydos.phonetic
"""

import codecs
import os
import unittest
from random import choice, randint, sample

from abydos.phonetic.alpha_sis import alpha_sis
from abydos.phonetic.bmpm import bmpm
from abydos.phonetic.caverphone import caverphone
from abydos.phonetic.davidson import davidson
from abydos.phonetic.de import haase_phonetik, koelner_phonetik, \
    koelner_phonetik_alpha, koelner_phonetik_num_to_alpha, phonem, \
    reth_schek_phonetik
from abydos.phonetic.dm import dm_soundex
from abydos.phonetic.dolby import dolby
from abydos.phonetic.es import phonetic_spanish, spanish_metaphone
from abydos.phonetic.eudex import eudex
from abydos.phonetic.fr import fonem, henry_early
from abydos.phonetic.hybrid import metasoundex, onca
from abydos.phonetic.metaphone import double_metaphone, metaphone
from abydos.phonetic.mra import mra
from abydos.phonetic.nrl import nrl
from abydos.phonetic.nysiis import nysiis
from abydos.phonetic.parmar_kumbharana import parmar_kumbharana
from abydos.phonetic.phonet import phonet
from abydos.phonetic.pt import soundex_br
from abydos.phonetic.roger_root import roger_root
from abydos.phonetic.russell import russell_index, russell_index_alpha, \
    russell_index_num_to_alpha
from abydos.phonetic.sound_d import sound_d
from abydos.phonetic.soundex import fuzzy_soundex, lein, phonex, phonix, \
    pshp_soundex_first, pshp_soundex_last, refined_soundex, soundex
from abydos.phonetic.spfc import spfc
from abydos.phonetic.statistics_canada import statistics_canada
from abydos.phonetic.sv import norphone, sfinxbis


from . import _fuzz, _random_char

algorithms = {'russell_index': lambda name: russell_index(name),
              'russell_index_num_to_alpha':
                  lambda name: russell_index_num_to_alpha(russell_index(name)),
              'russell_index_alpha': russell_index_alpha,
              'soundex': soundex,
              'reverse_soundex': lambda name: soundex(name, reverse=True),
              'soundex_0pad_ml6':
                  lambda name: soundex(name, zero_pad=True, max_length=6),
              'soundex_special': lambda name: soundex(name, var='special'),
              'soundex_census': lambda name: soundex(name, var='Census'),
              'refined_soundex': refined_soundex,
              'refined_soundex_vowels':
                  lambda name: refined_soundex(name, retain_vowels=True),
              'refined_soundex_0pad_ml6':
                  lambda name:
                  refined_soundex(name, zero_pad=True, max_length=6),
              'dm_soundex': lambda name: dm_soundex(name),
              'koelner_phonetik': koelner_phonetik,
              'koelner_phonetik_num_to_alpha':
                  lambda name:
                  koelner_phonetik_num_to_alpha(koelner_phonetik(name)),
              'koelner_phonetik_alpha': koelner_phonetik_alpha,
              'nysiis': nysiis,
              'nysiis_modified': lambda name: nysiis(name, modified=True),
              'nysiis_ml_inf':
                  lambda name: nysiis(name, max_length=-1),
              'mra': mra,
              'metaphone': metaphone,
              'double_metaphone':
                  lambda name: double_metaphone(name),
              'caverphone_1': lambda name: caverphone(name, version=1),
              'caverphone_2': caverphone,
              'alpha_sis': lambda name: alpha_sis(name),
              'fuzzy_soundex': fuzzy_soundex,
              'fuzzy_soundex_0pad_ml8':
                  lambda name:
                  fuzzy_soundex(name, max_length=8, zero_pad=True),
              'phonex': phonex,
              'phonex_0pad_ml6':
                  lambda name: phonex(name, max_length=6, zero_pad=True),
              'phonem': phonem,
              'phonix': phonix,
              'phonix_0pad_ml6':
                  lambda name: phonix(name, max_length=6, zero_pad=True),
              'sfinxbis': lambda name: sfinxbis(name),
              'sfinxbis_ml6': lambda name: sfinxbis(name, max_length=6),
              'phonet_1': phonet,
              'phonet_2': lambda name: phonet(name, mode=2),
              'phonet_1_none': lambda name: phonet(name, lang='none'),
              'phonet_2_none': lambda name: phonet(name, mode=2, lang='none'),
              'spfc': lambda name: spfc(' '.join((name, name))),
              'statistics_canada': statistics_canada,
              'statistics_canada_ml8':
                  lambda name: statistics_canada(name, max_length=8),
              'lein': lein,
              'lein_nopad_ml8':
                  lambda name: lein(name, max_length=8, zero_pad=False),
              'roger_root': roger_root,
              'roger_root_nopad_ml8':
                  lambda name: roger_root(name, max_length=8, zero_pad=False),
              'onca': onca,
              'onca_nopad_ml8':
                  lambda name: onca(name, max_length=8, zero_pad=False),
              'eudex': lambda name: eudex(name),
              'haase_phonetik': lambda name: haase_phonetik(name),
              'haase_phonetik_primary':
                  lambda name: haase_phonetik(name, primary_only=True)[:1],
              'reth_schek_phonetik': reth_schek_phonetik,
              'fonem': fonem,
              'parmar_kumbharana': parmar_kumbharana,
              'davidson': davidson,
              'sound_d': sound_d,
              'sound_d_ml8': lambda name: sound_d(name, max_length=8),
              'pshp_soundex_last': pshp_soundex_last,
              'pshp_soundex_last_german':
                  lambda name: pshp_soundex_last(name, german=True),
              'pshp_soundex_last_ml8':
                  lambda name: pshp_soundex_last(name, max_length=8),
              'pshp_soundex_first': pshp_soundex_first,
              'pshp_soundex_first_german':
                  lambda name: pshp_soundex_first(name, german=True),
              'pshp_soundex_first_ml8':
                  lambda name: pshp_soundex_first(name, max_length=8),
              'henry_early': henry_early,
              'henry_early_ml8': lambda name: henry_early(name, max_length=8),
              'norphone': norphone,
              'dolby': dolby,
              'dolby_ml4': lambda name: dolby(name, max_length=4),
              'dolby_vowels': lambda name: dolby(name, keep_vowels=True),
              'phonetic_spanish': phonetic_spanish,
              'phonetic_spanish_ml4':
                  lambda name: phonetic_spanish(name, max_length=4),
              'spanish_metaphone': spanish_metaphone,
              'spanish_metaphone_modified':
                  lambda name: spanish_metaphone(name, modified=True),
              'spanish_metaphone_ml4':
                  lambda name: spanish_metaphone(name, max_length=4),
              'metasoundex': metasoundex,
              'metasoundex_es': lambda name: metasoundex(name, lang='es'),
              'soundex_br': soundex_br,
              'nrl': nrl,
              'bmpm': bmpm,
              }


TESTDIR = os.path.dirname(__file__)

EXTREME_TEST = False  # Set to True to test EVERY single case (NB: takes hours)

if not EXTREME_TEST and os.path.isfile(TESTDIR + '/EXTREME_TEST'):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True
if not EXTREME_TEST and os.path.isfile(TESTDIR + '/../EXTREME_TEST'):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True


class BigListOfNaughtyStringsTestCases(unittest.TestCase):
    """Test each phonetic algorithm against the BLNS set.

    Here, we test each algorithm against each string, but we only care that it
    does not result in an exception.

    While not actually a fuzz test, this does serve the purpose of looking for
    errors resulting from unanticipated input.
    """

    def fuzz_test_blns(self):
        """Test each phonetic algorithm against the BLNS set."""
        blns = []
        omit_section = False
        with codecs.open(TESTDIR+'/corpora/blns.txt', encoding='UTF-8') as nsf:
            for line in nsf:
                line = line[:-1]
                if 'Script Injection' in line:
                    omit_section = True
                if 'SQL Injection' in line:
                    omit_section = False
                if line and line[0] != '#':
                    bmpm_omit = omit_section | (len(line.split()) > 5)
                    blns.append((bmpm_omit, line))

        for algo in algorithms:
            for bmpm_omit, ns in blns:
                try:
                    if not (bmpm_omit and 'bmpm' in algo):
                        algorithms[algo](ns)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for BLNS: {}'
                              .format(inst, algo, ns))


class FuzzedWordsTestCases(unittest.TestCase):
    """Test each phonetic algorithm against the base words set."""

    reps = 1000 * (10000 if EXTREME_TEST else 1)

    basewords = []
    with codecs.open(TESTDIR + '/corpora/basewords.txt',
                     encoding='UTF-8') as basewords_file:
        for line in basewords_file:
            line = line[:-1]
            if line:
                basewords.append(line)

    def fuzz_test_base(self):
        """Test each phonetic algorithm against the unfuzzed base words."""
        for algo in algorithms:
            for word in self.basewords:
                try:
                    if not ('bmpm' in algo and len(word) > 12):
                        algorithms[algo](word)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, word))

    def fuzz_test_20pct(self):
        """Fuzz test phonetic algorithms against 20% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = _fuzz(choice(self.basewords), fuzziness=0.2)  # noqa: S311

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)  # noqa: S311

            for algo in algs:
                try:
                    if not ('bmpm' in algo and len(fuzzed) > 12):
                        algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_100pct(self):
        """Fuzz test phonetic algorithms against 100% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = _fuzz(choice(self.basewords), fuzziness=1)  # noqa: S311

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)  # noqa: S311

            for algo in algs:
                try:
                    if not ('bmpm' in algo and len(fuzzed) > 12):
                        algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_fuzz_bmp(self):
        """Fuzz test phonetic algorithms against BMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(_random_char(0xffff) for _ in
                             range(0, randint(8, 16)))  # noqa: S311

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)  # noqa: S311

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_fuzz_bmpsmp_letter(self):
        """Fuzz test phonetic algorithms against alphabetic BMP+SMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(_random_char(0x1ffff, ' LETTER ') for _ in
                             range(0, randint(8, 16)))  # noqa: S311

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)  # noqa: S311

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_fuzz_bmpsmp_latin(self):
        """Fuzz test phonetic algorithms against Latin BMP+SMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(_random_char(0x1ffff, 'LATIN ') for _ in
                             range(0, randint(8, 16)))  # noqa: S311

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)  # noqa: S311

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_fuzz_unicode(self):
        """Fuzz test phonetic algorithms against valid Unicode fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(_random_char() for _ in
                             range(0, randint(8, 16)))  # noqa: S311

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)  # noqa: S311

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))


if __name__ == '__main__':
    unittest.main()
