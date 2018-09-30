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
import random
import unittest

from string import printable

from abydos.phonetic import alpha_sis, bmpm, caverphone, davidson, \
    dm_soundex, dolby, double_metaphone, eudex, fonem, fuzzy_soundex, \
    haase_phonetik, henry_early, koelner_phonetik, koelner_phonetik_alpha, \
    koelner_phonetik_num_to_alpha, lein, metaphone, metasoundex, mra, \
    norphone, nysiis, onca, parmar_kumbharana, phonem, phonet, \
    phonetic_spanish, phonex, phonix, pshp_soundex_first, pshp_soundex_last, \
    refined_soundex, reth_schek_phonetik, roger_root, russell_index, \
    russell_index_alpha, russell_index_num_to_alpha, sfinxbis, sound_d, \
    soundex, spanish_metaphone, spfc, statistics_canada

import unicodedata

from six import unichr


algorithms = {'russell_index': lambda name: russell_index(name),
              'russell_index_num_to_alpha':
                  lambda name: russell_index_num_to_alpha(russell_index(name)),
              'russell_index_alpha': russell_index_alpha,
              'soundex': soundex,
              'reverse_soundex': lambda name: soundex(name, reverse=True),
              'soundex_0pad_ml6':
                  lambda name: soundex(name, zero_pad=True, maxlength=6),
              'soundex_special': lambda name: soundex(name, var='special'),
              'soundex_census': lambda name: soundex(name, var='Census'),
              'refined_soundex': refined_soundex,
              'refined_soundex_vowels':
                  lambda name: refined_soundex(name, retain_vowels=True),
              'refined_soundex_0pad_ml6':
                  lambda name:
                  refined_soundex(name, zero_pad=True, maxlength=6),
              'dm_soundex': lambda name: dm_soundex(name),
              'koelner_phonetik': koelner_phonetik,
              'koelner_phonetik_num_to_alpha':
                  lambda name:
                  koelner_phonetik_num_to_alpha(koelner_phonetik(name)),
              'koelner_phonetik_alpha': koelner_phonetik_alpha,
              'nysiis': nysiis,
              'nysiis_modified': lambda name: nysiis(name, modified=True),
              'nysiis_ml_inf':
                  lambda name: nysiis(name, maxlength=float('inf')),
              'mra': mra,
              'metaphone': metaphone,
              'double_metaphone':
                  lambda name: double_metaphone(name),
              'caverphone_1': lambda name: caverphone(name, version=1),
              'caverphone_2': caverphone,
              'alpha_sis': lambda name: alpha_sis(name),
              'fuzzy_soundex': fuzzy_soundex,
              'fuzzy_soundex_0pad_ml8':
                  lambda name: fuzzy_soundex(name, maxlength=8, zero_pad=True),
              'phonex': phonex,
              'phonex_0pad_ml6':
                  lambda name: phonex(name, maxlength=6, zero_pad=True),
              'phonem': phonem,
              'phonix': phonix,
              'phonix_0pad_ml6':
                  lambda name: phonix(name, maxlength=6, zero_pad=True),
              'sfinxbis': lambda name: sfinxbis(name),
              'sfinxbis_ml6': lambda name: sfinxbis(name, maxlength=6),
              'phonet_1': phonet,
              'phonet_2': lambda name: phonet(name, mode=2),
              'phonet_1_none': lambda name: phonet(name, lang='none'),
              'phonet_2_none': lambda name: phonet(name, mode=2, lang='none'),
              'spfc': lambda name: spfc(' '.join((name, name))),
              'statistics_canada': statistics_canada,
              'statistics_canada_ml8':
                  lambda name: statistics_canada(name, maxlength=8),
              'lein': lein,
              'lein_nopad_ml8':
                  lambda name: lein(name, maxlength=8, zero_pad=False),
              'roger_root': roger_root,
              'roger_root_nopad_ml8':
                  lambda name: roger_root(name, maxlength=8, zero_pad=False),
              'onca': onca,
              'onca_nopad_ml8':
                  lambda name: onca(name, maxlength=8, zero_pad=False),
              'eudex': lambda name: eudex(name),
              'haase_phonetik': lambda name: haase_phonetik(name),
              'haase_phonetik_primary':
                  lambda name: haase_phonetik(name, primary_only=True)[:1],
              'reth_schek_phonetik': reth_schek_phonetik,
              'fonem': fonem,
              'parmar_kumbharana': parmar_kumbharana,
              'davidson': davidson,
              'sound_d': sound_d,
              'sound_d_ml8': lambda name: sound_d(name, maxlength=8),
              'pshp_soundex_last': pshp_soundex_last,
              'pshp_soundex_last_german':
                  lambda name: pshp_soundex_last(name, german=True),
              'pshp_soundex_last_ml8':
                  lambda name: pshp_soundex_last(name, maxlength=8),
              'pshp_soundex_first': pshp_soundex_first,
              'pshp_soundex_first_german':
                  lambda name: pshp_soundex_first(name, german=True),
              'pshp_soundex_first_ml8':
                  lambda name: pshp_soundex_first(name, maxlength=8),
              'henry_early': henry_early,
              'henry_early_ml8': lambda name: henry_early(name, maxlength=8),
              'norphone': norphone,
              'dolby': dolby,
              'dolby_ml4': lambda name: dolby(name, maxlength=4),
              'dolby_vowels': lambda name: dolby(name, keep_vowels=True),
              'phonetic_spanish': phonetic_spanish,
              'phonetic_spanish_ml4':
                  lambda name: phonetic_spanish(name, maxlength=4),
              'spanish_metaphone': spanish_metaphone,
              'spanish_metaphone_modified':
                  lambda name: spanish_metaphone(name, modified=True),
              'spanish_metaphone_ml4':
                  lambda name: spanish_metaphone(name, maxlength=4),
              'metasoundex': metasoundex,
              'metasoundex_es': lambda name: metasoundex(name, language='es'),
              'bmpm': bmpm,
              }


