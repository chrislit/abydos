# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from abydos.util import qgrams, _qgram_lists, _qgram_counts

class qgram_test_cases(unittest.TestCase):
    def test_qgrams(self):
        self.assertEquals(qgrams(''), [])
        self.assertEquals(qgrams('NELSON', 3), ['##N', '#NE', 'NEL', 'ELS',
                                                'LSO', 'SON', 'ON#', 'N##'])
        self.assertEquals(qgrams('NELSON', 7), [])

        #http://www.sound-ex.com/alternative_qgram.htm
        self.assertEquals(qgrams('NELSON'),
                          ['#N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#'])
        self.assertEquals(qgrams('NEILSEN'),
                          ['#N', 'NE', 'EI', 'IL', 'LS', 'SE', 'EN', 'N#'])

    def test_qgram_lists(self):
        self.assertEquals(_qgram_lists('NELSON', ''),
                          (['#N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#'], [], []))
        self.assertEquals(_qgram_lists('', 'NEILSEN'),
                          ([], ['#N', 'NE', 'EI', 'IL', 'LS',
                                'SE', 'EN', 'N#'], []))
        self.assertEquals(_qgram_lists('NELSON', 'NEILSEN'),
                          (['#N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#'],
                           ['#N', 'NE', 'EI', 'IL', 'LS', 'SE', 'EN', 'N#'],
                           ['#N', 'NE', 'LS', 'N#']))
        self.assertEquals(_qgram_lists('NELSON', 'NOSLEN'),
                          (['#N', 'NE', 'EL', 'LS', 'SO', 'ON', 'N#'],
                           ['#N', 'NO', 'OS', 'SL', 'LE', 'EN', 'N#'],
                           ['#N', 'N#']))
        self.assertEquals(_qgram_lists('NAIL', 'LIAN'),
                          (['#N', 'NA', 'AI', 'IL', 'L#'],
                           ['#L', 'LI', 'IA', 'AN', 'N#'],
                           []))

    def test_qgram_counts(self):
        self.assertEquals(_qgram_counts('NELSON', ''), (7, 0, 0))
        self.assertEquals(_qgram_counts('', 'NEILSEN'), (0, 8, 0))
        self.assertEquals(_qgram_counts('NELSON', 'NEILSEN'), (7, 8, 4))
        self.assertEquals(_qgram_counts('NELSON', 'NOSLEN'), (7, 7, 2))
        self.assertEquals(_qgram_counts('NAIL', 'LIAN'), (5, 5, 0))
