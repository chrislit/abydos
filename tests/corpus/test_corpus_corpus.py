# -*- coding: utf-8 -*-

# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.corpus.test_corpus_corpus.

This module contains unit tests for abydos.corpus.Corpus
"""

import unittest

from abydos.corpus import Corpus
from abydos.tokenizer import QSkipgrams


class CorpusTestCases(unittest.TestCase):
    """Test Corpus class."""

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

    def test_corpus(self):
        """Test abydos.corpus.Corpus."""
        # base cases
        self.assertEqual(Corpus().corpus, [])
        self.assertEqual(Corpus('').corpus, [])
        self.assertEqual(Corpus(' ').corpus, [])
        self.assertEqual(Corpus('\n').corpus, [])
        self.assertEqual(Corpus(' \n').corpus, [])
        self.assertEqual(Corpus(' \n ').corpus, [])

        # one document/one sentence
        self.assertEqual(Corpus('a').corpus, [[['a']]])
        self.assertEqual(Corpus('ab ab').corpus, [[['ab', 'ab']]])
        self.assertEqual(
            Corpus('abc def ghi').corpus, [[['abc', 'def', 'ghi']]]
        )

        # multiple documents (one sentence each)
        self.assertEqual(
            Corpus('abc\n\ndef ghi').corpus, [[['abc']], [['def', 'ghi']]]
        )
        self.assertEqual(
            Corpus('abc\n\ndef ghi\n\n').corpus, [[['abc']], [['def', 'ghi']]]
        )
        self.assertEqual(
            Corpus('\n\nabc\r\n\ndef ghi\n\n').corpus,
            [[['abc']], [['def', 'ghi']]],
        )

        # one document (multiple sentences each)
        self.assertEqual(
            Corpus('abc\n def ghi').corpus, [[['abc'], ['def', 'ghi']]]
        )
        self.assertEqual(
            Corpus('abc\n def ghi\n').corpus, [[['abc'], ['def', 'ghi']]]
        )
        self.assertEqual(
            Corpus('\nabc\n def ghi\n').corpus, [[['abc'], ['def', 'ghi']]]
        )

        # multiple documents (multiple sentences each)
        self.assertEqual(
            Corpus('abc\n abc def\n\n\ndef ghi\n jkl\n').corpus,
            [[['abc'], ['abc', 'def']], [['def', 'ghi'], ['jkl']]],
        )

        # sentence(s) with ignorables
        self.assertEqual(
            Corpus('abc\nd-ef ghi\n', filter_chars='.-').corpus,
            [[['abc'], ['def', 'ghi']]],
        )
        self.assertEqual(
            Corpus('abc\n\n\nd-ef ghi\n\n\n', filter_chars='.-').corpus,
            [[['abc']], [['def', 'ghi']]],
        )
        self.assertEqual(
            Corpus(
                '\n\nabc\r\n\ndef ghi.\n\n' + 'a b c d e f g.\n\n\n',
                filter_chars='.-',
            ).corpus,
            [
                [['abc']],
                [['def', 'ghi']],
                [['a', 'b', 'c', 'd', 'e', 'f', 'g']],
            ],
        )

        # sentences with stopword removal
        self.assertEqual(
            Corpus(
                'The quick brown fox jumped over the lazy dog',
                stop_words=('The', 'the'),
            ).corpus,
            [[['quick', 'brown', 'fox', 'jumped', 'over', 'lazy', 'dog']]],
        )
        self.assertEqual(
            Corpus('a ab abc def', stop_words=('A', 'a')).corpus,
            [[['ab', 'abc', 'def']]],
        )

        # alternate document divider
        self.assertEqual(
            Corpus(
                'The quick brown@ fox jumped over@' + 'the lazy dog',
                doc_split='@',
            ).corpus,
            [
                [['The', 'quick', 'brown']],
                [['fox', 'jumped', 'over']],
                [['the', 'lazy', 'dog']],
            ],
        )

        # alternate sentence divider
        self.assertEqual(
            Corpus(
                'The quick brown$ fox jumped over$' + 'the lazy dog',
                sent_split='$',
            ).corpus,
            [
                [
                    ['The', 'quick', 'brown'],
                    ['fox', 'jumped', 'over'],
                    ['the', 'lazy', 'dog'],
                ]
            ],
        )
        self.assertEqual(
            Corpus(
                'The quick brown$ fox jumped over@' + 'the lazy dog',
                doc_split='@',
                sent_split='$',
            ).corpus,
            [
                [['The', 'quick', 'brown'], ['fox', 'jumped', 'over']],
                [['the', 'lazy', 'dog']],
            ],
        )
        self.assertEqual(
            Corpus(
                '<BOS> The quick brown <EOS>'
                + '<BOS> fox jumped over the lazy dog <EOS>',
                sent_split='<BOS>',
                stop_words=['<EOS>'],
            ).corpus,
            [
                [
                    ['The', 'quick', 'brown'],
                    ['fox', 'jumped', 'over', 'the', 'lazy', 'dog'],
                ]
            ],
        )
        self.assertEqual(
            Corpus(
                'quick', word_tokenizer=QSkipgrams(qval=3, start_stop='')
            ).corpus,
            [
                [
                    [
                        'qui',
                        'quc',
                        'quk',
                        'qic',
                        'qik',
                        'qck',
                        'uic',
                        'uik',
                        'uck',
                        'ick',
                    ]
                ]
            ],
        )

    def test_corpus_docs_raw(self):
        """Test abydos.corpus.Corpus.paras, .docs, .docs_of_words, .raw."""
        doc_str = 'a b c d\n\ne f g\nh i j\nk'
        doc_corp = Corpus(doc_str)

        self.assertEqual(
            doc_corp.paras(),
            [
                [['a', 'b', 'c', 'd']],
                [['e', 'f', 'g'], ['h', 'i', 'j'], ['k']],
            ],
        )
        self.assertEqual(
            doc_corp.docs(),
            [
                [['a', 'b', 'c', 'd']],
                [['e', 'f', 'g'], ['h', 'i', 'j'], ['k']],
            ],
        )
        self.assertEqual(
            doc_corp.docs_of_words(),
            [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h', 'i', 'j', 'k']],
        )
        self.assertEqual(doc_corp.raw(), doc_str)

    def test_corpus_sents_words(self):
        """Test abydos.corpus.Corpus.sents, .words."""
        doc_str = 'a b c d\n\ne f g\nh i j\nk'
        doc_corp = Corpus(doc_str)

        self.assertEqual(
            doc_corp.sents(),
            [['a', 'b', 'c', 'd'], ['e', 'f', 'g'], ['h', 'i', 'j'], ['k']],
        )
        self.assertEqual(
            doc_corp.words(),
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'],
        )

    def test_corpus_idf(self):
        """Test abydos.corpus.Corpus.idf."""
        wiki_idf_sample = 'this is a a sample\n\nthis is another another \
        example example example'
        wiki_idf_corpus = Corpus(wiki_idf_sample)

        self.assertAlmostEqual(wiki_idf_corpus.idf('this'), 0)
        self.assertAlmostEqual(wiki_idf_corpus.idf('example'), 0.69314718056)
        self.assertAlmostEqual(wiki_idf_corpus.idf('these'), float('inf'))
        self.assertAlmostEqual(wiki_idf_corpus.idf('A'), float('inf'))
        self.assertAlmostEqual(
            wiki_idf_corpus.idf('A', lambda w: w.upper()), 0.69314718056
        )


if __name__ == '__main__':
    unittest.main()
