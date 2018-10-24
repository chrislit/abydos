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

"""abydos.tests.test_phonetic_sv.

This module contains unit tests for abydos.phonetic.sv
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.sv import norphone, sfinxbis


class SfinxBisTestCases(unittest.TestCase):
    """Test SfinxBis functions.

    test cases for abydos.phonetic.sfinxbis
    """

    def test_sfinxbis(self):
        """Test abydos.phonetic.sfinxbis."""
        self.assertEqual(sfinxbis(''), ('',))

        # http://www.swami.se/download/18.248ad5af12aa81365338000106/TestSfinx.txt
        # cases where the gold standard gave clearly wrong values have been
        # corrected below (marked with '# wrong'
        self.assertEqual(sfinxbis('af Sandeberg'), ('S53162',))
        self.assertEqual(sfinxbis('av Ekenstam'), ('$25835',))
        self.assertEqual(sfinxbis('Da Costa'), ('K83',))
        self.assertEqual(sfinxbis('Das Neves'), ('D8', 'N78'))
        self.assertEqual(sfinxbis('de Besche'), ('B8',))
        self.assertEqual(sfinxbis('de la Motte'), ('M3',))
        self.assertEqual(sfinxbis('de Las Heras'), ('H68',))  # wrong
        self.assertEqual(sfinxbis('de Los Santos'), ('S538',))
        self.assertEqual(sfinxbis('del Rosario'), ('R862',))
        self.assertEqual(sfinxbis('Den Boer'), ('B6',))
        self.assertEqual(sfinxbis('Der de Kazinczy'), ('D6', 'K8528'))  # wrong
        self.assertEqual(sfinxbis('des Rieux'), ('R28',))
        self.assertEqual(sfinxbis('Di Luca'), ('L2',))
        self.assertEqual(sfinxbis('Do Rosario'), ('R862',))
        self.assertEqual(sfinxbis('Don Lind'), ('L53',))
        self.assertEqual(sfinxbis('Dos Santos'), ('S538',))
        self.assertEqual(sfinxbis('du Rietz'), ('R38',))
        self.assertEqual(sfinxbis('in de Betou'), ('B3',))
        self.assertEqual(sfinxbis('La Fleur'), ('F46',))
        self.assertEqual(sfinxbis('Le Grand'), ('G653',))
        self.assertEqual(sfinxbis('li Puma'), ('L', 'P5'))
        self.assertEqual(sfinxbis('lo Martire'), ('L', 'M636'))
        self.assertEqual(sfinxbis('mac Donald'), ('D543',))
        self.assertEqual(sfinxbis('mc Intosh'), ('$538',))
        self.assertEqual(sfinxbis('S:t Cyr'), ('S6',))
        self.assertEqual(sfinxbis('Van Doom'), ('D5',))
        self.assertEqual(sfinxbis('Van de Peppel'), ('P14',))
        self.assertEqual(sfinxbis('Van den Berg'), ('B62',))
        self.assertEqual(sfinxbis('Van Der Kwast'), ('K783',))
        self.assertEqual(sfinxbis('von Ahn'), ('$5',))
        self.assertEqual(sfinxbis('von Dem Knesebeck'), ('K5812',))
        self.assertEqual(sfinxbis('von Der Burg'), ('B62',))
        self.assertEqual(sfinxbis('D\'Angelo'), ('D524',))
        self.assertEqual(sfinxbis('O\'Conner'), ('$256',))
        self.assertEqual(sfinxbis('Los'), ('L8',))
        self.assertEqual(sfinxbis('Mac'), ('M2',))
        self.assertEqual(sfinxbis('Till'), ('T4',))
        self.assertEqual(sfinxbis('Van'), ('V5',))
        self.assertEqual(sfinxbis('Von'), ('V5',))
        self.assertEqual(sfinxbis('Bernadotte af Wisborg'), ('B6533', 'V8162'))
        self.assertEqual(sfinxbis('Hjort af Ornäs'), ('J63', '$658'))
        self.assertEqual(sfinxbis('Horn af Åminne'), ('H65', '$55'))
        self.assertEqual(sfinxbis('Horn av Åminne'), ('H65', '$55'))
        self.assertEqual(sfinxbis('Hård af Segerstad'), ('H63', 'S26833'))
        self.assertEqual(sfinxbis('Hård av Segerstad'), ('H63', 'S26833'))
        self.assertEqual(sfinxbis('Stael von Holstein'), ('S34', 'H48325'))
        self.assertEqual(sfinxbis('de Oliveira e Silva'), ('$4726', 'S47'))
        self.assertEqual(sfinxbis('de Alfaro y Gómez'), ('$476', 'G58'))
        self.assertEqual(sfinxbis('Arjaliès-de la Lande'), ('$6248', 'L53'))
        self.assertEqual(
            sfinxbis('Dominicus van den Bussche'), ('D5528', 'B8')
        )
        self.assertEqual(
            sfinxbis('Edebol Eeg-Olofsson'), ('$314', '$2', '$4785')
        )
        self.assertEqual(sfinxbis('Jonsson-Blomqvist'), ('J585', 'B452783'))
        self.assertEqual(sfinxbis('Kiviniemi Birgersson'), ('#755', 'B62685'))
        self.assertEqual(
            sfinxbis('Massena Serpa dos Santos'), ('M85', 'S61', 'S538')
        )
        self.assertEqual(sfinxbis('S:t Clair Renard'), ('K426', 'R563'))
        self.assertEqual(sfinxbis('Skoog H Andersson'), ('S22', 'H', '$53685'))
        self.assertEqual(sfinxbis('von Post-Skagegård'), ('P83', 'S22263'))
        self.assertEqual(sfinxbis('von Zur-Mühlen'), ('S6', 'M45'))
        self.assertEqual(sfinxbis('Waltå O:son'), ('V43', '$85'))
        self.assertEqual(
            sfinxbis('Zardán Gómez de la Torre'), ('S635', 'G58', 'T6')
        )
        self.assertEqual(sfinxbis('af Jochnick'), ('J252',))
        self.assertEqual(sfinxbis('af Ioscnick'), ('J8252',))
        self.assertEqual(sfinxbis('Aabakken'), ('$125',))
        self.assertEqual(sfinxbis('Åbacken'), ('$125',))
        self.assertEqual(sfinxbis('Ahlen'), ('$45',))
        self.assertEqual(sfinxbis('Aleen'), ('$45',))
        self.assertEqual(sfinxbis('Braunerhielm'), ('B656245',))
        self.assertEqual(sfinxbis('Branneerhielm'), ('B656245',))
        self.assertEqual(sfinxbis('Carlzon'), ('K6485',))
        self.assertEqual(sfinxbis('Karlsson'), ('K6485',))
        self.assertEqual(sfinxbis('Enochsson'), ('$5285',))
        self.assertEqual(sfinxbis('Ericsson'), ('$6285',))
        self.assertEqual(sfinxbis('Ericksson'), ('$6285',))
        self.assertEqual(sfinxbis('Erixson'), ('$6285',))
        self.assertEqual(sfinxbis('Filipsson'), ('F4185',))
        self.assertEqual(sfinxbis('Philipson'), ('F4185',))
        self.assertEqual(sfinxbis('Flycht'), ('F423',))
        self.assertEqual(sfinxbis('Flygt'), ('F423',))
        self.assertEqual(sfinxbis('Flykt'), ('F423',))
        self.assertEqual(sfinxbis('Fröijer'), ('F626',))
        self.assertEqual(sfinxbis('Fröjer'), ('F626',))
        self.assertEqual(sfinxbis('Gertner'), ('J6356',))
        self.assertEqual(sfinxbis('Hiertner'), ('J6356',))
        self.assertEqual(sfinxbis('Hirch'), ('H62',))
        self.assertEqual(sfinxbis('Hirsch'), ('H68',))
        self.assertEqual(sfinxbis('Haegermarck'), ('H26562',))
        self.assertEqual(sfinxbis('Hägermark'), ('H26562',))
        self.assertEqual(sfinxbis('Isaxon'), ('$8285',))
        self.assertEqual(sfinxbis('Isacsson'), ('$8285',))
        self.assertEqual(sfinxbis('Joachimsson'), ('J2585',))
        self.assertEqual(sfinxbis('Joakimson'), ('J2585',))
        self.assertEqual(sfinxbis('Kjell'), ('#4',))
        self.assertEqual(sfinxbis('Käll'), ('#4',))
        self.assertEqual(sfinxbis('Knapp'), ('K51',))
        self.assertEqual(sfinxbis('Krans'), ('K658',))
        self.assertEqual(sfinxbis('Krantz'), ('K6538',))
        self.assertEqual(sfinxbis('Kvist'), ('K783',))
        self.assertEqual(sfinxbis('Quist'), ('K783',))
        self.assertEqual(sfinxbis('Lidbeck'), ('L312',))
        self.assertEqual(sfinxbis('Lidbäck'), ('L312',))
        self.assertEqual(sfinxbis('Linnér'), ('L56',))
        self.assertEqual(sfinxbis('Linner'), ('L56',))
        self.assertEqual(sfinxbis('Lorenzsonn'), ('L6585',))
        self.assertEqual(sfinxbis('Lorentzon'), ('L65385',))
        self.assertEqual(sfinxbis('Lorenßon'), ('L6585',))
        self.assertEqual(sfinxbis('Lyxell'), ('L284',))
        self.assertEqual(sfinxbis('Lycksell'), ('L284',))
        self.assertEqual(sfinxbis('Marcström'), ('M628365',))
        self.assertEqual(sfinxbis('Markström'), ('M628365',))
        self.assertEqual(sfinxbis('Michaelsson'), ('M2485',))
        self.assertEqual(sfinxbis('Mikaelson'), ('M2485',))
        self.assertEqual(sfinxbis('Mörch'), ('M62',))
        self.assertEqual(sfinxbis('Mörck'), ('M62',))
        self.assertEqual(sfinxbis('Mörk'), ('M62',))
        self.assertEqual(sfinxbis('Mørk'), ('M62',))
        self.assertEqual(sfinxbis('Nääs'), ('N8',))
        self.assertEqual(sfinxbis('Naess'), ('N8',))
        self.assertEqual(sfinxbis('Nordstedt'), ('N63833',))
        self.assertEqual(sfinxbis('Oxenstierna'), ('$28583265',))
        self.assertEqual(sfinxbis('Palmçrañtz'), ('P4526538',))
        self.assertEqual(sfinxbis('Palmcrantz'), ('P4526538',))
        self.assertEqual(sfinxbis('Palmkrantz'), ('P4526538',))
        self.assertEqual(sfinxbis('Preuss'), ('P68',))
        self.assertEqual(sfinxbis('Preutz'), ('P638',))
        self.assertEqual(sfinxbis('Richardson'), ('R26385',))
        self.assertEqual(sfinxbis('Rikardson'), ('R26385',))
        self.assertEqual(sfinxbis('Ruuth'), ('R3',))
        self.assertEqual(sfinxbis('Ruth'), ('R3',))
        self.assertEqual(sfinxbis('Sæter'), ('S36',))
        self.assertEqual(sfinxbis('Zäter'), ('S36',))
        self.assertEqual(sfinxbis('Schedin'), ('#35',))
        self.assertEqual(sfinxbis('Sjödin'), ('#35',))
        self.assertEqual(sfinxbis('Siöö'), ('#',))
        self.assertEqual(sfinxbis('Sjöh'), ('#',))
        self.assertEqual(sfinxbis('Svedberg'), ('S73162',))
        self.assertEqual(sfinxbis('Zwedberg'), ('S73162',))
        self.assertEqual(sfinxbis('Tjäder'), ('#36',))
        self.assertEqual(sfinxbis('þornquist'), ('T652783',))
        self.assertEqual(sfinxbis('Thörnqvist'), ('T652783',))
        self.assertEqual(sfinxbis('Törnkvist'), ('T652783',))
        self.assertEqual(sfinxbis('Wichman'), ('V255',))
        self.assertEqual(sfinxbis('Wickman'), ('V255',))
        self.assertEqual(sfinxbis('Wictorin'), ('V2365',))
        self.assertEqual(sfinxbis('Wictorsson'), ('V23685',))
        self.assertEqual(sfinxbis('Viktorson'), ('V23685',))
        self.assertEqual(sfinxbis('Zachrisson'), ('S2685',))
        self.assertEqual(sfinxbis('Zakrison'), ('S2685',))
        self.assertEqual(sfinxbis('Övragård'), ('$76263',))
        self.assertEqual(sfinxbis('Öfvragårdh'), ('$76263',))
        self.assertEqual(sfinxbis('Bogdanovic'), ('B23572',))
        self.assertEqual(sfinxbis('Bogdanovitch'), ('B235732',))
        self.assertEqual(sfinxbis('Dieterich'), ('D362',))
        self.assertEqual(sfinxbis('Eichorn'), ('$265',))
        self.assertEqual(sfinxbis('Friedrich'), ('F6362',))
        self.assertEqual(sfinxbis('Grantcharova'), ('G653267',))
        self.assertEqual(sfinxbis('Ilichev'), ('$427',))
        self.assertEqual(sfinxbis('Ivankovic'), ('$75272',))
        self.assertEqual(sfinxbis('Ivangurich'), ('$75262',))
        self.assertEqual(sfinxbis('Kinch'), ('#52',))
        self.assertEqual(sfinxbis('Kirchmann'), ('#6255',))
        self.assertEqual(sfinxbis('Machado'), ('M23',))
        self.assertEqual(sfinxbis('Reich'), ('R2',))
        self.assertEqual(sfinxbis('Roche'), ('R2',))
        self.assertEqual(sfinxbis('Rubaszkin'), ('R1825',))
        self.assertEqual(sfinxbis('Rubaschkin'), ('R1825',))
        self.assertEqual(sfinxbis('Sanchez'), ('S528',))
        self.assertEqual(sfinxbis('Walukiewicz'), ('V42728',))
        self.assertEqual(sfinxbis('Valukievitch'), ('V42732',))
        self.assertEqual(sfinxbis('K'), ('K',))
        self.assertEqual(sfinxbis('2010'), ('',))
        self.assertEqual(sfinxbis('cese'), ('S8',))

        # a few max_length tests
        self.assertEqual(sfinxbis('Kiviniemi Birgersson', 3), ('#75', 'B62'))
        self.assertEqual(sfinxbis('Eichorn', 4), ('$265',))
        self.assertEqual(sfinxbis('Friedrich', 4), ('F636',))
        self.assertEqual(sfinxbis('Grantcharova', 4), ('G653',))
        self.assertEqual(sfinxbis('Ilichev', 4), ('$427',))
        self.assertEqual(sfinxbis('Ivankovic', 4), ('$752',))
        self.assertEqual(sfinxbis('Ivangurich', 4), ('$752',))
        self.assertEqual(sfinxbis('Kinch', 4), ('#52',))
        self.assertEqual(sfinxbis('Kirchmann', 4), ('#625',))
        self.assertEqual(sfinxbis('Machado', 4), ('M23',))
        self.assertEqual(sfinxbis('Reich', 4), ('R2',))
        self.assertEqual(sfinxbis('Roche', 4), ('R2',))
        self.assertEqual(sfinxbis('Rubaszkin', 4), ('R182',))
        self.assertEqual(sfinxbis('Rubaschkin', 4), ('R182',))
        self.assertEqual(sfinxbis('Sanchez', 4), ('S528',))
        self.assertEqual(sfinxbis('Walukiewicz', 4), ('V427',))
        self.assertEqual(sfinxbis('Valukievitch', 4), ('V427',))
        self.assertEqual(sfinxbis('K', 4), ('K',))
        self.assertEqual(sfinxbis('2010', 4), ('',))
        self.assertEqual(sfinxbis('cese', 4), ('S8',))

        # etc. (for code coverage)
        self.assertEqual(sfinxbis('chans'), ('#58',))
        self.assertEqual(sfinxbis('ljud'), ('J3',))
        self.assertEqual(sfinxbis('qi'), ('K',))
        self.assertEqual(sfinxbis('xavier'), ('S76',))
        self.assertEqual(sfinxbis('skjul'), ('#4',))
        self.assertEqual(sfinxbis('schul'), ('#4',))
        self.assertEqual(sfinxbis('skil'), ('#4',))

        # max_length bounds tests
        self.assertEqual(sfinxbis('Niall', max_length=-1), ('N4',))
        self.assertEqual(sfinxbis('Niall', max_length=0), ('N4',))


class NorphoneTestCases(unittest.TestCase):
    """Test Norphone functions.

    test cases for abydos.phonetic.norphone
    """

    def test_norphone(self):
        """Test abydos.phonetic.norphone."""
        # Base case
        self.assertEqual(norphone(''), '')

        # Examples given at
        # https://github.com/larsga/Duke/blob/master/duke-core/src/test/java/no/priv/garshol/duke/comparators/NorphoneComparatorTest.java
        self.assertEqual(norphone('Aarestad'), norphone('\u00C5rrestad'))
        self.assertEqual(norphone('Andreasen'), norphone('Andreassen'))
        self.assertEqual(norphone('Arntsen'), norphone('Arntzen'))
        self.assertEqual(norphone('Bache'), norphone('Bakke'))
        self.assertEqual(norphone('Frank'), norphone('Franck'))
        self.assertEqual(norphone('Christian'), norphone('Kristian'))
        self.assertEqual(norphone('Kielland'), norphone('Kjelland'))
        self.assertEqual(norphone('Krogh'), norphone('Krog'))
        self.assertEqual(norphone('Krog'), norphone('Krohg'))
        self.assertEqual(norphone('Jendal'), norphone('Jendahl'))
        self.assertEqual(norphone('Jendal'), norphone('Hjendal'))
        self.assertEqual(norphone('Jendal'), norphone('Gjendal'))
        self.assertEqual(norphone('Vold'), norphone('Wold'))
        self.assertEqual(norphone('Thomas'), norphone('Tomas'))
        self.assertEqual(norphone('Aamodt'), norphone('Aamot'))
        self.assertEqual(norphone('Aksel'), norphone('Axel'))
        self.assertEqual(norphone('Kristoffersen'), norphone('Christophersen'))
        self.assertEqual(norphone('Voll'), norphone('Vold'))
        self.assertEqual(norphone('Granli'), norphone('Granlid'))
        self.assertEqual(norphone('Gjever'), norphone('Giever'))
        self.assertEqual(norphone('Sannerhaugen'), norphone('Sanderhaugen'))
        self.assertEqual(norphone('Jahren'), norphone('Jaren'))
        self.assertEqual(norphone('Amundsrud'), norphone('Amundsr\u00F8d'))
        self.assertEqual(norphone('Karlson'), norphone('Carlson'))

        # Additional tests to increase coverage
        self.assertEqual(norphone('Århus'), 'ÅRHS')
        self.assertEqual(norphone('Skyrim'), 'XRM')
        self.assertEqual(norphone('kyss'), 'XS')
        self.assertEqual(norphone('Äthelwulf'), 'ÆTLVLF')
        self.assertEqual(norphone('eit'), 'ÆT')
        self.assertEqual(norphone('Öl'), 'ØL')

        # test cases by larsga (the algorithm's author) posted to Reddit
        # https://www.reddit.com/r/norge/comments/vksb5/norphone_mitt_forslag_til_en_norsk_soundex_vel/
        # modified, where necessary to match the "not implemented" rules
        # and rule added after the Reddit post
        reddit_tests = (
            (
                'MKLSN',
                (
                    'MICHALSEN',
                    'MIKKELSEN',
                    'MIKALSEN',
                    'MICHAELSEN',
                    'MIKAELSEN',
                    'MICKAELSEN',
                    'MICHELSEN',
                    'MIKELSEN',
                ),
            ),
            (
                'BRKR',
                (
                    'BERGER',
                    'BORGERUD',
                    'BURGER',
                    'BORGER',
                    'BORGAR',
                    'BIRGER',
                    'BRAGER',
                    'BERGERUD',
                ),
            ),
            (
                'TMS',
                (
                    'TOMMAS',
                    'THOMAS',
                    'THAMS',
                    'TOUMAS',
                    'THOMMAS',
                    'TIMMS',
                    'TOMAS',
                    'TUOMAS',
                ),
            ),
            (
                'HLR',
                (
                    'HOLER',
                    'HELLERUD',
                    'HALLRE',
                    'HOLLERUD',
                    'HILLER',
                    'HALLERUD',
                    'HOLLER',
                    'HALLER',
                ),
            ),
            (
                'MS',
                (
                    'MASS',
                    'MMS',
                    'MSS',
                    'MOES',
                    'MEZZO',
                    'MESA',
                    'MESSE',
                    'MOSS',
                ),
            ),
            (
                'HRST',
                (
                    'HIRSTI',
                    'HAARSETH',
                    'HAARSTAD',
                    'HARSTAD',
                    'HARESTUA',
                    'HERSETH',
                    'HERSTAD',
                    'HERSTUA',
                ),
            ),
            (
                'SVN',
                (
                    'SWANN',
                    'SVENI',
                    'SWAN',
                    'SVEN',
                    'SVEIN',
                    'SVEEN',
                    'SVENN',
                    'SVANE',
                ),
            ),
            (
                'SLT',
                (
                    'SELTE',
                    'SALT',
                    'SALTE',
                    'SLOTT',
                    'SLAATTO',
                    'SLETT',
                    'SLETTA',
                    'SLETTE',
                ),
            ),
            (
                'JNSN',
                (
                    'JANSSEN',
                    'JANSEN',
                    'JENSEN',
                    'JONASSEN',
                    'JANSON',
                    'JONSON',
                    'JENSSEN',
                    'JONSSON',
                ),
            ),
            (
                'ANRSN',
                (
                    'ANDRESSEN',
                    'ANDERSSON',
                    'ANDRESEN',
                    'ANDREASSEN',
                    'ANDERSEN',
                    'ANDERSON',
                    'ANDORSEN',
                    'ANDERSSEN',
                ),
            ),
            (
                'BRK',
                (
                    'BREKKE',
                    'BORCH',
                    'BRAKKE',
                    'BORK',
                    'BRECKE',
                    'BROCH',
                    'BRICK',
                    'BRUK',
                ),
            ),
            (
                'LN',
                (
                    'LINDE',
                    'LENDE',
                    'LUND',
                    'LAND',
                    'LINDA',
                    'LANDE',
                    'LIND',
                    'LUNDE',
                ),
            ),
            (
                'SF',
                (
                    'SOPHIE',
                    'SFE',
                    'SEFF',
                    'SEAFOOD',
                    'SOFIE',
                    'SAFE',
                    'SOFI',
                    'SOPHIA',
                ),
            ),
            (
                'BRST',
                (
                    'BRUASET',
                    'BUERSTAD',
                    'BARSTAD',
                    'BAARSTAD',
                    'BRUSETH',
                    'BERSTAD',
                    'BORSTAD',
                    'BRUSTAD',
                ),
            ),
            (
                'OLSN',
                (
                    'OHLSSON',
                    'OLESEN',
                    'OLSSON',
                    'OLAUSSON',
                    'OLAUSEN',
                    'OLAUSSEN',
                    'OLSEN',
                    'OLSON',
                ),
            ),
            (
                'MKL',
                (
                    'MIKAEL',
                    'MICHELA',
                    'MEIKLE',
                    'MIKAL',
                    'MIKKEL',
                    'MICHEL',
                    'MICHAL',
                    'MICHAEL',
                ),
            ),
            (
                'HR',
                (
                    'HEIER',
                    'HAR',
                    'HEER',
                    'HARRY',
                    'HEIR',
                    'HURRE',
                    'HERO',
                    'HUURRE',
                ),
            ),
            (
                'VLM',
                (
                    'VILLUM',
                    'WOLLUM',
                    'WILLIAM',
                    'WILLAM',
                    'WALLEM',
                    'WILLUM',
                    'VALUM',
                    'WILMO',
                ),
            ),
            (
                'SNS',
                (
                    'SYNNES',
                    'SINUS',
                    'SNUS',
                    'SNEIS',
                    'SANNES',
                    'SUNAAS',
                    'SUNNAAS',
                    'SAINES',
                ),
            ),
            (
                'SNL',
                (
                    'SANDAL',
                    'SANDAHL',
                    'SUNDEL',
                    'SANDLI',
                    'SUNNDAL',
                    'SANDELL',
                    'SANDLIE',
                    'SUNDAL',
                ),
            ),
            (
                'VK',
                ('VEKA', 'VIKA', 'WIIK', 'WOK', 'WIKE', 'WEEK', 'VIK', 'VIAK'),
            ),
            (
                'MTS',
                (
                    'METSO',
                    'MOTHES',
                    'MATHIAS',
                    'MATHIS',
                    'MATTIS',
                    'MYTHES',
                    'METOS',
                    'MATS',
                ),
            ),
        )
        for encoded, names in reddit_tests:
            for name in names:
                self.assertEqual(encoded, norphone(name))


if __name__ == '__main__':
    unittest.main()
