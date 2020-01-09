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

"""abydos.fingerprint._phonetic.

phonetic fingerprint
"""

from deprecation import deprecated

from ._string import String
from .. import __version__
from ..phonetic import DoubleMetaphone, double_metaphone
from ..phonetic._phonetic import _Phonetic


__all__ = ['Phonetic', 'phonetic_fingerprint']


class Phonetic(String):
    """Phonetic Fingerprint.

    A phonetic fingerprint is identical to a standard string fingerprint, as
    implemented in :py:class:`.String`, but performs the fingerprinting
    function after converting the string to its phonetic form, as determined by
    some phonetic algorithm. This fingerprint is described at
    :cite:`OpenRefine:2012`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, phonetic_algorithm=None, joiner=' '):
        """Initialize Phonetic instance.

        phonetic_algorithm : function
            A phonetic algorithm that takes a string and returns a string
            (presumably a phonetic representation of the original string). By
            default, this function uses :py:func:`.double_metaphone`.
        joiner : str
            The string that will be placed between each word


        .. versionadded:: 0.4.0

        """
        self._phonetic_algorithm = phonetic_algorithm
        if phonetic_algorithm is None:
            self._phonetic_algorithm = DoubleMetaphone()

        self._joiner = joiner

    def fingerprint(self, phrase):
        """Return the phonetic fingerprint of a phrase.

        Parameters
        ----------
        phrase : str
            The string from which to calculate the phonetic fingerprint

        Returns
        -------
        str
            The phonetic fingerprint of the phrase

        Examples
        --------
        >>> pf = Phonetic()
        >>> pf.fingerprint('The quick brown fox jumped over the lazy dog.')
        '0 afr fks jmpt kk ls prn tk'

        >>> from abydos.phonetic import Soundex
        >>> pf = Phonetic(Soundex())
        >>> pf.fingerprint('The quick brown fox jumped over the lazy dog.')
        'b650 d200 f200 j513 l200 o160 q200 t000'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        phonetic = ''
        for word in phrase.split():
            if isinstance(self._phonetic_algorithm, _Phonetic):
                word = self._phonetic_algorithm.encode(word)
            else:
                word = self._phonetic_algorithm(word)
            if not isinstance(word, str) and hasattr(word, '__iter__'):
                word = word[0]
            phonetic += word + self._joiner
        phonetic = phonetic[: -len(self._joiner)]
        return super(Phonetic, self).fingerprint(phonetic)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Phonetic.fingerprint method instead.',
)
def phonetic_fingerprint(
    phrase, phonetic_algorithm=double_metaphone, joiner=' ', *args, **kwargs
):
    """Return the phonetic fingerprint of a phrase.

    This is a wrapper for :py:meth:`Phonetic.fingerprint`.

    Parameters
    ----------
    phrase : str
        The string from which to calculate the phonetic fingerprint
    phonetic_algorithm : function
        A phonetic algorithm that takes a string and returns a string
        (presumably a phonetic representation of the original string). By
        default, this function uses :py:func:`.double_metaphone`.
    joiner : str
        The string that will be placed between each word
    *args
        Variable length argument list
    **kwargs
        Arbitrary keyword arguments

    Returns
    -------
    str
        The phonetic fingerprint of the phrase

    Examples
    --------
    >>> phonetic_fingerprint('The quick brown fox jumped over the lazy dog.')
    '0 afr fks jmpt kk ls prn tk'

    >>> from abydos.phonetic import soundex
    >>> phonetic_fingerprint('The quick brown fox jumped over the lazy dog.',
    ... phonetic_algorithm=soundex)
    'b650 d200 f200 j513 l200 o160 q200 t000'

    .. versionadded:: 0.1.0

    """
    return Phonetic(
        lambda phrase: phonetic_algorithm(phrase, *args, **kwargs), joiner
    ).fingerprint(phrase)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
