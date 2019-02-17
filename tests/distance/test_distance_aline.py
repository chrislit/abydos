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

"""abydos.tests.distance.test_distance_aline.

This module contains unit tests for abydos.distance.ALINE
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ALINE


class ALINETestCases(unittest.TestCase):
    """Test ALINE functions.

    abydos.distance.ALINE
    """

    cmp = ALINE()

    def test_aline_alignment(self):
        """Test abydos.distance.ALINE.alignment."""
        # test cases from Kondrak (2000)
        self.assertEqual(
            self.cmp.alignment('driy', 'tres'),
            [(70.0, '‖ d r iy ‖', '‖ t r e  ‖ s')],
        )
        self.assertEqual(
            self.cmp.alignment('blow', 'flare'),
            [(53.0, '‖ b l o ‖ w', '‖ f l a ‖ re')],
        )
        self.assertEqual(
            self.cmp.alignment('ful', 'plenus'),
            [(48.0, '‖ f u l ‖', '‖ p - l ‖ enus')],
        )
        self.assertEqual(
            self.cmp.alignment('fiz', 'piskis'),
            [(63.0, '‖ f i z ‖', '‖ p i s ‖ kis')],
        )
        self.assertEqual(
            self.cmp.alignment('ay', 'ego'), [(17.5, '‖ ay ‖', '‖ e  ‖ go')]
        )
        self.assertEqual(
            self.cmp.alignment('tuwz', 'dentis'),
            [(75.0, '‖ t uw z ‖', 'den ‖ t i  s ‖')],
        )

        # test cases from Kondrak (2002) after Covington (1996)
        # Some of these alignments are a little different from what's in the
        # thesis because of the differing encoding used.
        self.assertEqual(
            self.cmp.alignment('jo', 'ze'), [(37.5, '‖ j o ‖', '‖ z e ‖')]
        )
        self.assertEqual(
            self.cmp.alignment('tu', 'to'), [(47.5, '‖ t u ‖', '‖ t o ‖')]
        )
        self.assertEqual(
            self.cmp.alignment('nostros', 'nu'),
            [(47.5, '‖ n o ‖ stros', '‖ n u ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('kyen', 'ki'),
            [
                (45.0, '‖ k y ‖ en', '‖ k i ‖'),
                (45.0, '‖ k ye ‖ n', '‖ k i  ‖'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('ke', 'kwa'), [(47.5, '‖ k e  ‖', '‖ k wa ‖')]
        )
        self.assertEqual(
            self.cmp.alignment('todos', 'tu'),
            [(47.5, '‖ t o ‖ dos', '‖ t u ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('una', 'on'), [(47.5, '‖ u n ‖ a', '‖ o n ‖')]
        )
        self.assertEqual(
            self.cmp.alignment('dos', 'du'), [(47.5, '‖ d o ‖ s', '‖ d u ‖')]
        )
        self.assertEqual(
            self.cmp.alignment('tres', 'trwa'),
            [(82.5, '‖ t r e  ‖ s', '‖ t r wa ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('ombre', 'om'),
            [
                (50.0, '‖ o m ‖ bre', '‖ o m ‖'),
                (50.0, '‖ o mb ‖ re', '‖ o m  ‖'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('arbol', 'arbre'),
            [(88.0, '‖ a r b o l ‖', '‖ a r b - r ‖ e')],
        )
        self.assertEqual(
            self.cmp.alignment('pluma', 'plom'),
            [(117.5, '‖ p l u m ‖ a', '‖ p l o m ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('kabeza', 'kap'),
            [(75.0, '‖ k a b ‖ eza', '‖ k a p ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('boka', 'bus'),
            [(62.5, '‖ b o k ‖ a', '‖ b u s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('pje', 'pje'),
            [(85.0, '‖ p j e ‖', '‖ p j e ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('korazon', 'kur'),
            [(82.5, '‖ k o r ‖ azon', '‖ k u r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('ber', 'vwar'),
            [(65.5, '‖ b e  r ‖', '‖ v wa r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('benir', 'vanir'),
            [(115.5, '‖ b e n i r ‖', '‖ v a n i r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('desir', 'dir'),
            [
                (65.0, 'de ‖ s i r ‖', '‖ d i r ‖'),
                (65.0, '‖ d e s i r ‖', '‖ d - - i r ‖'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('pobre', 'povra'),
            [(115.5, '‖ p o b r e ‖', '‖ p o v r a ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('fis', 'dizes'),
            [(61.0, '‖ f i s ‖', 'di ‖ z e s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('fet', 'das'),
            [(48.5, '‖ f e t ‖', '‖ d a s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('wat', 'vas'),
            [(40.0, 'w ‖ a t ‖', 'v ‖ a s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('nat', 'nixt'),
            [
                (62.5, '‖ n a - t ‖', '‖ n i x t ‖'),
                (62.5, '‖ n a t  ‖', '‖ n i xt ‖'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('lon', 'lan'),
            [(75.0, '‖ l o n ‖', '‖ l a n ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('men', 'man'),
            [(82.5, '‖ m e n ‖', '‖ m a n ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('fles', 'flays'),
            [(122.5, '‖ f l e  s ‖', '‖ f l ay s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('bled', 'blut'),
            [(100.0, '‖ b l e d ‖', '‖ b l u t ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('fezar', 'fedar'),
            [(125.0, '‖ f e z a r ‖', '‖ f e d a r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('her', 'har'),
            [(82.5, '‖ h e r ‖', '‖ h a r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('ir', 'or'), [(42.5, '‖ i r ‖', '‖ o r ‖')]
        )
        self.assertEqual(
            self.cmp.alignment('ay', 'awge'), [(20.0, '‖ a y ‖', '‖ a w ‖ ge')]
        )
        self.assertEqual(
            self.cmp.alignment('nowz', 'naze'),
            [(72.5, '‖ n ow z ‖', '‖ n a  z ‖ e')],
        )
        self.assertEqual(
            self.cmp.alignment('mawz', 'munt'),
            [(62.5, '‖ m aw z ‖', '‖ m u  n ‖ t')],
        )
        self.assertEqual(
            self.cmp.alignment('ten', 'tsune'),
            [(75.0, '‖ t  e n ‖', '‖ ts u n ‖ e')],
        )
        self.assertEqual(
            self.cmp.alignment('fot', 'fus'),
            [(72.5, '‖ f o t ‖', '‖ f u s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('niy', 'kni'),
            [(55.0, '‖ n iy ‖', 'k ‖ n i  ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('hend', 'hant'),
            [(107.5, '‖ h e n d ‖', '‖ h a n t ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('hart', 'herts'),
            [
                (117.5, '‖ h a r t ‖', '‖ h e r t ‖ s'),
                (117.5, '‖ h a r t  ‖', '‖ h e r ts ‖'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('liver', 'leber'),
            [(108.0, '‖ l i v e r ‖', '‖ l e b e r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('end', 'ante'),
            [(72.5, '‖ e n d ‖', '‖ a n t ‖ e')],
        )
        self.assertEqual(
            self.cmp.alignment('et', 'ad'), [(37.5, '‖ e t ‖', '‖ a d ‖')]
        )
        self.assertEqual(
            self.cmp.alignment('blow', 'flare'),
            [(53.0, '‖ b l o ‖ w', '‖ f l a ‖ re')],
        )
        self.assertEqual(
            self.cmp.alignment('ir', 'awris'),
            [(45.0, '‖ i r ‖', 'a ‖ w r ‖ is')],
        )
        self.assertEqual(
            self.cmp.alignment('iyt', 'edere'),
            [
                (35.0, 'i ‖ y t ‖', '‖ e d ‖ ere'),
                (35.0, '‖ iy t ‖', '‖ e  d ‖ ere'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('fis', 'piskis'),
            [(73.0, '‖ f i s ‖', '‖ p i s ‖ kis')],
        )
        self.assertEqual(
            self.cmp.alignment('flow', 'fluere'),
            [(92.5, '‖ f l ow ‖', '‖ f l u  ‖ ere')],
        )
        self.assertEqual(
            self.cmp.alignment('star', 'stella'),
            [(95.5, '‖ s t a r ‖', '‖ s t e l ‖ la')],
        )
        self.assertEqual(
            self.cmp.alignment('ful', 'plenus'),
            [(48.0, '‖ f u l ‖', '‖ p - l ‖ enus')],
        )
        self.assertEqual(
            self.cmp.alignment('gres', 'gramen'),
            [(82.5, '‖ g r e ‖ s', '‖ g r a ‖ men')],
        )
        self.assertEqual(
            self.cmp.alignment('hart', 'kordis'),
            [(70.0, '‖ h a r t ‖', '‖ k o r d ‖ is')],
        )
        self.assertEqual(
            self.cmp.alignment('horn', 'kornu'),
            [(90.0, '‖ h o r n ‖', '‖ k o r n ‖ u')],
        )
        self.assertEqual(
            self.cmp.alignment('ay', 'ego'), [(17.5, '‖ ay ‖', '‖ e  ‖ go')]
        )
        self.assertEqual(
            self.cmp.alignment('niy', 'genu'),
            [
                (45.0, '‖ n i ‖ y', 'ge ‖ n u ‖'),
                (45.0, '‖ n iy ‖', 'ge ‖ n u  ‖'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('mezer', 'mater'),
            [(112.5, '‖ m e z e r ‖', '‖ m a t e r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('mawnten', 'mons'),
            [(107.5, '‖ m aw n t ‖ en', '‖ m o  n s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('neym', 'nomen'),
            [(78.0, '‖ n ey m ‖', 'no ‖ m e  n ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('nyuw', 'nowus'),
            [(70.0, '‖ n yu w  ‖', '‖ n o  wu ‖ s')],
        )
        self.assertEqual(
            self.cmp.alignment('wen', 'unus'),
            [(50.0, '‖ we n ‖', '‖ u  n ‖ us')],
        )
        self.assertEqual(
            self.cmp.alignment('rawnd', 'rotundus'),
            [(115.0, '‖ r a - w n d ‖', '‖ r o t u n d ‖ us')],
        )
        self.assertEqual(
            self.cmp.alignment('sow', 'suere'),
            [(57.5, '‖ s ow ‖', '‖ s u  ‖ ere')],
        )
        self.assertEqual(
            self.cmp.alignment('sit', 'sedere'),
            [(65.0, '‖ s i t ‖', '‖ s e d ‖ ere')],
        )
        self.assertEqual(
            self.cmp.alignment('zrij', 'tres'),
            [(75.0, '‖ z r i j ‖', '‖ t r e s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('tuwz', 'dentis'),
            [(75.0, '‖ t uw z ‖', 'den ‖ t i  s ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('zin', 'tenuis'),
            [(55.0, '‖ z i n ‖', '‖ t e n ‖ uis')],
        )
        self.assertEqual(
            self.cmp.alignment('kinwawa', 'kenuat'),
            [(105.0, '‖ k i n w a ‖ wa', '‖ k e n u a ‖ t')],
        )
        self.assertEqual(
            self.cmp.alignment('nina', 'nenah'),
            [(90.0, '‖ n i n a ‖', '‖ n e n a ‖ h')],
        )
        self.assertEqual(
            self.cmp.alignment('napiwa', 'napew'),
            [(105.0, '‖ n a p i w ‖ a', '‖ n a p e w ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('wapimini', 'wapemen'),
            [(145.0, '‖ w a p i m i n ‖ i', '‖ w a p e m e n ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('namisa', 'namets'),
            [(125.0, '‖ n a m i s  ‖ a', '‖ n a m e ts ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('okimawa', 'okemaw'),
            [(120.0, '‖ o k i m a w ‖ a', '‖ o k e m a w ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('zizipa', 'setsep'),
            [
                (85.0, '‖ z i - z i p ‖ a', '‖ s e t s e p ‖'),
                (85.0, '‖ z i z  i p ‖ a', '‖ s e ts e p ‖'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('ahkohkwa', 'ahkeh'),
            [(127.5, '‖ a h k o h ‖ kwa', '‖ a h k e h ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('pematesiweni', 'pematesewen'),
            [
                (
                    255.0,
                    '‖ p e m a t e s i w e n ‖ i',
                    '‖ p e m a t e s e w e n ‖',
                )
            ],
        )
        self.assertEqual(
            self.cmp.alignment('asinya', 'atsen'),
            [(90.0, '‖ a s  i n ‖ ya', '‖ a ts e n ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('didomi', 'do'),
            [(50.0, 'di ‖ d o ‖ mi', '‖ d o ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('dugater', 'toxtur'),
            [(117.5, '‖ d u g a t e r ‖', '‖ t o x - t u r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('dotur', 'tugater'),
            [(105.0, '‖ d o t u r ‖', 'tu ‖ g a t e r ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('ager', 'azras'),
            [(55.0, '‖ a g e r ‖', '‖ a z - r ‖ as')],
        )
        self.assertEqual(
            self.cmp.alignment('barami', 'pero'),
            [(77.5, '‖ b a r a ‖ mi', '‖ p e r o ‖')],
        )
        self.assertEqual(
            self.cmp.alignment('kentum', 'hekaton'),
            [
                (114.0, '‖ k e n t u m ‖', 'he ‖ k a - t o n ‖'),
                (114.0, '‖ k e nt u m ‖', 'he ‖ k a t  o n ‖'),
            ],
        )
        self.assertEqual(
            self.cmp.alignment('kentum', 'satem'),
            [
                (92.5, '‖ k e n t u m ‖', '‖ s a - t e m ‖'),
                (92.5, '‖ k e nt u m ‖', '‖ s a t  e m ‖'),
            ],
        )

    def test_aline_sim(self):
        """Test abydos.distance.ALINE.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.44583333333333336)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.625)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.625)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.775)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.775)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT'.lower(), 'AACGATTAG'.lower()),
            0.732673267327,
        )

    def test_aline_sim_abs(self):
        """Test abydos.distance.ALINE.sim_abs."""
        # Base cases
        self.assertEqual(self.cmp.sim_abs('', ''), 1.0)
        self.assertEqual(self.cmp.sim_abs('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_abs('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_abs('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_abs('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_abs('abc', 'abc'), 85.0)
        self.assertEqual(self.cmp.sim_abs('abcd', 'efgh'), 53.5)

        self.assertAlmostEqual(self.cmp.sim_abs('Nigel', 'Niall'), 62.5)
        self.assertAlmostEqual(self.cmp.sim_abs('Niall', 'Nigel'), 62.5)
        self.assertAlmostEqual(self.cmp.sim_abs('Colin', 'Coiln'), 77.5)
        self.assertAlmostEqual(self.cmp.sim_abs('Coiln', 'Colin'), 77.5)
        self.assertAlmostEqual(
            self.cmp.sim_abs('ATCAACGAGT'.lower(), 'AACGATTAG'.lower()), 185.0
        )


if __name__ == '__main__':
    unittest.main()
