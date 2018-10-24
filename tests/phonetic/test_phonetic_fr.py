# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.tests.test_phonetic_fr.

This module contains unit tests for abydos.phonetic.fr
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.fr import fonem, henry_early


class FonemTestCases(unittest.TestCase):
    """Test FONEM functions.

    test cases for abydos.phonetic.fonem
    """

    def test_fonem(self):
        """Test abydos.phonetic.fonem."""
        # Base cases
        self.assertEqual(fonem(''), '')

        # Test cases, mostly from the FONEM specification,
        # but copied from Talisman:
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/french/fonem.js
        test_cases = (
            ('BEAULAC', 'BOLAK'),
            ('BAULAC', 'BOLAK'),
            ('IMBEAULT', 'INBO'),
            ('DUFAUT', 'DUFO'),
            ('THIBOUTOT', 'TIBOUTOT'),
            ('DEVAUX', 'DEVO'),
            ('RONDEAUX', 'RONDO'),
            ('BOURGAULX', 'BOURGO'),
            ('PINCHAUD', 'PINCHO'),
            ('PEDNAULD', 'PEDNO'),
            ('MAZENOD', 'MASENOD'),
            ('ARNOLD', 'ARNOL'),
            ('BERTOLD', 'BERTOL'),
            ('BELLAY', 'BELE'),
            ('SANDAY', 'SENDE'),
            ('GAY', 'GAI'),
            ('FAYARD', 'FAYAR'),
            ('LEMIEUX', 'LEMIEU'),
            ('LHEUREUX', 'LEUREU'),
            ('BELLEY', 'BELE'),
            ('WELLEY', 'WELE'),
            ('MEYER', 'MEYER'),
            ('BOILY', 'BOILI'),
            ('LOYSEAU', 'LOISO'),
            ('MAYRAND', 'MAIREN'),
            ('GUYON', 'GUYON'),
            ('FAILLARD', 'FAYAR'),
            ('FAIARD', 'FAYAR'),
            ('MEIER', 'MEYER'),
            ('MEILLER', 'MEYER'),
            ('GUILLON', 'GUYON'),
            ('LAVILLE', 'LAVILLE'),
            ('COUET', 'CWET'),
            ('EDOUARD', 'EDWAR'),
            ('GIROUARD', 'JIRWAR'),
            ('OZOUADE', 'OSWADE'),  # differs from test set
            ('BOUILLE', 'BOUYE'),
            ('POUYEZ', 'POUYES'),  # differs from test set
            ('LEMEE', 'LEME'),
            ('ABRAAM', 'ABRAM'),
            ('ARCHEMBAULT', 'ARCHENBO'),
            ('AMTHIME', 'ENTIME'),
            ('ROMPRE', 'RONPRE'),
            ('BOMSECOURS', 'BONSECOURS'),
            ('BOULANGER', 'BOULENJER'),
            ('TANCREDE', 'TENKREDE'),
            ('BLAIN', 'BLIN'),
            ('BLAINVILLE', 'BLINVILLE'),
            ('MAINARD', 'MAINAR'),
            ('RAIMOND', 'RAIMON'),
            ('BLACKBORN', 'BLAKBURN'),
            ('SEABOURNE', 'SEABURN'),
            ('IMBO', 'INBO'),
            ('RIMFRET', 'RINFRET'),
            ('LEFEBVRE', 'LEFEVRE'),
            ('MACE', 'MASSE'),
            ('MACON', 'MACON'),
            ('MARCELIN', 'MARSELIN'),
            ('MARCEAU', 'MARSO'),
            ('VINCELETTE', 'VINSELETE'),
            ('FORCADE', 'FORCADE'),
            ('CELINE', 'SELINE'),
            ('CERAPHIN', 'SERAFIN'),
            ('CAMILLE', 'KAMILLE'),
            ('CAYETTE', 'KAYETE'),
            ('CARINE', 'KARINE'),
            ('LUC', 'LUK'),
            ('LEBLANC', 'LEBLEN'),
            ('VICTOR', 'VIKTOR'),
            ('LACCOULINE', 'LAKOULINE'),
            ('MACCIMILIEN', 'MAXIMILIEN'),
            ('MAGELLA', 'MAJELA'),
            ('GINETTE', 'JINETE'),
            ('GANDET', 'GANDET'),
            ('GEORGES', 'JORJES'),
            ('GEOFFROID', 'JOFROID'),
            ('PAGEAU', 'PAJO'),
            ('GAGNION', 'GAGNON'),
            ('MIGNIER', 'MIGNER'),
            ('HALLEY', 'ALE'),
            ('GAUTHIER', 'GOTIER'),
            ('CHARTIER', 'CHARTIER'),
            ('JEANNE', 'JANE'),
            ('MACGREGOR', 'MACGREGOR'),
            ('MACKAY', 'MACKE'),
            ('MCNICOL', 'MACNICOL'),
            ('MCNEIL', 'MACNEIL'),
            ('PHANEUF', 'FANEUF'),
            ('PHILIPPE', 'FILIPE'),
            ('QUENNEVILLE', 'KENEVILLE'),
            ('LAROCQUE', 'LAROKE'),
            ('SCIPION', 'SIPION'),
            ('ASCELIN', 'ASSELIN'),
            ('VASCO', 'VASKO'),
            ('PASCALINE', 'PASKALINE'),
            ('ESHEMBACK', 'ECHENBAK'),
            ('ASHED', 'ACHED'),
            ('GRATIA', 'GRASSIA'),
            ('PATRITIA', 'PATRISSIA'),
            ('BERTIO', 'BERTIO'),
            ('MATIEU', 'MATIEU'),
            ('BERTIAUME', 'BERTIOME'),
            ('MUNROW', 'MUNRO'),
            ('BRANISLAW', 'BRANISLA'),
            ('LOWMEN', 'LOMEN'),
            ('ANDREW', 'ENDREW'),
            ('EXCEL', 'EXEL'),
            ('EXCERINE', 'EXERINE'),
            ('EXSILDA', 'EXILDA'),
            ('EXZELDA', 'EXELDA'),
            ('CAZEAU', 'KASO'),
            ('BRAZEAU', 'BRASO'),
            ('FITZPATRICK', 'FITSPATRIK'),
            ('SINGELAIS', 'ST-JELAIS'),
            ('CINQMARS', 'ST-MARS'),
            ('SAINT-AMAND', 'ST-AMEN'),
            ('SAINTECROIX', 'STE-KROIX'),
            ('ST-HILAIRE', 'ST-ILAIRE'),
            ('STE-CROIX', 'STE-KROIX'),
            ('LAVALLEE', 'LAVALE'),
            ('CORINNE', 'KORINE'),
            ('DUTILE', 'DUTILLE'),
        )
        for name, encoding in test_cases:
            self.assertEqual(fonem(name), encoding)


