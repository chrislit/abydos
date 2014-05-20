# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from abydos.util import qgrams, _qgram_lists, _qgram_counts

class qgram_test_cases(unittest.TestCase):
    def test_qgrams(self):
        self.assertEquals(qgrams(''), [])
        self.assertEquals(qgrams('NELSON', 3), ['NEL', 'ELS', 'LSO', 'SON'])
        self.assertEquals(qgrams('NELSON', 6), ['NELSON'])
        self.assertEquals(qgrams('NELSON', 7), [])

        #http://www.sound-ex.com/alternative_qgram.htm
        self.assertEquals(qgrams('NELSON'), ['NE', 'EL', 'LS', 'SO', 'ON'])
        self.assertEquals(qgrams('NEILSEN'),
                          ['NE', 'EI', 'IL', 'LS', 'SE', 'EN'])

    def test_qgram_lists(self):
        self.assertEquals(_qgram_lists('NELSON', ''),
                          (['NE', 'EL', 'LS', 'SO', 'ON'], [], []))
        self.assertEquals(_qgram_lists('', 'NEILSEN'),
                          ([], ['NE', 'EI', 'IL', 'LS', 'SE', 'EN'], []))
        self.assertEquals(_qgram_lists('NELSON', 'NEILSEN'),
                          (['NE', 'EL', 'LS', 'SO', 'ON'],
                           ['NE', 'EI', 'IL', 'LS', 'SE', 'EN'],
                           ['NE', 'LS']))
        self.assertEquals(_qgram_lists('NELSON', 'NOSLEN'),
                          (['NE', 'EL', 'LS', 'SO', 'ON'],
                           ['NO', 'OS', 'SL', 'LE', 'EN'],
                           []))

    def test_qgram_counts(self):
        self.assertEquals(_qgram_counts('NELSON', ''), (5, 0, 0))
        self.assertEquals(_qgram_counts('', 'NEILSEN'), (0, 6, 0))
        self.assertEquals(_qgram_counts('NELSON', 'NEILSEN'), (5, 6, 2))
        self.assertEquals(_qgram_counts('NELSON', 'NOSLEN'), (5, 5, 0))
