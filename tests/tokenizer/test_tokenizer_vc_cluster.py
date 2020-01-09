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

"""abydos.tests.tokenizer.test_tokenizer_vc_cluster.

This module contains unit tests for abydos.tokenizer.VCClusterTokenizer
"""

import unittest

from abydos.tokenizer import VCClusterTokenizer


class VCClusterTokenizerTestCases(unittest.TestCase):
    """Test abydos.tokenizer.VCClusterTokenizer."""

    def test_vc_cluster_tokenizer(self):
        """Test abydos.tokenizer.VCClusterTokenizer."""
        self.assertEqual(
            sorted(VCClusterTokenizer().tokenize('').get_list()), []
        )
        self.assertEqual(
            sorted(VCClusterTokenizer().tokenize('a').get_list()), ['a']
        )

        tok = VCClusterTokenizer()

        self.assertEqual(
            sorted(tok.tokenize('nelson').get_list()),
            sorted(['n', 'els', 'on']),
        )
        self.assertEqual(
            sorted(tok.tokenize('neilson').get_list()),
            sorted(['n', 'eils', 'on']),
        )
        self.assertEqual(
            sorted(tok.tokenize('peninsular').get_list()),
            sorted(['p', 'en', 'ins', 'ul', 'ar']),
        )
        self.assertEqual(
            sorted(tok.tokenize('spectacular').get_list()),
            sorted(['sp', 'ect', 'ac', 'ul', 'ar']),
        )
        self.assertEqual(
            sorted(tok.tokenize('sufficiently').get_list()),
            sorted(['s', 'uff', 'ic', 'ientl', 'y']),
        )
        self.assertEqual(
            sorted(tok.tokenize('yachting').get_list()),
            sorted(['yacht', 'ing']),
        )
        self.assertEqual(
            sorted(tok.tokenize('caterpillars').get_list()),
            sorted(['c', 'at', 'erp', 'ill', 'ars']),
        )
        self.assertEqual(
            sorted(tok.tokenize('Götterdämmerung').get_list()),
            sorted(['G', 'ött', 'erd', 'ämm', 'er', 'ung']),
        )

        tok = VCClusterTokenizer(consonants='ptkbdgmn', vowels='aeiouwy')
        self.assertEqual(
            sorted(tok.tokenize('#winning #losing').get_list()),
            sorted(['#', 'winn', 'ing', '#', 'losing']),
        )


if __name__ == '__main__':
    unittest.main()
