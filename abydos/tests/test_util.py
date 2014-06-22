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

from __future__ import unicode_literals
from abydos._compat import _range, _long
from abydos.util import prod, jitter, Rational, ac_train, ac_encode, ac_decode
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
    half_9 = Rational(_long(1), 2)
    half_A = Rational(2.0, _long(4))

    third = Rational(1, 3)
    twosevenths = Rational(2, 7)
    twosevenths_alt = Rational(14, 49)
    sevenhalves = Rational(7, 2)
    seven = Rational(7)

    def test_rational_init(self):
        """test abydos.util.Rational constructor and getters
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

        self.assertEqual(self.twosevenths.numerator(), 2)
        self.assertEqual(self.twosevenths.denominator(), 7)
        self.assertEqual(self.seven.numerator(), 7)
        self.assertEqual(self.seven.denominator(), 1)

    def test_rational_helpers(self):
        """test abydos.util.Rational helper functions
        (_gcd & _simplify)
        """
        # pylint: disable=protected-access
        self.assertEqual(Rational()._gcd(2, 7), 1)
        self.assertEqual(Rational(2, 7)._gcd(), 1)
        self.assertEqual(Rational()._gcd(3, 18), 3)
        self.assertEqual(Rational(3, 18)._gcd(), 1)
        self.assertEqual(Rational()._gcd(2, 4), 2)
        self.assertEqual(Rational(2, 4)._gcd(), 1)
        self.assertEqual(Rational()._gcd(1, 7), 1)
        self.assertEqual(Rational(1, 7)._gcd(), 1)
        self.assertEqual(Rational()._gcd(54, 7), 1)
        self.assertEqual(Rational(54, 7)._gcd(), 1)
        self.assertEqual(Rational()._gcd(49, 21), 7)
        self.assertEqual(Rational(49, 21)._gcd(), 1)

        self.assertEqual(Rational(49, 21)._gcd(p=1), 1)
        self.assertEqual(Rational(49, 21)._gcd(q=1), 1)

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
        # negation
        self.assertEqual(Rational(1), -Rational(-1))
        self.assertEqual(-Rational(1), Rational(-1))
        self.assertEqual(-self.third, -Rational(1, 3))
        self.assertEqual(-Rational(1, 3), -self.third)
        self.assertEqual(self.third, -Rational(-1, 3))
        self.assertEqual(-Rational(-1, 3), self.third)

        # +
        self.assertEqual(self.half_1+self.half_2, Rational(1))
        self.assertEqual(self.half_1+0.5, Rational(1))
        self.assertEqual(0.5+self.half_1, Rational(1))
        self.assertEqual(self.sevenhalves+self.half_1, Rational(4))
        self.assertEqual(self.half_1+self.sevenhalves, Rational(4))
        self.assertEqual(self.sevenhalves+0.5, Rational(4))
        self.assertEqual(0.5+self.sevenhalves, Rational(4))
        self.assertEqual(Rational(3)+2, Rational(5))
        self.assertEqual(2+Rational(3), Rational(5))

        # -
        self.assertEqual(self.half_1-self.half_2, Rational(0))
        self.assertEqual(self.half_1-0.5, Rational(0))
        self.assertEqual(0.5-self.half_1, Rational(0))
        self.assertEqual(self.sevenhalves-self.half_1, Rational(3))
        self.assertEqual(self.half_1-self.sevenhalves, Rational(-3))
        self.assertEqual(self.sevenhalves-0.5, Rational(3))
        self.assertEqual(0.5-self.sevenhalves, Rational(-3))
        self.assertEqual(Rational(3)-2, Rational(1))
        self.assertEqual(2-Rational(3), Rational(-1))

        # *
        self.assertEqual(self.half_1*self.half_2, Rational(1, 4))
        self.assertEqual(self.half_1*0.5, Rational(1, 4))
        self.assertEqual(0.5*self.half_1, Rational(1, 4))
        self.assertEqual(self.sevenhalves*self.half_1, Rational(7, 4))
        self.assertEqual(self.half_1*self.sevenhalves, Rational(7, 4))
        self.assertEqual(self.sevenhalves*0.5, Rational(7, 4))
        self.assertEqual(0.5*self.sevenhalves, Rational(7, 4))
        self.assertEqual(Rational(3)*2, Rational(6))
        self.assertEqual(2*Rational(3), Rational(6))

        # /
        self.assertEqual(self.half_1/self.half_2, Rational(1))
        self.assertEqual(self.half_1/0.5, Rational(1))
        self.assertEqual(0.5/self.half_1, Rational(1))
        self.assertEqual(self.sevenhalves/self.half_1, self.seven)
        self.assertEqual(self.half_1/self.sevenhalves, Rational(1, 7))
        self.assertEqual(self.sevenhalves/0.5, self.seven)
        self.assertEqual(0.5/self.sevenhalves, Rational(1, 7))
        self.assertEqual(Rational(3)/2, Rational(3, 2))
        self.assertEqual(2/Rational(3), Rational(2, 3))

        # **
        self.assertEqual(Rational(1, 2)**2, Rational(1, 4))
        self.assertEqual(Rational(2, 3)**3, Rational(8, 27))
        self.assertEqual(Rational(3)**0, Rational(1))
        self.assertEqual(Rational(0)**2, Rational(0))
        self.assertEqual(Rational(3)**2, Rational(9))
        self.assertEqual(2**Rational(3), Rational(8))
        self.assertEqual(Rational(1, 2)**2.0, Rational(1, 4))
        self.assertEqual(Rational(2, 3)**3.0, Rational(8, 27))
        self.assertEqual(Rational(3)**0.0, Rational(1))
        self.assertEqual(Rational(0)**2.0, Rational(0))
        self.assertEqual(Rational(3)**2.0, Rational(9))
        self.assertEqual(2.0**Rational(3), Rational(8))

        # <<
        self.assertEqual(Rational(1, 2)<<1, Rational(1))
        self.assertEqual(Rational(1, 2)<<2, Rational(2))
        self.assertEqual(Rational(1, 3)<<1, Rational(2, 3))
        self.assertEqual(Rational(1, 3)<<2, Rational(4, 3))
        self.assertEqual(Rational(2, 5)<<1, Rational(4, 5))
        self.assertEqual(Rational(2, 5)<<2, Rational(8, 5))

        # >>
        self.assertEqual(Rational(1, 2)>>1, Rational(1, 4))
        self.assertEqual(Rational(1, 2)>>2, Rational(1, 8))
        self.assertEqual(Rational(1, 3)>>1, Rational(1, 6))
        self.assertEqual(Rational(1, 3)>>2, Rational(1, 12))
        self.assertEqual(Rational(2, 5)>>1, Rational(1, 5))
        self.assertEqual(Rational(2, 5)>>2, Rational(1, 10))

    def test_rational_casts(self):
        """test abydos.util.Rational cast functions
        (int, float, str, __repr__)
        """
        # int
        self.assertEqual(int(Rational(1, 4)), 0)
        self.assertEqual(int(Rational(1, 3)), 0)
        self.assertEqual(int(Rational(1, 2)), 0)
        self.assertEqual(int(Rational(1)), 1)
        self.assertEqual(int(Rational(2)), 2)
        self.assertEqual(int(Rational(5, 2)), 2)

        # float
        self.assertEqual(float(Rational(1, 4)), 0.25)
        self.assertAlmostEqual(float(Rational(1, 3)), 0.33333333)
        self.assertEqual(float(Rational(1, 2)), 0.5)
        self.assertEqual(float(Rational(1)), 1.0)
        self.assertEqual(float(Rational(2)), 2.0)
        self.assertEqual(float(Rational(5, 2)), 2.5)

        # str
        self.assertEqual(str(Rational(1, 4)), '1/4')
        self.assertEqual(str(Rational(1, 3)), '1/3')
        self.assertEqual(str(Rational(1, 2)), '1/2')
        self.assertEqual(str(Rational(1)), '1/1')
        self.assertEqual(str(Rational(2)), '2/1')
        self.assertEqual(str(Rational(5, 2)), '5/2')

        # __repr__
        self.assertEqual(Rational(1, 4).__repr__(), '1/4')
        self.assertEqual(Rational(1, 3).__repr__(), '1/3')
        self.assertEqual(Rational(1, 2).__repr__(), '1/2')
        self.assertEqual(Rational(1).__repr__(), '1/1')
        self.assertEqual(Rational(2).__repr__(), '2/1')
        self.assertEqual(Rational(5, 2).__repr__(), '5/2')


class ArithmeticCoderTestCases(unittest.TestCase):
    """test cases for abydos.util.ac_train & abydos.util.ac_encode
    """
    niall_probs = {'a': (Rational(41, 57), Rational(91, 114)),
                   ' ': (Rational(25, 114), Rational(7, 19)),
                   'c': (Rational(97, 114), Rational(50, 57)),
                   'e': (Rational(29, 57), Rational(73, 114)),
                   "'": (Rational(56, 57), Rational(113, 114)),
                   'g': (Rational(47, 57), Rational(97, 114)),
                   '\x00': (Rational(113, 114), Rational(1, 1)),
                   'i': (Rational(73, 114), Rational(41, 57)),
                   'M': (Rational(17, 19), Rational(52, 57)),
                   'K': (Rational(37, 38), Rational(56, 57)),
                   'j': (Rational(50, 57), Rational(17, 19)),
                   '\xed': (Rational(91, 114), Rational(47, 57)),
                   'l': (Rational(0, 1), Rational(25, 114)),
                   'o': (Rational(53, 57), Rational(107, 114)),
                   'N': (Rational(7, 19), Rational(29, 57)),
                   '\xe9': (Rational(52, 57), Rational(35, 38)),
                   '\xe1': (Rational(35, 38), Rational(53, 57)),
                   'U': (Rational(109, 114), Rational(55, 57)),
                   'O': (Rational(55, 57), Rational(37, 38)),
                   'h': (Rational(18, 19), Rational(109, 114)),
                   'n': (Rational(107, 114), Rational(18, 19))}

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
        self.assertEqual(ac_encode('', self.niall_probs), (254, 8))
        self.assertEqual(ac_encode('a', self.niall_probs), (3268, 12))
        self.assertEqual(ac_encode('Niall', self.niall_probs), (3911665, 23))
        self.assertEqual(ac_encode('Niel', self.niall_probs), (486801, 20))
        self.assertEqual(ac_encode('Mean', self.niall_probs), (243067161, 28))
        self.assertEqual(ac_encode('Neil Noígíallach', self.niall_probs),
                         (2133315320471368785758, 72))
        self.assertRaises(KeyError, ac_encode, 'NIALL', self.niall_probs)

    def test_ac_decode(self):
        """test abydos.util.ac_decode
        """
        self.assertEqual(ac_decode(254, 8, self.niall_probs), '')
        self.assertEqual(ac_decode(3268, 12, self.niall_probs), 'a')
        self.assertEqual(ac_decode(3911665, 23, self.niall_probs), 'Niall')
        self.assertEqual(ac_decode(486801, 20, self.niall_probs), 'Niel')
        self.assertEqual(ac_decode(243067161, 28, self.niall_probs), 'Mean')
        self.assertEqual(ac_decode(2133315320471368785758, 72,
                                   self.niall_probs), 'Neil Noígíallach')


if __name__ == '__main__':
    unittest.main()
