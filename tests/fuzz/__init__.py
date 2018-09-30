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

import random
import unicodedata
from string import printable

from six import unichr


def random_char(below=0x10ffff, must_be=None):
    """Generate a random Unicode character below U+{below}."""
    while True:
        char = unichr(random.randint(0, below))
        try:
            name = unicodedata.name(char)
            if must_be is None or must_be in name:
                return char
        except ValueError:
            pass


def fuzz(word, fuzziness=0.2):
    """Fuzz a word with noise."""
    while True:
        new_word = []
        for ch in word:
            if random.random() > fuzziness:
                new_word.append(ch)
            else:
                if random.random() > 0.5:
                    new_word.append(random.choice(printable))
                elif random.random() > 0.8:
                    new_word.append(unichr(random.randint(0, 0x10ffff)))
                else:
                    new_word.append(unichr(random.randint(0, 0xffff)))
                if random.random() > 0.5:
                    new_word.append(ch)
        new_word = ''.join(new_word)
        if new_word != word:
            return new_word
