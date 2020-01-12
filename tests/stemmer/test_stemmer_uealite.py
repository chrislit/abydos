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

"""abydos.tests.stemmer.test_stemmer_uealite.

This module contains unit tests for abydos.stemmer.UEALite
"""

import unittest

from abydos.stemmer import UEALite

from .. import _corpus_file


class UEALiteTestCases(unittest.TestCase):
    """Test UEA-lite functions.

    abydos.stemmer.UEALite
    """

    stmr = UEALite()
    stmr_adams = UEALite(var='Adams')

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
        self.assertEqual(self.stmr_adams.stem('man'), 'man')
        self.assertEqual(self.stmr_adams.stem('happiness'), 'happiness')
        # stem theses as thesis but not bases as basis
        self.assertEqual(self.stmr_adams.stem('theses'), 'thesis')
        self.assertNotEqual(self.stmr_adams.stem('bases'), 'basis')
        # stem preterite words ending in -ed without the -ed
        self.assertEqual(self.stmr_adams.stem('ordained'), 'ordain')
        self.assertEqual(self.stmr_adams.stem('killed'), 'kill')
        self.assertEqual(self.stmr_adams.stem('liked'), 'like')
        self.assertEqual(self.stmr_adams.stem('helped'), 'help')
        # self.assertEqual(self.stmr_adams.stem('scarred'), 'scar')
        self.assertEqual(self.stmr_adams.stem('invited'), 'invite')
        self.assertEqual(self.stmr_adams.stem('exited'), 'exit')
        self.assertEqual(self.stmr_adams.stem('debited'), 'debit')
        self.assertEqual(self.stmr_adams.stem('smited'), 'smite')
        # stem progressive verbs and gerunds without the -ing
        self.assertEqual(self.stmr_adams.stem('running'), 'run')
        self.assertEqual(self.stmr_adams.stem('settings'), 'set')
        self.assertEqual(self.stmr_adams.stem('timing'), 'time')
        self.assertEqual(self.stmr_adams.stem('dying'), 'die')
        self.assertEqual(self.stmr_adams.stem('harping'), 'harp')
        self.assertEqual(self.stmr_adams.stem('charring'), 'char')
        # not stem false progressive verbs such as 'sing'
        self.assertEqual(self.stmr_adams.stem('ring'), 'ring')
        self.assertEqual(self.stmr_adams.stem('sing'), 'sing')
        self.assertEqual(self.stmr_adams.stem('ring'), 'ring')
        self.assertEqual(self.stmr_adams.stem('bring'), 'bring')
        self.assertEqual(self.stmr_adams.stem('fling'), 'fling')
        # stem various plural nouns and 3rd-pres verbs without the -s/-es
        self.assertEqual(self.stmr_adams.stem('changes'), 'change')
        self.assertEqual(self.stmr_adams.stem('deaths'), 'death')
        self.assertEqual(self.stmr_adams.stem('shadows'), 'shadow')
        self.assertEqual(self.stmr_adams.stem('flies'), 'fly')
        self.assertEqual(self.stmr_adams.stem('things'), 'thing')
        self.assertEqual(self.stmr_adams.stem('nothings'), 'nothing')
        self.assertEqual(self.stmr_adams.stem('witches'), 'witch')
        self.assertEqual(self.stmr_adams.stem('makes'), 'make')
        self.assertEqual(self.stmr_adams.stem('smokes'), 'smoke')
        self.assertEqual(self.stmr_adams.stem('does'), 'do')
        # stem various words with -des suffix
        self.assertEqual(self.stmr_adams.stem('abodes'), 'abode')
        self.assertEqual(self.stmr_adams.stem('escapades'), 'escapade')
        self.assertEqual(self.stmr_adams.stem('crusades'), 'crusade')
        self.assertEqual(self.stmr_adams.stem('grades'), 'grade')
        # stem various words with -res suffix
        self.assertEqual(self.stmr_adams.stem('wires'), 'wire')
        self.assertEqual(self.stmr_adams.stem('acres'), 'acre')
        self.assertEqual(self.stmr_adams.stem('fires'), 'fire')
        self.assertEqual(self.stmr_adams.stem('cares'), 'care')
        # stem acronyms when pluralized otherwise they should be left alone
        self.assertEqual(self.stmr_adams.stem('USA'), 'USA')
        self.assertEqual(self.stmr_adams.stem('FLOSS'), 'FLOSS')
        self.assertEqual(self.stmr_adams.stem('MREs'), 'MRE')
        self.assertEqual(self.stmr_adams.stem('USAED'), 'USAED')

        # Perl version tests
        self.assertEqual(self.stmr.stem('ragings'), 'rage')
        self.assertEqual(UEALite(var='Perl').stem('ragings'), 'rag')

        # complete coverage
        self.assertEqual(self.stmr.stem('was'), 'was')
        self.assertEqual(self.stmr.stem('during'), 'during')
        self.assertEqual(
            UEALite(max_word_length=20).stem('abcdefghijklmnopqrstuvwxyz'),
            'abcdefghijklmnopqrstuvwxyz',
        )
        self.assertEqual(self.stmr.stem('10'), '10')
        self.assertEqual(self.stmr.stem('top-ten'), 'top-ten')
        self.assertEqual(self.stmr.stem('top-10'), 'top-10')
        self.assertEqual(self.stmr.stem('top_ten'), 'top_ten')
        self.assertEqual(
            UEALite(max_acro_length=8, var='Adams').stem('ABCDEFGHIJKLMs'),
            'ABCDEFGHIJKLMs',
        )
        self.assertEqual(
            UEALite(max_acro_length=8, var='Adams').stem('ABCDEFGHIJKLM'),
            'ABCDEFGHIJKLM',
        )
        self.assertEqual(self.stmr.stem('abcDefGhij'), 'abcDefGhij')
        self.assertEqual(self.stmr.stem('Tophat'), 'Tophat')

    def test_uealite_wsj_set(self):
        """Test abydos.stemmer.UEALite (WSJ testset)."""
        stmr_rrn = UEALite(return_rule_no=True)
        with open(_corpus_file('uea-lite_wsj.csv')) as wsj_ts:
            for wsj_line in wsj_ts:
                (word, uea, rule) = wsj_line.strip().split(',')
                self.assertEqual(stmr_rrn.stem(word), (uea, float(rule)))


if __name__ == '__main__':
    unittest.main()
