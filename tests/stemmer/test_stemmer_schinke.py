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

"""abydos.tests.stemmer.test_stemmer_schinke.

This module contains unit tests for abydos.stemmer.Schinke
"""

import unittest

from abydos.stemmer import Schinke

from .. import _corpus_file


class SchinkeTestCases(unittest.TestCase):
    """Test Schinke functions.

    abydos.stemmer.Schinke
    """

    stmr = Schinke()

    def test_schinke(self):
        """Test abydos.stemmer.Schinke.

        These tests are copied from the Snowball testset at
        http://snowball.tartarus.org/otherapps/schinke/schinke.tgz
        """
        with open(_corpus_file('snowball_schinke.csv')) as schinke_ts:
            for schinke_line in schinke_ts:
                word, noun, verb = schinke_line.strip().split(',')
                nv = self.stmr.stem_dict(word)
                self.assertEqual(nv['n'], noun)
                self.assertEqual(nv['v'], verb)
                nv = self.stmr.stem(word)
                self.assertEqual(nv, '{},{}'.format(noun, verb))


if __name__ == '__main__':
    unittest.main()
