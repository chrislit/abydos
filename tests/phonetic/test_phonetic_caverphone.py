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

"""abydos.tests.phonetic.test_phonetic_caverphone.

This module contains unit tests for abydos.phonetic._caverphone
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import caverphone, metaphone, soundex

from .. import _corpus_file


class CaverphoneTestCases(unittest.TestCase):
    """Test Caverphone functions.

    test cases for abydos.phonetic._caverphone.caverphone
    """

    def test_caverphone2(self):
        """Test abydos.phonetic._caverphone.caverphone (Caverphone 2)."""
        self.assertEqual(caverphone(''), '1111111111')
        self.assertEqual(caverphone('', 2), '1111111111')
        self.assertEqual(caverphone('', version=2), '1111111111')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(caverphone('Henrichsen'), 'ANRKSN1111')
        self.assertEqual(caverphone('Henricsson'), 'ANRKSN1111')
        self.assertEqual(caverphone('Henriksson'), 'ANRKSN1111')
        self.assertEqual(caverphone('Hinrichsen'), 'ANRKSN1111')
        self.assertEqual(caverphone('Izchaki'), 'ASKKA11111')
        self.assertEqual(caverphone('Maclaverty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Mccleverty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Mcclifferty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Mclafferty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Mclaverty'), 'MKLFTA1111')
        self.assertEqual(caverphone('Slocomb'), 'SLKM111111')
        self.assertEqual(caverphone('Slocombe'), 'SLKM111111')
        self.assertEqual(caverphone('Slocumb'), 'SLKM111111')
        self.assertEqual(caverphone('Whitlam'), 'WTLM111111')

        # http://caversham.otago.ac.nz/files/working/ctp150804.pdf
        self.assertEqual(caverphone('Stevenson'), 'STFNSN1111')
        self.assertEqual(caverphone('Peter'), 'PTA1111111')
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
            self.assertEqual(caverphone(word), 'TTA1111111')
            self.assertEqual(caverphone(word, 2), 'TTA1111111')
            self.assertEqual(caverphone(word, version=2), 'TTA1111111')
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
            self.assertEqual(caverphone(word), 'KLN1111111')
            self.assertEqual(caverphone(word, 2), 'KLN1111111')
            self.assertEqual(caverphone(word, version=2), 'KLN1111111')
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
            self.assertEqual(caverphone(word), 'TN11111111')
            self.assertEqual(caverphone(word, 2), 'TN11111111')
            self.assertEqual(caverphone(word, version=2), 'TN11111111')

        # etc. (for code coverage)
        self.assertEqual(caverphone('enough'), 'ANF1111111')
        self.assertEqual(caverphone('trough'), 'TRF1111111')
        self.assertEqual(caverphone('gnu'), 'NA11111111')

    def test_caverphone2_php_testset(self):
        """Test abydos.phonetic._caverphone.caverphone (PHP version testset)."""  # noqa: E501
        # https://raw.githubusercontent.com/kiphughes/caverphone/master/unit_tests.php
        with open(_corpus_file('php_caverphone.csv')) as php_testset:
            for php_line in php_testset:
                (word, caver) = php_line.strip().split(',')
                self.assertEqual(caverphone(word), caver)

    def test_caverphone1(self):
        """Test abydos.phonetic._caverphone.caverphone (Caverphone 1)."""
        self.assertEqual(caverphone('', 1), '111111')
        self.assertEqual(caverphone('', version=1), '111111')

        # http://caversham.otago.ac.nz/files/working/ctp060902.pdf
        self.assertEqual(caverphone('David', version=1), 'TFT111')
        self.assertEqual(caverphone('Whittle', version=1), 'WTL111')

    def test_caversham(self):
        """Test using Caversham test set (SoundEx, Metaphone, & Caverphone)."""
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

                self.assertEqual(soundex(name1), soundex1)
                self.assertEqual(soundex(name2), soundex2)
                if soundex_same == '1':
                    self.assertEqual(soundex(name1), soundex(name2))
                else:
                    self.assertNotEqual(soundex(name1), soundex(name2))

                self.assertEqual(metaphone(name1), metaphone1)
                self.assertEqual(metaphone(name2), metaphone2)
                if metaphone_same == '1':
                    self.assertEqual(metaphone(name1), metaphone(name2))
                else:
                    self.assertNotEqual(metaphone(name1), metaphone(name2))

                self.assertEqual(caverphone(name1), caverphone1)
                self.assertEqual(caverphone(name2), caverphone2)
                if caverphone_same == '1':
                    self.assertEqual(caverphone(name1), caverphone(name2))
                else:
                    self.assertNotEqual(caverphone(name1), caverphone(name2))


if __name__ == '__main__':
    unittest.main()
