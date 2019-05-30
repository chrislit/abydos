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

"""abydos.tests.distance.test_distance_meta_levenshtein.

This module contains unit tests for abydos.distance.MetaLevenshtein
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
from abydos.distance import Jaccard, MetaLevenshtein
from abydos.tokenizer import QGrams
from abydos.util import download_package, package_path

from six import PY2


class MetaLevenshteinTestCases(unittest.TestCase):
    """Test MetaLevenshtein functions.

    abydos.distance.MetaLevenshtein
    """

    cmp = MetaLevenshtein()
    cmp_jac1 = MetaLevenshtein(metric=Jaccard(qval=1))

    def test_meta_levenshtein_dist(self):
        """Test abydos.distance.MetaLevenshtein.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.8463953614713058)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.3077801314)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.3077801314)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.3077801314)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.3077801314)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.2931752664
        )

    def test_meta_levenshtein_sim(self):
        """Test abydos.distance.MetaLevenshtein.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.15360463852869422)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6922198686)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6922198686)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6922198686)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6922198686)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.7068247336
        )

        self.assertAlmostEqual(
            self.cmp_jac1.sim('Nigel', 'Niall'), 0.569107816
        )
        self.assertAlmostEqual(
            self.cmp_jac1.sim('Niall', 'Nigel'), 0.569107816
        )
        self.assertAlmostEqual(
            self.cmp_jac1.sim('Colin', 'Coiln'), 0.753775895
        )
        self.assertAlmostEqual(
            self.cmp_jac1.sim('Coiln', 'Colin'), 0.753775895
        )
        self.assertAlmostEqual(
            self.cmp_jac1.sim('ATCAACGAGT', 'AACGATTAG'), 0.5746789477
        )

    def test_meta_levenshtein_dist_abs(self):
        """Test abydos.distance.MetaLevenshtein.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 3.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 3.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 3.385581445885223)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 1.5389006572
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 1.5389006572
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 1.5389006572
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 1.5389006572
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 2.9317526638
        )

    def test_meta_levenshtein_corpus(self):
        """Test abydos.distance.MetaLevenshtein with corpus."""
        if PY2:  # disable testing in Py2.7; the pickled data isn't supported
            return

        q3_corpus = UnigramCorpus(word_tokenizer=QGrams(qval=3))
        download_package('en_qgram', silent=True)
        q3_corpus.load_corpus(
            os.path.join(package_path('en_qgram'), 'q3_en.dat')
        )
        cmp_q3 = MetaLevenshtein(tokenizer=QGrams(qval=3), corpus=q3_corpus)

        self.assertAlmostEqual(cmp_q3.dist_abs('Nigel', 'Niall'), 7.378939370)
        self.assertAlmostEqual(cmp_q3.dist_abs('Niall', 'Nigel'), 7.378939370)
        self.assertAlmostEqual(cmp_q3.dist_abs('Colin', 'Coiln'), 8.0)
        self.assertAlmostEqual(cmp_q3.dist_abs('Coiln', 'Colin'), 8.0)

        self.assertAlmostEqual(cmp_q3.dist('Nigel', 'Niall'), 0.527067098)
        self.assertAlmostEqual(cmp_q3.dist('Niall', 'Nigel'), 0.527067098)
        self.assertAlmostEqual(cmp_q3.dist('Colin', 'Coiln'), 0.571428571)
        self.assertAlmostEqual(cmp_q3.dist('Coiln', 'Colin'), 0.571428571)

        self.assertAlmostEqual(cmp_q3.sim('Nigel', 'Niall'), 0.472932902)
        self.assertAlmostEqual(cmp_q3.sim('Niall', 'Nigel'), 0.472932902)
        self.assertAlmostEqual(cmp_q3.sim('Colin', 'Coiln'), 0.428571429)
        self.assertAlmostEqual(cmp_q3.sim('Coiln', 'Colin'), 0.428571429)


if __name__ == '__main__':
    unittest.main()
