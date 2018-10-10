# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

import unicodedata
from random import choice, randint, random
from string import printable

from six import unichr


def _random_char(below=0x10ffff, must_be=None):
    """Generate a random Unicode character below U+{below}."""
    while True:
        char = unichr(randint(0, below))  # noqa: S311
        try:
            name = unicodedata.name(char)
            if must_be is None or must_be in name:
                return char
        except ValueError:
            pass


def _fuzz(word, fuzziness=0.2):
    """Fuzz a word with noise."""
    while True:
        new_word = []
        for ch in word:
            if random() > fuzziness:  # noqa: S311
                new_word.append(ch)
            else:
                if random() > 0.5:  # noqa: S311
                    new_word.append(choice(printable))  # noqa: S311
                elif random() > 0.8:  # noqa: S311
                    new_word.append(unichr(randint(0, 0x10ffff)))  # noqa: S311
                else:
                    new_word.append(unichr(randint(0, 0xffff)))  # noqa: S311
                if random() > 0.5:  # noqa: S311
                    new_word.append(ch)
        new_word = ''.join(new_word)
        if new_word != word:
            return new_word
