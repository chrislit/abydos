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


# pylint: disable=R0904
# pylint: disable=R0915
class FingerprintTestCases(unittest.TestCase):
    """test cases for abydos.clustering.fingerprint,
    abydos.clustering.qgram_fingerprint, and
    abydos.clustering.phonetic_fingerprint
    """
    _testset = ('À noite, vovô Kowalsky vê o ímã cair no pé do pingüim \
queixoso e vovó põe açúcar no chá de tâmaras do jabuti feliz.', )
    _anssetw = ('a acucar cair cha de do e feliz ima jabuti kowalsky no noite \
o pe pinguim poe queixoso tamaras ve vovo', )
    _anssetq2 = ('abacadaialamanarasbucachcudedoeaedeieleoetevfeguhaifiminirit\
ixizjakokylilsmamqngnoocoeoiojokoposovowpepipoqurarnsdsksotatetiucueuiutvevowa\
xoyv', )
    _anssetq1 = ('abcdefghijklmnopqrstuvwxyz', )

    def test_fingerprint(self):
        """test abydos.clustering.fingerprint
        """
        self.assertEqual(fingerprint(''), '')
        for i in _range(len(self._testset)):
            self.assertEqual(fingerprint(self._testset[i]), self._anssetw[i])

    def test_qgram_fingerprint(self):
        """test abydos.clustering.qgram_fingerprint
        """
        self.assertEqual(qgram_fingerprint(''), '')
        for i in _range(len(self._testset)):
            self.assertEqual(qgram_fingerprint(self._testset[i], 1),
                              self._anssetq1[i])
            self.assertEqual(qgram_fingerprint(self._testset[i], 2),
                              self._anssetq2[i])
            self.assertEqual(qgram_fingerprint(self._testset[i]),
                              self._anssetq2[i])

    def test_phonetic_fingerprint(self):
        """test abydos.clustering.phonetic_fingerprint
        """
        self.assertEqual(phonetic_fingerprint(''), '')
        # TODO: add non-trivial tests
