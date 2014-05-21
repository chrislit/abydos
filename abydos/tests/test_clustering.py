# -*- coding: utf-8 -*-
"""abydos.tests.test_clustering

This module contains unit tests for abydos.clustering

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
from abydos._compat import _range
import unittest
from abydos.clustering import fingerprint, qgram_fingerprint, \
    phonetic_fingerprint

testset = ('À noite, vovô Kowalsky vê o ímã cair no pé do pingüim queixoso e \
vovó põe açúcar no chá de tâmaras do jabuti feliz.', )
anssetw = ('a acucar cair cha de do e feliz ima jabuti kowalsky no noite o pe \
pinguim poe queixoso tamaras ve vovo', )
anssetq2 = ('abacadaialamanarasbucachcudedoeaedeieleoetevfeguhaifiminiritix\
izjakokylilsmamqngnoocoeoiojokoposovowpepipoqurarnsdsksotatetiucueuiutvevo\
waxoyv', )
anssetq1 = ('abcdefghijklmnopqrstuvwxyz', )

class fingerprint_test_cases(unittest.TestCase):
    def test_fingerprint(self):
        self.assertEquals(fingerprint(''), '')
        for i in _range(len(testset)):
            self.assertEquals(fingerprint(testset[i]), anssetw[i])

class qgram_fingerprint_test_cases(unittest.TestCase):
    def test_qgram_fingerprint(self):
        self.assertEquals(qgram_fingerprint(''), '')
        for i in _range(len(testset)):
            self.assertEquals(qgram_fingerprint(testset[i], 1), anssetq1[i])
            self.assertEquals(qgram_fingerprint(testset[i], 2), anssetq2[i])
            self.assertEquals(qgram_fingerprint(testset[i]), anssetq2[i])

class phonetic_fingerprint_test_cases(unittest.TestCase):
    def test_phonetic_fingerprint(self):
        self.assertEquals(phonetic_fingerprint(''), '')
        # TODO: add non-trivial tests
