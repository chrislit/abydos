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

"""abydos.distance._aline.

ALINE distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from numpy import float as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['ALINE']


class ALINE(_Distance):
    r"""ALINE distance.

    ALINE distance :cite:`Kondrak:2000`

    .. versionadded:: 0.4.0
    """

    # The three dicts below are mostly copied from NLTK's implementation
    # https://www.nltk.org/_modules/nltk/metrics/aline.html
    # But values have been returned, as much as possible to the reference
    # values supplied in Kondrak's paper.
    feature_weights = {
        # place
        'bilabial': 1.0,
        'labiodental': 0.95,
        'dental': 0.9,
        'alveolar': 0.85,
        'retroflex': 0.8,
        'palato-alveolar': 0.75,
        'palatal': 0.7,
        'velar': 0.6,
        'uvular': 0.5,
        'pharyngeal': 0.3,
        'glottal': 0.1,
        # manner
        'stop': 1.0,
        'affricate': 0.9,
        'fricative': 0.8,
        'trill': 0.7,
        'tap': 0.65,
        'approximant': 0.6,
        'high vowel': 0.4,
        'mid vowel': 0.2,
        'low vowel': 0.0,
        # high
        'high': 1.0,
        'mid': 0.5,
        'low': 0.0,
        # back
        'front': 1.0,
        'central': 0.5,
        'back': 0.0,
        # binary features
        'plus': 1.0,
        'minus': 0.0,
    }

    v_features = {
        'syllabic',
        'nasal',
        'retroflex',
        'high',
        'back',
        'round',
        'long',
    }
    c_features = {
        'syllabic',
        'manner',
        'voice',
        'nasal',
        'retroflex',
        'lateral',
        'aspirated',
        'place',
    }

    salience = {
        'syllabic': 5,
        'voice': 10,
        'lateral': 10,
        'high': 5,
        'manner': 50,
        'long': 1,
        'place': 40,
        'nasal': 10,
        'aspirated': 5,
        'back': 5,
        'retroflex': 10,
        'round': 5,
    }

    phones_ipa = {
        'p': {
            'place': 'bilabial',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'b': {
            'place': 'bilabial',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        't': {
            'place': 'alveolar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'd': {
            'place': 'alveolar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʈ': {
            'place': 'retroflex',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'plus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɖ': {
            'place': 'retroflex',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'plus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'c': {
            'place': 'palatal',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɟ': {
            'place': 'palatal',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'k': {
            'place': 'velar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'g': {
            'place': 'velar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'q': {
            'place': 'uvular',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɢ': {
            'place': 'uvular',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʔ': {
            'place': 'glottal',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'm': {
            'place': 'bilabial',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɱ': {
            'place': 'labiodental',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'n': {
            'place': 'alveolar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɳ': {
            'place': 'retroflex',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'plus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɲ': {
            'place': 'palatal',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ŋ': {
            'place': 'velar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɴ': {
            'place': 'uvular',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʙ': {
            'place': 'bilabial',
            'manner': 'trill',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'r': {
            'place': 'alveolar',
            'manner': 'trill',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'plus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʀ': {
            'place': 'uvular',
            'manner': 'trill',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɾ': {
            'place': 'alveolar',
            'manner': 'tap',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɽ': {
            'place': 'retroflex',
            'manner': 'tap',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'plus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɸ': {
            'place': 'bilabial',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'β': {
            'place': 'bilabial',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'f': {
            'place': 'labiodental',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'v': {
            'place': 'labiodental',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'θ': {
            'place': 'dental',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ð': {
            'place': 'dental',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        's': {
            'place': 'alveolar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'z': {
            'place': 'alveolar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʃ': {
            'place': 'palato-alveolar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʒ': {
            'place': 'palato-alveolar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʂ': {
            'place': 'retroflex',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'plus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʐ': {
            'place': 'retroflex',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'plus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ç': {
            'place': 'palatal',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʝ': {
            'place': 'palatal',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'x': {
            'place': 'velar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɣ': {
            'place': 'velar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'χ': {
            'place': 'uvular',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʁ': {
            'place': 'uvular',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ħ': {
            'place': 'pharyngeal',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ʕ': {
            'place': 'pharyngeal',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'h': {
            'place': 'glottal',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɦ': {
            'place': 'glottal',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɬ': {
            'place': 'alveolar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'plus',
            'aspirated': 'minus',
        },
        'ɮ': {
            'place': 'alveolar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'plus',
            'aspirated': 'minus',
        },
        'ʋ': {
            'place': 'labiodental',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɹ': {
            'place': 'alveolar',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɻ': {
            'place': 'retroflex',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'plus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'j': {
            'place': 'palatal',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'ɰ': {
            'place': 'velar',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
        },
        'l': {
            'place': 'alveolar',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'plus',
            'aspirated': 'minus',
        },
        'w': {
            'place': 'velar',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'aspirated': 'minus',
            'double': 'bilabial',
        },
        'i': {
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'front',
            'round': 'minus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'y': {
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'front',
            'round': 'plus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'e': {
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'front',
            'round': 'minus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'ø': {
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'front',
            'round': 'plus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'ɛ': {
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'front',
            'round': 'minus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'œ': {
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'front',
            'round': 'plus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'æ': {
            'manner': 'low vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'low',
            'back': 'front',
            'round': 'minus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'a': {
            'manner': 'low vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'low',
            'back': 'front',
            'round': 'minus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'ɨ': {
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'central',
            'round': 'minus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'ʉ': {
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'central',
            'round': 'plus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'ə': {
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'central',
            'round': 'minus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'u': {
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'back',
            'round': 'plus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'o': {
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'back',
            'round': 'plus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'ɔ': {
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'back',
            'round': 'plus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'ɒ': {
            'manner': 'low vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'low',
            'back': 'back',
            'round': 'minus',
            'long': 'minus',
            'aspirated': 'minus',
        },
        'ː': {'long': 'plus', 'supplemental': True},
        'ʰ': {'aspirated': 'plus', 'supplemental': True},
    }

    phones_kondrak = {
        'a': {
            'place': 'velar',
            'manner': 'low vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'low',
            'back': 'central',
            'round': 'minus',
        },
        'b': {
            'place': 'bilabial',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'c': {
            'place': 'alveolar',
            'manner': 'affricate',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'd': {
            'place': 'alveolar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'e': {
            'place': 'palatal',
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'central',
            'round': 'minus',
        },
        'f': {
            'place': 'labiodental',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'g': {
            'place': 'velar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'h': {
            'place': 'glottal',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'i': {
            'place': 'palatal',
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'front',
            'round': 'plus',
        },
        'j': {
            'place': 'alveolar',
            'manner': 'affricate',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'k': {
            'place': 'velar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'l': {
            'place': 'alveolar',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'plus',
        },
        'm': {
            'place': 'bilabial',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'n': {
            'place': 'alveolar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'plus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'o': {
            'place': 'velar',
            'manner': 'mid vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'mid',
            'back': 'back',
            'round': 'plus',
        },
        'p': {
            'place': 'bilabial',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'q': {
            'place': 'glottal',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'r': {
            'place': 'retroflex',
            'manner': 'approximant',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'plus',
            'lateral': 'minus',
        },
        's': {
            'place': 'alveolar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        't': {
            'place': 'alveolar',
            'manner': 'stop',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'u': {
            'place': 'velar',
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'back',
            'round': 'plus',
        },
        'v': {
            'place': 'labiodental',
            'manner': 'fricative',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'w': {
            'place': 'velar',
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'back',
            'round': 'plus',
            'double': 'bilabial',
        },
        'x': {
            'place': 'velar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'minus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'y': {
            'place': 'velar',
            'manner': 'high vowel',
            'syllabic': 'plus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
            'high': 'high',
            'back': 'front',
            'round': 'minus',
        },
        'z': {
            'place': 'alveolar',
            'manner': 'fricative',
            'syllabic': 'minus',
            'voice': 'plus',
            'nasal': 'minus',
            'retroflex': 'minus',
            'lateral': 'minus',
        },
        'A': {'aspirated': 'plus', 'supplemental': True},
        'B': {'back': 'back', 'supplemental': True},
        'C': {'back': 'central', 'supplemental': True},
        'D': {'place': 'dental', 'supplemental': True},
        'F': {'back': 'front', 'supplemental': True},
        'H': {'long': 'plus', 'supplemental': True},
        'N': {'nasal': 'plus', 'supplemental': True},
        'P': {'place': 'palatal', 'supplemental': True},
        'R': {'round': 'plus', 'supplemental': True},
        'S': {'manner': 'fricative', 'supplemental': True},
        'V': {'place': 'palato-alveolar', 'supplemental': True},
    }

    def __init__(
        self,
        epsilon=0,
        c_skip=-10,
        c_sub=35,
        c_exp=45,
        c_vwl=10,
        ipa=False,
        **kwargs
    ):
        """Initialize ALINE instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(ALINE, self).__init__(**kwargs)
        self._epsilon = epsilon
        self._c_skip = c_skip
        self._c_sub = c_sub
        self._c_exp = c_exp
        self._c_vwl = c_vwl
        self._phones = self.phones_ipa if ipa else self.phones_kondrak

    def sig_sub(self, seg1, seg2):
        return (
            self._c_sub
            - self.delta(seg1, seg2)
            - self.sig_vwl(seg1)
            - self.sig_vwl(seg2)
        )

    def sig_exp(self, seg1, seg2a, seg2b):
        return (
            self._c_exp
            - self.delta(seg1, seg2a)
            - self.delta(seg1, seg2b)
            - self.sig_vwl(seg1)
            - max(self.sig_vwl(seg2a), self.sig_vwl(seg2b))
        )

    def sig_vwl(self, seg):
        return (
            0.0
            if seg['manner'] > self.feature_weights['high vowel']
            else self._c_vwl
        )

    def delta(self, seg1, seg2):
        features = (
            self.c_features
            if max(seg1['manner'], seg2['manner'])
            > self.feature_weights['high vowel']
            else self.v_features
        )
        diff = 0.0
        for f in features:
            diff += abs(seg1.get(f, 0.0) - seg2.get(f, 0.0)) * self.salience[f]
        return diff

    def retrieve(self, i, j, score, s_mat, threshold, src, tar, out):
        pass

    def sim_abs(self, src, tar):
        """Return the ALINE distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            ALINE distance

        Examples
        --------
        >>> cmp = ALINE()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        src = list(src)
        tar = list(tar)

        for ch in range(len(src)):
            if src[ch] in self._phones:
                src[ch] = dict(self._phones[src[ch]])
        for ch in range(len(tar)):
            if tar[ch] in self._phones:
                tar[ch] = dict(self._phones[tar[ch]])

        src = [fb for fb in src if isinstance(fb, dict)]
        tar = [fb for fb in tar if isinstance(fb, dict)]

        for i in range(1, len(src)):
            if 'supplemental' in src[i]:
                for j in range(i - 1, -1, -1):
                    if 'supplemental' not in src[j]:
                        for key, value in src[i].items():
                            if key != 'supplemental':
                                src[j][key] = value
                        break
        src = [fb for fb in src if 'supplemental' not in fb]

        for i in range(1, len(tar)):
            if 'supplemental' in tar[i]:
                for j in range(i - 1, -1, -1):
                    if 'supplemental' not in tar[j]:
                        for key, value in tar[i].items():
                            if key != 'supplemental':
                                tar[j][key] = value
                        break
        tar = [fb for fb in tar if 'supplemental' not in fb]

        for i in range(len(src)):
            for key, value in src[i].items():
                src[i][key] = self.feature_weights[value]
        for i in range(len(tar)):
            for key in tar[i].keys():
                tar[i][key] = self.feature_weights[tar[i][key]]

        src_len = len(src)
        tar_len = len(tar)

        s_mat = np_zeros((src_len + 1, tar_len + 1), dtype=np_float)

        for i in range(1, src_len + 1):
            for j in range(1, tar_len + 1):
                s_mat[i, j] = max(
                    s_mat[i - 1, j] + self._c_skip,
                    s_mat[i, j - 1] + self._c_skip,
                    s_mat[i - 1, j - 1] + self.sig_sub(src[i - 1], tar[j - 1]),
                    s_mat[i - 1, j - 2]
                    + self.sig_exp(src[i - 1], tar[j - 2], tar[j - 1]),
                    s_mat[i - 2, j - 1]
                    + self.sig_exp(tar[j - 1], src[i - 2], src[i - 1]),
                    0,
                )

        threshold = (1 - self._epsilon) * s_mat.max()
        """
        for i in range(1, src_len+1):
            for j in range(1, tar_len):
                if s_mat[i,j] >= threshold:
                    self.retrieve(i,j,0,s_mat,threshold,src,tar,[])
        """
        return s_mat.max()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
