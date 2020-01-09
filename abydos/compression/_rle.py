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

"""abydos.compression._rle.

Run-Length Encoding encoder/decoder
"""

from itertools import groupby

from deprecation import deprecated

from ._bwt import BWT
from .. import __version__

__all__ = ['RLE', 'rle_decode', 'rle_encode']


class RLE(object):
    """Run-Length Encoding.

    Cf. :cite:`Robinson:1967`.

    Based on http://rosettacode.org/wiki/Run-length_encoding#Python
    :cite:`rosettacode:2018`. This is licensed GFDL 1.2.

    Digits 0-9 cannot be in text.

    .. versionadded:: 0.3.6
    """

    def encode(self, text):
        r"""Perform encoding of run-length-encoding (RLE).

        Parameters
        ----------
        text : str
            A text string to encode

        Returns
        -------
        str
            Word decoded by RLE

        Examples
        --------
        >>> rle = RLE()
        >>> bwt = BWT()
        >>> rle.encode(bwt.encode('align'))
        'n\x00ilag'
        >>> rle.encode('align')
        'align'

        >>> rle.encode(bwt.encode('banana'))
        'annb\x00aa'
        >>> rle.encode('banana')
        'banana'

        >>> rle.encode(bwt.encode('aaabaabababa'))
        'ab\x00abbab5a'
        >>> rle.encode('aaabaabababa')
        '3abaabababa'

        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if text:
            text = ((len(list(g)), k) for k, g in groupby(text))
            text = (
                (str(n) + k if n > 2 else (k if n == 1 else 2 * k))
                for n, k in text
            )
        return ''.join(text)

    def decode(self, text):
        r"""Perform decoding of run-length-encoding (RLE).

        Parameters
        ----------
        text : str
            A text string to decode

        Returns
        -------
        str
            Word decoded by RLE

        Examples
        --------
        >>> rle = RLE()
        >>> bwt = BWT()
        >>> bwt.decode(rle.decode('n\x00ilag'))
        'align'
        >>> rle.decode('align')
        'align'

        >>> bwt.decode(rle.decode('annb\x00aa'))
        'banana'
        >>> rle.decode('banana')
        'banana'

        >>> bwt.decode(rle.decode('ab\x00abbab5a'))
        'aaabaabababa'
        >>> rle.decode('3abaabababa')
        'aaabaabababa'

        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

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
        return text


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the RLE.encode method instead.',
)
def rle_encode(text, use_bwt=True):
    r"""Perform encoding of run-length-encoding (RLE).

    This is a wrapper for :py:meth:`RLE.encode`.

    Parameters
    ----------
    text : str
        A text string to encode
    use_bwt : bool
        Indicates whether to perform BWT encoding before RLE encoding

    Returns
    -------
    str
        Word decoded by RLE

    Examples
    --------
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

    .. versionadded:: 0.1.0

    """
    if use_bwt:
        text = BWT().encode(text)
    return RLE().encode(text)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the RLE.decode method instead.',
)
def rle_decode(text, use_bwt=True):
    r"""Perform decoding of run-length-encoding (RLE).

    This is a wrapper for :py:meth:`RLE.decode`.

    Parameters
    ----------
    text : str
        A text string to decode
    use_bwt : bool
        Indicates whether to perform BWT decoding after RLE decoding

    Returns
    -------
    str
        Word decoded by RLE

    Examples
    --------
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

    .. versionadded:: 0.1.0

    """
    text = RLE().decode(text)
    if use_bwt:
        text = BWT().decode(text)
    return text


if __name__ == '__main__':
    import doctest

    doctest.testmod()
