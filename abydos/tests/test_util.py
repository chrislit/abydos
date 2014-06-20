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
from abydos.util import prod, jitter, Rational, ac_train, ac_encode
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

class RationalTestCases(unittest.TestCase):
    """test cases for the abydos.util.Rational class
    """
    half_1 = Rational('1/2')
    half_2 = Rational(1, 2)
    half_3 = Rational('0.5')
    half_4 = Rational(0.5)
    half_5 = Rational(6, 12)
    half_6 = Rational(0.25, 0.5)
    half_7 = Rational('1 / 2')
    half_8 = Rational('2.5 /5.0')
    half_9 = Rational(long(1), 2)
    half_A = Rational(2.0, long(4))

    third = Rational(1, 3)
    twosevenths = Rational(2, 7)
    twosevenths_alt = Rational(14, 49)
    sevenhalves = Rational(7, 2)
    seven = Rational(7)

    def test_rational_init(self):
        """test abydos.util.Rational constructor
        """
        self.assertEqual(self.half_1, self.half_2)
        self.assertEqual(self.half_3, self.half_4)
        self.assertEqual(self.half_5, self.half_6)
        self.assertEqual(self.half_7, self.half_8)
        self.assertEqual(self.half_9, self.half_A)
        self.assertEqual(self.half_1, self.half_3)
        self.assertEqual(self.half_5, self.half_7)
        self.assertEqual(self.half_3, self.half_5)
        self.assertEqual(self.half_1, self.half_9)

        self.assertEqual(self.twosevenths, self.twosevenths_alt)

    def test_rational_helpers(self):
        """test abydos.util.Rational helper functions
        (_gcd & _simplify)
        """
        self.assertEqual(Rational()._gcd(2, 7), 1)
        self.assertEqual(Rational()._gcd(3, 18), 3)
        self.assertEqual(Rational()._gcd(2, 4), 2)
        self.assertEqual(Rational()._gcd(1, 7), 1)
        self.assertEqual(Rational()._gcd(54, 7), 1)
        self.assertEqual(Rational()._gcd(49, 21), 7)

        # Create a default Rational (0), set p & q manually, without simplifying
        rat_twothirds = Rational()
        rat_twothirds.p = 10
        rat_twothirds.q = 15
        # It should not be equal to a numerically equal Rational
        self.assertNotEqual(Rational(2, 3), rat_twothirds)
        # After simplification, it should become equal to the same Rational
        rat_twothirds._simplify()
        self.assertEqual(Rational(2, 3), rat_twothirds)

    def test_rational_comparisons(self):
        """test abydos.util.Rational comparison operators
        (==, !=, <, <=, >, >=)
        """
        # ==
        self.assertTrue(self.half_1 == self.half_2)
        self.assertFalse(self.third == self.twosevenths)
        self.assertFalse(self.twosevenths == self.third)
        self.assertFalse(0.3333333 == self.twosevenths)
        self.assertFalse(self.twosevenths == 0.3333333)
        self.assertTrue(7 == self.seven)
        self.assertTrue(7.0 == self.seven)
        self.assertTrue(self.seven == 7)
        self.assertTrue(self.seven == 7.0)
        self.assertFalse(self.sevenhalves == 4)
        self.assertFalse(4 == self.sevenhalves)

        # !=
        self.assertFalse(self.half_1 != self.half_2)
        self.assertTrue(self.third != self.twosevenths)
        self.assertTrue(self.twosevenths != self.third)
        self.assertTrue(0.3333333 != self.twosevenths)
        self.assertTrue(self.twosevenths != 0.3333333)
        self.assertFalse(7 != self.seven)
        self.assertFalse(7.0 != self.seven)
        self.assertFalse(self.seven != 7)
        self.assertFalse(self.seven != 7.0)
        self.assertTrue(self.sevenhalves != 4)
        self.assertTrue(4 != self.sevenhalves)

        # <
        self.assertFalse(self.half_1 < self.half_2)
        self.assertFalse(self.third < self.twosevenths)
        self.assertTrue(self.twosevenths < self.third)
        self.assertFalse(0.3333333 < self.twosevenths)
        self.assertTrue(self.twosevenths < 0.3333333)
        self.assertFalse(7 < self.seven)
        self.assertFalse(7.0 < self.seven)
        self.assertFalse(self.seven < 7)
        self.assertFalse(self.seven < 7.0)
        self.assertTrue(self.sevenhalves < 4)
        self.assertFalse(4 < self.sevenhalves)

        # <=
        self.assertTrue(self.half_1 <= self.half_2)
        self.assertFalse(self.third <= self.twosevenths)
        self.assertTrue(self.twosevenths <= self.third)
        self.assertFalse(0.3333333 <= self.twosevenths)
        self.assertTrue(self.twosevenths <= 0.3333333)
        self.assertTrue(7 <= self.seven)
        self.assertTrue(7.0 <= self.seven)
        self.assertTrue(self.seven <= 7)
        self.assertTrue(self.seven <= 7.0)
        self.assertTrue(self.sevenhalves <= 4)
        self.assertFalse(4 <= self.sevenhalves)

        # >
        self.assertFalse(self.half_1 > self.half_2)
        self.assertTrue(self.third > self.twosevenths)
        self.assertFalse(self.twosevenths > self.third)
        self.assertTrue(0.3333333 > self.twosevenths)
        self.assertFalse(self.twosevenths > 0.3333333)
        self.assertFalse(7 > self.seven)
        self.assertFalse(7.0 > self.seven)
        self.assertFalse(self.seven > 7)
        self.assertFalse(self.seven > 7.0)
        self.assertFalse(self.sevenhalves > 4)
        self.assertTrue(4 > self.sevenhalves)

        # >=
        self.assertTrue(self.half_1 >= self.half_2)
        self.assertTrue(self.third >= self.twosevenths)
        self.assertFalse(self.twosevenths >= self.third)
        self.assertTrue(0.3333333 >= self.twosevenths)
        self.assertFalse(self.twosevenths >= 0.3333333)
        self.assertTrue(7 >= self.seven)
        self.assertTrue(7.0 >= self.seven)
        self.assertTrue(self.seven >= 7)
        self.assertTrue(self.seven >= 7.0)
        self.assertFalse(self.sevenhalves >= 4)
        self.assertTrue(4 >= self.sevenhalves)

    def test_rational_arithmetic(self):
        """test abydos.util.Rational arithmetic operators
        (negation, +, -, *, / (future & non), **, <<, >>)
        """
        pass

    def test_rational_casts(self):
        """test abydos.util.Rational cast functions
        (int, float, str, __repr__)
        """
        pass


