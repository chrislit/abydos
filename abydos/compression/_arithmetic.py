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

"""abydos.compression._arithmetic.

Arithmetic coder/decoder
"""

from collections import Counter
from fractions import Fraction
from typing import Dict, Tuple, Union

__all__ = ['Arithmetic']


class Arithmetic:
    """Arithmetic Coder.

    This is based on Andrew Dalke's public domain implementation
    :cite:`Dalke:2005`. It has been ported to use the fractions.Fraction class.


    .. versionadded:: 0.3.6
    """

    _probs = {}  # type: Dict[str, Tuple[Fraction, Fraction]]

    def __init__(self, text: Union[str, None] = None) -> None:
        """Initialize arithmetic coder object.

        Parameters
        ----------
        text : str or None
            The training text


        .. versionadded:: 0.3.6

        """
        if text is not None:
            self.train(text)

    def get_probs(self) -> Dict[str, Tuple[Fraction, Fraction]]:
        """Return the probs dictionary.

        Returns
        -------
        dict
            The dictionary of probabilities


        .. versionadded:: 0.3.6

        """
        return self._probs

    def set_probs(self, probs: Dict[str, Tuple[Fraction, Fraction]]) -> None:
        """Set the probs dictionary.

        Parameters
        ----------
        probs : dict
            The dictionary of probabilities


        .. versionadded:: 0.3.6

        """
        self._probs = probs

    def train(self, text: str) -> None:
        r"""Generate a probability dict from the provided text.

        Text to 0-order probability statistics as a dict

        Parameters
        ----------
        text : str
            The text data over which to calculate probability statistics. This
            must not contain the NUL (0x00) character because that is used to
            indicate the end of data.

        Example
        -------
        >>> ac = Arithmetic()
        >>> ac.train('the quick brown fox jumped over the lazy dog')
        >>> ac.get_probs()
        {' ': (Fraction(0, 1), Fraction(8, 45)),
         'o': (Fraction(8, 45), Fraction(4, 15)),
         'e': (Fraction(4, 15), Fraction(16, 45)),
         'u': (Fraction(16, 45), Fraction(2, 5)),
         't': (Fraction(2, 5), Fraction(4, 9)),
         'r': (Fraction(4, 9), Fraction(22, 45)),
         'h': (Fraction(22, 45), Fraction(8, 15)),
         'd': (Fraction(8, 15), Fraction(26, 45)),
         'z': (Fraction(26, 45), Fraction(3, 5)),
         'y': (Fraction(3, 5), Fraction(28, 45)),
         'x': (Fraction(28, 45), Fraction(29, 45)),
         'w': (Fraction(29, 45), Fraction(2, 3)),
         'v': (Fraction(2, 3), Fraction(31, 45)),
         'q': (Fraction(31, 45), Fraction(32, 45)),
         'p': (Fraction(32, 45), Fraction(11, 15)),
         'n': (Fraction(11, 15), Fraction(34, 45)),
         'm': (Fraction(34, 45), Fraction(7, 9)),
         'l': (Fraction(7, 9), Fraction(4, 5)),
         'k': (Fraction(4, 5), Fraction(37, 45)),
         'j': (Fraction(37, 45), Fraction(38, 45)),
         'i': (Fraction(38, 45), Fraction(13, 15)),
         'g': (Fraction(13, 15), Fraction(8, 9)),
         'f': (Fraction(8, 9), Fraction(41, 45)),
         'c': (Fraction(41, 45), Fraction(14, 15)),
         'b': (Fraction(14, 15), Fraction(43, 45)),
         'a': (Fraction(43, 45), Fraction(44, 45)),
         '\x00': (Fraction(44, 45), Fraction(1, 1))}


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if '\x00' in text:
            text = text.replace('\x00', ' ')
        counts = Counter(text)
        counts['\x00'] = 1
        tot_letters = sum(counts.values())

        tot = 0
        self._probs = {}
        prev = Fraction(0)
        for char, count in sorted(
            counts.items(), key=lambda x: (x[1], x[0]), reverse=True
        ):
            follow = Fraction(tot + count, tot_letters)
            self._probs[char] = (prev, follow)
            prev = follow
            tot = tot + count

    def encode(self, text: str) -> Tuple[int, int]:
        """Encode a text using arithmetic coding.

        Text and the 0-order probability statistics -> longval, nbits

        The encoded number is Fraction(longval, 2**nbits)

        Parameters
        ----------
        text : str
            A string to encode

        Returns
        -------
        tuple
            The arithmetically coded text

        Example
        -------
        >>> ac = Arithmetic('the quick brown fox jumped over the lazy dog')
        >>> ac.encode('align')
        (16720586181, 34)


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if '\x00' in text:
            text = text.replace('\x00', ' ')
        minval = Fraction(0)
        maxval = Fraction(1)

        for char in f'{text}\x00':
            prob_range = self._probs[char]
            delta = maxval - minval
            maxval = minval + prob_range[1] * delta
            minval = minval + prob_range[0] * delta

        # I tried without the /2 just to check.  Doesn't work.
        # Keep scaling up until the error range is >= 1.  That
        # gives me the minimum number of bits needed to resolve
        # down to the end-of-data character.
        delta = (maxval - minval) / 2
        nbits = int(0)
        while delta < 1:
            nbits += 1
            delta *= 2
        # The below condition shouldn't ever be false
        if nbits == 0:  # pragma: no cover
            return 0, 0
        # using -1 instead of /2
        avg = (maxval + minval) * 2 ** (nbits - 1)
        # Could return a rational instead ...
        # the division truncation is deliberate
        return avg.numerator // avg.denominator, nbits

    def decode(self, longval: int, nbits: int) -> str:
        """Decode the number to a string using the given statistics.

        Parameters
        ----------
        longval : int
            The first part of an encoded tuple from encode
        nbits : int
            The second part of an encoded tuple from encode

        Returns
        -------
        str
            The arithmetically decoded text

        Example
        -------
        >>> ac = Arithmetic('the quick brown fox jumped over the lazy dog')
        >>> ac.decode(16720586181, 34)
        'align'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        val = Fraction(longval, int(1) << nbits)
        letters = []

        probs_items = [
            (char, minval, maxval)
            for (char, (minval, maxval)) in self._probs.items()
        ]

        char = '\x00'
        minval = maxval = Fraction(0)
        while True:
            for (char, minval, maxval) in probs_items:  # noqa: B007
                if minval <= val < maxval:
                    break

            if char == '\x00':
                break
            letters.append(char)
            delta = maxval - minval
            val = (val - minval) / delta
        return ''.join(letters)


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
