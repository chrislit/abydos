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

"""abydos.phones._lad.

Phonetic features according to Sommers' "Lad" system :cite:`Somers:1998`, after
Connolly :cite:`Connolly:1997` and Ladefoged :cite:`Ladefoged:1995`.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import namedtuple

__all__ = []

lad_features = namedtuple(
    'lad_features',
    [
        'glottalic',
        'voice',
        'place',
        'constrictor',
        'stop',
        'length',
        'velaric',
        'aspirated',
        'nasal',
        'lateral',
        'trill',
        'tap',
        'retroflex',
        'rounded',
        'syllabic',
        'unreleased',
        'grooved',
    ],
)

_PHONETIC_FEATURES = {
    # symbol: (glottalic, voice, place, constrictor, stop, length, velaric,
    # aspirated, nasal, lateral, trill, tap, retroflex, rounded, syllabic,
    # unreleased, grooved)
}

if __name__ == '__main__':
    import doctest

    doctest.testmod()
