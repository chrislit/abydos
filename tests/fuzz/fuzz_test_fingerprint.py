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

"""abydos.tests.fuzz.test_fingerprint.

This module contains fuzz tests for abydos.fingerprint
"""

import codecs
import os
import unittest
from random import choice, randint, sample

from abydos.fingerprint import count_fingerprint, occurrence_fingerprint, \
    occurrence_halved_fingerprint, omission_key, phonetic_fingerprint, \
    position_fingerprint, qgram_fingerprint, skeleton_key, str_fingerprint, \
    synoname_toolcode

from . import fuzz, random_char

algorithms = {'str_fingerprint': str_fingerprint,
              'qgram_fingerprint': qgram_fingerprint,
              'qgram_fingerprint_3':
                  lambda name: qgram_fingerprint(name, qval=3),
              'qgram_fingerprint_ssj':
                  lambda name:
                  qgram_fingerprint(name, start_stop='$#', joiner=' '),
              'phonetic_fingerprint': phonetic_fingerprint,
              'skeleton_key': skeleton_key,
              'omission_key': omission_key,
              'occurrence_fingerprint': occurrence_fingerprint,
              'occurrence_halved_fingerprint': occurrence_halved_fingerprint,
              'count_fingerprint': count_fingerprint,
              'position_fingerprint': position_fingerprint,
              'synoname_toolcode': synoname_toolcode,
              'synoname_toolcode_2name':
                  lambda name: synoname_toolcode(name, name)}

TESTDIR = os.path.dirname(__file__)

EXTREME_TEST = False  # Set to True to test EVERY single case (NB: takes hours)

if not EXTREME_TEST and os.path.isfile(TESTDIR + '/EXTREME_TEST'):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True
if not EXTREME_TEST and os.path.isfile(TESTDIR + '/../EXTREME_TEST'):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True


class BigListOfNaughtyStringsTestCases(unittest.TestCase):
    """Test each fingerprint algorithm against the BLNS set.

    Here, we test each algorithm against each string, but we only care that it
    does not result in an exception.

    While not actually a fuzz test, this does serve the purpose of looking for
    errors resulting from unanticipated input.
    """

    def test_blns(self):
        """Test each fingerprint algorithm against the BLNS set."""
        blns = []
        with codecs.open(TESTDIR+'/corpora/blns.txt', encoding='UTF-8') as nsf:
            for line in nsf:
                line = line[:-1]
                if line and line[0] != '#':
                    blns.append(line)

        for algo in algorithms:
            for ns in blns:
                try:
                    algorithms[algo](ns)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for BLNS: {}'
                              .format(inst, algo, ns))


class FuzzedWordsTestCases(unittest.TestCase):
    """Test each fingerprint algorithm against the base words set."""

    reps = 100000 * (100 if EXTREME_TEST else 1)

    basewords = []
    with codecs.open(TESTDIR + '/corpora/basewords.txt',
                     encoding='UTF-8') as basewords_file:
        for line in basewords_file:
            line = line[:-1]
            if line:
                basewords.append(line)

    def fuzz_test_base(self):
        """Test each fingerprint algorithm against the unfuzzed base words."""
        for algo in algorithms:
            for word in self.basewords:
                try:
                    algorithms[algo](word)
                except Exception as inst:
                    self.fail('Exception "{}" thrown by {} for word: {}'
                              .format(inst, algo, word))

    def fuzz_test_20pct(self):
        """Fuzz test fingerprint algorithms against 20% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = fuzz(choice(self.basewords), fuzziness=0.2)  # noqa: S311

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

    def fuzz_test_100pct(self):
        """Fuzz test fingerprint algorithms against 100% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = fuzz(choice(self.basewords), fuzziness=1)  # noqa: S311

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

    def fuzz_test_fuzz_bmp(self):
        """Fuzz test fingerprint algorithms against BMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(random_char(0xffff) for _ in
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
        """Fuzz test fingerprint algorithms against alphabetic BMP+SMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(random_char(0x1ffff, ' LETTER ') for _ in
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
        """Fuzz test fingerprint algorithms against Latin BMP+SMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(random_char(0x1ffff, 'LATIN ') for _ in
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
        """Fuzz test fingerprint algorithms against valid Unicode fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(random_char() for _ in
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
