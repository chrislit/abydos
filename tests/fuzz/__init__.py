# -*- coding: utf-8 -*-

# Copyright 2018-2020 by Christopher C. Little.
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


"""abydos.tests.fuzz.

This module contains fuzz tests for Abydos
"""

import os
import unicodedata
from random import choice, randint, random
from string import printable

from six import unichr

from .. import EXTREME_TEST as SUPER_EXTREME_TEST
from .. import _corpus_file as _super_corpus_file

CORPORA = os.path.join(os.path.dirname(__file__), 'corpora')

EXTREME_TEST = SUPER_EXTREME_TEST  # inherit setting from base tests
EXTREME_TEST = False  # Set to True to test EVERY single case (NB: takes hours)


if not EXTREME_TEST and os.path.isfile(
    os.path.join(os.path.dirname(__file__), 'EXTREME_TEST')
):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True
if not EXTREME_TEST and os.path.isfile(
    os.path.join(os.path.dirname(__file__), '..', 'EXTREME_TEST')
):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True


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
    str
        The path to the corpus file

    """
    return _super_corpus_file(name, corpora_dir)


def _random_char(below=0x10FFFF, must_be=None):
    """Generate a random Unicode character below U+{below}.

    Parameters
    ----------
    below : int
        Maximum Unicode value
    must_be : str
        A required part of the character name

    Returns
    -------
    str
        A character

    """
    while True:
        char = unichr(randint(0, below))  # noqa: S311
        try:
            name = unicodedata.name(char)
            if must_be is None or must_be in name:
                return char
        except ValueError:
            pass


def _fuzz(word, fuzziness=0.2, must_be=None):
    """Fuzz a word with noise.

    Parameters
    ----------
    word : str
        A word to fuzz
    fuzziness : float
        How fuzzy to make the word
    must_be : str
        A required part of the character name

    Returns
    -------
    str
        A fuzzed word

    """
    while True:
        new_word = []
        for ch in word:
            if random() > fuzziness:  # noqa: S311
                new_word.append(ch)
            else:
                if random() > 0.5:  # noqa: S311
                    new_word.append(choice(printable))  # noqa: S311
                elif random() > 0.8:  # noqa: S311
                    new_word.append(
                        _random_char(0x10FFFF, must_be)
                    )  # noqa: S311
                else:
                    new_word.append(
                        _random_char(0xFFFF, must_be)
                    )  # noqa: S311
                if random() > 0.5:  # noqa: S311
                    new_word.append(ch)
        new_word = ''.join(new_word)
        if new_word != word:
            return new_word
