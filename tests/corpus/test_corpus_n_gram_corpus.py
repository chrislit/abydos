# -*- coding: utf-8 -*-

# Copyright 2014-2019 by Christopher C. Little.
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

"""abydos.tests.corpus.test_n_gram_corpus.

This module contains unit tests for abydos.corpus._n_gram_corpus
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest
from collections import Counter

from abydos.corpus import Corpus
from abydos.corpus import NGramCorpus

from .. import _corpus_file


class NGramCorpusTestCases(unittest.TestCase):
    """Test abydos.corpus.NGramCorpus."""

    simple_corpus = NGramCorpus()
    simple_corpus.gng_importer(_corpus_file('simple-ngrams.txt'))

    double_corpus = NGramCorpus()
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
    sotu2015_corpus = Corpus(sotu2015_sample, filter_chars='.?-;,:')

    sotu_ngcorpus_uni = NGramCorpus(sotu2015_corpus)

    sotu_ngcorpus_tri = NGramCorpus()
    sotu_ngcorpus_tri.corpus_importer(sotu2015_corpus, 3, '<SOS>', '<EOS>')

    sotu_ngcorpus_5 = NGramCorpus()
    sotu_ngcorpus_5.corpus_importer(sotu2015_corpus, 5, '', '')

    simple_ngcorpus_5 = NGramCorpus()
    simple_ngcorpus_5.corpus_importer(
        Corpus(' '.join(['a'] * 10)), 15
    )  # 10 a's

    def test_init(self):
        """Test abydos.corpus.NGramCorpus.__init__."""
        self.assertIsInstance(NGramCorpus(), NGramCorpus)
        self.assertRaises(TypeError, NGramCorpus, ['a', 'b', 'c'])
        self.assertIsInstance(NGramCorpus(self.sotu2015_corpus), NGramCorpus)

    def test_corpus_importer(self):
        """Test abydos.corpus.NGramCorpus.corpus_importer."""
        self.assertRaises(
            TypeError, self.sotu_ngcorpus_5.corpus_importer, 'a b c d'
        )
        self.assertRaises(TypeError, self.sotu_ngcorpus_5.corpus_importer)

        self.assertIsInstance(self.sotu_ngcorpus_uni, NGramCorpus)
        self.assertIsInstance(self.sotu_ngcorpus_tri, NGramCorpus)

        self.assertIsInstance(self.sotu_ngcorpus_uni.ngcorpus, Counter)
        self.assertIsInstance(self.sotu_ngcorpus_tri.ngcorpus, Counter)

        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 1)), 10
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 2)), 9
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 3)), 8
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 4)), 7
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 5)), 6
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 6)), 5
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 7)), 4
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 8)), 3
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 9)), 2
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 10)), 1
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 11)), 0
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 12)), 0
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 13)), 0
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 14)), 0
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count(' '.join('a' * 15)), 0
        )
        self.assertEqual(self.simple_ngcorpus_5.get_count('_START_ a'), 1)
        self.assertEqual(self.simple_ngcorpus_5.get_count('a _END_'), 1)
        self.assertEqual(self.simple_ngcorpus_5.get_count('_END_ a'), 0)
        self.assertEqual(self.simple_ngcorpus_5.get_count('a _START_'), 0)
        self.assertEqual(
            self.simple_ngcorpus_5.get_count('_START_ a _END_'), 0
        )
        self.assertEqual(
            self.simple_ngcorpus_5.get_count('_END_ a _START_'), 0
        )

        self.assertEqual(self.sotu_ngcorpus_uni.get_count('Mr'), 2)
        self.assertEqual(self.sotu_ngcorpus_tri.get_count('Mr'), 2)

        self.assertEqual(self.sotu_ngcorpus_uni.get_count('the'), 19)
        self.assertEqual(self.sotu_ngcorpus_tri.get_count('the'), 19)

        self.assertEqual(self.sotu_ngcorpus_uni.get_count('to come'), 0)
        self.assertEqual(self.sotu_ngcorpus_tri.get_count('to come'), 2)

        self.assertEqual(self.sotu_ngcorpus_tri.get_count('<SOS> And'), 3)
        self.assertGreater(
            self.sotu_ngcorpus_tri.get_count('<SOS> And'),
            self.sotu_ngcorpus_5.get_count('<SOS> And'),
        )

    def test_gng_importer(self):
        """Test abydos.corpus.NGramCorpus.gng_importer."""
        self.assertIsInstance(self.simple_corpus, NGramCorpus)
        self.assertIsInstance(self.simple_corpus.ngcorpus, Counter)

        self.assertEqual(self.simple_corpus.get_count('the'), 20)
        self.assertEqual(self.double_corpus.get_count('the'), 40)

    def test_get_count(self):
        """Test abydos.corpus.NGramCorpus.get_count."""
        # string-style tests
        self.assertEqual(self.simple_corpus.get_count('the'), 20)
        self.assertEqual(self.simple_corpus.get_count('the quick'), 2)
        self.assertEqual(self.simple_corpus.get_count('trolley'), 0)

        # list-style tests
        self.assertEqual(self.simple_corpus.get_count(['the']), 20)
        self.assertEqual(self.simple_corpus.get_count(['the', 'quick']), 2)
        self.assertEqual(self.simple_corpus.get_count(['trolley']), 0)


if __name__ == '__main__':
    unittest.main()
