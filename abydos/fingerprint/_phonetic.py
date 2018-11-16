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

"""abydos.fingerprint._phonetic.

phonetic fingerprint
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six import text_type

from ._string import String
from ..phonetic import double_metaphone

__all__ = ['Phonetic', 'phonetic_fingerprint']


class Phonetic(String):
    """Phonetic Fingerprint.

    A phonetic fingerprint is identical to a standard string fingerprint, as
    implemented in :py:class:`.String`, but performs the fingerprinting
    function after converting the string to its phonetic form, as determined by
    some phonetic algorithm. This fingerprint is described at
    :cite:`OpenRefine:2012`.
    """

    def fingerprint(
        self,
        phrase,
        phonetic_algorithm=double_metaphone,
        joiner=' ',
        *args,
        **kwargs
    ):
        """Return the phonetic fingerprint of a phrase.

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
        >>> pf = Phonetic()
        >>> pf.fingerprint('The quick brown fox jumped over the lazy dog.')
        '0 afr fks jmpt kk ls prn tk'
        >>> from abydos.phonetic import soundex
        >>> pf.fingerprint('The quick brown fox jumped over the lazy dog.',
        ... phonetic_algorithm=soundex)
        'b650 d200 f200 j513 l200 o160 q200 t000'

        """
        phonetic = ''
        for word in phrase.split():
            word = phonetic_algorithm(word, *args, **kwargs)
            if not isinstance(word, text_type) and hasattr(word, '__iter__'):
                word = word[0]
            phonetic += word + joiner
        phonetic = phonetic[: -len(joiner)]
        return super(self.__class__, self).fingerprint(phonetic)


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

    """
    return Phonetic().fingerprint(
        phrase, phonetic_algorithm, joiner, *args, **kwargs
    )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