class HenryCodeTestCases(unittest.TestCase):
    """Test Henry Code functions.

    test cases for abydos.phonetic.henry_early
    """

    def test_henry_early(self):
        """Test abydos.phonetic.henry_early."""
        # Base case
        self.assertEqual(henry_early(''), '')

        # Examples from Legare 1972 paper
        self.assertEqual(henry_early('Descarry'), 'DKR')
        self.assertEqual(henry_early('Descaries'), 'DKR')
        self.assertEqual(henry_early('Campo'), 'KP')
        self.assertEqual(henry_early('Campot'), 'KP')
        self.assertEqual(henry_early('Gausselin'), 'GSL')
        self.assertEqual(henry_early('Gosselin'), 'GSL')
        self.assertEqual(henry_early('Bergeron'), 'BRJ')
        self.assertEqual(henry_early('Bergereau'), 'BRJ')
        self.assertEqual(henry_early('Bosseron'), 'BSR')
        self.assertEqual(henry_early('Cicire'), 'SSR')
        self.assertEqual(henry_early('Lechevalier'), 'LCV')
        self.assertEqual(henry_early('Chevalier'), 'CVL')
        self.assertEqual(henry_early('Peloy'), 'PL')
        self.assertEqual(henry_early('Beloy'), 'BL')
        self.assertEqual(henry_early('Beret'), 'BR')
        self.assertEqual(henry_early('Benet'), 'BN')
        self.assertEqual(henry_early('Turcot'), 'TRK')
        self.assertEqual(henry_early('Turgot'), 'TRG')
        self.assertEqual(henry_early('Vigier'), 'VJ')
        self.assertEqual(henry_early('Vigiere'), 'VJR')
        self.assertEqual(henry_early('Dodin'), 'DD')
        self.assertEqual(henry_early('Dodelin'), 'DDL')

        # Tests to complete coverage
        self.assertEqual(henry_early('Anil'), 'ANL')
        self.assertEqual(henry_early('Emmanuel'), 'AMN')
        self.assertEqual(henry_early('Ainu'), 'EN')
        self.assertEqual(henry_early('Oeuf'), 'OF')
        self.assertEqual(henry_early('Yves'), 'IV')
        self.assertEqual(henry_early('Yo'), 'I')
        self.assertEqual(henry_early('Umman'), 'EM')
        self.assertEqual(henry_early('Omman'), 'OM')
        self.assertEqual(henry_early('Zoe'), 'S')
        self.assertEqual(henry_early('Beauchamp'), 'BCP')
        self.assertEqual(henry_early('Chloe'), 'KL')
        self.assertEqual(henry_early('Gerard'), 'JRR')
        self.assertEqual(henry_early('Agnes'), 'ANN')
        self.assertEqual(henry_early('Pinot'), 'PN')
        self.assertEqual(henry_early('Philo'), 'FL')
        self.assertEqual(henry_early('Quisling'), 'GL')
        self.assertEqual(henry_early('Qualite'), 'KLT')
        self.assertEqual(henry_early('Sainte-Marie'), 'XMR')
        self.assertEqual(henry_early('Saint-Jean'), 'XJ')
        self.assertEqual(henry_early('Ste-Marie'), 'XMR')
        self.assertEqual(henry_early('St-Jean'), 'XJ')
        self.assertEqual(henry_early('Cloe'), 'KL')
        self.assertEqual(henry_early('Ahch-To'), 'AKT')
        self.assertEqual(henry_early('Zdavros'), 'SDV')
        self.assertEqual(henry_early('Sdavros'), 'DVR')
        self.assertEqual(henry_early('Coulomb'), 'KLB')
        self.assertEqual(henry_early('Calm'), 'K')
        self.assertEqual(henry_early('Omnia'), 'ON')
        self.assertEqual(henry_early('Ramps'), 'RPS')
        self.assertEqual(henry_early('Renault'), 'RN')
        self.assertEqual(henry_early('Czech'), 'CSK')
        self.assertEqual(henry_early('Imran'), 'ER')
        self.assertEqual(henry_early('Christopher', max_length=-1), 'KRXF')


if __name__ == '__main__':
    unittest.main()
