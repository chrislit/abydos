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

"""abydos.stemmer._schinke.

Schinke Latin stemmer.
"""

from unicodedata import normalize

from deprecation import deprecated

from ._stemmer import _Stemmer
from .. import __version__

__all__ = ['Schinke', 'schinke']


class Schinke(_Stemmer):
    """Schinke stemmer.

    This is defined in :cite:`Schinke:1996`.

    .. versionadded:: 0.3.6
    """

    _keep_que = {
        'at',
        'quo',
        'ne',
        'ita',
        'abs',
        'aps',
        'abus',
        'adae',
        'adus',
        'deni',
        'de',
        'sus',
        'obli',
        'perae',
        'plenis',
        'quando',
        'quis',
        'quae',
        'cuius',
        'cui',
        'quem',
        'quam',
        'qua',
        'qui',
        'quorum',
        'quarum',
        'quibus',
        'quos',
        'quas',
        'quotusquis',
        'quous',
        'ubi',
        'undi',
        'us',
        'uter',
        'uti',
        'utro',
        'utribi',
        'tor',
        'co',
        'conco',
        'contor',
        'detor',
        'deco',
        'exco',
        'extor',
        'obtor',
        'optor',
        'retor',
        'reco',
        'attor',
        'inco',
        'intor',
        'praetor',
    }

    _n_endings = {
        4: {'ibus'},
        3: {'ius'},
        2: {
            'is',
            'nt',
            'ae',
            'os',
            'am',
            'ud',
            'as',
            'um',
            'em',
            'us',
            'es',
            'ia',
        },
        1: {'a', 'e', 'i', 'o', 'u'},
    }

    _v_endings_strip = {
        6: {},
        5: {},
        4: {'mini', 'ntur', 'stis'},
        3: {'mur', 'mus', 'ris', 'sti', 'tis', 'tur'},
        2: {'ns', 'nt', 'ri'},
        1: {'m', 'r', 's', 't'},
    }
    _v_endings_alter = {
        6: {'iuntur'},
        5: {'beris', 'erunt', 'untur'},
        4: {'iunt'},
        3: {'bor', 'ero', 'unt'},
        2: {'bo'},
        1: {},
    }

    def stem(self, word):
        """Return the stem of a word according to the Schinke stemmer.

        Parameters
        ----------
        word : str
            The word to stem

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = Schinke()
        >>> stmr.stem('atque')
        {'n': 'atque', 'v': 'atque'}
        >>> stmr.stem('census')
        {'n': 'cens', 'v': 'censu'}
        >>> stmr.stem('virum')
        {'n': 'uir', 'v': 'uiru'}
        >>> stmr.stem('populusque')
        {'n': 'popul', 'v': 'populu'}
        >>> stmr.stem('senatus')
        {'n': 'senat', 'v': 'senatu'}


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = normalize('NFKD', word.lower())
        word = ''.join(
            c
            for c in word
            if c
            in {
                'a',
                'b',
                'c',
                'd',
                'e',
                'f',
                'g',
                'h',
                'i',
                'j',
                'k',
                'l',
                'm',
                'n',
                'o',
                'p',
                'q',
                'r',
                's',
                't',
                'u',
                'v',
                'w',
                'x',
                'y',
                'z',
            }
        )

        # Rule 2
        word = word.replace('j', 'i').replace('v', 'u')

        # Rule 3
        if word[-3:] == 'que':
            # This diverges from the paper by also returning 'que' itself
            #  unstemmed
            if word[:-3] in self._keep_que or word == 'que':
                return {'n': word, 'v': word}
            else:
                word = word[:-3]

        # Base case will mean returning the words as is
        noun = word
        verb = word

        # Rule 4
        for endlen in range(4, 0, -1):
            if word[-endlen:] in self._n_endings[endlen]:
                if len(word) - 2 >= endlen:
                    noun = word[:-endlen]
                else:
                    noun = word
                break

        for endlen in range(6, 0, -1):
            if word[-endlen:] in self._v_endings_strip[endlen]:
                if len(word) - 2 >= endlen:
                    verb = word[:-endlen]
                else:
                    verb = word
                break
            if word[-endlen:] in self._v_endings_alter[endlen]:
                if word[-endlen:] in {
                    'iuntur',
                    'erunt',
                    'untur',
                    'iunt',
                    'unt',
                }:
                    new_word = word[:-endlen] + 'i'
                    addlen = 1
                elif word[-endlen:] in {'beris', 'bor', 'bo'}:
                    new_word = word[:-endlen] + 'bi'
                    addlen = 2
                else:
                    new_word = word[:-endlen] + 'eri'
                    addlen = 3

                # Technically this diverges from the paper by considering the
                # length of the stem without the new suffix
                if len(new_word) >= 2 + addlen:
                    verb = new_word
                else:
                    verb = word
                break

        return {'n': noun, 'v': verb}


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Schinke.stem method instead.',
)
def schinke(word):
    """Return the stem of a word according to the Schinke stemmer.

    This is a wrapper for :py:meth:`Schinke.stem`.

    Parameters
    ----------
    word : str
        The word to stem

    Returns
    -------
    str
        Word stem

    Examples
    --------
    >>> schinke('atque')
    {'n': 'atque', 'v': 'atque'}
    >>> schinke('census')
    {'n': 'cens', 'v': 'censu'}
    >>> schinke('virum')
    {'n': 'uir', 'v': 'uiru'}
    >>> schinke('populusque')
    {'n': 'popul', 'v': 'populu'}
    >>> schinke('senatus')
    {'n': 'senat', 'v': 'senatu'}

    .. versionadded:: 0.3.0

    """
    return Schinke().stem(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
