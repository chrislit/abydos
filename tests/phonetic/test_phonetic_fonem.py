# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_fonem.

This module contains unit tests for abydos.phonetic.FONEM
"""

import unittest

from abydos.phonetic import FONEM


class FONEMTestCases(unittest.TestCase):
    """Test FONEM functions.

    test cases for abydos.phonetic.FONEM
    """

    pa = FONEM()

    def test_fonem(self):
        """Test abydos.phonetic.FONEM."""
        # Base cases
        self.assertEqual(self.pa.encode(''), '')

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
            self.assertEqual(self.pa.encode(name), encoding)


if __name__ == '__main__':
    unittest.main()
