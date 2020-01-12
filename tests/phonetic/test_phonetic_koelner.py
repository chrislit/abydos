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

"""abydos.tests.phonetic.test_phonetic_koelner.

This module contains unit tests for abydos.phonetic.Koelner
"""

import unittest

from abydos.phonetic import Koelner


class KoelnerTestCases(unittest.TestCase):
    """Test Koelner Phonetic functions.

    test cases for abydos.phonetic.Koelner
    """

    pa = Koelner()

    def test_koelner_phonetik(self):
        """Test abydos.phonetic.Koelner."""
        self.assertEqual(self.pa.encode(''), '')

        # https://de.wikipedia.org/wiki/K%C3%B6lner_Phonetik
        self.assertEqual(self.pa.encode('Müller-Lüdenscheidt'), '65752682')
        self.assertEqual(self.pa.encode('Wikipedia'), '3412')
        self.assertEqual(self.pa.encode('Breschnew'), '17863')

        # http://search.cpan.org/~maros/Text-Phonetic/lib/Text/Phonetic/Koeln.pm
        self.assertEqual(self.pa.encode('Müller'), '657')
        self.assertEqual(self.pa.encode('schmidt'), '862')
        self.assertEqual(self.pa.encode('schneider'), '8627')
        self.assertEqual(self.pa.encode('fischer'), '387')
        self.assertEqual(self.pa.encode('weber'), '317')
        self.assertEqual(self.pa.encode('meyer'), '67')
        self.assertEqual(self.pa.encode('wagner'), '3467')
        self.assertEqual(self.pa.encode('schulz'), '858')
        self.assertEqual(self.pa.encode('becker'), '147')
        self.assertEqual(self.pa.encode('hoffmann'), '0366')
        self.assertEqual(self.pa.encode('schäfer'), '837')
        self.assertEqual(self.pa.encode('cater'), '427')
        self.assertEqual(self.pa.encode('axel'), '0485')

        # etc. (for code coverage)
        self.assertEqual(self.pa.encode('Akxel'), '0485')
        self.assertEqual(self.pa.encode('Adz'), '08')
        self.assertEqual(self.pa.encode('Alpharades'), '053728')
        self.assertEqual(self.pa.encode('Cent'), '862')
        self.assertEqual(self.pa.encode('Acre'), '087')
        self.assertEqual(self.pa.encode('H'), '')

    def test_koelner_phonetik_n2a(self):
        """Test abydos.phonetic.Koelner._to_alpha."""
        self.assertEqual(
            self.pa._to_alpha('0123456789'), 'APTFKLNRS'  # noqa: SF01
        )

    def test_koelner_phonetik_alpha(self):
        """Test abydos.phonetic.Koelner.encode_alpha."""
        self.assertEqual(
            self.pa.encode_alpha('Müller-Lüdenscheidt'), 'NLRLTNST'
        )
        self.assertEqual(self.pa.encode_alpha('Wikipedia'), 'FKPT')
        self.assertEqual(self.pa.encode_alpha('Breschnew'), 'PRSNF')
        self.assertEqual(self.pa.encode_alpha('Müller'), 'NLR')
        self.assertEqual(self.pa.encode_alpha('schmidt'), 'SNT')
        self.assertEqual(self.pa.encode_alpha('schneider'), 'SNTR')
        self.assertEqual(self.pa.encode_alpha('fischer'), 'FSR')
        self.assertEqual(self.pa.encode_alpha('weber'), 'FPR')
        self.assertEqual(self.pa.encode_alpha('meyer'), 'NR')
        self.assertEqual(self.pa.encode_alpha('wagner'), 'FKNR')
        self.assertEqual(self.pa.encode_alpha('schulz'), 'SLS')
        self.assertEqual(self.pa.encode_alpha('becker'), 'PKR')
        self.assertEqual(self.pa.encode_alpha('hoffmann'), 'AFNN')
        self.assertEqual(self.pa.encode_alpha('schäfer'), 'SFR')
        self.assertEqual(self.pa.encode_alpha('cater'), 'KTR')
        self.assertEqual(self.pa.encode_alpha('axel'), 'AKSL')


if __name__ == '__main__':
    unittest.main()
