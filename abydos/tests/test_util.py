# -*- coding: utf-8 -*-
"""abydos.tests.test_util

This module contains unit tests for abydos.util

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from abydos._compat import _range
from abydos.util import prod, jitter, ac_train, ac_encode
import unittest

NIALL = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel', 'Nele',
         'Nigelli', 'Nel', 'Kneale', 'Uí Néill', 'O\'Neill', 'MacNeil',
         'MacNele', 'Niall Noígíallach')

class ProdTestCases(unittest.TestCase):
    """test cases for abydos.util.prod
    """
    def test_prod(self):
        """test abydos.util.prod
        """
        self.assertEqual(prod([]), 1)
        self.assertEqual(prod(tuple()), 1)
        self.assertEqual(prod(set()), 1)

        self.assertEqual(prod([1, 1, 1, 1, 1]), 1)
        self.assertEqual(prod((1, 1, 1, 1, 1)), 1)
        self.assertEqual(prod(set([1, 1, 1, 1, 1])), 1)

        self.assertEqual(prod([2, 2, 2, 2, 2]), 32)
        self.assertEqual(prod((2, 2, 2, 2, 2)), 32)
        self.assertEqual(prod(set([2, 2, 2, 2, 2])), 2)

        self.assertEqual(prod([1, 2, 3, 4, 5]), 120)
        self.assertEqual(prod((1, 2, 3, 4, 5)), 120)
        self.assertEqual(prod(set([1, 2, 3, 4, 5])), 120)
        self.assertEqual(prod(_range(1, 6)), 120)
        self.assertEqual(prod(list(_range(1, 6))), 120)
        self.assertEqual(prod(tuple(_range(1, 6))), 120)
        self.assertEqual(prod(set(_range(1, 6))), 120)

        self.assertEqual(prod(_range(6)), 0)
        self.assertEqual(prod(list(_range(6))), 0)
        self.assertEqual(prod(tuple(_range(6))), 0)
        self.assertEqual(prod(set(_range(6))), 0)


class JitterTestCases(unittest.TestCase):
    """test cases for abydos.util.jitter
    """
    def test_jitter(self):
        """test abydos.util.jitter
        """
        self.assertEqual(jitter([]), [])
        self.assertEqual(jitter(tuple()), [])
        self.assertTrue(isinstance(jitter(5), float))
        self.assertTrue(isinstance(jitter([5]), list))
        self.assertEqual(len(jitter([1, 2, 3])), 3)
        self.assertEqual(len(jitter([0, 0, 0])), 3)
        self.assertEqual(len(jitter([0, 0, 0, 0, 0])), 5)
        self.assertEqual(len(jitter((0, 0, 0, 0, 0))), 5)
        self.assertEqual(len(jitter(set([1, 2, 3, 4, 5]))), 5)
        self.assertEqual(len(jitter(_range(5))), 5)
        self.assertRaises(AttributeError, jitter, ['a'])
        self.assertRaises(AttributeError, jitter, [1, 2, 3, 'a', 4])
        self.assertRaises(AttributeError, jitter, [0, 0, 0, 'a', 0])
        self.assertRaises(AttributeError, jitter, [0, 1], min_val=0.5)
        self.assertRaises(AttributeError, jitter, [0, 1], max_val=0.5)
        self.assertEqual(len(jitter([0]*5, 1, 0)), 5)
        self.assertEqual(len(jitter([0]*5, rfunc='uniform')), 5)
        self.assertEqual(len(jitter([0]*5, rfunc='normal')), 5)
        self.assertEqual(len(jitter([0]*5, rfunc='laplace')), 5)


class ArithmeticCoderTestCases(unittest.TestCase):
    """test cases for abydos.util.ac_train & abydos.util.ac_encode
    niall_probs = {'\x00': (R(0), R(1, 119)), '\xa1': (R(1/119), R(2/119)),
                   ' ': (R(2/119), R(19/119)), "'": (R(19/119), R(20/119)),
                   '\xa9': (R(20/119), R(3/17)), '\xad': (R(3/17), R(24/119)),
                   '\xc3': (R(24/119), R(29/119)), 'K': (R(29/119), R(30/119)),
                   'M': (R(30/119), R(32/119)), 'O': (R(32/119), R(33/119)),
                   'N': (R(33/119), R(7/17)), 'U': (R(7/17), R(50/119)),
                   'a': (R(50/119), R(59/119)), 'c': (R(59/119), R(62/119)),
                   'e': (R(62/119), R(11/17)), 'g': (R(11/17), R(80/119)),
                   'i': (R(80/119), R(89/119)), 'h': (R(89/119), R(90/119)),
                   'j': (R(90/119), R(92/119)), 'l': (R(92/119), R(117/119)),
                   'o': (R(117/119), R(118/119)), 'n': (R(118/119), R(1))}
    """

    def test_ac_train(self):
        """test abydos.util.ac_train
        """
        #self.assertEqual(ac_train(''), {'\x00': (0, 1)})
        #self.assertEqual(ac_train(' '.join(NIALL)), self.niall_probs)
        #self.assertEqual(ac_train(' '.join(sorted(NIALL))), self.niall_probs)
        #self.assertEqual(ac_train(' '.join(NIALL)),
        #                 ac_train(' '.join(sorted(NIALL))))
        #self.assertEqual(ac_train(' '.join(NIALL)),
        #                 ac_train('\x00'.join(NIALL)))

    def test_ac_encode(self):
        """test abydos.util.ac_encode
        """
        #self.assertEqual(ac_encode('', self.niall_probs), (1, 8L))
        #self.assertEqual(ac_encode('a', self.niall_probs), (1722, 12L))
        #self.assertEqual(ac_encode('Niall', self.niall_probs), (3126369, 23L))
        #self.assertEqual(ac_encode('Niel', self.niall_probs), (392157, 20L))
        #self.assertEqual(ac_encode('Mean', self.niall_probs), (70304934, 28L))
        #self.assertEqual(ac_encode('Neil Noígíallach', self.niall_probs),
        #                 (1739727914825858776309937L, 82L))
        #self.assertRaise(KeyError, ac_encode, 'NIALL', self.niall_probs) 


if __name__ == '__main__':
    unittest.main()
