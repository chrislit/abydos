# -*- coding: utf-8 -*-

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

"""abydos.tests.corpus.test_unigram_corpus.

This module contains unit tests for abydos.corpus._unigram_corpus
"""

import os
import sys
import tempfile
import unittest
from collections import defaultdict

from abydos.corpus import UnigramCorpus
from abydos.phonetic import Soundex
from abydos.tokenizer import QSkipgrams

from .. import _corpus_file


class UnigramCorpusTestCases(unittest.TestCase):
    """Test abydos.corpus.UnigramCorpus."""

    simple_corpus = UnigramCorpus()
    simple_corpus.gng_importer(_corpus_file('simple-ngrams.txt'))

    double_corpus = UnigramCorpus()
    double_corpus.gng_importer(_corpus_file('simple-ngrams.txt'))
    double_corpus.gng_importer(_corpus_file('simple-ngrams.txt'))

    sotu2015_sample = "Mr. Speaker, Mr. Vice President, Members of Congress,\
    my fellow Americans:\n\nWe are 15 years into this new century.\n Fifteen\
    years that dawned with terror touching our shores; that unfolded with a\
    new generation fighting two long and costly wars; that saw a vicious\
    recession spread across our nation and the world.\n It has been, and still\
    is, a hard time for many.\n\nBut tonight, we turn the page.\n Tonight,\
    after a breakthrough year for America, our economy is growing and creating\
    jobs at the fastest pace since 1999.\n Our unemployment rate is now lower\
    than it was before the financial crisis.\n More of our kids are graduating\
    than ever before.\n More of our people are insured than ever before.\n And\
    we are as free from the grip of foreign oil as we've been in almost 30\
    years.\n\nTonight, for the first time since 9/11, our combat mission in\
    Afghanistan is over.\n Six years ago, nearly 180,000 American troops\
    served in Iraq and Afghanistan.\n Today, fewer than 15,000 remain.\n And\
    we salute the courage and sacrifice of every man and woman in this 9/11\
    Generation who has served to keep us safe.\n We are humbled and grateful\
    for your service.\n\nAmerica, for all that we have endured; for all the\
    grit and hard work required to come back; for all the tasks that lie\
    ahead, know this: The shadow of crisis has passed, and the State of the\
    Union is strong.\n\nAt this moment -- with a growing economy, shrinking\
    deficits, bustling industry, booming energy production -- we have risen\
    from recession freer to write our own future than any other nation on\
    Earth.\n It's now up to us to choose who we want to be over the next 15\
    years and for decades to come.\n\nWill we accept an economy where only a\
    few of us do spectacularly well?\n Or will we commit ourselves to an\
    economy that generates rising incomes and chances for everyone who makes\
    the effort?\n\nWill we approach the world fearful and reactive, dragged\
    into costly conflicts that strain our military and set back our\
    standing?\n Or will we lead wisely, using all elements of our power to\
    defeat new threats and protect our planet?\n\nWill we allow ourselves to\
    be sorted into factions and turned against one another?\n Or will we\
    recapture the sense of common purpose that has always propelled America\
    forward?\n\nIn two weeks, I will send this Congress a budget filled with\
    ideas that are practical, not partisan.\n And in the months ahead, I'll\
    crisscross the country making a case for those ideas.\n So tonight, I want\
    to focus less on a checklist of proposals, and focus more on the values at\
    stake in the choices before us."
    sotu2015_corpus = UnigramCorpus(sotu2015_sample)

    sdx_corpus = UnigramCorpus(word_transform=Soundex().encode)

    qsg_corpus = UnigramCorpus(
        word_tokenizer=QSkipgrams(qval=3, start_stop='')
    )

    pos_corpus = UnigramCorpus()
    pos_corpus.gng_importer(_corpus_file('simple-ngrams-pos.txt'))

    def test_unigram_corpus_init(self):
        """Test abydos.corpus.UnigramCorpus.__init__."""
        self.assertIsInstance(UnigramCorpus(), UnigramCorpus)
        self.assertIsInstance(self.sotu2015_corpus, UnigramCorpus)

    def test_unigram_corpus_gng_importer(self):
        """Test abydos.corpus.UnigramCorpus.gng_importer."""
        self.assertIsInstance(self.simple_corpus, UnigramCorpus)
        self.assertIsInstance(self.simple_corpus.corpus, defaultdict)

        # skip tests of UnigramCorpus on Python < 3.6 (lack ordered dict)
        if sys.version_info < (3, 6):
            return

        self.sdx_corpus.gng_importer('tests/corpora/simple-ngrams.txt')
        self.assertEqual(
            list(self.sdx_corpus.corpus.items()),
            [
                ('T000', (20, 20)),
                ('Q200', (2, 2)),
                ('B650', (3, 3)),
                ('F200', (1, 1)),
                ('J513', (4, 4)),
                ('O160', (6, 6)),
                ('L200', (1, 1)),
                ('D200', (5, 5)),
                ('T220', (2, 2)),
                ('Q216', (1, 1)),
                ('B651', (1, 1)),
                ('F251', (1, 1)),
                ('O163', (3, 3)),
                ('T420', (2, 2)),
                ('L232', (1, 1)),
            ],
        )

        self.qsg_corpus.gng_importer('tests/corpora/simple-ngrams.txt')
        self.assertEqual(
            list(self.qsg_corpus.corpus.items())[:30:2],
            [
                ('the', (27, 27)),
                ('quc', (5, 5)),
                ('qic', (5, 5)),
                ('qck', (5, 5)),
                ('uik', (5, 5)),
                ('ick', (5, 5)),
                ('brw', (5, 5)),
                ('bow', (5, 5)),
                ('bwn', (5, 5)),
                ('ron', (5, 5)),
                ('own', (5, 5)),
                ('jum', (5, 5)),
                ('jue', (6, 5)),
                ('jmp', (5, 5)),
                ('jmd', (5, 5)),
            ],
        )

        for term, _ in self.pos_corpus.corpus.items():
            self.assertTrue('_' not in term)

    def test_unigram_corpus_save_load_corpus(self):
        """Test abydos.corpus.UnigramCorpus.save_corpus & .load_corpus."""
        handle, path = tempfile.mkstemp('.dat')
        self.sotu2015_corpus.save_corpus(path)
        self.sotu2015_corpus.load_corpus(path)
        statinfo = os.stat(path)
        self.assertGreater(statinfo.st_size, 0)
        os.close(handle)
        os.remove(path)

    def test_unigram_corpus_idf(self):
        """Test abydos.corpus.UnigramCorpus.idf."""
        # string-style tests
        self.assertAlmostEqual(self.simple_corpus.idf('the'), 0.69314718056)
        self.assertAlmostEqual(self.simple_corpus.idf('quick'), 2.3978952728)
        self.assertAlmostEqual(self.simple_corpus.idf('trolley'), float('inf'))


if __name__ == '__main__':
    unittest.main()
