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


"""abydos.tests.

This module contains unit tests for Abydos
"""

import os
import unittest
from random import random

CORPORA = os.path.join(os.path.dirname(__file__), 'corpora')

EXTREME_TEST = False  # Set to True to test EVERY single case (NB: takes hours)
ALLOW_RANDOM = True  # Set to False to skip all random tests

if not EXTREME_TEST and os.path.isfile(
    os.path.join(os.path.dirname(__file__), 'EXTREME_TEST')
):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True

NIALL = (
    'Niall',
    'Neal',
    'Neil',
    'Njall',
    'Njáll',
    'Nigel',
    'Neel',
    'Nele',
    'Nigelli',
    'Nel',
    'Kneale',
    'Uí Néill',
    "O'Neill",
    'MacNeil',
    'MacNele',
    'Niall Noígíallach',
)

COLIN = (
    'Colin',
    'Collin',
    'Cullen',
    'Cuilen',
    'Cailean',
    'MacCailean',
    'Cuilén',
    'Colle',
    'Calum',
    'Callum',
    'Colinn',
    'Colon',
    'Colynn',
    'Col',
    'Cole',
    'Nicolas',
    'Nicholas',
    'Cailean Mór Caimbeul',
)

NONQ_FROM = 'The quick brown fox jumped over the lazy dog.'
NONQ_TO = 'That brown dog jumped over the fox.'


def _corpus_file(name, corpora_dir=CORPORA):
    """Return the path to a corpus file.

    Parameters
    ----------
    name : str
        Corpus file
        corpora_dir : str
        The directory containing the corpora

    Returns
    -------
    str: The full path to the corpus file

    """
    return os.path.join(corpora_dir, name)


def _one_in(inverse_probability):
    """Return whether to run a test.

    Return True if:
        EXTREME_TEST is True
        OR
        (ALLOW_RANDOM is True
        AND
        random.random() * inverse_probability < 1)
    Otherwise return False

    Parameters
    ----------
    inverse_probability : int
        The inverse of the probability

    Returns
    -------
    bool: Whether to run a test

    """
    if EXTREME_TEST:
        return True
    elif ALLOW_RANDOM and random() * inverse_probability < 1:  # noqa: S311
        return True
    else:
        return False


if __name__ == '__main__':
    unittest.main()
