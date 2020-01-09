# -*- coding: utf-8 -*-

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

"""abydos.tests.distance.test_distance_softtf_idf.

This module contains unit tests for abydos.distance.SoftTFIDF
"""

import os
import unittest

from abydos.corpus import UnigramCorpus
from abydos.distance import Levenshtein, SoftTFIDF
from abydos.tokenizer import QGrams
from abydos.util import download_package, package_path

from six import PY2


class SoftTFIDFTestCases(unittest.TestCase):
    """Test SoftTFIDF functions.

    abydos.distance.SoftTFIDF
    """

    cmp = SoftTFIDF()
    cmp_lev = SoftTFIDF(metric=Levenshtein())

    def test_softtf_idf_sim(self):
        """Test abydos.distance.SoftTFIDF.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.304044497)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.304044497)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.304044497)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.304044497)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.4676712137
        )

        self.assertAlmostEqual(self.cmp_lev.sim('Nigel', 'Niall'), 0.304044497)
        self.assertAlmostEqual(self.cmp_lev.sim('Niall', 'Nigel'), 0.304044497)
        self.assertAlmostEqual(self.cmp_lev.sim('Colin', 'Coiln'), 0.304044497)
        self.assertAlmostEqual(self.cmp_lev.sim('Coiln', 'Colin'), 0.304044497)
        self.assertAlmostEqual(
            self.cmp_lev.sim('ATCAACGAGT', 'AACGATTAG'), 0.4676712137
        )

    def test_softtf_idf_dist(self):
        """Test abydos.distance.SoftTFIDF.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 1.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.695955503)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.695955503)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.695955503)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.695955503)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.5323287863
        )

    def test_softtf_idf_corpus(self):
        """Test abydos.distance.SoftTFIDF.sim & .dist with corpus."""
        if PY2:  # disable testing in Py2.7; the pickled data isn't supported
            return

        download_package('en_qgram', silent=True)

        q3_corpus = UnigramCorpus(word_tokenizer=QGrams(qval=3))
        q3_corpus.load_corpus(
            os.path.join(package_path('en_qgram'), 'q3_en.dat')
        )
        cmp_q3_08 = SoftTFIDF(
            tokenizer=QGrams(qval=3), corpus=q3_corpus, threshold=0.8
        )
        cmp_q3_03 = SoftTFIDF(
            tokenizer=QGrams(qval=3), corpus=q3_corpus, threshold=0.3
        )

        self.assertAlmostEqual(cmp_q3_08.sim('Nigel', 'Niall'), 0.608842672)
        self.assertAlmostEqual(cmp_q3_08.sim('Niall', 'Nigel'), 0.608842672)
        self.assertAlmostEqual(cmp_q3_08.sim('Colin', 'Coiln'), 0.383052250)
        self.assertAlmostEqual(cmp_q3_08.sim('Coiln', 'Colin'), 0.383052250)

        # These values won't be stable, so we just use Greater/Less
        self.assertGreater(cmp_q3_03.sim('Nigel', 'Niall'), 0.5)
        self.assertGreater(cmp_q3_03.sim('Niall', 'Nigel'), 0.5)
        self.assertGreater(cmp_q3_03.sim('Colin', 'Coiln'), 0.5)
        self.assertGreater(cmp_q3_03.sim('Coiln', 'Colin'), 0.5)

        self.assertAlmostEqual(cmp_q3_08.dist('Nigel', 'Niall'), 0.391157328)
        self.assertAlmostEqual(cmp_q3_08.dist('Niall', 'Nigel'), 0.391157328)
        self.assertAlmostEqual(cmp_q3_08.dist('Colin', 'Coiln'), 0.616947750)
        self.assertAlmostEqual(cmp_q3_08.dist('Coiln', 'Colin'), 0.616947750)

        # These values won't be stable, so we just use Greater/Less
        self.assertLess(cmp_q3_03.dist('Nigel', 'Niall'), 0.5)
        self.assertLess(cmp_q3_03.dist('Niall', 'Nigel'), 0.5)
        self.assertLess(cmp_q3_03.dist('Colin', 'Coiln'), 0.5)
        self.assertLess(cmp_q3_03.dist('Coiln', 'Colin'), 0.5)


if __name__ == '__main__':
    unittest.main()
