# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.fuzz.test_tokenizer.

This module contains fuzz tests for abydos.tokenizer
"""

import codecs
import unittest
from inspect import getdoc, getmembers, isclass
from random import choice, randint, sample

import abydos.distance as ad

from six import PY2

from . import EXTREME_TEST, _corpus_file, _fuzz, _random_char

algorithms = {}

for name, obj in getmembers(ad):
    if isclass(obj) and name[0] != '_':
        if name in {
            'Synoname',
            'Covington',
            'Gotoh',
            'SmithWaterman',
            'NeedlemanWunsch',
        }:
            continue
        if PY2 and name in {
            'NCDpaq9a',
            'NCDlzss',
            'NCDlzma',
            'ReesLevenshtein',
            'MinHash',
        }:
            continue

        cls = obj()
        if 'dist_abs' in obj.__dict__ and 'Method disabled' not in getdoc(
            obj.dist_abs
        ):
            algorithms[name.lower() + '_dist_abs'] = cls.dist_abs
        if 'sim_score' in obj.__dict__ and 'Method disabled' not in getdoc(
            obj.sim_score
        ):
            algorithms[name.lower() + '_sim_score'] = cls.sim_score
        if 'dist' in obj.__dict__ and 'Method disabled' not in getdoc(
            obj.dist
        ):
            algorithms[name.lower() + '_dist'] = cls.dist
        if 'sim' in obj.__dict__ and 'Method disabled' not in getdoc(obj.sim):
            algorithms[name.lower() + '_sim'] = cls.sim

# corrections and additions
algorithms['typo_dist_abs'] = ad.Typo(failsafe=True).dist_abs
algorithms['typo_dist'] = ad.Typo(failsafe=True).dist


class BigListOfNaughtyStringsTestCases(unittest.TestCase):
    """Test each distance measure against the BLNS set.

    Here, we test each algorithm against each string, but we only care that it
    does not result in an exception.

    While not actually a fuzz test, this does serve the purpose of looking for
    errors resulting from unanticipated input.
    """

    def fuzz_test_blns(self):
        """Test each distance measure against the BLNS set."""
        blns = []
        with codecs.open(_corpus_file('blns.txt'), encoding='UTF-8') as nsf:
            for line in nsf:
                line = line[:-1]
                if line and line[0] != '#':
                    blns.append(line)

        for algo in algorithms:
            for ns in blns:
                try:
                    algorithms[algo](ns, ns[: min(1, len(ns) - 2)])
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for BLNS: {} & {}'.format(
                            inst, algo, ns, ns[: min(1, len(ns) - 1)]
                        )
                    )


class FuzzedWordsTestCases(unittest.TestCase):
    """Test each distance measure against the base words set."""

    reps = 1000 * (10000 if EXTREME_TEST else 1)

    basewords = []
    with codecs.open(
        _corpus_file('basewords.txt'), encoding='UTF-8'
    ) as basewords_file:
        for line in basewords_file:
            line = line[:-1]
            if line:
                basewords.append(line)

    def fuzz_test_50pct(self):
        """Fuzz test distance measures against 50% fuzzed words."""
        for _ in range(self.reps):
            chosen = choice(self.basewords)
            fuzzed = _fuzz(chosen, fuzziness=0.5)

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](chosen, fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for words: {} & {}'.format(
                            inst, algo, chosen, fuzzed
                        )
                    )

    def fuzz_test_fuzz_bmpsmp_letter(self):
        """Fuzz test distance measures against alphabetic BMP+SMP fuzz."""
        for _ in range(self.reps):
            chosen = ''.join(
                _random_char(0x1FFFF, ' LETTER ')
                for _ in range(0, randint(8, 16))
            )
            fuzzed = _fuzz(chosen, fuzziness=0.5, must_be=' LETTER ')

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](chosen, fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for words: {} & {}'.format(
                            inst, algo, chosen, fuzzed
                        )
                    )


if __name__ == '__main__':
    unittest.main()
