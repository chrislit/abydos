# Copyright 2019-2022 by Christopher C. Little.
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
from random import choice, randint, sample

from abydos.tokenizer import (
    COrVClusterTokenizer,
    CVClusterTokenizer,
    CharacterTokenizer,
    LegaliPyTokenizer,
    NLTKTokenizer,
    QGrams,
    QSkipgrams,
    RegexpTokenizer,
    SAPSTokenizer,
    SonoriPyTokenizer,
    VCClusterTokenizer,
    WhitespaceTokenizer,
    WordpunctTokenizer,
)

from nltk import TweetTokenizer

from . import EXTREME_TEST, _corpus_file, _fuzz, _random_char

algorithms = {
    'corvcluster': COrVClusterTokenizer().tokenize,
    'cvcluster': CVClusterTokenizer().tokenize,
    'character': CharacterTokenizer().tokenize,
    'legalipy': LegaliPyTokenizer().tokenize,
    'nltk': NLTKTokenizer(nltk_tokenizer=TweetTokenizer()).tokenize,
    'qgrams': QGrams().tokenize,
    'qskipgrams': QSkipgrams().tokenize,
    'regexp': RegexpTokenizer().tokenize,
    'saps': SAPSTokenizer().tokenize,
    'sonoripy': SonoriPyTokenizer().tokenize,
    'vccluster': VCClusterTokenizer().tokenize,
    'whitespace': WhitespaceTokenizer().tokenize,
    'wordpunct': WordpunctTokenizer().tokenize,
}


class BigListOfNaughtyStringsTestCases(unittest.TestCase):
    """Test each tokenizer against the BLNS set.

    Here, we test each algorithm against each string, but we only care that it
    does not result in an exception.

    While not actually a fuzz test, this does serve the purpose of looking for
    errors resulting from unanticipated input.
    """

    def fuzz_test_blns(self):
        """Test each tokenizer against the BLNS set."""
        blns = []
        with codecs.open(_corpus_file('blns.txt'), encoding='UTF-8') as nsf:
            for line in nsf:
                line = line[:-1]
                if line and line[0] != '#':
                    blns.append(line)

        for algo in algorithms:
            for ns in blns:
                try:
                    algorithms[algo](ns)
                except Exception as inst:  # noqa: B902
                    self.fail(
                        f'Exception "{inst}" thrown by {algo} for '
                        f'BLNS: {ns}'
                    )


class FuzzedWordsTestCases(unittest.TestCase):
    """Test each tokenizer against the base words set."""

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
        """Test each tokenizer against the unfuzzed base words."""
        for algo in algorithms:
            for word in self.basewords:
                try:
                    algorithms[algo](word)
                except Exception as inst:  # noqa: B902
                    self.fail(
                        f'Exception "{inst}" thrown by {algo} for '
                        f'word: {word}'
                    )

    def fuzz_test_20pct(self):
        """Fuzz test tokenizers against 20% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = _fuzz(choice(self.basewords), fuzziness=0.2)

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:  # noqa: B902
                    self.fail(
                        f'Exception "{inst}" thrown by {algo} for '
                        f'word: {fuzzed}'
                    )

    def fuzz_test_100pct(self):
        """Fuzz test tokenizers against 100% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = _fuzz(choice(self.basewords), fuzziness=1)

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:  # noqa: B902
                    self.fail(
                        f'Exception "{inst}" thrown by {algo} for '
                        f'word: {fuzzed}'
                    )

    def fuzz_test_fuzz_bmp(self):
        """Fuzz test tokenizers against BMP fuzz."""
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
                except Exception as inst:  # noqa: B902
                    self.fail(
                        f'Exception "{inst}" thrown by {algo} for '
                        f'word: {fuzzed}'
                    )

    def fuzz_test_fuzz_bmpsmp_letter(self):
        """Fuzz test tokenizers against alphabetic BMP+SMP fuzz."""
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
                except Exception as inst:  # noqa: B902
                    self.fail(
                        f'Exception "{inst}" thrown by {algo} for '
                        f'word: {fuzzed}'
                    )

    def fuzz_test_fuzz_bmpsmp_latin(self):
        """Fuzz test tokenizers against Latin BMP+SMP fuzz."""
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
                except Exception as inst:  # noqa: B902
                    self.fail(
                        f'Exception "{inst}" thrown by {algo} for '
                        f'word: {fuzzed}'
                    )

    def fuzz_test_fuzz_unicode(self):
        """Fuzz test tokenizers against valid Unicode fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(_random_char() for _ in range(0, randint(8, 16)))

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:  # noqa: B902
                    self.fail(
                        f'Exception "{inst}" thrown by {algo} for '
                        f'word: {fuzzed}'
                    )


if __name__ == '__main__':
    unittest.main()
