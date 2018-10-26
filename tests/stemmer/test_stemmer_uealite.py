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

This module contains unit tests for abydos.stemmer.uealite
"""

from __future__ import unicode_literals

import unittest

from abydos.stemmer.uealite import uealite

from .. import _corpus_file


class UEALiteTestCases(unittest.TestCase):
    """Test UEA-lite functions.

    abydos.stemmer.uealite.uealite
    """

    def test_uealite(self):
        """Test abydos.stemmer.uealite.uealite."""
        # base case
        self.assertEqual(uealite(''), '')

        # test cases copied from Ruby port
        # https://github.com/ealdent/uea-stemmer/blob/master/test/uea_stemmer_test.rb
        # These are corrected to match the Java version's output.
        # stem base words to just the base word
        self.assertEqual(uealite('man'), 'man')
        self.assertEqual(uealite('happiness'), 'happiness')
        # stem theses as thesis but not bases as basis
        self.assertEqual(uealite('theses'), 'thesis')
        self.assertNotEqual(uealite('bases'), 'basis')
        # stem preterite words ending in -ed without the -ed
        self.assertEqual(uealite('ordained'), 'ordain')
        self.assertEqual(uealite('killed'), 'kill')
        self.assertEqual(uealite('liked'), 'lik')
        self.assertEqual(uealite('helped'), 'help')
        self.assertEqual(uealite('scarred'), 'scarre')
        self.assertEqual(uealite('invited'), 'invit')
        self.assertEqual(uealite('exited'), 'exit')
        self.assertEqual(uealite('debited'), 'debit')
        self.assertEqual(uealite('smited'), 'smit')
        # stem progressive verbs and gerunds without the -ing
        self.assertEqual(uealite('running'), 'run')
        self.assertEqual(uealite('settings'), 'set')
        self.assertEqual(uealite('timing'), 'time')
        self.assertEqual(uealite('dying'), 'dy')
        self.assertEqual(uealite('harping'), 'harp')
        self.assertEqual(uealite('charring'), 'char')
        # not stem false progressive verbs such as 'sing'
        self.assertEqual(uealite('ring'), 'ring')
        self.assertEqual(uealite('sing'), 'se')
        self.assertEqual(uealite('bring'), 'br')
        self.assertEqual(uealite('fling'), 'fle')
        # stem various plural nouns and 3rd-pres verbs without the -s/-es
        self.assertEqual(uealite('changes'), 'change')
        self.assertEqual(uealite('deaths'), 'death')
        self.assertEqual(uealite('shadows'), 'shadow')
        self.assertEqual(uealite('flies'), 'fly')
        self.assertEqual(uealite('things'), 'thing')
        self.assertEqual(uealite('nothings'), 'nothing')
        self.assertEqual(uealite('witches'), 'witch')
        self.assertEqual(uealite('makes'), 'mak')
        self.assertEqual(uealite('smokes'), 'smok')
        self.assertEqual(uealite('does'), 'do')
        # stem various words with -des suffix
        self.assertEqual(uealite('abodes'), 'abod')
        self.assertEqual(uealite('escapades'), 'escapad')
        self.assertEqual(uealite('crusades'), 'crusad')
        self.assertEqual(uealite('grades'), 'grad')
        # stem various words with -res suffix
        self.assertEqual(uealite('wires'), 'wir')
        self.assertEqual(uealite('acres'), 'acr')
        self.assertEqual(uealite('fires'), 'fir')
        self.assertEqual(uealite('cares'), 'car')
        # stem acronyms when pluralized otherwise they should be left alone
        self.assertEqual(uealite('USA'), 'USA')
        self.assertEqual(uealite('FLOSS'), 'FLOSS')
        self.assertEqual(uealite('MREs'), 'MRE')
        self.assertEqual(uealite('USAED'), 'USAED')

        # test cases copied from Ruby port
        # https://github.com/ealdent/uea-stemmer/blob/master/test/uea_stemmer_test.rb
        # stem base words to just the base word
        self.assertEqual(uealite('man', var='Adams'), 'man')
        self.assertEqual(uealite('happiness', var='Adams'), 'happiness')
        # stem theses as thesis but not bases as basis
        self.assertEqual(uealite('theses', var='Adams'), 'thesis')
        self.assertNotEqual(uealite('bases', var='Adams'), 'basis')
        # stem preterite words ending in -ed without the -ed
        self.assertEqual(uealite('ordained', var='Adams'), 'ordain')
        self.assertEqual(uealite('killed', var='Adams'), 'kill')
        self.assertEqual(uealite('liked', var='Adams'), 'like')
        self.assertEqual(uealite('helped', var='Adams'), 'help')
        # self.assertEqual(uealite('scarred', var='Adams'), 'scar')
        self.assertEqual(uealite('invited', var='Adams'), 'invite')
        self.assertEqual(uealite('exited', var='Adams'), 'exit')
        self.assertEqual(uealite('debited', var='Adams'), 'debit')
        self.assertEqual(uealite('smited', var='Adams'), 'smite')
        # stem progressive verbs and gerunds without the -ing
        self.assertEqual(uealite('running', var='Adams'), 'run')
        self.assertEqual(uealite('settings', var='Adams'), 'set')
        self.assertEqual(uealite('timing', var='Adams'), 'time')
        self.assertEqual(uealite('dying', var='Adams'), 'die')
        self.assertEqual(uealite('harping', var='Adams'), 'harp')
        self.assertEqual(uealite('charring', var='Adams'), 'char')
        # not stem false progressive verbs such as 'sing'
        self.assertEqual(uealite('ring', var='Adams'), 'ring')
        self.assertEqual(uealite('sing', var='Adams'), 'sing')
        self.assertEqual(uealite('ring', var='Adams'), 'ring')
        self.assertEqual(uealite('bring', var='Adams'), 'bring')
        self.assertEqual(uealite('fling', var='Adams'), 'fling')
        # stem various plural nouns and 3rd-pres verbs without the -s/-es
        self.assertEqual(uealite('changes', var='Adams'), 'change')
        self.assertEqual(uealite('deaths', var='Adams'), 'death')
        self.assertEqual(uealite('shadows', var='Adams'), 'shadow')
        self.assertEqual(uealite('flies', var='Adams'), 'fly')
        self.assertEqual(uealite('things', var='Adams'), 'thing')
        self.assertEqual(uealite('nothings', var='Adams'), 'nothing')
        self.assertEqual(uealite('witches', var='Adams'), 'witch')
        self.assertEqual(uealite('makes', var='Adams'), 'make')
        self.assertEqual(uealite('smokes', var='Adams'), 'smoke')
        self.assertEqual(uealite('does', var='Adams'), 'do')
        # stem various words with -des suffix
        self.assertEqual(uealite('abodes', var='Adams'), 'abode')
        self.assertEqual(uealite('escapades', var='Adams'), 'escapade')
        self.assertEqual(uealite('crusades', var='Adams'), 'crusade')
        self.assertEqual(uealite('grades', var='Adams'), 'grade')
        # stem various words with -res suffix
        self.assertEqual(uealite('wires', var='Adams'), 'wire')
        self.assertEqual(uealite('acres', var='Adams'), 'acre')
        self.assertEqual(uealite('fires', var='Adams'), 'fire')
        self.assertEqual(uealite('cares', var='Adams'), 'care')
        # stem acronyms when pluralized otherwise they should be left alone
        self.assertEqual(uealite('USA', var='Adams'), 'USA')
        self.assertEqual(uealite('FLOSS', var='Adams'), 'FLOSS')
        self.assertEqual(uealite('MREs', var='Adams'), 'MRE')
        self.assertEqual(uealite('USAED', var='Adams'), 'USAED')

        # Perl version tests
        self.assertEqual(uealite('ragings'), 'rage')
        self.assertEqual(uealite('ragings', var='Perl'), 'rag')

        # complete coverage
        self.assertEqual(uealite('was'), 'was')
        self.assertEqual(uealite('during'), 'during')
        self.assertEqual(
            uealite('abcdefghijklmnopqrstuvwxyz', max_word_length=20),
            'abcdefghijklmnopqrstuvwxyz',
        )
        self.assertEqual(uealite('10'), '10')
        self.assertEqual(uealite('top-ten'), 'top-ten')
        self.assertEqual(uealite('top-10'), 'top-10')
        self.assertEqual(uealite('top_ten'), 'top_ten')
        self.assertEqual(
            uealite('ABCDEFGHIJKLMs', max_acro_length=8, var='Adams'),
            'ABCDEFGHIJKLMs',
        )
        self.assertEqual(
            uealite('ABCDEFGHIJKLM', max_acro_length=8, var='Adams'),
            'ABCDEFGHIJKLM',
        )
        self.assertEqual(uealite('abcDefGhij'), 'abcDefGhij')
        self.assertEqual(uealite('Tophat'), 'Tophat')
        self.assertEqual(uealite(''), '')
        self.assertEqual(uealite(''), '')

    def test_uealite_wsj_set(self):
        """Test abydos.stemmer.uealite.uealite (WSJ testset)."""
        with open(_corpus_file('uea-lite_wsj.csv')) as wsj_ts:
            for wsj_line in wsj_ts:
                (word, uea, rule) = wsj_line.strip().split(',')
                self.assertEqual(
                    uealite(word, return_rule_no=True), (uea, float(rule))
                )


if __name__ == '__main__':
    unittest.main()
