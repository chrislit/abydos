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

Burrows-Wheeler transform encoder/decoder (bwt_encode & bwt_decode)
"""

from __future__ import unicode_literals

from six.moves import range


__all__ = ['bwt_decode', 'bwt_encode']


def bwt_encode(word, terminator='\0'):
    r"""Return the Burrows-Wheeler transformed form of a word.

    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression.
    Cf. :cite:`Burrows:1994`.

    :param str word: the word to transform using BWT
    :param str terminator: a character to add to word to signal the end of the
        string
    :returns: word encoded by BWT
    :rtype: str

    >>> bwt_encode('align')
    'n\x00ilag'
    >>> bwt_encode('banana')
    'annb\x00aa'
    >>> bwt_encode('banana', '@')
    'annb@aa'
    """
    if word:
        if terminator in word:
            raise ValueError(
                'Specified terminator, %s, already in word.'.format(
                    terminator if terminator != '\0' else '\\0'
                )
            )
        else:
            word += terminator
            wordlist = sorted(word[i:] + word[:i] for i in range(len(word)))
            return ''.join([w[-1] for w in wordlist])
    else:
        return terminator


def bwt_decode(code, terminator='\0'):
    r"""Return a word decoded from BWT form.

    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression. This function reverses the transform.
    Cf. :cite:`Burrows:1994`.

    :param str code: the word to transform from BWT form
    :param str terminator: a character added to word to signal the end of the
        string
    :returns: word decoded by BWT
    :rtype: str

    >>> bwt_decode('n\x00ilag')
    'align'
    >>> bwt_decode('annb\x00aa')
    'banana'
    >>> bwt_decode('annb@aa', '@')
    'banana'
    """
    if code:
        if terminator not in code:
            raise ValueError(
                'Specified terminator, %s, absent from code.'.format(
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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
