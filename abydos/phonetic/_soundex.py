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

"""abydos.phonetic._soundex.

American Soundex
"""

from unicodedata import normalize as unicode_normalize

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['Soundex', 'soundex']


class Soundex(_Phonetic):
    """Soundex.

    Three variants of Soundex are implemented:

    - 'American' follows the American Soundex algorithm, as described at
      :cite:`US:2007` and in :cite:`Knuth:1998`; this is also called
      Miracode
    - 'special' follows the rules from the 1880-1910 US Census
      retrospective re-analysis, in which h & w are not treated as blocking
      consonants but as vowels. Cf. :cite:`Repici:2013`.
    - 'Census' follows the rules laid out in GIL 55 :cite:`US:1997` by the
      US Census, including coding prefixed and unprefixed versions of some
      names

    .. versionadded:: 0.3.6
    """

    _trans = dict(
        zip(
            (ord(_) for _ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            '01230129022455012623019202',
        )
    )

    _alphabetic = dict(zip((ord(_) for _ in '01234569'), 'APKTLNRH'))

    def __init__(
        self, max_length=4, var='American', reverse=False, zero_pad=True
    ):
        """Initialize Soundex instance.

        Parameters
        ----------
        max_length : int
            The length of the code returned (defaults to 4)
        var : str
            The variant of the algorithm to employ (defaults to ``American``):

                - ``American`` follows the American Soundex algorithm, as
                  described at :cite:`US:2007` and in :cite:`Knuth:1998`; this
                  is also called Miracode
                - ``special`` follows the rules from the 1880-1910 US Census
                  retrospective re-analysis, in which h & w are not treated as
                  blocking consonants but as vowels. Cf. :cite:`Repici:2013`.
                - ``Census`` follows the rules laid out in GIL 55
                  :cite:`US:1997` by the US Census, including coding prefixed
                  and unprefixed versions of some names

        reverse : bool
            Reverse the word before computing the selected Soundex (defaults to
            False); This results in "Reverse Soundex", which is useful for
            blocking in cases where the initial elements may be in error.
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string


        .. versionadded:: 0.4.0

        """
        # Require a max_length of at least 4 and not more than 64
        if max_length != -1:
            self._max_length = min(max(4, max_length), 64)
        else:
            self._max_length = 64

        self._var = var
        self._reverse = reverse
        self._zero_pad = zero_pad

    def encode_alpha(self, word):
        """Return the alphabetic Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Soundex value

        Examples
        --------
        >>> pe = Soundex()
        >>> pe.encode_alpha("Christopher")
        'CRKT'
        >>> pe.encode_alpha("Niall")
        'NL'
        >>> pe.encode_alpha('Smith')
        'SNT'
        >>> pe.encode_alpha('Schmidt')
        'SNT'


        .. versionadded:: 0.4.0

        """
        code = self.encode(word).rstrip('0')
        return code[:1] + code[1:].translate(self._alphabetic)

    def encode(self, word):
        """Return the Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Soundex value

        Examples
        --------
        >>> pe = Soundex()
        >>> pe.encode("Christopher")
        'C623'
        >>> pe.encode("Niall")
        'N400'
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Schmidt')
        'S530'

        >>> Soundex(max_length=-1).encode('Christopher')
        'C623160000000000000000000000000000000000000000000000000000000000'
        >>> Soundex(max_length=-1, zero_pad=False).encode('Christopher')
        'C62316'

        >>> Soundex(reverse=True).encode('Christopher')
        'R132'

        >>> pe.encode('Ashcroft')
        'A261'
        >>> pe.encode('Asicroft')
        'A226'

        >>> pe_special = Soundex(var='special')
        >>> pe_special.encode('Ashcroft')
        'A226'
        >>> pe_special.encode('Asicroft')
        'A226'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', word.upper())

        if self._var == 'Census':
            if word[:3] in {'VAN', 'CON'} and len(word) > 4:
                return (
                    soundex(
                        word,
                        self._max_length,
                        'American',
                        self._reverse,
                        self._zero_pad,
                    ),
                    soundex(
                        word[3:],
                        self._max_length,
                        'American',
                        self._reverse,
                        self._zero_pad,
                    ),
                )
            if word[:2] in {'DE', 'DI', 'LA', 'LE'} and len(word) > 3:
                return (
                    soundex(
                        word,
                        self._max_length,
                        'American',
                        self._reverse,
                        self._zero_pad,
                    ),
                    soundex(
                        word[2:],
                        self._max_length,
                        'American',
                        self._reverse,
                        self._zero_pad,
                    ),
                )
            # Otherwise, proceed as usual (var='American' mode, ostensibly)

        word = ''.join(c for c in word if c in self._uc_set)

        # Nothing to convert, return base case
        if not word:
            if self._zero_pad:
                return '0' * self._max_length
            return '0'

        # Reverse word if computing Reverse Soundex
        if self._reverse:
            word = word[::-1]

        # apply the Soundex algorithm
        sdx = word.translate(self._trans)

        if self._var == 'special':
            sdx = sdx.replace('9', '0')  # special rule for 1880-1910 census
        else:
            sdx = sdx.replace('9', '')  # rule 1
        sdx = self._delete_consecutive_repeats(sdx)  # rule 3

        if word[0] in 'HW':
            sdx = word[0] + sdx
        else:
            sdx = word[0] + sdx[1:]
        sdx = sdx.replace('0', '')  # rule 1

        if self._zero_pad:
            sdx += '0' * self._max_length  # rule 4

        return sdx[: self._max_length]


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Soundex.encode method instead.',
)
def soundex(word, max_length=4, var='American', reverse=False, zero_pad=True):
    """Return the Soundex code for a word.

    This is a wrapper for :py:meth:`Soundex.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)
    var : str
        The variant of the algorithm to employ (defaults to ``American``):

            - ``American`` follows the American Soundex algorithm, as described
              at :cite:`US:2007` and in :cite:`Knuth:1998`; this is also called
              Miracode
            - ``special`` follows the rules from the 1880-1910 US Census
              retrospective re-analysis, in which h & w are not treated as
              blocking consonants but as vowels. Cf. :cite:`Repici:2013`.
            - ``Census`` follows the rules laid out in GIL 55 :cite:`US:1997`
              by the US Census, including coding prefixed and unprefixed
              versions of some names

    reverse : bool
        Reverse the word before computing the selected Soundex (defaults to
        False); This results in "Reverse Soundex", which is useful for blocking
        in cases where the initial elements may be in error.
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The Soundex value

    Examples
    --------
    >>> soundex("Christopher")
    'C623'
    >>> soundex("Niall")
    'N400'
    >>> soundex('Smith')
    'S530'
    >>> soundex('Schmidt')
    'S530'

    >>> soundex('Christopher', max_length=-1)
    'C623160000000000000000000000000000000000000000000000000000000000'
    >>> soundex('Christopher', max_length=-1, zero_pad=False)
    'C62316'

    >>> soundex('Christopher', reverse=True)
    'R132'

    >>> soundex('Ashcroft')
    'A261'
    >>> soundex('Asicroft')
    'A226'
    >>> soundex('Ashcroft', var='special')
    'A226'
    >>> soundex('Asicroft', var='special')
    'A226'

    .. versionadded:: 0.1.0

    """
    return Soundex(max_length, var, reverse, zero_pad).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
