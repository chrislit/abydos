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

__all__ = ['BWT']


class BWT:
    """Burrows-Wheeler Transform.

    The Burrows-Wheeler transform is an attempt at placing similar characters
    together to improve compression.
    Cf. :cite:`Burrows:1994`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, terminator: str = '\0') -> None:
        """Initialize BWT instance.

        Parameters
        ----------
        terminator : str
            A character added to signal the end of the string


        .. versionadded:: 0.4.0

        """
        self._terminator = terminator

    def encode(self, word: str) -> str:
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
                    'Specified terminator, {}, already in word.'.format(  # noqa: SFS201, E501
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

    def decode(self, code: str) -> str:
        r"""Return a word decoded from BWT form.

        Parameters
        ----------
        code : str
            The word to transform from BWT form

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
                    'Specified terminator, {}, absent from code.'.format(  # noqa: SFS201, E501
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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
