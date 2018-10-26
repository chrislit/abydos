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

"""abydos.tests.distance.test_distance_synoname.

This module contains unit tests for abydos.distance._synoname
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance import synoname
# noinspection PyProtectedMember
from abydos.distance._synoname import _synoname_strip_punct, _synoname_word_approximation


class SynonameTestCases(unittest.TestCase):
    """Test Synoname functions.

    abydos.distance._synoname._synoname_strip_punct,
    _synoname_word_approximation, & synoname
    """

    def test_synoname_strip_punct(self):
        """Test abydos.distance._synoname._synoname_strip_punct."""
        # Base cases
        self.assertEqual(_synoname_strip_punct(''), '')
        self.assertEqual(_synoname_strip_punct('abcdefg'), 'abcdefg')
        self.assertEqual(_synoname_strip_punct('a\'b-c,d!e:f%g'), 'abcdefg')

    def test_synoname_word_approximation(self):
        """Test abydos.distance._synoname._synoname_word_approximation."""
        # Base cases
        self.assertEqual(_synoname_word_approximation('', ''), 0)

        self.assertEqual(
            _synoname_word_approximation(
                'di Domenico di Bonaventura',
                'di Tomme di Nuto',
                'Cosimo',
                'Luca',
            ),
            0.4,
        )
        self.assertEqual(
            _synoname_word_approximation(
                'Antonello da Messina',
                'Messina',
                '',
                'Antonello da',
                {
                    'gen_conflict': False,
                    'roman_conflict': False,
                    'src_specials': [(35, 'b'), (35, 'c')],
                    'tar_specials': [(35, 'b'), (35, 'c')],
                },
            ),
            0,
        )
        self.assertEqual(
            _synoname_word_approximation(
                'louis ii',
                'louis ii',
                'sr jean',
                'sr  pierre',
                {
                    'gen_conflict': False,
                    'roman_conflict': False,
                    'src_specials': [(49, 'b'), (68, 'd'), (121, 'b')],
                    'tar_specials': [(49, 'b'), (68, 'd'), (121, 'b')],
                },
            ),
            0,
        )
        self.assertEqual(
            _synoname_word_approximation(
                'louis ii',
                'louis ii',
                'il giovane',
                'sr cadet',
                {
                    'gen_conflict': False,
                    'roman_conflict': False,
                    'src_specials': [
                        (46, 'a'),
                        (49, 'b'),
                        (52, 'a'),
                        (68, 'd'),
                    ],
                    'tar_specials': [
                        (8, 'a'),
                        (49, 'b'),
                        (68, 'd'),
                        (121, 'a'),
                    ],
                },
            ),
            1,
        )
        self.assertAlmostEqual(
            _synoname_word_approximation(
                'louis ii',
                'louis ii',
                'ste.-geo ste.',
                'ste.-jo ste.',
                {
                    'gen_conflict': False,
                    'roman_conflict': False,
                    'src_specials': [
                        (49, 'b'),
                        (68, 'd'),
                        (127, 'b'),
                        (127, 'X'),
                    ],
                    'tar_specials': [
                        (49, 'b'),
                        (68, 'd'),
                        (127, 'b'),
                        (127, 'X'),
                    ],
                },
            ),
            2 / 3,
        )
        self.assertAlmostEqual(
            _synoname_word_approximation(
                'louis ii',
                'louis',
                'ste.-geo ste.',
                '',
                {
                    'gen_conflict': False,
                    'roman_conflict': False,
                    'src_specials': [
                        (49, 'b'),
                        (68, 'd'),
                        (127, 'b'),
                        (127, 'X'),
                    ],
                    'tar_specials': [],
                },
            ),
            0,
        )
        self.assertAlmostEqual(
            _synoname_word_approximation(
                'lou ii', 'louis', 'louis iv', 'ste.', {}
            ),
            0,
        )
        self.assertEqual(
            _synoname_word_approximation(
                'ren',
                'loren ste.',
                '',
                '',
                {
                    'tar_specials': [(68, 'd'), (127, 'X')],
                    'src_specials': [(0, '')],
                },
            ),
            1,
        )

    def test_synoname(self):
        """Test abydos.distance._synoname.synoname."""
        # Base cases
        self.assertEqual(synoname('', ''), 1)
        self.assertEqual(synoname('', '', tests=['exact']), 1)
        self.assertEqual(synoname('', '', tests=[]), 13)
        self.assertEqual(synoname('', '', tests=['nonsense-test']), 13)
        self.assertEqual(synoname('', '', ret_name=True), 'exact')

        # Test input formats
        self.assertEqual(
            synoname(
                ('Brueghel II (the Younger)', 'Pieter', 'Workshop of'),
                ('Brueghel II (the Younger)', 'Pieter', 'Workshop of'),
            ),
            1,
        )
        self.assertEqual(
            synoname(
                'Brueghel II (the Younger)#Pieter#' + 'Workshop of',
                'Brueghel II (the Younger)#Pieter#' + 'Workshop of',
            ),
            1,
        )
        self.assertEqual(
            synoname(
                '22#Brueghel II (the Younger)#Pieter#' + 'Workshop of',
                '44#Brueghel II (the Younger)#Pieter#' + 'Workshop of',
            ),
            1,
        )

        # approx_c tests
        self.assertEqual(
            synoname(
                (
                    'Master of Brueghel II (the Younger)',
                    'Pieter',
                    'Workshop of',
                ),
                ('Brueghel I (the Elder)', 'Pieter', 'Workshop of'),
            ),
            13,
        )
        self.assertEqual(
            synoname(
                ('Master of Brueghel II', 'Pieter', 'Workshop of'),
                ('Master known as the Brueghel II', 'Pieter', 'Workshop of'),
            ),
            10,
        )

        # Types 1-12
        self.assertEqual(
            synoname(
                ('Brueghel', 'Pieter', ''),
                ('Brueghel', 'Pieter', ''),
                ret_name=True,
            ),
            'exact',
        )

        self.assertEqual(
            synoname(
                ('Brueghel II', 'Pieter', ''),
                ('Brueghel I', 'Pieter', ''),
                ret_name=True,
            ),
            'no_match',
        )
        self.assertEqual(
            synoname(
                ('Breghel', 'Pieter', ''),
                ('Brueghel', 'Pieter', ''),
                ret_name=True,
            ),
            'omission',
        )
        self.assertEqual(
            synoname(
                ('Brueghel', 'Pieter', ''),
                ('Breghel', 'Pieter', ''),
                ret_name=True,
            ),
            'omission',
        )
        self.assertEqual(
            synoname(
                ('Brueghel', 'Piter', ''),
                ('Brueghel', 'Pieter', ''),
                ret_name=True,
            ),
            'omission',
        )
        self.assertEqual(
            synoname(
                ('Brueghel', 'Pieter', ''),
                ('Brueghel', 'Piter', ''),
                ret_name=True,
            ),
            'omission',
        )
        self.assertEqual(
            synoname(
                ('Brughel', 'Pieter', ''),
                ('Breghel', 'Pieter', ''),
                ret_name=True,
            ),
            'substitution',
        )
        self.assertEqual(
            synoname(
                ('Breughel', 'Peter', ''),
                ('Breughel', 'Piter', ''),
                ret_name=True,
            ),
            'substitution',
        )
        self.assertEqual(
            synoname(
                ('Brueghel', 'Pieter', ''),
                ('Breughel', 'Pieter', ''),
                ret_name=True,
            ),
            'transposition',
        )
        self.assertEqual(
            synoname(
                ('Brueghel', 'Peiter', ''),
                ('Brueghel', 'Pieter', ''),
                ret_name=True,
            ),
            'transposition',
        )

        self.assertEqual(
            synoname(
                ('Brueghel:', 'Pieter', ''),
                ('Brueghel', 'Pi-eter', ''),
                ret_name=True,
            ),
            'punctuation',
        )
        self.assertEqual(
            synoname(
                ('Brueghel,', 'Pieter', ''),
                ('Brueghel', 'Pieter...', ''),
                ret_name=True,
            ),
            'punctuation',
        )
        self.assertEqual(
            synoname(
                ('Seu rat', 'George Pierre', ''),
                ('Seu-rat', 'George-Pierre', ''),
                ret_name=True,
            ),
            'punctuation',
        )
        self.assertEqual(
            synoname(
                ('Picasso', '', ''), ('Picasso', 'Pablo', ''), ret_name=True
            ),
            'no_first',
        )
        self.assertEqual(
            synoname(
                ('Pereira', 'I. R.', ''),
                ('Pereira', 'Irene Rice', ''),
                ret_name=True,
            ),
            'initials',
        )
        self.assertEqual(
            synoname(
                ('Pereira', 'I.', ''),
                ('Pereira', 'Irene Rice', ''),
                ret_name=True,
            ),
            'initials',
        )
        self.assertNotEqual(
            synoname(
                ('Pereira', 'I. R.', ''),
                ('Pereira', 'I. Smith', ''),
                ret_name=True,
            ),
            'initials',
        )
        self.assertNotEqual(
            synoname(
                ('Pereira', 'I. R. S.', ''),
                ('Pereira', 'I. S. R.', ''),
                ret_name=True,
            ),
            'initials',
        )
        self.assertEqual(
            synoname(
                ('de Goya', 'Francisco', ''),
                ('de Goya y Lucientes', 'Francisco', ''),
                ret_name=True,
            ),
            'extension',
        )
        self.assertEqual(
            synoname(
                ('Seurat', 'George', ''),
                ('Seurat', 'George-Pierre', ''),
                ret_name=True,
            ),
            'extension',
        )
        self.assertEqual(
            synoname(
                ('Gericault', 'Theodore', ''),
                ('Gericault', 'Jean Louis Andre Theodore', ''),
                ret_name=True,
            ),
            'inclusion',
        )
        self.assertEqual(
            synoname(
                ('Dore', 'Gustave', ''),
                ('Dore', 'Paul Gustave Louis Christophe', ''),
                ret_name=True,
            ),
            'inclusion',
        )

        self.assertEqual(
            synoname(
                ('Rosetti', 'Dante Gabriel', ''),
                ('Rosetti', 'Gabriel Charles Dante', ''),
                ret_name=True,
            ),
            'word_approx',
        )
        self.assertEqual(
            synoname(
                ('di Domenico di Bonaventura', 'Cosimo', ''),
                ('di Tomme di Nuto', 'Luca', ''),
                ret_name=True,
            ),
            'no_match',
        )
        self.assertEqual(
            synoname(
                ('Pereira', 'I. R.', ''),
                ('Pereira', 'I. Smith', ''),
                ret_name=True,
            ),
            'word_approx',
        )
        self.assertEqual(
            synoname(
                ('Antonello da Messina', '', ''),
                ('Messina', 'Antonello da', ''),
                ret_name=True,
            ),
            'confusions',
        )
        self.assertEqual(
            synoname(
                ('Brueghel', 'Pietter', ''),
                ('Bruegghel', 'Pieter', ''),
                ret_name=True,
            ),
            'char_approx',
        )


if __name__ == '__main__':
    unittest.main()
