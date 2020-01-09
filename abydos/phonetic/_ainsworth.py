# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.phonetic._ainsworth.

Ainsworth's grapheme to phoneme converter
"""

import re

from ._phonetic import _Phonetic

__all__ = ['Ainsworth']


class Ainsworth(_Phonetic):
    """Ainsworth's grapheme to phoneme converter.

    Based on the ruleset listed in :cite:`Ainsworth:1973`.


    .. versionadded:: 0.4.1
    """

    _suffixes = (
        '('
        + '|'.join(
            [
                'able',
                'ance',
                'ence',
                'less',
                'ment',
                'ness',
                'ship',
                'sion',
                'tion',
                'age',
                'ant',
                'ate',
                'ent',
                'ery',
                'ful',
                'ify',
                'ise',
                'ism',
                'ity',
                'ive',
                'ize',
                'ous',
                'al',
                'cy',
                'en',
                'er',
                'es',
                'fy',
                'ry',
                's',
                'y',
            ]
        )
        + ')'
    )

    _rules = [
        (re.compile('^a$'), 'ə', 1),
        (re.compile('^are'), 'ɑ', 3),
        (re.compile('a(?=[ei])'), 'ɛi', 1),
        (re.compile('ar'), 'ɑ', 2),
        (re.compile('a(?=sk)'), 'ɑ', 1),
        (re.compile('a(?=st)'), 'ɑ', 1),
        (re.compile('a(?=th)'), 'ɑ', 1),
        (re.compile('a(?=ft)'), 'ɑ', 1),
        (re.compile('ai'), 'ɛi', 2),
        (re.compile('ay'), 'ɛi', 2),
        (re.compile('aw'), 'ɔ', 2),
        (re.compile('au'), 'ɔ', 2),
        (re.compile('al(?=l)'), 'ɔ', 2),
        (re.compile('a(?=ble)'), 'ɛi', 1),
        (re.compile('a(?=ng' + _suffixes + ')'), 'ɛi', 1),
        (re.compile('a'), 'æ', 1),
        (re.compile('b'), 'b', 1),
        (re.compile('ch'), 'tʃ', 2),
        (re.compile('ck'), 'k', 2),
        (re.compile('c(?=y)'), 's', 1),
        (re.compile('c(?=e)'), 's', 1),
        (re.compile('c(?=i)'), 's', 1),
        (re.compile('c'), 'k', 1),
        (re.compile('d'), 'd', 1),
        (re.compile('(?<=[aeiou][bcdfghjklmnpqrstvwxyz])e$'), '', 1),
        (re.compile('(?<=th)e$'), 'ə', 1),
        (re.compile('^(?<=[bcdfghjklmnpqrstvwxyz])e$'), 'i', 1),
        (re.compile('^(?<=[bcdfghjklmnpqrstvwxyz])e(?=d)'), 'ɛ', 1),
        (re.compile('o(?=ld)'), 'əʊ', 1),
        (re.compile('oy'), 'ɔi', 2),
        (re.compile('o(?=ing)'), 'əʊ', 1),
        (re.compile('oi'), 'ɔi', 2),
        (re.compile('(?<=y)ou'), 'u', 2),
        (re.compile('ou(?=s)'), 'ʌ', 2),
        (re.compile('ough(?=t)'), 'ɔ', 4),
        (re.compile('(?<=b)ough'), 'aʊ', 4),
        (re.compile('(?<=t)ough'), 'ʌf', 4),
        (re.compile('(?<=c)ough'), 'of', 4),
        (re.compile('^(?<=r)ough'), 'ʌf', 4),
        (re.compile('(?<=r)ough'), 'ʊ', 4),
        (re.compile('ough'), 'əʊ', 4),
        (re.compile('oul(?=d)'), 'ʊ', 3),
        (re.compile('ou'), 'aʊ', 2),
        (re.compile('oor'), 'ɔ', 3),
        (re.compile('oo(?=k)'), 'ʊ', 2),
        (re.compile('(?<=f)oo(?=d)'), 'u', 2),
        (re.compile('oo(?=d)'), 'ʊ', 2),
        (re.compile('(?<=f)oo(?=t)'), 'ʊ', 2),
        (re.compile('(?<=s)oo(?=t)'), 'ʊ', 2),
        (re.compile('(?<=w)oo'), 'ʊ', 2),
        (re.compile('oo'), 'u', 2),
        (re.compile('(?<=sh)oe'), 'u', 2),
        (re.compile('oe'), 'əʊ', 2),
        (re.compile('(?<=[aeiou][bcdfghjklmnpqrstvwxyz]d)e(?=d)$'), 'ə', 1),
        (re.compile('(?<=[aeiou][bcdfghjklmnpqrstvwxyz]t)e(?=d)$'), 'ə', 1),
        (re.compile('(?<=[aeiou][bcdfghjklmnpqrstvwxyz])e(?=d)$'), '', 1),
        (re.compile('e(?=r)$'), 'ə', 1),
        (re.compile('(?<=wh)ere'), 'ɛə', 3),
        (re.compile('(?<=h)ere'), 'iə', 3),
        (re.compile('(?<=w)ere'), 'ɜ', 3),
        (re.compile('ere'), 'ir', 3),
        (re.compile('ee'), 'i', 2),
        (re.compile('ear'), 'ir', 3),
        (re.compile('ea'), 'i', 2),
        (re.compile('e(?=ver)'), 'ɛ', 1),
        (re.compile('eye'), 'ɑi', 3),
        (re.compile('e(?=[ei])'), 'i', 1),
        (re.compile('(?<=c)ei'), 'i', 2),
        (re.compile('ei'), 'ɑi', 2),
        (re.compile('e(?=r)'), 'ɜ', 1),
        (re.compile('eo'), 'i', 2),
        (re.compile('ew'), 'ju', 2),
        (re.compile('e(?=u)'), '', 1),
        (re.compile('e'), 'ɛ', 1),
        (re.compile('f$'), 'v', 1),
        (re.compile('f'), 'f', 1),
        (re.compile('g(?=e)$'), 'dʒ', 1),
        (re.compile('g(?=es)$'), 'dʒ', 1),
        (re.compile('g(?=' + _suffixes + ')'), 'g', 1),
        (re.compile('g(?=i)'), 'dʒ', 1),
        (re.compile('g(?=et)'), 'g', 1),
        (re.compile('(?<=c)ow'), 'ɑʊ', 2),
        (re.compile('(?<=h)ow'), 'ɑʊ', 2),
        (re.compile('(?<=n)ow'), 'ɑʊ', 2),
        (re.compile('(?<=v)ow'), 'ɑʊ', 2),
        (re.compile('(?<=r)ow'), 'ɑʊ', 2),
        (re.compile('ow'), 'əʊ', 2),
        (re.compile('(?<=g)o$'), 'əʊ', 1),
        (re.compile('(?<=n)o$'), 'əʊ', 1),
        (re.compile('(?<=s)o$'), 'əʊ', 1),
        (re.compile('o$'), 'u', 1),
        (re.compile('o'), 'o', 1),
        (re.compile('ph'), 'f', 2),
        (re.compile('psy'), 'sɑi', 3),
        (re.compile('p'), 'p', 1),
        (re.compile('q'), 'kw', 1),
        (re.compile('r$'), '', 1),
        (re.compile('rho'), 'rəʊ', 3),
        (re.compile('r'), 'r', 1),
        (re.compile('sh'), 'ʃ', 2),
        (re.compile('ss'), 's', 2),
        (re.compile('sch'), 'sk', 3),
        (re.compile('(?<=Xv)s'), 'z', 1),
        (re.compile('(?<=[aeiou])s$'), 'z', 1),
        (re.compile('s'), 's', 1),
        (re.compile('there'), 'ðɛə', 5),
        (re.compile('g(?=e)'), 'dʒ', 1),
        (re.compile('gh'), 'g', 2),
        (re.compile('g'), 'g', 1),
        (re.compile('(?<=w)h'), '', 1),
        (re.compile('ha(?=v)'), 'hæ', 2),
        (re.compile('h'), 'h', 1),
        (re.compile('^i$'), 'ɑi', 1),
        (re.compile('i(?=ty)'), 'ɪ', 1),
        (re.compile('i(?=[ei])'), 'ɑi', 1),
        (re.compile('ir'), 'ɜ', 2),
        (re.compile('igh'), 'ɑi', 3),
        (re.compile('(?<=t)io(?=n)'), 'ʌ', 2),
        (re.compile('i(?=nd)'), 'ɑi', 1),
        (re.compile('i(?=ld)'), 'ɑi', 1),
        (re.compile('^(?<=[bcdfghjklmnpqrstvwxyz])ie'), 'ɑi', 2),
        (re.compile('(?<=[aeiou][bcdfghjklmnpqrstvwxyz])ie'), 'i', 2),
        (re.compile('i'), 'ɪ', 1),
        (re.compile('j'), 'dʒ', 1),
        (re.compile('^k(?=n)'), '', 1),
        (re.compile('k'), 'k', 1),
        (re.compile('le$'), 'əl', 2),
        (re.compile('l'), 'l', 1),
        (re.compile('m'), 'm', 1),
        (re.compile('n(?=g)'), 'ŋ', 1),
        (re.compile('n'), 'n', 1),
        (re.compile('or'), 'ɔ', 2),
        (re.compile('o(?=[ei])'), 'əʊ', 1),
        (re.compile('oa'), 'əʊ', 2),
        (re.compile('their'), 'ðɛə', 5),
        (re.compile('th(?=r)'), 'θ', 2),
        (re.compile('th'), 'ð', 2),
        (re.compile('t(?=ion)'), 'ʃ', 1),
        (re.compile('t'), 't', 1),
        (re.compile('u(?=pon)'), 'ʌ', 1),
        (re.compile('u(?=[aeiou])'), 'u', 1),
        (re.compile('u(?=[bcdfghjklmnpqrstvwxyz])$'), 'ʌ', 1),
        (re.compile('(?<=r)u'), 'u', 1),
        (re.compile('(?<=l)u'), 'u', 1),
        (re.compile('u'), 'ju', 1),
        (re.compile('v'), 'v', 1),
        (re.compile('w(?=r)'), '', 1),
        (re.compile('wh(?=o)'), 'h', 2),
        (re.compile('wha(?=t)'), 'wo', 3),
        (re.compile('wa'), 'wo', 2),
        (re.compile('wo(?=r)'), 'wɜ', 2),
        (re.compile('w'), 'w', 1),
        (re.compile('x'), 'ks', 1),
        (re.compile('^y'), 'j', 1),
        (re.compile('(?<=[aeiou][bcdfghjklmnpqrstvwxyz])y'), 'ɪ', 1),
        (re.compile('^(?<=[bcdfghjklmnpqrstvwxyz])y'), 'ɑi', 1),
        (re.compile('y(?=[ei])'), 'ɑi', 1),
        (re.compile('y'), 'ɪ', 1),
        (re.compile('z'), 'z', 1),
    ]

    def encode(self, word):
        """Return the phonemic representation of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The phonemic representation in IPA

        Examples
        --------
        >>> pe = Ainsworth()
        >>> pe.encode('Christopher')
        'tʃrɪstofɜ'
        >>> pe.encode('Niall')
        'nɪɔl'
        >>> pe.encode('Smith')
        'smɪð'
        >>> pe.encode('Schmidt')
        'skmɪdt'


        .. versionadded:: 0.4.1

        """
        # lowercase
        word = word.lower()
        pron = []

        pos = 0
        while pos < len(word):
            for rule, repl, matchlen in self._rules:
                if rule.match(word, pos):
                    pron.append(repl)
                    pos += matchlen
                    break
            else:
                # failed to match, but advance anyway
                pos += 1

        return ''.join(pron)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
