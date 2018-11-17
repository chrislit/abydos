# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.phonetic._reth_schek.

Reth-Schek Phonetik
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six.moves import range

from ._phonetic import _Phonetic

__all__ = ['RethSchek', 'reth_schek_phonetik']


class RethSchek(_Phonetic):
    """Reth-Schek Phonetik.

    This algorithm is proposed in :cite:`Reth:1977`.

    Since I couldn't secure a copy of that document (maybe I'll look for it
    next time I'm in Germany), this implementation is based on what I could
    glean from the implementations published by German Record Linkage
    Center (www.record-linkage.de):

    - Privacy-preserving Record Linkage (PPRL) (in R) :cite:`Rukasz:2018`
    - Merge ToolBox (in Java) :cite:`Schnell:2004`

    Rules that are unclear:

    - Should 'C' become 'G' or 'Z'? (PPRL has both, 'Z' rule blocked)
    - Should 'CC' become 'G'? (PPRL has blocked 'CK' that may be typo)
    - Should 'TUI' -> 'ZUI' rule exist? (PPRL has rule, but I can't
      think of a German word with '-tui-' in it.)
    - Should we really change 'SCH' -> 'CH' and then 'CH' -> 'SCH'?
    """

    _replacements = {
        3: {
            'AEH': 'E',
            'IEH': 'I',
            'OEH': 'OE',
            'UEH': 'UE',
            'SCH': 'CH',
            'ZIO': 'TIO',
            'TIU': 'TIO',
            'ZIU': 'TIO',
            'CHS': 'X',
            'CKS': 'X',
            'AEU': 'OI',
        },
        2: {
            'LL': 'L',
            'AA': 'A',
            'AH': 'A',
            'BB': 'B',
            'PP': 'B',
            'BP': 'B',
            'PB': 'B',
            'DD': 'D',
            'DT': 'D',
            'TT': 'D',
            'TH': 'D',
            'EE': 'E',
            'EH': 'E',
            'AE': 'E',
            'FF': 'F',
            'PH': 'F',
            'KK': 'K',
            'GG': 'G',
            'GK': 'G',
            'KG': 'G',
            'CK': 'G',
            'CC': 'C',
            'IE': 'I',
            'IH': 'I',
            'MM': 'M',
            'NN': 'N',
            'OO': 'O',
            'OH': 'O',
            'SZ': 'S',
            'UH': 'U',
            'GS': 'X',
            'KS': 'X',
            'TZ': 'Z',
            'AY': 'AI',
            'EI': 'AI',
            'EY': 'AI',
            'EU': 'OI',
            'RR': 'R',
            'SS': 'S',
            'KW': 'QU',
        },
        1: {
            'P': 'B',
            'T': 'D',
            'V': 'F',
            'W': 'F',
            'C': 'G',
            'K': 'G',
            'Y': 'I',
        },
    }

    def encode(self, word):
        """Return Reth-Schek Phonetik code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Reth-Schek Phonetik code

        Examples
        --------
        >>> reth_schek_phonetik('Joachim')
        'JOAGHIM'
        >>> reth_schek_phonetik('Christoph')
        'GHRISDOF'
        >>> reth_schek_phonetik('Jörg')
        'JOERG'
        >>> reth_schek_phonetik('Smith')
        'SMID'
        >>> reth_schek_phonetik('Schmidt')
        'SCHMID'

        """
        # Uppercase
        word = word.upper()

        # Replace umlauts/eszett
        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = word.replace('ß', 'SS')

        # Main loop, using above replacements table
        pos = 0
        while pos < len(word):
            for num in range(3, 0, -1):
                if word[pos : pos + num] in self._replacements[num]:
                    word = (
                        word[:pos]
                        + self._replacements[num][word[pos : pos + num]]
                        + word[pos + num :]
                    )
                    pos += 1
                    break
            else:
                pos += 1  # Advance if nothing is recognized

        # Change 'CH' back(?) to 'SCH'
        word = word.replace('CH', 'SCH')

        # Replace final sequences
        if word[-2:] == 'ER':
            word = word[:-2] + 'R'
        elif word[-2:] == 'EL':
            word = word[:-2] + 'L'
        elif word[-1:] == 'H':
            word = word[:-1]

        return word


def reth_schek_phonetik(word):
    """Return Reth-Schek Phonetik code for a word.

    This is a wrapper for :py:meth:`RethSchek.encode`.

    Parameters
    ----------
    word : str
        The word to transform

    Returns
    -------
    str
        The Reth-Schek Phonetik code

    Examples
    --------
    >>> reth_schek_phonetik('Joachim')
    'JOAGHIM'
    >>> reth_schek_phonetik('Christoph')
    'GHRISDOF'
    >>> reth_schek_phonetik('Jörg')
    'JOERG'
    >>> reth_schek_phonetik('Smith')
    'SMID'
    >>> reth_schek_phonetik('Schmidt')
    'SCHMID'

    """
    return RethSchek().encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
