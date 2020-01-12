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

"""abydos.tests.phonetic.test_phonetic_parmar_kumbharana.

This module contains unit tests for abydos.phonetic.ParmarKumbharana
"""

import unittest

from abydos.phonetic import ParmarKumbharana


class ParmarKumbharanaTestCases(unittest.TestCase):
    """Test Parmar-Kumbharana functions.

    test cases for abydos.phonetic.ParmarKumbharana
    """

    pa = ParmarKumbharana()

    def test_parmar_kumbharana(self):
        """Test abydos.phonetic.ParmarKumbharana."""
        # Base cases
        self.assertEqual(self.pa.encode(''), '')

        # Test cases from Parmar & Kumbharana (2014)
        test_cases = (
            ('Week', 'WK'),
            ('Weak', 'WK'),
            ('Piece', 'PS'),
            ('Peace', 'PS'),
            ('Bed', 'BD'),
            ('Bad', 'BD'),
            ('Would', 'WD'),
            ('Wood', 'WD'),
            ('Sun', 'SN'),
            ('Son', 'SN'),
            ('Ship', 'SP'),
            ('Sheep', 'SP'),
            ('Later', 'LTR'),
            ('Letter', 'LTR'),
            ('Low', 'LW'),
            ('Law', 'LW'),
            ('She', 'S'),
            ('See', 'S'),
            ('Sea', 'S'),
            ('Case', 'CS'),
            ('Cash', 'CS'),
            ('Of', 'OF'),
            ('Off', 'OF'),
            ('Live', 'LV'),
            ('Leave', 'LV'),
            ('Sign', 'SN'),
            ('Sine', 'SN'),
            ('Sin', 'SN'),
            ('Seen', 'SN'),
            ('By', 'B'),
            ('Bye', 'B'),
            ('Reach', 'RCH'),
            ('Rich', 'RCH'),
            ('Sort', 'SRT'),
            ('Short', 'SRT'),
            ('Center', 'SNTR'),
            ('Centre', 'SNTR'),
            ('Full', 'FL'),
            ('Fool', 'FL'),
            ('Then', 'THN'),
            ('Than', 'THN'),
            ('Fill', 'FL'),
            ('Feel', 'FL'),
            ('Two', 'TW'),
            ('To', 'T'),
            ('Too', 'T'),
            ('Four', 'FR'),
            ('For', 'FR'),
            ('Mat', 'MT'),
            ('Met', 'MT'),
            ('Merry', 'MR'),
            ('Marry', 'MR'),
        )
        for word, encoding in test_cases:
            self.assertEqual(self.pa.encode(word), encoding)


if __name__ == '__main__':
    unittest.main()
