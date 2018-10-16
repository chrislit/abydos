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

"""abydos.compression.rle.

Run-Length Encoding encoder/decoder
"""

from __future__ import unicode_literals

from itertools import groupby

from . import bwt


__all__ = ['decode', 'encode']


def encode(text, use_bwt=True):
    r"""Perform encoding of run-length-encoding (RLE).

    Cf. :cite:`Robinson:1967`.

    Based on http://rosettacode.org/wiki/Run-length_encoding#Python
    :cite:`rosettacode:2018`. This is licensed GFDL 1.2.

    Digits 0-9 cannot be in text.

    :param str text: a text string to encode
    :param bool use_bwt: boolean indicating whether to perform BWT encoding
        before RLE encoding
    :returns: word decoded by BWT
    :rtype: str

    >>> encode('align')
    'n\x00ilag'
    >>> encode('align', use_bwt=False)
    'align'

    >>> encode('banana')
    'annb\x00aa'
    >>> encode('banana', use_bwt=False)
    'banana'

    >>> encode('aaabaabababa')
    'ab\x00abbab5a'
    >>> encode('aaabaabababa', False)
    '3abaabababa'
    """
    if use_bwt:
        text = bwt.encode(text)
    if text:
        text = ((len(list(g)), k) for k, g in groupby(text))
        text = ((str(n) + k if n > 2 else (k if n == 1 else 2*k)) for
                n, k in text)
    return ''.join(text)


def decode(text, use_bwt=True):
    r"""Perform decoding of run-length-encoding (RLE).

    Cf. :cite:`Robinson:1967`.

    Based on http://rosettacode.org/wiki/Run-length_encoding#Python
    :cite:`rosettacode:2018`. This is licensed GFDL 1.2.

    Digits 0-9 cannot have been in the original text.

    :param str text: a text string to decode
    :param bool use_bwt: boolean indicating whether to perform BWT decoding
        after RLE decoding
    :returns: word decoded by BWT
    :rtype: str

    >>> decode('n\x00ilag')
    'align'
    >>> decode('align', use_bwt=False)
    'align'

    >>> decode('annb\x00aa')
    'banana'
    >>> decode('banana', use_bwt=False)
    'banana'

    >>> decode('ab\x00abbab5a')
    'aaabaabababa'
    >>> decode('3abaabababa', False)
    'aaabaabababa'
    """
    mult = ''
    decoded = []
    for letter in list(text):
        if not letter.isdigit():
            if mult:
                decoded.append(int(mult)*letter)
                mult = ''
            else:
                decoded.append(letter)
        else:
            mult += letter

    text = ''.join(decoded)
    if use_bwt:
        text = bwt.decode(text)
    return text


if __name__ == '__main__':
    import doctest
    doctest.testmod()
