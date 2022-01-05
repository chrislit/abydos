# Copyright 2014-2022 by Christopher C. Little.
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

This module contains unit tests for abydos.stemmer.Caumanns
"""

import unittest

from abydos.stemmer import Caumanns


class CaumannsTestCases(unittest.TestCase):
    """Test Caumanns functions.

    abydos.stemmer.Caumanns
    """

    stmr = Caumanns()

    def test_caumanns(self):
        """Test abydos.stemmer.Caumanns."""
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        # tests from Caumanns' description of the algorithm
        self.assertEqual(self.stmr.stem('singt'), 'sing')
        self.assertEqual(self.stmr.stem('singen'), 'sing')
        self.assertEqual(self.stmr.stem('beliebt'), 'belieb')
        self.assertEqual(self.stmr.stem('beliebtester'), 'belieb')
        self.assertEqual(self.stmr.stem('stören'), 'stor')
        self.assertEqual(self.stmr.stem('stöhnen'), 'stoh')
        self.assertEqual(self.stmr.stem('Kuß'), 'kuss')
        self.assertEqual(self.stmr.stem('Küsse'), 'kuss')
        self.assertEqual(self.stmr.stem('Verlierer'), 'verlier')
        self.assertEqual(self.stmr.stem('Verlies'), 'verlie')
        self.assertEqual(self.stmr.stem('Maus'), 'mau')
        self.assertEqual(self.stmr.stem('Mauer'), 'mau')
        self.assertEqual(self.stmr.stem('Störsender'), 'stor')

        # additional tests to achieve full coverage
        self.assertEqual(self.stmr.stem('Müllerinnen'), 'mullerin')
        self.assertEqual(self.stmr.stem('Matrix'), 'matrix')
        self.assertEqual(self.stmr.stem('Matrizen'), 'matrix')

    def test_caumanns_lucene(self):
        """Test abydos.stemmer.Caumanns (Lucene tests).

        Based on tests from
        https://svn.apache.org/repos/asf/lucene.net/trunk/test/contrib/Analyzers/De/data.txt
        This is presumably Apache-licensed.
        """
        # German special characters are replaced:
        self.assertEqual(self.stmr.stem('häufig'), 'haufig')
        self.assertEqual(self.stmr.stem('üor'), 'uor')
        self.assertEqual(self.stmr.stem('björk'), 'bjork')

        # here the stemmer works okay, it maps related words to the same stem:
        self.assertEqual(self.stmr.stem('abschließen'), 'abschliess')
        self.assertEqual(self.stmr.stem('abschließender'), 'abschliess')
        self.assertEqual(self.stmr.stem('abschließendes'), 'abschliess')
        self.assertEqual(self.stmr.stem('abschließenden'), 'abschliess')

        self.assertEqual(self.stmr.stem('Tisch'), 'tisch')
        self.assertEqual(self.stmr.stem('Tische'), 'tisch')
        self.assertEqual(self.stmr.stem('Tischen'), 'tisch')
        self.assertEqual(self.stmr.stem('geheimtür'), 'geheimtur')

        self.assertEqual(self.stmr.stem('Haus'), 'hau')
        self.assertEqual(self.stmr.stem('Hauses'), 'hau')
        self.assertEqual(self.stmr.stem('Häuser'), 'hau')
        self.assertEqual(self.stmr.stem('Häusern'), 'hau')
        # here's a case where overstemming occurs, i.e. a word is
        # mapped to the same stem as unrelated words:
        self.assertEqual(self.stmr.stem('hauen'), 'hau')

        # here's a case where understemming occurs, i.e. two related words
        # are not mapped to the same stem. This is the case with basically
        # all irregular forms:
        self.assertEqual(self.stmr.stem('Drama'), 'drama')
        self.assertEqual(self.stmr.stem('Dramen'), 'dram')

        # replace "ß" with 'ss':
        self.assertEqual(self.stmr.stem('Ausmaß'), 'ausmass')

        # fake words to test if suffixes are cut off:
        self.assertEqual(self.stmr.stem('xxxxxe'), 'xxxxx')
        self.assertEqual(self.stmr.stem('xxxxxs'), 'xxxxx')
        self.assertEqual(self.stmr.stem('xxxxxn'), 'xxxxx')
        self.assertEqual(self.stmr.stem('xxxxxt'), 'xxxxx')
        self.assertEqual(self.stmr.stem('xxxxxem'), 'xxxxx')
        self.assertEqual(self.stmr.stem('xxxxxer'), 'xxxxx')
        self.assertEqual(self.stmr.stem('xxxxxnd'), 'xxxxx')
        # the suffixes are also removed when combined:
        self.assertEqual(self.stmr.stem('xxxxxetende'), 'xxxxx')

        # words that are shorter than four charcters are not changed:
        self.assertEqual(self.stmr.stem('xxe'), 'xxe')
        # -em and -er are not removed from words shorter than five characters:
        self.assertEqual(self.stmr.stem('xxem'), 'xxem')
        self.assertEqual(self.stmr.stem('xxer'), 'xxer')
        # -nd is not removed from words shorter than six characters:
        self.assertEqual(self.stmr.stem('xxxnd'), 'xxxnd')


if __name__ == '__main__':
    unittest.main()
