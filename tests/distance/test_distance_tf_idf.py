# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_tf_idf.

This module contains unit tests for abydos.distance.TFIDF
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
import unittest

from abydos.corpus import UnigramCorpus
from abydos.distance import TFIDF
from abydos.tokenizer import QGrams
from abydos.util import download_package, package_path

from six import PY2


class TFIDFTestCases(unittest.TestCase):
    """Test TFIDF functions.

    abydos.distance.TFIDF
    """

    cmp = TFIDF()

    def test_tf_idf_sim(self):
        """Test abydos.distance.TFIDF.sim."""
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

    def test_tf_idf_dist(self):
        """Test abydos.distance.TFIDF.dist."""
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

    def test_tf_idf_corpus(self):
        """Test abydos.distance.TFIDF.sim & .dist with corpus."""
        if PY2:  # disable testing in Py2.7; the pickled data isn't supported
            return

        q3_corpus = UnigramCorpus(word_tokenizer=QGrams(qval=3))
        download_package('en_qgram', silent=True)
        q3_corpus.load_corpus(
            os.path.join(package_path('en_qgram'), 'q3_en.dat')
        )
        cmp_q3 = TFIDF(tokenizer=QGrams(qval=3), corpus=q3_corpus)

        self.assertAlmostEqual(cmp_q3.sim('Nigel', 'Niall'), 0.259985047)
        self.assertAlmostEqual(cmp_q3.sim('Niall', 'Nigel'), 0.259985047)
        self.assertAlmostEqual(cmp_q3.sim('Colin', 'Coiln'), 0.114867563)
        self.assertAlmostEqual(cmp_q3.sim('Coiln', 'Colin'), 0.114867563)

        self.assertAlmostEqual(cmp_q3.dist('Nigel', 'Niall'), 0.740014953)
        self.assertAlmostEqual(cmp_q3.dist('Niall', 'Nigel'), 0.740014953)
        self.assertAlmostEqual(cmp_q3.dist('Colin', 'Coiln'), 0.885132437)
        self.assertAlmostEqual(cmp_q3.dist('Coiln', 'Colin'), 0.885132437)


if __name__ == '__main__':
    unittest.main()
