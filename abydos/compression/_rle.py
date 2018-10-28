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

"""abydos.compression._rle.

Run-Length Encoding encoder/decoder (rle_encoder & rle_decoder)
"""

from __future__ import unicode_literals

from itertools import groupby

from ._bwt import bwt_decode, bwt_encode


__all__ = ['rle_decode', 'rle_encode']


def rle_encode(text, use_bwt=True):
    r"""Perform encoding of run-length-encoding (RLE).

    Cf. :cite:`Robinson:1967`.

    Based on http://rosettacode.org/wiki/Run-length_encoding#Python
    :cite:`rosettacode:2018`. This is licensed GFDL 1.2.

    Digits 0-9 cannot be in text.

    :param str text: a text string to encode
    :param bool use_bwt: boolean indicating whether to perform BWT encoding
        before RLE encoding
    :returns: word decoded by RLE
    :rtype: str

    >>> rle_encode('align')
    'n\x00ilag'
    >>> rle_encode('align', use_bwt=False)
    'align'

    >>> rle_encode('banana')
    'annb\x00aa'
    >>> rle_encode('banana', use_bwt=False)
    'banana'

    >>> rle_encode('aaabaabababa')
    'ab\x00abbab5a'
    >>> rle_encode('aaabaabababa', False)
    '3abaabababa'
    """
    if use_bwt:
        text = bwt_encode(text)
    if text:
        text = ((len(list(g)), k) for k, g in groupby(text))
        text = (
            (str(n) + k if n > 2 else (k if n == 1 else 2 * k))
            for n, k in text
        )
    return ''.join(text)


def rle_decode(text, use_bwt=True):
    r"""Perform decoding of run-length-encoding (RLE).

    Cf. :cite:`Robinson:1967`.

    Based on http://rosettacode.org/wiki/Run-length_encoding#Python
    :cite:`rosettacode:2018`. This is licensed GFDL 1.2.

    Digits 0-9 cannot have been in the original text.

    :param str text: a text string to decode
    :param bool use_bwt: boolean indicating whether to perform BWT decoding
        after RLE decoding
    :returns: word decoded by RLE
    :rtype: str

    >>> rle_decode('n\x00ilag')
    'align'
    >>> rle_decode('align', use_bwt=False)
    'align'

    >>> rle_decode('annb\x00aa')
    'banana'
    >>> rle_decode('banana', use_bwt=False)
    'banana'

    >>> rle_decode('ab\x00abbab5a')
    'aaabaabababa'
    >>> rle_decode('3abaabababa', False)
    'aaabaabababa'
    """
    mult = ''
    decoded = []
    for letter in list(text):
        if not letter.isdigit():
            if mult:
                decoded.append(int(mult) * letter)
                mult = ''
            else:
                decoded.append(letter)
        else:
            mult += letter

    text = ''.join(decoded)
    if use_bwt:
        text = bwt_decode(text)
    return text


if __name__ == '__main__':
    import doctest

    doctest.testmod()
