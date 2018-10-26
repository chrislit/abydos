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

"""abydos.tests.phonetic.test_phonetic_es.

This module contains unit tests for abydos.phonetic.es
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.es import phonetic_spanish, spanish_metaphone


class PhoneticSpanishTestCases(unittest.TestCase):
    """Test PhoneticSpanish functions.

    test cases for abydos.phonetic.es.phonetic_spanish
    """

    def test_phonetic_spanish(self):
        """Test abydos.phonetic.es.phonetic_spanish."""
        # Base case
        self.assertEqual(phonetic_spanish(''), '')

        # Examples given in
        self.assertEqual(phonetic_spanish('Giraldo'), '8953')
        self.assertEqual(phonetic_spanish('Jiraldo'), '8953')
        self.assertEqual(phonetic_spanish('Halla'), '25')
        self.assertEqual(phonetic_spanish('Haya'), '25')
        self.assertEqual(phonetic_spanish('Cielo'), '45')
        self.assertEqual(phonetic_spanish('Sielo'), '45')

        # Test to maximize coverage
        self.assertEqual(phonetic_spanish('Giraldo', max_length=2), '89')


class SpanishMetaphoneTestCases(unittest.TestCase):
    """Test Spanish Metaphone functions.

    test cases for abydos.phonetic.es.spanish_metaphone
    """

    def test_spanish_metaphone(self):
        """Test abydos.phonetic.es.spanish_metaphone."""
        # Base case
        self.assertEqual(spanish_metaphone(''), '')

        # Examples given in
        # https://github.com/amsqr/Spanish-Metaphone/blob/master/phonetic_algorithms_es.py
        self.assertEqual(spanish_metaphone('X'), 'X')
        self.assertEqual(spanish_metaphone('xplosion'), 'EXPLSN')
        self.assertEqual(spanish_metaphone('escalera'), 'ESKLR')
        self.assertEqual(spanish_metaphone('scalera'), 'ESKLR')
        self.assertEqual(spanish_metaphone('mi'), 'M')
        self.assertEqual(spanish_metaphone('tu'), 'T')
        self.assertEqual(spanish_metaphone('su'), 'S')
        self.assertEqual(spanish_metaphone('te'), 'T')
        self.assertEqual(spanish_metaphone('ochooomiiiillllllll'), 'OXMYY')
        self.assertEqual(spanish_metaphone('complicado'), 'KMPLKD')
        self.assertEqual(spanish_metaphone('ácaro'), 'AKR')
        self.assertEqual(spanish_metaphone('ácido'), 'AZD')
        self.assertEqual(spanish_metaphone('clown'), 'KLUN')
        self.assertEqual(spanish_metaphone('down'), 'DUN')
        self.assertEqual(spanish_metaphone('col'), 'KL')
        self.assertEqual(spanish_metaphone('clon'), 'KLN')
        self.assertEqual(spanish_metaphone('waterpolo'), 'UTRPL')
        self.assertEqual(spanish_metaphone('aquino'), 'AKN')
        self.assertEqual(spanish_metaphone('rebosar'), 'RVSR')
        self.assertEqual(spanish_metaphone('rebozar'), 'RVZR')
        self.assertEqual(spanish_metaphone('grajea'), 'GRJ')
        self.assertEqual(spanish_metaphone('gragea'), 'GRJ')
        self.assertEqual(spanish_metaphone('encima'), 'ENZM')
        self.assertEqual(spanish_metaphone('enzima'), 'ENZM')
        self.assertEqual(spanish_metaphone('alhamar'), 'ALAMR')
        self.assertEqual(spanish_metaphone('abollar'), 'AVYR')
        self.assertEqual(spanish_metaphone('aboyar'), 'AVYR')
        self.assertEqual(spanish_metaphone('huevo'), 'UV')
        self.assertEqual(spanish_metaphone('webo'), 'UV')
        self.assertEqual(spanish_metaphone('macho'), 'MX')
        self.assertEqual(spanish_metaphone('xocolate'), 'XKLT')
        self.assertEqual(spanish_metaphone('chocolate'), 'XKLT')
        self.assertEqual(spanish_metaphone('axioma'), 'AXM')
        self.assertEqual(spanish_metaphone('abedul'), 'AVDL')
        self.assertEqual(spanish_metaphone('a'), 'A')
        self.assertEqual(spanish_metaphone('gengibre'), 'JNJVR')
        self.assertEqual(spanish_metaphone('yema'), 'YM')
        self.assertEqual(spanish_metaphone('wHISKY'), 'UISKY')
        self.assertEqual(spanish_metaphone('google'), 'GGL')
        self.assertEqual(spanish_metaphone('xilófono'), 'XLFN')
        self.assertEqual(spanish_metaphone('web'), 'UV')
        self.assertEqual(spanish_metaphone('guerra'), 'GRR')
        self.assertEqual(spanish_metaphone('pingüino'), 'PNUN')
        self.assertEqual(spanish_metaphone('si'), 'S')
        self.assertEqual(spanish_metaphone('ke'), 'K')
        self.assertEqual(spanish_metaphone('que'), 'K')
        self.assertEqual(spanish_metaphone('tu'), 'T')
        self.assertEqual(spanish_metaphone('gato'), 'GT')
        self.assertEqual(spanish_metaphone('gitano'), 'JTN')
        self.assertEqual(spanish_metaphone('queso'), 'KS')
        self.assertEqual(spanish_metaphone('paquete'), 'PKT')
        self.assertEqual(spanish_metaphone('cuco'), 'KK')
        self.assertEqual(spanish_metaphone('perro'), 'PRR')
        self.assertEqual(spanish_metaphone('pero'), 'PR')
        self.assertEqual(spanish_metaphone('arrebato'), 'ARRVT')
        self.assertEqual(spanish_metaphone('hola'), 'OL')
        self.assertEqual(spanish_metaphone('zapato'), 'ZPT')
        self.assertEqual(spanish_metaphone('españa'), 'ESPNY')
        self.assertEqual(spanish_metaphone('garrulo'), 'GRRL')
        self.assertEqual(spanish_metaphone('expansión'), 'EXPNSN')
        self.assertEqual(spanish_metaphone('membrillo'), 'MMVRY')
        self.assertEqual(spanish_metaphone('jamón'), 'JMN')
        self.assertEqual(spanish_metaphone('risa'), 'RS')
        self.assertEqual(spanish_metaphone('caricia'), 'KRZ')
        self.assertEqual(spanish_metaphone('llaves'), 'YVS')
        self.assertEqual(spanish_metaphone('paella'), 'PY')
        self.assertEqual(spanish_metaphone('cerilla'), 'ZRY')

        # tests from file:///home/chrislit/Downloads/ICTRS_2016_12.pdf
        # including of the modified version of the algorithm
        self.assertEqual(spanish_metaphone('Caricia'), 'KRZ')
        self.assertEqual(spanish_metaphone('Caricia', modified=True), 'KRZ')
        self.assertEqual(spanish_metaphone('Llaves'), 'YVS')
        self.assertEqual(spanish_metaphone('Llaves', modified=True), 'YVZ')
        self.assertEqual(spanish_metaphone('Paella'), 'PY')
        self.assertEqual(spanish_metaphone('Paella', modified=True), 'PY')
        self.assertEqual(spanish_metaphone('Cerilla'), 'ZRY')
        self.assertEqual(spanish_metaphone('Cerilla', modified=True), 'ZRY')
        self.assertEqual(spanish_metaphone('Empeorar'), 'EMPRR')
        self.assertEqual(spanish_metaphone('Empeorar', modified=True), 'ENPRR')
        self.assertEqual(spanish_metaphone('Embotellar'), 'EMVTYR')
        self.assertEqual(
            spanish_metaphone('Embotellar', modified=True), 'ENVTYR'
        )
        self.assertEqual(spanish_metaphone('Hoy'), 'OY')
        self.assertEqual(spanish_metaphone('Hoy', modified=True), 'OY')
        self.assertEqual(spanish_metaphone('Xochimilco'), 'XXMLK')
        self.assertEqual(
            spanish_metaphone('Xochimilco', modified=True), 'XXMLK'
        )
        self.assertEqual(spanish_metaphone('Psiquiatra'), 'PSKTR')
        self.assertEqual(
            spanish_metaphone('Psiquiatra', modified=True), 'ZKTR'
        )
        self.assertEqual(spanish_metaphone('siquiatra'), 'SKTR')
        self.assertEqual(spanish_metaphone('siquiatra', modified=True), 'ZKTR')
        self.assertEqual(spanish_metaphone('Obscuro'), 'OVSKR')
        self.assertEqual(spanish_metaphone('Obscuro', modified=True), 'OZKR')
        self.assertEqual(spanish_metaphone('Oscuro'), 'OSKR')
        self.assertEqual(spanish_metaphone('Oscuro', modified=True), 'OZKR')
        self.assertEqual(spanish_metaphone('Combate'), 'KMVT')
        self.assertEqual(spanish_metaphone('Combate', modified=True), 'KNVT')
        self.assertEqual(spanish_metaphone('Convate'), 'KNVT')
        self.assertEqual(spanish_metaphone('Convate', modified=True), 'KNVT')
        self.assertEqual(spanish_metaphone('Conbate'), 'KNVT')
        self.assertEqual(spanish_metaphone('Conbate', modified=True), 'KNVT')
        self.assertEqual(spanish_metaphone('Comportar'), 'KMPRTR')
        self.assertEqual(
            spanish_metaphone('Comportar', modified=True), 'KNPRTR'
        )
        self.assertEqual(spanish_metaphone('Conportar'), 'KNPRTR')
        self.assertEqual(
            spanish_metaphone('Conportar', modified=True), 'KNPRTR'
        )
        self.assertEqual(spanish_metaphone('Zapato'), 'ZPT')
        self.assertEqual(spanish_metaphone('Zapato', modified=True), 'ZPT')
        self.assertEqual(spanish_metaphone('Sapato'), 'SPT')
        self.assertEqual(spanish_metaphone('Sapato', modified=True), 'ZPT')
        self.assertEqual(spanish_metaphone('Escalera'), 'ESKLR')
        self.assertEqual(spanish_metaphone('Escalera', modified=True), 'EZKLR')
        self.assertEqual(spanish_metaphone('scalera'), 'ESKLR')
        self.assertEqual(spanish_metaphone('scalera', modified=True), 'EZKLR')

        # terms from algorithm/source
        self.assertEqual(spanish_metaphone('acción'), 'AXN')
        self.assertEqual(spanish_metaphone('reacción'), 'RXN')
        self.assertEqual(spanish_metaphone('cesar'), 'ZSR')
        self.assertEqual(spanish_metaphone('cien'), 'ZN')
        self.assertEqual(spanish_metaphone('cid'), 'ZD')
        self.assertEqual(spanish_metaphone('conciencia'), 'KNZNZ')
        self.assertEqual(spanish_metaphone('gente'), 'JNT')
        self.assertEqual(spanish_metaphone('ecologia'), 'EKLJ')

        # completing coverage
        self.assertEqual(spanish_metaphone('hola'), 'OL')
        self.assertEqual(spanish_metaphone('aqi'), 'AK')
        self.assertEqual(spanish_metaphone('hjordis'), 'HJRDS')


if __name__ == '__main__':
    unittest.main()
