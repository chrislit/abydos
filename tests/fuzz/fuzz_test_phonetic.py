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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import codecs
import unittest
from random import choice, randint, sample

from abydos.phonetic import (
    AlphaSIS,
    BeiderMorse,
    Caverphone,
    DaitchMokotoff,
    Davidson,
    Dolby,
    DoubleMetaphone,
    Eudex,
    FONEM,
    FuzzySoundex,
    Haase,
    HenryEarly,
    Koelner,
    Lein,
    MRA,
    MetaSoundex,
    Metaphone,
    NRL,
    NYSIIS,
    Norphone,
    ONCA,
    PSHPSoundexFirst,
    PSHPSoundexLast,
    ParmarKumbharana,
    Phonem,
    Phonet,
    PhoneticSpanish,
    Phonex,
    Phonix,
    RefinedSoundex,
    RethSchek,
    RogerRoot,
    RussellIndex,
    SPFC,
    SfinxBis,
    SoundD,
    Soundex,
    SoundexBR,
    SpanishMetaphone,
    StatisticsCanada,
)

from . import EXTREME_TEST, _corpus_file, _fuzz, _random_char

alpha_sis = AlphaSIS()
bm = BeiderMorse()
caverphone = Caverphone()
davidson = Davidson()
dm = DaitchMokotoff()
dolby = Dolby()
double_metaphone = DoubleMetaphone()
eudex = Eudex()
fonem = FONEM()
fuzzy_soundex = FuzzySoundex()
haase = Haase()
henry_early = HenryEarly()
koelner = Koelner()
lein = Lein()
metaphone = Metaphone()
metasoundex = MetaSoundex()
mra = MRA()
norphone = Norphone()
nrl = NRL()
nysiis = NYSIIS()
onca = ONCA()
parmar_kumbharana = ParmarKumbharana()
phonem = Phonem()
phonet = Phonet()
phonetic_spanish = PhoneticSpanish()
phonex = Phonex()
phonix = Phonix()
pshp_soundex_first = PSHPSoundexFirst()
pshp_soundex_last = PSHPSoundexLast()
refined_soundex = RefinedSoundex()
reth_schek = RethSchek()
roger_root = RogerRoot()
russell = RussellIndex()
sfinxbis = SfinxBis()
sound_d = SoundD()
soundex = Soundex()
soundex_br = SoundexBR()
spanish_metaphone = SpanishMetaphone()
spfc = SPFC()
statistics_canada = StatisticsCanada()

