# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.stemmer.

The stemmer package collects stemmer classes for a number of
languages including:

    - English stemmers:

        - Lovins' (:py:class:`.Lovins`)
        - Porter (:py:class:`.Porter`)
        - Porter2 (i.e. Snowball English) (:py:class:`.Porter2`)
        - UEA-Lite (:py:class:`.UEALite`)
        - Paice-Husk (:py:class:`.PaiceHusk`)
        - S-stemmer (:py:class:`.SStemmer`)

    - German stemmers:

        - Caumanns' (:py:class:`.Caumanns`)
        - CLEF German (:py:class:`.CLEFGerman`)
        - CLEF German Plus (:py:class:`.CLEFGermanPlus`)
        - Snowball German (:py:class:`.SnowballGerman`)

    - Swedish stemmers:

        - CLEF Swedish (:py:class:`.CLEFSwedish`)
        - Snowball Swedish (:py:class:`.SnowballSwedish`)

    - Latin stemmer:

        - Schinke (:py:class:`.Schinke`)

    - Danish stemmer:

        - Snowball Danish (:py:class:`.SnowballDanish`)

    - Dutch stemmer:

        - Snowball Dutch (:py:class:`.SnowballDutch`)

    - Norwegian stemmer:

        - Snowball Norwegian (:py:class:`.SnowballNorwegian`)


Each stemmer has a ``stem`` method, which takes a word and returns its stemmed
form:

>>> stmr = Porter()
>>> stmr.stem('democracy')
'democraci'
>>> stmr.stem('trusted')
'trust'

----

"""

from ._caumanns import Caumanns
from ._clef_german import CLEFGerman
from ._clef_german_plus import CLEFGermanPlus
from ._clef_swedish import CLEFSwedish
from ._lovins import Lovins
from ._paice_husk import PaiceHusk
from ._porter import Porter
from ._porter2 import Porter2
from ._s_stemmer import SStemmer
from ._schinke import Schinke
from ._snowball import _Snowball
from ._snowball_danish import SnowballDanish
from ._snowball_dutch import SnowballDutch
from ._snowball_german import SnowballGerman
from ._snowball_norwegian import SnowballNorwegian
from ._snowball_swedish import SnowballSwedish
from ._stemmer import _Stemmer
from ._uea_lite import UEALite

__all__ = [
    '_Stemmer',
    '_Snowball',
    'Lovins',
    'PaiceHusk',
    'UEALite',
    'SStemmer',
    'Caumanns',
    'Schinke',
    'Porter',
    'Porter2',
    'SnowballDanish',
    'SnowballDutch',
    'SnowballGerman',
    'SnowballNorwegian',
    'SnowballSwedish',
    'CLEFGerman',
    'CLEFGermanPlus',
    'CLEFSwedish',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
