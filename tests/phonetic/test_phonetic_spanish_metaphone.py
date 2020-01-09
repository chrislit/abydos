# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_spanish_metaphone.

This module contains unit tests for abydos.phonetic.SpanishMetaphone
"""

import unittest

from abydos.phonetic import SpanishMetaphone, spanish_metaphone


class SpanishMetaphoneTestCases(unittest.TestCase):
    """Test Spanish Metaphone functions.

    test cases for abydos.phonetic.SpanishMetaphone
    """

    pa = SpanishMetaphone()
    pa_mod = SpanishMetaphone(modified=True)

    def test_spanish_metaphone(self):
        """Test abydos.phonetic.SpanishMetaphone."""
        # Base case
        self.assertEqual(self.pa.encode(''), '')

        # Examples given in
        # https://github.com/amsqr/Spanish-Metaphone/blob/master/phonetic_algorithms_es.py
        self.assertEqual(self.pa.encode('X'), 'X')
        self.assertEqual(self.pa.encode('xplosion'), 'EXPLSN')
        self.assertEqual(self.pa.encode('escalera'), 'ESKLR')
        self.assertEqual(self.pa.encode('scalera'), 'ESKLR')
        self.assertEqual(self.pa.encode('mi'), 'M')
        self.assertEqual(self.pa.encode('tu'), 'T')
        self.assertEqual(self.pa.encode('su'), 'S')
        self.assertEqual(self.pa.encode('te'), 'T')
        self.assertEqual(self.pa.encode('ochooomiiiillllllll'), 'OXMYY')
        self.assertEqual(self.pa.encode('complicado'), 'KMPLKD')
        self.assertEqual(self.pa.encode('ácaro'), 'AKR')
        self.assertEqual(self.pa.encode('ácido'), 'AZD')
        self.assertEqual(self.pa.encode('clown'), 'KLUN')
        self.assertEqual(self.pa.encode('down'), 'DUN')
        self.assertEqual(self.pa.encode('col'), 'KL')
        self.assertEqual(self.pa.encode('clon'), 'KLN')
        self.assertEqual(self.pa.encode('waterpolo'), 'UTRPL')
        self.assertEqual(self.pa.encode('aquino'), 'AKN')
        self.assertEqual(self.pa.encode('rebosar'), 'RVSR')
        self.assertEqual(self.pa.encode('rebozar'), 'RVZR')
        self.assertEqual(self.pa.encode('grajea'), 'GRJ')
        self.assertEqual(self.pa.encode('gragea'), 'GRJ')
        self.assertEqual(self.pa.encode('encima'), 'ENZM')
        self.assertEqual(self.pa.encode('enzima'), 'ENZM')
        self.assertEqual(self.pa.encode('alhamar'), 'ALAMR')
        self.assertEqual(self.pa.encode('abollar'), 'AVYR')
        self.assertEqual(self.pa.encode('aboyar'), 'AVYR')
        self.assertEqual(self.pa.encode('huevo'), 'UV')
        self.assertEqual(self.pa.encode('webo'), 'UV')
        self.assertEqual(self.pa.encode('macho'), 'MX')
        self.assertEqual(self.pa.encode('xocolate'), 'XKLT')
        self.assertEqual(self.pa.encode('chocolate'), 'XKLT')
        self.assertEqual(self.pa.encode('axioma'), 'AXM')
        self.assertEqual(self.pa.encode('abedul'), 'AVDL')
        self.assertEqual(self.pa.encode('a'), 'A')
        self.assertEqual(self.pa.encode('gengibre'), 'JNJVR')
        self.assertEqual(self.pa.encode('yema'), 'YM')
        self.assertEqual(self.pa.encode('wHISKY'), 'UISKY')
        self.assertEqual(self.pa.encode('google'), 'GGL')
        self.assertEqual(self.pa.encode('xilófono'), 'XLFN')
        self.assertEqual(self.pa.encode('web'), 'UV')
        self.assertEqual(self.pa.encode('guerra'), 'GRR')
        self.assertEqual(self.pa.encode('pingüino'), 'PNUN')
        self.assertEqual(self.pa.encode('si'), 'S')
        self.assertEqual(self.pa.encode('ke'), 'K')
        self.assertEqual(self.pa.encode('que'), 'K')
        self.assertEqual(self.pa.encode('tu'), 'T')
        self.assertEqual(self.pa.encode('gato'), 'GT')
        self.assertEqual(self.pa.encode('gitano'), 'JTN')
        self.assertEqual(self.pa.encode('queso'), 'KS')
        self.assertEqual(self.pa.encode('paquete'), 'PKT')
        self.assertEqual(self.pa.encode('cuco'), 'KK')
        self.assertEqual(self.pa.encode('perro'), 'PRR')
        self.assertEqual(self.pa.encode('pero'), 'PR')
        self.assertEqual(self.pa.encode('arrebato'), 'ARRVT')
        self.assertEqual(self.pa.encode('hola'), 'OL')
        self.assertEqual(self.pa.encode('zapato'), 'ZPT')
        self.assertEqual(self.pa.encode('españa'), 'ESPNY')
        self.assertEqual(self.pa.encode('garrulo'), 'GRRL')
        self.assertEqual(self.pa.encode('expansión'), 'EXPNSN')
        self.assertEqual(self.pa.encode('membrillo'), 'MMVRY')
        self.assertEqual(self.pa.encode('jamón'), 'JMN')
        self.assertEqual(self.pa.encode('risa'), 'RS')
        self.assertEqual(self.pa.encode('caricia'), 'KRZ')
        self.assertEqual(self.pa.encode('llaves'), 'YVS')
        self.assertEqual(self.pa.encode('paella'), 'PY')
        self.assertEqual(self.pa.encode('cerilla'), 'ZRY')

        # tests from file:///home/chrislit/Downloads/ICTRS_2016_12.pdf
        # including of the modified version of the algorithm
        self.assertEqual(self.pa.encode('Caricia'), 'KRZ')
        self.assertEqual(self.pa_mod.encode('Caricia'), 'KRZ')
        self.assertEqual(self.pa.encode('Llaves'), 'YVS')
        self.assertEqual(self.pa_mod.encode('Llaves'), 'YVZ')
        self.assertEqual(self.pa.encode('Paella'), 'PY')
        self.assertEqual(self.pa_mod.encode('Paella'), 'PY')
        self.assertEqual(self.pa.encode('Cerilla'), 'ZRY')
        self.assertEqual(self.pa_mod.encode('Cerilla'), 'ZRY')
        self.assertEqual(self.pa.encode('Empeorar'), 'EMPRR')
        self.assertEqual(self.pa_mod.encode('Empeorar'), 'ENPRR')
        self.assertEqual(self.pa.encode('Embotellar'), 'EMVTYR')
        self.assertEqual(self.pa_mod.encode('Embotellar'), 'ENVTYR')
        self.assertEqual(self.pa.encode('Hoy'), 'OY')
        self.assertEqual(self.pa_mod.encode('Hoy'), 'OY')
        self.assertEqual(self.pa.encode('Xochimilco'), 'XXMLK')
        self.assertEqual(self.pa_mod.encode('Xochimilco'), 'XXMLK')
        self.assertEqual(self.pa.encode('Psiquiatra'), 'PSKTR')
        self.assertEqual(self.pa_mod.encode('Psiquiatra'), 'ZKTR')
        self.assertEqual(self.pa.encode('siquiatra'), 'SKTR')
        self.assertEqual(self.pa_mod.encode('siquiatra'), 'ZKTR')
        self.assertEqual(self.pa.encode('Obscuro'), 'OVSKR')
        self.assertEqual(self.pa_mod.encode('Obscuro'), 'OZKR')
        self.assertEqual(self.pa.encode('Oscuro'), 'OSKR')
        self.assertEqual(self.pa_mod.encode('Oscuro'), 'OZKR')
        self.assertEqual(self.pa.encode('Combate'), 'KMVT')
        self.assertEqual(self.pa_mod.encode('Combate'), 'KNVT')
        self.assertEqual(self.pa.encode('Convate'), 'KNVT')
        self.assertEqual(self.pa_mod.encode('Convate'), 'KNVT')
        self.assertEqual(self.pa.encode('Conbate'), 'KNVT')
        self.assertEqual(self.pa_mod.encode('Conbate'), 'KNVT')
        self.assertEqual(self.pa.encode('Comportar'), 'KMPRTR')
        self.assertEqual(self.pa_mod.encode('Comportar'), 'KNPRTR')
        self.assertEqual(self.pa.encode('Conportar'), 'KNPRTR')
        self.assertEqual(self.pa_mod.encode('Conportar'), 'KNPRTR')
        self.assertEqual(self.pa.encode('Zapato'), 'ZPT')
        self.assertEqual(self.pa_mod.encode('Zapato'), 'ZPT')
        self.assertEqual(self.pa.encode('Sapato'), 'SPT')
        self.assertEqual(self.pa_mod.encode('Sapato'), 'ZPT')
        self.assertEqual(self.pa.encode('Escalera'), 'ESKLR')
        self.assertEqual(self.pa_mod.encode('Escalera'), 'EZKLR')
        self.assertEqual(self.pa.encode('scalera'), 'ESKLR')
        self.assertEqual(self.pa_mod.encode('scalera'), 'EZKLR')

        # terms from algorithm/source
        self.assertEqual(self.pa.encode('acción'), 'AXN')
        self.assertEqual(self.pa.encode('reacción'), 'RXN')
        self.assertEqual(self.pa.encode('cesar'), 'ZSR')
        self.assertEqual(self.pa.encode('cien'), 'ZN')
        self.assertEqual(self.pa.encode('cid'), 'ZD')
        self.assertEqual(self.pa.encode('conciencia'), 'KNZNZ')
        self.assertEqual(self.pa.encode('gente'), 'JNT')
        self.assertEqual(self.pa.encode('ecologia'), 'EKLJ')

        # completing coverage
        self.assertEqual(self.pa.encode('hola'), 'OL')
        self.assertEqual(self.pa.encode('aqi'), 'AK')
        self.assertEqual(self.pa.encode('hjordis'), 'HJRDS')

        # Test wrapper
        self.assertEqual(spanish_metaphone('complicado'), 'KMPLKD')


if __name__ == '__main__':
    unittest.main()