algorithms = {
    'russell_index': lambda _: str(russell.encode(_)),
    'russell_index_num_to_alpha': lambda _: russell._to_alpha(  # noqa: SF01
        russell.encode(_)
    ),
    'russell_index_alpha': russell.encode_alpha,
    'soundex': soundex.encode,
    'reverse_soundex': lambda _: soundex.encode(_, reverse=True),
    'soundex_0pad_ml6': lambda _: soundex.encode(
        _, zero_pad=True, max_length=6
    ),
    'soundex_special': lambda _: soundex.encode(_, var='special'),
    'soundex_census': lambda _: ', '.join(soundex.encode(_, var='Census')),
    'refined_soundex': refined_soundex.encode,
    'refined_soundex_vowels': lambda _: refined_soundex.encode(
        _, retain_vowels=True
    ),
    'refined_soundex_0pad_ml6': lambda _: refined_soundex.encode(
        _, zero_pad=True, max_length=6
    ),
    'dm_soundex': lambda _: ', '.join(sorted(dm.encode(_))),
    'koelner_phonetik': koelner.encode,
    'koelner_phonetik_num_to_alpha': lambda _: koelner._to_alpha(  # noqa: SF01
        koelner.encode(_)
    ),
    'koelner_phonetik_alpha': koelner.encode_alpha,
    'nysiis': nysiis.encode,
    'nysiis_modified': lambda _: nysiis.encode(_, modified=True),
    'nysiis_ml_inf': lambda _: nysiis.encode(_, max_length=-1),
    'mra': mra.encode,
    'metaphone': metaphone.encode,
    'double_metaphone': lambda _: ', '.join(double_metaphone.encode(_)),
    'caverphone_1': lambda _: caverphone.encode(_, version=1),
    'caverphone_2': caverphone.encode,
    'alpha_sis': lambda _: ', '.join(alpha_sis.encode(_)),
    'fuzzy_soundex': fuzzy_soundex.encode,
    'fuzzy_soundex_0pad_ml8': lambda _: fuzzy_soundex.encode(
        _, max_length=8, zero_pad=True
    ),
    'phonex': phonex.encode,
    'phonex_0pad_ml6': lambda _: phonex.encode(_, max_length=6, zero_pad=True),
    'phonem': phonem.encode,
    'phonix': phonix.encode,
    'phonix_0pad_ml6': lambda _: phonix.encode(_, max_length=6, zero_pad=True),
    'sfinxbis': lambda _: ', '.join(sfinxbis.encode(_)),
    'sfinxbis_ml6': lambda _: ', '.join(sfinxbis.encode(_, max_length=6)),
    'phonet_1': phonet.encode,
    'phonet_2': lambda _: phonet.encode(_, mode=2),
    'phonet_1_none': lambda _: phonet.encode(_, lang='none'),
    'phonet_2_none': lambda _: phonet.encode(_, mode=2, lang='none'),
    'spfc': lambda _: spfc.encode(_ + ' ' + _),
    'statistics_canada': statistics_canada.encode,
    'statistics_canada_ml8': lambda _: statistics_canada.encode(
        _, max_length=8
    ),
    'lein': lein.encode,
    'lein_nopad_ml8': lambda _: lein.encode(_, max_length=8, zero_pad=False),
    'roger_root': roger_root.encode,
    'roger_root_nopad_ml8': lambda _: roger_root.encode(
        _, max_length=8, zero_pad=False
    ),
    'onca': onca.encode,
    'onca_nopad_ml8': lambda _: onca.encode(_, max_length=8, zero_pad=False),
    'eudex': lambda _: str(eudex.encode(_)),
    'haase_phonetik': lambda _: ', '.join(haase.encode(_)),
    'haase_phonetik_primary': lambda _: haase.encode(_, primary_only=True)[0],
    'reth_schek_phonetik': reth_schek.encode,
    'fonem': fonem.encode,
    'parmar_kumbharana': parmar_kumbharana.encode,
    'davidson': davidson.encode,
    'sound_d': sound_d.encode,
    'sound_d_ml8': lambda _: sound_d.encode(_, max_length=8),
    'pshp_soundex_last': pshp_soundex_last.encode,
    'pshp_soundex_last_german': lambda _: pshp_soundex_last.encode(
        _, german=True
    ),
    'pshp_soundex_last_ml8': lambda _: pshp_soundex_last.encode(
        _, max_length=8
    ),
    'pshp_soundex_first': pshp_soundex_first.encode,
    'pshp_soundex_first_german': lambda _: pshp_soundex_first.encode(
        _, german=True
    ),
    'pshp_soundex_first_ml8': lambda _: pshp_soundex_first.encode(
        _, max_length=8
    ),
    'henry_early': henry_early.encode,
    'henry_early_ml8': lambda _: henry_early.encode(_, max_length=8),
    'norphone': norphone.encode,
    'dolby': dolby.encode,
    'dolby_ml4': lambda _: dolby.encode(_, max_length=4),
    'dolby_vowels': lambda _: dolby.encode(_, keep_vowels=True),
    'phonetic_spanish': phonetic_spanish.encode,
    'phonetic_spanish_ml4': lambda _: phonetic_spanish.encode(_, max_length=4),
    'spanish_metaphone': spanish_metaphone.encode,
    'spanish_metaphone_modified': lambda _: spanish_metaphone.encode(
        _, modified=True
    ),
    'spanish_metaphone_ml4': lambda _: spanish_metaphone.encode(
        _, max_length=4
    ),
    'metasoundex': metasoundex.encode,
    'metasoundex_es': lambda _: metasoundex.encode(_, lang='es'),
    'soundex_br': soundex_br.encode,
    'nrl': nrl.encode,
    'bmpm': bm.encode,
    'bmpm_german': lambda _: bm.encode(_, language_arg='german'),
    'bmpm_french': lambda _: bm.encode(_, language_arg='french'),
    'bmpm_gen_exact': lambda _: bm.encode(_, match_mode='exact'),
    'bmpm_ash_approx': lambda _: bm.encode(_, name_mode='ash'),
    'bmpm_ash_exact': lambda _: bm.encode(
        _, name_mode='ash', match_mode='exact'
    ),
    'bmpm_sep_approx': lambda _: bm.encode(_, name_mode='sep'),
    'bmpm_sep_exact': lambda _: bm.encode(
        _, name_mode='sep', match_mode='exact'
    ),
}


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
        with codecs.open(_corpus_file('blns.txt'), encoding='UTF-8') as nsf:
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
                    self.fail(
                        'Exception "{}" thrown by {} for BLNS: {}'.format(
                            inst, algo, ns
                        )
                    )


class FuzzedWordsTestCases(unittest.TestCase):
    """Test each phonetic algorithm against the base words set."""

    reps = 1000 * (10000 if EXTREME_TEST else 1)

    basewords = []
    with codecs.open(
        _corpus_file('basewords.txt'), encoding='UTF-8'
    ) as basewords_file:
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
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, word
                        )
                    )

    def fuzz_test_20pct(self):
        """Fuzz test phonetic algorithms against 20% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = _fuzz(choice(self.basewords), fuzziness=0.2)

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    if not ('bmpm' in algo and len(fuzzed) > 12):
                        algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_100pct(self):
        """Fuzz test phonetic algorithms against 100% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = _fuzz(choice(self.basewords), fuzziness=1)

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    if not ('bmpm' in algo and len(fuzzed) > 12):
                        algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_fuzz_bmp(self):
        """Fuzz test phonetic algorithms against BMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(
                _random_char(0xFFFF) for _ in range(0, randint(8, 16))
            )

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_fuzz_bmpsmp_letter(self):
        """Fuzz test phonetic algorithms against alphabetic BMP+SMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(
                _random_char(0x1FFFF, ' LETTER ')
                for _ in range(0, randint(8, 16))
            )

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_fuzz_bmpsmp_latin(self):
        """Fuzz test phonetic algorithms against Latin BMP+SMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(
                _random_char(0x1FFFF, 'LATIN ')
                for _ in range(0, randint(8, 16))
            )

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_fuzz_unicode(self):
        """Fuzz test phonetic algorithms against valid Unicode fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(_random_char() for _ in range(0, randint(8, 16)))

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )


if __name__ == '__main__':
    unittest.main()
