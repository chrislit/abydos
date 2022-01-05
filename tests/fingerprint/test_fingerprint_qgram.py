# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.fingerprint.test_fingerprint_qgram_fingerprint.

This module contains unit tests for abydos.fingerprint.QGram
"""

import unittest

from abydos.fingerprint import QGram

from .. import NIALL


class QGramTestCases(unittest.TestCase):
    """Test q-gram fingerprint functions.

    abydos.fingerprint.QGram
    """

    fp = QGram()

    _testset = (
        'À noite, vovô Kowalsky vê o ímã cair no pé do pingüim \
queixoso e vovó põe açúcar no chá de tâmaras do jabuti feliz.',
    )
    _anssetq2 = (
        'abacadaialamanarasbucachcudedoeaedeieleoetevfeguhaifiminirit\
ixizjakokylilsmamqngnoocoeoiojokoposovowpepipoqurarnsdsksotatetiucueuiutvevowa\
xoyv',
    )
    _anssetq1 = ('abcdefghijklmnopqrstuvwxyz',)

    def test_qgram_fingerprint(self):
        """Test abydos.fingerprint.QGram."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '')

        for i in range(len(self._testset)):
            self.assertEqual(
                QGram(1).fingerprint(self._testset[i]), self._anssetq1[i]
            )
            self.assertEqual(
                QGram(2).fingerprint(self._testset[i]), self._anssetq2[i]
            )
            self.assertEqual(
                self.fp.fingerprint(self._testset[i]), self._anssetq2[i]
            )

        qgram_fp_niall = (
            'aliallni',
            'aleane',
            'eiilne',
            'aljallnj',
            'aljallnj',
            'elgeigni',
            'eeelne',
            'ellene',
            'elgeiglillni',
            'elne',
            'aleaknlene',
            'eiilinllneui',
            'eiilllneon',
            'accneiilmane',
            'accnellemane',
            'acalchgiiaiglalllnninooi',
        )
        for i in range(len(NIALL)):
            self.assertEqual(self.fp.fingerprint(NIALL[i]), qgram_fp_niall[i])


if __name__ == '__main__':
    unittest.main()
