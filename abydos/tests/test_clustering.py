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
    phonetic_fingerprint, skeleton_key, omission_key, mean_pairwise_similarity
import abydos.stats as stats
import abydos.phonetic as phonetic

NIALL = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel', 'Nele',
         'Nigelli', 'Nel', 'Kneale', 'Uí Néill', 'O\'Neill', 'MacNeil',
         'MacNele', 'Niall Noígíallach')

NIALL_1WORD = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel',
               'Nele', 'Nigelli', 'Nel', 'Kneale', 'O\'Neill', 'MacNeil',
               'MacNele')

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

        qgram_fp_niall = ('aliallni', 'aleane', 'eiilne', 'aljallnj',
                          'aljallnj', 'elgeigni', 'eeelne', 'ellene',
                          'elgeiglillni', 'elne', 'aleaknlene', 'eiilinllneui',
                          'eiilllneon', 'accneiilmane', 'accnellemane',
                          'acalchgiiaiglalllnninooi')
        for i in _range(len(NIALL)):
            self.assertEqual(qgram_fingerprint(NIALL[i]), qgram_fp_niall[i])

    def test_phonetic_fingerprint(self):
        """test abydos.clustering.phonetic_fingerprint
        """
        self.assertEqual(phonetic_fingerprint(''), '')

        self.assertEqual(phonetic_fingerprint(' '.join(NIALL)),
                         'a anl mknl njl nklk nl')
        self.assertEqual(phonetic_fingerprint(' '.join(NIALL), phonetic.phonet),
                         'knile makneil maknele neil nel nele nial nigeli nigl'+
                         ' nil noigialach oneil ui')
        self.assertEqual(phonetic_fingerprint(' '.join(NIALL),
                                              phonetic.soundex),
                         'k540 m254 n240 n242 n400 o540 u000')

class SPEEDCOPTestCases(unittest.TestCase):
    """test cases for abydos.clustering.skeleton_key and
    abydos.clustering.omission_key
    """
    def test_skeleton_key(self):
        """test abydos.clustering.skeleton_key
        """
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
        """test abydos.clustering.omission_key
        """
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


class MPSTestCases(unittest.TestCase):
    """test cases for abydos.clustering.mean_pairwise_similarity
    """
    def test_mean_pairwise_similarity(self):
        """test abydos.clustering.mean_pairwise_similarity
        """
        self.assertEqual(mean_pairwise_similarity(NIALL), 0.29362587170180676)
        self.assertEqual(mean_pairwise_similarity(NIALL, symmetric=True),
                         0.29362587170180632)
        self.assertEqual(mean_pairwise_similarity(NIALL, meanfunc=stats.hmean),
                         0.29362587170180676)
        self.assertEqual(mean_pairwise_similarity(NIALL, meanfunc=stats.hmean,
                                                  symmetric=True),
                         0.29362587170180632)
        self.assertEqual(mean_pairwise_similarity(NIALL, meanfunc=stats.gmean),
                         0.33747245800668441)
        self.assertEqual(mean_pairwise_similarity(NIALL, meanfunc=stats.gmean,
                                                  symmetric=True),
                         0.33747245800668441)
        self.assertEqual(mean_pairwise_similarity(NIALL, meanfunc=stats.amean),
                         0.38009278711484623)
        self.assertEqual(mean_pairwise_similarity(NIALL, meanfunc=stats.amean,
                                                  symmetric=True),
                         0.38009278711484584)

        self.assertEqual(mean_pairwise_similarity(NIALL_1WORD),
                         mean_pairwise_similarity(' '.join(NIALL_1WORD)))
        self.assertEqual(mean_pairwise_similarity(NIALL_1WORD, symmetric=True),
                         mean_pairwise_similarity(' '.join(NIALL_1WORD),
                                                  symmetric=True))
        self.assertEqual(mean_pairwise_similarity(NIALL_1WORD,
                                                  meanfunc=stats.gmean),
                         mean_pairwise_similarity(' '.join(NIALL_1WORD),
                                                  meanfunc=stats.gmean))
        self.assertEqual(mean_pairwise_similarity(NIALL_1WORD,
                                                  meanfunc=stats.amean),
                         mean_pairwise_similarity(' '.join(NIALL_1WORD),
                                                  meanfunc=stats.amean))

        self.assertRaises(ValueError, mean_pairwise_similarity, ['a b c'])
        self.assertRaises(ValueError, mean_pairwise_similarity, 'abc')
        self.assertRaises(ValueError, mean_pairwise_similarity, 0)
        self.assertRaises(ValueError, mean_pairwise_similarity, NIALL,
                          meanfunc='imaginary')

        self.assertEqual(mean_pairwise_similarity(NIALL),
                         mean_pairwise_similarity(tuple(NIALL)))
        self.assertEqual(mean_pairwise_similarity(NIALL),
                         mean_pairwise_similarity(list(NIALL)))
        self.assertAlmostEqual(mean_pairwise_similarity(NIALL),
                               mean_pairwise_similarity(sorted(NIALL)))
        self.assertAlmostEqual(mean_pairwise_similarity(NIALL),
                               mean_pairwise_similarity(set(NIALL)))


if __name__ == '__main__':
    unittest.main()
