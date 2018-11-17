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

"""abydos.tests.stemmer.test_stemmer_uealite.

This module contains unit tests for abydos.stemmer.UEALite
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.stemmer import UEALite, uealite

from .. import _corpus_file


class UEALiteTestCases(unittest.TestCase):
    """Test UEA-lite functions.

    abydos.stemmer.UEALite
    """

    stmr = UEALite()

    def test_uealite(self):
        """Test abydos.stemmer.UEALite."""
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        # test cases copied from Ruby port
        # https://github.com/ealdent/uea-stemmer/blob/master/test/uea_stemmer_test.rb
        # These are corrected to match the Java version's output.
        # stem base words to just the base word
        self.assertEqual(self.stmr.stem('man'), 'man')
        self.assertEqual(self.stmr.stem('happiness'), 'happiness')
        # stem theses as thesis but not bases as basis
        self.assertEqual(self.stmr.stem('theses'), 'thesis')
        self.assertNotEqual(self.stmr.stem('bases'), 'basis')
        # stem preterite words ending in -ed without the -ed
        self.assertEqual(self.stmr.stem('ordained'), 'ordain')
        self.assertEqual(self.stmr.stem('killed'), 'kill')
        self.assertEqual(self.stmr.stem('liked'), 'lik')
        self.assertEqual(self.stmr.stem('helped'), 'help')
        self.assertEqual(self.stmr.stem('scarred'), 'scarre')
        self.assertEqual(self.stmr.stem('invited'), 'invit')
        self.assertEqual(self.stmr.stem('exited'), 'exit')
        self.assertEqual(self.stmr.stem('debited'), 'debit')
        self.assertEqual(self.stmr.stem('smited'), 'smit')
        # stem progressive verbs and gerunds without the -ing
        self.assertEqual(self.stmr.stem('running'), 'run')
        self.assertEqual(self.stmr.stem('settings'), 'set')
        self.assertEqual(self.stmr.stem('timing'), 'time')
        self.assertEqual(self.stmr.stem('dying'), 'dy')
        self.assertEqual(self.stmr.stem('harping'), 'harp')
        self.assertEqual(self.stmr.stem('charring'), 'char')
        # not stem false progressive verbs such as 'sing'
        self.assertEqual(self.stmr.stem('ring'), 'ring')
        self.assertEqual(self.stmr.stem('sing'), 'se')
        self.assertEqual(self.stmr.stem('bring'), 'br')
        self.assertEqual(self.stmr.stem('fling'), 'fle')
        # stem various plural nouns and 3rd-pres verbs without the -s/-es
        self.assertEqual(self.stmr.stem('changes'), 'change')
        self.assertEqual(self.stmr.stem('deaths'), 'death')
        self.assertEqual(self.stmr.stem('shadows'), 'shadow')
        self.assertEqual(self.stmr.stem('flies'), 'fly')
        self.assertEqual(self.stmr.stem('things'), 'thing')
        self.assertEqual(self.stmr.stem('nothings'), 'nothing')
        self.assertEqual(self.stmr.stem('witches'), 'witch')
        self.assertEqual(self.stmr.stem('makes'), 'mak')
        self.assertEqual(self.stmr.stem('smokes'), 'smok')
        self.assertEqual(self.stmr.stem('does'), 'do')
        # stem various words with -des suffix
        self.assertEqual(self.stmr.stem('abodes'), 'abod')
        self.assertEqual(self.stmr.stem('escapades'), 'escapad')
        self.assertEqual(self.stmr.stem('crusades'), 'crusad')
        self.assertEqual(self.stmr.stem('grades'), 'grad')
        # stem various words with -res suffix
        self.assertEqual(self.stmr.stem('wires'), 'wir')
        self.assertEqual(self.stmr.stem('acres'), 'acr')
        self.assertEqual(self.stmr.stem('fires'), 'fir')
        self.assertEqual(self.stmr.stem('cares'), 'car')
        # stem acronyms when pluralized otherwise they should be left alone
        self.assertEqual(self.stmr.stem('USA'), 'USA')
        self.assertEqual(self.stmr.stem('FLOSS'), 'FLOSS')
        self.assertEqual(self.stmr.stem('MREs'), 'MRE')
        self.assertEqual(self.stmr.stem('USAED'), 'USAED')

        # test cases copied from Ruby port
        # https://github.com/ealdent/uea-stemmer/blob/master/test/uea_stemmer_test.rb
        # stem base words to just the base word
        self.assertEqual(self.stmr.stem('man', var='Adams'), 'man')
        self.assertEqual(self.stmr.stem('happiness', var='Adams'), 'happiness')
        # stem theses as thesis but not bases as basis
        self.assertEqual(self.stmr.stem('theses', var='Adams'), 'thesis')
        self.assertNotEqual(self.stmr.stem('bases', var='Adams'), 'basis')
        # stem preterite words ending in -ed without the -ed
        self.assertEqual(self.stmr.stem('ordained', var='Adams'), 'ordain')
        self.assertEqual(self.stmr.stem('killed', var='Adams'), 'kill')
        self.assertEqual(self.stmr.stem('liked', var='Adams'), 'like')
        self.assertEqual(self.stmr.stem('helped', var='Adams'), 'help')
        # self.assertEqual(self.stmr.stem('scarred', var='Adams'), 'scar')
        self.assertEqual(self.stmr.stem('invited', var='Adams'), 'invite')
        self.assertEqual(self.stmr.stem('exited', var='Adams'), 'exit')
        self.assertEqual(self.stmr.stem('debited', var='Adams'), 'debit')
        self.assertEqual(self.stmr.stem('smited', var='Adams'), 'smite')
        # stem progressive verbs and gerunds without the -ing
        self.assertEqual(self.stmr.stem('running', var='Adams'), 'run')
        self.assertEqual(self.stmr.stem('settings', var='Adams'), 'set')
        self.assertEqual(self.stmr.stem('timing', var='Adams'), 'time')
        self.assertEqual(self.stmr.stem('dying', var='Adams'), 'die')
        self.assertEqual(self.stmr.stem('harping', var='Adams'), 'harp')
        self.assertEqual(self.stmr.stem('charring', var='Adams'), 'char')
        # not stem false progressive verbs such as 'sing'
        self.assertEqual(self.stmr.stem('ring', var='Adams'), 'ring')
        self.assertEqual(self.stmr.stem('sing', var='Adams'), 'sing')
        self.assertEqual(self.stmr.stem('ring', var='Adams'), 'ring')
        self.assertEqual(self.stmr.stem('bring', var='Adams'), 'bring')
        self.assertEqual(self.stmr.stem('fling', var='Adams'), 'fling')
        # stem various plural nouns and 3rd-pres verbs without the -s/-es
        self.assertEqual(self.stmr.stem('changes', var='Adams'), 'change')
        self.assertEqual(self.stmr.stem('deaths', var='Adams'), 'death')
        self.assertEqual(self.stmr.stem('shadows', var='Adams'), 'shadow')
        self.assertEqual(self.stmr.stem('flies', var='Adams'), 'fly')
        self.assertEqual(self.stmr.stem('things', var='Adams'), 'thing')
        self.assertEqual(self.stmr.stem('nothings', var='Adams'), 'nothing')
        self.assertEqual(self.stmr.stem('witches', var='Adams'), 'witch')
        self.assertEqual(self.stmr.stem('makes', var='Adams'), 'make')
        self.assertEqual(self.stmr.stem('smokes', var='Adams'), 'smoke')
        self.assertEqual(self.stmr.stem('does', var='Adams'), 'do')
        # stem various words with -des suffix
        self.assertEqual(self.stmr.stem('abodes', var='Adams'), 'abode')
        self.assertEqual(self.stmr.stem('escapades', var='Adams'), 'escapade')
        self.assertEqual(self.stmr.stem('crusades', var='Adams'), 'crusade')
        self.assertEqual(self.stmr.stem('grades', var='Adams'), 'grade')
        # stem various words with -res suffix
        self.assertEqual(self.stmr.stem('wires', var='Adams'), 'wire')
        self.assertEqual(self.stmr.stem('acres', var='Adams'), 'acre')
        self.assertEqual(self.stmr.stem('fires', var='Adams'), 'fire')
        self.assertEqual(self.stmr.stem('cares', var='Adams'), 'care')
        # stem acronyms when pluralized otherwise they should be left alone
        self.assertEqual(self.stmr.stem('USA', var='Adams'), 'USA')
        self.assertEqual(self.stmr.stem('FLOSS', var='Adams'), 'FLOSS')
        self.assertEqual(self.stmr.stem('MREs', var='Adams'), 'MRE')
        self.assertEqual(self.stmr.stem('USAED', var='Adams'), 'USAED')

        # Perl version tests
        self.assertEqual(self.stmr.stem('ragings'), 'rage')
        self.assertEqual(self.stmr.stem('ragings', var='Perl'), 'rag')

        # complete coverage
        self.assertEqual(self.stmr.stem('was'), 'was')
        self.assertEqual(self.stmr.stem('during'), 'during')
        self.assertEqual(
            self.stmr.stem('abcdefghijklmnopqrstuvwxyz', max_word_length=20),
            'abcdefghijklmnopqrstuvwxyz',
        )
        self.assertEqual(self.stmr.stem('10'), '10')
        self.assertEqual(self.stmr.stem('top-ten'), 'top-ten')
        self.assertEqual(self.stmr.stem('top-10'), 'top-10')
        self.assertEqual(self.stmr.stem('top_ten'), 'top_ten')
        self.assertEqual(
            self.stmr.stem('ABCDEFGHIJKLMs', max_acro_length=8, var='Adams'),
            'ABCDEFGHIJKLMs',
        )
        self.assertEqual(
            self.stmr.stem('ABCDEFGHIJKLM', max_acro_length=8, var='Adams'),
            'ABCDEFGHIJKLM',
        )
        self.assertEqual(self.stmr.stem('abcDefGhij'), 'abcDefGhij')
        self.assertEqual(self.stmr.stem('Tophat'), 'Tophat')

        # Test wrapper
        self.assertEqual(uealite('debited'), 'debit')

    def test_uealite_wsj_set(self):
        """Test abydos.stemmer.UEALite (WSJ testset)."""
        with open(_corpus_file('uea-lite_wsj.csv')) as wsj_ts:
            for wsj_line in wsj_ts:
                (word, uea, rule) = wsj_line.strip().split(',')
                self.assertEqual(
                    self.stmr.stem(word, return_rule_no=True),
                    (uea, float(rule)),
                )


if __name__ == '__main__':
    unittest.main()
