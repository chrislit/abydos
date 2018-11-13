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

"""abydos.compression._bwt.

Burrows-Wheeler Transform encoder/decoder
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from six.moves import range


__all__ = ['BWT', 'bwt_decode', 'bwt_encode']


class BWT(object):
    """Burrows-Wheeler Transform.

    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression.
    Cf. :cite:`Burrows:1994`.
    """

    def encode(self, word, terminator='\0'):
        r"""Return the Burrows-Wheeler transformed form of a word.

        Parameters
        ----------
        word : str
            The word to transform using BWT
        terminator : str
            A character added to signal the end of the string

        Returns
        -------
        str
            Word encoded by BWT

        Raises
        ------
        ValueError
            Specified terminator absent from code.

        Examples
        --------
        >>> bwt = BWT()
        >>> bwt.encode('align')
        'n\x00ilag'
        >>> bwt.encode('banana')
        'annb\x00aa'
        >>> bwt.encode('banana', '@')
        'annb@aa'

        """
        if word:
            if terminator in word:
                raise ValueError(
                    'Specified terminator, {}, already in word.'.format(
                        terminator if terminator != '\0' else '\\0'
                    )
                )
            else:
                word += terminator
                wordlist = sorted(
                    word[i:] + word[:i] for i in range(len(word))
                )
                return ''.join([w[-1] for w in wordlist])
        else:
            return terminator

    def decode(self, code, terminator='\0'):
        r"""Return a word decoded from BWT form.

        Parameters
        ----------
        code : str
            The word to transform from BWT form
        terminator : str
            A character added to signal the end of the string

        Returns
        -------
        str
            Word decoded by BWT

        Raises
        ------
        ValueError
            Specified terminator absent from code.

        Examples
        --------
        >>> bwt = BWT()
        >>> bwt.decode('n\x00ilag')
        'align'
        >>> bwt.decode('annb\x00aa')
        'banana'
        >>> bwt.decode('annb@aa', '@')
        'banana'

        """
        if code:
            if terminator not in code:
                raise ValueError(
                    'Specified terminator, {}, absent from code.'.format(
                        terminator if terminator != '\0' else '\\0'
                    )
                )
            else:
                wordlist = [''] * len(code)
                for i in range(len(code)):
                    wordlist = sorted(
                        code[i] + wordlist[i] for i in range(len(code))
                    )
                rows = [w for w in wordlist if w[-1] == terminator][0]
                return rows.rstrip(terminator)
        else:
            return ''


def bwt_encode(word, terminator='\0'):
    r"""Return the Burrows-Wheeler transformed form of a word.

    This is a wrapper for :py:meth:`BWT.encode`.

    Parameters
    ----------
    word : str
        The word to transform using BWT
    terminator : str
        A character added to signal the end of the string

    Returns
    -------
    str
        Word encoded by BWT

    Examples
    --------
    >>> bwt_encode('align')
    'n\x00ilag'
    >>> bwt_encode('banana')
    'annb\x00aa'
    >>> bwt_encode('banana', '@')
    'annb@aa'

    """
    return BWT().encode(word, terminator)


def bwt_decode(code, terminator='\0'):
    r"""Return a word decoded from BWT form.

    This is a wrapper for :py:meth:`BWT.decode`.

    Parameters
    ----------
    code : str
        The word to transform from BWT form
    terminator : str
        A character added to signal the end of the string

    Returns
    -------
    str
        Word decoded by BWT

    Examples
    --------
    >>> bwt_decode('n\x00ilag')
    'align'
    >>> bwt_decode('annb\x00aa')
    'banana'
    >>> bwt_decode('annb@aa', '@')
    'banana'

    """
    return BWT().decode(code, terminator)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
