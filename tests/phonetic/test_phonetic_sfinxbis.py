# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_sfinxbis.

This module contains unit tests for abydos.phonetic.SfinxBis
"""

import unittest

from abydos.phonetic import SfinxBis, sfinxbis


class SfinxBisTestCases(unittest.TestCase):
    """Test SfinxBis functions.

    test cases for abydos.phonetic.SfinxBis
    """

    pa = SfinxBis()
    pa4 = SfinxBis(4)

    def test_sfinxbis(self):
        """Test abydos.phonetic.SfinxBis."""
        self.assertEqual(self.pa.encode(''), ('',))

        # http://www.swami.se/download/18.248ad5af12aa81365338000106/TestSfinx.txt
        # cases where the gold standard gave clearly wrong values have been
        # corrected below (marked with '# wrong'
        self.assertEqual(self.pa.encode('af Sandeberg'), ('S53162',))
        self.assertEqual(self.pa.encode('av Ekenstam'), ('$25835',))
        self.assertEqual(self.pa.encode('Da Costa'), ('K83',))
        self.assertEqual(self.pa.encode('Das Neves'), ('D8', 'N78'))
        self.assertEqual(self.pa.encode('de Besche'), ('B8',))
        self.assertEqual(self.pa.encode('de la Motte'), ('M3',))
        self.assertEqual(self.pa.encode('de Las Heras'), ('H68',))  # wrong
        self.assertEqual(self.pa.encode('de Los Santos'), ('S538',))
        self.assertEqual(self.pa.encode('del Rosario'), ('R862',))
        self.assertEqual(self.pa.encode('Den Boer'), ('B6',))
        self.assertEqual(
            self.pa.encode('Der de Kazinczy'), ('D6', 'K8528')
        )  # wrong
        self.assertEqual(self.pa.encode('des Rieux'), ('R28',))
        self.assertEqual(self.pa.encode('Di Luca'), ('L2',))
        self.assertEqual(self.pa.encode('Do Rosario'), ('R862',))
        self.assertEqual(self.pa.encode('Don Lind'), ('L53',))
        self.assertEqual(self.pa.encode('Dos Santos'), ('S538',))
        self.assertEqual(self.pa.encode('du Rietz'), ('R38',))
        self.assertEqual(self.pa.encode('in de Betou'), ('B3',))
        self.assertEqual(self.pa.encode('La Fleur'), ('F46',))
        self.assertEqual(self.pa.encode('Le Grand'), ('G653',))
        self.assertEqual(self.pa.encode('li Puma'), ('L', 'P5'))
        self.assertEqual(self.pa.encode('lo Martire'), ('L', 'M636'))
        self.assertEqual(self.pa.encode('mac Donald'), ('D543',))
        self.assertEqual(self.pa.encode('mc Intosh'), ('$538',))
        self.assertEqual(self.pa.encode('S:t Cyr'), ('S6',))
        self.assertEqual(self.pa.encode('Van Doom'), ('D5',))
        self.assertEqual(self.pa.encode('Van de Peppel'), ('P14',))
        self.assertEqual(self.pa.encode('Van den Berg'), ('B62',))
        self.assertEqual(self.pa.encode('Van Der Kwast'), ('K783',))
        self.assertEqual(self.pa.encode('von Ahn'), ('$5',))
        self.assertEqual(self.pa.encode('von Dem Knesebeck'), ('K5812',))
        self.assertEqual(self.pa.encode('von Der Burg'), ('B62',))
        self.assertEqual(self.pa.encode("D'Angelo"), ('D524',))
        self.assertEqual(self.pa.encode("O'Conner"), ('$256',))
        self.assertEqual(self.pa.encode('Los'), ('L8',))
        self.assertEqual(self.pa.encode('Mac'), ('M2',))
        self.assertEqual(self.pa.encode('Till'), ('T4',))
        self.assertEqual(self.pa.encode('Van'), ('V5',))
        self.assertEqual(self.pa.encode('Von'), ('V5',))
        self.assertEqual(
            self.pa.encode('Bernadotte af Wisborg'), ('B6533', 'V8162')
        )
        self.assertEqual(self.pa.encode('Hjort af Ornäs'), ('J63', '$658'))
        self.assertEqual(self.pa.encode('Horn af Åminne'), ('H65', '$55'))
        self.assertEqual(self.pa.encode('Horn av Åminne'), ('H65', '$55'))
        self.assertEqual(
            self.pa.encode('Hård af Segerstad'), ('H63', 'S26833')
        )
        self.assertEqual(
            self.pa.encode('Hård av Segerstad'), ('H63', 'S26833')
        )
        self.assertEqual(
            self.pa.encode('Stael von Holstein'), ('S34', 'H48325')
        )
        self.assertEqual(
            self.pa.encode('de Oliveira e Silva'), ('$4726', 'S47')
        )
        self.assertEqual(self.pa.encode('de Alfaro y Gómez'), ('$476', 'G58'))
        self.assertEqual(
            self.pa.encode('Arjaliès-de la Lande'), ('$6248', 'L53')
        )
        self.assertEqual(
            self.pa.encode('Dominicus van den Bussche'), ('D5528', 'B8')
        )
        self.assertEqual(
            self.pa.encode('Edebol Eeg-Olofsson'), ('$314', '$2', '$4785')
        )
        self.assertEqual(
            self.pa.encode('Jonsson-Blomqvist'), ('J585', 'B452783')
        )
        self.assertEqual(
            self.pa.encode('Kiviniemi Birgersson'), ('#755', 'B62685')
        )
        self.assertEqual(
            self.pa.encode('Massena Serpa dos Santos'), ('M85', 'S61', 'S538')
        )
        self.assertEqual(self.pa.encode('S:t Clair Renard'), ('K426', 'R563'))
        self.assertEqual(
            self.pa.encode('Skoog H Andersson'), ('S22', 'H', '$53685')
        )
        self.assertEqual(
            self.pa.encode('von Post-Skagegård'), ('P83', 'S22263')
        )
        self.assertEqual(self.pa.encode('von Zur-Mühlen'), ('S6', 'M45'))
        self.assertEqual(self.pa.encode('Waltå O:son'), ('V43', '$85'))
        self.assertEqual(
            self.pa.encode('Zardán Gómez de la Torre'), ('S635', 'G58', 'T6')
        )
        self.assertEqual(self.pa.encode('af Jochnick'), ('J252',))
        self.assertEqual(self.pa.encode('af Ioscnick'), ('J8252',))
        self.assertEqual(self.pa.encode('Aabakken'), ('$125',))
        self.assertEqual(self.pa.encode('Åbacken'), ('$125',))
        self.assertEqual(self.pa.encode('Ahlen'), ('$45',))
        self.assertEqual(self.pa.encode('Aleen'), ('$45',))
        self.assertEqual(self.pa.encode('Braunerhielm'), ('B656245',))
        self.assertEqual(self.pa.encode('Branneerhielm'), ('B656245',))
        self.assertEqual(self.pa.encode('Carlzon'), ('K6485',))
        self.assertEqual(self.pa.encode('Karlsson'), ('K6485',))
        self.assertEqual(self.pa.encode('Enochsson'), ('$5285',))
        self.assertEqual(self.pa.encode('Ericsson'), ('$6285',))
        self.assertEqual(self.pa.encode('Ericksson'), ('$6285',))
        self.assertEqual(self.pa.encode('Erixson'), ('$6285',))
        self.assertEqual(self.pa.encode('Filipsson'), ('F4185',))
        self.assertEqual(self.pa.encode('Philipson'), ('F4185',))
        self.assertEqual(self.pa.encode('Flycht'), ('F423',))
        self.assertEqual(self.pa.encode('Flygt'), ('F423',))
        self.assertEqual(self.pa.encode('Flykt'), ('F423',))
        self.assertEqual(self.pa.encode('Fröijer'), ('F626',))
        self.assertEqual(self.pa.encode('Fröjer'), ('F626',))
        self.assertEqual(self.pa.encode('Gertner'), ('J6356',))
        self.assertEqual(self.pa.encode('Hiertner'), ('J6356',))
        self.assertEqual(self.pa.encode('Hirch'), ('H62',))
        self.assertEqual(self.pa.encode('Hirsch'), ('H68',))
        self.assertEqual(self.pa.encode('Haegermarck'), ('H26562',))
        self.assertEqual(self.pa.encode('Hägermark'), ('H26562',))
        self.assertEqual(self.pa.encode('Isaxon'), ('$8285',))
        self.assertEqual(self.pa.encode('Isacsson'), ('$8285',))
        self.assertEqual(self.pa.encode('Joachimsson'), ('J2585',))
        self.assertEqual(self.pa.encode('Joakimson'), ('J2585',))
        self.assertEqual(self.pa.encode('Kjell'), ('#4',))
        self.assertEqual(self.pa.encode('Käll'), ('#4',))
        self.assertEqual(self.pa.encode('Knapp'), ('K51',))
        self.assertEqual(self.pa.encode('Krans'), ('K658',))
        self.assertEqual(self.pa.encode('Krantz'), ('K6538',))
        self.assertEqual(self.pa.encode('Kvist'), ('K783',))
        self.assertEqual(self.pa.encode('Quist'), ('K783',))
        self.assertEqual(self.pa.encode('Lidbeck'), ('L312',))
        self.assertEqual(self.pa.encode('Lidbäck'), ('L312',))
        self.assertEqual(self.pa.encode('Linnér'), ('L56',))
        self.assertEqual(self.pa.encode('Linner'), ('L56',))
        self.assertEqual(self.pa.encode('Lorenzsonn'), ('L6585',))
        self.assertEqual(self.pa.encode('Lorentzon'), ('L65385',))
        self.assertEqual(self.pa.encode('Lorenßon'), ('L6585',))
        self.assertEqual(self.pa.encode('Lyxell'), ('L284',))
        self.assertEqual(self.pa.encode('Lycksell'), ('L284',))
        self.assertEqual(self.pa.encode('Marcström'), ('M628365',))
        self.assertEqual(self.pa.encode('Markström'), ('M628365',))
        self.assertEqual(self.pa.encode('Michaelsson'), ('M2485',))
        self.assertEqual(self.pa.encode('Mikaelson'), ('M2485',))
        self.assertEqual(self.pa.encode('Mörch'), ('M62',))
        self.assertEqual(self.pa.encode('Mörck'), ('M62',))
        self.assertEqual(self.pa.encode('Mörk'), ('M62',))
        self.assertEqual(self.pa.encode('Mørk'), ('M62',))
        self.assertEqual(self.pa.encode('Nääs'), ('N8',))
        self.assertEqual(self.pa.encode('Naess'), ('N8',))
        self.assertEqual(self.pa.encode('Nordstedt'), ('N63833',))
        self.assertEqual(self.pa.encode('Oxenstierna'), ('$28583265',))
        self.assertEqual(self.pa.encode('Palmçrañtz'), ('P4526538',))
        self.assertEqual(self.pa.encode('Palmcrantz'), ('P4526538',))
        self.assertEqual(self.pa.encode('Palmkrantz'), ('P4526538',))
        self.assertEqual(self.pa.encode('Preuss'), ('P68',))
        self.assertEqual(self.pa.encode('Preutz'), ('P638',))
        self.assertEqual(self.pa.encode('Richardson'), ('R26385',))
        self.assertEqual(self.pa.encode('Rikardson'), ('R26385',))
        self.assertEqual(self.pa.encode('Ruuth'), ('R3',))
        self.assertEqual(self.pa.encode('Ruth'), ('R3',))
        self.assertEqual(self.pa.encode('Sæter'), ('S36',))
        self.assertEqual(self.pa.encode('Zäter'), ('S36',))
        self.assertEqual(self.pa.encode('Schedin'), ('#35',))
        self.assertEqual(self.pa.encode('Sjödin'), ('#35',))
        self.assertEqual(self.pa.encode('Siöö'), ('#',))
        self.assertEqual(self.pa.encode('Sjöh'), ('#',))
        self.assertEqual(self.pa.encode('Svedberg'), ('S73162',))
        self.assertEqual(self.pa.encode('Zwedberg'), ('S73162',))
        self.assertEqual(self.pa.encode('Tjäder'), ('#36',))
        self.assertEqual(self.pa.encode('þornquist'), ('T652783',))
        self.assertEqual(self.pa.encode('Thörnqvist'), ('T652783',))
        self.assertEqual(self.pa.encode('Törnkvist'), ('T652783',))
        self.assertEqual(self.pa.encode('Wichman'), ('V255',))
        self.assertEqual(self.pa.encode('Wickman'), ('V255',))
        self.assertEqual(self.pa.encode('Wictorin'), ('V2365',))
        self.assertEqual(self.pa.encode('Wictorsson'), ('V23685',))
        self.assertEqual(self.pa.encode('Viktorson'), ('V23685',))
        self.assertEqual(self.pa.encode('Zachrisson'), ('S2685',))
        self.assertEqual(self.pa.encode('Zakrison'), ('S2685',))
        self.assertEqual(self.pa.encode('Övragård'), ('$76263',))
        self.assertEqual(self.pa.encode('Öfvragårdh'), ('$76263',))
        self.assertEqual(self.pa.encode('Bogdanovic'), ('B23572',))
        self.assertEqual(self.pa.encode('Bogdanovitch'), ('B235732',))
        self.assertEqual(self.pa.encode('Dieterich'), ('D362',))
        self.assertEqual(self.pa.encode('Eichorn'), ('$265',))
        self.assertEqual(self.pa.encode('Friedrich'), ('F6362',))
        self.assertEqual(self.pa.encode('Grantcharova'), ('G653267',))
        self.assertEqual(self.pa.encode('Ilichev'), ('$427',))
        self.assertEqual(self.pa.encode('Ivankovic'), ('$75272',))
        self.assertEqual(self.pa.encode('Ivangurich'), ('$75262',))
        self.assertEqual(self.pa.encode('Kinch'), ('#52',))
        self.assertEqual(self.pa.encode('Kirchmann'), ('#6255',))
        self.assertEqual(self.pa.encode('Machado'), ('M23',))
        self.assertEqual(self.pa.encode('Reich'), ('R2',))
        self.assertEqual(self.pa.encode('Roche'), ('R2',))
        self.assertEqual(self.pa.encode('Rubaszkin'), ('R1825',))
        self.assertEqual(self.pa.encode('Rubaschkin'), ('R1825',))
        self.assertEqual(self.pa.encode('Sanchez'), ('S528',))
        self.assertEqual(self.pa.encode('Walukiewicz'), ('V42728',))
        self.assertEqual(self.pa.encode('Valukievitch'), ('V42732',))
        self.assertEqual(self.pa.encode('K'), ('K',))
        self.assertEqual(self.pa.encode('2010'), ('',))
        self.assertEqual(self.pa.encode('cese'), ('S8',))

        # a few max_length tests
        self.assertEqual(
            SfinxBis(3).encode('Kiviniemi Birgersson'), ('#75', 'B62')
        )
        self.assertEqual(self.pa4.encode('Eichorn'), ('$265',))
        self.assertEqual(self.pa4.encode('Friedrich'), ('F636',))
        self.assertEqual(self.pa4.encode('Grantcharova'), ('G653',))
        self.assertEqual(self.pa4.encode('Ilichev'), ('$427',))
        self.assertEqual(self.pa4.encode('Ivankovic'), ('$752',))
        self.assertEqual(self.pa4.encode('Ivangurich'), ('$752',))
        self.assertEqual(self.pa4.encode('Kinch'), ('#52',))
        self.assertEqual(self.pa4.encode('Kirchmann'), ('#625',))
        self.assertEqual(self.pa4.encode('Machado'), ('M23',))
        self.assertEqual(self.pa4.encode('Reich'), ('R2',))
        self.assertEqual(self.pa4.encode('Roche'), ('R2',))
        self.assertEqual(self.pa4.encode('Rubaszkin'), ('R182',))
        self.assertEqual(self.pa4.encode('Rubaschkin'), ('R182',))
        self.assertEqual(self.pa4.encode('Sanchez'), ('S528',))
        self.assertEqual(self.pa4.encode('Walukiewicz'), ('V427',))
        self.assertEqual(self.pa4.encode('Valukievitch'), ('V427',))
        self.assertEqual(self.pa4.encode('K'), ('K',))
        self.assertEqual(self.pa4.encode('2010'), ('',))
        self.assertEqual(self.pa4.encode('cese'), ('S8',))

        # etc. (for code coverage)
        self.assertEqual(self.pa.encode('chans'), ('#58',))
        self.assertEqual(self.pa.encode('ljud'), ('J3',))
        self.assertEqual(self.pa.encode('qi'), ('K',))
        self.assertEqual(self.pa.encode('xavier'), ('S76',))
        self.assertEqual(self.pa.encode('skjul'), ('#4',))
        self.assertEqual(self.pa.encode('schul'), ('#4',))
        self.assertEqual(self.pa.encode('skil'), ('#4',))

        # max_length bounds tests
        self.assertEqual(SfinxBis(max_length=-1).encode('Niall'), ('N4',))
        self.assertEqual(SfinxBis(max_length=0).encode('Niall'), ('N4',))

        # encode_alpha
        self.assertEqual(
            self.pa.encode_alpha('Stael von Holstein'), ('STL', 'HLSTKN')
        )
        self.assertEqual(
            self.pa.encode_alpha('de Oliveira e Silva'), ('$LFKR', 'SLF')
        )
        self.assertEqual(
            self.pa.encode_alpha('de Alfaro y Gómez'), ('$LFR', 'GNS')
        )
        self.assertEqual(
            self.pa.encode_alpha('Arjaliès-de la Lande'), ('$RKLS', 'LNT')
        )

        # Test wrapper
        self.assertEqual(sfinxbis('af Sandeberg'), ('S53162',))


if __name__ == '__main__':
    unittest.main()
