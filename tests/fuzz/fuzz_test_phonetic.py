# Copyright 2018-2020 by Christopher C. Little.
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
import unittest
from random import choice, randint, sample

from abydos.phonetic import (
    Ainsworth,
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
    LEIN,
    MRA,
    MetaSoundex,
    Metaphone,
    NRL,
    NYSIIS,
    Norphone,
    ONCA,
    PHONIC,
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
    Waahlin,
)

from . import EXTREME_TEST, _corpus_file, _fuzz, _random_char

alpha_sis = AlphaSIS()
daitch_mokotoff = DaitchMokotoff()
double_metaphone = DoubleMetaphone()
haase = Haase()
haase_primary = Haase(primary_only=True)
koelner = Koelner()
russell = RussellIndex()
sfinxbis = SfinxBis()
sfinxbis_6 = SfinxBis(max_length=6)
soundex_census = Soundex(var='Census')
spfc = SPFC()

algorithms = {
    'ainsworth': Ainsworth().encode,
    'alpha_sis': lambda _: ', '.join(alpha_sis.encode(_)),
    'bmpm': BeiderMorse().encode,
    'bmpm_german': BeiderMorse(language_arg='german').encode,
    'bmpm_french': BeiderMorse(language_arg='french').encode,
    'bmpm_gen_exact': BeiderMorse(match_mode='exact').encode,
    'bmpm_ash_approx': BeiderMorse(name_mode='ash').encode,
    'bmpm_ash_exact': BeiderMorse(name_mode='ash', match_mode='exact').encode,
    'bmpm_sep_approx': BeiderMorse(name_mode='sep').encode,
    'bmpm_sep_exact': BeiderMorse(name_mode='sep', match_mode='exact').encode,
    'caverphone_1': Caverphone(version=1).encode,
    'caverphone_2': Caverphone().encode,
    'daitch_mokotoff_soundex': lambda _: ', '.join(
        sorted(daitch_mokotoff.encode(_))
    ),
    'davidson': Davidson().encode,
    'dolby': Dolby().encode,
    'dolby_ml4': Dolby(max_length=4).encode,
    'dolby_vowels': Dolby(keep_vowels=True).encode,
    'double_metaphone': lambda _: ', '.join(double_metaphone.encode(_)),
    'eudex': Eudex().encode,
    'fonem': FONEM().encode,
    'fuzzy_soundex': FuzzySoundex().encode,
    'fuzzy_soundex_0pad_ml8': FuzzySoundex(max_length=8, zero_pad=True).encode,
    'haase_phonetik': lambda _: ', '.join(haase.encode(_)),
    'haase_phonetik_primary': lambda _: haase_primary.encode(_)[0],
    'henry_early': HenryEarly().encode,
    'henry_early_ml8': HenryEarly(max_length=8).encode,
    'koelner_phonetik': koelner.encode,
    'koelner_phonetik_num_to_alpha': (
        lambda _: koelner._to_alpha(koelner.encode(_))  # noqa: SF01
    ),
    'koelner_phonetik_alpha': koelner.encode_alpha,
    'lein': LEIN().encode,
    'lein_nopad_ml8': LEIN(max_length=8, zero_pad=False).encode,
    'metasoundex': MetaSoundex().encode,
    'metasoundex_es': MetaSoundex(lang='es').encode,
    'metaphone': Metaphone().encode,
    'mra': MRA().encode,
    'norphone': Norphone().encode,
    'nrl': NRL().encode,
    'nysiis': NYSIIS().encode,
    'nysiis_modified': NYSIIS(modified=True).encode,
    'nysiis_ml_inf': NYSIIS(max_length=-1).encode,
    'onca': ONCA().encode,
    'onca_nopad_ml8': ONCA(max_length=8, zero_pad=False).encode,
    'parmar_kumbharana': ParmarKumbharana().encode,
    'phonem': Phonem().encode,
    'phonet_1': Phonet().encode,
    'phonet_2': Phonet(mode=2).encode,
    'phonet_1_none': Phonet(lang='none').encode,
    'phonet_2_none': Phonet(mode=2, lang='none').encode,
    'phonetic_spanish': PhoneticSpanish().encode,
    'phonetic_spanish_ml4': PhoneticSpanish(max_length=4).encode,
    'phonex': Phonex().encode,
    'phonex_0pad_ml6': Phonex(max_length=6, zero_pad=True).encode,
    'phonic': PHONIC().encode,
    'phonic_0pad_ml6': PHONIC(max_length=6, zero_pad=True).encode,
    'phonic_ext': PHONIC(extended=True).encode,
    'phonix': Phonix().encode,
    'phonix_0pad_ml6': Phonix(max_length=6, zero_pad=True).encode,
    'pshp_soundex_first': PSHPSoundexFirst().encode,
    'pshp_soundex_first_german': PSHPSoundexFirst(german=True).encode,
    'pshp_soundex_first_ml8': PSHPSoundexFirst(max_length=8).encode,
    'pshp_soundex_last': PSHPSoundexLast().encode,
    'pshp_soundex_last_german': PSHPSoundexLast(german=True).encode,
    'pshp_soundex_last_ml8': PSHPSoundexLast(max_length=8).encode,
    'refined_soundex': RefinedSoundex().encode,
    'refined_soundex_vowels': RefinedSoundex(retain_vowels=True).encode,
    'refined_soundex_0pad_ml6': RefinedSoundex(
        zero_pad=True, max_length=6
    ).encode,
    'reth_schek_phonetik': RethSchek().encode,
    'roger_root': RogerRoot().encode,
    'roger_root_nopad_ml8': RogerRoot(max_length=8, zero_pad=False).encode,
    'russell_index': russell.encode,
    'russell_index_num_to_alpha': (
        lambda _: russell._to_alpha(russell.encode(_))  # noqa: SF01
    ),
    'russell_index_alpha': russell.encode_alpha,
    'sfinxbis': lambda _: ', '.join(sfinxbis.encode(_)),
    'sfinxbis_ml6': lambda _: ', '.join(sfinxbis_6.encode(_)),
    'sound_d': SoundD().encode,
    'sound_d_ml8': SoundD(max_length=8).encode,
    'soundex': Soundex().encode,
    'soundex_reverse': Soundex(reverse=True).encode,
    'soundex_0pad_ml6': Soundex(zero_pad=True, max_length=6).encode,
    'soundex_special': Soundex(var='special').encode,
    'soundex_census': lambda _: ', '.join(soundex_census.encode(_)),
    'soundex_br': SoundexBR().encode,
    'spanish_metaphone': SpanishMetaphone().encode,
    'spanish_metaphone_modified': SpanishMetaphone(modified=True).encode,
    'spanish_metaphone_ml4': SpanishMetaphone(max_length=4).encode,
    'spfc': lambda _: spfc.encode(_ + ' ' + _),
    'statistics_canada': StatisticsCanada().encode,
    'statistics_canada_ml8': StatisticsCanada(max_length=8).encode,
    'waahlin': Waahlin().encode,
    'waahlin_soundex': Waahlin(encoder=Soundex()).encode,
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
