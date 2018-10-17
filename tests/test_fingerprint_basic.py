# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tests.test_fingerprint.basic.

This module contains unit tests for abydos.fingerprint.basic
"""

from __future__ import unicode_literals

import unittest

import abydos.phonetic as phonetic
from abydos.fingerprint.basic import phonetic_fingerprint, qgram_fingerprint, \
    str_fingerprint

from six.moves import range


NIALL = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel', 'Nele',
         'Nigelli', 'Nel', 'Kneale', 'Uí Néill', 'O\'Neill', 'MacNeil',
         'MacNele', 'Niall Noígíallach')


class FingerprintTestCases(unittest.TestCase):
    """Test basic fingerprint functions.

    abydos.fingerprint.basic.str_fingerprint, .qgram_fingerprint, &
    .phonetic_fingerprint
    """

    _testset = ('À noite, vovô Kowalsky vê o ímã cair no pé do pingüim \
queixoso e vovó põe açúcar no chá de tâmaras do jabuti feliz.', )
    _anssetw = ('a acucar cair cha de do e feliz ima jabuti kowalsky no noite \
o pe pinguim poe queixoso tamaras ve vovo', )
    _anssetq2 = ('abacadaialamanarasbucachcudedoeaedeieleoetevfeguhaifiminirit\
ixizjakokylilsmamqngnoocoeoiojokoposovowpepipoqurarnsdsksotatetiucueuiutvevowa\
xoyv', )
    _anssetq1 = ('abcdefghijklmnopqrstuvwxyz', )

    def test_str_fingerprint(self):
        """Test abydos.fingerprint.basic.str_fingerprint."""
        # Base case
        self.assertEqual(str_fingerprint(''), '')

        for i in range(len(self._testset)):
            self.assertEqual(str_fingerprint(self._testset[i]),
                             self._anssetw[i])

    def test_qgram_fingerprint(self):
        """Test abydos.fingerprint.basic.qgram_fingerprint."""
        # Base case
        self.assertEqual(qgram_fingerprint(''), '')

        for i in range(len(self._testset)):
            self.assertEqual(qgram_fingerprint(self._testset[i], 1),
                             self._anssetq1[i])
            self.assertEqual(qgram_fingerprint(self._testset[i], 2),
                             self._anssetq2[i])
            self.assertEqual(qgram_fingerprint(self._testset[i]),
                             self._anssetq2[i])

        qgram_fp_niall = ('aliallni', 'aleane', 'eiilne', 'aljallnj',
                          'aljallnj', 'elgeigni', 'eeelne', 'ellene',
                          'elgeiglillni', 'elne', 'aleaknlene', 'eiilinllneui',
                          'eiilllneon', 'accneiilmane', 'accnellemane',
                          'acalchgiiaiglalllnninooi')
        for i in range(len(NIALL)):
            self.assertEqual(qgram_fingerprint(NIALL[i]), qgram_fp_niall[i])

    def test_phonetic_fingerprint(self):
        """Test abydos.fingerprint.basic.phonetic_fingerprint."""
        # Base case
        self.assertEqual(phonetic_fingerprint(''), '')

        self.assertEqual(phonetic_fingerprint(' '.join(NIALL)),
                         'a anl mknl njl nklk nl')
        self.assertEqual(phonetic_fingerprint(' '.join(NIALL),
                                              phonetic.phonet),
                         'knile makneil maknele neil nel nele nial nigeli ' +
                         'nigl nil noigialach oneil ui')
        self.assertEqual(phonetic_fingerprint(' '.join(NIALL),
                                              phonetic.soundex),
                         'k540 m254 n240 n242 n400 o540 u000')


if __name__ == '__main__':
    unittest.main()
