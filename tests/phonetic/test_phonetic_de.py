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

"""abydos.tests.phonetic.test_phonetic_de.

This module contains unit tests for abydos.phonetic._de
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic import (
    haase_phonetik,
    koelner_phonetik,
    koelner_phonetik_alpha,
    koelner_phonetik_num_to_alpha,
    phonem,
    reth_schek_phonetik,
)


class KoelnerPhonetikTestCases(unittest.TestCase):
    """Test Koelner Phonetic functions.

    test cases for abydos.phonetic._de.koelner_phonetik,
    .koelner_phonetik_num_to_alpha, & .koelner_phonetik_alpha
    """

    def test_koelner_phonetik(self):
        """Test abydos.phonetic.de.koelner_phonetik."""
        self.assertEqual(koelner_phonetik(''), '')

        # https://de.wikipedia.org/wiki/K%C3%B6lner_Phonetik
        self.assertEqual(koelner_phonetik('Müller-Lüdenscheidt'), '65752682')
        self.assertEqual(koelner_phonetik('Wikipedia'), '3412')
        self.assertEqual(koelner_phonetik('Breschnew'), '17863')

        # http://search.cpan.org/~maros/Text-Phonetic/lib/Text/Phonetic/Koeln.pm
        self.assertEqual(koelner_phonetik('Müller'), '657')
        self.assertEqual(koelner_phonetik('schmidt'), '862')
        self.assertEqual(koelner_phonetik('schneider'), '8627')
        self.assertEqual(koelner_phonetik('fischer'), '387')
        self.assertEqual(koelner_phonetik('weber'), '317')
        self.assertEqual(koelner_phonetik('meyer'), '67')
        self.assertEqual(koelner_phonetik('wagner'), '3467')
        self.assertEqual(koelner_phonetik('schulz'), '858')
        self.assertEqual(koelner_phonetik('becker'), '147')
        self.assertEqual(koelner_phonetik('hoffmann'), '0366')
        self.assertEqual(koelner_phonetik('schäfer'), '837')
        self.assertEqual(koelner_phonetik('cater'), '427')
        self.assertEqual(koelner_phonetik('axel'), '0485')

        # etc. (for code coverage)
        self.assertEqual(koelner_phonetik('Akxel'), '0485')
        self.assertEqual(koelner_phonetik('Adz'), '08')
        self.assertEqual(koelner_phonetik('Alpharades'), '053728')
        self.assertEqual(koelner_phonetik('Cent'), '862')
        self.assertEqual(koelner_phonetik('Acre'), '087')
        self.assertEqual(koelner_phonetik('H'), '')

    def test_koelner_phonetik_n2a(self):
        """Test abydos.phonetic._de.koelner_phonetik_num_to_alpha."""
        self.assertEqual(
            koelner_phonetik_num_to_alpha('0123456789'), 'APTFKLNRS'
        )

    def test_koelner_phonetik_alpha(self):
        """Test abydos.phonetic._de.koelner_phonetik_alpha."""
        self.assertEqual(
            koelner_phonetik_alpha('Müller-Lüdenscheidt'), 'NLRLTNST'
        )
        self.assertEqual(koelner_phonetik_alpha('Wikipedia'), 'FKPT')
        self.assertEqual(koelner_phonetik_alpha('Breschnew'), 'PRSNF')
        self.assertEqual(koelner_phonetik_alpha('Müller'), 'NLR')
        self.assertEqual(koelner_phonetik_alpha('schmidt'), 'SNT')
        self.assertEqual(koelner_phonetik_alpha('schneider'), 'SNTR')
        self.assertEqual(koelner_phonetik_alpha('fischer'), 'FSR')
        self.assertEqual(koelner_phonetik_alpha('weber'), 'FPR')
        self.assertEqual(koelner_phonetik_alpha('meyer'), 'NR')
        self.assertEqual(koelner_phonetik_alpha('wagner'), 'FKNR')
        self.assertEqual(koelner_phonetik_alpha('schulz'), 'SLS')
        self.assertEqual(koelner_phonetik_alpha('becker'), 'PKR')
        self.assertEqual(koelner_phonetik_alpha('hoffmann'), 'AFNN')
        self.assertEqual(koelner_phonetik_alpha('schäfer'), 'SFR')
        self.assertEqual(koelner_phonetik_alpha('cater'), 'KTR')
        self.assertEqual(koelner_phonetik_alpha('axel'), 'AKSL')


class PhonemTestCases(unittest.TestCase):
    """Test Phonem functions.

    test cases for abydos.phonetic._de.phonem
    """

    def test_phonem(self):
        """Test abydos.phonetic._de.phonem."""
        self.assertEqual(phonem(''), '')

        # http://phonetik.phil-fak.uni-koeln.de/fileadmin/home/ritters/Allgemeine_Dateien/Martin_Wilz.pdf
        self.assertEqual(phonem('müller'), 'MYLR')
        self.assertEqual(phonem('schmidt'), 'CMYD')
        self.assertEqual(phonem('schneider'), 'CNAYDR')
        self.assertEqual(phonem('fischer'), 'VYCR')
        self.assertEqual(phonem('weber'), 'VBR')
        self.assertEqual(phonem('meyer'), 'MAYR')
        self.assertEqual(phonem('wagner'), 'VACNR')
        self.assertEqual(phonem('schulz'), 'CULC')
        self.assertEqual(phonem('becker'), 'BCR')
        self.assertEqual(phonem('hoffmann'), 'OVMAN')
        self.assertEqual(phonem('schäfer'), 'CVR')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/008_phonem.t
        self.assertEqual(phonem('mair'), 'MAYR')
        self.assertEqual(phonem('bäker'), 'BCR')
        self.assertEqual(phonem('schaeffer'), 'CVR')
        self.assertEqual(phonem('computer'), 'COMBUDR')
        self.assertEqual(phonem('pfeifer'), 'VAYVR')
        self.assertEqual(phonem('pfeiffer'), 'VAYVR')


class HaasePhonetikTestCases(unittest.TestCase):
    """Test Haase Phonetik functions.

    test cases for abydos.phonetic._de.haase_phonetik
    """

    def test_haase_phonetik(self):
        """Test abydos.phonetic._de.haase_phonetik."""
        # Base cases
        self.assertEqual(haase_phonetik(''), ('',))

        # equivalents
        self.assertEqual(haase_phonetik('Häschen'), haase_phonetik('Haeschen'))
        self.assertEqual(haase_phonetik('Schloß'), haase_phonetik('Schloss'))
        self.assertEqual(haase_phonetik('üben'), haase_phonetik('ueben'))
        self.assertEqual(
            haase_phonetik('Eichörnchen'), haase_phonetik('Eichoernchen')
        )

        # coverage completion
        self.assertEqual(haase_phonetik('Häschen'), ('9896', '9496'))
        self.assertEqual(
            haase_phonetik('Häschen', primary_only=True), ('9896',)
        )
        self.assertEqual(haase_phonetik('Eichörnchen'), ('94976496',))
        self.assertEqual(haase_phonetik('Hexe'), ('9489',))
        self.assertEqual(haase_phonetik('Chemie'), ('4969', '8969'))

        self.assertEqual(haase_phonetik('Brille'), ('17959', '179'))
        self.assertEqual(
            haase_phonetik('Brilleille'), ('1795959', '17959', '179')
        )
        self.assertEqual(haase_phonetik('Niveau'), ('6939',))
        self.assertEqual(haase_phonetik('Korb'), ('4971', '4973'))
        self.assertEqual(haase_phonetik('Heino'), ('969', '9693'))
        self.assertEqual(haase_phonetik('Nekka'), ('6949', '69497'))
        self.assertEqual(haase_phonetik('Aleph'), ('9593',))
        self.assertEqual(haase_phonetik('Aleppo'), ('95919', '959193'))
        self.assertEqual(haase_phonetik('Endzipfel'), ('96891395',))
        self.assertEqual(haase_phonetik('verbrandt'), ('39717962', '39737962'))
        self.assertEqual(haase_phonetik('Cent'), ('8962',))
        self.assertEqual(haase_phonetik('addiscendae'), ('92989629',))
        self.assertEqual(haase_phonetik('kickx'), ('4948',))
        self.assertEqual(haase_phonetik('sanctionen'), ('896829696',))


class RethSchekTestCases(unittest.TestCase):
    """Test Reth-Schek Phonetik functions.

    test cases for abydos.phonetic._de.reth_schek_phonetik
    """

    def test_reth_schek_phonetik(self):
        """Test abydos.phonetic._de.reth_schek_phonetik."""
        # Base cases
        self.assertEqual(reth_schek_phonetik(''), '')

        # equivalents
        self.assertEqual(
            reth_schek_phonetik('Häschen'), reth_schek_phonetik('Haeschen')
        )
        self.assertEqual(
            reth_schek_phonetik('Schloß'), reth_schek_phonetik('Schloss')
        )
        self.assertEqual(
            reth_schek_phonetik('üben'), reth_schek_phonetik('ueben')
        )
        self.assertEqual(
            reth_schek_phonetik('Eichörnchen'),
            reth_schek_phonetik('Eichoernchen'),
        )

        self.assertEqual(reth_schek_phonetik('Häschen'), 'HESCHEN')
        self.assertEqual(reth_schek_phonetik('Eichörnchen'), 'AIGHOERNGHEN')
        self.assertEqual(reth_schek_phonetik('Hexe'), 'HEXE')
        self.assertEqual(reth_schek_phonetik('Chemie'), 'GHEMI')
        self.assertEqual(reth_schek_phonetik('Brille'), 'BRILE')
        self.assertEqual(reth_schek_phonetik('Brilleille'), 'BRILAILE')
        self.assertEqual(reth_schek_phonetik('Niveau'), 'NIFEAU')
        self.assertEqual(reth_schek_phonetik('Korb'), 'GORB')
        self.assertEqual(reth_schek_phonetik('Heino'), 'HAINO')
        self.assertEqual(reth_schek_phonetik('Nekka'), 'NEKA')
        self.assertEqual(reth_schek_phonetik('Aleph'), 'ALEF')
        self.assertEqual(reth_schek_phonetik('Aleppo'), 'ALEBO')
        self.assertEqual(reth_schek_phonetik('Endzipfel'), 'ENDZIBFL')
        self.assertEqual(reth_schek_phonetik('verbrandt'), 'FERBRAND')
        self.assertEqual(reth_schek_phonetik('Cent'), 'GEND')
        self.assertEqual(reth_schek_phonetik('addiscendae'), 'ADISGENDE')
        self.assertEqual(reth_schek_phonetik('kickx'), 'GIGX')
        self.assertEqual(reth_schek_phonetik('sanctionen'), 'SANGDIONEN')
        self.assertEqual(reth_schek_phonetik('Kuh'), 'GU')
        self.assertEqual(reth_schek_phonetik('lecker'), 'LEGR')
        self.assertEqual(reth_schek_phonetik('rödlich'), 'ROEDLIG')


if __name__ == '__main__':
    unittest.main()