class ArithmeticCoderTestCases(unittest.TestCase):
    """test cases for abydos.util.ac_train & abydos.util.ac_encode
    """
    niall_probs = {'\x00': (Rational(0), Rational(1, 119)),
                   '\xa1': (Rational(1, 119), Rational(2, 119)),
                   ' ': (Rational(2, 119), Rational(19, 119)),
                   "'": (Rational(19, 119), Rational(20, 119)),
                   '\xa9': (Rational(20, 119), Rational(3, 17)),
                   '\xad': (Rational(3, 17), Rational(24, 119)),
                   '\xc3': (Rational(24, 119), Rational(29, 119)),
                   'K': (Rational(29, 119), Rational(30, 119)),
                   'M': (Rational(30, 119), Rational(32, 119)),
                   'O': (Rational(32, 119), Rational(33, 119)),
                   'N': (Rational(33, 119), Rational(7, 17)),
                   'U': (Rational(7, 17), Rational(50, 119)),
                   'a': (Rational(50, 119), Rational(59, 119)),
                   'c': (Rational(59, 119), Rational(62, 119)),
                   'e': (Rational(62, 119), Rational(11, 17)),
                   'g': (Rational(11, 17), Rational(80, 119)),
                   'i': (Rational(80, 119), Rational(89, 119)),
                   'h': (Rational(89, 119), Rational(90, 119)),
                   'j': (Rational(90, 119), Rational(92, 119)),
                   'l': (Rational(92, 119), Rational(117, 119)),
                   'o': (Rational(117, 119), Rational(118, 119)),
                   'n': (Rational(118, 119), Rational(1))}

    def test_ac_train(self):
        """test abydos.util.ac_train
        """
        self.assertEqual(ac_train(''), {'\x00': (0, 1)})
        self.assertEqual(ac_train(' '.join(NIALL)), self.niall_probs)
        self.assertEqual(ac_train(' '.join(sorted(NIALL))), self.niall_probs)
        self.assertEqual(ac_train(' '.join(NIALL)),
                         ac_train(' '.join(sorted(NIALL))))
        self.assertEqual(ac_train(' '.join(NIALL)),
                         ac_train('\x00'.join(NIALL)))

    def test_ac_encode(self):
        """test abydos.util.ac_encode
        """
        #self.assertEqual(ac_encode('', self.niall_probs), (1, 8L))
        self.assertEqual(ac_encode('a', self.niall_probs), (1722, 12L))
        self.assertEqual(ac_encode('Niall', self.niall_probs), (3126369, 23L))
        self.assertEqual(ac_encode('Niel', self.niall_probs), (392157, 20L))
        self.assertEqual(ac_encode('Mean', self.niall_probs), (70304934, 28L))
        self.assertEqual(ac_encode('Neil Noígíallach', self.niall_probs),
                         (1739727914825858776309937L, 82L))
        self.assertRaises(KeyError, ac_encode, 'NIALL', self.niall_probs)


if __name__ == '__main__':
    unittest.main()
