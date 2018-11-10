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

This module contains unit tests for abydos.phonetic._nysiis
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import nysiis


class NysiisTestCases(unittest.TestCase):
    """Test NYSIIS functions.

    test cases for abydos.phonetic._nysiis.nysiis
    """

    def test_nysiis(self):
        """Test abydos.phonetic._nysiis.nysiis."""
        self.assertEqual(nysiis(''), '')

        # http://coryodaniel.com/index.php/2009/12/30/ruby-nysiis-implementation/
        self.assertEqual(nysiis('O\'Daniel'), 'ODANAL')
        self.assertEqual(nysiis('O\'Donnel'), 'ODANAL')
        self.assertEqual(nysiis('Cory'), 'CARY')
        self.assertEqual(nysiis('Corey'), 'CARY')
        self.assertEqual(nysiis('Kory'), 'CARY')

        # http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
        self.assertEqual(nysiis('Diggell'), 'DAGAL')
        self.assertEqual(nysiis('Dougal'), 'DAGAL')
        self.assertEqual(nysiis('Doughill'), 'DAGAL')
        self.assertEqual(nysiis('Dougill'), 'DAGAL')
        self.assertEqual(nysiis('Dowgill'), 'DAGAL')
        self.assertEqual(nysiis('Dugall'), 'DAGAL')
        self.assertEqual(nysiis('Dugall'), 'DAGAL')
        self.assertEqual(nysiis('Glinde'), 'GLAND')
        self.assertEqual(nysiis('Plumridge', max_length=20), 'PLANRADG')
        self.assertEqual(nysiis('Chinnick'), 'CANAC')
        self.assertEqual(nysiis('Chinnock'), 'CANAC')
        self.assertEqual(nysiis('Chinnock'), 'CANAC')
        self.assertEqual(nysiis('Chomicki'), 'CANAC')
        self.assertEqual(nysiis('Chomicz'), 'CANAC')
        self.assertEqual(nysiis('Schimek'), 'SANAC')
        self.assertEqual(nysiis('Shimuk'), 'SANAC')
        self.assertEqual(nysiis('Simak'), 'SANAC')
        self.assertEqual(nysiis('Simek'), 'SANAC')
        self.assertEqual(nysiis('Simic'), 'SANAC')
        self.assertEqual(nysiis('Sinnock'), 'SANAC')
        self.assertEqual(nysiis('Sinnocke'), 'SANAC')
        self.assertEqual(nysiis('Sunnex'), 'SANAX')
        self.assertEqual(nysiis('Sunnucks'), 'SANAC')
        self.assertEqual(nysiis('Sunock'), 'SANAC')
        self.assertEqual(nysiis('Webberley', max_length=20), 'WABARLY')
        self.assertEqual(nysiis('Wibberley', max_length=20), 'WABARLY')

        # etc. (for code coverage)
        self.assertEqual(nysiis('Alpharades'), 'ALFARA')
        self.assertEqual(nysiis('Aschenputtel'), 'ASANPA')
        self.assertEqual(nysiis('Beverly'), 'BAFARL')
        self.assertEqual(nysiis('Hardt'), 'HARD')
        self.assertEqual(nysiis('acknowledge'), 'ACNALA')
        self.assertEqual(nysiis('MacNeill'), 'MCNAL')
        self.assertEqual(nysiis('MacNeill'), nysiis('McNeill'))
        self.assertEqual(nysiis('Knight'), 'NAGT')
        self.assertEqual(nysiis('Knight'), nysiis('Night'))
        self.assertEqual(nysiis('Pfarr'), 'FAR')
        self.assertEqual(nysiis('Phair'), 'FAR')
        self.assertEqual(nysiis('Phair'), nysiis('Pfarr'))
        self.assertEqual(nysiis('Cherokee'), 'CARACY')
        self.assertEqual(nysiis('Iraq'), 'IRAG')

        # max_length bounds tests
        self.assertEqual(nysiis('Niall', max_length=-1), 'NAL')
        self.assertEqual(nysiis('Niall', max_length=0), 'NAL')

    def test_modified_nysiis(self):
        """Test abydos.phonetic._nysiis.nysiis (modified version)."""
        self.assertEqual(nysiis('', max_length=-1, modified=True), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        # Some of these were... wrong... and have been corrected
        self.assertEqual(nysiis('Daves', max_length=8, modified=True), 'DAV')
        self.assertEqual(nysiis('Davies', max_length=8, modified=True), 'DAVY')
        self.assertEqual(nysiis('Devies', max_length=8, modified=True), 'DAFY')
        self.assertEqual(
            nysiis('Divish', max_length=8, modified=True), 'DAVAS'
        )
        self.assertEqual(nysiis('Dove', max_length=8, modified=True), 'DAV')
        self.assertEqual(
            nysiis('Devese', max_length=8, modified=True), 'DAFAS'
        )
        self.assertEqual(nysiis('Devies', max_length=8, modified=True), 'DAFY')
        self.assertEqual(nysiis('Devos', max_length=8, modified=True), 'DAF')

        self.assertEqual(nysiis('Schmit', max_length=8, modified=True), 'SNAT')
        self.assertEqual(
            nysiis('Schmitt', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            nysiis('Schmitz', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            nysiis('Schmoutz', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(
            nysiis('Schnitt', max_length=8, modified=True), 'SNAT'
        )
        self.assertEqual(nysiis('Smit', max_length=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smite', max_length=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smits', max_length=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smoot', max_length=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smuts', max_length=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Sneath', max_length=8, modified=True), 'SNAT')
        self.assertEqual(nysiis('Smyth', max_length=8, modified=True), 'SNAT')
        self.assertEqual(
            nysiis('Smithy', max_length=8, modified=True), 'SNATY'
        )
        self.assertEqual(
            nysiis('Smithey', max_length=8, modified=True), 'SNATY'
        )

        # http://www.dropby.com/NYSIISTextStrings.html
        # Some of these have been altered since the above uses a different set
        # of modifications.
        self.assertEqual(
            nysiis('Edwards', max_length=8, modified=True), 'EDWAD'
        )
        self.assertEqual(nysiis('Perez', max_length=8, modified=True), 'PAR')
        self.assertEqual(
            nysiis('Macintosh', max_length=8, modified=True), 'MCANTAS'
        )
        self.assertEqual(
            nysiis('Phillipson', max_length=8, modified=True), 'FALAPSAN'
        )
        self.assertEqual(
            nysiis('Haddix', max_length=8, modified=True), 'HADAC'
        )
        self.assertEqual(nysiis('Essex', max_length=8, modified=True), 'ESAC')
        self.assertEqual(nysiis('Moye', max_length=8, modified=True), 'MY')
        self.assertEqual(nysiis('McKee', max_length=8, modified=True), 'MCY')
        self.assertEqual(nysiis('Mackie', max_length=8, modified=True), 'MCY')
        self.assertEqual(
            nysiis('Heitschmidt', max_length=8, modified=True), 'HATSNAD'
        )
        self.assertEqual(nysiis('Bart', max_length=8, modified=True), 'BAD')
        self.assertEqual(nysiis('Hurd', max_length=8, modified=True), 'HAD')
        self.assertEqual(nysiis('Hunt', max_length=8, modified=True), 'HAN')
        self.assertEqual(
            nysiis('Westerlund', max_length=8, modified=True), 'WASTARLA'
        )
        self.assertEqual(nysiis('Evers', max_length=8, modified=True), 'EVAR')
        self.assertEqual(
            nysiis('Devito', max_length=8, modified=True), 'DAFAT'
        )
        self.assertEqual(
            nysiis('Rawson', max_length=8, modified=True), 'RASAN'
        )
        self.assertEqual(
            nysiis('Shoulders', max_length=8, modified=True), 'SALDAR'
        )
        self.assertEqual(
            nysiis('Leighton', max_length=8, modified=True), 'LATAN'
        )
        self.assertEqual(
            nysiis('Wooldridge', max_length=8, modified=True), 'WALDRAG'
        )
        self.assertEqual(
            nysiis('Oliphant', max_length=8, modified=True), 'OLAFAN'
        )
        self.assertEqual(
            nysiis('Hatchett', max_length=8, modified=True), 'HATCAT'
        )
        self.assertEqual(
            nysiis('McKnight', max_length=8, modified=True), 'MCNAT'
        )
        self.assertEqual(
            nysiis('Rickert', max_length=8, modified=True), 'RACAD'
        )
        self.assertEqual(
            nysiis('Bowman', max_length=8, modified=True), 'BANAN'
        )
        self.assertEqual(
            nysiis('Vasquez', max_length=8, modified=True), 'VASG'
        )
        self.assertEqual(nysiis('Bashaw', max_length=8, modified=True), 'BAS')
        self.assertEqual(
            nysiis('Schoenhoeft', max_length=8, modified=True), 'SANAFT'
        )
        self.assertEqual(nysiis('Heywood', max_length=8, modified=True), 'HAD')
        self.assertEqual(
            nysiis('Hayman', max_length=8, modified=True), 'HANAN'
        )
        self.assertEqual(
            nysiis('Seawright', max_length=8, modified=True), 'SARAT'
        )
        self.assertEqual(
            nysiis('Kratzer', max_length=8, modified=True), 'CRATSAR'
        )
        self.assertEqual(
            nysiis('Canaday', max_length=8, modified=True), 'CANADY'
        )
        self.assertEqual(
            nysiis('Crepeau', max_length=8, modified=True), 'CRAP'
        )

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/nysiis.js
        self.assertEqual(nysiis('Andrew', max_length=8, modified=True), 'ANDR')
        self.assertEqual(
            nysiis('Robertson', max_length=8, modified=True), 'RABARTSA'
        )
        self.assertEqual(nysiis('Nolan', max_length=8, modified=True), 'NALAN')
        self.assertEqual(
            nysiis('Louis XVI', max_length=8, modified=True), 'LASXV'
        )
        self.assertEqual(nysiis('Case', max_length=8, modified=True), 'CAS')
        self.assertEqual(
            nysiis('Mclaughlin', max_length=8, modified=True), 'MCLAGLAN'
        )
        self.assertEqual(nysiis('Awale', max_length=8, modified=True), 'AL')
        self.assertEqual(nysiis('Aegir', max_length=8, modified=True), 'AGAR')
        self.assertEqual(
            nysiis('Lundgren', max_length=8, modified=True), 'LANGRAN'
        )
        self.assertEqual(
            nysiis('Philbert', max_length=8, modified=True), 'FALBAD'
        )
        self.assertEqual(nysiis('Harry', max_length=8, modified=True), 'HARY')
        self.assertEqual(
            nysiis('Mackenzie', max_length=8, modified=True), 'MCANSY'
        )

        # max_length bounds tests
        self.assertEqual(nysiis('Niall', max_length=-1, modified=True), 'NAL')
        self.assertEqual(nysiis('Niall', max_length=0, modified=True), 'NAL')

        # coverage
        self.assertEqual(nysiis('Sam Jr.', modified=True), 'ERROR')
        self.assertEqual(nysiis('John Sr.', modified=True), 'ERROR')
        self.assertEqual(nysiis('Wright', modified=True), 'RAT')
        self.assertEqual(nysiis('Rhodes', modified=True), 'RAD')
        self.assertEqual(nysiis('Dgagoda', modified=True), 'GAGAD')
        self.assertEqual(nysiis('Bosch', modified=True), 'BAS')
        self.assertEqual(nysiis('Schrader', modified=True), 'SRADAR')


if __name__ == '__main__':
    unittest.main()
