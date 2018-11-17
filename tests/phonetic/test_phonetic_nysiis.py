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

"""abydos.tests.phonetic.test_phonetic_nysiis.

This module contains unit tests for abydos.phonetic.NYSIIS
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import NYSIIS, nysiis


class NysiisTestCases(unittest.TestCase):
    """Test NYSIIS functions.

    test cases for abydos.phonetic.NYSIIS
    """

    pa = NYSIIS()

    def test_nysiis(self):
        """Test abydos.phonetic.NYSIIS."""
        self.assertEqual(self.pa.encode(''), '')

        # http://coryodaniel.com/index.php/2009/12/30/ruby-nysiis-implementation/
        self.assertEqual(self.pa.encode('O\'Daniel'), 'ODANAL')
        self.assertEqual(self.pa.encode('O\'Donnel'), 'ODANAL')
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
        self.assertEqual(
            self.pa.encode('Plumridge', max_length=20), 'PLANRADG'
        )
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
        self.assertEqual(self.pa.encode('Webberley', max_length=20), 'WABARLY')
        self.assertEqual(self.pa.encode('Wibberley', max_length=20), 'WABARLY')

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
        self.assertEqual(self.pa.encode('Niall', max_length=-1), 'NAL')
        self.assertEqual(self.pa.encode('Niall', max_length=0), 'NAL')

        # Test wrapper
        self.assertEqual(nysiis('O\'Daniel'), 'ODANAL')

    def test_modified_nysiis(self):
        """Test abydos.phonetic.NYSIIS (modified version)."""
        self.assertEqual(self.pa.encode('', max_length=-1, modified=True), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        # Some of these were... wrong... and have been corrected
        self.assertEqual(
            self.pa.encode('Daves', max_length=8, modified=True), 'DAV'
        )
        self.assertEqual(
            self.pa.encode('Davies', max_length=8, modified=True), 'DAVY'
        )
        self.assertEqual(
            self.pa.encode('Devies', max_length=8, modified=True), 'DAFY'
        )
        self.assertEqual(
            self.pa.encode('Divish', max_length=8, modified=True), 'DAVAS'
        )
        self.assertEqual(
            self.pa.encode('Dove', max_length=8, modified=True), 'DAV'
        )
        self.assertEqual(
            self.pa.encode('Devese', max_length=8, modified=True), 'DAFAS'
        )
        self.assertEqual(
            self.pa.encode('Devies', max_length=8, modified=True), 'DAFY'
        )
        self.assertEqual(
            self.pa.encode('Devos', max_length=8, modified=True), 'DAF'
        )

        self.assertEqual(
            self.pa.encode('Schmit', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Schmitt', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Schmitz', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Schmoutz', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Schnitt', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Smit', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Smite', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Smits', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Smoot', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Smuts', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Sneath', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Smyth', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            self.pa.encode('Smithy', max_length=8, modified=True), 'SNATY'
        )
        self.assertEqual(
            self.pa.encode('Smithey', max_length=8, modified=True), 'SNATY'
        )

        # http://www.dropby.com/NYSIISTextStrings.html
        # Some of these have been altered since the above uses a different set
        # of modifications.
        self.assertEqual(
            self.pa.encode('Edwards', max_length=8, modified=True), 'EDWAD'
        )
        self.assertEqual(
            self.pa.encode('Perez', max_length=8, modified=True), 'PAR'
        )
        self.assertEqual(
            self.pa.encode('Macintosh', max_length=8, modified=True), 'MCANTAS'
        )
        self.assertEqual(
            self.pa.encode('Phillipson', max_length=8, modified=True),
            'FALAPSAN',
        )
        self.assertEqual(
            self.pa.encode('Haddix', max_length=8, modified=True), 'HADAC'
        )
        self.assertEqual(
            self.pa.encode('Essex', max_length=8, modified=True), 'ESAC'
        )
        self.assertEqual(
            self.pa.encode('Moye', max_length=8, modified=True), 'MY'
        )
        self.assertEqual(
            self.pa.encode('McKee', max_length=8, modified=True), 'MCY'
        )
        self.assertEqual(
            self.pa.encode('Mackie', max_length=8, modified=True), 'MCY'
        )
        self.assertEqual(
            self.pa.encode('Heitschmidt', max_length=8, modified=True),
            'HATSNAD',
        )
        self.assertEqual(
            self.pa.encode('Bart', max_length=8, modified=True), 'BAD'
        )
        self.assertEqual(
            self.pa.encode('Hurd', max_length=8, modified=True), 'HAD'
        )
        self.assertEqual(
            self.pa.encode('Hunt', max_length=8, modified=True), 'HAN'
        )
        self.assertEqual(
            self.pa.encode('Westerlund', max_length=8, modified=True),
            'WASTARLA',
        )
        self.assertEqual(
            self.pa.encode('Evers', max_length=8, modified=True), 'EVAR'
        )
        self.assertEqual(
            self.pa.encode('Devito', max_length=8, modified=True), 'DAFAT'
        )
        self.assertEqual(
            self.pa.encode('Rawson', max_length=8, modified=True), 'RASAN'
        )
        self.assertEqual(
            self.pa.encode('Shoulders', max_length=8, modified=True), 'SALDAR'
        )
        self.assertEqual(
            self.pa.encode('Leighton', max_length=8, modified=True), 'LATAN'
        )
        self.assertEqual(
            self.pa.encode('Wooldridge', max_length=8, modified=True),
            'WALDRAG',
        )
        self.assertEqual(
            self.pa.encode('Oliphant', max_length=8, modified=True), 'OLAFAN'
        )
        self.assertEqual(
            self.pa.encode('Hatchett', max_length=8, modified=True), 'HATCAT'
        )
        self.assertEqual(
            self.pa.encode('McKnight', max_length=8, modified=True), 'MCNAT'
        )
        self.assertEqual(
            self.pa.encode('Rickert', max_length=8, modified=True), 'RACAD'
        )
        self.assertEqual(
            self.pa.encode('Bowman', max_length=8, modified=True), 'BANAN'
        )
        self.assertEqual(
            self.pa.encode('Vasquez', max_length=8, modified=True), 'VASG'
        )
        self.assertEqual(
            self.pa.encode('Bashaw', max_length=8, modified=True), 'BAS'
        )
        self.assertEqual(
            self.pa.encode('Schoenhoeft', max_length=8, modified=True),
            'SANAFT',
        )
        self.assertEqual(
            self.pa.encode('Heywood', max_length=8, modified=True), 'HAD'
        )
        self.assertEqual(
            self.pa.encode('Hayman', max_length=8, modified=True), 'HANAN'
        )
        self.assertEqual(
            self.pa.encode('Seawright', max_length=8, modified=True), 'SARAT'
        )
        self.assertEqual(
            self.pa.encode('Kratzer', max_length=8, modified=True), 'CRATSAR'
        )
        self.assertEqual(
            self.pa.encode('Canaday', max_length=8, modified=True), 'CANADY'
        )
        self.assertEqual(
            self.pa.encode('Crepeau', max_length=8, modified=True), 'CRAP'
        )

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/nysiis.js
        self.assertEqual(
            self.pa.encode('Andrew', max_length=8, modified=True), 'ANDR'
        )
        self.assertEqual(
            self.pa.encode('Robertson', max_length=8, modified=True),
            'RABARTSA',
        )
        self.assertEqual(
            self.pa.encode('Nolan', max_length=8, modified=True), 'NALAN'
        )
        self.assertEqual(
            self.pa.encode('Louis XVI', max_length=8, modified=True), 'LASXV'
        )
        self.assertEqual(
            self.pa.encode('Case', max_length=8, modified=True), 'CAS'
        )
        self.assertEqual(
            self.pa.encode('Mclaughlin', max_length=8, modified=True),
            'MCLAGLAN',
        )
        self.assertEqual(
            self.pa.encode('Awale', max_length=8, modified=True), 'AL'
        )
        self.assertEqual(
            self.pa.encode('Aegir', max_length=8, modified=True), 'AGAR'
        )
        self.assertEqual(
            self.pa.encode('Lundgren', max_length=8, modified=True), 'LANGRAN'
        )
        self.assertEqual(
            self.pa.encode('Philbert', max_length=8, modified=True), 'FALBAD'
        )
        self.assertEqual(
            self.pa.encode('Harry', max_length=8, modified=True), 'HARY'
        )
        self.assertEqual(
            self.pa.encode('Mackenzie', max_length=8, modified=True), 'MCANSY'
        )

        # max_length bounds tests
        self.assertEqual(
            self.pa.encode('Niall', max_length=-1, modified=True), 'NAL'
        )
        self.assertEqual(
            self.pa.encode('Niall', max_length=0, modified=True), 'NAL'
        )

        # coverage
        self.assertEqual(self.pa.encode('Sam Jr.', modified=True), 'ERROR')
        self.assertEqual(self.pa.encode('John Sr.', modified=True), 'ERROR')
        self.assertEqual(self.pa.encode('Wright', modified=True), 'RAT')
        self.assertEqual(self.pa.encode('Rhodes', modified=True), 'RAD')
        self.assertEqual(self.pa.encode('Dgagoda', modified=True), 'GAGAD')
        self.assertEqual(self.pa.encode('Bosch', modified=True), 'BAS')
        self.assertEqual(self.pa.encode('Schrader', modified=True), 'SRADAR')

        # Test wrapper
        self.assertEqual(
            nysiis('Schmitt', max_length=8, modified=True), 'SNAT'
        )


if __name__ == '__main__':
    unittest.main()
