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

"""abydos.tests.test_fingerprint.

This module contains unit tests for abydos.fingerprint
"""

from __future__ import unicode_literals

import unittest

import abydos.phonetic as phonetic
from abydos.fingerprint import fingerprint, omission_key, \
    phonetic_fingerprint, qgram_fingerprint, skeleton_key

from six.moves import range


NIALL = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel', 'Nele',
         'Nigelli', 'Nel', 'Kneale', 'Uí Néill', 'O\'Neill', 'MacNeil',
         'MacNele', 'Niall Noígíallach')


class FingerprintTestCases(unittest.TestCase):
    """Test fingerprint functions.

    abydos.clustering.fingerprint, abydos.clustering.qgram_fingerprint, &
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
        """Test abydos.clustering.fingerprint."""
        self.assertEqual(fingerprint(''), '')
        for i in range(len(self._testset)):
            self.assertEqual(fingerprint(self._testset[i]), self._anssetw[i])

    def test_qgram_fingerprint(self):
        """Test abydos.clustering.qgram_fingerprint."""
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
        """Test abydos.clustering.phonetic_fingerprint."""
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


class SPEEDCOPTestCases(unittest.TestCase):
    """Test SPEEDCOP functions.

    abydos.clustering.skeleton_key & abydos.clustering.omission_key
    """

    def test_skeleton_key(self):
        """Test abydos.clustering.skeleton_key."""
        self.assertEqual(skeleton_key(''), '')

        # http://dl.acm.org/citation.cfm?id=358048
        self.assertEqual(skeleton_key('chemogenic'), 'CHMGNEOI')
        self.assertEqual(skeleton_key('chemomagnetic'), 'CHMGNTEOAI')
        self.assertEqual(skeleton_key('chemcal'), 'CHMLEA')
        self.assertEqual(skeleton_key('chemcial'), 'CHMLEIA')
        self.assertEqual(skeleton_key('chemical'), 'CHMLEIA')
        self.assertEqual(skeleton_key('chemicial'), 'CHMLEIA')
        self.assertEqual(skeleton_key('chimical'), 'CHMLIA')
        self.assertEqual(skeleton_key('chemiluminescence'), 'CHMLNSEIU')
        self.assertEqual(skeleton_key('chemiluminescent'), 'CHMLNSTEIU')
        self.assertEqual(skeleton_key('chemicals'), 'CHMLSEIA')
        self.assertEqual(skeleton_key('chemically'), 'CHMLYEIA')

    def test_omission_key(self):
        """Test abydos.clustering.omission_key."""
        self.assertEqual(omission_key(''), '')

        # http://dl.acm.org/citation.cfm?id=358048
        self.assertEqual(omission_key('microelectronics'), 'MCLNTSRIOE')
        self.assertEqual(omission_key('circumstantial'), 'MCLNTSRIUA')
        self.assertEqual(omission_key('luminescent'), 'MCLNTSUIE')
        self.assertEqual(omission_key('multinucleate'), 'MCLNTUIEA')
        self.assertEqual(omission_key('multinucleon'), 'MCLNTUIEO')
        self.assertEqual(omission_key('cumulene'), 'MCLNUE')
        self.assertEqual(omission_key('luminance'), 'MCLNUIAE')
        self.assertEqual(omission_key('coelomic'), 'MCLOEI')
        self.assertEqual(omission_key('molecule'), 'MCLOEU')
        self.assertEqual(omission_key('cameral'), 'MCLRAE')
        self.assertEqual(omission_key('caramel'), 'MCLRAE')
        self.assertEqual(omission_key('maceral'), 'MCLRAE')
        self.assertEqual(omission_key('lacrimal'), 'MCLRAI')


if __name__ == '__main__':
    unittest.main()
