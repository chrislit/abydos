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

"""abydos.tests.phones.test_phones.

This module contains unit tests for abydos.phones.
"""

import unittest
from math import isnan

from abydos.phones import (
    cmp_features,
    get_feature,
    ipa_to_feature_dicts,
    ipa_to_features,
)


class PhonesTestCases(unittest.TestCase):
    """Test abydos.phones."""

    def test_phones_ipa_to_features(self):
        """Test abydos.phones.ipa_to_features."""
        self.assertEqual(
            ipa_to_features('medçen'),
            [
                2709662981243185770,
                1826957430176000426,
                2783230754501864106,
                2783233463150094762,
                1826957430176000426,
                2711173160463936106,
            ],
        )
        self.assertEqual(
            ipa_to_features('axtuŋ'),
            [
                1826957425952336298,
                2783233462881659306,
                2783230754502126250,
                1825831513894594986,
                2711175868843469418,
            ],
        )
        self.assertEqual(
            ipa_to_features('iç'), [1826957412996131242, 2783233463150094762]
        )
        self.assertEqual(
            ipa_to_features('bakofen'),
            [
                2781720575281113770,
                1826957425952336298,
                2783233462881659562,
                1825831531074464170,
                2781702983095331242,
                1826957430176000426,
                2711173160463936106,
            ],
        )
        self.assertEqual(
            ipa_to_features('dʒuŋel'),
            [
                2783230754501864106,
                2783231556184353178,
                1825831513894594986,
                2711175868843469418,
                1826957430176000426,
                2693158761954453926,
            ],
        )
        self.assertEqual(
            ipa_to_features('kvatʃ'),
            [
                2783233462881659562,
                2781702983095069098,
                1826957425952336298,
                2783230754502126250,
                2783231556184615322,
            ],
        )
        self.assertEqual(
            ipa_to_features('nitʃe'),
            [
                2711173160463936106,
                1826957412996131242,
                2783230754502126250,
                2783231556184615322,
                1826957430176000426,
            ],
        )
        self.assertEqual(
            ipa_to_features('klø'),
            [2783233462881659562, 2693158761954453926, 1825831530269157802],
        )
        self.assertEqual(
            ipa_to_features('kybax'),
            [
                2783233462881659562,
                1825831513089288618,
                2781720575281113770,
                1826957425952336298,
                2783233462881659306,
            ],
        )
        self.assertEqual(
            ipa_to_features('i@c'),
            [1826957412996131242, -1, 2783233463150095018],
        )

    def test_phones_ipa_to_feature_dicts(self):
        """Test abydos.phones.ipa_to_feature_dicts."""
        self.assertEqual(
            ipa_to_feature_dicts('medçen'),
            [
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '+',
                    'approximant': '-',
                    'labial': '+',
                    'round': '-',
                    'protruded': '-',
                    'compressed': '-',
                    'labiodental': '-',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '-',
                    'high': '0',
                    'low': '0',
                    'front': '0',
                    'back': '0',
                    'tense': '0',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '-',
                    'nasal': '+',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '+',
                    'consonantal': '-',
                    'sonorant': '+',
                    'approximant': '+',
                    'labial': '+',
                    'round': '-',
                    'protruded': '-',
                    'compressed': '-',
                    'labiodental': '-',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '-',
                    'low': '-',
                    'front': '+',
                    'back': '-',
                    'tense': '+',
                    'pharyngeal': '+',
                    'atr': '+',
                    'rtr': '-',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '-',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '+',
                    'anterior': '+',
                    'distributed': '-',
                    'dorsal': '-',
                    'high': '0',
                    'low': '0',
                    'front': '0',
                    'back': '0',
                    'tense': '0',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '-',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '-',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '-',
                    'back': '-',
                    'tense': '-',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '-',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '+',
                    'consonantal': '-',
                    'sonorant': '+',
                    'approximant': '+',
                    'labial': '+',
                    'round': '-',
                    'protruded': '-',
                    'compressed': '-',
                    'labiodental': '-',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '-',
                    'low': '-',
                    'front': '+',
                    'back': '-',
                    'tense': '+',
                    'pharyngeal': '+',
                    'atr': '+',
                    'rtr': '-',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '+',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '+',
                    'anterior': '+',
                    'distributed': '-',
                    'dorsal': '-',
                    'high': '0',
                    'low': '0',
                    'front': '0',
                    'back': '0',
                    'tense': '0',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '-',
                    'nasal': '+',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
            ],
        )
        self.assertEqual(
            ipa_to_feature_dicts('axtuŋ'),
            [
                {
                    'syllabic': '+',
                    'consonantal': '-',
                    'sonorant': '+',
                    'approximant': '+',
                    'labial': '+',
                    'round': '-',
                    'protruded': '-',
                    'compressed': '-',
                    'labiodental': '-',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '-',
                    'low': '+',
                    'front': '+',
                    'back': '-',
                    'tense': '-',
                    'pharyngeal': '+',
                    'atr': '-',
                    'rtr': '-',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '-',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '-',
                    'back': '+',
                    'tense': '-',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '-',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '-',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '+',
                    'anterior': '+',
                    'distributed': '-',
                    'dorsal': '-',
                    'high': '0',
                    'low': '0',
                    'front': '0',
                    'back': '0',
                    'tense': '0',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '-',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '-',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '+',
                    'consonantal': '-',
                    'sonorant': '+',
                    'approximant': '+',
                    'labial': '+',
                    'round': '+',
                    'protruded': '-',
                    'compressed': '-',
                    'labiodental': '-',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '-',
                    'back': '+',
                    'tense': '+',
                    'pharyngeal': '+',
                    'atr': '+',
                    'rtr': '-',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '+',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '-',
                    'back': '+',
                    'tense': '-',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '-',
                    'nasal': '+',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
            ],
        )
        self.assertEqual(
            ipa_to_feature_dicts('iç'),
            [
                {
                    'syllabic': '+',
                    'consonantal': '-',
                    'sonorant': '+',
                    'approximant': '+',
                    'labial': '+',
                    'round': '-',
                    'protruded': '-',
                    'compressed': '-',
                    'labiodental': '-',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '+',
                    'back': '-',
                    'tense': '+',
                    'pharyngeal': '+',
                    'atr': '+',
                    'rtr': '-',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '-',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '-',
                    'back': '-',
                    'tense': '-',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '-',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
            ],
        )
        self.assertEqual(
            ipa_to_feature_dicts('ʤɪn'),
            [
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '-',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '+',
                    'anterior': '-',
                    'distributed': '+',
                    'dorsal': '+',
                    'high': '-',
                    'low': '-',
                    'front': '-',
                    'back': '-',
                    'tense': '-',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+/-',
                    'nasal': '-',
                    'strident': '+',
                    'lateral': '-',
                    'delayed_release': '+',
                },
                {
                    'syllabic': '+',
                    'consonantal': '-',
                    'sonorant': '+',
                    'approximant': '+',
                    'labial': '+',
                    'round': '-',
                    'protruded': '-',
                    'compressed': '-',
                    'labiodental': '-',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '+',
                    'back': '-',
                    'tense': '-',
                    'pharyngeal': '+',
                    'atr': '-',
                    'rtr': '-',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '+',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '+',
                    'anterior': '+',
                    'distributed': '-',
                    'dorsal': '-',
                    'high': '0',
                    'low': '0',
                    'front': '0',
                    'back': '0',
                    'tense': '0',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '-',
                    'nasal': '+',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
            ],
        )
        self.assertEqual(
            ipa_to_feature_dicts('i@c'),
            [
                {
                    'syllabic': '+',
                    'consonantal': '-',
                    'sonorant': '+',
                    'approximant': '+',
                    'labial': '+',
                    'round': '-',
                    'protruded': '-',
                    'compressed': '-',
                    'labiodental': '-',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '+',
                    'back': '-',
                    'tense': '+',
                    'pharyngeal': '+',
                    'atr': '+',
                    'rtr': '-',
                    'voice': '+',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '+',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
                {},
                {
                    'syllabic': '-',
                    'consonantal': '+',
                    'sonorant': '-',
                    'approximant': '-',
                    'labial': '-',
                    'round': '0',
                    'protruded': '0',
                    'compressed': '0',
                    'labiodental': '0',
                    'coronal': '-',
                    'anterior': '0',
                    'distributed': '0',
                    'dorsal': '+',
                    'high': '+',
                    'low': '-',
                    'front': '-',
                    'back': '-',
                    'tense': '-',
                    'pharyngeal': '-',
                    'atr': '0',
                    'rtr': '0',
                    'voice': '-',
                    'spread_glottis': '-',
                    'constricted_glottis': '-',
                    'glottalic_suction': '-',
                    'velaric_suction': '-',
                    'continuant': '-',
                    'nasal': '-',
                    'strident': '-',
                    'lateral': '-',
                    'delayed_release': '-',
                },
            ],
        )

    def test_phones_get_feature(self):
        """Test abydos.phones.get_feature."""
        self.assertEqual(
            get_feature(ipa_to_features('medçen'), 'nasal'),
            [1, -1, -1, -1, -1, 1],
        )
        self.assertRaises(
            AttributeError, get_feature, ipa_to_features('medçen'), 'vocalic'
        )

        self.assertEqual(
            get_feature(ipa_to_features('nitʃe'), 'nasal'), [1, -1, -1, -1, -1]
        )
        self.assertEqual(
            get_feature(ipa_to_features('nitʃe'), 'strident'),
            [-1, -1, -1, 1, -1],
        )
        self.assertEqual(
            get_feature(ipa_to_features('nitʃe'), 'syllabic'),
            [-1, 1, -1, -1, 1],
        )
        self.assertEqual(
            get_feature(ipa_to_features('nitʃe'), 'continuant'),
            [-1, 1, -1, 1, 1],
        )

        self.assertEqual(
            get_feature(ipa_to_features('nit͡ʃe'), 'nasal'), [1, -1, -1, -1]
        )
        self.assertEqual(
            get_feature(ipa_to_features('nit͡ʃe'), 'strident'), [-1, -1, 1, -1]
        )
        self.assertEqual(
            get_feature(ipa_to_features('nit͡ʃe'), 'syllabic'), [-1, 1, -1, 1]
        )
        self.assertEqual(
            get_feature(ipa_to_features('nit͡ʃe'), 'continuant'), [-1, 1, 2, 1]
        )

        self.assertEqual(
            get_feature(ipa_to_features('løvenbroy'), 'atr'),
            [0, 1, 0, 1, 0, 0, 0, 1, 1],
        )
        self.assertNotEqual(
            get_feature(ipa_to_features('i@c'), 'syllabic'),
            [1, float('NaN'), -1],
        )
        self.assertTrue(
            isnan(get_feature(ipa_to_features('i@c'), 'syllabic')[1])
        )

    def test_phones_cmp_features(self):
        """Test abydos.phones.cmp_features."""
        # # negatives
        self.assertEqual(cmp_features(-1, 1826957425952336298), 0)
        self.assertEqual(cmp_features(1826957425952336298, -1), 0)
        self.assertEqual(cmp_features(-1, -1), 0)
        # # equals
        self.assertEqual(cmp_features(0, 0), 1)
        self.assertEqual(
            cmp_features(1826957425952336298, 1826957425952336298), 1
        )

        # # unequals
        # pre-calc everything
        cced = ipa_to_features('ç')[0]
        esh = ipa_to_features('ʃ')[0]
        tesh = ipa_to_features('t͡ʃ')[0]

        cmp_cced_tesh = cmp_features(cced, tesh)
        cmp_cced_esh = cmp_features(cced, esh)
        cmp_esh_tesh = cmp_features(esh, tesh)

        cmp_tesh_cced = cmp_features(tesh, cced)
        cmp_esh_cced = cmp_features(esh, cced)
        cmp_tesh_esh = cmp_features(tesh, esh)

        # check symmetric equality
        self.assertEqual(cmp_cced_tesh, cmp_tesh_cced)
        self.assertEqual(cmp_cced_esh, cmp_esh_cced)
        self.assertEqual(cmp_esh_tesh, cmp_tesh_esh)

        # check that they're all greater than 0
        self.assertGreater(cmp_cced_tesh, 0)
        self.assertGreater(cmp_cced_esh, 0)
        self.assertGreater(cmp_esh_tesh, 0)

        # check that they're all less than 1
        self.assertLess(cmp_cced_tesh, 1)
        self.assertLess(cmp_cced_esh, 1)
        self.assertLess(cmp_esh_tesh, 1)

        # ʃ and t͡ʃ should be more similar than either of these and ç
        self.assertGreater(cmp_esh_tesh, cmp_cced_tesh)
        self.assertGreater(cmp_esh_tesh, cmp_cced_esh)

        # weight modification
        self.assertEqual(cmp_features(cced, esh), 0.8709677419354839)
        self.assertEqual(cmp_features(cced, esh, {'syllabic': 1}), 1)
        self.assertEqual(
            cmp_features(cced, esh, [1, 1, 1]), 0.6666666666666667
        )
        with self.assertRaises(TypeError):
            cmp_features(cced, esh, 10)


if __name__ == '__main__':
    unittest.main()
