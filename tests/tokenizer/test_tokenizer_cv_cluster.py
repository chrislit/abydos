# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.tokenizer.test_tokenizer_cv_cluster.

This module contains unit tests for abydos.tokenizer.CVClusterTokenizer
"""

import unittest

from abydos.tokenizer import CVClusterTokenizer


class CVClusterTokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer.CVClusterTokenizer."""

    def test_cv_cluster_tokenizer(self):
        """Test abydos.tokenizer.CVClusterTokenizer."""
        self.assertEqual(
            sorted(CVClusterTokenizer().tokenize('').get_list()), []
        )
        self.assertEqual(
            sorted(CVClusterTokenizer().tokenize('a').get_list()), ['a']
        )

        tok = CVClusterTokenizer()

        self.assertEqual(
            sorted(tok.tokenize('nelson').get_list()),
            sorted(['ne', 'lso', 'n']),
        )
        self.assertEqual(
            sorted(tok.tokenize('neilson').get_list()),
            sorted(['nei', 'lso', 'n']),
        )
        self.assertEqual(
            sorted(tok.tokenize('peninsular').get_list()),
            sorted(['pe', 'ni', 'nsu', 'la', 'r']),
        )
        self.assertEqual(
            sorted(tok.tokenize('spectacular').get_list()),
            sorted(['spe', 'cta', 'cu', 'la', 'r']),
        )
        self.assertEqual(
            sorted(tok.tokenize('sufficiently').get_list()),
            sorted(['su', 'ffi', 'cie', 'ntly']),
        )
        self.assertEqual(
            sorted(tok.tokenize('yachting').get_list()),
            sorted(['ya', 'chti', 'ng']),
        )
        self.assertEqual(
            sorted(tok.tokenize('caterpillars').get_list()),
            sorted(['ca', 'te', 'rpi', 'lla', 'rs']),
        )
        self.assertEqual(
            sorted(tok.tokenize('Götterdämmerung').get_list()),
            sorted(['Gö', 'tte', 'rdä', 'mme', 'ru', 'ng']),
        )

        tok = CVClusterTokenizer(consonants='ptkbdgmn', vowels='aeiouwy')
        self.assertEqual(
            sorted(tok.tokenize('#winning #losing').get_list()),
            sorted(['#', 'wi', 'nni', 'ng', '#', 'losing']),
        )


if __name__ == '__main__':
    unittest.main()
