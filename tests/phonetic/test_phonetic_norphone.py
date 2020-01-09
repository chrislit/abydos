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

"""abydos.tests.phonetic.test_phonetic_norphone.

This module contains unit tests for abydos.phonetic.Norphone
"""

import unittest

from abydos.phonetic import Norphone, norphone


class NorphoneTestCases(unittest.TestCase):
    """Test Norphone functions.

    test cases for abydos.phonetic.Norphone
    """

    pa = Norphone()

    def test_norphone(self):
        """Test abydos.phonetic.Norphone."""
        # Base case
        self.assertEqual(self.pa.encode(''), '')

        # Examples given at
        # https://github.com/larsga/Duke/blob/master/duke-core/src/test/java/no/priv/garshol/duke/comparators/NorphoneComparatorTest.java
        self.assertEqual(
            self.pa.encode('Aarestad'), self.pa.encode('\u00C5rrestad')
        )
        self.assertEqual(
            self.pa.encode('Andreasen'), self.pa.encode('Andreassen')
        )
        self.assertEqual(self.pa.encode('Arntsen'), self.pa.encode('Arntzen'))
        self.assertEqual(self.pa.encode('Bache'), self.pa.encode('Bakke'))
        self.assertEqual(self.pa.encode('Frank'), self.pa.encode('Franck'))
        self.assertEqual(
            self.pa.encode('Christian'), self.pa.encode('Kristian')
        )
        self.assertEqual(
            self.pa.encode('Kielland'), self.pa.encode('Kjelland')
        )
        self.assertEqual(self.pa.encode('Krogh'), self.pa.encode('Krog'))
        self.assertEqual(self.pa.encode('Krog'), self.pa.encode('Krohg'))
        self.assertEqual(self.pa.encode('Jendal'), self.pa.encode('Jendahl'))
        self.assertEqual(self.pa.encode('Jendal'), self.pa.encode('Hjendal'))
        self.assertEqual(self.pa.encode('Jendal'), self.pa.encode('Gjendal'))
        self.assertEqual(self.pa.encode('Vold'), self.pa.encode('Wold'))
        self.assertEqual(self.pa.encode('Thomas'), self.pa.encode('Tomas'))
        self.assertEqual(self.pa.encode('Aamodt'), self.pa.encode('Aamot'))
        self.assertEqual(self.pa.encode('Aksel'), self.pa.encode('Axel'))
        self.assertEqual(
            self.pa.encode('Kristoffersen'), self.pa.encode('Christophersen')
        )
        self.assertEqual(self.pa.encode('Voll'), self.pa.encode('Vold'))
        self.assertEqual(self.pa.encode('Granli'), self.pa.encode('Granlid'))
        self.assertEqual(self.pa.encode('Gjever'), self.pa.encode('Giever'))
        self.assertEqual(
            self.pa.encode('Sannerhaugen'), self.pa.encode('Sanderhaugen')
        )
        self.assertEqual(self.pa.encode('Jahren'), self.pa.encode('Jaren'))
        self.assertEqual(
            self.pa.encode('Amundsrud'), self.pa.encode('Amundsr\u00F8d')
        )
        self.assertEqual(self.pa.encode('Karlson'), self.pa.encode('Carlson'))

        # Additional tests to increase coverage
        self.assertEqual(self.pa.encode('Århus'), 'ÅRHS')
        self.assertEqual(self.pa.encode('Skyrim'), 'XRM')
        self.assertEqual(self.pa.encode('kyss'), 'XS')
        self.assertEqual(self.pa.encode('Äthelwulf'), 'ÆTLVLF')
        self.assertEqual(self.pa.encode('eit'), 'ÆT')
        self.assertEqual(self.pa.encode('Öl'), 'ØL')

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
                self.assertEqual(encoded, self.pa.encode(name))

        # Test wrapper
        self.assertEqual(norphone('Århus'), 'ÅRHS')


if __name__ == '__main__':
    unittest.main()
