# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._phonetic import _Phonetic

__all__ = ['Ainsworth']


rules = [
    ('-(a)-', 'ə'),
    ('-(are)', 'ɑ'),
    ('(a)E', 'ɛi'),
    ('(ar)', 'ɑ'),
    ('(a)sk', 'ɑ'),
    ('(a)st', 'ɑ'),
    ('(a)th', 'ɑ'),
    ('(a)ft', 'ɑ'),
    ('(ai)', 'ɛi'),
    ('(ay)', 'ɛi'),
    ('(aw)', 'ɔ'),
    ('(au)', 'ɔ'),
    ('(al)l', 'ɔ'),
    ('(a)ble', 'ɛi'),
    ('(a)ngSUF', 'ɛi'),  # meaning of SUF? suffix?
    ('(a)', 'æ'),
    ('(b)', 'b'),
    ('(ch)', 'tʃ'),
    ('(ck)', 'k'),
    ('(c)y', 's'),
    ('(c)e', 's'),
    ('(c)i', 's'),
    ('(c)', 'k'),
    ('(d)', 'd'),
    ('VC(e)-', ''),
    ('th(e)-', 'ə'),
    ('-C(e)-', 'i'),
    ('-C(e)d', 'ɛ'),
    ('(o)ld', 'əʊ'),
    ('(oy)', 'ɔi'),
    ('(o)ing', 'əʊ'),
    ('(oi)', 'ɔi'),
    ('y(ou)', 'u'),
    ('(ou)s', 'ʌ'),
    ('(ough)t', 'ɔ'),
    ('b(ough)', 'aʊ'),
    ('t(ough)', 'ʌf'),
    ('c(ough)', 'of'),
    ('-r(ough)', 'ʌf'),
    ('r(ough)', 'ʊ'),
    ('(ough)', 'əʊ'),
    ('(oul)d', 'ʊ'),
    ('(ou)', 'aʊ'),
    ('(oor)', 'ɔ'),
    ('(oo)k', 'ʊ'),
    ('f(oo)d', 'u'),
    ('(oo)d', 'ʊ'),
    ('f(oo)t', 'ʊ'),
    ('s(oo)t', 'ʊ'),
    ('w(oo)', 'ʊ'),
    ('(oo)', 'u'),
    ('sh(oe)', 'u'),
    ('(oe)', 'əʊ'),
    ('VCd(e)d-', 'ə'),
    ('VCt(e)d-', 'ə'),
    ('VC(e)d-', ''),
    ('(e)r-', 'ə'),
    ('wh(ere)', 'ɛə'),
    ('h(ere)', 'iə'),
    ('w(ere)', 'ɜ'),
    ('(ere)', 'ir'),
    ('(ee)', 'i'),
    ('(ear)', 'ir'),
    ('(ea)', 'i'),
    ('(e)ver', 'ɛ'),
    ('(eye)', 'ɑi'),
    ('(e)E', 'i'),  # meaning of E? front vowels?
    ('c(ei)', 'i'),
    ('(ei)', 'ɑi'),
    ('(e)r', 'ɜ'),
    ('(eo)', 'i'),
    ('(ew)', 'ju'),
    ('(e)u', ''),
    ('(e)', 'ɛ'),
    ('(f)-', 'v'),
    ('(f)', 'f'),
    ('(g)e-', 'dʒ'),
    ('(g)es-', 'dʒ'),
    ('(g)SUF', 'g'),
    ('(g)i', 'dʒ'),
    ('(g)et', 'g'),
    ('c(ow)', 'ɑʊ'),
    ('h(ow)', 'ɑʊ'),
    ('n(ow)', 'ɑʊ'),
    ('v(ow)', 'ɑʊ'),
    ('r(ow)', 'ɑʊ'),
    ('(ow)', 'əʊ'),
    ('g(o)-', 'əʊ'),
    ('n(o)-', 'əʊ'),
    ('s(o)-', 'əʊ'),
    ('(o)-', 'u'),
    ('(o)', 'o'),
    ('(ph)', 'f'),
    ('(psy)', 'sɑi'),
    ('(p)', 'p'),
    ('(q)', 'kw'),
    ('(r)-', ''),
    ('(rho)', 'rəʊ'),
    ('(r)', 'r'),
    ('(sh)', 'ʃ'),
    ('(ss)', 's'),
    ('(sch)', 'sk'),
    ('Xv(s)', 'z'),  # X is any char?
    ('V(s)-', 'z'),
    ('(s)', 's'),
    ('(there)', 'ðɛə'),
    ('(g)e', 'dʒ'),
    ('(gh)', 'g'),
    ('(g)', 'g'),
    ('w(h)', ''),
    ('(ha)v', 'hæ'),
    ('(h)', 'h'),
    ('-(i)-', 'ɑi'),
    ('(i)ty', 'ɪ'),
    ('(i)E', 'ɑi'),
    ('(ir)', 'ɜ'),
    ('(igh)', 'ɑi'),
    ('t(io)n', 'ʌ'),
    ('(i)nd', 'ɑi'),
    ('(i)ld', 'ɑi'),
    ('-C(ie)', 'ɑi'),
    ('VC(ie)', 'i'),
    ('(i)', 'ɪ'),
    ('(j)', 'dʒ'),
    ('-(k)n', ''),
    ('(k)', 'k'),
    ('(le)-', 'əl'),
    ('(l)', 'l'),
    ('(m)', 'm'),
    ('(n)g', 'ŋ'),
    ('(n)', 'n'),
    ('(or)', 'ɔ'),
    ('(o)E', 'əʊ'),
    ('(oa)', 'əʊ'),
    ('(their)', 'ðɛə'),
    ('(th)r', 'θ'),
    ('(th)', 'ð'),
    ('(t)ion', 'ʃ'),
    ('(t)', 't'),
    ('(u)pon', 'ʌ'),
    ('(u)V', 'u'),
    ('(u)C-', 'ʌ'),
    ('r(u)', 'u'),
    ('l(u)', 'u'),
    ('(u)', 'ju'),
    ('(v)', 'v'),
    ('(w)r', ''),
    ('(wh)o', 'h'),
    ('(wha)t', 'wo'),
    ('(wa)', 'wo'),
    ('(wo)r', 'wɜ'),
    ('(w)', 'w'),
    ('(x)', 'ks'),
    ('-(y)', 'j'),
    ('VC(y)', 'ɪ'),
    ('-C(y)', 'ɑi'),
    ('(y)E', 'ɑi'),
    ('(y)', 'ɪ'),
    ('(z)', 'z'),
]


class Ainsworth(_Phonetic):
    """Ainsworth's grapheme to phoneme converter.

    Based on the ruleset listed in :cite:`Ainsworth:1973`.


    .. versionadded:: 0.4.1
    """
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
        'C6401'
        >>> pe.encode('Niall')
        'N2500'
        >>> pe.encode('Smith')
        'S0310'
        >>> pe.encode('Schmidt')
        'S0631'


        .. versionadded:: 0.4.1

        """
        # lowercase
        word = word.lower()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
