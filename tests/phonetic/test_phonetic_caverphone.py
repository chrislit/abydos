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

"""abydos.tests.phonetic.test_phonetic_caverphone.

This module contains unit tests for abydos.phonetic.Caverphone
"""

import unittest

from abydos.phonetic import Caverphone, Metaphone, Soundex

from .. import _corpus_file


class CaverphoneTestCases(unittest.TestCase):
    """Test Caverphone functions.

    test cases for abydos.phonetic.Caverphone
    """

    pa = Caverphone()
    pa_1 = Caverphone(version=1)
    pa_2 = Caverphone(version=2)

    def test_caverphone2_encode(self):
        """Test abydos.phonetic.Caverphone (Caverphone 2)."""
        self.assertEqual(self.pa.encode(''), '1111111111')
        self.assertEqual(self.pa_2.encode(''), '1111111111')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(self.pa.encode('Henrichsen'), 'ANRKSN1111')
        self.assertEqual(self.pa.encode('Henricsson'), 'ANRKSN1111')
        self.assertEqual(self.pa.encode('Henriksson'), 'ANRKSN1111')
        self.assertEqual(self.pa.encode('Hinrichsen'), 'ANRKSN1111')
        self.assertEqual(self.pa.encode('Izchaki'), 'ASKKA11111')
        self.assertEqual(self.pa.encode('Maclaverty'), 'MKLFTA1111')
        self.assertEqual(self.pa.encode('Mccleverty'), 'MKLFTA1111')
        self.assertEqual(self.pa.encode('Mcclifferty'), 'MKLFTA1111')
        self.assertEqual(self.pa.encode('Mclafferty'), 'MKLFTA1111')
        self.assertEqual(self.pa.encode('Mclaverty'), 'MKLFTA1111')
        self.assertEqual(self.pa.encode('Slocomb'), 'SLKM111111')
        self.assertEqual(self.pa.encode('Slocombe'), 'SLKM111111')
        self.assertEqual(self.pa.encode('Slocumb'), 'SLKM111111')
        self.assertEqual(self.pa.encode('Whitlam'), 'WTLM111111')

        # http://caversham.otago.ac.nz/files/working/ctp150804.pdf
        self.assertEqual(self.pa.encode('Stevenson'), 'STFNSN1111')
        self.assertEqual(self.pa.encode('Peter'), 'PTA1111111')
        for word in (
            'Darda',
            'Datha',
            'Dedie',
            'Deedee',
            'Deerdre',
            'Deidre',
            'Deirdre',
            'Detta',
            'Didi',
            'Didier',
            'Dido',
            'Dierdre',
            'Dieter',
            'Dita',
            'Ditter',
            'Dodi',
            'Dodie',
            'Dody',
            'Doherty',
            'Dorthea',
            'Dorthy',
            'Doti',
            'Dotti',
            'Dottie',
            'Dotty',
            'Doty',
            'Doughty',
            'Douty',
            'Dowdell',
            'Duthie',
            'Tada',
            'Taddeo',
            'Tadeo',
            'Tadio',
            'Tati',
            'Teador',
            'Tedda',
            'Tedder',
            'Teddi',
            'Teddie',
            'Teddy',
            'Tedi',
            'Tedie',
            'Teeter',
            'Teodoor',
            'Teodor',
            'Terti',
            'Theda',
            'Theodor',
            'Theodore',
            'Theta',
            'Thilda',
            'Thordia',
            'Tilda',
            'Tildi',
            'Tildie',
            'Tildy',
            'Tita',
            'Tito',
            'Tjader',
            'Toddie',
            'Toddy',
            'Torto',
            'Tuddor',
            'Tudor',
            'Turtle',
            'Tuttle',
            'Tutto',
        ):
            self.assertEqual(self.pa.encode(word), 'TTA1111111')
            self.assertEqual(self.pa_2.encode(word), 'TTA1111111')
        for word in (
            'Cailean',
            'Calan',
            'Calen',
            'Callahan',
            'Callan',
            'Callean',
            'Carleen',
            'Carlen',
            'Carlene',
            'Carlin',
            'Carline',
            'Carlyn',
            'Carlynn',
            'Carlynne',
            'Charlean',
            'Charleen',
            'Charlene',
            'Charline',
            'Cherlyn',
            'Chirlin',
            'Clein',
            'Cleon',
            'Cline',
            'Cohleen',
            'Colan',
            'Coleen',
            'Colene',
            'Colin',
            'Colleen',
            'Collen',
            'Collin',
            'Colline',
            'Colon',
            'Cullan',
            'Cullen',
            'Cullin',
            'Gaelan',
            'Galan',
            'Galen',
            'Garlan',
            'Garlen',
            'Gaulin',
            'Gayleen',
            'Gaylene',
            'Giliane',
            'Gillan',
            'Gillian',
            'Glen',
            'Glenn',
            'Glyn',
            'Glynn',
            'Gollin',
            'Gorlin',
            'Kalin',
            'Karlan',
            'Karleen',
            'Karlen',
            'Karlene',
            'Karlin',
            'Karlyn',
            'Kaylyn',
            'Keelin',
            'Kellen',
            'Kellene',
            'Kellyann',
            'Kellyn',
            'Khalin',
            'Kilan',
            'Kilian',
            'Killen',
            'Killian',
            'Killion',
            'Klein',
            'Kleon',
            'Kline',
            'Koerlin',
            'Kylen',
            'Kylynn',
            'Quillan',
            'Quillon',
            'Qulllon',
            'Xylon',
        ):
            self.assertEqual(self.pa.encode(word), 'KLN1111111')
            self.assertEqual(self.pa_2.encode(word), 'KLN1111111')
        for word in (
            'Dan',
            'Dane',
            'Dann',
            'Darn',
            'Daune',
            'Dawn',
            'Ddene',
            'Dean',
            'Deane',
            'Deanne',
            'DeeAnn',
            'Deeann',
            'Deeanne',
            'Deeyn',
            'Den',
            'Dene',
            'Denn',
            'Deonne',
            'Diahann',
            'Dian',
            'Diane',
            'Diann',
            'Dianne',
            'Diannne',
            'Dine',
            'Dion',
            'Dione',
            'Dionne',
            'Doane',
            'Doehne',
            'Don',
            'Donn',
            'Doone',
            'Dorn',
            'Down',
            'Downe',
            'Duane',
            'Dun',
            'Dunn',
            'Duyne',
            'Dyan',
            'Dyane',
            'Dyann',
            'Dyanne',
            'Dyun',
            'Tan',
            'Tann',
            'Teahan',
            'Ten',
            'Tenn',
            'Terhune',
            'Thain',
            'Thaine',
            'Thane',
            'Thanh',
            'Thayne',
            'Theone',
            'Thin',
            'Thorn',
            'Thorne',
            'Thun',
            'Thynne',
            'Tien',
            'Tine',
            'Tjon',
            'Town',
            'Towne',
            'Turne',
            'Tyne',
        ):
            self.assertEqual(self.pa.encode(word), 'TN11111111')
            self.assertEqual(self.pa_2.encode(word), 'TN11111111')

        # etc. (for code coverage)
        self.assertEqual(self.pa.encode('enough'), 'ANF1111111')
        self.assertEqual(self.pa.encode('trough'), 'TRF1111111')
        self.assertEqual(self.pa.encode('gnu'), 'NA11111111')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Henrichsen'), 'ANRKSN')
        self.assertEqual(self.pa.encode_alpha('Dierdre'), 'TTA')
        self.assertEqual(self.pa.encode_alpha('Mcclifferty'), 'MKLFTA')
        self.assertEqual(self.pa.encode_alpha('Killen'), 'KLN')
        self.assertEqual(self.pa.encode_alpha('Whittle'), 'WTA')

    def test_caverphone2_encode_php_testset(self):
        """Test abydos.phonetic.Caverphone (PHP version testset)."""
        # https://raw.githubusercontent.com/kiphughes/caverphone/master/unit_tests.php
        with open(_corpus_file('php_caverphone.csv')) as php_testset:
            for php_line in php_testset:
                (word, caver) = php_line.strip().split(',')
                self.assertEqual(self.pa.encode(word), caver)

    def test_caverphone1_encode(self):
        """Test abydos.phonetic.Caverphone (Caverphone 1)."""
        self.assertEqual(self.pa_1.encode(''), '111111')

        # http://caversham.otago.ac.nz/files/working/ctp060902.pdf
        self.assertEqual(self.pa_1.encode('David'), 'TFT111')
        self.assertEqual(self.pa_1.encode('Whittle'), 'WTL111')

    def test_caversham(self):
        """Test using Caversham test set (SoundEx, Metaphone, & Caverphone)."""
        soundex = Soundex()
        metaphone = Metaphone()

        with open(_corpus_file('variantNames.csv')) as cav_testset:
            next(cav_testset)
            for cav_line in cav_testset:
                (
                    name1,
                    soundex1,
                    metaphone1,
                    caverphone1,
                    name2,
                    soundex2,
                    metaphone2,
                    caverphone2,
                    soundex_same,
                    metaphone_same,
                    caverphone_same,
                ) = cav_line.strip().split(',')

                self.assertEqual(soundex.encode(name1), soundex1)
                self.assertEqual(soundex.encode(name2), soundex2)
                if soundex_same == '1':
                    self.assertEqual(
                        soundex.encode(name1), soundex.encode(name2)
                    )
                else:
                    self.assertNotEqual(
                        soundex.encode(name1), soundex.encode(name2)
                    )

                self.assertEqual(metaphone.encode(name1), metaphone1)
                self.assertEqual(metaphone.encode(name2), metaphone2)
                if metaphone_same == '1':
                    self.assertEqual(
                        metaphone.encode(name1), metaphone.encode(name2)
                    )
                else:
                    self.assertNotEqual(
                        metaphone.encode(name1), metaphone.encode(name2)
                    )

                self.assertEqual(self.pa.encode(name1), caverphone1)
                self.assertEqual(self.pa.encode(name2), caverphone2)
                if caverphone_same == '1':
                    self.assertEqual(
                        self.pa.encode(name1), self.pa.encode(name2)
                    )
                else:
                    self.assertNotEqual(
                        self.pa.encode(name1), self.pa.encode(name2)
                    )


if __name__ == '__main__':
    unittest.main()
