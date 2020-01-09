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

"""abydos.compression._bwt.

Burrows-Wheeler Transform encoder/decoder
"""

from deprecation import deprecated

from .. import __version__

__all__ = ['BWT', 'bwt_decode', 'bwt_encode']


class BWT(object):
    """Burrows-Wheeler Transform.

    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression.
    Cf. :cite:`Burrows:1994`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, terminator='\0'):
        """Initialize BWT instance.

        Parameters
        ----------
        terminator : str
            A character added to signal the end of the string


        .. versionadded:: 0.4.0

        """
        self._terminator = terminator

    def encode(self, word):
        r"""Return the Burrows-Wheeler transformed form of a word.

        Parameters
        ----------
        word : str
            The word to transform using BWT

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

        >>> bwt = BWT('@')
        >>> bwt.encode('banana')
        'annb@aa'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if word:
            if self._terminator in word:
                raise ValueError(
                    'Specified terminator, {}, already in word.'.format(
                        self._terminator if self._terminator != '\0' else '\\0'
                    )
                )
            else:
                word += self._terminator
                wordlist = sorted(
                    word[i:] + word[:i] for i in range(len(word))
                )
                return ''.join([w[-1] for w in wordlist])
        else:
            return self._terminator

    def decode(self, code):
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

        >>> bwt = BWT('@')
        >>> bwt.decode('annb@aa')
        'banana'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if code:
            if self._terminator not in code:
                raise ValueError(
                    'Specified terminator, {}, absent from code.'.format(
                        self._terminator if self._terminator != '\0' else '\\0'
                    )
                )
            else:
                wordlist = [''] * len(code)
                for i in range(len(code)):
                    wordlist = sorted(
                        code[i] + wordlist[i] for i in range(len(code))
                    )
                rows = [w for w in wordlist if w[-1] == self._terminator][0]
                return rows.rstrip(self._terminator)
        else:
            return ''


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the BWT.encode method instead.',
)
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

    .. versionadded:: 0.1.0

    """
    return BWT(terminator).encode(word)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the BWT.decode method instead.',
)
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

    .. versionadded:: 0.1.0

    """
    return BWT(terminator).decode(code)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
