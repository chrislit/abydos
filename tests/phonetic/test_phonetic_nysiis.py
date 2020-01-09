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

"""abydos.tests.phonetic.test_phonetic_nysiis.

This module contains unit tests for abydos.phonetic.NYSIIS
"""

import unittest

from abydos.phonetic import NYSIIS, nysiis


class NysiisTestCases(unittest.TestCase):
    """Test NYSIIS functions.

    test cases for abydos.phonetic.NYSIIS
    """

    pa = NYSIIS()
    pa_20 = NYSIIS(max_length=20)
    pa_8mod = NYSIIS(max_length=8, modified=True)
    pa_mod = NYSIIS(modified=True)

    def test_nysiis(self):
        """Test abydos.phonetic.NYSIIS."""
        self.assertEqual(self.pa.encode(''), '')

        # http://coryodaniel.com/index.php/2009/12/30/ruby-nysiis-implementation/
        self.assertEqual(self.pa.encode("O'Daniel"), 'ODANAL')
        self.assertEqual(self.pa.encode("O'Donnel"), 'ODANAL')
        self.assertEqual(self.pa.encode('Cory'), 'CARY')
        self.assertEqual(self.pa.encode('Corey'), 'CARY')
        self.assertEqual(self.pa.encode('Kory'), 'CARY')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(self.pa.encode('Diggell'), 'DAGAL')
        self.assertEqual(self.pa.encode('Dougal'), 'DAGAL')
        self.assertEqual(self.pa.encode('Doughill'), 'DAGAL')
        self.assertEqual(self.pa.encode('Dougill'), 'DAGAL')
        self.assertEqual(self.pa.encode('Dowgill'), 'DAGAL')
        self.assertEqual(self.pa.encode('Dugall'), 'DAGAL')
        self.assertEqual(self.pa.encode('Dugall'), 'DAGAL')
        self.assertEqual(self.pa.encode('Glinde'), 'GLAND')
        self.assertEqual(self.pa_20.encode('Plumridge'), 'PLANRADG')
        self.assertEqual(self.pa.encode('Chinnick'), 'CANAC')
        self.assertEqual(self.pa.encode('Chinnock'), 'CANAC')
        self.assertEqual(self.pa.encode('Chinnock'), 'CANAC')
        self.assertEqual(self.pa.encode('Chomicki'), 'CANAC')
        self.assertEqual(self.pa.encode('Chomicz'), 'CANAC')
        self.assertEqual(self.pa.encode('Schimek'), 'SANAC')
        self.assertEqual(self.pa.encode('Shimuk'), 'SANAC')
        self.assertEqual(self.pa.encode('Simak'), 'SANAC')
        self.assertEqual(self.pa.encode('Simek'), 'SANAC')
        self.assertEqual(self.pa.encode('Simic'), 'SANAC')
        self.assertEqual(self.pa.encode('Sinnock'), 'SANAC')
        self.assertEqual(self.pa.encode('Sinnocke'), 'SANAC')
        self.assertEqual(self.pa.encode('Sunnex'), 'SANAX')
        self.assertEqual(self.pa.encode('Sunnucks'), 'SANAC')
        self.assertEqual(self.pa.encode('Sunock'), 'SANAC')
        self.assertEqual(self.pa_20.encode('Webberley'), 'WABARLY')
        self.assertEqual(self.pa_20.encode('Wibberley'), 'WABARLY')

        # etc. (for code coverage)
        self.assertEqual(self.pa.encode('Alpharades'), 'ALFARA')
        self.assertEqual(self.pa.encode('Aschenputtel'), 'ASANPA')
        self.assertEqual(self.pa.encode('Beverly'), 'BAFARL')
        self.assertEqual(self.pa.encode('Hardt'), 'HARD')
        self.assertEqual(self.pa.encode('acknowledge'), 'ACNALA')
        self.assertEqual(self.pa.encode('MacNeill'), 'MCNAL')
        self.assertEqual(self.pa.encode('MacNeill'), self.pa.encode('McNeill'))
        self.assertEqual(self.pa.encode('Knight'), 'NAGT')
        self.assertEqual(self.pa.encode('Knight'), self.pa.encode('Night'))
        self.assertEqual(self.pa.encode('Pfarr'), 'FAR')
        self.assertEqual(self.pa.encode('Phair'), 'FAR')
        self.assertEqual(self.pa.encode('Phair'), self.pa.encode('Pfarr'))
        self.assertEqual(self.pa.encode('Cherokee'), 'CARACY')
        self.assertEqual(self.pa.encode('Iraq'), 'IRAG')

        # max_length bounds tests
        self.assertEqual(NYSIIS(max_length=-1).encode('Niall'), 'NAL')
        self.assertEqual(NYSIIS(max_length=0).encode('Niall'), 'NAL')

        # Test wrapper
        self.assertEqual(nysiis("O'Daniel"), 'ODANAL')

    def test_modified_nysiis(self):
        """Test abydos.phonetic.NYSIIS (modified version)."""
        self.assertEqual(NYSIIS(max_length=-1, modified=True).encode(''), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        # Some of these were... wrong... and have been corrected
        self.assertEqual(self.pa_8mod.encode('Daves'), 'DAV')
        self.assertEqual(self.pa_8mod.encode('Davies'), 'DAVY')
        self.assertEqual(self.pa_8mod.encode('Devies'), 'DAFY')
        self.assertEqual(self.pa_8mod.encode('Divish'), 'DAVAS')
        self.assertEqual(self.pa_8mod.encode('Dove'), 'DAV')
        self.assertEqual(self.pa_8mod.encode('Devese'), 'DAFAS')
        self.assertEqual(self.pa_8mod.encode('Devies'), 'DAFY')
        self.assertEqual(self.pa_8mod.encode('Devos'), 'DAF')

        self.assertEqual(self.pa_8mod.encode('Schmit'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Schmitt'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Schmitz'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Schmoutz'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Schnitt'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Smit'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Smite'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Smits'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Smoot'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Smuts'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Sneath'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Smyth'), 'SNAT')
        self.assertEqual(self.pa_8mod.encode('Smithy'), 'SNATY')
        self.assertEqual(self.pa_8mod.encode('Smithey'), 'SNATY')

        # http://www.dropby.com/NYSIISTextStrings.html
        # Some of these have been altered since the above uses a different set
        # of modifications.
        self.assertEqual(self.pa_8mod.encode('Edwards'), 'EDWAD')
        self.assertEqual(self.pa_8mod.encode('Perez'), 'PAR')
        self.assertEqual(self.pa_8mod.encode('Macintosh'), 'MCANTAS')
        self.assertEqual(self.pa_8mod.encode('Phillipson'), 'FALAPSAN')
        self.assertEqual(self.pa_8mod.encode('Haddix'), 'HADAC')
        self.assertEqual(self.pa_8mod.encode('Essex'), 'ESAC')
        self.assertEqual(self.pa_8mod.encode('Moye'), 'MY')
        self.assertEqual(self.pa_8mod.encode('McKee'), 'MCY')
        self.assertEqual(self.pa_8mod.encode('Mackie'), 'MCY')
        self.assertEqual(self.pa_8mod.encode('Heitschmidt'), 'HATSNAD')
        self.assertEqual(self.pa_8mod.encode('Bart'), 'BAD')
        self.assertEqual(self.pa_8mod.encode('Hurd'), 'HAD')
        self.assertEqual(self.pa_8mod.encode('Hunt'), 'HAN')
        self.assertEqual(self.pa_8mod.encode('Westerlund'), 'WASTARLA')
        self.assertEqual(self.pa_8mod.encode('Evers'), 'EVAR')
        self.assertEqual(self.pa_8mod.encode('Devito'), 'DAFAT')
        self.assertEqual(self.pa_8mod.encode('Rawson'), 'RASAN')
        self.assertEqual(self.pa_8mod.encode('Shoulders'), 'SALDAR')
        self.assertEqual(self.pa_8mod.encode('Leighton'), 'LATAN')
        self.assertEqual(self.pa_8mod.encode('Wooldridge'), 'WALDRAG')
        self.assertEqual(self.pa_8mod.encode('Oliphant'), 'OLAFAN')
        self.assertEqual(self.pa_8mod.encode('Hatchett'), 'HATCAT')
        self.assertEqual(self.pa_8mod.encode('McKnight'), 'MCNAT')
        self.assertEqual(self.pa_8mod.encode('Rickert'), 'RACAD')
        self.assertEqual(self.pa_8mod.encode('Bowman'), 'BANAN')
        self.assertEqual(self.pa_8mod.encode('Vasquez'), 'VASG')
        self.assertEqual(self.pa_8mod.encode('Bashaw'), 'BAS')
        self.assertEqual(self.pa_8mod.encode('Schoenhoeft'), 'SANAFT')
        self.assertEqual(self.pa_8mod.encode('Heywood'), 'HAD')
        self.assertEqual(self.pa_8mod.encode('Hayman'), 'HANAN')
        self.assertEqual(self.pa_8mod.encode('Seawright'), 'SARAT')
        self.assertEqual(self.pa_8mod.encode('Kratzer'), 'CRATSAR')
        self.assertEqual(self.pa_8mod.encode('Canaday'), 'CANADY')
        self.assertEqual(self.pa_8mod.encode('Crepeau'), 'CRAP')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/nysiis.js
        self.assertEqual(self.pa_8mod.encode('Andrew'), 'ANDR')
        self.assertEqual(self.pa_8mod.encode('Robertson'), 'RABARTSA')
        self.assertEqual(self.pa_8mod.encode('Nolan'), 'NALAN')
        self.assertEqual(self.pa_8mod.encode('Louis XVI'), 'LASXV')
        self.assertEqual(self.pa_8mod.encode('Case'), 'CAS')
        self.assertEqual(self.pa_8mod.encode('Mclaughlin'), 'MCLAGLAN')
        self.assertEqual(self.pa_8mod.encode('Awale'), 'AL')
        self.assertEqual(self.pa_8mod.encode('Aegir'), 'AGAR')
        self.assertEqual(self.pa_8mod.encode('Lundgren'), 'LANGRAN')
        self.assertEqual(self.pa_8mod.encode('Philbert'), 'FALBAD')
        self.assertEqual(self.pa_8mod.encode('Harry'), 'HARY')
        self.assertEqual(self.pa_8mod.encode('Mackenzie'), 'MCANSY')

        # max_length bounds tests
        self.assertEqual(
            NYSIIS(max_length=-1, modified=True).encode('Niall'), 'NAL'
        )
        self.assertEqual(
            NYSIIS(max_length=0, modified=True).encode('Niall'), 'NAL'
        )

        # coverage
        self.assertEqual(self.pa_mod.encode('Sam Jr.'), 'ERROR')
        self.assertEqual(self.pa_mod.encode('John Sr.'), 'ERROR')
        self.assertEqual(self.pa_mod.encode('Wright'), 'RAT')
        self.assertEqual(self.pa_mod.encode('Rhodes'), 'RAD')
        self.assertEqual(self.pa_mod.encode('Dgagoda'), 'GAGAD')
        self.assertEqual(self.pa_mod.encode('Bosch'), 'BAS')
        self.assertEqual(self.pa_mod.encode('Schrader'), 'SRADAR')

        # Test wrapper
        self.assertEqual(
            nysiis('Schmitt', max_length=8, modified=True), 'SNAT'
        )


if __name__ == '__main__':
    unittest.main()
