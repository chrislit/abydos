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

"""abydos.tests.stemmer.test_stemmer_caumanns.

This module contains unit tests for abydos.stemmer._caumanns
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.stemmer import caumanns


class CaumannsTestCases(unittest.TestCase):
    """Test Caumanns functions.

    abydos.stemmer._caumanns
    """

    def test_caumanns(self):
        """Test abydos.stemmer._caumanns.caumanns."""
        # base case
        self.assertEqual(caumanns(''), '')

        # tests from Caumanns' description of the algorithm
        self.assertEqual(caumanns('singt'), 'sing')
        self.assertEqual(caumanns('singen'), 'sing')
        self.assertEqual(caumanns('beliebt'), 'belieb')
        self.assertEqual(caumanns('beliebtester'), 'belieb')
        self.assertEqual(caumanns('stören'), 'stor')
        self.assertEqual(caumanns('stöhnen'), 'stoh')
        self.assertEqual(caumanns('Kuß'), 'kuss')
        self.assertEqual(caumanns('Küsse'), 'kuss')
        self.assertEqual(caumanns('Verlierer'), 'verlier')
        self.assertEqual(caumanns('Verlies'), 'verlie')
        self.assertEqual(caumanns('Maus'), 'mau')
        self.assertEqual(caumanns('Mauer'), 'mau')
        self.assertEqual(caumanns('Störsender'), 'stor')

        # additional tests to achieve full coverage
        self.assertEqual(caumanns('Müllerinnen'), 'mullerin')
        self.assertEqual(caumanns('Matrix'), 'matrix')
        self.assertEqual(caumanns('Matrizen'), 'matrix')

    def test_caumanns_lucene(self):
        """Test abydos.stemmer._caumanns.caumanns (Lucene tests).

        Based on tests from
        https://svn.apache.org/repos/asf/lucene.net/trunk/test/contrib/Analyzers/De/data.txt
        This is presumably Apache-licensed.
        """
        # German special characters are replaced:
        self.assertEqual(caumanns('häufig'), 'haufig')
        self.assertEqual(caumanns('üor'), 'uor')
        self.assertEqual(caumanns('björk'), 'bjork')

        # here the stemmer works okay, it maps related words to the same stem:
        self.assertEqual(caumanns('abschließen'), 'abschliess')
        self.assertEqual(caumanns('abschließender'), 'abschliess')
        self.assertEqual(caumanns('abschließendes'), 'abschliess')
        self.assertEqual(caumanns('abschließenden'), 'abschliess')

        self.assertEqual(caumanns('Tisch'), 'tisch')
        self.assertEqual(caumanns('Tische'), 'tisch')
        self.assertEqual(caumanns('Tischen'), 'tisch')
        self.assertEqual(caumanns('geheimtür'), 'geheimtur')

        self.assertEqual(caumanns('Haus'), 'hau')
        self.assertEqual(caumanns('Hauses'), 'hau')
        self.assertEqual(caumanns('Häuser'), 'hau')
        self.assertEqual(caumanns('Häusern'), 'hau')
        # here's a case where overstemming occurs, i.e. a word is
        # mapped to the same stem as unrelated words:
        self.assertEqual(caumanns('hauen'), 'hau')

        # here's a case where understemming occurs, i.e. two related words
        # are not mapped to the same stem. This is the case with basically
        # all irregular forms:
        self.assertEqual(caumanns('Drama'), 'drama')
        self.assertEqual(caumanns('Dramen'), 'dram')

        # replace "ß" with 'ss':
        self.assertEqual(caumanns('Ausmaß'), 'ausmass')

        # fake words to test if suffixes are cut off:
        self.assertEqual(caumanns('xxxxxe'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxs'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxn'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxt'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxem'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxer'), 'xxxxx')
        self.assertEqual(caumanns('xxxxxnd'), 'xxxxx')
        # the suffixes are also removed when combined:
        self.assertEqual(caumanns('xxxxxetende'), 'xxxxx')

        # words that are shorter than four charcters are not changed:
        self.assertEqual(caumanns('xxe'), 'xxe')
        # -em and -er are not removed from words shorter than five characters:
        self.assertEqual(caumanns('xxem'), 'xxem')
        self.assertEqual(caumanns('xxer'), 'xxer')
        # -nd is not removed from words shorter than six characters:
        self.assertEqual(caumanns('xxxnd'), 'xxxnd')


if __name__ == '__main__':
    unittest.main()
