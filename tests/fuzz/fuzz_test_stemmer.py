# -*- coding: utf-8 -*-

# Copyright 2018-2019 by Christopher C. Little.
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

"""abydos.tests.fuzz.test_stemmer.

This module contains fuzz tests for abydos.stemmer
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

from abydos.stemmer import (
    Caumanns,
    CLEFGerman,
    CLEFGermanPlus,
    CLEFSwedish,
    Lovins,
    PaiceHusk,
    Porter,
    Porter2,
    SStemmer,
    Schinke,
    SnowballDanish,
    SnowballDutch,
    SnowballGerman,
    SnowballNorwegian,
    SnowballSwedish,
    UEALite,
)

from . import EXTREME_TEST, _corpus_file, _fuzz, _random_char

algorithms = {
    'caumanns': Caumanns().stem,
    'clef_german': CLEFGerman().stem,
    'clef_german_plus': CLEFGermanPlus().stem,
    'clef_swedish': CLEFSwedish().stem,
    'lovins': Lovins().stem,
    'paice_husk': PaiceHusk().stem,
    'porter': Porter().stem,
    'porter_earlyenglish': Porter(early_english=True).stem,
    'porter2': Porter2().stem,
    'porter2_earlyenglish': Porter2(early_english=True).stem,
    's_stemmer': SStemmer().stem,
    'schinke': Schinke().stem,
    'snowball_danish': SnowballDanish().stem,
    'snowball_dutch': SnowballDutch().stem,
    'snowball_german': SnowballGerman().stem,
    'snowball_german_alt': SnowballGerman(alternate_vowels=True).stem,
    'snowball_norwegian': SnowballNorwegian().stem,
    'snowball_swedish': SnowballSwedish().stem,
    'uea_lite': UEALite().stem,
    'uea_lite_adams': UEALite(var='Adams').stem,
    'uea_lite_perl': UEALite(var='Perl').stem,
}


class BigListOfNaughtyStringsTestCases(unittest.TestCase):
    """Test each stemmer against the BLNS set.

    Here, we test each algorithm against each string, but we only care that it
    does not result in an exception.

    While not actually a fuzz test, this does serve the purpose of looking for
    errors resulting from unanticipated input.
    """

    def fuzz_test_blns(self):
        """Test each stemmer against the BLNS set."""
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
    """Test each stemmer against the base words set."""

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
        """Test each stemmer against the unfuzzed base words."""
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
        """Fuzz test stemmers against 20% fuzzed words."""
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
        """Fuzz test stemmers against 100% fuzzed words."""
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
        """Fuzz test stemmers against BMP fuzz."""
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
        """Fuzz test stemmers against alphabetic BMP+SMP fuzz."""
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
        """Fuzz test stemmers against Latin BMP+SMP fuzz."""
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
        """Fuzz test stemmers against valid Unicode fuzz."""
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