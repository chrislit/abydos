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

"""abydos.distance._aline.

ALINE alignment, similarity, and distance
"""

from copy import deepcopy

from numpy import NINF
from numpy import float as np_float
from numpy import zeros as np_zeros

from ._distance import _Distance

__all__ = ['ALINE']


class ALINE(_Distance):
    r"""ALINE alignment, similarity, and distance.

    ALINE alignment was developed by
    :cite:`Kondrak:2000,Kondrak:2002,Downey:2008`, and establishes an
    alignment algorithm based on multivalued phonetic features and feature
    salience weights. Along with the alignment itself, the algorithm produces a
    term similarity score.

    :cite:`Downey:2008` develops ALINE's similarity score into a similarity
    measure & distance measure:

        .. math::

            sim_{ALINE} = \frac{2 \dot score_{ALINE}(src, tar)}
            {score_{ALINE}(src, src) + score_{ALINE}(tar, tar)}

    However, because the average of the two self-similarity scores is not
    guaranteed to be greater than or equal to the similarity score between
    the two strings, by default, this formula is not used here in order to
    guarantee that the similarity measure is bounded to [0, 1]. Instead,
    Kondrak's similarity measure is employed:

        .. math::

            sim_{ALINE} = \frac{score_{ALINE}(src, tar)}
            {max(score_{ALINE}(src, src), score_{ALINE}(tar, tar))}


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
        'approximant': 0.6,
        'trill': 0.55,  # not in original
        'tap': 0.5,  # not in original
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
            'back': 'front',
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
        mode='local',
        phones='aline',
        normalizer=max,
        **kwargs
    ):
        """Initialize ALINE instance.

        Parameters
        ----------
        epsilon : float
            The portion (out of 1.0) of the maximum ALINE score, above which
            alignments are returned. If set to 0, only the alignments matching
            the maximum alignment score are returned. If set to 1, all
            alignments scoring 0 or higher are returned.
        c_skip : int
            The cost of an insertion or deletion
        c_sub : int
            The cost of a substitution
        c_exp : int
            The cost of an expansion or contraction
        c_vwl : int
            The additional cost of a vowel substitution, expansion, or
            contraction
        mode : str
            Alignment mode, which can be ``local`` (default), ``global``,
            ``half-local``, or ``semi-global``
        phones : str
            Phonetic symbol set, which can be:
                - ``aline`` selects Kondrak's original symbols set
                - ``ipa`` selects IPA symbols
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). For the
            normalization proposed by Downey, et al. (2008), set this to:
            ``lambda x: sum(x)/len(x)``
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
        self._mode = mode
        if self._mode not in {'local', 'global', 'half-local', 'semi-global'}:
            self._mode = 'local'
        if phones == 'ipa':
            self._phones = self.phones_ipa
        else:
            self._phones = self.phones_kondrak
        self._normalizer = normalizer

    def alignment(self, src, tar):
        """Return the top ALINE alignment of two strings.

        The `top` ALINE alignment is the first alignment with the best score.
        The purpose of this function is to have a single tuple as a return
        value.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        tuple(float, str, str)
            ALINE alignment and its score

        Examples
        --------
        >>> cmp = ALINE()
        >>> cmp.alignment('cat', 'hat')
        (50.0, 'c ‖ a t ‖', 'h ‖ a t ‖')
        >>> cmp.alignment('niall', 'neil')
        (90.0, '‖ n i a ll ‖', '‖ n e i l  ‖')
        >>> cmp.alignment('aluminum', 'catalan')
        (81.5, '‖ a l u m ‖ inum', 'cat ‖ a l a n ‖')
        >>> cmp.alignment('atcg', 'tagc')
        (65.0, '‖ a t c ‖ g', 't ‖ a g c ‖')


        .. versionadded:: 0.4.1

        """
        return self.alignments(src, tar)[0]

    def alignments(self, src, tar, score_only=False):
        """Return the ALINE alignments of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        score_only : bool
            Return the score only, not the alignments

        Returns
        -------
        list(tuple(float, str, str) or float
            ALINE alignments and their scores or the top score

        Examples
        --------
        >>> cmp = ALINE()
        >>> cmp.alignments('cat', 'hat')
        [(50.0, 'c ‖ a t ‖', 'h ‖ a t ‖')]
        >>> cmp.alignments('niall', 'neil')
        [(90.0, '‖ n i a ll ‖', '‖ n e i l  ‖')]
        >>> cmp.alignments('aluminum', 'catalan')
        [(81.5, '‖ a l u m ‖ inum', 'cat ‖ a l a n ‖')]
        >>> cmp.alignments('atcg', 'tagc')
        [(65.0, '‖ a t c ‖ g', 't ‖ a g c ‖'), (65.0, 'a ‖ tc - g ‖',
        '‖ t  a g ‖ c')]


        .. versionadded:: 0.4.0
        .. versionchanged:: 0.4.1
            Renamed from .alignment to .alignments

        """

        def _sig_skip(seg):
            return self._c_skip

        def _sig_sub(seg1, seg2):
            return (
                self._c_sub
                - _delta(seg1, seg2)
                - _sig_vwl(seg1)
                - _sig_vwl(seg2)
            )

        def _sig_exp(seg1, seg2a, seg2b):
            return (
                self._c_exp
                - _delta(seg1, seg2a)
                - _delta(seg1, seg2b)
                - _sig_vwl(seg1)
                - max(_sig_vwl(seg2a), _sig_vwl(seg2b))
            )

        def _sig_vwl(seg):
            return (
                0.0
                if seg['manner'] > self.feature_weights['high vowel']
                else self._c_vwl
            )

        def _delta(seg1, seg2):
            features = (
                self.c_features
                if max(seg1['manner'], seg2['manner'])
                > self.feature_weights['high vowel']
                else self.v_features
            )
            diff = 0.0
            for f in features:
                diff += (
                    abs(seg1.get(f, 0.0) - seg2.get(f, 0.0)) * self.salience[f]
                )
            return diff

        def _retrieve(i, j, score, out):
            def _record(score, out):
                out.append(('‖', '‖'))
                for i1 in range(i - 1, -1, -1):
                    out.append((src[i1]['segment'], ''))
                for j1 in range(j - 1, -1, -1):
                    out.append(('', tar[j1]['segment']))
                if self._mode == 'global':
                    score += (i + j) * _sig_skip('')

                out = out[::-1]

                src_alignment = []
                tar_alignment = []

                out.append(('‖', '‖'))
                part = 0
                s_segment = ''
                t_segment = ''
                for ss, ts in out:
                    if ss == '‖':
                        if part % 2 == 0:
                            src_alignment.append(s_segment)
                            tar_alignment.append(t_segment)
                            s_segment = []
                            t_segment = []
                        else:
                            src_alignment.append(' '.join(s_segment))
                            tar_alignment.append(' '.join(t_segment))
                            s_segment = ''
                            t_segment = ''
                        part += 1
                    else:
                        if part % 2 == 0:
                            s_segment += ss
                            t_segment += ts
                        else:
                            s_segment.append(ss + ' ' * (len(ts) - len(ss)))
                            t_segment.append(ts + ' ' * (len(ss) - len(ts)))

                src_alignment = ' ‖ '.join(src_alignment).strip()
                tar_alignment = ' ‖ '.join(tar_alignment).strip()

                alignments.append((score, src_alignment, tar_alignment))
                return

            if s_mat[i, j] == 0:
                _record(score, out)
                return
            else:
                if (
                    i > 0
                    and j > 0
                    and s_mat[i - 1, j - 1]
                    + _sig_sub(src[i - 1], tar[j - 1])
                    + score
                    >= threshold
                ):
                    loc_out = deepcopy(out)
                    loc_out.append(
                        (src[i - 1]['segment'], tar[j - 1]['segment'])
                    )
                    _retrieve(
                        i - 1,
                        j - 1,
                        score + _sig_sub(src[i - 1], tar[j - 1]),
                        loc_out,
                    )
                    loc_out.pop()

                if (
                    j > 0
                    and s_mat[i, j - 1] + _sig_skip(tar[j - 1]) + score
                    >= threshold
                ):
                    loc_out = deepcopy(out)
                    loc_out.append(('-', tar[j - 1]['segment']))
                    _retrieve(i, j - 1, score + _sig_skip(tar[j - 1]), loc_out)
                    loc_out.pop()

                if (
                    i > 0
                    and j > 1
                    and s_mat[i - 1, j - 2]
                    + _sig_exp(src[i - 1], tar[j - 2], tar[j - 1])
                    + score
                    >= threshold
                ):
                    loc_out = deepcopy(out)
                    loc_out.append(
                        (
                            src[i - 1]['segment'],
                            tar[j - 2]['segment'] + tar[j - 1]['segment'],
                        )
                    )
                    _retrieve(
                        i - 1,
                        j - 2,
                        score + _sig_exp(src[i - 1], tar[j - 2], tar[j - 1]),
                        loc_out,
                    )
                    loc_out.pop()

                if (
                    i > 0
                    and s_mat[i - 1, j] + _sig_skip(src[i - 1]) + score
                    >= threshold
                ):
                    loc_out = deepcopy(out)
                    loc_out.append((src[i - 1]['segment'], '-'))
                    _retrieve(i - 1, j, score + _sig_skip(src[i - 1]), loc_out)
                    loc_out.pop()

                if (
                    i > 1
                    and j > 0
                    and s_mat[i - 2, j - 1]
                    + _sig_exp(tar[j - 1], src[i - 2], src[i - 1])
                    + score
                    >= threshold
                ):
                    loc_out = deepcopy(out)
                    loc_out.append(
                        (
                            src[i - 2]['segment'] + src[i - 1]['segment'],
                            tar[j - 1]['segment'],
                        )
                    )
                    _retrieve(
                        i - 2,
                        j - 1,
                        score + _sig_exp(tar[j - 1], src[i - 2], src[i - 1]),
                        loc_out,
                    )
                    loc_out.pop()

        sg_max = 0.0

        src = list(src)
        tar = list(tar)

        for ch in range(len(src)):
            if src[ch] in self._phones:
                seg = src[ch]
                src[ch] = dict(self._phones[src[ch]])
                src[ch]['segment'] = seg
        for ch in range(len(tar)):
            if tar[ch] in self._phones:
                seg = tar[ch]
                tar[ch] = dict(self._phones[tar[ch]])
                tar[ch]['segment'] = seg

        src = [fb for fb in src if isinstance(fb, dict)]
        tar = [fb for fb in tar if isinstance(fb, dict)]

        for i in range(1, len(src)):
            if 'supplemental' in src[i]:
                j = i - 1
                while j > -1:
                    if 'supplemental' not in src[j]:
                        for key, value in src[i].items():
                            if key != 'supplemental':
                                if key == 'segment':
                                    src[j]['segment'] += value
                                else:
                                    src[j][key] = value
                        j = 0
                    j -= 1
        src = [fb for fb in src if 'supplemental' not in fb]

        for i in range(1, len(tar)):
            if 'supplemental' in tar[i]:
                j = i - 1
                while j > -1:
                    if 'supplemental' not in tar[j]:
                        for key, value in tar[i].items():
                            if key != 'supplemental':
                                if key == 'segment':
                                    tar[j]['segment'] += value
                                else:
                                    tar[j][key] = value
                        j = 0
                    j -= 1
        tar = [fb for fb in tar if 'supplemental' not in fb]

        for i in range(len(src)):
            for key in src[i].keys():
                if key != 'segment':
                    src[i][key] = self.feature_weights[src[i][key]]
        for i in range(len(tar)):
            for key in tar[i].keys():
                if key != 'segment':
                    tar[i][key] = self.feature_weights[tar[i][key]]

        src_len = len(src)
        tar_len = len(tar)

        s_mat = np_zeros((src_len + 1, tar_len + 1), dtype=np_float)

        if self._mode == 'global':
            for i in range(1, src_len + 1):
                s_mat[i, 0] = s_mat[i - 1, 0] + _sig_skip(src[i - 1])
            for j in range(1, tar_len + 1):
                s_mat[0, j] = s_mat[0, j - 1] + _sig_skip(tar[j - 1])

        for i in range(1, src_len + 1):
            for j in range(1, tar_len + 1):
                s_mat[i, j] = max(
                    s_mat[i - 1, j] + _sig_skip(src[i - 1]),
                    s_mat[i, j - 1] + _sig_skip(tar[j - 1]),
                    s_mat[i - 1, j - 1] + _sig_sub(src[i - 1], tar[j - 1]),
                    s_mat[i - 1, j - 2]
                    + _sig_exp(src[i - 1], tar[j - 2], tar[j - 1])
                    if j > 1
                    else NINF,
                    s_mat[i - 2, j - 1]
                    + _sig_exp(tar[j - 1], src[i - 2], src[i - 1])
                    if i > 1
                    else NINF,
                    0 if self._mode in {'local', 'half-local'} else NINF,
                )

                if s_mat[i, j] > sg_max:
                    if self._mode == 'semi-global':
                        if i == src_len or j == tar_len:
                            sg_max = s_mat[i, j]
                    else:
                        sg_max = s_mat[i, j]

        if self._mode in {'global', 'half-local'}:
            dp_score = s_mat[src_len, tar_len]
        else:
            dp_score = s_mat.max()

        if score_only:
            return dp_score

        threshold = (1 - self._epsilon) * dp_score

        alignments = []

        for i in range(1, src_len + 1):
            for j in range(1, tar_len + 1):
                if self._mode in {'global', 'half-local'} and (
                    i < src_len or j < tar_len
                ):
                    continue
                if self._mode == 'semi-global' and (
                    i < src_len and j < tar_len
                ):
                    continue
                if s_mat[i, j] >= threshold:
                    out = []
                    for j1 in range(tar_len - 1, j - 1, -1):
                        out.append(('', tar[j1]['segment']))
                    for i1 in range(src_len - 1, i - 1, -1):
                        out.append((src[i1]['segment'], ''))
                    out.append(('‖', '‖'))
                    _retrieve(i, j, 0, out)

        def _first_element(x):
            return x[0]

        return sorted(alignments, key=_first_element, reverse=True)

    def sim_score(self, src, tar):
        """Return the ALINE alignment score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            ALINE alignment score

        Examples
        --------
        >>> cmp = ALINE()
        >>> cmp.sim_score('cat', 'hat')
        50.0
        >>> cmp.sim_score('niall', 'neil')
        90.0
        >>> cmp.sim_score('aluminum', 'catalan')
        81.5
        >>> cmp.sim_score('atcg', 'tagc')
        65.0


        .. versionadded:: 0.4.0

        """
        if src == '' and tar == '':
            return 1.0
        return self.alignments(src, tar, score_only=True)

    def sim(self, src, tar):
        """Return the normalized ALINE similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized ALINE similarity

        Examples
        --------
        >>> cmp = ALINE()
        >>> cmp.dist('cat', 'hat')
        0.4117647058823529
        >>> cmp.dist('niall', 'neil')
        0.33333333333333337
        >>> cmp.dist('aluminum', 'catalan')
        0.5925
        >>> cmp.dist('atcg', 'tagc')
        0.45833333333333337


        .. versionadded:: 0.4.0

        """
        num = self.sim_score(src, tar)
        if num:
            return num / self._normalizer(
                [self.sim_score(src, src), self.sim_score(tar, tar)]
            )
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