TESTDIR = os.path.dirname(__file__)

EXTREME_TEST = False  # Set to True to test EVERY single case (NB: takes hours)
ALLOW_RANDOM = True  # Set to False to skip all random tests

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
                if "Script Injection" in line:
                    omit_section = True
                if "SQL Injection" in line:
                    omit_section = False
                if line and line[0] != '#':
                    bmpm_omit = omit_section | (len(line.split()) > 5)
                    blns.append((bmpm_omit, line))

        for algo in algorithms:
            for bmpm_omit, ns in blns:
                try:
                    if not (bmpm_omit and 'bmpm' in algo):
                        _ = algorithms[algo](ns)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for BLNS: {}'
                              .format(inst, algo, ns))


class FuzzedWordsTestCases(unittest.TestCase):
    """Test each phonetic algorithm against the base words set."""
    basewords = []
    with codecs.open(TESTDIR + '/corpora/blns.txt',
                     encoding='UTF-8') as basewords_file:
        for line in basewords_file:
            line = line[:-1]
            if line:
                basewords.append(line)

    def random_char(self, below=0x10ffff, must_be=None):
        """Generate a random Unicode character below U+{below}."""
        while True:
            char = unichr(random.randint(0, below))
            try:
                name = unicodedata.name(char)
                if must_be is None or must_be in name:
                    return char
            except ValueError:
                pass

    def fuzz(self, word, fuzziness=0.2):
        """Fuzz a word with noise."""
        while True:
            new_word = []
            for ch in word:
                if random.random() > fuzziness:
                    new_word.append(ch)
                else:
                    if random.random() > 0.5:
                        new_word.append(random.choice(printable))
                    elif random.random() > 0.8:
                        new_word.append(unichr(random.randint(0, 0x10ffff)))
                    else:
                        new_word.append(unichr(random.randint(0, 0xffff)))
                    if random.random() > 0.5:
                        new_word.append(ch)
            new_word = ''.join(new_word)
            if new_word != word:
                return new_word

    def fuzz_test_base(self):
        """Test each phonetic algorithm against the unfuzzed base words."""
        for algo in algorithms:
            for word in self.basewords:
                try:
                    if not ('bmpm' in algo and len(word) > 12):
                        _ = algorithms[algo](word)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, word))

    def fuzz_test_20pct(self):
        """Fuzz test phonetic algorithms against 20% fuzzed words."""
        for _ in range(100000):
            fuzzed = self.fuzz(random.choice(self.basewords), fuzziness=0.2)
            algs = random.choices(list(algorithms.keys()), k=5)
            for algo in algs:
                try:
                    if not ('bmpm' in algo and len(fuzzed) > 12):
                        _ = algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_100pct(self):
        """Fuzz test phonetic algorithms against 100% fuzzed words."""
        for _ in range(100000):
            fuzzed = self.fuzz(random.choice(self.basewords), fuzziness=1)
            algs = random.choices(list(algorithms.keys()), k=5)
            for algo in algs:
                try:
                    if not ('bmpm' in algo and len(fuzzed) > 12):
                        _ = algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_fuzz_bmp(self):
        """Fuzz test phonetic algorithms against BMP fuzz."""
        for _ in range(100000):
            fuzzed = ''.join(self.random_char(0xffff) for _ in
                             range(0, random.randint(8, 16)))

            algs = random.choices(list(algorithms.keys()), k=5)
            for algo in algs:
                try:
                    _ = algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_fuzz_bmpsmp_letter(self):
        """Fuzz test phonetic algorithms against alphabetic BMP+SMP fuzz."""
        for _ in range(100000):
            fuzzed = ''.join(self.random_char(0x1ffff, ' LETTER ') for _ in
                             range(0, random.randint(8, 16)))

            algs = random.choices(list(algorithms.keys()), k=5)
            for algo in algs:
                try:
                    _ = algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_fuzz_bmpsmp_latin(self):
        """Fuzz test phonetic algorithms against Latin BMP+SMP fuzz."""
        for _ in range(100000):
            fuzzed = ''.join(self.random_char(0x1ffff, 'LATIN ') for _ in
                             range(0, random.randint(8, 16)))

            algs = random.choices(list(algorithms.keys()), k=5)
            for algo in algs:
                try:
                    _ = algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))

    def fuzz_test_fuzz_unicode(self):
        """Fuzz test phonetic algorithms against valid Unicode fuzz."""
        for _ in range(100000):
            fuzzed = ''.join(self.random_char() for _ in
                             range(0, random.randint(8, 16)))

            algs = random.choices(list(algorithms.keys()), k=5)
            for algo in algs:
                try:
                    _ = algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, fuzzed))


if __name__ == '__main__':
    unittest.main()
