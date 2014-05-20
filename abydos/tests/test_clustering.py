# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from abydos.clustering import fingerprint, qgram_fingerprint, \
    phonetic_fingerprint

testset = ('À noite, vovô Kowalsky vê o ímã cair no pé do pingüim queixoso e vovó põe açúcar no chá de tâmaras do jabuti feliz.',)
anssetw = ('a acucar cair cha de do e feliz ima jabuti kowalsky no noite o pe pinguim poe queixoso tamaras ve vovo',)
anssetq2 = ('abacadaialamanarasbucachcudedoeaedeieleoetevfeguhaifiminiritixizjakokylilsmamqngnoocoeoiojokoposovowpepipoqurarnsdsksotatetiucueuiutvevowaxoyv',)
anssetq1 = ('abcdefghijklmnopqrstuvwxyz',)

class fingerprint_test_cases(unittest.TestCase):
    def test_fingerprint(self):
        self.assertEquals(fingerprint(''), '')
        for i in xrange(len(testset)):
            self.assertEquals(fingerprint(testset[i]), anssetw[i])

class qgram_fingerprint_test_cases(unittest.TestCase):
    def test_qgram_fingerprint(self):
        self.assertEquals(qgram_fingerprint(''), '')
        for i in xrange(len(testset)):
            self.assertEquals(qgram_fingerprint(testset[i], 1), anssetq1[i])
            self.assertEquals(qgram_fingerprint(testset[i], 2), anssetq2[i])
            self.assertEquals(qgram_fingerprint(testset[i]), anssetq2[i])

class phonetic_fingerprint_test_cases(unittest.TestCase):
    def test_phonetic_fingerprint(self):
        self.assertEquals(phonetic_fingerprint(''), '')
        # TODO: add non-trivial tests
