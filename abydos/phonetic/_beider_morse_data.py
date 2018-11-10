# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
# This file is part of Abydos.
#
# This file is based on Alexander Beider and Stephen P. Morse's implementation
# of the Beider-Morse Phonetic Matching (BMPM) System, available at
# http://stevemorse.org/phonetics/bmpm.htm.
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

"""abydos.phonetic._beider_morse_data.

Behind-the-scenes constants, rules, etc. for the Beider-Morse Phonentic
Matching (BMPM) algorithm

DO NOT EDIT - This document is automatically generated from the reference
implementation in PHP.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

L_NONE = 0
L_ANY = 2 ** 0
L_ARABIC = 2 ** 1
L_CYRILLIC = 2 ** 2
L_CZECH = 2 ** 3
L_DUTCH = 2 ** 4
L_ENGLISH = 2 ** 5
L_FRENCH = 2 ** 6
L_GERMAN = 2 ** 7
L_GREEK = 2 ** 8
L_GREEKLATIN = 2 ** 9
L_HEBREW = 2 ** 10
L_HUNGARIAN = 2 ** 11
L_ITALIAN = 2 ** 12
L_LATVIAN = 2 ** 13
L_POLISH = 2 ** 14
L_PORTUGUESE = 2 ** 15
L_ROMANIAN = 2 ** 16
L_RUSSIAN = 2 ** 17
L_SPANISH = 2 ** 18
L_TURKISH = 2 ** 19

# gen/approxany.php

# GENERIC
# A, E, I, O, P, U should create variants, but a, e, i, o, u should not create any new variant  # noqa: E501
# Q = ü ; Y = ä = ö
# EE = final "e" (english or french)

_GEN_APPROX_ANY = (
    # VOWELS
    # "ALL" DIPHTHONGS are interchangeable BETWEEN THEM and with monophthongs of which they are composed ("D" means "diphthong")  # noqa: E501
    # {a,o} are totally interchangeable if non-stressed; in German "a/o" can actually be from "ä/ö" (that are equivalent to "e")  # noqa: E501
    # {i,e} are interchangeable if non-stressed, while in German "u" can actually be from "ü" (that is equivalent to "i")  # noqa: E501
    ('mb', '', '', '(mb|b[512])'),
    ('mp', '', '', '(mp|b[512])'),
    ('ng', '', '', '(ng|g[512])'),
    ('B', '', '[fktSs]', '(p|f[262144])'),
    ('B', '', 'p', ''),
    ('B', '', '$', '(p|f[262144])'),
    ('V', '', '[pktSs]', '(f|p[262144])'),
    ('V', '', 'f', ''),
    ('V', '', '$', '(f|p[262144])'),
    ('B', '', '', '(b|v[262144])'),
    ('V', '', '', '(v|b[262144])'),
    # French word-final and word-part-final letters
    ('t', '', '$', '(t|[64])'),
    ('g', 'n', '$', '(g|[64])'),
    ('k', 'n', '$', '(k|[64])'),
    ('p', '', '$', '(p|[64])'),
    ('r', '[Ee]', '$', '(r|[64])'),
    ('s', '', '$', '(s|[64])'),
    ('t', '[aeiouAEIOU]', '[^aeiouAEIOU]', '(t|[64])'),  # Petitjean
    ('s', '[aeiouAEIOU]', '[^aeiouAEIOU]', '(s|[64])'),  # Groslot, Grosleau
    # ("p","[aeiouAEIOU]","[^aeiouAEIOU]","(p|[64])"),
    ('I', '[aeiouAEIBFOUQY]', '', 'i'),
    ('I', '', '[^aeiouAEBFIOU]e', '(Q[128]|i|D[32])'),  # "line"
    ('I', '', '$', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk[128])'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts[128])'),
    ('Its', '', '$', 'its'),
    ('I', '', '', '(Q[128]|i)'),
    ('lEE', '[bdfgkmnprsStvzZ]', '', '(li|il[32])'),  # Apple = Appel
    ('rEE', '[bdfgkmnprsStvzZ]', '', '(ri|ir[32])'),
    (
        'lE',
        '[bdfgkmnprsStvzZ]',
        '',
        '(li|il[32]|lY[128])',
    ),  # Applebaum < Appelbaum  # noqa: E501
    ('rE', '[bdfgkmnprsStvzZ]', '', '(ri|ir[32]|rY[128])'),
    ('EE', '', '', '(i|)'),
    ('ea', '', '', '(D|a|i)'),
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('eu', '', '', '(D|e|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('Ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('Oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('Ui', '', '', '(D|u|i)'),
    ('ei', '', '', '(D|i)'),
    ('Ei', '', '', '(D|i)'),
    ('iA', '', '$', '(ia|io)'),
    ('iA', '', '', '(ia|io|iY[128])'),
    ('A', '', '[^aeiouAEBFIOU]e', '(a|o|Y[128]|D[32])'),  # "plane"
    (
        'E',
        'i[^aeiouAEIOU]',
        '',
        '(i|Y[128]|[32])',
    ),  # Wineberg (vineberg/vajneberg) --> vajnberg  # noqa: E501
    (
        'E',
        'a[^aeiouAEIOU]',
        '',
        '(i|Y[128]|[32])',
    ),  # Shaneberg (shaneberg/shejneberg) --> shejnberg  # noqa: E501
    ('E', '', '[fklmnprst]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '', '$', 'i'),
    ('E', '[DaoiuAOIUQY]', '', 'i'),
    ('E', '', '[aoAOQY]', 'i'),
    ('E', '', '', '(i|Y[128])'),
    ('P', '', '', '(o|u)'),
    ('O', '', '[fklmnprstv]$', 'o'),
    ('O', '', 'ts$', 'o'),
    ('O', '', '$', 'o'),
    ('O', '[oeiuQY]', '', 'o'),
    ('O', '', '', '(o|Y[128])'),
    ('O', '', '', 'o'),
    ('A', '', '[fklmnprst]$', '(a|o)'),
    ('A', '', 'ts$', '(a|o)'),
    ('A', '', '$', '(a|o)'),
    ('A', '[oeiuQY]', '', '(a|o)'),
    ('A', '', '', '(a|o|Y[128])'),
    ('A', '', '', '(a|o)'),
    ('U', '', '$', 'u'),
    ('U', '[DoiuQY]', '', 'u'),
    ('U', '', '[^k]$', 'u'),
    ('Uk', '[lr]', '$', '(uk|Qk[128])'),
    ('Uk', '', '$', 'uk'),
    ('sUts', '', '$', '(suts|sQts[128])'),
    ('Uts', '', '$', 'uts'),
    ('U', '', '', '(u|Q[128])'),
    ('U', '', '', 'u'),
    ('e', '', '[fklmnprstv]$', 'i'),
    ('e', '', 'ts$', 'i'),
    ('e', '', '$', 'i'),
    ('e', '[DaoiuAOIUQY]', '', 'i'),
    ('e', '', '[aoAOQY]', 'i'),
    ('e', '', '', '(i|Y[128])'),
    ('a', '', '', '(a|o)'),
)

# gen/approxarabic.php
_GEN_APPROX_ARABIC = (
    ('1a', '', '', '(D|a)'),
    ('1i', '', '', '(D|i|e)'),
    ('1u', '', '', '(D|u|o)'),
    ('j1', '', '', '(ja|je|jo|ju|j)'),
    ('1', '', '', '(a|e|i|o|u|)'),
    ('u', '', '', '(o|u)'),
    ('i', '', '', '(i|e)'),
    ('p', '', '$', 'p'),
    ('p', '', '', '(p|b)'),
)

# gen/approxcommon.php

# GENERIC

_GEN_APPROX_COMMON = (
    # DUTCH
    ('van', '^', '[bp]', '(vam|)'),
    ('van', '^', '', '(van|)'),
    # REGRESSIVE ASSIMILATION OF CONSONANTS
    ('n', '', '[bp]', 'm'),
    # PECULIARITY OF "h"
    ('h', '', '', ''),
    ('H', '', '', '(x|)'),
    # "e" and "i" ARE TO BE OMITTED BEFORE (SYLLABIC) n & l: Halperin=Halpern; Frankel = Frankl, Finkelstein = Finklstein  # noqa: E501
    # but Andersen & Anderson should match
    ('sen', '[rmnl]', '$', '(zn|zon)'),
    ('sen', '', '$', '(sn|son)'),
    ('sEn', '[rmnl]', '$', '(zn|zon)'),
    ('sEn', '', '$', '(sn|son)'),
    ('e', '[BbdfgklmnprsStvzZ]', '[ln]$', ''),
    ('i', '[BbdfgklmnprsStvzZ]', '[ln]$', ''),
    ('E', '[BbdfgklmnprsStvzZ]', '[ln]$', ''),
    ('I', '[BbdfgklmnprsStvzZ]', '[ln]$', ''),
    ('Q', '[BbdfgklmnprsStvzZ]', '[ln]$', ''),
    ('Y', '[BbdfgklmnprsStvzZ]', '[ln]$', ''),
    ('e', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(e|)'),
    ('i', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(i|)'),
    ('E', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(E|)'),
    ('I', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(I|)'),
    ('Q', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(Q|)'),
    ('Y', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(Y|)'),
    # ("e", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
    # ("i", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
    # ("E", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
    # ("I", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
    # ("Q", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
    # ("Y", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
    (
        'lEs',
        '',
        '',
        '(lEs|lz)',
    ),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)  # noqa: E501
    (
        'lE',
        '[bdfgkmnprStvzZ]',
        '',
        '(lE|l)',
    ),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)  # noqa: E501
    # SIMPLIFICATION: (TRIPHTHONGS & DIPHTHONGS) -> ONE GENERIC DIPHTHONG "D"
    ('aue', '', '', 'D'),
    ('oue', '', '', 'D'),
    ('AvE', '', '', '(D|AvE)'),
    ('Ave', '', '', '(D|Ave)'),
    ('avE', '', '', '(D|avE)'),
    ('ave', '', '', '(D|ave)'),
    ('OvE', '', '', '(D|OvE)'),
    ('Ove', '', '', '(D|Ove)'),
    ('ovE', '', '', '(D|ovE)'),
    ('ove', '', '', '(D|ove)'),
    ('ea', '', '', '(D|ea)'),
    ('EA', '', '', '(D|EA)'),
    ('Ea', '', '', '(D|Ea)'),
    ('eA', '', '', '(D|eA)'),
    ('aji', '', '', 'D'),
    ('ajI', '', '', 'D'),
    ('aje', '', '', 'D'),
    ('ajE', '', '', 'D'),
    ('Aji', '', '', 'D'),
    ('AjI', '', '', 'D'),
    ('Aje', '', '', 'D'),
    ('AjE', '', '', 'D'),
    ('oji', '', '', 'D'),
    ('ojI', '', '', 'D'),
    ('oje', '', '', 'D'),
    ('ojE', '', '', 'D'),
    ('Oji', '', '', 'D'),
    ('OjI', '', '', 'D'),
    ('Oje', '', '', 'D'),
    ('OjE', '', '', 'D'),
    ('eji', '', '', 'D'),
    ('ejI', '', '', 'D'),
    ('eje', '', '', 'D'),
    ('ejE', '', '', 'D'),
    ('Eji', '', '', 'D'),
    ('EjI', '', '', 'D'),
    ('Eje', '', '', 'D'),
    ('EjE', '', '', 'D'),
    ('uji', '', '', 'D'),
    ('ujI', '', '', 'D'),
    ('uje', '', '', 'D'),
    ('ujE', '', '', 'D'),
    ('Uji', '', '', 'D'),
    ('UjI', '', '', 'D'),
    ('Uje', '', '', 'D'),
    ('UjE', '', '', 'D'),
    ('iji', '', '', 'D'),
    ('ijI', '', '', 'D'),
    ('ije', '', '', 'D'),
    ('ijE', '', '', 'D'),
    ('Iji', '', '', 'D'),
    ('IjI', '', '', 'D'),
    ('Ije', '', '', 'D'),
    ('IjE', '', '', 'D'),
    ('aja', '', '', 'D'),
    ('ajA', '', '', 'D'),
    ('ajo', '', '', 'D'),
    ('ajO', '', '', 'D'),
    ('aju', '', '', 'D'),
    ('ajU', '', '', 'D'),
    ('Aja', '', '', 'D'),
    ('AjA', '', '', 'D'),
    ('Ajo', '', '', 'D'),
    ('AjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('oja', '', '', 'D'),
    ('ojA', '', '', 'D'),
    ('ojo', '', '', 'D'),
    ('ojO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('Oja', '', '', 'D'),
    ('OjA', '', '', 'D'),
    ('Ojo', '', '', 'D'),
    ('OjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('eja', '', '', 'D'),
    ('ejA', '', '', 'D'),
    ('ejo', '', '', 'D'),
    ('ejO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('Eja', '', '', 'D'),
    ('EjA', '', '', 'D'),
    ('Ejo', '', '', 'D'),
    ('EjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('uja', '', '', 'D'),
    ('ujA', '', '', 'D'),
    ('ujo', '', '', 'D'),
    ('ujO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('Uja', '', '', 'D'),
    ('UjA', '', '', 'D'),
    ('Ujo', '', '', 'D'),
    ('UjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('ija', '', '', 'D'),
    ('ijA', '', '', 'D'),
    ('ijo', '', '', 'D'),
    ('ijO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('Ija', '', '', 'D'),
    ('IjA', '', '', 'D'),
    ('Ijo', '', '', 'D'),
    ('IjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('j', '', '', 'i'),
    # lander = lender = lÃ¤nder
    ('lYndEr', '', '$', 'lYnder'),
    ('lander', '', '$', 'lYnder'),
    ('lAndEr', '', '$', 'lYnder'),
    ('lAnder', '', '$', 'lYnder'),
    ('landEr', '', '$', 'lYnder'),
    ('lender', '', '$', 'lYnder'),
    ('lEndEr', '', '$', 'lYnder'),
    ('lendEr', '', '$', 'lYnder'),
    ('lEnder', '', '$', 'lYnder'),
    # burg = berg
    ('burk', '', '$', '(burk|berk)'),
    ('bUrk', '', '$', '(burk|berk)'),
    ('burg', '', '$', '(burk|berk)'),
    ('bUrg', '', '$', '(burk|berk)'),
    ('Burk', '', '$', '(burk|berk)'),
    ('BUrk', '', '$', '(burk|berk)'),
    ('Burg', '', '$', '(burk|berk)'),
    ('BUrg', '', '$', '(burk|berk)'),
    # CONSONANTS {z & Z; s & S} are approximately interchangeable
    ('s', '', '[rmnl]', 'z'),
    ('S', '', '[rmnl]', 'z'),
    ('s', '[rmnl]', '', 'z'),
    ('S', '[rmnl]', '', 'z'),
    ('dS', '', '$', 'S'),
    ('dZ', '', '$', 'S'),
    ('Z', '', '$', 'S'),
    ('S', '', '$', '(S|s)'),
    ('z', '', '$', '(S|s)'),
    ('S', '', '', 's'),
    ('dZ', '', '', 'z'),
    ('Z', '', '', 'z'),
)

# gen/approxcyrillic.php
# this file uses the same rules as approxrussian.php

# gen/approxczech.php

# this file uses the same rules as approxfrench.php

# gen/approxdutch.php
# this file uses the same rules as approxfrench.php

# gen/approxenglish.php
_GEN_APPROX_ENGLISH = (
    # VOWELS
    ('I', '', '[^aEIeiou]e', '(Q|i|D)'),  # like in "five"
    ('I', '', '$', 'i'),
    ('I', '[aEIeiou]', '', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '', '', '(i|Q)'),
    ('lE', '[bdfgkmnprsStvzZ]', '', '(il|li|lY)'),  # Applebaum < Appelbaum
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    (
        'E',
        'D[^aeiEIou]',
        '',
        '(i|)',
    ),  # Weinberg, Shaneberg (shaneberg/shejneberg) --> shejnberg  # noqa: E501
    ('e', 'D[^aeiEIou]', '', '(i|)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprsStv]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '[DaoiEuQY]', '', 'i'),
    ('E', '', '[aoQY]', 'i'),
    ('E', '', '', '(Y|i)'),
    ('a', '', '', '(a|o)'),
)

# gen/approxfrench.php
# GENERAL
_GEN_APPROX_FRENCH = (
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('a', '', '', '(a|o)'),
    ('e', '', '', 'i'),
)

# gen/approxgerman.php

_GEN_APPROX_GERMAN = (
    ('I', '', '$', 'i'),
    ('I', '[aeiAEIOUouQY]', '', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '', '', '(Q|i)'),
    ('AU', '', '', '(D|a|u)'),
    ('aU', '', '', '(D|a|u)'),
    ('Au', '', '', '(D|a|u)'),
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('OU', '', '', '(D|o|u)'),
    ('oU', '', '', '(D|o|u)'),
    ('Ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('Ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('Oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('Ui', '', '', '(D|u|i)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprst]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '', '$', 'i'),
    ('E', '[DaoAOUiuQY]', '', 'i'),
    ('E', '', '[aoAOQY]', 'i'),
    ('E', '', '', '(Y|i)'),
    ('O', '', '$', 'o'),
    ('O', '', '[fklmnprst]$', 'o'),
    ('O', '', 'ts$', 'o'),
    ('O', '[aoAOUeiuQY]', '', 'o'),
    ('O', '', '', '(o|Y)'),
    ('a', '', '', '(a|o)'),
    ('A', '', '$', '(a|o)'),
    ('A', '', '[fklmnprst]$', '(a|o)'),
    ('A', '', 'ts$', '(a|o)'),
    ('A', '[aoeOUiuQY]', '', '(a|o)'),
    ('A', '', '', '(a|o|Y)'),
    ('U', '', '$', 'u'),
    ('U', '[DaoiuUQY]', '', 'u'),
    ('U', '', '[^k]$', 'u'),
    ('Uk', '[lr]', '$', '(uk|Qk)'),
    ('Uk', '', '$', 'uk'),
    ('sUts', '', '$', '(suts|sQts)'),
    ('Uts', '', '$', 'uts'),
    ('U', '', '', '(u|Q)'),
)

# gen/approxgreek.php

# this file uses the same rules as approxfrench.php

# gen/approxgreeklatin.php
_GEN_APPROX_GREEKLATIN = (('N', '', '', ''),)

# gen/approxhebrew.php
_GEN_APPROX_HEBREW = ()

# gen/approxhungarian.php

# this file uses the same rules as approxfrench.php

# gen/approxitalian.php
# this file uses the same rules as approxfrench.php

# gen/approxlatvian.php
# this file uses the same rules as approxfrench.php

# gen/approxpolish.php
_GEN_APPROX_POLISH = (
    ('aiB', '', '[bp]', '(D|Dm)'),
    ('oiB', '', '[bp]', '(D|Dm)'),
    ('uiB', '', '[bp]', '(D|Dm)'),
    ('eiB', '', '[bp]', '(D|Dm)'),
    ('EiB', '', '[bp]', '(D|Dm)'),
    ('iiB', '', '[bp]', '(D|Dm)'),
    ('IiB', '', '[bp]', '(D|Dm)'),
    ('aiB', '', '[dgkstvz]', '(D|Dn)'),
    ('oiB', '', '[dgkstvz]', '(D|Dn)'),
    ('uiB', '', '[dgkstvz]', '(D|Dn)'),
    ('eiB', '', '[dgkstvz]', '(D|Dn)'),
    ('EiB', '', '[dgkstvz]', '(D|Dn)'),
    ('iiB', '', '[dgkstvz]', '(D|Dn)'),
    ('IiB', '', '[dgkstvz]', '(D|Dn)'),
    ('B', '', '[bp]', '(o|om|im)'),
    ('B', '', '[dgkstvz]', '(o|on|in)'),
    ('B', '', '', 'o'),
    ('aiF', '', '[bp]', '(D|Dm)'),
    ('oiF', '', '[bp]', '(D|Dm)'),
    ('uiF', '', '[bp]', '(D|Dm)'),
    ('eiF', '', '[bp]', '(D|Dm)'),
    ('EiF', '', '[bp]', '(D|Dm)'),
    ('iiF', '', '[bp]', '(D|Dm)'),
    ('IiF', '', '[bp]', '(D|Dm)'),
    ('aiF', '', '[dgkstvz]', '(D|Dn)'),
    ('oiF', '', '[dgkstvz]', '(D|Dn)'),
    ('uiF', '', '[dgkstvz]', '(D|Dn)'),
    ('eiF', '', '[dgkstvz]', '(D|Dn)'),
    ('EiF', '', '[dgkstvz]', '(D|Dn)'),
    ('iiF', '', '[dgkstvz]', '(D|Dn)'),
    ('IiF', '', '[dgkstvz]', '(D|Dn)'),
    ('F', '', '[bp]', '(i|im|om)'),
    ('F', '', '[dgkstvz]', '(i|in|on)'),
    ('F', '', '', 'i'),
    ('P', '', '', '(o|u)'),
    ('I', '', '$', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '[aeiAEBFIou]', '', 'i'),
    ('I', '', '', '(i|Q)'),
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('a', '', '', '(a|o)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprst]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '', '$', 'i'),
    ('E', '[DaoiuQ]', '', 'i'),
    ('E', '', '[aoQ]', 'i'),
    ('E', '', '', '(Y|i)'),
)

# gen/approxportuguese.php

# this file uses the same rules as approxfrench.php

# gen/approxromanian.php
# this file uses the same rules as approxpolish.php

# gen/approxrussian.php

_GEN_APPROX_RUSSIAN = (
    # VOWELS
    ('I', '', '$', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '[aeiEIou]', '', 'i'),
    ('I', '', '', '(i|Q)'),
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('om', '', '[bp]', '(om|im)'),
    ('on', '', '[dgkstvz]', '(on|in)'),
    ('em', '', '[bp]', '(im|om)'),
    ('en', '', '[dgkstvz]', '(in|on)'),
    ('Em', '', '[bp]', '(im|Ym|om)'),
    ('En', '', '[dgkstvz]', '(in|Yn|on)'),
    ('a', '', '', '(a|o)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprsStv]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '[DaoiuQ]', '', 'i'),
    ('E', '', '[aoQ]', 'i'),
    ('E', '', '', '(Y|i)'),
)

# gen/approxspanish.php

_GEN_APPROX_SPANISH = (('B', '', '', '(b|v)'), ('V', '', '', '(b|v)'))

# gen/approxturkish.php
# this file uses the same rules as approxfrench.php

# gen/exactany.php
# GENERAL
# A, E, I, O, P, U should create variants,
# EE = final "e" (english & french)
# V, B from Spanish
# but a, e, i, o, u should not create any new variant
_GEN_EXACT_ANY = (
    ('EE', '', '$', 'e'),
    ('A', '', '', 'a'),
    ('E', '', '', 'e'),
    ('I', '', '', 'i'),
    ('O', '', '', 'o'),
    ('P', '', '', 'o'),
    ('U', '', '', 'u'),
    ('B', '', '[fktSs]', 'p'),
    ('B', '', 'p', ''),
    ('B', '', '$', 'p'),
    ('V', '', '[pktSs]', 'f'),
    ('V', '', 'f', ''),
    ('V', '', '$', 'f'),
    ('B', '', '', 'b'),
    ('V', '', '', 'v'),
)

# gen/exactapproxcommon.php
# GENERAL
_GEN_EXACT_APPROX_COMMON = (
    ('h', '', '$', ''),
    # VOICED - UNVOICED CONSONANTS
    ('b', '', '[fktSs]', 'p'),
    ('b', '', 'p', ''),
    ('b', '', '$', 'p'),
    ('p', '', '[vgdZz]', 'b'),  # Ashk: "v" excluded (everythere)
    ('p', '', 'b', ''),
    ('v', '', '[pktSs]', 'f'),
    ('v', '', 'f', ''),
    ('v', '', '$', 'f'),
    ('f', '', '[vbgdZz]', 'v'),
    ('f', '', 'v', ''),
    ('g', '', '[pftSs]', 'k'),
    ('g', '', 'k', ''),
    ('g', '', '$', 'k'),
    ('k', '', '[vbdZz]', 'g'),
    ('k', '', 'g', ''),
    ('d', '', '[pfkSs]', 't'),
    ('d', '', 't', ''),
    ('d', '', '$', 't'),
    ('t', '', '[vbgZz]', 'd'),
    ('t', '', 'd', ''),
    ('s', '', 'dZ', ''),
    ('s', '', 'tS', ''),
    ('z', '', '[pfkSt]', 's'),
    ('z', '', '[sSzZ]', ''),
    ('s', '', '[sSzZ]', ''),
    ('Z', '', '[sSzZ]', ''),
    ('S', '', '[sSzZ]', ''),
    # SIMPLIFICATION OF CONSONANT CLUSTERS
    ('jnm', '', '', 'jm'),
    # DOUBLE --> SINGLE
    ('ji', '^', '', 'i'),
    ('jI', '^', '', 'I'),
    ('a', '', '[aA]', ''),
    ('a', 'A', '', ''),
    ('A', '', 'A', ''),
    ('b', '', 'b', ''),
    ('d', '', 'd', ''),
    ('f', '', 'f', ''),
    ('g', '', 'g', ''),
    ('j', '', 'j', ''),
    ('k', '', 'k', ''),
    ('l', '', 'l', ''),
    ('m', '', 'm', ''),
    ('n', '', 'n', ''),
    ('p', '', 'p', ''),
    ('r', '', 'r', ''),
    ('t', '', 't', ''),
    ('v', '', 'v', ''),
    ('z', '', 'z', '')
    # do not put name of file here since it always gets merged into another file  # noqa: E501
)

# gen/exactarabic.php
_GEN_EXACT_ARABIC = (('1', '', '', ''),)

# gen/exactcommon.php
# GENERAL

_GEN_EXACT_COMMON = (
    ('H', '', '', ''),
    # VOICED - UNVOICED CONSONANTS
    ('s', '[^t]', '[bgZd]', 'z'),
    ('Z', '', '[pfkst]', 'S'),
    ('Z', '', '$', 'S'),
    ('S', '', '[bgzd]', 'Z'),
    ('z', '', '$', 's'),
    ('ji', '[aAoOeEiIuU]', '', 'j'),
    ('jI', '[aAoOeEiIuU]', '', 'j'),
    ('je', '[aAoOeEiIuU]', '', 'j'),
    ('jE', '[aAoOeEiIuU]', '', 'j'),
)

# gen/exactcyrillic.php
# this file uses the same rules as exactrussian.php

# gen/exactczech.php
# this file uses the same rules as exactrussian.php

# gen/exactdutch.php
_GEN_EXACT_DUTCH = ()

# gen/exactenglish.php
# this file uses the same rules as exactrussian.php

# gen/exactfrench.php
# GENERAL
_GEN_EXACT_FRENCH = ()

# gen/exactgerman.php
# this file uses the same rules as exactany.php

# gen/exactgreek.php
_GEN_EXACT_GREEK = ()

# gen/exactgreeklatin.php
_GEN_EXACT_GREEKLATIN = (('N', '', '', 'n'),)

# gen/exacthebrew.php
_GEN_EXACT_HEBREW = ()

# gen/exacthungarian.php
# this file uses the same rules as exactrussian.php

# gen/exactitalian.php
# GENERAL
_GEN_EXACT_ITALIAN = ()

# gen/exactlatvian.php
# GENERAL
_GEN_EXACT_LATVIAN = ()

# gen/exactpolish.php
_GEN_EXACT_POLISH = (
    ('B', '', '', 'a'),
    ('F', '', '', 'e'),
    ('P', '', '', 'o'),
    ('E', '', '', 'e'),
    ('I', '', '', 'i'),
)

# gen/exactportuguese.php
# GENERAL
_GEN_EXACT_PORTUGUESE = ()

# gen/exactromanian.php
# this file uses the same rules as exactrussian.php

# gen/exactrussian.php
_GEN_EXACT_RUSSIAN = (('E', '', '', 'e'), ('I', '', '', 'i'))

# gen/exactspanish.php
# GENERAL
_GEN_EXACT_SPANISH = (('B', '', '', 'b'), ('V', '', '', 'v'))

# gen/exactturkish.php
_GEN_EXACT_TURKISH = ()

# gen/hebrewcommon.php
# GENERAL

_GEN_HEBREW_COMMON = (
    ('ts', '', '', 'C'),  # for not confusion Gutes [=guts] and Guts [=guc]
    ('tS', '', '', 'C'),  # same reason
    ('S', '', '', 's'),
    ('p', '', '', 'f'),
    ('b', '^', '', 'b'),
    ('b', '', '', '(b|v)'),
    ('B', '', '', '(b|v)'),  # Spanish "b"
    ('V', '', '', 'v'),  # Spanish "v"
    ('EE', '', '', '(1|)'),  # final "e" (english & french)
    ('ja', '', '', 'i'),
    ('jA', '', '', 'i'),
    ('je', '', '', 'i'),
    ('jE', '', '', 'i'),
    ('aj', '', '', 'i'),
    ('Aj', '', '', 'i'),
    ('I', '', '', 'i'),
    ('j', '', '', 'i'),
    ('a', '^', '', '1'),
    ('A', '^', '', '1'),
    ('e', '^', '', '1'),
    ('E', '^', '', '1'),
    ('Y', '^', '', '1'),
    ('a', '', '$', '1'),
    ('A', '', '$', '1'),
    ('e', '', '$', '1'),
    ('E', '', '$', '1'),
    ('Y', '', '$', '1'),
    ('a', '', '', ''),
    ('A', '', '', ''),
    ('e', '', '', ''),
    ('E', '', '', ''),
    ('Y', '', '', ''),
    ('oj', '^', '', '(u|vi)'),
    ('Oj', '^', '', '(u|vi)'),
    ('uj', '^', '', '(u|vi)'),
    ('Uj', '^', '', '(u|vi)'),
    ('oj', '', '', 'u'),
    ('Oj', '', '', 'u'),
    ('uj', '', '', 'u'),
    ('Uj', '', '', 'u'),
    ('ou', '^', '', '(u|v|1)'),
    ('o', '^', '', '(u|v|1)'),
    ('O', '^', '', '(u|v|1)'),
    ('P', '^', '', '(u|v|1)'),
    ('U', '^', '', '(u|v|1)'),
    ('u', '^', '', '(u|v|1)'),
    ('o', '', '$', '(u|1)'),
    ('O', '', '$', '(u|1)'),
    ('P', '', '$', '(u|1)'),
    ('u', '', '$', '(u|1)'),
    ('U', '', '$', '(u|1)'),
    ('ou', '', '', 'u'),
    ('o', '', '', 'u'),
    ('O', '', '', 'u'),
    ('P', '', '', 'u'),
    ('U', '', '', 'u'),
    ('VV', '', '', 'u'),  # alef/ayin + vov from ruleshebrew
    ('V', '', '', 'v'),  # tsvey-vov from ruleshebrew;; only Ashkenazic
    ('L', '^', '', '1'),  # alef/ayin from  ruleshebrew
    ('L', '', '$', '1'),  # alef/ayin from  ruleshebrew
    ('L', '', '', ''),  # alef/ayin from  ruleshebrew
    ('WW', '^', '', '(vi|u)'),  # vav-yod from  ruleshebrew
    ('WW', '', '', 'u'),  # vav-yod from  ruleshebrew
    ('W', '^', '', '(u|v)'),  # vav from  ruleshebrew
    ('W', '', '', 'u'),  # vav from  ruleshebrew
    # ("g","","","(g|Z)"),
    # ("z","","","(z|Z)"),
    # ("d","","","(d|dZ)"),
    ('TB', '^', '', 't'),  # tav from ruleshebrew
    ('TB', '', '', '(t|s)'),  # tav from ruleshebrew; s is only Ashkenazic
    ('T', '', '', 't'),  # tet from  ruleshebrew
    # ("k","","","(k|x)"),
    # ("x","","","(k|x)"),
    ('K', '', '', 'k'),  # kof and initial kaf from ruleshebrew
    ('X', '', '', 'x'),  # khet and final kaf from ruleshebrew
    ('H', '^', '', '(x|1)'),
    ('H', '', '$', '(x|1)'),
    ('H', '', '', '(x|)'),
    ('h', '^', '', '1'),
    ('h', '', '', ''),
)

# gen/lang.php
# GENERIC

# format of entries in $languageRules table is
# (pattern, language, Acceptance)
# where
# pattern is a regular expression
# e.g., ^ means start of word, $ Means End Of Word, [^ei] means anything but e or i, etc.  # noqa: E501
# language is one or more of the languages defined above separated by + signs
# acceptance is true or false
# meaning is:
# if "pattern" matches and acceptance is true, name is in one of the languages indicated and no others  # noqa: E501
# if "pattern" matches and acceptance is false, name is not in any of the languages indicated  # noqa: E501

_GEN_LANGUAGE_RULES = (
    # 1. following are rules to accept the language
    # 1.1 Special letter combinations
    ('^o’', 32, True),
    ('^o\'', 32, True),
    ('^mc', 32, True),
    ('^fitz', 32, True),
    ('ceau', 65600, True),
    ('eau', 65536, True),
    ('ault$', 64, True),
    ('oult$', 64, True),
    ('eux$', 64, True),
    ('eix$', 64, True),
    ('glou$', 512, True),
    ('uu', 16, True),
    ('tx', 262144, True),
    ('witz', 128, True),
    ('tz$', 131232, True),
    ('^tz', 131104, True),
    ('poulos$', 512, True),
    ('pulos$', 512, True),
    ('iou', 512, True),
    ('sj$', 16, True),
    ('^sj', 16, True),
    ('güe', 262144, True),
    ('güi', 262144, True),
    ('ghe', 66048, True),
    ('ghi', 66048, True),
    ('escu$', 65536, True),
    ('esco$', 65536, True),
    ('vici$', 65536, True),
    ('schi$', 65536, True),
    ('ii$', 131072, True),
    ('iy$', 131072, True),
    ('yy$', 131072, True),
    ('yi$', 131072, True),
    ('^rz', 16384, True),
    ('rz$', 16512, True),
    ('[bcdfgklmnpstwz]rz', 16384, True),
    ('rz[bcdfghklmnpstw]', 16384, True),
    ('cki$', 16384, True),
    ('ska$', 16384, True),
    ('cka$', 16384, True),
    ('ae', 131232, True),
    ('oe', 131312, True),
    ('th$', 160, True),
    ('^th', 672, True),
    ('mann', 128, True),
    ('cz', 16384, True),
    ('cy', 16896, True),
    ('niew', 16384, True),
    ('etti$', 4096, True),
    ('eti$', 4096, True),
    ('ati$', 4096, True),
    ('ato$', 4096, True),
    ('[aoei]no$', 4096, True),
    ('[aoei]ni$', 4096, True),
    ('esi$', 4096, True),
    ('oli$', 4096, True),
    ('field$', 32, True),
    ('stein', 128, True),
    ('heim$', 128, True),
    ('heimer$', 128, True),
    ('thal', 128, True),
    ('zweig', 128, True),
    ('[aeou]h', 128, True),
    ('äh', 128, True),
    ('öh', 128, True),
    ('üh', 128, True),
    ('[ln]h[ao]$', 32768, True),
    ('[ln]h[aou]', 819416, True),
    ('chsch', 128, True),
    ('tsch', 128, True),
    ('sch$', 131200, True),
    ('^sch', 131200, True),
    ('ck$', 160, True),
    ('c$', 608264, True),
    ('sz', 18432, True),
    ('cs$', 2048, True),
    ('^cs', 2048, True),
    ('dzs', 2048, True),
    ('zs$', 2048, True),
    ('^zs', 2048, True),
    ('^wl', 16384, True),
    ('^wr', 16560, True),
    ('gy$', 2048, True),
    ('gy[aeou]', 2048, True),
    ('gy', 133696, True),
    ('guy', 64, True),
    ('gu[ei]', 294976, True),
    ('gu[ao]', 294912, True),
    ('gi[aou]', 4608, True),
    ('ly', 150016, True),
    ('ny', 412160, True),
    ('ty', 150016, True),
    # 1.2 special characters
    ('ā', 8192, True),
    ('ć', 16384, True),
    ('ç', 819264, True),
    ('č', 8200, True),
    ('ď', 8, True),
    ('ē', 8192, True),
    ('ğ', 524288, True),
    ('ģ', 8192, True),
    ('ī', 8192, True),
    ('ķ', 8192, True),
    ('ļ', 8192, True),
    ('ł', 16384, True),
    ('ņ', 8192, True),
    ('ń', 16384, True),
    ('ñ', 262144, True),
    ('ň', 8, True),
    ('ř', 8, True),
    ('ś', 16384, True),
    ('ş', 589824, True),
    ('š', 8200, True),
    ('ţ', 65536, True),
    ('ť', 8, True),
    ('ź', 16384, True),
    ('ž', 8200, True),
    ('ż', 16384, True),
    ('ß', 128, True),
    ('ä', 128, True),
    ('á', 297480, True),
    ('â', 98368, True),
    ('ă', 65536, True),
    ('ą', 16384, True),
    ('à', 32768, True),
    ('ã', 32768, True),
    ('ę', 16384, True),
    ('é', 2632, True),
    ('è', 266304, True),
    ('ê', 64, True),
    ('ě', 8, True),
    ('ê', 32832, True),
    ('í', 297480, True),
    ('î', 65600, True),
    ('ı', 524288, True),
    ('ó', 317960, True),
    ('ö', 526464, True),
    ('ô', 32832, True),
    ('õ', 34816, True),
    ('ò', 266240, True),
    ('ű', 2048, True),
    ('ú', 297480, True),
    ('ü', 821376, True),
    ('ù', 64, True),
    ('ů', 8, True),
    ('ý', 520, True),
    # Every Cyrillic word has at least one Cyrillic vowel (аёеоиуыэюя)
    ('а', 4, True),
    ('ё', 4, True),
    ('о', 4, True),
    ('е', 4, True),
    ('и', 4, True),
    ('у', 4, True),
    ('ы', 4, True),
    ('э', 4, True),
    ('ю', 4, True),
    ('я', 4, True),
    # Every Greek word has at least one Greek vowel
    ('α', 256, True),
    ('ε', 256, True),
    ('η', 256, True),
    ('ι', 256, True),
    ('ο', 256, True),
    ('υ', 256, True),
    ('ω', 256, True),
    # Arabic (only initial)
    ('ا', 2, True),  # alif (isol + init)
    ('ب', 2, True),  # ba'
    ('ت', 2, True),  # ta'
    ('ث', 2, True),  # tha'
    ('ج', 2, True),  # jim
    ('ح', 2, True),  # h.a'
    ('خ\'', 2, True),  # kha'
    ('د', 2, True),  # dal (isol + init)
    ('ذ', 2, True),  # dhal (isol + init)
    ('ر', 2, True),  # ra' (isol + init)
    ('ز', 2, True),  # za' (isol + init)
    ('س', 2, True),  # sin
    ('ش', 2, True),  # shin
    ('ص', 2, True),  # s.ad
    ('ض', 2, True),  # d.ad
    ('ط', 2, True),  # t.a'
    ('ظ', 2, True),  # z.a'
    ('ع', 2, True),  # 'ayn
    ('غ', 2, True),  # ghayn
    ('ف', 2, True),  # fa'
    ('ق', 2, True),  # qaf
    ('ك', 2, True),  # kaf
    ('ل', 2, True),  # lam
    ('م', 2, True),  # mim
    ('ن', 2, True),  # nun
    ('ه', 2, True),  # ha'
    ('و', 2, True),  # waw (isol + init)
    ('ي', 2, True),  # ya'
    ('آ', 2, True),  # alif madda
    ('إ', 2, True),  # alif + diacritic
    ('أ', 2, True),  # alif + hamza
    ('ؤ', 2, True),  # waw + hamza
    ('ئ', 2, True),  # ya' + hamza
    # ("لا‎", 2, True), # ligature l+a
    # Hebrew
    ('א', 1024, True),
    ('ב', 1024, True),
    ('ג', 1024, True),
    ('ד', 1024, True),
    ('ה', 1024, True),
    ('ו', 1024, True),
    ('ז', 1024, True),
    ('ח', 1024, True),
    ('ט', 1024, True),
    ('י', 1024, True),
    ('כ', 1024, True),
    ('ל', 1024, True),
    ('מ', 1024, True),
    ('נ', 1024, True),
    ('ס', 1024, True),
    ('ע', 1024, True),
    ('פ', 1024, True),
    ('צ', 1024, True),
    ('ק', 1024, True),
    ('ר', 1024, True),
    ('ש', 1024, True),
    ('ת', 1024, True),
    # 2. following are rules to reject the language
    # Every Latin character word has at least one Latin vowel
    ('a', 1286, False),
    ('o', 1286, False),
    ('e', 1286, False),
    ('i', 1286, False),
    ('y', 75030, False),
    ('u', 1286, False),
    ('j', 4096, False),
    ('j[^aoeiuy]', 295488, False),
    ('g', 8, False),
    ('k', 364608, False),
    ('q', 748056, False),
    ('v', 16384, False),
    ('w', 993864, False),
    ('x', 534552, False),  # polish excluded from the list
    ('dj', 786432, False),
    (
        'v[^aoeiu]',
        128,
        False,
    ),  # in german, "v" can be found before a vowel only  # noqa: E501
    (
        'y[^aoeiu]',
        128,
        False,
    ),  # in german, "y" usually appears only in the last position; sometimes before a vowel  # noqa: E501
    ('c[^aohk]', 128, False),
    ('dzi', 524512, False),
    ('ou', 128, False),
    ('a[eiou]', 524288, False),  # no diphthongs in Turkish
    ('ö[eaiou]', 524288, False),
    ('ü[eaiou]', 524288, False),
    ('e[aiou]', 524288, False),
    ('i[aeou]', 524288, False),
    ('o[aieu]', 524288, False),
    ('u[aieo]', 524288, False),
    ('aj', 240, False),
    ('ej', 240, False),
    ('oj', 240, False),
    ('uj', 240, False),
    ('eu', 147456, False),
    ('ky', 16384, False),
    ('kie', 262720, False),
    ('gie', 360960, False),
    ('ch[aou]', 4096, False),
    ('ch', 524288, False),
    ('son$', 128, False),
    ('sc[ei]', 64, False),
    ('sch', 280640, False),
    ('^h', 131072, False),
)

# gen/languagenames.php
_GEN_LANGUAGES = (
    'any',
    'arabic',
    'cyrillic',
    'czech',
    'dutch',
    'english',
    'french',
    'german',
    'greek',  # noqa: E501
    'greeklatin',
    'hebrew',
    'hungarian',
    'italian',
    'latvian',
    'polish',
    'portuguese',  # noqa: E501
    'romanian',
    'russian',
    'spanish',
    'turkish',
)

# gen/rulesany.php
# format of each entry rule in the table
# (pattern, left context, right context, phonetic)
# where
# pattern is a sequence of characters that might appear in the word to be transliterated  # noqa: E501
# left context is the context that precedes the pattern
# right context is the context that follows the pattern
# phonetic is the result that this rule generates
#
# note that both left context and right context can be regular expressions
# ex: left context of ^ would mean start of word
# left context of [aeiouy] means following a vowel
# right context of [^aeiouy] means preceding a consonant
# right context of e$ means preceding a final e

# GENERIC
_GEN_RULES_ANY = (
    # CONVERTING FEMININE TO MASCULINE
    ('yna', '', '$', '(in[131072]|ina)'),
    ('ina', '', '$', '(in[131072]|ina)'),
    ('liova', '', '$', '(lova|lof[131072]|lef[131072])'),
    ('lova', '', '$', '(lova|lof[131072]|lef[131072]|l[8]|el[8])'),
    ('kova', '', '$', '(kova|kof[131072]|k[8]|ek[8])'),
    ('ova', '', '$', '(ova|of[131072]|[8])'),
    ('ová', '', '$', '(ova|[8])'),
    ('eva', '', '$', '(eva|ef[131072])'),
    ('aia', '', '$', '(aja|i[131072])'),
    ('aja', '', '$', '(aja|i[131072])'),
    ('aya', '', '$', '(aja|i[131072])'),
    ('lowa', '', '$', '(lova|lof[16384]|l[16384]|el[16384])'),
    ('kowa', '', '$', '(kova|kof[16384]|k[16384]|ek[16384])'),
    ('owa', '', '$', '(ova|of[16384]|)'),
    ('lowna', '', '$', '(lovna|levna|l[16384]|el[16384])'),
    ('kowna', '', '$', '(kovna|k[16384]|ek[16384])'),
    ('owna', '', '$', '(ovna|[16384])'),
    ('lówna', '', '$', '(l|el)'),  # polish
    ('kówna', '', '$', '(k|ek)'),  # polish
    ('ówna', '', '$', ''),  # polish
    ('á', '', '$', '(a|i[8])'),
    ('a', '', '$', '(a|i[16392])'),
    # CONSONANTS
    ('pf', '', '', '(pf|p|f)'),
    ('que', '', '$', '(k[64]|ke|kve)'),
    ('qu', '', '', '(kv|k)'),
    ('m', '', '[bfpv]', '(m|n)'),
    ('m', '[aeiouy]', '[aeiouy]', 'm'),
    ('m', '[aeiouy]', '', '(m|n[32832])'),  # nasal
    ('ly', '', '[au]', 'l'),
    ('li', '', '[au]', 'l'),
    ('lio', '', '', '(lo|le[131072])'),
    ('lyo', '', '', '(lo|le[131072])'),
    # ("ll","","","(l|J[262144])"),  # Disabled Argentinian rule
    ('lt', 'u', '$', '(lt|[64])'),
    ('v', '^', '', '(v|f[128]|b[262144])'),
    ('ex', '', '[aáuiíoóeéêy]', '(ez[32768]|eS[32768]|eks|egz)'),
    ('ex', '', '[cs]', '(e[32768]|ek)'),
    ('x', 'u', '$', '(ks|[64])'),
    ('ck', '', '', '(k|tsk[16392])'),
    ('cz', '', '', '(tS|tsz[8])'),  # Polish
    # Proceccing of "h" in various combinations
    ('rh', '^', '', 'r'),
    ('dh', '^', '', 'd'),
    ('bh', '^', '', 'b'),
    ('ph', '', '', '(ph|f)'),
    ('kh', '', '', '(x[131104]|kh)'),
    ('lh', '', '', '(lh|l[32768])'),
    ('nh', '', '', '(nh|nj[32768])'),
    ('ssch', '', '', 'S'),  # german
    ('chsch', '', '', 'xS'),  # german
    ('tsch', '', '', 'tS'),  # german
    # ("desch","^","","deS"),
    # ("desh","^","","(dES|de[64])"),
    # ("des","^","[^aeiouy]","(dEs|de[64])"),
    ('sch', '[aeiouy]', '[ei]', '(S|StS[131072]|sk[69632])'),
    ('sch', '[aeiouy]', '', '(S|StS[131072])'),
    ('sch', '', '[ei]', '(sk[69632]|S|StS[131072])'),
    ('sch', '', '', '(S|StS[131072])'),
    ('ssh', '', '', 'S'),
    ('sh', '', '[äöü]', 'sh'),  # german
    ('sh', '', '[aeiou]', '(S[131104]|sh)'),
    ('sh', '', '', 'S'),
    ('zh', '', '', '(Z[131104]|zh|tsh[128])'),
    ('chs', '', '', '(ks[128]|xs|tSs[131104])'),
    ('ch', '', '[ei]', '(x|tS[393248]|k[69632]|S[32832])'),
    ('ch', '', '', '(x|tS[393248]|S[32832])'),
    ('th', '^', '', 't'),  # english+german+greeklatin
    ('th', '', '[äöüaeiou]', '(t[672]|th)'),
    ('th', '', '', 't'),  # english+german+greeklatin
    ('gh', '', '[ei]', '(g[70144]|gh)'),
    ('ouh', '', '[aioe]', '(v[64]|uh)'),
    ('uh', '', '[aioe]', '(v|uh)'),
    ('h', '', '$', ''),
    ('h', '[aeiouyäöü]', '', ''),  # 128
    ('h', '^', '', '(h|x[66048]|H[381024])'),
    # Processing of "ci", "ce" & "cy"
    ('cia', '', '', '(tSa[16384]|tsa)'),  # Polish
    ('cią', '', '[bp]', '(tSom|tsom)'),  # Polish
    ('cią', '', '', '(tSon[16384]|tson)'),  # Polish
    ('cię', '', '[bp]', '(tSem[16384]|tsem)'),  # Polish
    ('cię', '', '', '(tSen[16384]|tsen)'),  # Polish
    ('cie', '', '', '(tSe[16384]|tse)'),  # Polish
    ('cio', '', '', '(tSo[16384]|tso)'),  # Polish
    ('ciu', '', '', '(tSu[16384]|tsu)'),  # Polish
    (
        'sci',
        '',
        '$',
        '(Si[4096]|stsi[16392]|dZi[524288]|tSi[81920]|tS[65536]|si)',
    ),  # noqa: E501
    ('sc', '', '[ei]', '(S[4096]|sts[16392]|dZ[524288]|tS[81920]|s)'),
    ('ci', '', '$', '(tsi[16392]|dZi[524288]|tSi[81920]|tS[65536]|si)'),
    ('cy', '', '', '(si|tsi[16384])'),
    ('c', '', '[ei]', '(ts[16392]|dZ[524288]|tS[81920]|k[512]|s)'),
    # Processing of "s"
    ('sç', '', '[aeiou]', '(s|stS[524288])'),
    ('ssz', '', '', 'S'),  # polish
    ('sz', '^', '', '(S|s[2048])'),  # polish
    ('sz', '', '$', '(S|s[2048])'),  # polish
    ('sz', '', '', '(S|s[2048]|sts[128])'),  # polish
    ('ssp', '', '', '(Sp[128]|sp)'),
    ('sp', '', '', '(Sp[128]|sp)'),
    ('sst', '', '', '(St[128]|st)'),
    ('st', '', '', '(St[128]|st)'),
    ('ss', '', '', 's'),
    ('sj', '^', '', 'S'),  # dutch
    ('sj', '', '$', 'S'),  # dutch
    ('sj', '', '', '(sj|S[16]|sx[262144]|sZ[589824])'),
    ('sia', '', '', '(Sa[16384]|sa[16384]|sja)'),
    ('sią', '', '[bp]', '(Som[16384]|som)'),  # polish
    ('sią', '', '', '(Son[16384]|son)'),  # polish
    ('się', '', '[bp]', '(Sem[16384]|sem)'),  # polish
    ('się', '', '', '(Sen[16384]|sen)'),  # polish
    ('sie', '', '', '(se|sje|Se[16384]|zi[128])'),
    ('sio', '', '', '(So[16384]|so)'),
    ('siu', '', '', '(Su[16384]|sju)'),
    ('si', '[äöüaáuiíoóeéêy]', '', '(Si[16384]|si|zi[37056])'),
    ('si', '', '', '(Si[16384]|si|zi[128])'),
    ('s', '[aáuiíoóeéêy]', '[aáuíoóeéêy]', '(s|z[37056])'),
    ('s', '', '[aeouäöü]', '(s|z[128])'),
    ('s', '[aeiouy]', '[dglmnrv]', '(s|z|Z[32768]|[64])'),  # Groslot
    ('s', '', '[dglmnrv]', '(s|z|Z[32768])'),
    # Processing of "g"
    ('gue', '', '$', '(k[64]|gve)'),  # portuguese+spanish
    ('gu', '', '[ei]', '(g[64]|gv[294912])'),  # portuguese+spanish
    ('gu', '', '[ao]', 'gv'),  # portuguese+spanish
    ('guy', '', '', 'gi'),  # french
    ('gli', '', '', '(glI|l[4096])'),
    ('gni', '', '', '(gnI|ni[4160])'),
    ('gn', '', '[aeou]', '(n[4160]|nj[4160]|gn)'),
    ('ggie', '', '', '(je[512]|dZe)'),  # dZ is Italian
    ('ggi', '', '[aou]', '(j[512]|dZ)'),  # dZ is Italian
    ('ggi', '[yaeiou]', '[aou]', '(gI|dZ[4096]|j[512])'),
    ('gge', '[yaeiou]', '', '(gE|xe[262144]|gZe[32832]|dZe[331808]|je[512])'),
    ('ggi', '[yaeiou]', '', '(gI|xi[262144]|gZi[32832]|dZi[331808]|i[512])'),
    ('ggi', '', '[aou]', '(gI|dZ[4096]|j[512])'),
    ('gie', '', '$', '(ge|gi[128]|ji[64]|dZe[4096])'),
    ('gie', '', '', '(ge|gi[128]|dZe[4096]|je[512])'),
    ('gi', '', '[aou]', '(i[512]|dZ)'),  # dZ is Italian
    ('ge', '[yaeiou]', '', '(gE|xe[262144]|Ze[32832]|dZe[331808])'),
    ('gi', '[yaeiou]', '', '(gI|xi[262144]|Zi[32832]|dZi[331808])'),
    ('ge', '', '', '(gE|xe[262144]|hE[131072]|je[512]|Ze[32832]|dZe[331808])'),
    ('gi', '', '', '(gI|xi[262144]|hI[131072]|i[512]|Zi[32832]|dZi[331808])'),
    ('gy', '', '[aeouáéóúüöőű]', '(gi|dj[2048])'),
    ('gy', '', '', '(gi|d[2048])'),
    ('g', '[yaeiou]', '[aouyei]', 'g'),
    ('g', '', '[aouei]', '(g|h[131072])'),
    # Processing of "j"
    ('ij', '', '', '(i|ej[16]|ix[262144]|iZ[622656])'),
    ('j', '', '[aoeiuy]', '(j|dZ[32]|x[262144]|Z[622656])'),
    # Processing of "z"
    ('rz', 't', '', '(S[16384]|r)'),  # polish
    ('rz', '', '', '(rz|rts[128]|Z[16384]|r[16384]|rZ[16384])'),
    ('tz', '', '$', '(ts|tS[160])'),
    ('tz', '^', '', '(ts[131232]|tS[160])'),
    ('tz', '', '', '(ts[131232]|tz)'),
    ('zia', '', '[bcdgkpstwzż]', '(Za[16384]|za[16384]|zja)'),
    ('zia', '', '', '(Za[16384]|zja)'),
    ('zią', '', '[bp]', '(Zom[16384]|zom)'),  # polish
    ('zią', '', '', '(Zon[16384]|zon)'),  # polish
    ('zię', '', '[bp]', '(Zem[16384]|zem)'),  # polish
    ('zię', '', '', '(Zen[16384]|zen)'),  # polish
    ('zie', '', '[bcdgkpstwzż]', '(Ze[16384]|ze[16384]|ze|tsi[128])'),
    ('zie', '', '', '(ze|Ze[16384]|tsi[128])'),
    ('zio', '', '', '(Zo[16384]|zo)'),
    ('ziu', '', '', '(Zu[16384]|zju)'),
    ('zi', '', '', '(Zi[16384]|zi|tsi[128]|dzi[4096]|tsi[4096]|si[262144])'),
    (
        'z',
        '',
        '$',
        '(s|ts[128]|ts[4096]|S[32768])',
    ),  # ts It, s/S/Z Port, s in Sp, z Fr  # noqa: E501
    ('z', '', '[bdgv]', '(z|dz[4096]|Z[32768])'),  # dz It, Z/z Port, z Sp & Fr
    ('z', '', '[ptckf]', '(s|ts[4096]|S[32768])'),  # ts It, s/S/z Port, z/s Sp
    # VOWELS
    ('aue', '', '', 'aue'),
    ('oue', '', '', '(oue|ve[64])'),
    ('eau', '', '', 'o'),  # French
    ('ae', '', '', '(Y[128]|aje[131072]|ae)'),
    ('ai', '', '', 'aj'),
    ('au', '', '', '(au|o[64])'),
    ('ay', '', '', 'aj'),
    ('ão', '', '', '(au|an)'),  # Port
    ('ãe', '', '', '(aj|an)'),  # Port
    ('ãi', '', '', '(aj|an)'),  # Port
    ('ea', '', '', '(ea|ja[65536])'),
    ('ee', '', '', '(i[32]|aje[131072]|e)'),
    ('ei', '', '', '(aj|ej)'),
    ('eu', '', '', '(eu|Yj[128]|ej[128]|oj[128]|Y[16])'),
    ('ey', '', '', '(aj|ej)'),
    ('ia', '', '', 'ja'),
    # ("ie","","","(Die[8192]|i[128]|e[16384]|ije[131072]|Q[16]|je)"), # Beider_2017  # noqa: E501
    ('ie', '', '', '(i[128]|e[16384]|ije[131072]|Q[16]|je)'),
    ('ii', '', '$', 'i'),  # russian
    ('io', '', '', '(jo|e[131072])'),
    # ("iu","","","(Diu[8192]|ju)"), # Beider_2017
    ('iu', '', '', 'ju'),
    ('iy', '', '$', 'i'),  # russian
    ('oe', '', '', '(Y[128]|oje[131072]|u[16]|oe)'),
    ('oi', '', '', 'oj'),
    ('oo', '', '', '(u[32]|o)'),
    ('ou', '', '', '(ou|u[576]|au[16])'),
    ('où', '', '', 'u'),  # french
    ('oy', '', '', 'oj'),
    ('õe', '', '', '(oj|on)'),  # Port
    ('ua', '', '', 'va'),
    ('ue', '', '', '(Q[128]|uje[131072]|ve)'),
    # ("ui","","","(Dui[8192]|uj|vi|Y[16])"), # Beider_2017
    ('ui', '', '', '(uj|vi|Y[16])'),
    ('uu', '', '', '(u|Q[16])'),
    ('uo', '', '', '(vo|o)'),
    ('uy', '', '', 'uj'),
    ('ya', '', '', 'ja'),
    ('ye', '', '', '(je|ije[131072])'),
    ('yi', '^', '', 'i'),
    ('yi', '', '$', 'i'),  # russian
    ('yo', '', '', '(jo|e[131072])'),
    ('yu', '', '', 'ju'),
    ('yy', '', '$', 'i'),  # russian
    ('i', '[áóéê]', '', 'j'),
    ('y', '[áóéê]', '', 'j'),
    ('e', '^', '', '(e|je[131072])'),
    ('e', '', '$', '(e|EE[96])'),
    # LANGUAGE SPECIFIC CHARACTERS
    ('ą', '', '[bp]', 'om'),  # polish
    ('ą', '', '', 'on'),  # polish
    ('ä', '', '', '(Y|e)'),
    ('á', '', '', 'a'),  # Port & Sp
    ('à', '', '', 'a'),
    ('â', '', '', 'a'),
    ('ã', '', '', '(a|an)'),  # Port
    ('ă', '', '', '(e[65536]|a)'),  # romanian
    ('ā', '', '', 'a'),  # latvian
    ('č', '', '', 'tS'),  # czech + latvian
    ('ć', '', '', '(tS[16384]|ts)'),  # polish
    ('ç', '', '', '(s|tS[524288])'),
    ('ď', '', '', '(d|dj[8])'),
    ('ę', '', '[bp]', 'em'),  # polish
    ('ę', '', '', 'en'),  # polish
    ('é', '', '', 'e'),
    ('è', '', '', 'e'),
    ('ê', '', '', 'e'),
    ('ě', '', '', '(e|je[8])'),
    ('ē', '', '', 'e'),  # latvian
    ('ģ', '', '', '(d|dj)'),  # latvian
    ('ğ', '', '', ''),  # turkish
    ('í', '', '', 'i'),
    ('î', '', '', 'i'),
    ('ī', '', '', 'i'),  # latvian
    ('ı', '', '', '(i|e[524288]|[524288])'),
    ('ķ', '', '', '(k|t[8192]|tj[8192])'),  # latvian
    # ("ļ","","","(l|lj)"), # latvian Beider_2017
    ('ļ', '', '', 'l'),  # latvian
    ('ł', '', '', 'l'),
    ('ń', '', '', '(n|nj[16384])'),  # polish
    ('ñ', '', '', '(n|nj[262144])'),
    ('ņ', '', '', '(n|nj[8192])'),
    ('ó', '', '', '(u[16384]|o)'),
    ('ô', '', '', 'o'),  # Port & Fr
    ('õ', '', '', '(o|on[32768]|Y[2048])'),
    ('ò', '', '', 'o'),  # Sp & It
    ('ö', '', '', 'Y'),
    ('ř', '', '', '(r|rZ[8])'),
    ('ś', '', '', '(S[16384]|s)'),
    ('ş', '', '', 'S'),  # romanian+turkish
    ('š', '', '', 'S'),  # czech + latvian
    ('ţ', '', '', 'ts'),  # romanian
    ('ť', '', '', '(t|tj[8])'),
    ('ű', '', '', 'Q'),  # hungarian
    ('ü', '', '', '(Q|u[294912])'),
    ('ū', '', '', 'u'),  # latvian
    ('ú', '', '', 'u'),
    ('ů', '', '', 'u'),  # czech
    ('ù', '', '', 'u'),  # french
    ('ý', '', '', 'i'),  # czech
    ('ż', '', '', 'Z'),  # polish
    ('ź', '', '', '(Z[16384]|z)'),
    ('ž', '', '', 'Z'),  # czech + latvian
    ('ß', '', '', 's'),  # german
    ('\'', '', '', ''),  # russian
    ('"', '', '', ''),  # russian
    ('o', '', '[bcćdgklłmnńrsśtwzźż]', '(O|P[16384])'),
    # LATIN ALPHABET
    ('a', '', '', 'A'),
    ('b', '', '', 'B'),
    ('c', '', '', '(k|ts[16392]|dZ[524288])'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    # ("g","","","(g|x[16])"), # Dutch sound disabled
    ('g', '', '', 'g'),
    ('h', '', '', '(h|x[65536]|H[299072])'),
    ('i', '', '', 'I'),
    ('j', '', '', '(j|x[262144]|Z[622656])'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'O'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', '(s|S[32768])'),
    ('t', '', '', 't'),
    ('u', '', '', 'U'),
    ('v', '', '', 'V'),
    ('w', '', '', '(v|w[48])'),
    ('x', '', '', '(ks|gz|S[294912])'),  # S/ks Port & Sp, gz Sp, It only ks
    ('y', '', '', 'i'),
    (
        'z',
        '',
        '',
        '(z|ts[128]|dz[4096]|ts[4096]|s[262144])',
    ),  # ts/dz It, z Port & Fr, z/s Sp  # noqa: E501
)

# gen/rulesarabic.php

# General
_GEN_RULES_ARABIC = (
    ('ا', '', '', 'a'),  # alif isol & init
    ('ب', '', '$', 'b'),
    ('ب', '', '', 'b1'),  # ba' isol
    ('ت', '', '$', 't'),
    ('ت', '', '', 't1'),  # ta' isol
    ('ث', '', '$', 't'),
    ('ث', '', '', 't1'),  # tha' isol
    ('ج', '', '$', '(dZ|Z)'),
    ('ج', '', '', '(dZ1|Z1)'),  # jim isol
    ('ح', '^', '', '1'),
    ('ح', '', '$', '1'),
    ('ح', '', '', '(h1|1)'),  # h.a' isol
    ('خ', '', '$', 'x'),
    ('خ', '', '', 'x1'),  # kha' isol
    ('د', '', '$', 'd'),
    ('د', '', '', 'd1'),  # dal isol & init
    ('ذ', '', '$', 'd'),
    ('ذ', '', '', 'd1'),  # dhal isol & init
    ('ر', '', '$', 'r'),
    ('ر', '', '', 'r1'),  # ra' isol & init
    ('ز', '', '$', 'z'),
    ('ز', '', '', 'z1'),  # za' isol & init
    ('س', '', '$', 's'),
    ('س', '', '', 's1'),  # sin isol
    ('ش', '', '$', 'S'),
    ('ش', '', '', 'S1'),  # shin isol
    ('ص', '', '$', 's'),
    ('ص', '', '', 's1'),  # s.ad isol
    ('ض', '', '$', 'd'),
    ('ض', '', '', 'd1'),  # d.ad isol
    ('ط', '', '$', 't'),
    ('ط', '', '', 't1'),  # t.a' isol
    ('ظ', '', '$', 'z'),
    ('ظ', '', '', 'z1'),  # z.a' isol
    ('ع', '^', '', '1'),
    ('ع', '', '$', '1'),
    ('ع', '', '', '(h1|1)'),  # ayin isol
    ('غ', '', '$', 'g'),
    ('غ', '', '', 'g1'),  # ghayin isol
    ('ف', '', '$', 'f'),
    ('ف', '', '', 'f1'),  # fa' isol
    ('ق', '', '$', 'k'),
    ('ق', '', '', 'k1'),  # qaf isol
    ('ك', '', '$', 'k'),
    ('ك', '', '', 'k1'),  # kaf isol
    ('ل', '', '$', 'l'),
    ('ل', '', '', 'l1'),  # lam isol
    ('م', '', '$', 'm'),
    ('م', '', '', 'm1'),  # mim isol
    ('ن', '', '$', 'n'),
    ('ن', '', '', 'n1'),  # nun isol
    ('ه', '^', '', '1'),
    ('ه', '', '$', '1'),
    ('ه', '', '', '(h1|1)'),  # h isol
    ('و', '', '$', '(u|v)'),
    ('و', '', '', '(u|v1)'),  # waw, isol + init
    ('ي‎', '', '$', '(i|j)'),
    ('ي‎', '', '', '(i|j1)'),  # ya' isol
)

# gen/rulescyrillic.php

# GENERAL
_GEN_RULES_CYRILLIC = (
    ('ця', '', '', 'tsa'),
    ('цю', '', '', 'tsu'),
    ('циа', '', '', 'tsa'),
    ('цие', '', '', 'tse'),
    ('цио', '', '', 'tso'),
    ('циу', '', '', 'tsu'),
    ('сие', '', '', 'se'),
    ('сио', '', '', 'so'),
    ('зие', '', '', 'ze'),
    ('зио', '', '', 'zo'),
    ('с', '', 'с', ''),
    ('гауз', '', '$', 'haus'),
    ('гаус', '', '$', 'haus'),
    ('гольц', '', '$', 'holts'),
    ('геймер', '', '$', '(hejmer|hajmer)'),
    ('гейм', '', '$', '(hejm|hajm)'),
    ('гоф', '', '$', 'hof'),
    ('гер', '', '$', 'ger'),
    ('ген', '', '$', 'gen'),
    ('гин', '', '$', 'gin'),
    ('г', '(й|ё|я|ю|ы|а|е|о|и|у)', '(а|е|о|и|у)', 'g'),
    ('г', '', '(а|е|о|и|у)', '(g|h)'),
    ('ля', '', '', 'la'),
    ('лю', '', '', 'lu'),
    ('лё', '', '', '(le|lo)'),
    ('лио', '', '', '(le|lo)'),
    ('ле', '', '', '(lE|lo)'),
    ('ийе', '', '', 'je'),
    ('ие', '', '', 'je'),
    ('ыйе', '', '', 'je'),
    ('ые', '', '', 'je'),
    ('ий', '', '(а|о|у)', 'j'),
    ('ый', '', '(а|о|у)', 'j'),
    ('ий', '', '$', 'i'),
    ('ый', '', '$', 'i'),
    ('ей', '^', '', '(jej|ej)'),
    ('е', '(а|е|о|у)', '', 'je'),
    ('е', '^', '', 'je'),
    ('эй', '', '', 'ej'),
    ('ей', '', '', 'ej'),
    ('ауе', '', '', 'aue'),
    ('ауэ', '', '', 'aue'),
    ('а', '', '', 'a'),
    ('б', '', '', 'b'),
    ('в', '', '', 'v'),
    ('г', '', '', 'g'),
    ('д', '', '', 'd'),
    ('е', '', '', 'E'),
    ('ё', '', '', '(e|jo)'),
    ('ж', '', '', 'Z'),
    ('з', '', '', 'z'),
    ('и', '', '', 'I'),
    ('й', '', '', 'j'),
    ('к', '', '', 'k'),
    ('л', '', '', 'l'),
    ('м', '', '', 'm'),
    ('н', '', '', 'n'),
    ('о', '', '', 'o'),
    ('п', '', '', 'p'),
    ('р', '', '', 'r'),
    ('с', '', '', 's'),
    ('т', '', '', 't'),
    ('у', '', '', 'u'),
    ('ф', '', '', 'f'),
    ('х', '', '', 'x'),
    ('ц', '', '', 'ts'),
    ('ч', '', '', 'tS'),
    ('ш', '', '', 'S'),
    ('щ', '', '', 'StS'),
    ('ъ', '', '', ''),
    ('ы', '', '', 'I'),
    ('ь', '', '', ''),
    ('э', '', '', 'E'),
    ('ю', '', '', 'ju'),
    ('я', '', '', 'ja'),
)

# gen/rulesczech.php

_GEN_RULES_CZECH = (
    ('ch', '', '', 'x'),
    ('qu', '', '', '(k|kv)'),
    ('aue', '', '', 'aue'),
    ('ei', '', '', '(ej|aj)'),
    ('i', '[aou]', '', 'j'),
    ('i', '', '[aeou]', 'j'),
    ('č', '', '', 'tS'),
    ('š', '', '', 'S'),
    ('ž', '', '', 'Z'),
    ('ň', '', '', 'n'),
    ('ť', '', '', '(t|tj)'),
    ('ď', '', '', '(d|dj)'),
    ('ř', '', '', '(r|rZ)'),
    ('á', '', '', 'a'),
    ('é', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ó', '', '', 'o'),
    ('ú', '', '', 'u'),
    ('ý', '', '', 'i'),
    ('ě', '', '', '(e|je)'),
    ('ů', '', '', 'u'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'ts'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', '(h|g)'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', '(k|kv)'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# gen/rulesdutch.php

_GEN_RULES_DUTCH = (
    # CONSONANTS
    ('ssj', '', '', 'S'),
    ('sj', '', '', 'S'),
    ('ch', '', '', 'x'),
    ('c', '', '[eiy]', 'ts'),
    ('ck', '', '', 'k'),  # German
    ('pf', '', '', '(pf|p|f)'),  # German
    ('ph', '', '', '(ph|f)'),
    ('qu', '', '', 'kv'),
    ('th', '^', '', 't'),  # German
    ('th', '', '[äöüaeiou]', '(t|th)'),  # German
    ('th', '', '', 't'),  # German
    ('ss', '', '', 's'),
    ('h', '[aeiouy]', '', ''),
    # VOWELS
    ('aue', '', '', 'aue'),
    ('ou', '', '', 'au'),
    ('ie', '', '', '(Q|i)'),
    ('uu', '', '', '(Q|u)'),
    ('ee', '', '', 'e'),
    ('eu', '', '', '(Y|Yj)'),  # Dutch Y
    ('aa', '', '', 'a'),
    ('oo', '', '', 'o'),
    ('oe', '', '', 'u'),
    ('ij', '', '', 'ej'),
    ('ui', '', '', '(Y|uj)'),
    ('ei', '', '', '(ej|aj)'),  # Dutch ej
    ('i', '', '[aou]', 'j'),
    ('y', '', '[aeou]', 'j'),
    ('i', '[aou]', '', 'j'),
    ('y', '[aeou]', '', 'j'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', '(g|x)'),
    ('h', '', '', 'h'),
    ('i', '', '', '(i|Q)'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', '(u|Q)'),
    ('v', '', '', 'v'),
    ('w', '', '', '(w|v)'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# gen/rulesenglish.php

# GENERAL
_GEN_RULES_ENGLISH = (
    # CONSONANTS
    ('’', '', '', ''),  # O’Neill
    ('\'', '', '', ''),  # O’Neill
    ('mc', '^', '', 'mak'),  # McDonald
    ('tz', '', '', 'ts'),  # Fitzgerald
    ('tch', '', '', 'tS'),
    ('ch', '', '', '(tS|x)'),
    ('ck', '', '', 'k'),
    ('cc', '', '[iey]', 'ks'),  # success, accent
    ('c', '', 'c', ''),
    ('c', '', '[iey]', 's'),  # circle
    ('gh', '^', '', 'g'),  # ghost
    ('gh', '', '', '(g|f|w)'),  # burgh | tough | bough
    ('gn', '', '', '(gn|n)'),
    ('g', '', '[iey]', '(g|dZ)'),  # get, gem, giant, gigabyte
    # ("th","","","(6|8|t)"),
    ('th', '', '', 't'),
    ('kh', '', '', 'x'),
    ('ph', '', '', 'f'),
    ('sch', '', '', '(S|sk)'),
    ('sh', '', '', 'S'),
    ('who', '^', '', 'hu'),
    ('wh', '^', '', 'w'),
    ('h', '', '$', ''),  # hard to find an example that isn't in a name
    ('h', '', '[^aeiou]', ''),  # hard to find an example that isn't in a name
    ('h', '^', '', 'H'),
    ('kn', '^', '', 'n'),  # knight
    ('mb', '', '$', 'm'),
    ('ng', '', '$', '(N|ng)'),
    ('pn', '^', '', '(pn|n)'),
    ('ps', '^', '', '(ps|s)'),
    ('qu', '', '', 'kw'),
    ('tia', '', '', '(So|Sa)'),
    ('tio', '', '', 'So'),
    ('wr', '^', '', 'r'),
    ('x', '^', '', 'z'),
    # VOWELS
    ('y', '^', '', 'j'),
    ('y', '^', '[aeiouy]', 'j'),
    ('yi', '^', '', 'i'),
    ('aue', '', '', 'aue'),
    ('oue', '', '', '(aue|oue)'),
    ('ai', '', '', '(aj|ej|e)'),  # rain | said
    ('ay', '', '', '(aj|ej)'),
    ('a', '', '[^aeiou]e', 'ej'),  # plane
    ('ei', '', '', '(ej|aj|i)'),  # weigh | receive
    ('ey', '', '', '(ej|aj|i)'),  # hey | barley
    ('ear', '', '', 'ia'),  # tear
    ('ea', '', '', '(i|e)'),  # reason | treasure
    ('ee', '', '', 'i'),  # between
    ('e', '', '[^aeiou]e', 'i'),  # meter
    ('e', '', '$', '(|E)'),  # blame, badge
    ('ie', '', '', 'i'),  # believe
    ('i', '', '[^aeiou]e', 'aj'),  # five
    ('oa', '', '', 'ou'),  # toad
    ('oi', '', '', 'oj'),  # join
    ('oo', '', '', 'u'),  # food
    ('ou', '', '', '(u|ou)'),  # through | tough | could
    ('oy', '', '', 'oj'),  # boy
    ('o', '', '[^aeiou]e', 'ou'),  # rode
    ('u', '', '[^aeiou]e', '(ju|u)'),  # cute | flute
    (
        'u',
        '',
        'r',
        '(e|u)',
    ),  # turn -- Morse disagrees, feels it should go to E  # noqa: E501
    # LATIN ALPHABET
    ('a', '', '', '(e|o|a)'),  # hat | call | part
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),  # candy
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),  # bed
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),
    ('j', '', '', 'dZ'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', '(o|a)'),  # hot
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', '(u|a)'),  # put
    ('v', '', '', 'v'),
    (
        'w',
        '',
        '',
        '(w|v)',
    ),  # the variant "v" is for spellings coming from German/Polish  # noqa: E501
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# gen/rulesfrench.php

# GENERAL
_GEN_RULES_FRENCH = (
    # CONSONANTS
    ('lt', 'u', '$', '(lt|)'),  # Renault
    ('c', 'n', '$', '(k|)'),  # Tronc
    # ("f","","","(f|)"), # Clef
    ('d', '', '$', '(t|)'),  # Durand
    ('g', 'n', '$', '(k|)'),  # Gang
    ('p', '', '$', '(p|)'),  # Trop, Champ
    ('r', 'e', '$', '(r|)'),  # Barbier
    ('t', '', '$', '(t|)'),  # Murat, Constant
    ('z', '', '$', '(s|)'),
    ('ds', '', '$', '(ds|)'),
    ('ps', '', '$', '(ps|)'),  # Champs
    ('rs', 'e', '$', '(rs|)'),
    ('ts', '', '$', '(ts|)'),
    ('s', '', '$', '(s|)'),  # Denis
    ('x', 'u', '$', '(ks|)'),  # Arnoux
    (
        's',
        '[aeéèêiou]',
        '[^aeéèêiou]',
        '(s|)',
    ),  # Deschamps, Malesherbes, Groslot  # noqa: E501
    ('t', '[aeéèêiou]', '[^aeéèêiou]', '(t|)'),  # Petitjean
    ('kh', '', '', 'x'),  # foreign
    ('ph', '', '', 'f'),
    ('ç', '', '', 's'),
    ('x', '', '', 'ks'),
    ('ch', '', '', 'S'),
    ('c', '', '[eiyéèê]', 's'),
    ('gn', '', '', '(n|gn)'),
    ('g', '', '[eiy]', 'Z'),
    ('gue', '', '$', 'k'),
    ('gu', '', '[eiy]', 'g'),
    ('aill', '', 'e', 'aj'),  # non Jewish
    ('ll', '', 'e', '(l|j)'),  # non Jewish
    ('que', '', '$', 'k'),
    ('qu', '', '', 'k'),
    ('s', '[aeiouyéèê]', '[aeiouyéèê]', 'z'),
    ('h', '[bdgt]', '', ''),  # translit from Arabic
    ('m', '[aeiouy]', '[aeiouy]', 'm'),
    ('m', '[aeiouy]', '', '(m|n)'),  # nasal
    ('ou', '', '[aeio]', 'v'),
    ('u', '', '[aeio]', 'v'),
    # VOWELS
    ('aue', '', '', 'aue'),
    ('eau', '', '', 'o'),
    ('au', '', '', '(o|au)'),  # non Jewish
    ('ai', '', '', '(e|aj)'),  # [e] is non Jewish
    ('ay', '', '', '(e|aj)'),  # [e] is non Jewish
    ('é', '', '', 'e'),
    ('ê', '', '', 'e'),
    ('è', '', '', 'e'),
    ('à', '', '', 'a'),
    ('â', '', '', 'a'),
    ('où', '', '', 'u'),
    ('ou', '', '', 'u'),
    ('oi', '', '', '(oj|va)'),  # [va] (actually "ua") is non Jewish
    ('ei', '', '', '(aj|ej|e)'),  # [e] is non Jewish
    ('ey', '', '', '(aj|ej|e)'),  # [e] non Jewish
    ('eu', '', '', '(ej|Y)'),  # non Jewish
    ('y', '[ou]', '', 'j'),
    ('e', '', '$', '(e|)'),
    ('i', '', '[aou]', 'j'),
    ('y', '', '[aoeu]', 'j'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('j', '', '', 'Z'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', '(u|Q)'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# gen/rulesgerman.php

# GENERIC
_GEN_RULES_GERMAN = (
    # CONSONANTS
    ('ewitsch', '', '$', 'evitS'),
    ('owitsch', '', '$', 'ovitS'),
    ('evitsch', '', '$', 'evitS'),
    ('ovitsch', '', '$', 'ovitS'),
    ('witsch', '', '$', 'vitS'),
    ('vitsch', '', '$', 'vitS'),
    ('ssch', '', '', 'S'),
    ('chsch', '', '', 'xS'),
    ('sch', '', '', 'S'),
    ('ziu', '', '', 'tsu'),
    ('zia', '', '', 'tsa'),
    ('zio', '', '', 'tso'),
    ('chs', '', '', 'ks'),
    ('ch', '', '', 'x'),
    ('ck', '', '', 'k'),
    ('c', '', '[eiy]', 'ts'),
    ('sp', '^', '', 'Sp'),
    ('st', '^', '', 'St'),
    ('ssp', '', '', '(Sp|sp)'),
    ('sp', '', '', '(Sp|sp)'),
    ('sst', '', '', '(St|st)'),
    ('st', '', '', '(St|st)'),
    ('pf', '', '', '(pf|p|f)'),
    ('ph', '', '', '(ph|f)'),
    ('qu', '', '', 'kv'),
    ('ewitz', '', '$', '(evits|evitS)'),
    ('ewiz', '', '$', '(evits|evitS)'),
    ('evitz', '', '$', '(evits|evitS)'),
    ('eviz', '', '$', '(evits|evitS)'),
    ('owitz', '', '$', '(ovits|ovitS)'),
    ('owiz', '', '$', '(ovits|ovitS)'),
    ('ovitz', '', '$', '(ovits|ovitS)'),
    ('oviz', '', '$', '(ovits|ovitS)'),
    ('witz', '', '$', '(vits|vitS)'),
    ('wiz', '', '$', '(vits|vitS)'),
    ('vitz', '', '$', '(vits|vitS)'),
    ('viz', '', '$', '(vits|vitS)'),
    ('tz', '', '', 'ts'),
    ('thal', '', '$', 'tal'),
    ('th', '^', '', 't'),
    ('th', '', '[äöüaeiou]', '(t|th)'),
    ('th', '', '', 't'),
    ('rh', '^', '', 'r'),
    ('h', '[aeiouyäöü]', '', ''),
    ('h', '^', '', 'H'),
    ('ss', '', '', 's'),
    ('s', '', '[äöüaeiouy]', '(z|s)'),
    ('s', '[aeiouyäöüj]', '[aeiouyäöü]', 'z'),
    ('ß', '', '', 's'),
    # VOWELS
    ('ij', '', '$', 'i'),
    ('aue', '', '', 'aue'),
    ('ue', '', '', 'Q'),
    ('ae', '', '', 'Y'),
    ('oe', '', '', 'Y'),
    ('ü', '', '', 'Q'),
    ('ä', '', '', '(Y|e)'),
    ('ö', '', '', 'Y'),
    ('ei', '', '', '(aj|ej)'),
    ('ey', '', '', '(aj|ej)'),
    ('eu', '', '', '(Yj|ej|aj|oj)'),
    ('i', '[aou]', '', 'j'),
    ('y', '[aou]', '', 'j'),
    ('ie', '', '', 'I'),
    ('i', '', '[aou]', 'j'),
    ('y', '', '[aoeu]', 'j'),
    # FOREIGN LETTERs
    ('ñ', '', '', 'n'),
    ('ã', '', '', 'a'),
    ('ő', '', '', 'o'),
    ('ű', '', '', 'u'),
    ('ç', '', '', 's'),
    # LATIN ALPHABET
    ('a', '', '', 'A'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'O'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'U'),
    ('v', '', '', '(f|v)'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', 'ts'),
)

# gen/rulesgreek.php

_GEN_RULES_GREEK = (
    (
        'αυ',
        '',
        '$',
        'af',
    ),  # "av" before vowels and voiced consonants, "af" elsewhere  # noqa: E501
    ('αυ', '', '(κ|π|σ|τ|φ|θ|χ|ψ)', 'af'),
    ('αυ', '', '', 'av'),
    (
        'ευ',
        '',
        '$',
        'ef',
    ),  # "ev" before vowels and voiced consonants, "ef" elsewhere  # noqa: E501
    ('ευ', '', '(κ|π|σ|τ|φ|θ|χ|ψ)', 'ef'),
    ('ευ', '', '', 'ev'),
    (
        'ηυ',
        '',
        '$',
        'if',
    ),  # "iv" before vowels and voiced consonants, "if" elsewhere  # noqa: E501
    ('ηυ', '', '(κ|π|σ|τ|φ|θ|χ|ψ)', 'if'),
    ('ηυ', '', '', 'iv'),
    ('ου', '', '', 'u'),  # [u:]
    ('αι', '', '', 'aj'),  # modern [e]
    ('ει', '', '', 'ej'),  # modern [i]
    ('οι', '', '', 'oj'),  # modern [i]
    ('ωι', '', '', 'oj'),
    ('ηι', '', '', 'ej'),
    ('υι', '', '', 'i'),  # modern Greek "i"
    ('γγ', '(ε|ι|η|α|ο|ω|υ)', '(ε|ι|η)', '(nj|j)'),
    ('γγ', '', '(ε|ι|η)', 'j'),
    ('γγ', '(ε|ι|η|α|ο|ω|υ)', '', '(ng|g)'),
    ('γγ', '', '', 'g'),
    ('γκ', '^', '', 'g'),
    ('γκ', '(ε|ι|η|α|ο|ω|υ)', '(ε|ι|η)', '(nj|j)'),
    ('γκ', '', '(ε|ι|η)', 'j'),
    ('γκ', '(ε|ι|η|α|ο|ω|υ)', '', '(ng|g)'),
    ('γκ', '', '', 'g'),
    ('γι', '', '(α|ο|ω|υ)', 'j'),
    ('γι', '', '', '(gi|i)'),
    ('γε', '', '(α|ο|ω|υ)', 'j'),
    ('γε', '', '', '(ge|je)'),
    ('κζ', '', '', 'gz'),
    ('τζ', '', '', 'dz'),
    ('σ', '', '(β|γ|δ|μ|ν|ρ)', 'z'),
    ('μβ', '', '', '(mb|b)'),
    ('μπ', '^', '', 'b'),
    ('μπ', '(ε|ι|η|α|ο|ω|υ)', '', 'mb'),
    ('μπ', '', '', 'b'),  # after any consonant
    ('ντ', '^', '', 'd'),
    ('ντ', '(ε|ι|η|α|ο|ω|υ)', '', '(nd|nt)'),  # Greek is "nd"
    ('ντ', '', '', '(nt|d)'),  # Greek is "d" after any consonant
    ('ά', '', '', 'a'),
    ('έ', '', '', 'e'),
    ('ή', '', '', '(i|e)'),
    ('ί', '', '', 'i'),
    ('ό', '', '', 'o'),
    ('ύ', '', '', '(Q|i|u)'),
    ('ώ', '', '', 'o'),
    ('ΰ', '', '', '(Q|i|u)'),
    ('ϋ', '', '', '(Q|i|u)'),
    ('ϊ', '', '', 'j'),
    ('α', '', '', 'a'),
    ('β', '', '', '(v|b)'),  # modern "v", old "b"
    ('γ', '', '', 'g'),
    ('δ', '', '', 'd'),  # modern like "th" in English "them", old "d"
    ('ε', '', '', 'e'),
    ('ζ', '', '', 'z'),
    ('η', '', '', '(i|e)'),  # modern "i", old "e:"
    ('ι', '', '', 'i'),
    ('κ', '', '', 'k'),
    ('λ', '', '', 'l'),
    ('μ', '', '', 'm'),
    ('ν', '', '', 'n'),
    ('ξ', '', '', 'ks'),
    ('ο', '', '', 'o'),
    ('π', '', '', 'p'),
    ('ρ', '', '', 'r'),
    ('σ', '', '', 's'),
    ('ς', '', '', 's'),
    ('τ', '', '', 't'),
    ('υ', '', '', '(Q|i|u)'),  # modern "i", old like German "ü"
    ('φ', '', '', 'f'),
    ('θ', '', '', 't'),  # old greek like "th" in English "theme"
    ('χ', '', '', 'x'),
    ('ψ', '', '', 'ps'),
    ('ω', '', '', 'o'),
)

# gen/rulesgreeklatin.php

_GEN_RULES_GREEKLATIN = (
    ('au', '', '$', 'af'),
    ('au', '', '[kpstfh]', 'af'),
    ('au', '', '', 'av'),
    ('eu', '', '$', 'ef'),
    ('eu', '', '[kpstfh]', 'ef'),
    ('eu', '', '', 'ev'),
    ('ou', '', '', 'u'),
    ('gge', '[aeiouy]', '', '(nje|je)'),  # aggelopoulos
    ('ggi', '[aeiouy]', '[aou]', '(nj|j)'),
    ('ggi', '[aeiouy]', '', '(ni|i)'),
    ('gge', '', '', 'je'),
    ('ggi', '', '', 'i'),
    ('gg', '[aeiouy]', '', '(ng|g)'),
    ('gg', '', '', 'g'),
    ('gk', '^', '', 'g'),
    ('gke', '[aeiouy]', '', '(nje|je)'),
    ('gki', '[aeiouy]', '', '(ni|i)'),
    ('gke', '', '', 'je'),
    ('gki', '', '', 'i'),
    ('gk', '[aeiouy]', '', '(ng|g)'),
    ('gk', '', '', 'g'),
    ('nghi', '', '[aouy]', 'Nj'),
    ('nghi', '', '', '(Ngi|Ni)'),
    ('nghe', '', '[aouy]', 'Nj'),
    ('nghe', '', '', '(Nje|Nge)'),
    ('ghi', '', '[aouy]', 'j'),
    ('ghi', '', '', '(gi|i)'),
    ('ghe', '', '[aouy]', 'j'),
    ('ghe', '', '', '(je|ge)'),
    ('ngh', '', '', 'Ng'),
    ('gh', '', '', 'g'),
    ('ngi', '', '[aouy]', 'Nj'),
    ('ngi', '', '', '(Ngi|Ni)'),
    ('nge', '', '[aouy]', 'Nj'),
    ('nge', '', '', '(Nje|Nge)'),
    ('gi', '', '[aouy]', 'j'),
    ('gi', '', '', '(gi|i)'),  # what about Pantazis = Pantagis ???
    ('ge', '', '[aouy]', 'j'),
    ('ge', '', '', '(je|ge)'),
    (
        'ng',
        '',
        '',
        'Ng',
    ),  # fragakis = fraggakis = frangakis; angel = agel = aggel  # noqa: E501
    ('i', '', '[aeou]', 'j'),
    ('i', '[aeou]', '', 'j'),
    ('y', '', '[aeou]', 'j'),
    ('y', '[aeou]', '', 'j'),
    ('yi', '', '[aeou]', 'j'),
    ('yi', '', '', 'i'),
    ('ch', '', '', 'x'),
    ('kh', '', '', 'x'),
    ('dh', '', '', 'd'),  # actually as "th" in English "that"
    ('dj', '', '', 'dZ'),  # Turkish words
    ('ph', '', '', 'f'),
    ('th', '', '', 't'),
    ('kz', '', '', 'gz'),
    ('tz', '', '', 'dz'),
    ('s', '', '[bgdmnr]', 'z'),
    ('mb', '', '', '(mb|b)'),  # Liberis = Limperis = Limberis
    ('mp', '^', '', 'b'),
    ('mp', '[aeiouy]', '', 'mp'),
    ('mp', '', '', 'b'),
    ('nt', '^', '', 'd'),
    ('nt', '[aeiouy]', '', '(nd|nt)'),  # Greek "nd"
    ('nt', '', '', '(nt|d)'),  # Greek "d" after any consonant
    ('á', '', '', 'a'),
    ('é', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ó', '', '', 'o'),
    ('óu', '', '', 'u'),
    ('ú', '', '', 'u'),
    ('ý', '', '', '(i|Q|u)'),  # [ü]
    ('a', '', '', 'a'),
    ('b', '', '', '(b|v)'),  # beta: modern "v", old "b"
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),  # modern like "th" in English "them", old "d"
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'x'),
    ('i', '', '', 'i'),
    (
        'j',
        '',
        '',
        '(j|Z)',
    ),  # Panajotti = Panaiotti; Louijos = Louizos; Pantajis = Pantazis = Pantagis  # noqa: E501
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('ο', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),  # foreign
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),  # foreign
    ('x', '', '', 'ks'),
    ('y', '', '', '(i|Q|u)'),  # [ü]
    ('z', '', '', 'z'),
)

# gen/ruleshebrew.php

# General = Ashkenazic
_GEN_RULES_HEBREW = (
    ('אי', '', '', 'i'),
    ('עי', '', '', 'i'),
    ('עו', '', '', 'VV'),
    ('או', '', '', 'VV'),
    ('ג׳', '', '', 'Z'),
    ('ד׳', '', '', 'dZ'),
    ('א', '', '', 'L'),
    ('ב', '', '', 'b'),
    ('ג', '', '', 'g'),
    ('ד', '', '', 'd'),
    ('ה', '^', '', '1'),
    ('ה', '', '$', '1'),
    ('ה', '', '', ''),
    ('וו', '', '', 'V'),
    ('וי', '', '', 'WW'),
    ('ו', '', '', 'W'),
    ('ז', '', '', 'z'),
    ('ח', '', '', 'X'),
    ('ט', '', '', 'T'),
    ('יי', '', '', 'i'),
    ('י', '', '', 'i'),
    ('ך', '', '', 'X'),
    ('כ', '^', '', 'K'),
    ('כ', '', '', 'k'),
    ('ל', '', '', 'l'),
    ('ם', '', '', 'm'),
    ('מ', '', '', 'm'),
    ('ן', '', '', 'n'),
    ('נ', '', '', 'n'),
    ('ס', '', '', 's'),
    ('ע', '', '', 'L'),
    ('ף', '', '', 'f'),
    ('פ', '', '', 'f'),
    ('ץ', '', '', 'C'),
    ('צ', '', '', 'C'),
    ('ק', '', '', 'K'),
    ('ר', '', '', 'r'),
    ('ש', '', '', 's'),
    ('ת', '', '', 'TB'),  # only Ashkenazic
)

# gen/ruleshungarian.php

# GENERAL
_GEN_RULES_HUNGARIAN = (
    # CONSONANTS
    ('sz', '', '', 's'),
    ('zs', '', '', 'Z'),
    ('cs', '', '', 'tS'),
    ('ay', '', '', '(oj|aj)'),
    ('ai', '', '', '(oj|aj)'),
    ('aj', '', '', '(oj|aj)'),
    ('ei', '', '', '(aj|ej)'),  # German element
    ('ey', '', '', '(aj|ej)'),  # German element
    ('y', '[áo]', '', 'j'),
    ('i', '[áo]', '', 'j'),
    ('ee', '', '', '(ej|e)'),
    ('ely', '', '', '(ej|eli)'),
    ('ly', '', '', '(j|li)'),
    ('gy', '', '[aeouáéóúüöőű]', 'dj'),
    ('gy', '', '', '(d|gi)'),
    ('ny', '', '[aeouáéóúüöőű]', 'nj'),
    ('ny', '', '', '(n|ni)'),
    ('ty', '', '[aeouáéóúüöőű]', 'tj'),
    ('ty', '', '', '(t|ti)'),
    ('qu', '', '', '(ku|kv)'),
    ('h', '', '$', ''),
    # SPECIAL VOWELS
    ('á', '', '', 'a'),
    ('é', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ó', '', '', 'o'),
    ('ú', '', '', 'u'),
    ('ö', '', '', 'Y'),
    ('ő', '', '', 'Y'),
    ('ü', '', '', 'Q'),
    ('ű', '', '', 'Q'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'ts'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', '(S|s)'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# gen/rulesitalian.php

_GEN_RULES_ITALIAN = (
    ('kh', '', '', 'x'),  # foreign
    ('gli', '', '', '(l|gli)'),
    ('gn', '', '[aeou]', '(n|nj|gn)'),
    ('gni', '', '', '(ni|gni)'),
    ('gi', '', '[aeou]', 'dZ'),
    ('gg', '', '[ei]', 'dZ'),
    ('g', '', '[ei]', 'dZ'),
    ('h', '[bdgt]', '', 'g'),  # gh is It; others from Arabic translit
    ('h', '', '$', ''),  # foreign
    ('ci', '', '[aeou]', 'tS'),
    ('ch', '', '[ei]', 'k'),
    ('sc', '', '[ei]', 'S'),
    ('cc', '', '[ei]', 'tS'),
    ('c', '', '[ei]', 'tS'),
    ('s', '[aeiou]', '[aeiou]', 'z'),
    ('i', '[aeou]', '', 'j'),
    ('i', '', '[aeou]', 'j'),
    ('y', '[aeou]', '', 'j'),  # foreign
    ('y', '', '[aeou]', 'j'),  # foreign
    ('qu', '', '', 'k'),
    ('uo', '', '', '(vo|o)'),
    ('u', '', '[aei]', 'v'),
    ('è', '', '', 'e'),
    ('é', '', '', 'e'),
    ('ò', '', '', 'o'),
    ('ó', '', '', 'o'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('j', '', '', '(Z|dZ|j)'),  # foreign
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),  # foreign
    ('x', '', '', 'ks'),  # foreign
    ('y', '', '', 'i'),  # foreign
    ('z', '', '', '(ts|dz)'),
)

# gen/ruleslatvian.php

# GENERAL
_GEN_RULES_LATVIAN = (
    # CONSONANTS
    ('č', '', '', 'tS'),
    ('ģ', '', '', '(d|dj)'),
    # ("ķ","","","(t|ti)"),
    ('ķ', '', '', '(t|tj)'),
    # ("ļ","","","lj"),
    ('ļ', '', '', 'l'),
    ('š', '', '', 'S'),
    ('ņ', '', '', '(n|nj)'),
    ('ž', '', '', 'Z'),
    # SPECIAL VOWELS
    ('ā', '', '', 'a'),
    ('ē', '', '', 'e'),
    ('ī', '', '', 'i'),
    ('ū', '', '', 'u'),
    # DIPHTONGS
    # ("ai","","","(D|ai)"),
    ('ai', '', '', 'aj'),
    # ("ei","","","(D|ei)"),
    ('ei', '', '', 'ej'),
    ('io', '', '', 'jo'),
    # ("iu","","","(D|iu)"),
    ('iu', '', '', 'ju'),
    # ("ie","","","(D|ie)"),
    ('ie', '', '', 'je'),
    # ("o","","","(D|uo)"),
    ('o', '', '', 'o'),
    # ("ui","","","(D|ui)"),
    ('ui', '', '', 'uj'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'ts'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('p', '', '', 'p'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('z', '', '', 'z'),
)

# gen/rulespolish.php

# GENERIC
_GEN_RULES_POLISH = (
    # CONVERTING FEMININE TO MASCULINE
    ('ska', '', '$', 'ski'),
    ('cka', '', '$', 'tski'),
    ('lowa', '', '$', '(lova|lof|l|el)'),
    ('kowa', '', '$', '(kova|kof|k|ek)'),
    ('owa', '', '$', '(ova|of|)'),
    ('lowna', '', '$', '(lovna|levna|l|el)'),
    ('kowna', '', '$', '(kovna|k|ek)'),
    ('owna', '', '$', '(ovna|)'),
    ('lówna', '', '$', '(l|el)'),
    ('kówna', '', '$', '(k|ek)'),
    ('ówna', '', '$', ''),
    ('a', '', '$', '(a|i)'),
    # CONSONANTS
    ('czy', '', '', 'tSi'),
    ('cze', '', '[bcdgkpstwzż]', '(tSe|tSF)'),
    ('ciewicz', '', '', '(tsevitS|tSevitS)'),
    ('siewicz', '', '', '(sevitS|SevitS)'),
    ('ziewicz', '', '', '(zevitS|ZevitS)'),
    ('riewicz', '', '', 'rjevitS'),
    ('diewicz', '', '', 'djevitS'),
    ('tiewicz', '', '', 'tjevitS'),
    ('iewicz', '', '', 'evitS'),
    ('ewicz', '', '', 'evitS'),
    ('owicz', '', '', 'ovitS'),
    ('icz', '', '', 'itS'),
    ('cz', '', '', 'tS'),
    ('ch', '', '', 'x'),
    ('cia', '', '[bcdgkpstwzż]', '(tSB|tsB)'),
    ('cia', '', '', '(tSa|tsa)'),
    ('cią', '', '[bp]', '(tSom|tsom)'),
    ('cią', '', '', '(tSon|tson)'),
    ('cię', '', '[bp]', '(tSem|tsem)'),
    ('cię', '', '', '(tSen|tsen)'),
    ('cie', '', '[bcdgkpstwzż]', '(tSF|tsF)'),
    ('cie', '', '', '(tSe|tse)'),
    ('cio', '', '', '(tSo|tso)'),
    ('ciu', '', '', '(tSu|tsu)'),
    ('ci', '', '', '(tSi|tsI)'),
    ('ć', '', '', '(tS|ts)'),
    ('ssz', '', '', 'S'),
    ('sz', '', '', 'S'),
    ('sia', '', '[bcdgkpstwzż]', '(SB|sB|sja)'),
    ('sia', '', '', '(Sa|sja)'),
    ('sią', '', '[bp]', '(Som|som)'),
    ('sią', '', '', '(Son|son)'),
    ('się', '', '[bp]', '(Sem|sem)'),
    ('się', '', '', '(Sen|sen)'),
    ('sie', '', '[bcdgkpstwzż]', '(SF|sF|se)'),
    ('sie', '', '', '(Se|se)'),
    ('sio', '', '', '(So|so)'),
    ('siu', '', '', '(Su|sju)'),
    ('si', '', '', '(Si|sI)'),
    ('ś', '', '', '(S|s)'),
    ('zia', '', '[bcdgkpstwzż]', '(ZB|zB|zja)'),
    ('zia', '', '', '(Za|zja)'),
    ('zią', '', '[bp]', '(Zom|zom)'),
    ('zią', '', '', '(Zon|zon)'),
    ('zię', '', '[bp]', '(Zem|zem)'),
    ('zię', '', '', '(Zen|zen)'),
    ('zie', '', '[bcdgkpstwzż]', '(ZF|zF)'),
    ('zie', '', '', '(Ze|ze)'),
    ('zio', '', '', '(Zo|zo)'),
    ('ziu', '', '', '(Zu|zju)'),
    ('zi', '', '', '(Zi|zI)'),
    ('że', '', '[bcdgkpstwzż]', '(Ze|ZF)'),
    ('że', '', '[bcdgkpstwzż]', '(Ze|ZF|ze|zF)'),
    ('że', '', '', 'Ze'),
    ('źe', '', '', '(Ze|ze)'),
    ('ży', '', '', 'Zi'),
    ('źi', '', '', '(Zi|zi)'),
    ('ż', '', '', 'Z'),
    ('ź', '', '', '(Z|z)'),
    ('rze', 't', '', '(Se|re)'),
    ('rze', '', '', '(Ze|re|rZe)'),
    ('rzy', 't', '', '(Si|ri)'),
    ('rzy', '', '', '(Zi|ri|rZi)'),
    ('rz', 't', '', '(S|r)'),
    ('rz', '', '', '(Z|r|rZ)'),
    ('lio', '', '', '(lo|le)'),
    ('ł', '', '', 'l'),
    ('ń', '', '', 'n'),
    ('qu', '', '', 'k'),
    ('s', '', 's', ''),
    # VOWELS
    ('ó', '', '', '(u|o)'),
    ('ą', '', '[bp]', 'om'),
    ('ę', '', '[bp]', 'em'),
    ('ą', '', '', 'on'),
    ('ę', '', '', 'en'),
    ('ije', '', '', 'je'),
    ('yje', '', '', 'je'),
    ('iie', '', '', 'je'),
    ('yie', '', '', 'je'),
    ('iye', '', '', 'je'),
    ('yye', '', '', 'je'),
    ('ij', '', '[aou]', 'j'),
    ('yj', '', '[aou]', 'j'),
    ('ii', '', '[aou]', 'j'),
    ('yi', '', '[aou]', 'j'),
    ('iy', '', '[aou]', 'j'),
    ('yy', '', '[aou]', 'j'),
    ('rie', '', '', 'rje'),
    ('die', '', '', 'dje'),
    ('tie', '', '', 'tje'),
    ('ie', '', '[bcdgkpstwzż]', 'F'),
    ('ie', '', '', 'e'),
    ('aue', '', '', 'aue'),
    ('au', '', '', 'au'),
    ('ei', '', '', 'aj'),
    ('ey', '', '', 'aj'),
    ('ej', '', '', 'aj'),
    ('ai', '', '', 'aj'),
    ('ay', '', '', 'aj'),
    ('aj', '', '', 'aj'),
    ('i', '[aeou]', '', 'j'),
    ('y', '[aeou]', '', 'j'),
    ('i', '', '[aou]', 'j'),
    ('y', '', '[aeou]', 'j'),
    ('a', '', '[bcdgkpstwzż]', 'B'),
    ('e', '', '[bcdgkpstwzż]', '(E|F)'),
    ('o', '', '[bcćdgklłmnńrsśtwzźż]', 'P'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'ts'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', '(h|x)'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'I'),
    ('z', '', '', 'z'),
)

# gen/rulesportuguese.php

_GEN_RULES_PORTUGUESE = (
    ('kh', '', '', 'x'),  # foreign
    ('ch', '', '', 'S'),
    ('ss', '', '', 's'),
    ('sc', '', '[ei]', 's'),
    ('sç', '', '[aou]', 's'),
    ('ç', '', '', 's'),
    ('c', '', '[ei]', 's'),
    # ("c","","[aou]","(k|C)"),
    ('s', '^', '', 's'),
    ('s', '[aáuiíoóeéêy]', '[aáuiíoóeéêy]', 'z'),
    ('s', '', '[dglmnrv]', '(Z|S)'),  # Z is Brazil
    ('z', '', '$', '(Z|s|S)'),  # s and S in Brazil
    ('z', '', '[bdgv]', '(Z|z)'),  # Z in Brazil
    ('z', '', '[ptckf]', '(s|S|z)'),  # s and S in Brazil
    ('gu', '', '[eiu]', 'g'),
    ('gu', '', '[ao]', 'gv'),
    ('g', '', '[ei]', 'Z'),
    ('qu', '', '[eiu]', 'k'),
    ('qu', '', '[ao]', 'kv'),
    ('uo', '', '', '(vo|o|u)'),
    ('u', '', '[aei]', 'v'),
    ('lh', '', '', 'l'),
    ('nh', '', '', 'nj'),
    ('h', '[bdgt]', '', ''),  # translit. from Arabic
    ('h', '', '$', ''),  # foreign
    ('ex', '', '[aáuiíoóeéêy]', '(ez|eS|eks)'),  # ez in Brazil
    ('ex', '', '[cs]', 'e'),
    ('y', '[aáuiíoóeéê]', '', 'j'),
    ('y', '', '[aeiíou]', 'j'),
    (
        'm',
        '',
        '[bcdfglnprstv]',
        '(m|n)',
    ),  # maybe to add a rule for m/n before a consonant that disappears [preceeding vowel becomes nasalized]  # noqa: E501
    (
        'm',
        '',
        '$',
        '(m|n)',
    ),  # maybe to add a rule for final m/n that disappears [preceeding vowel becomes nasalized]  # noqa: E501
    ('ão', '', '', '(au|an|on)'),
    ('ãe', '', '', '(aj|an)'),
    ('ãi', '', '', '(aj|an)'),
    ('õe', '', '', '(oj|on)'),
    ('i', '[aáuoóeéê]', '', 'j'),
    ('i', '', '[aeou]', 'j'),
    ('â', '', '', 'a'),
    ('à', '', '', 'a'),
    ('á', '', '', 'a'),
    ('ã', '', '', '(a|an|on)'),
    ('é', '', '', 'e'),
    ('ê', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ô', '', '', 'o'),
    ('ó', '', '', 'o'),
    ('õ', '', '', '(o|on)'),
    ('ú', '', '', 'u'),
    ('ü', '', '', 'u'),
    ('aue', '', '', 'aue'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', '(e|i)'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('j', '', '', 'Z'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', '(o|u)'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 'S'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', '(S|ks)'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# gen/rulesromanian.php

# GENERAL
_GEN_RULES_ROMANIAN = (
    ('ce', '', '', 'tSe'),
    ('ci', '', '', '(tSi|tS)'),
    ('ch', '', '[ei]', 'k'),
    ('ch', '', '', 'x'),  # foreign
    ('gi', '', '', '(dZi|dZ)'),
    ('g', '', '[ei]', 'dZ'),
    ('gh', '', '', 'g'),
    ('i', '[aeou]', '', 'j'),
    ('i', '', '[aeou]', 'j'),
    ('ţ', '', '', 'ts'),
    ('ş', '', '', 'S'),
    ('qu', '', '', 'k'),
    ('î', '', '', 'i'),
    ('ea', '', '', 'ja'),
    ('ă', '', '', '(e|a)'),
    ('aue', '', '', 'aue'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', '(x|h)'),
    ('i', '', '', 'I'),
    ('j', '', '', 'Z'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# gen/rulesrussian.php

# GENERAL
_GEN_RULES_RUSSIAN = (
    # CONVERTING FEMININE TO MASCULINE
    ('yna', '', '$', '(in|ina)'),
    ('ina', '', '$', '(in|ina)'),
    ('liova', '', '$', '(lof|lef)'),
    ('lova', '', '$', '(lof|lef|lova)'),
    ('ova', '', '$', '(of|ova)'),
    ('eva', '', '$', '(ef|ova)'),
    ('aia', '', '$', '(aja|i)'),
    ('aja', '', '$', '(aja|i)'),
    ('aya', '', '$', '(aja|i)'),
    # SPECIAL CONSONANTS
    ('tsya', '', '', 'tsa'),
    ('tsyu', '', '', 'tsu'),
    ('tsia', '', '', 'tsa'),
    ('tsie', '', '', 'tse'),
    ('tsio', '', '', 'tso'),
    ('tsye', '', '', 'tse'),
    ('tsyo', '', '', 'tso'),
    ('tsiu', '', '', 'tsu'),
    ('sie', '', '', 'se'),
    ('sio', '', '', 'so'),
    ('zie', '', '', 'ze'),
    ('zio', '', '', 'zo'),
    ('sye', '', '', 'se'),
    ('syo', '', '', 'so'),
    ('zye', '', '', 'ze'),
    ('zyo', '', '', 'zo'),
    ('ger', '', '$', 'ger'),
    ('gen', '', '$', 'gen'),
    ('gin', '', '$', 'gin'),
    ('gg', '', '', 'g'),
    ('g', '[jaeoiuy]', '[aeoiu]', 'g'),
    ('g', '', '[aeoiu]', '(g|h)'),
    ('kh', '', '', 'x'),
    ('ch', '', '', '(tS|x)'),
    ('sch', '', '', '(StS|S)'),
    ('ssh', '', '', 'S'),
    ('sh', '', '', 'S'),
    ('zh', '', '', 'Z'),
    ('tz', '', '$', 'ts'),
    ('tz', '', '', '(ts|tz)'),
    ('c', '', '[iey]', 's'),
    ('qu', '', '', '(kv|k)'),
    ('s', '', 's', ''),
    # SPECIAL VOWELS
    ('lya', '', '', 'la'),
    ('lyu', '', '', 'lu'),
    ('lia', '', '', 'la'),  # not in DJSRE
    ('liu', '', '', 'lu'),  # not in DJSRE
    ('lja', '', '', 'la'),  # not in DJSRE
    ('lju', '', '', 'lu'),  # not in DJSRE
    ('le', '', '', '(lo|lE)'),  # not in DJSRE
    ('lyo', '', '', '(lo|le)'),  # not in DJSRE
    ('lio', '', '', '(lo|le)'),
    ('ije', '', '', 'je'),
    ('ie', '', '', 'je'),
    ('iye', '', '', 'je'),
    ('iie', '', '', 'je'),
    ('yje', '', '', 'je'),
    ('ye', '', '', 'je'),
    ('yye', '', '', 'je'),
    ('yie', '', '', 'je'),
    ('ij', '', '[aou]', 'j'),
    ('iy', '', '[aou]', 'j'),
    ('ii', '', '[aou]', 'j'),
    ('yj', '', '[aou]', 'j'),
    ('yy', '', '[aou]', 'j'),
    ('yi', '', '[aou]', 'j'),
    ('io', '', '', '(jo|e)'),
    ('i', '', '[au]', 'j'),
    ('i', '[aeou]', '', 'j'),
    ('yo', '', '', '(jo|e)'),
    ('y', '', '[au]', 'j'),
    ('y', '[aeiou]', '', 'j'),
    ('ii', '', '$', 'i'),
    ('iy', '', '$', 'i'),
    ('yy', '', '$', 'i'),
    ('yi', '', '$', 'i'),
    ('yj', '', '$', 'i'),
    ('ij', '', '$', 'i'),
    ('e', '^', '', '(je|E)'),
    ('ee', '', '', '(aje|i)'),
    ('e', '[aou]', '', 'je'),
    ('oo', '', '', '(oo|u)'),
    ('\'', '', '', ''),
    ('"', '', '', ''),
    ('aue', '', '', 'aue'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'I'),
    ('z', '', '', 'z'),
)

# gen/rulesspanish.php

# GENERAL
_GEN_RULES_SPANISH = (
    # Includes both Spanish (Castillian) & Catalan
    # CONSONANTS
    ('ñ', '', '', '(n|nj)'),
    ('ny', '', '', 'nj'),  # Catalan
    ('ç', '', '', 's'),  # Catalan
    ('ig', '[aeiou]', '', '(tS|ig)'),  # tS is Catalan
    ('ix', '[aeiou]', '', 'S'),  # Catalan
    ('tx', '', '', 'tS'),  # Catalan
    ('tj', '', '$', 'tS'),  # Catalan
    ('tj', '', '', 'dZ'),  # Catalan
    ('tg', '', '', '(tg|dZ)'),  # dZ is Catalan
    ('ch', '', '', '(tS|dZ)'),  # dZ is typical for Argentina
    ('bh', '', '', 'b'),  # translit. from Arabic
    ('h', '[dgt]', '', ''),  # translit. from Arabic
    ('h', '', '$', ''),  # foreign
    # ("ll","","","(l|Z)"), # Z is typical for Argentina, only Ashkenazic
    ('m', '', '[bpvf]', '(m|n)'),
    ('c', '', '[ei]', 's'),
    # ("c","","[aou]","(k|C)"),
    ('gu', '', '[ei]', '(g|gv)'),  # "gv" because "u" can actually be "ü"
    ('g', '', '[ei]', '(x|g|dZ)'),  # "g" only for foreign words; dZ is Catalan
    ('qu', '', '', 'k'),
    ('uo', '', '', '(vo|o)'),
    ('u', '', '[aei]', 'v'),
    # SPECIAL VOWELS
    ('ü', '', '', 'v'),
    ('á', '', '', 'a'),
    ('é', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ó', '', '', 'o'),
    ('ú', '', '', 'u'),
    ('à', '', '', 'a'),  # Catalan
    ('è', '', '', 'e'),  # Catalan
    ('ò', '', '', 'o'),  # Catalan
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'B'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('j', '', '', '(x|Z)'),  # Z is Catalan
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'V'),
    ('w', '', '', 'v'),  # foreign words
    ('x', '', '', '(ks|gz|S)'),  # ks is Spanish, all are Catalan
    ('y', '', '', '(i|j)'),
    (
        'z',
        '',
        '',
        '(z|s)',
    ),  # as "c" befoire "e" or "i", in Spain it is like unvoiced English "th"  # noqa: E501
)

# gen/rulesturkish.php

_GEN_RULES_TURKISH = (
    ('ç', '', '', 'tS'),
    ('ğ', '', '', ''),  # to show that previous vowel is long
    ('ş', '', '', 'S'),
    ('ü', '', '', 'Q'),
    ('ö', '', '', 'Y'),
    ('ı', '', '', '(e|i|)'),  # as "e" in English "label"
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'dZ'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('j', '', '', 'Z'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),  # foreign words
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),  # foreign words
    ('x', '', '', 'ks'),  # foreign words
    ('y', '', '', 'j'),
    ('z', '', '', 'z'),
)

# sep/approxany.php

# SEPHARDIC
_SEP_APPROX_ANY = (('E', '', '', ''),)  # Final French "e"

# sep/approxcommon.php
# Sephardic

_SEP_APPROX_COMMON = (
    ('bens', '^', '', '(binz|s)'),
    ('benS', '^', '', '(binz|s)'),
    ('ben', '^', '', '(bin|)'),
    ('abens', '^', '', '(abinz|binz|s)'),
    ('abenS', '^', '', '(abinz|binz|s)'),
    ('aben', '^', '', '(abin|bin|)'),
    ('els', '^', '', '(ilz|alz|s)'),
    ('elS', '^', '', '(ilz|alz|s)'),
    ('el', '^', '', '(il|al|)'),
    ('als', '^', '', '(alz|s)'),
    ('alS', '^', '', '(alz|s)'),
    ('al', '^', '', '(al|)'),
    # ("dels", "^", "", "(dilz|s)"),
    # ("delS", "^", "", "(dilz|s)"),
    ('del', '^', '', '(dil|)'),
    ('dela', '^', '', '(dila|)'),
    # ("delo", "^", "", "(dila|)"),
    ('da', '^', '', '(da|)'),
    ('de', '^', '', '(di|)'),
    # ("des", "^", "", "(dis|dAs|)"),
    # ("di", "^", "", "(di|)"),
    # ("dos", "^", "", "(das|dus|)"),
    ('oa', '', '', '(va|a|D)'),
    ('oe', '', '', '(vi|D)'),
    ('ae', '', '', 'D'),
    # ("s", "", "$", "(s|)"), # Attia(s)
    # ("C", "", "", "s"),  # "c" could actually be "ç"
    ('n', '', '[bp]', 'm'),
    (
        'h',
        '',
        '',
        '(|h|f)',
    ),  # sound "h" (absent) can be expressed via /x/, Cojab in Spanish = Kohab ; Hakim = Fakim  # noqa: E501
    ('x', '', '', 'h'),
    # DIPHTHONGS ARE APPROXIMATELY equivalent
    ('aja', '^', '', '(Da|ia)'),
    ('aje', '^', '', '(Di|Da|i|ia)'),
    ('aji', '^', '', '(Di|i)'),
    ('ajo', '^', '', '(Du|Da|iu|ia)'),
    ('aju', '^', '', '(Du|iu)'),
    ('aj', '', '', 'D'),
    ('ej', '', '', 'D'),
    ('oj', '', '', 'D'),
    ('uj', '', '', 'D'),
    ('au', '', '', 'D'),
    ('eu', '', '', 'D'),
    ('ou', '', '', 'D'),
    ('a', '^', '', '(a|)'),  # Arabic
    ('ja', '^', '', 'ia'),
    ('je', '^', '', 'i'),
    ('jo', '^', '', '(iu|ia)'),
    ('ju', '^', '', 'iu'),
    ('ja', '', '', 'a'),
    ('je', '', '', 'i'),
    ('ji', '', '', 'i'),
    ('jo', '', '', 'u'),
    ('ju', '', '', 'u'),
    ('j', '', '', 'i'),
    # CONSONANTS {z & Z & dZ; s & S} are approximately interchangeable
    ('s', '', '[rmnl]', 'z'),
    ('S', '', '[rmnl]', 'z'),
    ('s', '[rmnl]', '', 'z'),
    ('S', '[rmnl]', '', 'z'),
    ('dS', '', '$', 'S'),
    ('dZ', '', '$', 'S'),
    ('Z', '', '$', 'S'),
    ('S', '', '$', '(S|s)'),
    ('z', '', '$', '(S|s)'),
    ('S', '', '', 's'),
    ('dZ', '', '', 'z'),
    ('Z', '', '', 'z'),
    ('i', '', '$', '(i|)'),  # often in Arabic
    ('e', '', '', 'i'),
    ('o', '', '$', '(a|u)'),
    ('o', '', '', 'u'),
    # special character to deal correctly in Hebrew match
    ('B', '', '', 'b'),
    ('V', '', '', 'v'),
    # Arabic
    ('p', '^', '', 'b'),
)

# sep/approxfrench.php
_SEP_APPROX_FRENCH = ()

# sep/approxhebrew.php
_SEP_APPROX_HEBREW = ()

# sep/approxitalian.php

# this file uses the same rules as approxfrench.php

# sep/approxportuguese.php
# this file uses the same rules as approxfrench.php

# sep/approxspanish.php
# this file uses the same rules as approxfrench.php

# sep/exactany.php
_SEP_EXACT_ANY = (('E', '', '', 'e'),)  # final French "e"

# sep/exactapproxcommon.php
# Sephardic
_SEP_EXACT_APPROX_COMMON = (
    ('h', '', '$', ''),
    # VOICED - UNVOICED CONSONANTS
    ('b', '', '[fktSs]', 'p'),
    ('b', '', 'p', ''),
    ('b', '', '$', 'p'),
    ('p', '', '[vgdZz]', 'b'),
    ('p', '', 'b', ''),
    ('v', '', '[pktSs]', 'f'),
    ('v', '', 'f', ''),
    ('v', '', '$', 'f'),
    ('f', '', '[vbgdZz]', 'v'),
    ('f', '', 'v', ''),
    ('g', '', '[pftSs]', 'k'),
    ('g', '', 'k', ''),
    ('g', '', '$', 'k'),
    ('k', '', '[vbdZz]', 'g'),
    ('k', '', 'g', ''),
    ('d', '', '[pfkSs]', 't'),
    ('d', '', 't', ''),
    ('d', '', '$', 't'),
    ('t', '', '[vbgZz]', 'd'),
    ('t', '', 'd', ''),
    ('s', '', 'dZ', ''),
    ('s', '', 'tS', ''),
    ('z', '', '[pfkSt]', 's'),
    ('z', '', '[sSzZ]', ''),
    ('s', '', '[sSzZ]', ''),
    ('Z', '', '[sSzZ]', ''),
    ('S', '', '[sSzZ]', ''),
    # SIMPLIFICATION OF CONSONANT CLUSTERS
    ('nm', '', '', 'm'),
    # DOUBLE --> SINGLE
    ('ji', '^', '', 'i'),
    ('a', '', 'a', ''),
    ('b', '', 'b', ''),
    ('d', '', 'd', ''),
    ('e', '', 'e', ''),
    ('f', '', 'f', ''),
    ('g', '', 'g', ''),
    ('i', '', 'i', ''),
    ('k', '', 'k', ''),
    ('l', '', 'l', ''),
    ('m', '', 'm', ''),
    ('n', '', 'n', ''),
    ('o', '', 'o', ''),
    ('p', '', 'p', ''),
    ('r', '', 'r', ''),
    ('t', '', 't', ''),
    ('u', '', 'u', ''),
    ('v', '', 'v', ''),
    ('z', '', 'z', '')
    # do not put name of file here since it always gets merged into another file  # noqa: E501
)

# sep/exactcommon.php
# Sephardic

_SEP_EXACT_COMMON = (
    ('h', '', '', ''),
    # ("C","","","k"),  # c that can actually be ç
    # VOICED - UNVOICED CONSONANTS
    ('s', '[^t]', '[bgZd]', 'z'),
    ('Z', '', '[pfkst]', 'S'),
    ('Z', '', '$', 'S'),
    ('S', '', '[bgzd]', 'Z'),
    ('z', '', '$', 's'),
    # special character to deal correctly in Hebrew match
    ('B', '', '', 'b'),
    ('V', '', '', 'v'),
)

# sep/exactfrench.php
# Sephardic
_SEP_EXACT_FRENCH = ()

# sep/exacthebrew.php
_SEP_EXACT_HEBREW = ()

# sep/exactitalian.php
# Sephardic
_SEP_EXACT_ITALIAN = ()

# sep/exactportuguese.php
# Sephardic
_SEP_EXACT_PORTUGUESE = ()

# sep/exactspanish.php
# Sephardic
_SEP_EXACT_SPANISH = ()

# sep/hebrewcommon.php
# Sephardic

_SEP_HEBREW_COMMON = (
    ('E', '', '', ''),  # final French "e": only in Sephardic
    ('ts', '', '', 'C'),  # for not confusion Gutes [=guts] and Guts [=guc]
    ('tS', '', '', 'C'),  # same reason
    ('S', '', '', 's'),
    ('p', '', '', 'f'),
    ('b', '^', '', 'b'),
    ('b', '', '', '(b|v)'),
    ('ja', '', '', 'i'),
    ('je', '', '', 'i'),
    ('aj', '', '', 'i'),
    ('j', '', '', 'i'),
    ('a', '^', '', '1'),
    ('e', '^', '', '1'),
    ('a', '', '$', '1'),
    ('e', '', '$', '1'),
    ('a', '', '', ''),
    ('e', '', '', ''),
    ('oj', '^', '', '(u|vi)'),
    ('uj', '^', '', '(u|vi)'),
    ('oj', '', '', 'u'),
    ('uj', '', '', 'u'),
    ('ou', '^', '', '(u|v|1)'),
    ('o', '^', '', '(u|v|1)'),
    ('u', '^', '', '(u|v|1)'),
    ('o', '', '$', '(u|1)'),
    ('u', '', '$', '(u|1)'),
    ('ou', '', '', 'u'),
    ('o', '', '', 'u'),
    ('VV', '', '', 'u'),  # alef/ayin + vov from ruleshebrew
    ('L', '^', '', '1'),  # alef/ayin from  ruleshebrew
    ('L', '', '$', '1'),  # alef/ayin from  ruleshebrew
    ('L', '', '', ''),  # alef/ayin from  ruleshebrew
    ('WW', '^', '', '(vi|u)'),  # vav-yod from  ruleshebrew
    ('WW', '', '', 'u'),  # vav-yod from  ruleshebrew
    ('W', '^', '', '(u|v)'),  # vav from  ruleshebrew
    ('W', '', '', 'u'),  # vav from  ruleshebrew
    # ("g","","","(g|Z)"),
    # ("z","","","(z|Z)"),
    # ("d","","","(d|dZ)"),
    ('T', '', '', 't'),  # tet from  ruleshebrew
    # ("k","","","(k|x)"),
    # ("x","","","(k|x)"),
    ('K', '', '', 'k'),  # kof and initial kaf from ruleshebrew
    ('X', '', '', 'x'),  # khet and final kaf from ruleshebrew
    # special for Spanish initial B/V
    ('B', '', '', 'v'),
    ('V', '', '', 'b'),
    ('H', '^', '', '(x|1)'),
    ('H', '', '$', '(x|1)'),
    ('H', '', '', '(x|)'),
    ('h', '^', '', '1'),
    ('h', '', '', ''),
)

# sep/lang.php
# SEPHARDIC

_SEP_LANGUAGE_RULES = (
    # 1. following are rules to accept the language
    # 1.1 Special letter combinations
    ('eau', 64, True),
    ('ou', 64, True),
    ('gni', 4160, True),
    ('tx', 262144, True),
    ('tj', 262144, True),
    ('gy', 64, True),
    ('guy', 64, True),
    ('sh', 294912, True),  # English, but no sign for /sh/ in these languages
    ('lh', 32768, True),
    ('nh', 32768, True),
    ('ny', 262144, True),
    ('gue', 262208, True),
    ('gui', 262208, True),
    ('gia', 4096, True),
    ('gie', 4096, True),
    ('gio', 4096, True),
    ('giu', 4096, True),
    # 1.2 special characters
    ('ñ', 262144, True),
    ('â', 32832, True),
    ('á', 294912, True),
    ('à', 32768, True),
    ('ã', 32768, True),
    ('ê', 32832, True),
    ('í', 294912, True),
    ('î', 64, True),
    ('ô', 32832, True),
    ('õ', 32768, True),
    ('ò', 266240, True),
    ('ú', 294912, True),
    ('ù', 64, True),
    ('ü', 294912, True),
    # Hebrew
    ('א', 1024, True),
    ('ב', 1024, True),
    ('ג', 1024, True),
    ('ד', 1024, True),
    ('ה', 1024, True),
    ('ו', 1024, True),
    ('ז', 1024, True),
    ('ח', 1024, True),
    ('ט', 1024, True),
    ('י', 1024, True),
    ('כ', 1024, True),
    ('ל', 1024, True),
    ('מ', 1024, True),
    ('נ', 1024, True),
    ('ס', 1024, True),
    ('ע', 1024, True),
    ('פ', 1024, True),
    ('צ', 1024, True),
    ('ק', 1024, True),
    ('ר', 1024, True),
    ('ש', 1024, True),
    ('ת', 1024, True),
    # 2. following are rules to reject the language
    # Every Latin character word has at least one Latin vowel
    ('a', 1024, False),
    ('o', 1024, False),
    ('e', 1024, False),
    ('i', 1024, False),
    ('y', 1024, False),
    ('u', 1024, False),
    ('kh', 262144, False),
    ('gua', 4096, False),
    ('guo', 4096, False),
    ('ç', 4096, False),
    ('cha', 4096, False),
    ('cho', 4096, False),
    ('chu', 4096, False),
    ('j', 4096, False),
    ('dj', 262144, False),
    ('sce', 64, False),
    ('sci', 64, False),
    ('ó', 64, False),
    ('è', 32768, False),
)

# sep/languagenames.php
_SEP_LANGUAGES = (
    'any',
    'french',
    'hebrew',
    'italian',
    'portuguese',
    'spanish',
)  # noqa: E501

# sep/rulesany.php
# SEPHARDIC: INCORPORATES Portuguese + Italian + Spanish(+Catalan) + French
_SEP_RULES_ANY = (
    # CONSONANTS
    ('ph', '', '', 'f'),  # foreign
    ('sh', '', '', 'S'),  # foreign
    ('kh', '', '', 'x'),  # foreign
    ('gli', '', '', '(gli|l[4096])'),
    ('gni', '', '', '(gni|ni[4160])'),
    ('gn', '', '[aeou]', '(n[4160]|nj[4160]|gn)'),
    ('gh', '', '', 'g'),  # It + translit. from Arabic
    ('dh', '', '', 'd'),  # translit. from Arabic
    ('bh', '', '', 'b'),  # translit. from Arabic
    ('th', '', '', 't'),  # translit. from Arabic
    ('lh', '', '', 'l'),  # Port
    ('nh', '', '', 'nj'),  # Port
    ('ig', '[aeiou]', '', '(ig|tS[262144])'),
    ('ix', '[aeiou]', '', 'S'),  # Sp
    ('tx', '', '', 'tS'),  # Sp
    ('tj', '', '$', 'tS'),  # Sp
    ('tj', '', '', 'dZ'),  # Sp
    ('tg', '', '', '(tg|dZ[262144])'),
    ('gi', '', '[aeou]', 'dZ'),  # italian
    ('g', '', 'y', 'Z'),  # french
    ('gg', '', '[ei]', '(gZ[32832]|dZ[266240]|x[262144])'),
    ('g', '', '[ei]', '(Z[32832]|dZ[266240]|x[262144])'),
    ('guy', '', '', 'gi'),
    ('gue', '', '$', '(k[64]|ge)'),
    ('gu', '', '[ei]', '(g|gv)'),  # not It
    ('gu', '', '[ao]', 'gv'),  # not It
    ('ñ', '', '', '(n|nj)'),
    ('ny', '', '', 'nj'),
    ('sc', '', '[ei]', '(s|S[4096])'),
    ('sç', '', '[aeiou]', 's'),  # not It
    ('ss', '', '', 's'),
    ('ç', '', '', 's'),  # not It
    ('ch', '', '[ei]', '(k[4096]|S[32832]|tS[262144]|dZ[262144])'),
    ('ch', '', '', '(S|tS[262144]|dZ[262144])'),
    ('ci', '', '[aeou]', '(tS[4096]|si)'),
    ('cc', '', '[eiyéèê]', '(tS[4096]|ks[294976])'),
    ('c', '', '[eiyéèê]', '(tS[4096]|s[294976])'),
    # ("c","","[aou]","(k|C[294912])"), # "C" means that the actual letter could be "ç" (cedille omitted)  # noqa: E501
    ('s', '^', '', 's'),
    ('s', '[aáuiíoóeéêy]', '[aáuiíoóeéêy]', '(s[262144]|z[36928])'),
    ('s', '', '[dglmnrv]', '(z|Z[32768])'),
    (
        'z',
        '',
        '$',
        '(s|ts[4096]|S[32768])',
    ),  # ts It, s/S/Z Port, s in Sp, z Fr  # noqa: E501
    ('z', '', '[bdgv]', '(z|dz[4096]|Z[32768])'),  # dz It, Z/z Port, z Sp & Fr
    ('z', '', '[ptckf]', '(s|ts[4096]|S[32768])'),  # ts It, s/S/z Port, z/s Sp
    (
        'z',
        '',
        '',
        '(z|dz[4096]|ts[4096]|s[262144])',
    ),  # ts/dz It, z Port & Fr, z/s Sp  # noqa: E501
    ('que', '', '$', '(k[64]|ke)'),
    ('qu', '', '[eiu]', 'k'),
    ('qu', '', '[ao]', '(kv|k)'),  # k is It
    ('ex', '', '[aáuiíoóeéêy]', '(ez[32768]|eS[32768]|eks|egz)'),
    ('ex', '', '[cs]', '(e[32768]|ek)'),
    ('m', '', '[cdglnrst]', '(m|n[32768])'),
    ('m', '', '[bfpv]', '(m|n[294912])'),
    ('m', '', '$', '(m|n[32768])'),
    ('b', '^', '', '(b|V[262144])'),
    ('v', '^', '', '(v|B[262144])'),
    # VOWELS
    ('eau', '', '', 'o'),  # Fr
    ('ouh', '', '[aioe]', '(v[64]|uh)'),
    ('uh', '', '[aioe]', '(v|uh)'),
    ('ou', '', '[aioe]', 'v'),  # french
    ('uo', '', '', '(vo|o)'),
    ('u', '', '[aie]', 'v'),
    ('i', '[aáuoóeéê]', '', 'j'),
    ('i', '', '[aeou]', 'j'),
    ('y', '[aáuiíoóeéê]', '', 'j'),
    ('y', '', '[aeiíou]', 'j'),
    ('e', '', '$', '(e|E[64])'),
    ('ão', '', '', '(au|an)'),  # Port
    ('ãe', '', '', '(aj|an)'),  # Port
    ('ãi', '', '', '(aj|an)'),  # Port
    ('õe', '', '', '(oj|on)'),  # Port
    ('où', '', '', 'u'),  # Fr
    ('ou', '', '', '(ou|u[64])'),
    ('â', '', '', 'a'),  # Port & Fr
    ('à', '', '', 'a'),  # Port
    ('á', '', '', 'a'),  # Port & Sp
    ('ã', '', '', '(a|an)'),  # Port
    ('é', '', '', 'e'),
    ('ê', '', '', 'e'),  # Port & Fr
    ('è', '', '', 'e'),  # Sp & Fr & It
    ('í', '', '', 'i'),  # Port & Sp
    ('î', '', '', 'i'),  # Fr
    ('ô', '', '', 'o'),  # Port & Fr
    ('ó', '', '', 'o'),  # Port & Sp & It
    ('õ', '', '', '(o|on)'),  # Port
    ('ò', '', '', 'o'),  # Sp & It
    ('ú', '', '', 'u'),  # Port & Sp
    ('ü', '', '', 'u'),  # Port & Sp
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', '(b|v[262144])'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('j', '', '', '(x[262144]|Z)'),  # not It
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', '(s|S[32768])'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', '(v|b[262144])'),
    ('w', '', '', 'v'),  # foreign
    ('x', '', '', '(ks|gz|S[294912])'),  # S/ks Port & Sp, gz Sp, It only ks
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# sep/rulesfrench.php

# Sephardic
_SEP_RULES_FRENCH = (
    # CONSONANTS
    ('kh', '', '', 'x'),  # foreign
    ('ph', '', '', 'f'),
    ('ç', '', '', 's'),
    ('x', '', '', 'ks'),
    ('ch', '', '', 'S'),
    ('c', '', '[eiyéèê]', 's'),
    ('c', '', '', 'k'),
    ('gn', '', '', '(n|gn)'),
    ('g', '', '[eiy]', 'Z'),
    ('gue', '', '$', 'k'),
    ('gu', '', '[eiy]', 'g'),
    # ("aill","","e","aj"), # non Jewish
    # ("ll","","e","(l|j)"), # non Jewish
    ('que', '', '$', 'k'),
    ('qu', '', '', 'k'),
    ('q', '', '', 'k'),
    ('s', '[aeiouyéèê]', '[aeiouyéèê]', 'z'),
    ('h', '[bdgt]', '', ''),  # translit from Arabic
    ('h', '', '$', ''),  # foreign
    ('j', '', '', 'Z'),
    ('w', '', '', 'v'),
    ('ouh', '', '[aioe]', '(v|uh)'),
    ('ou', '', '[aeio]', 'v'),
    ('uo', '', '', '(vo|o)'),
    ('u', '', '[aeio]', 'v'),
    # VOWELS
    ('aue', '', '', 'aue'),
    ('eau', '', '', 'o'),
    # ("au","","","(o|au)"), # non Jewish
    ('ai', '', '', 'aj'),  # [e] is non Jewish
    ('ay', '', '', 'aj'),  # [e] is non Jewish
    ('é', '', '', 'e'),
    ('ê', '', '', 'e'),
    ('è', '', '', 'e'),
    ('à', '', '', 'a'),
    ('â', '', '', 'a'),
    ('où', '', '', 'u'),
    ('ou', '', '', 'u'),
    ('oi', '', '', 'oj'),  # [ua] is non Jewish
    ('ei', '', '', 'ej'),  # [e] is non Jewish, in Ashk should be aj
    ('ey', '', '', 'ej'),  # [e] non Jewish, in Ashk should be aj
    # ("eu","","","(e|o)"), # non Jewish
    ('y', '[ou]', '', 'j'),
    ('e', '', '$', '(e|)'),
    ('i', '', '[aou]', 'j'),
    ('y', '', '[aoeu]', 'j'),
    ('y', '', '', 'i'),
    # TRIVIAL
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('z', '', '', 'z'),
)

# sep/ruleshebrew.php

# Sephardic
_SEP_RULES_HEBREW = (
    ('אי', '', '', 'i'),
    ('עי', '', '', 'i'),
    ('עו', '', '', 'VV'),
    ('או', '', '', 'VV'),
    ('ג׳', '', '', 'Z'),
    ('ד׳', '', '', 'dZ'),
    ('א', '', '', 'L'),
    ('ב', '', '', 'b'),
    ('ג', '', '', 'g'),
    ('ד', '', '', 'd'),
    ('ה', '^', '', '1'),
    ('ה', '', '$', '1'),
    ('ה', '', '', ''),
    ('וו', '', '', 'V'),
    ('וי', '', '', 'WW'),
    ('ו', '', '', 'W'),
    ('ז', '', '', 'z'),
    ('ח', '', '', 'X'),
    ('ט', '', '', 'T'),
    ('יי', '', '', 'i'),
    ('י', '', '', 'i'),
    ('ך', '', '', 'X'),
    ('כ', '^', '', 'K'),
    ('כ', '', '', 'k'),
    ('ל', '', '', 'l'),
    ('ם', '', '', 'm'),
    ('מ', '', '', 'm'),
    ('ן', '', '', 'n'),
    ('נ', '', '', 'n'),
    ('ס', '', '', 's'),
    ('ע', '', '', 'L'),
    ('ף', '', '', 'f'),
    ('פ', '', '', 'f'),
    ('ץ', '', '', 'C'),
    ('צ', '', '', 'C'),
    ('ק', '', '', 'K'),
    ('ר', '', '', 'r'),
    ('ש', '', '', 's'),
    ('ת', '', '', 'T'),  # Special for Sephardim
)

# sep/rulesitalian.php

_SEP_RULES_ITALIAN = (
    ('kh', '', '', 'x'),  # foreign
    ('gli', '', '', '(l|gli)'),
    ('gn', '', '[aeou]', '(n|nj|gn)'),
    ('gni', '', '', '(ni|gni)'),
    ('gi', '', '[aeou]', 'dZ'),
    ('gg', '', '[ei]', 'dZ'),
    ('g', '', '[ei]', 'dZ'),
    ('h', '[bdgt]', '', 'g'),  # gh is It; others from Arabic translit
    ('ci', '', '[aeou]', 'tS'),
    ('ch', '', '[ei]', 'k'),
    ('sc', '', '[ei]', 'S'),
    ('cc', '', '[ei]', 'tS'),
    ('c', '', '[ei]', 'tS'),
    ('s', '[aeiou]', '[aeiou]', 'z'),
    ('i', '[aeou]', '', 'j'),
    ('i', '', '[aeou]', 'j'),
    ('y', '[aeou]', '', 'j'),  # foreign
    ('y', '', '[aeou]', 'j'),  # foreign
    ('qu', '', '', 'k'),
    ('uo', '', '', '(vo|o)'),
    ('u', '', '[aei]', 'v'),
    ('è', '', '', 'e'),
    ('é', '', '', 'e'),
    ('ò', '', '', 'o'),
    ('ó', '', '', 'o'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('j', '', '', '(Z|dZ|j)'),  # foreign
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),  # foreign
    ('x', '', '', 'ks'),  # foreign
    ('y', '', '', 'i'),  # foreign
    ('z', '', '', '(ts|dz)'),
)

# sep/rulesportuguese.php

_SEP_RULES_PORTUGUESE = (
    ('kh', '', '', 'x'),  # foreign
    ('ch', '', '', 'S'),
    ('ss', '', '', 's'),
    ('sc', '', '[ei]', 's'),
    ('sç', '', '[aou]', 's'),
    ('ç', '', '', 's'),
    ('c', '', '[ei]', 's'),
    # ("c","","[aou]","(k|C)"),
    ('s', '^', '', 's'),
    ('s', '[aáuiíoóeéêy]', '[aáuiíoóeéêy]', 'z'),
    ('s', '', '[dglmnrv]', '(Z|S)'),  # Z is Brazil
    ('z', '', '$', '(Z|s|S)'),  # s and S in Brazil
    ('z', '', '[bdgv]', '(Z|z)'),  # Z in Brazil
    ('z', '', '[ptckf]', '(s|S|z)'),  # s and S in Brazil
    ('gu', '', '[eiu]', 'g'),
    ('gu', '', '[ao]', 'gv'),
    ('g', '', '[ei]', 'Z'),
    ('qu', '', '[eiu]', 'k'),
    ('qu', '', '[ao]', 'kv'),
    ('uo', '', '', '(vo|o|u)'),
    ('u', '', '[aei]', 'v'),
    ('lh', '', '', 'l'),
    ('nh', '', '', 'nj'),
    ('h', '[bdgt]', '', ''),  # translit. from Arabic
    ('ex', '', '[aáuiíoóeéêy]', '(ez|eS|eks)'),  # ez in Brazil
    ('ex', '', '[cs]', 'e'),
    ('y', '[aáuiíoóeéê]', '', 'j'),
    ('y', '', '[aeiíou]', 'j'),
    (
        'm',
        '',
        '[bcdfglnprstv]',
        '(m|n)',
    ),  # maybe to add a rule for m/n before a consonant that disappears [preceeding vowel becomes nasalized]  # noqa: E501
    (
        'm',
        '',
        '$',
        '(m|n)',
    ),  # maybe to add a rule for final m/n that disappears [preceeding vowel becomes nasalized]  # noqa: E501
    ('ão', '', '', '(au|an|on)'),
    ('ãe', '', '', '(aj|an)'),
    ('ãi', '', '', '(aj|an)'),
    ('õe', '', '', '(oj|on)'),
    ('i', '[aáuoóeéê]', '', 'j'),
    ('i', '', '[aeou]', 'j'),
    ('â', '', '', 'a'),
    ('à', '', '', 'a'),
    ('á', '', '', 'a'),
    ('ã', '', '', '(a|an|on)'),
    ('é', '', '', 'e'),
    ('ê', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ô', '', '', 'o'),
    ('ó', '', '', 'o'),
    ('õ', '', '', '(o|on)'),
    ('ú', '', '', 'u'),
    ('ü', '', '', 'u'),
    ('aue', '', '', 'aue'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', '(e|i)'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('j', '', '', 'Z'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', '(o|u)'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 'S'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', '(S|ks)'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# sep/rulesspanish.php

# Sephardic
_SEP_RULES_SPANISH = (
    # Includes both Spanish (Castillian) & Catalan
    # CONSONANTS
    ('ñ', '', '', '(n|nj)'),
    ('ny', '', '', 'nj'),  # Catalan
    ('ç', '', '', 's'),  # Catalan
    ('ig', '[aeiou]', '', '(tS|ig)'),  # tS is Catalan
    ('ix', '[aeiou]', '', 'S'),  # Catalan
    ('tx', '', '', 'tS'),  # Catalan
    ('tj', '', '$', 'tS'),  # Catalan
    ('tj', '', '', 'dZ'),  # Catalan
    ('tg', '', '', '(tg|dZ)'),  # dZ is Catalan
    ('ch', '', '', '(tS|dZ)'),  # dZ is typical for Argentina
    ('bh', '', '', 'b'),  # translit. from Arabic
    ('h', '[dgt]', '', ''),  # translit. from Arabic
    ('j', '', '', '(x|Z)'),  # Z is Catalan
    ('x', '', '', '(ks|gz|S)'),  # ks is Spanish, all are Catalan
    # ("ll","","","(l|Z)"), # Z is typical for Argentina, only Ashkenazic
    ('w', '', '', 'v'),  # foreign words
    ('v', '^', '', '(B|v)'),
    ('b', '^', '', '(b|V)'),
    ('v', '', '', '(b|v)'),
    ('b', '', '', '(b|v)'),
    ('m', '', '[bpvf]', '(m|n)'),
    ('c', '', '[ei]', 's'),
    # ("c","","[aou]","(k|C)"),
    ('c', '', '', 'k'),
    (
        'z',
        '',
        '',
        '(z|s)',
    ),  # as "c" befoire "e" or "i", in Spain it is like unvoiced English "th"  # noqa: E501
    ('gu', '', '[ei]', '(g|gv)'),  # "gv" because "u" can actually be "ü"
    ('g', '', '[ei]', '(x|g|dZ)'),  # "g" only for foreign words; dZ is Catalan
    ('qu', '', '', 'k'),
    ('q', '', '', 'k'),
    ('uo', '', '', '(vo|o)'),
    ('u', '', '[aei]', 'v'),
    # ("y","","","(i|j|S|Z)"), # S or Z are peculiar to South America; only Ashkenazic  # noqa: E501
    ('y', '', '', '(i|j)'),
    # VOWELS
    ('ü', '', '', 'v'),
    ('á', '', '', 'a'),
    ('é', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ó', '', '', 'o'),
    ('ú', '', '', 'u'),
    ('à', '', '', 'a'),  # Catalan
    ('è', '', '', 'e'),  # Catalan
    ('ò', '', '', 'o'),  # Catalan
    # TRIVIAL
    ('a', '', '', 'a'),
    ('d', '', '', 'd'),
    ('e', '', '', 'e'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'i'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
)

# ash/approxany.php

# ASHKENAZIC

# A, E, I, O, P, U should create variants, but a, e, i, o, u should not create any new variant  # noqa: E501
# Q = ü ; Y = ä = ö
# H = initial "H" in German/English
_ASH_APPROX_ANY = (
    # CONSONANTS
    ('b', '', '', '(b|v[262144])'),
    (
        'J',
        '',
        '',
        'z',
    ),  # Argentina Spanish: "ll" = /Z/, but approximately /Z/ = /z/  # noqa: E501
    # VOWELS
    # "ALL" DIPHTHONGS are interchangeable BETWEEN THEM and with monophthongs of which they are composed ("D" means "diphthong")  # noqa: E501
    # {a,o} are totally interchangeable if non-stressed; in German "a/o" can actually be from "ä/ö" (that are equivalent to "e")  # noqa: E501
    # {i,e} are interchangeable if non-stressed, while in German "u" can actually be from "ü" (that is equivalent to "i")  # noqa: E501
    ('aiB', '', '[bp]', '(D|Dm)'),
    ('AiB', '', '[bp]', '(D|Dm)'),
    ('oiB', '', '[bp]', '(D|Dm)'),
    ('OiB', '', '[bp]', '(D|Dm)'),
    ('uiB', '', '[bp]', '(D|Dm)'),
    ('UiB', '', '[bp]', '(D|Dm)'),
    ('eiB', '', '[bp]', '(D|Dm)'),
    ('EiB', '', '[bp]', '(D|Dm)'),
    ('iiB', '', '[bp]', '(D|Dm)'),
    ('IiB', '', '[bp]', '(D|Dm)'),
    ('aiB', '', '[dgkstvz]', '(D|Dn)'),
    ('AiB', '', '[dgkstvz]', '(D|Dn)'),
    ('oiB', '', '[dgkstvz]', '(D|Dn)'),
    ('OiB', '', '[dgkstvz]', '(D|Dn)'),
    ('uiB', '', '[dgkstvz]', '(D|Dn)'),
    ('UiB', '', '[dgkstvz]', '(D|Dn)'),
    ('eiB', '', '[dgkstvz]', '(D|Dn)'),
    ('EiB', '', '[dgkstvz]', '(D|Dn)'),
    ('iiB', '', '[dgkstvz]', '(D|Dn)'),
    ('IiB', '', '[dgkstvz]', '(D|Dn)'),
    ('B', '', '[bp]', '(o|om[16384]|im[16384])'),
    ('B', '', '[dgkstvz]', '(a|o|on[16384]|in[16384])'),
    ('B', '', '', '(a|o)'),
    ('aiF', '', '[bp]', '(D|Dm)'),
    ('AiF', '', '[bp]', '(D|Dm)'),
    ('oiF', '', '[bp]', '(D|Dm)'),
    ('OiF', '', '[bp]', '(D|Dm)'),
    ('uiF', '', '[bp]', '(D|Dm)'),
    ('UiF', '', '[bp]', '(D|Dm)'),
    ('eiF', '', '[bp]', '(D|Dm)'),
    ('EiF', '', '[bp]', '(D|Dm)'),
    ('iiF', '', '[bp]', '(D|Dm)'),
    ('IiF', '', '[bp]', '(D|Dm)'),
    ('aiF', '', '[dgkstvz]', '(D|Dn)'),
    ('AiF', '', '[dgkstvz]', '(D|Dn)'),
    ('oiF', '', '[dgkstvz]', '(D|Dn)'),
    ('OiF', '', '[dgkstvz]', '(D|Dn)'),
    ('uiF', '', '[dgkstvz]', '(D|Dn)'),
    ('UiF', '', '[dgkstvz]', '(D|Dn)'),
    ('eiF', '', '[dgkstvz]', '(D|Dn)'),
    ('EiF', '', '[dgkstvz]', '(D|Dn)'),
    ('iiF', '', '[dgkstvz]', '(D|Dn)'),
    ('IiF', '', '[dgkstvz]', '(D|Dn)'),
    ('F', '', '[bp]', '(i|im[16384]|om[16384])'),
    ('F', '', '[dgkstvz]', '(i|in[16384]|on[16384])'),
    ('F', '', '', 'i'),
    ('P', '', '', '(o|u)'),
    ('I', '[aeiouAEIBFOUQY]', '', 'i'),
    ('I', '', '[^aeiouAEBFIOU]e', '(Q[128]|i|D[32])'),  # "line"
    ('I', '', '$', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk[128])'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts[128])'),
    ('Its', '', '$', 'its'),
    ('I', '', '', '(Q[128]|i)'),
    ('lE', '[bdfgkmnprsStvzZ]', '$', '(li|il[32])'),  # Apple < Appel
    (
        'lE',
        '[bdfgkmnprsStvzZ]',
        '',
        '(li|il[32]|lY[128])',
    ),  # Applebaum < Appelbaum  # noqa: E501
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('Ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('Oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('Ui', '', '', '(D|u|i)'),
    ('ei', '', '', '(D|i)'),
    ('Ei', '', '', '(D|i)'),
    ('iA', '', '$', '(ia|io)'),
    ('iA', '', '', '(ia|io|iY[128])'),
    ('A', '', '[^aeiouAEBFIOU]e', '(a|o|Y[128]|D[32])'),  # "plane"
    (
        'E',
        'i[^aeiouAEIOU]',
        '',
        '(i|Y[128]|[32])',
    ),  # Wineberg (vineberg/vajneberg) --> vajnberg  # noqa: E501
    (
        'E',
        'a[^aeiouAEIOU]',
        '',
        '(i|Y[128]|[32])',
    ),  # Shaneberg (shaneberg/shejneberg) --> shejnberg  # noqa: E501
    ('e', '', '[fklmnprstv]$', 'i'),
    ('e', '', 'ts$', 'i'),
    ('e', '', '$', 'i'),
    ('e', '[DaoiuAOIUQY]', '', 'i'),
    ('e', '', '[aoAOQY]', 'i'),
    ('e', '', '', '(i|Y[128])'),
    ('E', '', '[fklmnprst]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '', '$', 'i'),
    ('E', '[DaoiuAOIUQY]', '', 'i'),
    ('E', '', '[aoAOQY]', 'i'),
    ('E', '', '', '(i|Y[128])'),
    ('a', '', '', '(a|o)'),
    ('O', '', '[fklmnprstv]$', 'o'),
    ('O', '', 'ts$', 'o'),
    ('O', '', '$', 'o'),
    ('O', '[oeiuQY]', '', 'o'),
    ('O', '', '', '(o|Y[128])'),
    ('A', '', '[fklmnprst]$', '(a|o)'),
    ('A', '', 'ts$', '(a|o)'),
    ('A', '', '$', '(a|o)'),
    ('A', '[oeiuQY]', '', '(a|o)'),
    ('A', '', '', '(a|o|Y[128])'),
    ('U', '', '$', 'u'),
    ('U', '[DoiuQY]', '', 'u'),
    ('U', '', '[^k]$', 'u'),
    ('Uk', '[lr]', '$', '(uk|Qk[128])'),
    ('Uk', '', '$', 'uk'),
    ('sUts', '', '$', '(suts|sQts[128])'),
    ('Uts', '', '$', 'uts'),
    ('U', '', '', '(u|Q[128])'),
)

# ash/approxcommon.php
# Ashkenazic

_ASH_APPROX_COMMON = (
    # REGRESSIVE ASSIMILATION OF CONSONANTS
    ('n', '', '[bp]', 'm'),
    # PECULIARITY OF "h"
    ('h', '', '', ''),
    ('H', '', '', '(x|)'),
    # POLISH OGONEK IMPOSSIBLE
    ('F', '', '[bdgkpstvzZ]h', 'e'),
    ('F', '', '[bdgkpstvzZ]x', 'e'),
    ('B', '', '[bdgkpstvzZ]h', 'a'),
    ('B', '', '[bdgkpstvzZ]x', 'a'),
    # "e" and "i" ARE TO BE OMITTED BEFORE (SYLLABIC) n & l: Halperin=Halpern; Frankel = Frankl, Finkelstein = Finklstein  # noqa: E501
    ('e', '[bdfgklmnprsStvzZ]', '[ln]$', ''),
    ('i', '[bdfgklmnprsStvzZ]', '[ln]$', ''),
    ('E', '[bdfgklmnprsStvzZ]', '[ln]$', ''),
    ('I', '[bdfgklmnprsStvzZ]', '[ln]$', ''),
    ('F', '[bdfgklmnprsStvzZ]', '[ln]$', ''),
    ('Q', '[bdfgklmnprsStvzZ]', '[ln]$', ''),
    ('Y', '[bdfgklmnprsStvzZ]', '[ln]$', ''),
    ('e', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(e|)'),
    ('i', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(i|)'),
    ('E', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(E|)'),
    ('I', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(I|)'),
    ('F', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(F|)'),
    ('Q', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(Q|)'),
    ('Y', '[bdfgklmnprsStvzZ]', '[ln][bdfgklmnprsStvzZ]', '(Y|)'),
    (
        'lEs',
        '',
        '',
        '(lEs|lz)',
    ),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)  # noqa: E501
    (
        'lE',
        '[bdfgkmnprStvzZ]',
        '',
        '(lE|l)',
    ),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)  # noqa: E501
    # SIMPLIFICATION: (TRIPHTHONGS & DIPHTHONGS) -> ONE GENERIC DIPHTHONG "D"
    ('aue', '', '', 'D'),
    ('oue', '', '', 'D'),
    ('AvE', '', '', '(D|AvE)'),
    ('Ave', '', '', '(D|Ave)'),
    ('avE', '', '', '(D|avE)'),
    ('ave', '', '', '(D|ave)'),
    ('OvE', '', '', '(D|OvE)'),
    ('Ove', '', '', '(D|Ove)'),
    ('ovE', '', '', '(D|ovE)'),
    ('ove', '', '', '(D|ove)'),
    ('ea', '', '', '(D|ea)'),
    ('EA', '', '', '(D|EA)'),
    ('Ea', '', '', '(D|Ea)'),
    ('eA', '', '', '(D|eA)'),
    ('aji', '', '', 'D'),
    ('ajI', '', '', 'D'),
    ('aje', '', '', 'D'),
    ('ajE', '', '', 'D'),
    ('Aji', '', '', 'D'),
    ('AjI', '', '', 'D'),
    ('Aje', '', '', 'D'),
    ('AjE', '', '', 'D'),
    ('oji', '', '', 'D'),
    ('ojI', '', '', 'D'),
    ('oje', '', '', 'D'),
    ('ojE', '', '', 'D'),
    ('Oji', '', '', 'D'),
    ('OjI', '', '', 'D'),
    ('Oje', '', '', 'D'),
    ('OjE', '', '', 'D'),
    ('eji', '', '', 'D'),
    ('ejI', '', '', 'D'),
    ('eje', '', '', 'D'),
    ('ejE', '', '', 'D'),
    ('Eji', '', '', 'D'),
    ('EjI', '', '', 'D'),
    ('Eje', '', '', 'D'),
    ('EjE', '', '', 'D'),
    ('uji', '', '', 'D'),
    ('ujI', '', '', 'D'),
    ('uje', '', '', 'D'),
    ('ujE', '', '', 'D'),
    ('Uji', '', '', 'D'),
    ('UjI', '', '', 'D'),
    ('Uje', '', '', 'D'),
    ('UjE', '', '', 'D'),
    ('iji', '', '', 'D'),
    ('ijI', '', '', 'D'),
    ('ije', '', '', 'D'),
    ('ijE', '', '', 'D'),
    ('Iji', '', '', 'D'),
    ('IjI', '', '', 'D'),
    ('Ije', '', '', 'D'),
    ('IjE', '', '', 'D'),
    ('aja', '', '', 'D'),
    ('ajA', '', '', 'D'),
    ('ajo', '', '', 'D'),
    ('ajO', '', '', 'D'),
    ('aju', '', '', 'D'),
    ('ajU', '', '', 'D'),
    ('Aja', '', '', 'D'),
    ('AjA', '', '', 'D'),
    ('Ajo', '', '', 'D'),
    ('AjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('oja', '', '', 'D'),
    ('ojA', '', '', 'D'),
    ('ojo', '', '', 'D'),
    ('ojO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('Oja', '', '', 'D'),
    ('OjA', '', '', 'D'),
    ('Ojo', '', '', 'D'),
    ('OjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('eja', '', '', 'D'),
    ('ejA', '', '', 'D'),
    ('ejo', '', '', 'D'),
    ('ejO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('Eja', '', '', 'D'),
    ('EjA', '', '', 'D'),
    ('Ejo', '', '', 'D'),
    ('EjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('uja', '', '', 'D'),
    ('ujA', '', '', 'D'),
    ('ujo', '', '', 'D'),
    ('ujO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('Uja', '', '', 'D'),
    ('UjA', '', '', 'D'),
    ('Ujo', '', '', 'D'),
    ('UjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('ija', '', '', 'D'),
    ('ijA', '', '', 'D'),
    ('ijo', '', '', 'D'),
    ('ijO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('Ija', '', '', 'D'),
    ('IjA', '', '', 'D'),
    ('Ijo', '', '', 'D'),
    ('IjO', '', '', 'D'),
    ('Aju', '', '', 'D'),
    ('AjU', '', '', 'D'),
    ('j', '', '', 'i'),
    # lander = lender = lÃ¤nder
    ('lYndEr', '', '$', 'lYnder'),
    ('lander', '', '$', 'lYnder'),
    ('lAndEr', '', '$', 'lYnder'),
    ('lAnder', '', '$', 'lYnder'),
    ('landEr', '', '$', 'lYnder'),
    ('lender', '', '$', 'lYnder'),
    ('lEndEr', '', '$', 'lYnder'),
    ('lendEr', '', '$', 'lYnder'),
    ('lEnder', '', '$', 'lYnder'),
    # burg = berg
    ('bUrk', '', '$', '(burk|berk)'),
    ('burk', '', '$', '(burk|berk)'),
    ('bUrg', '', '$', '(burk|berk)'),
    ('burg', '', '$', '(burk|berk)'),
    # CONSONANTS {z & Z; s & S} are approximately interchangeable
    ('s', '', '[rmnl]', 'z'),
    ('S', '', '[rmnl]', 'z'),
    ('s', '[rmnl]', '', 'z'),
    ('S', '[rmnl]', '', 'z'),
    ('dS', '', '$', 'S'),
    ('dZ', '', '$', 'S'),
    ('Z', '', '$', 'S'),
    ('S', '', '$', '(S|s)'),
    ('z', '', '$', '(S|s)'),
    ('S', '', '', 's'),
    ('dZ', '', '', 'z'),
    ('Z', '', '', 'z'),
)

# ash/approxcyrillic.php
# this file uses the same rules as approxrussian.php

# ash/approxenglish.php

_ASH_APPROX_ENGLISH = (
    # VOWELS
    ('I', '', '[^aEIeiou]e', '(Q|i|D)'),  # like in "five"
    ('I', '', '$', 'i'),
    ('I', '[aEIeiou]', '', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '', '', '(i|Q)'),
    ('lE', '[bdfgkmnprsStvzZ]', '', '(il|li|lY)'),  # Applebaum < Appelbaum
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    (
        'E',
        'D[^aeiEIou]',
        '',
        '(i|)',
    ),  # Weinberg, Shaneberg (shaneberg/shejneberg) --> shejnberg  # noqa: E501
    ('e', 'D[^aeiEIou]', '', '(i|)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprsStv]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '[DaoiEuQY]', '', 'i'),
    ('E', '', '[aoQY]', 'i'),
    ('E', '', '', '(Y|i)'),
    ('a', '', '', '(a|o)'),
)

# ash/approxfrench.php
# THE LINES BELOW WERE VALID FOR ASHKENAZIM

_ASH_APPROX_FRENCH = (
    ('I', '', '$', 'i'),
    ('I', '[aEIeiou]', '', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '', '', '(i|Q)'),
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('a', '', '', '(a|o)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprsStv]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '[aoiuQ]', '', 'i'),
    ('E', '', '[aoQ]', 'i'),
    ('E', '', '', '(Y|i)'),
)

# ash/approxgerman.php

_ASH_APPROX_GERMAN = (
    ('I', '', '$', 'i'),
    ('I', '[aeiAEIOUouQY]', '', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '', '', '(Q|i)'),
    ('AU', '', '', '(D|a|u)'),
    ('aU', '', '', '(D|a|u)'),
    ('Au', '', '', '(D|a|u)'),
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('OU', '', '', '(D|o|u)'),
    ('oU', '', '', '(D|o|u)'),
    ('Ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('Ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('Oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('Ui', '', '', '(D|u|i)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprst]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '', '$', 'i'),
    ('E', '[DaoAOUiuQY]', '', 'i'),
    ('E', '', '[aoAOQY]', 'i'),
    ('E', '', '', '(Y|i)'),
    ('O', '', '$', 'o'),
    ('O', '', '[fklmnprst]$', 'o'),
    ('O', '', 'ts$', 'o'),
    ('O', '[aoAOUeiuQY]', '', 'o'),
    ('O', '', '', '(o|Y)'),
    ('a', '', '', '(a|o)'),
    ('A', '', '$', '(a|o)'),
    ('A', '', '[fklmnprst]$', '(a|o)'),
    ('A', '', 'ts$', '(a|o)'),
    ('A', '[aoeOUiuQY]', '', '(a|o)'),
    ('A', '', '', '(a|o|Y)'),
    ('U', '', '$', 'u'),
    ('U', '[DaoiuUQY]', '', 'u'),
    ('U', '', '[^k]$', 'u'),
    ('Uk', '[lr]', '$', '(uk|Qk)'),
    ('Uk', '', '$', 'uk'),
    ('sUts', '', '$', '(suts|sQts)'),
    ('Uts', '', '$', 'uts'),
    ('U', '', '', '(u|Q)'),
)

# ash/approxhebrew.php

_ASH_APPROX_HEBREW = ()

# ash/approxhungarian.php

# this file uses the same rules as approxfrench.php

# ash/approxpolish.php
_ASH_APPROX_POLISH = (
    ('aiB', '', '[bp]', '(D|Dm)'),
    ('oiB', '', '[bp]', '(D|Dm)'),
    ('uiB', '', '[bp]', '(D|Dm)'),
    ('eiB', '', '[bp]', '(D|Dm)'),
    ('EiB', '', '[bp]', '(D|Dm)'),
    ('iiB', '', '[bp]', '(D|Dm)'),
    ('IiB', '', '[bp]', '(D|Dm)'),
    ('aiB', '', '[dgkstvz]', '(D|Dn)'),
    ('oiB', '', '[dgkstvz]', '(D|Dn)'),
    ('uiB', '', '[dgkstvz]', '(D|Dn)'),
    ('eiB', '', '[dgkstvz]', '(D|Dn)'),
    ('EiB', '', '[dgkstvz]', '(D|Dn)'),
    ('iiB', '', '[dgkstvz]', '(D|Dn)'),
    ('IiB', '', '[dgkstvz]', '(D|Dn)'),
    ('B', '', '[bp]', '(o|om|im)'),
    ('B', '', '[dgkstvz]', '(o|on|in)'),
    ('B', '', '', 'o'),
    ('aiF', '', '[bp]', '(D|Dm)'),
    ('oiF', '', '[bp]', '(D|Dm)'),
    ('uiF', '', '[bp]', '(D|Dm)'),
    ('eiF', '', '[bp]', '(D|Dm)'),
    ('EiF', '', '[bp]', '(D|Dm)'),
    ('iiF', '', '[bp]', '(D|Dm)'),
    ('IiF', '', '[bp]', '(D|Dm)'),
    ('aiF', '', '[dgkstvz]', '(D|Dn)'),
    ('oiF', '', '[dgkstvz]', '(D|Dn)'),
    ('uiF', '', '[dgkstvz]', '(D|Dn)'),
    ('eiF', '', '[dgkstvz]', '(D|Dn)'),
    ('EiF', '', '[dgkstvz]', '(D|Dn)'),
    ('iiF', '', '[dgkstvz]', '(D|Dn)'),
    ('IiF', '', '[dgkstvz]', '(D|Dn)'),
    ('F', '', '[bp]', '(i|im|om)'),
    ('F', '', '[dgkstvz]', '(i|in|on)'),
    ('F', '', '', 'i'),
    ('P', '', '', '(o|u)'),
    ('I', '', '$', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '[aeiAEBFIou]', '', 'i'),
    ('I', '', '', '(i|Q)'),
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('a', '', '', '(a|o)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprst]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '', '$', 'i'),
    ('E', '[DaoiuQ]', '', 'i'),
    ('E', '', '[aoQ]', 'i'),
    ('E', '', '', '(Y|i)'),
)

# ash/approxromanian.php

# this file uses the same rules as approxpolish.php

# ash/approxrussian.php

_ASH_APPROX_RUSSIAN = (
    # VOWELS
    ('I', '', '$', 'i'),
    ('I', '', '[^k]$', 'i'),
    ('Ik', '[lr]', '$', '(ik|Qk)'),
    ('Ik', '', '$', 'ik'),
    ('sIts', '', '$', '(sits|sQts)'),
    ('Its', '', '$', 'its'),
    ('I', '[aeiEIou]', '', 'i'),
    ('I', '', '', '(i|Q)'),
    ('au', '', '', '(D|a|u)'),
    ('ou', '', '', '(D|o|u)'),
    ('ai', '', '', '(D|a|i)'),
    ('oi', '', '', '(D|o|i)'),
    ('ui', '', '', '(D|u|i)'),
    ('om', '', '[bp]', '(om|im)'),
    ('on', '', '[dgkstvz]', '(on|in)'),
    ('em', '', '[bp]', '(im|om)'),
    ('en', '', '[dgkstvz]', '(in|on)'),
    ('Em', '', '[bp]', '(im|Ym|om)'),
    ('En', '', '[dgkstvz]', '(in|Yn|on)'),
    ('a', '', '', '(a|o)'),
    ('e', '', '', 'i'),
    ('E', '', '[fklmnprsStv]$', 'i'),
    ('E', '', 'ts$', 'i'),
    ('E', '[DaoiuQ]', '', 'i'),
    ('E', '', '[aoQ]', 'i'),
    ('E', '', '', '(Y|i)'),
)

# ash/approxspanish.php

# this file uses the same rules as approxfrench.php

# ash/exactany.php
# These rules are applied after the word has been transliterated into the phonetic alphabet  # noqa: E501
# These rules are substitution rules within the phonetic character space rather than mapping rules  # noqa: E501

# format of each entry rule in the table
# (pattern, left context, right context, phonetic)
# where
# pattern is a sequence of characters that might appear after a word has been transliterated into phonetic alphabet  # noqa: E501
# left context is the context that precedes the pattern
# right context is the context that follows the pattern
# phonetic is the result that this rule generates
#
# note that both left context and right context can be regular expressions
# ex: left context of ^ would mean start of word
# right context of $ means end of word
#
# match occurs if all of the following are true:
# portion of word matches the pattern
# that portion satisfies the context

# A, E, I, O, P, U should create variants, but a, e, i, o, u should not create any new variant  # noqa: E501
# Q = ü ; Y = ä = ö

_ASH_EXACT_ANY = (
    ('A', '', '', 'a'),
    ('B', '', '', 'a'),
    ('E', '', '', 'e'),
    ('F', '', '', 'e'),
    ('I', '', '', 'i'),
    ('O', '', '', 'o'),
    ('P', '', '', 'o'),
    ('U', '', '', 'u'),
    ('J', '', '', 'l'),
)

# ash/exactapproxcommon.php
# Ashkenazic
_ASH_EXACT_APPROX_COMMON = (
    ('h', '', '$', ''),
    # VOICED - UNVOICED CONSONANTS
    ('b', '', '[fktSs]', 'p'),
    ('b', '', 'p', ''),
    ('b', '', '$', 'p'),
    ('p', '', '[gdZz]', 'b'),
    ('p', '', 'b', ''),
    ('v', '', '[pktSs]', 'f'),
    ('v', '', 'f', ''),
    ('v', '', '$', 'f'),
    ('f', '', '[bgdZz]', 'v'),
    ('f', '', 'v', ''),
    ('g', '', '[pftSs]', 'k'),
    ('g', '', 'k', ''),
    ('g', '', '$', 'k'),
    ('k', '', '[bdZz]', 'g'),
    ('k', '', 'g', ''),
    ('d', '', '[pfkSs]', 't'),
    ('d', '', 't', ''),
    ('d', '', '$', 't'),
    ('t', '', '[bgZz]', 'd'),
    ('t', '', 'd', ''),
    ('s', '', 'dZ', ''),
    ('s', '', 'tS', ''),
    ('z', '', '[pfkSt]', 's'),
    ('z', '', '[sSzZ]', ''),
    ('s', '', '[sSzZ]', ''),
    ('Z', '', '[sSzZ]', ''),
    ('S', '', '[sSzZ]', ''),
    # SIMPLIFICATION OF CONSONANT CLUSTERS
    ('jnm', '', '', 'jm'),
    # DOUBLE --> SINGLE
    ('ji', '^', '', 'i'),
    ('jI', '^', '', 'I'),
    ('a', '', '[aAB]', ''),
    ('a', '[AB]', '', ''),
    ('A', '', 'A', ''),
    ('B', '', 'B', ''),
    ('b', '', 'b', ''),
    ('d', '', 'd', ''),
    ('f', '', 'f', ''),
    ('g', '', 'g', ''),
    ('k', '', 'k', ''),
    ('l', '', 'l', ''),
    ('m', '', 'm', ''),
    ('n', '', 'n', ''),
    ('p', '', 'p', ''),
    ('r', '', 'r', ''),
    ('t', '', 't', ''),
    ('v', '', 'v', ''),
    ('z', '', 'z', '')
    # do not put name of file here since it always gets merged into another file  # noqa: E501
)

# ash/exactcommon.php
# Ashkenazic

_ASH_EXACT_COMMON = (
    ('H', '', '', 'h'),
    # VOICED - UNVOICED CONSONANTS
    ('s', '[^t]', '[bgZd]', 'z'),
    ('Z', '', '[pfkst]', 'S'),
    ('Z', '', '$', 'S'),
    ('S', '', '[bgzd]', 'Z'),
    ('z', '', '$', 's'),
    ('ji', '[aAoOeEiIuU]', '', 'j'),
    ('jI', '[aAoOeEiIuU]', '', 'j'),
    ('je', '[aAoOeEiIuU]', '', 'j'),
    ('jE', '[aAoOeEiIuU]', '', 'j'),
)

# ash/exactcyrillic.php
# this file uses the same rules as exactrussian.php

# ash/exactenglish.php
# this file uses the same rules as exactrussian.php

# ash/exactfrench.php
# For Ashkenazic searches:
# this file uses the same rules as exactrussian.php

# ash/exactgerman.php
# this file uses the same rules as exactany.php

# ash/exacthebrew.php
_ASH_EXACT_HEBREW = ()

# ash/exacthungarian.php
# this file uses the same rules as exactrussian.php

# ash/exactpolish.php
_ASH_EXACT_POLISH = (
    ('B', '', '', 'a'),
    ('F', '', '', 'e'),
    ('P', '', '', 'o'),
    ('E', '', '', 'e'),
    ('I', '', '', 'i'),
)

# ash/exactromanian.php
# this file uses the same rules as exactrussian.php

# ash/exactrussian.php
_ASH_EXACT_RUSSIAN = (('E', '', '', 'e'), ('I', '', '', 'i'))

# ash/exactspanish.php
# this Ashkenazic file uses the same rules as exactrussian.php

# ash/hebrewcommon.php
# Ashkenazic

_ASH_HEBREW_COMMON = (
    ('ts', '', '', 'C'),  # for not confusion Gutes [=guts] and Guts [=guc]
    ('tS', '', '', 'C'),  # same reason
    ('S', '', '', 's'),
    ('p', '', '', 'f'),
    ('b', '^', '', 'b'),
    ('b', '', '', '(b|v)'),
    ('J', '', '', 'l'),
    ('ja', '', '', 'i'),
    ('jA', '', '', 'i'),
    ('jB', '', '', 'i'),
    ('je', '', '', 'i'),
    ('jE', '', '', 'i'),
    ('jF', '', '', 'i'),
    ('aj', '', '', 'i'),
    ('Aj', '', '', 'i'),
    ('Bj', '', '', 'i'),
    ('Fj', '', '', 'i'),
    ('I', '', '', 'i'),
    ('Q', '', '', 'i'),
    ('j', '', '', 'i'),
    ('a', '^', '', '1'),
    ('A', '^', '', '1'),
    ('B', '^', '', '1'),
    ('e', '^', '', '1'),
    ('E', '^', '', '1'),
    ('F', '^', '', '1'),
    ('Y', '^', '', '1'),
    ('a', '', '$', '1'),
    ('A', '', '$', '1'),
    ('B', '', '$', '1'),
    ('e', '', '$', '1'),
    ('E', '', '$', '1'),
    ('F', '', '$', '1'),
    ('Y', '', '$', '1'),
    ('a', '', '', ''),
    ('A', '', '', ''),
    ('B', '', '', ''),
    ('e', '', '', ''),
    ('E', '', '', ''),
    ('F', '', '', ''),
    ('Y', '', '', ''),
    ('oj', '^', '', '(u|vi)'),
    ('Oj', '^', '', '(u|vi)'),
    ('uj', '^', '', '(u|vi)'),
    ('Uj', '^', '', '(u|vi)'),
    ('oj', '', '', 'u'),
    ('Oj', '', '', 'u'),
    ('uj', '', '', 'u'),
    ('Uj', '', '', 'u'),
    ('ou', '^', '', '(u|v|1)'),
    ('o', '^', '', '(u|v|1)'),
    ('O', '^', '', '(u|v|1)'),
    ('P', '^', '', '(u|v|1)'),
    ('U', '^', '', '(u|v|1)'),
    ('u', '^', '', '(u|v|1)'),
    ('o', '', '$', '(u|1)'),
    ('O', '', '$', '(u|1)'),
    ('P', '', '$', '(u|1)'),
    ('u', '', '$', '(u|1)'),
    ('U', '', '$', '(u|1)'),
    ('ou', '', '', 'u'),
    ('o', '', '', 'u'),
    ('O', '', '', 'u'),
    ('P', '', '', 'u'),
    ('U', '', '', 'u'),
    ('VV', '', '', 'u'),  # alef/ayin + vov from ruleshebrew
    ('V', '', '', 'v'),  # tsvey-vov from ruleshebrew;; only Ashkenazic
    ('L', '^', '', '1'),  # alef/ayin from ruleshebrew
    ('L', '', '$', '1'),  # alef/ayin from ruleshebrew
    ('L', '', '', ''),  # alef/ayin from ruleshebrew
    ('WW', '^', '', '(vi|u)'),  # vav-yod from ruleshebrew
    ('WW', '', '', 'u'),  # vav-yod from ruleshebrew
    ('W', '^', '', '(u|v)'),  # vav from ruleshebrew
    ('W', '', '', 'u'),  # vav from ruleshebrew
    # ("g","","","(g|Z)"),
    # ("z","","","(z|Z)"),
    # ("d","","","(d|dZ)"),
    ('TB', '^', '', 't'),  # tav from ruleshebrew; only Ashkenazic
    ('TB', '', '$', 's'),  # tav from ruleshebrew; only Ashkenazic
    ('TB', '', '', '(t|s)'),  # tav from ruleshebrew; only Ashkenazic
    ('T', '', '', 't'),  # tet from ruleshebrew
    # ("k","","","(k|x)"),
    # ("x","","","(k|x)"),
    ('K', '', '', 'k'),  # kof and initial kaf from ruleshebrew
    ('X', '', '', 'x'),  # khet and final kaf from ruleshebrew
    ('H', '^', '', '(x|1)'),
    ('H', '', '$', '(x|1)'),
    ('H', '', '', '(x|)'),
    ('h', '^', '', '1'),
    ('h', '', '', ''),
)

# ash/lang.php
# ASHKENAZIC

# format of entries in $languageRules table is
# (pattern, language, Acceptance)
# where
# pattern is a regular expression
# e.g., ^ means start of word, $ Means End Of Word, [^ei] means anything but e or i, etc.  # noqa: E501
# language is one or more of the languages defined above separated by + signs
# acceptance is true or false
# meaning is:
# if "pattern" matches and acceptance is true, name is in one of the languages indicated and no others  # noqa: E501
# if "pattern" matches and acceptance is false, name is not in any of the languages indicated  # noqa: E501

_ASH_LANGUAGE_RULES = (
    # 1. following are rules to accept the language
    # 1.1 Special letter combinations
    ('zh', 147616, True),
    ('eau', 64, True),
    ('[aoeiuäöü]h', 128, True),
    ('^vogel', 128, True),
    ('vogel$', 128, True),
    ('witz', 128, True),
    ('tz$', 131232, True),
    ('^tz', 131104, True),
    ('güe', 262144, True),
    ('güi', 262144, True),
    ('ghe', 65536, True),
    ('ghi', 65536, True),
    ('vici$', 65536, True),
    ('schi$', 65536, True),
    ('chsch', 128, True),
    ('tsch', 128, True),
    ('ssch', 128, True),
    ('sch$', 131200, True),
    ('^sch', 131200, True),
    ('^rz', 16384, True),
    ('rz$', 16512, True),
    ('[^aoeiuäöü]rz', 16384, True),
    ('rz[^aoeiuäöü]', 16384, True),
    ('cki$', 16384, True),
    ('ska$', 16384, True),
    ('cka$', 16384, True),
    ('ue', 131200, True),
    ('ae', 131232, True),
    ('oe', 131296, True),
    ('th$', 128, True),
    ('^th', 128, True),
    ('th[^aoeiu]', 128, True),
    ('mann', 128, True),
    ('cz', 16384, True),
    ('cy', 16384, True),
    ('niew', 16384, True),
    ('stein', 128, True),
    ('heim$', 128, True),
    ('heimer$', 128, True),
    ('ii$', 131072, True),
    ('iy$', 131072, True),
    ('yy$', 131072, True),
    ('yi$', 131072, True),
    ('yj$', 131072, True),
    ('ij$', 131072, True),
    ('gaus$', 131072, True),
    ('gauz$', 131072, True),
    ('gauz$', 131072, True),
    ('goltz$', 131072, True),
    ('gol\'tz$', 131072, True),
    ('golts$', 131072, True),
    ('gol\'ts$', 131072, True),
    ('^goltz', 131072, True),
    ('^gol\'tz', 131072, True),
    ('^golts', 131072, True),
    ('^gol\'ts', 131072, True),
    ('gendler$', 131072, True),
    ('gejmer$', 131072, True),
    ('gejm$', 131072, True),
    ('geimer$', 131072, True),
    ('geim$', 131072, True),
    ('geymer', 131072, True),
    ('geym$', 131072, True),
    ('gof$', 131072, True),
    ('thal', 128, True),
    ('zweig', 128, True),
    ('ck$', 160, True),
    ('c$', 83968, True),
    ('sz', 18432, True),
    ('gue', 262208, True),
    ('gui', 262208, True),
    ('guy', 64, True),
    ('cs$', 2048, True),
    ('^cs', 2048, True),
    ('dzs', 2048, True),
    ('zs$', 2048, True),
    ('^zs', 2048, True),
    ('^wl', 16384, True),
    ('^wr', 16544, True),
    ('gy$', 2048, True),
    ('gy[aeou]', 2048, True),
    ('gy', 133120, True),
    ('ly', 149504, True),
    ('ny', 149504, True),
    ('ty', 149504, True),
    # 1.2 special characters
    ('â', 65600, True),
    ('ă', 65536, True),
    ('à', 64, True),
    ('ä', 128, True),
    ('á', 264192, True),
    ('ą', 16384, True),
    ('ć', 16384, True),
    ('ç', 64, True),
    ('ę', 16384, True),
    ('é', 264256, True),
    ('è', 64, True),
    ('ê', 64, True),
    ('í', 264192, True),
    ('î', 65600, True),
    ('ł', 16384, True),
    ('ń', 16384, True),
    ('ñ', 262144, True),
    ('ó', 280576, True),
    ('ö', 2176, True),
    ('õ', 2048, True),
    ('ş', 65536, True),
    ('ś', 16384, True),
    ('ţ', 65536, True),
    ('ü', 2176, True),
    ('ù', 64, True),
    ('ű', 2048, True),
    ('ú', 264192, True),
    ('ź', 16384, True),
    ('ż', 16384, True),
    ('ß', 128, True),
    # Every Cyrillic word has at least one Cyrillic vowel (аёеоиуыэюя)
    ('а', 4, True),
    ('ё', 4, True),
    ('о', 4, True),
    ('е', 4, True),
    ('и', 4, True),
    ('у', 4, True),
    ('ы', 4, True),
    ('э', 4, True),
    ('ю', 4, True),
    ('я', 4, True),
    # Hebrew
    ('א', 1024, True),
    ('ב', 1024, True),
    ('ג', 1024, True),
    ('ד', 1024, True),
    ('ה', 1024, True),
    ('ו', 1024, True),
    ('ז', 1024, True),
    ('ח', 1024, True),
    ('ט', 1024, True),
    ('י', 1024, True),
    ('כ', 1024, True),
    ('ל', 1024, True),
    ('מ', 1024, True),
    ('נ', 1024, True),
    ('ס', 1024, True),
    ('ע', 1024, True),
    ('פ', 1024, True),
    ('צ', 1024, True),
    ('ק', 1024, True),
    ('ר', 1024, True),
    ('ש', 1024, True),
    ('ת', 1024, True),
    # 2. following are rules to reject the language
    # Every Latin character word has at least one Latin vowel
    ('a', 1028, False),
    ('o', 1028, False),
    ('e', 1028, False),
    ('i', 1028, False),
    ('y', 66564, False),
    ('u', 1028, False),
    (
        'v[^aoeiuäüö]',
        128,
        False,
    ),  # in german, "v" can be found before a vowel only  # noqa: E501
    (
        'y[^aoeiu]',
        128,
        False,
    ),  # in german, "y" usually appears only in the last position; sometimes before a vowel  # noqa: E501
    ('c[^aohk]', 128, False),
    ('dzi', 224, False),
    ('ou', 128, False),
    ('aj', 224, False),
    ('ej', 224, False),
    ('oj', 224, False),
    ('uj', 224, False),
    ('k', 65536, False),
    ('v', 16384, False),
    ('ky', 16384, False),
    ('eu', 147456, False),
    ('w', 460864, False),
    ('kie', 262208, False),
    ('gie', 327744, False),
    ('q', 215040, False),
    ('sch', 280640, False),
    ('^h', 131072, False),
)

# ash/languagenames.php
_ASH_LANGUAGES = (
    'any',
    'cyrillic',
    'english',
    'french',
    'german',
    'hebrew',
    'hungarian',
    'polish',
    'romanian',
    'russian',
    'spanish',
)

# ash/rulesany.php
# ASHKENAZIC
_ASH_RULES_ANY = (
    # CONVERTING FEMININE TO MASCULINE
    ('yna', '', '$', '(in[131072]|ina)'),
    ('ina', '', '$', '(in[131072]|ina)'),
    ('liova', '', '$', '(lof[131072]|lef[131072]|lova)'),
    ('lova', '', '$', '(lof[131072]|lef[131072]|lova)'),
    ('ova', '', '$', '(of[131072]|ova)'),
    ('eva', '', '$', '(ef[131072]|eva)'),
    ('aia', '', '$', '(aja|i[131072])'),
    ('aja', '', '$', '(aja|i[131072])'),
    ('aya', '', '$', '(aja|i[131072])'),
    ('lowa', '', '$', '(lova|lof[16384]|l[16384]|el[16384])'),
    ('kowa', '', '$', '(kova|kof[16384]|k[16384]|ek[16384])'),
    ('owa', '', '$', '(ova|of[16384]|)'),
    ('lowna', '', '$', '(lovna|levna|l[16384]|el[16384])'),
    ('kowna', '', '$', '(kovna|k[16384]|ek[16384])'),
    ('owna', '', '$', '(ovna|[16384])'),
    ('lówna', '', '$', '(l|el[16384])'),  # polish
    ('kówna', '', '$', '(k|ek[16384])'),  # polish
    ('ówna', '', '$', ''),  # polish
    ('a', '', '$', '(a|i[16384])'),
    # CONSONANTS  (integrated: German, Polish, Russian, Romanian and English)
    ('rh', '^', '', 'r'),
    ('ssch', '', '', 'S'),
    ('chsch', '', '', 'xS'),
    ('tsch', '', '', 'tS'),
    ('sch', '', '[ei]', '(sk[65536]|S|StS[131072])'),  # german
    ('sch', '', '', '(S|StS[131072])'),  # german
    ('ssh', '', '', 'S'),
    ('sh', '', '[äöü]', 'sh'),  # german
    ('sh', '', '[aeiou]', '(S[131104]|sh)'),
    ('sh', '', '', 'S'),  # russian+english
    ('kh', '', '', '(x[131104]|kh)'),
    ('chs', '', '', '(ks[128]|xs|tSs[131104])'),
    # French "ch" is currently disabled
    # ("ch","","[ei]","(x|tS|k[65536]|S[64])"),
    # ("ch","","","(x|tS[131104]|S[64])"),
    ('ch', '', '[ei]', '(x|k[65536]|tS[131104])'),
    ('ch', '', '', '(x|tS[131104])'),
    ('ck', '', '', '(k|tsk[16384])'),
    ('czy', '', '', 'tSi'),
    ('cze', '', '[bcdgkpstwzż]', '(tSe|tSF)'),
    ('ciewicz', '', '', '(tsevitS|tSevitS)'),
    ('siewicz', '', '', '(sevitS|SevitS)'),
    ('ziewicz', '', '', '(zevitS|ZevitS)'),
    ('riewicz', '', '', 'rjevitS'),
    ('diewicz', '', '', 'djevitS'),
    ('tiewicz', '', '', 'tjevitS'),
    ('iewicz', '', '', 'evitS'),
    ('ewicz', '', '', 'evitS'),
    ('owicz', '', '', 'ovitS'),
    ('icz', '', '', 'itS'),
    ('cz', '', '', 'tS'),  # Polish
    ('cia', '', '[bcdgkpstwzż]', '(tSB[16384]|tsB)'),
    ('cia', '', '', '(tSa[16384]|tsa)'),
    ('cią', '', '[bp]', '(tSom[16384]|tsom)'),
    ('cią', '', '', '(tSon[16384]|tson)'),
    ('cię', '', '[bp]', '(tSem[16384]|tsem)'),
    ('cię', '', '', '(tSen[16384]|tsen)'),
    ('cie', '', '[bcdgkpstwzż]', '(tSF[16384]|tsF)'),
    ('cie', '', '', '(tSe[16384]|tse)'),
    ('cio', '', '', '(tSo[16384]|tso)'),
    ('ciu', '', '', '(tSu[16384]|tsu)'),
    ('ci', '', '$', '(tsi[16384]|tSi[81920]|tS[65536]|si)'),
    ('ci', '', '', '(tsi[16384]|tSi[81920]|si)'),
    ('ce', '', '[bcdgkpstwzż]', '(tsF[16384]|tSe[81920]|se)'),
    ('ce', '', '', '(tSe[81920]|tse[16384]|se)'),
    ('cy', '', '', '(si|tsi[16384])'),
    ('ssz', '', '', 'S'),  # Polish
    (
        'sz',
        '',
        '',
        'S',
    ),  # Polish; actually could also be Hungarian /s/, disabled here  # noqa: E501
    ('ssp', '', '', '(Sp[128]|sp)'),
    ('sp', '', '', '(Sp[128]|sp)'),
    ('sst', '', '', '(St[128]|st)'),
    ('st', '', '', '(St[128]|st)'),
    ('ss', '', '', 's'),
    ('sia', '', '[bcdgkpstwzż]', '(SB[16384]|sB[16384]|sja)'),
    ('sia', '', '', '(Sa[16384]|sja)'),
    ('sią', '', '[bp]', '(Som[16384]|som)'),
    ('sią', '', '', '(Son[16384]|son)'),
    ('się', '', '[bp]', '(Sem[16384]|sem)'),
    ('się', '', '', '(Sen[16384]|sen)'),
    ('sie', '', '[bcdgkpstwzż]', '(SF[16384]|sF|zi[128])'),
    ('sie', '', '', '(se|Se[16384]|zi[128])'),
    ('sio', '', '', '(So[16384]|so)'),
    ('siu', '', '', '(Su[16384]|sju)'),
    ('si', '', '', '(Si[16384]|si|zi[128])'),
    ('s', '', '[aeiouäöü]', '(s|z[128])'),
    ('gue', '', '', 'ge'),
    ('gui', '', '', 'gi'),
    ('guy', '', '', 'gi'),
    ('gh', '', '[ei]', '(g[65536]|gh)'),
    ('gauz', '', '$', 'haus'),
    ('gaus', '', '$', 'haus'),
    ('gol\'ts', '', '$', 'holts'),
    ('golts', '', '$', 'holts'),
    ('gol\'tz', '', '$', 'holts'),
    ('goltz', '', '', 'holts'),
    ('gol\'ts', '^', '', 'holts'),
    ('golts', '^', '', 'holts'),
    ('gol\'tz', '^', '', 'holts'),
    ('goltz', '^', '', 'holts'),
    ('gendler', '', '$', 'hendler'),
    ('gejmer', '', '$', 'hajmer'),
    ('gejm', '', '$', 'hajm'),
    ('geymer', '', '$', 'hajmer'),
    ('geym', '', '$', 'hajm'),
    ('geimer', '', '$', 'hajmer'),
    ('geim', '', '$', 'hajm'),
    ('gof', '', '$', 'hof'),
    ('ger', '', '$', 'ger'),
    ('gen', '', '$', 'gen'),
    ('gin', '', '$', 'gin'),
    ('gie', '', '$', '(ge|gi[128]|ji[64])'),
    ('gie', '', '', 'ge'),
    ('ge', '[yaeiou]', '', '(gE|xe[262144]|dZe[65568])'),
    ('gi', '[yaeiou]', '', '(gI|xi[262144]|dZi[65568])'),
    ('ge', '', '', '(gE|dZe[65568]|hE[131072]|xe[262144])'),
    ('gi', '', '', '(gI|dZi[65568]|hI[131072]|xi[262144])'),
    ('gy', '', '[aeouáéóúüöőű]', '(gi|dj[2048])'),
    ('gy', '', '', '(gi|d[2048])'),
    ('g', '[jyaeiou]', '[aouyei]', 'g'),
    ('g', '', '[aouei]', '(g|h[131072])'),
    ('ej', '', '', '(aj|eZ[65600]|ex[262144])'),
    ('ej', '', '', 'aj'),
    ('ly', '', '[au]', 'l'),
    ('li', '', '[au]', 'l'),
    ('lj', '', '[au]', 'l'),
    ('lio', '', '', '(lo|le[131072])'),
    ('lyo', '', '', '(lo|le[131072])'),
    ('ll', '', '', '(l|J[262144])'),
    ('j', '', '[aoeiuy]', '(j|dZ[32]|x[262144]|Z[65600])'),
    ('j', '', '', '(j|x[262144])'),
    ('pf', '', '', '(pf|p|f)'),
    ('ph', '', '', '(ph|f)'),
    ('qu', '', '', '(kv[128]|k)'),
    ('rze', 't', '', '(Se[16384]|re)'),  # polish
    ('rze', '', '', '(rze|rtsE[128]|Ze[16384]|re[16384]|rZe[16384])'),
    ('rzy', 't', '', '(Si[16384]|ri)'),  # polish
    ('rzy', '', '', '(Zi[16384]|ri[16384]|rZi)'),
    ('rz', 't', '', '(S[16384]|r)'),  # polish
    ('rz', '', '', '(rz|rts[128]|Z[16384]|r[16384]|rZ[16384])'),  # polish
    ('tz', '', '$', '(ts|tS[160])'),
    ('tz', '^', '', '(ts|tS[160])'),
    ('tz', '', '', '(ts[131232]|tz)'),
    ('zh', '', '', '(Z|zh[16384]|tsh[128])'),
    ('zia', '', '[bcdgkpstwzż]', '(ZB[16384]|zB[16384]|zja)'),
    ('zia', '', '', '(Za[16384]|zja)'),
    ('zią', '', '[bp]', '(Zom[16384]|zom)'),
    ('zią', '', '', '(Zon[16384]|zon)'),
    ('zię', '', '[bp]', '(Zem[16384]|zem)'),
    ('zię', '', '', '(Zen[16384]|zen)'),
    ('zie', '', '[bcdgkpstwzż]', '(ZF[16384]|zF[16384]|ze|tsi[128])'),
    ('zie', '', '', '(ze|Ze[16384]|tsi[128])'),
    ('zio', '', '', '(Zo[16384]|zo)'),
    ('ziu', '', '', '(Zu[16384]|zju)'),
    ('zi', '', '', '(Zi[16384]|zi|tsi[128])'),
    ('thal', '', '$', 'tal'),
    ('th', '^', '', 't'),
    ('th', '', '[aeiou]', '(t[128]|th)'),
    ('th', '', '', 't'),  # german
    ('vogel', '', '', '(vogel|fogel[128])'),
    ('v', '^', '', '(v|f[128])'),
    ('h', '[aeiouyäöü]', '', ''),  # german
    ('h', '', '', '(h|x[81920])'),
    ('h', '^', '', '(h|H[160])'),  # H can be exact "h" or approximate "kh"
    # VOWELS
    ('yi', ' ', '', 'i'),
    ('ii', '', ' ', 'i'),
    ('iy', '', ' ', 'i'),
    ('yy', '', ' ', 'i'),
    # ("e","","$","(e|)"),  # French & English rule disabled except for final -ine  # noqa: E501
    ('e', 'in', '$', '(e|[64])'),
    ('yj', '', '$', 'i'),  # russian
    ('ij', '', '$', 'i'),  # russian
    ('aue', '', '', 'aue'),
    ('oue', '', '', 'oue'),
    ('au', '', '', '(au|o[64])'),
    ('ou', '', '', '(ou|u[64])'),
    ('ue', '', '', '(Q|uje[131072])'),
    ('ae', '', '', '(Y[128]|aje[131072]|ae)'),
    ('oe', '', '', '(Y[128]|oje[131072]|oe)'),
    ('ee', '', '', '(i[32]|aje[131072]|e)'),
    ('ei', '', '', 'aj'),
    ('ey', '', '', 'aj'),
    ('eu', '', '', '(aj[128]|oj[128]|eu)'),
    ('i', '[aou]', '', 'j'),
    ('y', '[aou]', '', 'j'),
    ('ie', '', '[bcdgkpstwzż]', '(i[128]|e[16384]|ije[131072]|je)'),
    ('ie', '', '', '(i[128]|e[16384]|ije[131072]|je)'),
    ('ye', '', '', '(je|ije[131072])'),
    ('i', '', '[au]', 'j'),
    ('y', '', '[au]', 'j'),
    ('io', '', '', '(jo|e[131072])'),
    ('yo', '', '', '(jo|e[131072])'),
    ('ea', '', '', '(ea|ja[65536])'),
    ('e', '^', '', '(e|je[131072])'),
    ('oo', '', '', '(u[32]|o)'),
    ('uu', '', '', 'u'),
    # LANGUAGE SPECIFIC CHARACTERS
    ('ć', '', '', '(tS[16384]|ts)'),  # polish
    ('ł', '', '', 'l'),  # polish
    ('ń', '', '', 'n'),  # polish
    ('ñ', '', '', '(n|nj[262144])'),
    ('ś', '', '', '(S[16384]|s)'),  # polish
    ('ş', '', '', 'S'),  # romanian
    ('ţ', '', '', 'ts'),  # romanian
    ('ż', '', '', 'Z'),  # polish
    ('ź', '', '', '(Z[16384]|z)'),  # polish
    ('où', '', '', 'u'),  # french
    ('ą', '', '[bp]', 'om'),  # polish
    ('ą', '', '', 'on'),  # polish
    ('ä', '', '', '(Y|e)'),  # german
    ('á', '', '', 'a'),  # hungarian
    ('ă', '', '', '(e[65536]|a)'),  # romanian
    ('à', '', '', 'a'),  # french
    ('â', '', '', 'a'),  # french+romanian
    ('é', '', '', 'e'),
    ('è', '', '', 'e'),  # french
    ('ê', '', '', 'e'),  # french
    ('ę', '', '[bp]', 'em'),  # polish
    ('ę', '', '', 'en'),  # polish
    ('í', '', '', 'i'),
    ('î', '', '', 'i'),
    ('ö', '', '', 'Y'),
    ('ő', '', '', 'Y'),  # hungarian
    ('ó', '', '', '(u[16384]|o)'),
    ('ű', '', '', 'Q'),
    ('ü', '', '', 'Q'),
    ('ú', '', '', 'u'),
    ('ű', '', '', 'Q'),  # hungarian
    ('ß', '', '', 's'),  # german
    ('\'', '', '', ''),
    ('"', '', '', ''),
    ('a', '', '[bcdgkpstwzż]', '(A|B[16384])'),
    ('e', '', '[bcdgkpstwzż]', '(E|F[16384])'),
    ('o', '', '[bcćdgklłmnńrsśtwzźż]', '(O|P[16384])'),
    # LATIN ALPHABET
    ('a', '', '', 'A'),
    ('b', '', '', 'b'),
    ('c', '', '', '(k|ts[16384])'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'O'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'U'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),  # English disabled
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', '(ts[128]|z)'),
)

# ash/rulescyrillic.php

_ASH_RULES_CYRILLIC = (
    ('ця', '', '', 'tsa'),
    ('цю', '', '', 'tsu'),
    ('циа', '', '', 'tsa'),
    ('цие', '', '', 'tse'),
    ('цио', '', '', 'tso'),
    ('циу', '', '', 'tsu'),
    ('сие', '', '', 'se'),
    ('сио', '', '', 'so'),
    ('зие', '', '', 'ze'),
    ('зио', '', '', 'zo'),
    ('гауз', '', '$', 'haus'),
    ('гаус', '', '$', 'haus'),
    ('гольц', '', '$', 'holts'),
    ('геймер', '', '$', 'hajmer'),
    ('гейм', '', '$', 'hajm'),
    ('гоф', '', '$', 'hof'),
    ('гер', '', '$', 'ger'),
    ('ген', '', '$', 'gen'),
    ('гин', '', '$', 'gin'),
    ('г', '(й|ё|я|ю|ы|а|е|о|и|у)', '(а|е|о|и|у)', 'g'),
    ('г', '', '(а|е|о|и|у)', '(g|h)'),
    ('ля', '', '', 'la'),
    ('лю', '', '', 'lu'),
    ('лё', '', '', '(le|lo)'),
    ('лио', '', '', '(le|lo)'),
    ('ле', '', '', '(lE|lo)'),
    ('ийе', '', '', 'je'),
    ('ие', '', '', 'je'),
    ('ыйе', '', '', 'je'),
    ('ые', '', '', 'je'),
    ('ий', '', '(а|о|у)', 'j'),
    ('ый', '', '(а|о|у)', 'j'),
    ('ий', '', '$', 'i'),
    ('ый', '', '$', 'i'),
    ('ё', '', '', '(e|jo)'),
    ('ей', '^', '', '(jaj|aj)'),
    ('е', '(а|е|о|у)', '', 'je'),
    ('е', '^', '', 'je'),
    ('эй', '', '', 'aj'),
    ('ей', '', '', 'aj'),
    ('ауе', '', '', 'aue'),
    ('ауэ', '', '', 'aue'),
    ('а', '', '', 'a'),
    ('б', '', '', 'b'),
    ('в', '', '', 'v'),
    ('г', '', '', 'g'),
    ('д', '', '', 'd'),
    ('е', '', '', 'E'),
    ('ж', '', '', 'Z'),
    ('з', '', '', 'z'),
    ('и', '', '', 'I'),
    ('й', '', '', 'j'),
    ('к', '', '', 'k'),
    ('л', '', '', 'l'),
    ('м', '', '', 'm'),
    ('н', '', '', 'n'),
    ('о', '', '', 'o'),
    ('п', '', '', 'p'),
    ('р', '', '', 'r'),
    ('с', '', 'с', ''),
    ('с', '', '', 's'),
    ('т', '', '', 't'),
    ('у', '', '', 'u'),
    ('ф', '', '', 'f'),
    ('х', '', '', 'x'),
    ('ц', '', '', 'ts'),
    ('ч', '', '', 'tS'),
    ('ш', '', '', 'S'),
    ('щ', '', '', 'StS'),
    ('ъ', '', '', ''),
    ('ы', '', '', 'I'),
    ('ь', '', '', ''),
    ('э', '', '', 'E'),
    ('ю', '', '', 'ju'),
    ('я', '', '', 'ja'),
)

# ash/rulesenglish.php

_ASH_RULES_ENGLISH = (
    # CONSONANTS
    ('tch', '', '', 'tS'),
    ('ch', '', '', '(tS|x)'),
    ('ck', '', '', 'k'),
    ('cc', '', '[iey]', 'ks'),  # success, accent
    ('c', '', 'c', ''),
    ('c', '', '[iey]', 's'),  # circle
    ('c', '', '', 'k'),  # candy
    ('gh', '^', '', 'g'),  # ghost
    ('gh', '', '', '(g|f|w)'),  # burgh | tough | bough
    ('gn', '', '', '(gn|n)'),
    ('g', '', '[iey]', '(g|dZ)'),  # get, gem, giant, gigabyte
    # ("th","","","(6|8|t)"),
    ('th', '', '', 't'),
    ('kh', '', '', 'x'),
    ('ph', '', '', 'f'),
    ('sch', '', '', '(S|sk)'),
    ('sh', '', '', 'S'),
    ('who', '^', '', 'hu'),
    ('wh', '^', '', 'w'),
    ('h', '', '$', ''),  # hard to find an example that isn't in a name
    ('h', '', '[^aeiou]', ''),  # hard to find an example that isn't in a name
    ('h', '^', '', 'H'),
    ('h', '', '', 'h'),
    ('j', '', '', 'dZ'),
    ('kn', '^', '', 'n'),  # knight
    ('mb', '', '$', 'm'),
    ('ng', '', '$', '(N|ng)'),
    ('pn', '^', '', '(pn|n)'),
    ('ps', '^', '', '(ps|s)'),
    ('qu', '', '', 'kw'),
    ('q', '', '', 'k'),
    ('tia', '', '', '(So|Sa)'),
    ('tio', '', '', 'So'),
    ('wr', '^', '', 'r'),
    (
        'w',
        '',
        '',
        '(w|v)',
    ),  # the variant "v" is for spellings coming from German/Polish  # noqa: E501
    ('x', '^', '', 'z'),
    ('x', '', '', 'ks'),
    # VOWELS
    ('yi', ' ', '', 'i'),
    ('y', '^', '[aeiouy]', 'j'),
    ('aue', '', '', 'aue'),
    ('oue', '', '', '(aue|oue)'),
    ('ai', '', '', '(aj|e)'),  # rain | said
    ('ay', '', '', 'aj'),
    ('a', '', '[^aeiou]e', 'aj'),  # plane (actually "ej")
    ('a', '', '', '(e|o|a)'),  # hat | call | part
    ('ei', '', '', '(aj|i)'),  # weigh | receive
    ('ey', '', '', '(aj|i)'),  # hey | barley
    ('ear', '', '', 'ia'),  # tear
    ('ea', '', '', '(i|e)'),  # reason | treasure
    ('ee', '', '', 'i'),  # between
    ('e', '', '[^aeiou]e', 'i'),  # meter
    ('e', '', '$', '(|E)'),  # blame, badge
    ('e', '', '', 'E'),  # bed
    ('ie', '', '', 'i'),  # believe
    ('i', '', '[^aeiou]e', 'aj'),  # five
    ('i', '', '', 'I'),  # hit -- Morse disagrees, feels it should go to I
    ('oa', '', '', 'ou'),  # toad
    ('oi', '', '', 'oj'),  # join
    ('oo', '', '', 'u'),  # food
    ('ou', '', '', '(u|ou)'),  # through | tough | could
    ('oy', '', '', 'oj'),  # boy
    ('o', '', '[^aeiou]e', 'ou'),  # rode
    ('o', '', '', '(o|a)'),  # hot -- Morse disagrees, feels it should go to 9
    ('u', '', '[^aeiou]e', '(ju|u)'),  # cute | flute
    (
        'u',
        '',
        'r',
        '(e|u)',
    ),  # turn -- Morse disagrees, feels it should go to E  # noqa: E501
    ('u', '', '', '(u|a)'),  # put
    ('y', '', '', 'i'),
    # TRIVIAL
    ('b', '', '', 'b'),
    ('d', '', '', 'd'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('p', '', '', 'p'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('v', '', '', 'v'),
    ('z', '', '', 'z'),
)

# ash/rulesfrench.php

# Ashkenazic
_ASH_RULES_FRENCH = (
    # CONSONANTS
    ('kh', '', '', 'x'),  # foreign
    ('ph', '', '', 'f'),
    ('ç', '', '', 's'),
    ('x', '', '', 'ks'),
    ('ch', '', '', 'S'),
    ('c', '', '[eiyéèê]', 's'),
    ('c', '', '', 'k'),
    ('gn', '', '', '(n|gn)'),
    ('g', '', '[eiy]', 'Z'),
    ('gue', '', '$', 'k'),
    ('gu', '', '[eiy]', 'g'),
    # ("aill","","e","aj"), # non Jewish
    # ("ll","","e","(l|j)"), # non Jewish
    ('que', '', '$', 'k'),
    ('qu', '', '', 'k'),
    ('q', '', '', 'k'),
    ('s', '[aeiouyéèê]', '[aeiouyéèê]', 'z'),
    ('h', '[bdgt]', '', ''),  # translit from Arabic
    ('h', '', '$', ''),  # foreign
    ('j', '', '', 'Z'),
    ('w', '', '', 'v'),
    ('ouh', '', '[aioe]', '(v|uh)'),
    ('ou', '', '[aeio]', 'v'),
    ('uo', '', '', '(vo|o)'),
    ('u', '', '[aeio]', 'v'),
    # VOWELS
    ('aue', '', '', 'aue'),
    ('eau', '', '', 'o'),
    # ("au","","","(o|au)"), # non Jewish
    ('ai', '', '', 'aj'),  # [e] is non Jewish
    ('ay', '', '', 'aj'),  # [e] is non Jewish
    ('é', '', '', 'e'),
    ('ê', '', '', 'e'),
    ('è', '', '', 'e'),
    ('à', '', '', 'a'),
    ('â', '', '', 'a'),
    ('où', '', '', 'u'),
    ('ou', '', '', 'u'),
    ('oi', '', '', 'oj'),  # [ua] is non Jewish
    ('ei', '', '', 'aj'),  # [e] is non Jewish
    ('ey', '', '', 'aj'),  # [e] non Jewish
    # ("eu","","","(e|o)"), # non Jewish
    ('y', '[ou]', '', 'j'),
    ('e', '', '$', '(e|)'),
    ('i', '', '[aou]', 'j'),
    ('y', '', '[aoeu]', 'j'),
    ('yi', '', '', 'i'),
    ('ii', '', '', 'i'),
    ('yy', '', '', 'i'),
    ('y', '', '', 'i'),
    # TRIVIAL
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),  # only Ashkenazic
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),  # only Ashkenazic
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('z', '', '', 'z'),
)

# ash/rulesgerman.php

# Ashkenazic
_ASH_RULES_GERMAN = (
    # CONSONANTS
    ('ziu', '', '', 'tsu'),
    ('zia', '', '', 'tsa'),
    ('zio', '', '', 'tso'),
    ('ssch', '', '', 'S'),
    ('chsch', '', '', 'xS'),
    ('ewitsch', '', '$', 'evitS'),
    ('owitsch', '', '$', 'ovitS'),
    ('evitsch', '', '$', 'evitS'),
    ('ovitsch', '', '$', 'ovitS'),
    ('witsch', '', '$', 'vitS'),
    ('vitsch', '', '$', 'vitS'),
    ('sch', '', '', 'S'),
    ('chs', '', '', 'ks'),
    ('ch', '', '', 'x'),
    ('ck', '', '', 'k'),
    ('c', '', '[eiy]', 'ts'),
    ('sp', '^', '', 'Sp'),
    ('st', '^', '', 'St'),
    ('ssp', '', '', '(Sp|sp)'),
    ('sp', '', '', '(Sp|sp)'),
    ('sst', '', '', '(St|st)'),
    ('st', '', '', '(St|st)'),
    ('pf', '', '', '(pf|p|f)'),
    ('ph', '', '', '(ph|f)'),
    ('qu', '', '', 'kv'),
    ('ewitz', '', '$', '(evits|evitS)'),
    ('ewiz', '', '$', '(evits|evitS)'),
    ('evitz', '', '$', '(evits|evitS)'),
    ('eviz', '', '$', '(evits|evitS)'),
    ('owitz', '', '$', '(ovits|ovitS)'),
    ('owiz', '', '$', '(ovits|ovitS)'),
    ('ovitz', '', '$', '(ovits|ovitS)'),
    ('oviz', '', '$', '(ovits|ovitS)'),
    ('witz', '', '$', '(vits|vitS)'),
    ('wiz', '', '$', '(vits|vitS)'),
    ('vitz', '', '$', '(vits|vitS)'),
    ('viz', '', '$', '(vits|vitS)'),
    ('tz', '', '', 'ts'),
    ('thal', '', '$', 'tal'),
    ('th', '^', '', 't'),
    ('th', '', '[äöüaeiou]', '(t|th)'),
    ('th', '', '', 't'),
    ('rh', '^', '', 'r'),
    ('h', '[aeiouyäöü]', '', ''),
    ('h', '^', '', 'H'),
    ('ss', '', '', 's'),
    ('s', '', '[äöüaeiouy]', '(z|s)'),
    ('s', '[aeiouyäöüj]', '[aeiouyäöü]', 'z'),
    ('ß', '', '', 's'),
    # VOWELS
    ('ij', '', '$', 'i'),
    ('aue', '', '', 'aue'),
    ('ue', '', '', 'Q'),
    ('ae', '', '', 'Y'),
    ('oe', '', '', 'Y'),
    ('ü', '', '', 'Q'),
    ('ä', '', '', '(Y|e)'),
    ('ö', '', '', 'Y'),
    ('ei', '', '', 'aj'),
    ('ey', '', '', 'aj'),
    ('eu', '', '', '(aj|oj)'),
    ('i', '[aou]', '', 'j'),
    ('y', '[aou]', '', 'j'),
    ('ie', '', '', 'I'),
    ('i', '', '[aou]', 'j'),
    ('y', '', '[aoeu]', 'j'),
    # FOREIGN LETTERs
    ('ñ', '', '', 'n'),
    ('ã', '', '', 'a'),
    ('ő', '', '', 'o'),
    ('ű', '', '', 'u'),
    ('ç', '', '', 's'),
    # ALPHABET
    ('a', '', '', 'A'),
    ('b', '', '', 'b'),
    ('c', '', '', 'k'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'O'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'U'),
    ('v', '', '', '(f|v)'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', 'ts'),
)

# ash/ruleshebrew.php

# Ashkenazic
_ASH_RULES_HEBREW = (
    ('אי', '', '', 'i'),
    ('עי', '', '', 'i'),
    ('עו', '', '', 'VV'),
    ('או', '', '', 'VV'),
    ('ג׳', '', '', 'Z'),
    ('ד׳', '', '', 'dZ'),
    ('א', '', '', 'L'),
    ('ב', '', '', 'b'),
    ('ג', '', '', 'g'),
    ('ד', '', '', 'd'),
    ('ה', '^', '', '1'),
    ('ה', '', '$', '1'),
    ('ה', '', '', ''),
    ('וו', '', '', 'V'),
    ('וי', '', '', 'WW'),
    ('ו', '', '', 'W'),
    ('ז', '', '', 'z'),
    ('ח', '', '', 'X'),
    ('ט', '', '', 'T'),
    ('יי', '', '', 'i'),
    ('י', '', '', 'i'),
    ('ך', '', '', 'X'),
    ('כ', '^', '', 'K'),
    ('כ', '', '', 'k'),
    ('ל', '', '', 'l'),
    ('ם', '', '', 'm'),
    ('מ', '', '', 'm'),
    ('ן', '', '', 'n'),
    ('נ', '', '', 'n'),
    ('ס', '', '', 's'),
    ('ע', '', '', 'L'),
    ('ף', '', '', 'f'),
    ('פ', '', '', 'f'),
    ('ץ', '', '', 'C'),
    ('צ', '', '', 'C'),
    ('ק', '', '', 'K'),
    ('ר', '', '', 'r'),
    ('ש', '', '', 's'),
    ('ת', '', '', 'TB'),  # only Ashkenazic
)

# ash/ruleshungarian.php

# ASHKENAZIC
_ASH_RULES_HUNGARIAN = (
    # CONSONANTS
    ('sz', '', '', 's'),
    ('zs', '', '', 'Z'),
    ('cs', '', '', 'tS'),
    ('ay', '', '', '(oj|aj)'),
    ('ai', '', '', '(oj|aj)'),
    ('aj', '', '', '(oj|aj)'),
    ('ei', '', '', 'aj'),  # German element
    ('ey', '', '', 'aj'),  # German element
    ('y', '[áo]', '', 'j'),
    ('i', '[áo]', '', 'j'),
    ('ee', '', '', '(aj|e)'),  # actually ej
    ('ely', '', '', '(aj|eli)'),  # actually ej
    ('ly', '', '', '(j|li)'),
    ('gy', '', '[aeouáéóúüöőű]', 'dj'),
    ('gy', '', '', '(d|gi)'),
    ('ny', '', '[aeouáéóúüöőű]', 'nj'),
    ('ny', '', '', '(n|ni)'),
    ('ty', '', '[aeouáéóúüöőű]', 'tj'),
    ('ty', '', '', '(t|ti)'),
    ('qu', '', '', '(ku|kv)'),
    ('h', '', '$', ''),
    # VOWELS
    ('á', '', '', 'a'),
    ('é', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ó', '', '', 'o'),
    ('ö', '', '', 'Y'),
    ('ő', '', '', 'Y'),
    ('ú', '', '', 'u'),
    ('ü', '', '', 'Q'),
    ('ű', '', '', 'Q'),
    # LATIN ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'ts'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', '(S|s)'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('z', '', '', 'z'),
)

# ash/rulespolish.php

# Ashkenazic
_ASH_RULES_POLISH = (
    # CONVERTING FEMININE TO MASCULINE
    ('ska', '', '$', 'ski'),
    ('cka', '', '$', 'tski'),
    ('lowa', '', '$', '(lova|lof|l|el)'),
    ('kowa', '', '$', '(kova|kof|k|ek)'),
    ('owa', '', '$', '(ova|of|)'),
    ('lowna', '', '$', '(lovna|levna|l|el)'),
    ('kowna', '', '$', '(kovna|k|ek)'),
    ('owna', '', '$', '(ovna|)'),
    ('lówna', '', '$', '(l|el)'),
    ('kówna', '', '$', '(k|ek)'),
    ('ówna', '', '$', ''),
    ('a', '', '$', '(a|i)'),
    # CONSONANTS
    ('czy', '', '', 'tSi'),
    ('cze', '', '[bcdgkpstwzż]', '(tSe|tSF)'),
    ('ciewicz', '', '', '(tsevitS|tSevitS)'),
    ('siewicz', '', '', '(sevitS|SevitS)'),
    ('ziewicz', '', '', '(zevitS|ZevitS)'),
    ('riewicz', '', '', 'rjevitS'),
    ('diewicz', '', '', 'djevitS'),
    ('tiewicz', '', '', 'tjevitS'),
    ('iewicz', '', '', 'evitS'),
    ('ewicz', '', '', 'evitS'),
    ('owicz', '', '', 'ovitS'),
    ('icz', '', '', 'itS'),
    ('cz', '', '', 'tS'),
    ('ch', '', '', 'x'),
    ('cia', '', '[bcdgkpstwzż]', '(tSB|tsB)'),
    ('cia', '', '', '(tSa|tsa)'),
    ('cią', '', '[bp]', '(tSom|tsom)'),
    ('cią', '', '', '(tSon|tson)'),
    ('cię', '', '[bp]', '(tSem|tsem)'),
    ('cię', '', '', '(tSen|tsen)'),
    ('cie', '', '[bcdgkpstwzż]', '(tSF|tsF)'),
    ('cie', '', '', '(tSe|tse)'),
    ('cio', '', '', '(tSo|tso)'),
    ('ciu', '', '', '(tSu|tsu)'),
    ('ci', '', '', '(tSi|tsI)'),
    ('ć', '', '', '(tS|ts)'),
    ('ssz', '', '', 'S'),
    ('sz', '', '', 'S'),
    ('sia', '', '[bcdgkpstwzż]', '(SB|sB|sja)'),
    ('sia', '', '', '(Sa|sja)'),
    ('sią', '', '[bp]', '(Som|som)'),
    ('sią', '', '', '(Son|son)'),
    ('się', '', '[bp]', '(Sem|sem)'),
    ('się', '', '', '(Sen|sen)'),
    ('sie', '', '[bcdgkpstwzż]', '(SF|sF|se)'),
    ('sie', '', '', '(Se|se)'),
    ('sio', '', '', '(So|so)'),
    ('siu', '', '', '(Su|sju)'),
    ('si', '', '', '(Si|sI)'),
    ('ś', '', '', '(S|s)'),
    ('zia', '', '[bcdgkpstwzż]', '(ZB|zB|zja)'),
    ('zia', '', '', '(Za|zja)'),
    ('zią', '', '[bp]', '(Zom|zom)'),
    ('zią', '', '', '(Zon|zon)'),
    ('zię', '', '[bp]', '(Zem|zem)'),
    ('zię', '', '', '(Zen|zen)'),
    ('zie', '', '[bcdgkpstwzż]', '(ZF|zF)'),
    ('zie', '', '', '(Ze|ze)'),
    ('zio', '', '', '(Zo|zo)'),
    ('ziu', '', '', '(Zu|zju)'),
    ('zi', '', '', '(Zi|zI)'),
    ('że', '', '[bcdgkpstwzż]', '(Ze|ZF)'),
    ('że', '', '[bcdgkpstwzż]', '(Ze|ZF|ze|zF)'),
    ('że', '', '', 'Ze'),
    ('źe', '', '', '(Ze|ze)'),
    ('ży', '', '', 'Zi'),
    ('źi', '', '', '(Zi|zi)'),
    ('ż', '', '', 'Z'),
    ('ź', '', '', '(Z|z)'),
    ('rze', 't', '', '(Se|re)'),
    ('rze', '', '', '(Ze|re|rZe)'),
    ('rzy', 't', '', '(Si|ri)'),
    ('rzy', '', '', '(Zi|ri|rZi)'),
    ('rz', 't', '', '(S|r)'),
    ('rz', '', '', '(Z|r|rZ)'),
    ('lio', '', '', '(lo|le)'),
    ('ł', '', '', 'l'),
    ('ń', '', '', 'n'),
    ('qu', '', '', 'k'),
    ('s', '', 's', ''),
    # VOWELS
    ('ó', '', '', '(u|o)'),
    ('ą', '', '[bp]', 'om'),
    ('ę', '', '[bp]', 'em'),
    ('ą', '', '', 'on'),
    ('ę', '', '', 'en'),
    ('ije', '', '', 'je'),
    ('yje', '', '', 'je'),
    ('iie', '', '', 'je'),
    ('yie', '', '', 'je'),
    ('iye', '', '', 'je'),
    ('yye', '', '', 'je'),
    ('ij', '', '[aou]', 'j'),
    ('yj', '', '[aou]', 'j'),
    ('ii', '', '[aou]', 'j'),
    ('yi', '', '[aou]', 'j'),
    ('iy', '', '[aou]', 'j'),
    ('yy', '', '[aou]', 'j'),
    ('rie', '', '', 'rje'),
    ('die', '', '', 'dje'),
    ('tie', '', '', 'tje'),
    ('ie', '', '[bcdgkpstwzż]', 'F'),
    ('ie', '', '', 'e'),
    ('aue', '', '', 'aue'),
    ('au', '', '', 'au'),
    ('ei', '', '', 'aj'),
    ('ey', '', '', 'aj'),
    ('ej', '', '', 'aj'),
    ('ai', '', '', 'aj'),
    ('ay', '', '', 'aj'),
    ('aj', '', '', 'aj'),
    ('i', '[ou]', '', 'j'),
    ('y', '[ou]', '', 'j'),
    ('i', '', '[aou]', 'j'),
    ('y', '', '[aeou]', 'j'),
    ('a', '', '[bcdgkpstwzż]', 'B'),
    ('e', '', '[bcdgkpstwzż]', '(E|F)'),
    ('o', '', '[bcćdgklłmnńrsśtwzźż]', 'P'),
    # ALPHABET
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('c', '', '', 'ts'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', '(h|x)'),
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('q', '', '', 'k'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'I'),
    ('z', '', '', 'z'),
)

# ash/rulesromanian.php

_ASH_RULES_ROMANIAN = (
    ('j', '', '', 'Z'),
    ('ce', '', '', 'tSe'),
    ('ci', '', '', '(tSi|tS)'),
    ('ch', '', '[ei]', 'k'),
    ('ch', '', '', 'x'),  # foreign
    ('c', '', '', 'k'),
    ('gi', '', '', '(dZi|dZ)'),
    ('g', '', '[ei]', 'dZ'),
    ('gh', '', '', 'g'),
    ('ei', '', '', 'aj'),
    ('i', '[aou]', '', 'j'),
    ('i', '', '[aeou]', 'j'),
    ('ţ', '', '', 'ts'),
    ('ş', '', '', 'S'),
    ('h', '', '', '(x|h)'),
    ('qu', '', '', 'k'),
    ('q', '', '', 'k'),
    ('w', '', '', 'v'),
    ('x', '', '', 'ks'),
    ('y', '', '', 'i'),
    ('î', '', '', 'i'),
    ('ea', '', '', 'ja'),
    ('ă', '', '', '(e|a)'),
    ('aue', '', '', 'aue'),
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('i', '', '', 'I'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('z', '', '', 'z'),
)

# ash/rulesrussian.php

_ASH_RULES_RUSSIAN = (
    # CONVERTING FEMININE TO MASCULINE
    ('yna', '', '$', '(in|ina)'),
    ('ina', '', '$', '(in|ina)'),
    ('liova', '', '$', '(lof|lef)'),
    ('lova', '', '$', '(lof|lef|lova)'),
    ('ova', '', '$', '(of|ova)'),
    ('eva', '', '$', '(ef|ova)'),
    ('aia', '', '$', '(aja|i)'),
    ('aja', '', '$', '(aja|i)'),
    ('aya', '', '$', '(aja|i)'),
    # SPECIFIC CONSONANTS
    ('tsya', '', '', 'tsa'),
    ('tsyu', '', '', 'tsu'),
    ('tsia', '', '', 'tsa'),
    ('tsie', '', '', 'tse'),
    ('tsio', '', '', 'tso'),
    ('tsye', '', '', 'tse'),
    ('tsyo', '', '', 'tso'),
    ('tsiu', '', '', 'tsu'),
    ('sie', '', '', 'se'),
    ('sio', '', '', 'so'),
    ('zie', '', '', 'ze'),
    ('zio', '', '', 'zo'),
    ('sye', '', '', 'se'),
    ('syo', '', '', 'so'),
    ('zye', '', '', 'ze'),
    ('zyo', '', '', 'zo'),
    ('gauz', '', '$', 'haus'),
    ('gaus', '', '$', 'haus'),
    ('gol\'ts', '', '$', 'holts'),
    ('golts', '', '$', 'holts'),
    ('gol\'tz', '', '$', 'holts'),
    ('goltz', '', '$', 'holts'),
    ('gejmer', '', '$', 'hajmer'),
    ('gejm', '', '$', 'hajm'),
    ('geimer', '', '$', 'hajmer'),
    ('geim', '', '$', 'hajm'),
    ('geymer', '', '$', 'hajmer'),
    ('geym', '', '$', 'hajm'),
    ('gendler', '', '$', 'hendler'),
    ('gof', '', '$', 'hof'),
    ('gojf', '', '$', 'hojf'),
    ('goyf', '', '$', 'hojf'),
    ('goif', '', '$', 'hojf'),
    ('ger', '', '$', 'ger'),
    ('gen', '', '$', 'gen'),
    ('gin', '', '$', 'gin'),
    ('gg', '', '', 'g'),
    ('g', '[jaeoiuy]', '[aeoiu]', 'g'),
    ('g', '', '[aeoiu]', '(g|h)'),
    ('kh', '', '', 'x'),
    (
        'ch',
        '',
        '',
        '(tS|x)',
    ),  # in DJSRE the rule is simpler: ("ch","","","tS")  # noqa: E501
    ('sch', '', '', '(StS|S)'),
    ('ssh', '', '', 'S'),
    ('sh', '', '', 'S'),
    ('zh', '', '', 'Z'),
    ('tz', '', '$', 'ts'),  # not in DJSRE
    ('tz', '', '', '(ts|tz)'),  # not in DJSRE
    ('c', '', '[iey]', 's'),  # not in DJSRE
    ('c', '', '', 'k'),  # not in DJSRE
    ('qu', '', '', '(kv|k)'),  # not in DJSRE
    ('q', '', '', 'k'),  # not in DJSRE
    ('s', '', 's', ''),
    ('w', '', '', 'v'),  # not in DJSRE
    ('x', '', '', 'ks'),  # not in DJSRE
    # SPECIFIC VOWELS
    ('lya', '', '', 'la'),
    ('lyu', '', '', 'lu'),
    ('lia', '', '', 'la'),  # not in DJSRE
    ('liu', '', '', 'lu'),  # not in DJSRE
    ('lja', '', '', 'la'),  # not in DJSRE
    ('lju', '', '', 'lu'),  # not in DJSRE
    ('le', '', '', '(lo|lE)'),  # not in DJSRE
    ('lyo', '', '', '(lo|le)'),  # not in DJSRE
    ('lio', '', '', '(lo|le)'),
    ('ije', '', '', 'je'),
    ('ie', '', '', 'je'),
    ('iye', '', '', 'je'),
    ('iie', '', '', 'je'),
    ('yje', '', '', 'je'),
    ('ye', '', '', 'je'),
    ('yye', '', '', 'je'),
    ('yie', '', '', 'je'),
    ('ij', '', '[aou]', 'j'),
    ('iy', '', '[aou]', 'j'),
    ('ii', '', '[aou]', 'j'),
    ('yj', '', '[aou]', 'j'),
    ('yy', '', '[aou]', 'j'),
    ('yi', '', '[aou]', 'j'),
    ('io', '', '', '(jo|e)'),
    ('i', '', '[au]', 'j'),
    ('i', '[aou]', '', 'j'),  # not in DJSRE
    ('ei', '', '', 'aj'),  # not in DJSRE
    ('ey', '', '', 'aj'),  # not in DJSRE
    ('ej', '', '', 'aj'),
    ('yo', '', '', '(jo|e)'),  # not in DJSRE
    ('y', '', '[au]', 'j'),
    ('y', '[aiou]', '', 'j'),  # not in DJSRE
    ('ii', '', ' ', 'i'),  # not in DJSRE
    ('iy', '', ' ', 'i'),  # not in DJSRE
    ('yy', '', ' ', 'i'),  # not in DJSRE
    ('yi', '', ' ', 'i'),  # not in DJSRE
    ('yj', '', '$', 'i'),
    ('ij', '', '$', 'i'),
    (
        'e',
        '^',
        '',
        '(je|E)',
    ),  # in DJSRE the rule is simpler: ("e","^","","je")  # noqa: E501
    (
        'ee',
        '',
        '',
        '(aje|i)',
    ),  # in DJSRE the rule is simpler: ("ee","","","(eje|aje)")  # noqa: E501
    ('e', '[aou]', '', 'je'),
    ('y', '', '', 'I'),
    ('oo', '', '', '(oo|u)'),  # not in DJSRE
    ('\'', '', '', ''),
    ('"', '', '', ''),
    ('aue', '', '', 'aue'),
    # TRIVIAL
    ('a', '', '', 'a'),
    ('b', '', '', 'b'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),  # not in DJSRE
    ('i', '', '', 'I'),
    ('j', '', '', 'j'),
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
    ('v', '', '', 'v'),
    ('z', '', '', 'z'),
)

# ash/rulesspanish.php

# Ashkenazic = Argentina
_ASH_RULES_SPANISH = (
    # CONSONANTS
    ('ñ', '', '', '(n|nj)'),
    ('ch', '', '', '(tS|dZ)'),  # dZ is typical for Argentina
    ('h', '[bdgt]', '', ''),  # translit. from Arabic
    ('h', '', '$', ''),  # foreign
    ('j', '', '', 'x'),
    ('x', '', '', 'ks'),
    ('ll', '', '', '(l|Z)'),  # Z is typical for Argentina, only Ashkenazic
    ('w', '', '', 'v'),  # foreign words
    ('v', '', '', '(b|v)'),
    ('b', '', '', '(b|v)'),
    ('m', '', '[bpvf]', '(m|n)'),
    ('c', '', '[ei]', 's'),
    ('c', '', '', 'k'),
    (
        'z',
        '',
        '',
        '(z|s)',
    ),  # as "c" befoire "e" or "i", in Spain it is like unvoiced English "th"  # noqa: E501
    ('gu', '', '[ei]', '(g|gv)'),  # "gv" because "u" can actually be "ü"
    ('g', '', '[ei]', '(x|g)'),  # "g" only for foreign words
    ('qu', '', '', 'k'),
    ('q', '', '', 'k'),
    ('uo', '', '', '(vo|o)'),
    ('u', '', '[aei]', 'v'),
    (
        'y',
        '',
        '',
        '(i|j|S|Z)',
    ),  # S or Z are peculiar to South America; only Ashkenazic  # noqa: E501
    # VOWELS
    ('ü', '', '', 'v'),
    ('á', '', '', 'a'),
    ('é', '', '', 'e'),
    ('í', '', '', 'i'),
    ('ó', '', '', 'o'),
    ('ú', '', '', 'u'),
    # TRIVIAL
    ('a', '', '', 'a'),
    ('d', '', '', 'd'),
    ('e', '', '', 'E'),  # Only Ashkenazic
    ('f', '', '', 'f'),
    ('g', '', '', 'g'),
    ('h', '', '', 'h'),
    ('i', '', '', 'I'),  # Only Ashkenazic
    ('k', '', '', 'k'),
    ('l', '', '', 'l'),
    ('m', '', '', 'm'),
    ('n', '', '', 'n'),
    ('o', '', '', 'o'),
    ('p', '', '', 'p'),
    ('r', '', '', 'r'),
    ('s', '', '', 's'),
    ('t', '', '', 't'),
    ('u', '', '', 'u'),
)

BMDATA = {}

BMDATA['gen'] = {}
BMDATA['gen']['approx'] = {}
BMDATA['gen']['exact'] = {}
BMDATA['gen']['rules'] = {}
BMDATA['gen']['hebrew'] = {}

BMDATA['gen']['language_rules'] = _GEN_LANGUAGE_RULES
BMDATA['gen']['languages'] = _GEN_LANGUAGES
BMDATA['gen']['approx'][1] = _GEN_APPROX_ANY
BMDATA['gen']['approx'][2] = _GEN_APPROX_ARABIC
BMDATA['gen']['approx']['common'] = (
    _GEN_EXACT_APPROX_COMMON + _GEN_APPROX_COMMON
)  # noqa: E501
BMDATA['gen']['approx'][4] = _GEN_APPROX_RUSSIAN
BMDATA['gen']['approx'][8] = _GEN_APPROX_FRENCH
BMDATA['gen']['approx'][16] = _GEN_APPROX_FRENCH
BMDATA['gen']['approx'][32] = _GEN_APPROX_ENGLISH
BMDATA['gen']['approx'][64] = _GEN_APPROX_FRENCH
BMDATA['gen']['approx'][128] = _GEN_APPROX_GERMAN
BMDATA['gen']['approx'][256] = _GEN_APPROX_FRENCH
BMDATA['gen']['approx'][512] = _GEN_APPROX_FRENCH + _GEN_APPROX_GREEKLATIN
BMDATA['gen']['approx'][1024] = _GEN_APPROX_HEBREW
BMDATA['gen']['approx'][2048] = _GEN_APPROX_FRENCH
BMDATA['gen']['approx'][4096] = _GEN_APPROX_FRENCH
BMDATA['gen']['approx'][8192] = _GEN_APPROX_FRENCH
BMDATA['gen']['approx'][16384] = _GEN_APPROX_POLISH
BMDATA['gen']['approx'][32768] = _GEN_APPROX_FRENCH
BMDATA['gen']['approx'][65536] = _GEN_APPROX_POLISH
BMDATA['gen']['approx'][131072] = _GEN_APPROX_RUSSIAN
BMDATA['gen']['approx'][262144] = _GEN_APPROX_FRENCH + _GEN_APPROX_SPANISH
BMDATA['gen']['approx'][524288] = _GEN_APPROX_FRENCH
BMDATA['gen']['exact'][1] = _GEN_EXACT_ANY
BMDATA['gen']['exact'][2] = _GEN_EXACT_ARABIC
BMDATA['gen']['exact']['common'] = _GEN_EXACT_APPROX_COMMON + _GEN_EXACT_COMMON
BMDATA['gen']['exact'][4] = _GEN_EXACT_RUSSIAN
BMDATA['gen']['exact'][8] = _GEN_EXACT_RUSSIAN
BMDATA['gen']['exact'][16] = _GEN_EXACT_DUTCH
BMDATA['gen']['exact'][32] = _GEN_EXACT_RUSSIAN
BMDATA['gen']['exact'][64] = _GEN_EXACT_FRENCH
BMDATA['gen']['exact'][128] = _GEN_EXACT_ANY
BMDATA['gen']['exact'][256] = _GEN_EXACT_GREEK
BMDATA['gen']['exact'][512] = _GEN_EXACT_GREEKLATIN
BMDATA['gen']['exact'][1024] = _GEN_EXACT_HEBREW
BMDATA['gen']['exact'][2048] = _GEN_EXACT_RUSSIAN
BMDATA['gen']['exact'][4096] = _GEN_EXACT_ITALIAN
BMDATA['gen']['exact'][8192] = _GEN_EXACT_LATVIAN
BMDATA['gen']['exact'][16384] = _GEN_EXACT_POLISH
BMDATA['gen']['exact'][32768] = _GEN_EXACT_PORTUGUESE
BMDATA['gen']['exact'][65536] = _GEN_EXACT_RUSSIAN
BMDATA['gen']['exact'][131072] = _GEN_EXACT_RUSSIAN
BMDATA['gen']['exact'][262144] = _GEN_EXACT_SPANISH
BMDATA['gen']['exact'][524288] = _GEN_EXACT_TURKISH
BMDATA['gen']['hebrew']['common'] = (
    _GEN_EXACT_APPROX_COMMON + _GEN_HEBREW_COMMON
)  # noqa: E501
BMDATA['gen']['rules'][1] = _GEN_RULES_ANY
BMDATA['gen']['rules'][2] = _GEN_RULES_ARABIC
BMDATA['gen']['rules'][4] = _GEN_RULES_CYRILLIC
BMDATA['gen']['rules'][8] = _GEN_RULES_CZECH
BMDATA['gen']['rules'][16] = _GEN_RULES_DUTCH
BMDATA['gen']['rules'][32] = _GEN_RULES_ENGLISH
BMDATA['gen']['rules'][64] = _GEN_RULES_FRENCH
BMDATA['gen']['rules'][128] = _GEN_RULES_GERMAN
BMDATA['gen']['rules'][256] = _GEN_RULES_GREEK
BMDATA['gen']['rules'][512] = _GEN_RULES_GREEKLATIN
BMDATA['gen']['rules'][1024] = _GEN_RULES_HEBREW
BMDATA['gen']['rules'][2048] = _GEN_RULES_HUNGARIAN
BMDATA['gen']['rules'][4096] = _GEN_RULES_ITALIAN
BMDATA['gen']['rules'][8192] = _GEN_RULES_LATVIAN
BMDATA['gen']['rules'][16384] = _GEN_RULES_POLISH
BMDATA['gen']['rules'][32768] = _GEN_RULES_PORTUGUESE
BMDATA['gen']['rules'][65536] = _GEN_RULES_ROMANIAN
BMDATA['gen']['rules'][131072] = _GEN_RULES_RUSSIAN
BMDATA['gen']['rules'][262144] = _GEN_RULES_SPANISH
BMDATA['gen']['rules'][524288] = _GEN_RULES_TURKISH

BMDATA['sep'] = {}
BMDATA['sep']['approx'] = {}
BMDATA['sep']['exact'] = {}
BMDATA['sep']['rules'] = {}
BMDATA['sep']['hebrew'] = {}

BMDATA['sep']['language_rules'] = _SEP_LANGUAGE_RULES
BMDATA['sep']['languages'] = _SEP_LANGUAGES
BMDATA['sep']['approx'][1] = _SEP_APPROX_ANY
BMDATA['sep']['approx']['common'] = (
    _SEP_EXACT_APPROX_COMMON + _SEP_APPROX_COMMON
)  # noqa: E501
BMDATA['sep']['approx'][64] = _SEP_APPROX_FRENCH
BMDATA['sep']['approx'][1024] = _SEP_APPROX_HEBREW
BMDATA['sep']['approx'][4096] = _SEP_APPROX_FRENCH
BMDATA['sep']['approx'][32768] = _SEP_APPROX_FRENCH
BMDATA['sep']['approx'][262144] = _SEP_APPROX_FRENCH
BMDATA['sep']['exact'][1] = _SEP_EXACT_ANY
BMDATA['sep']['exact']['common'] = _SEP_EXACT_APPROX_COMMON + _SEP_EXACT_COMMON
BMDATA['sep']['exact'][64] = _SEP_EXACT_FRENCH
BMDATA['sep']['exact'][1024] = _SEP_EXACT_HEBREW
BMDATA['sep']['exact'][4096] = _SEP_EXACT_ITALIAN
BMDATA['sep']['exact'][32768] = _SEP_EXACT_PORTUGUESE
BMDATA['sep']['exact'][262144] = _SEP_EXACT_SPANISH
BMDATA['sep']['hebrew']['common'] = (
    _SEP_EXACT_APPROX_COMMON + _SEP_HEBREW_COMMON
)  # noqa: E501
BMDATA['sep']['rules'][1] = _SEP_RULES_ANY
BMDATA['sep']['rules'][64] = _SEP_RULES_FRENCH
BMDATA['sep']['rules'][1024] = _SEP_RULES_HEBREW
BMDATA['sep']['rules'][4096] = _SEP_RULES_ITALIAN
BMDATA['sep']['rules'][32768] = _SEP_RULES_PORTUGUESE
BMDATA['sep']['rules'][262144] = _SEP_RULES_SPANISH

BMDATA['ash'] = {}
BMDATA['ash']['approx'] = {}
BMDATA['ash']['exact'] = {}
BMDATA['ash']['rules'] = {}
BMDATA['ash']['hebrew'] = {}

BMDATA['ash']['language_rules'] = _ASH_LANGUAGE_RULES
BMDATA['ash']['languages'] = _ASH_LANGUAGES
BMDATA['ash']['approx'][1] = _ASH_APPROX_ANY
BMDATA['ash']['approx']['common'] = (
    _ASH_EXACT_APPROX_COMMON + _ASH_APPROX_COMMON
)  # noqa: E501
BMDATA['ash']['approx'][4] = _ASH_APPROX_RUSSIAN
BMDATA['ash']['approx'][32] = _ASH_APPROX_ENGLISH
BMDATA['ash']['approx'][64] = _ASH_APPROX_FRENCH
BMDATA['ash']['approx'][128] = _ASH_APPROX_GERMAN
BMDATA['ash']['approx'][1024] = _ASH_APPROX_HEBREW
BMDATA['ash']['approx'][2048] = _ASH_APPROX_FRENCH
BMDATA['ash']['approx'][16384] = _ASH_APPROX_POLISH
BMDATA['ash']['approx'][65536] = _ASH_APPROX_POLISH
BMDATA['ash']['approx'][131072] = _ASH_APPROX_RUSSIAN
BMDATA['ash']['approx'][262144] = _ASH_APPROX_FRENCH
BMDATA['ash']['exact'][1] = _ASH_EXACT_ANY
BMDATA['ash']['exact']['common'] = _ASH_EXACT_APPROX_COMMON + _ASH_EXACT_COMMON
BMDATA['ash']['exact'][4] = _ASH_EXACT_RUSSIAN
BMDATA['ash']['exact'][32] = _ASH_EXACT_RUSSIAN
BMDATA['ash']['exact'][64] = _ASH_EXACT_RUSSIAN
BMDATA['ash']['exact'][128] = _ASH_EXACT_ANY
BMDATA['ash']['exact'][1024] = _ASH_EXACT_HEBREW
BMDATA['ash']['exact'][2048] = _ASH_EXACT_RUSSIAN
BMDATA['ash']['exact'][16384] = _ASH_EXACT_POLISH
BMDATA['ash']['exact'][65536] = _ASH_EXACT_RUSSIAN
BMDATA['ash']['exact'][131072] = _ASH_EXACT_RUSSIAN
BMDATA['ash']['exact'][262144] = _ASH_EXACT_RUSSIAN
BMDATA['ash']['hebrew']['common'] = (
    _ASH_EXACT_APPROX_COMMON + _ASH_HEBREW_COMMON
)  # noqa: E501
BMDATA['ash']['rules'][1] = _ASH_RULES_ANY
BMDATA['ash']['rules'][4] = _ASH_RULES_CYRILLIC
BMDATA['ash']['rules'][32] = _ASH_RULES_ENGLISH
BMDATA['ash']['rules'][64] = _ASH_RULES_FRENCH
BMDATA['ash']['rules'][128] = _ASH_RULES_GERMAN
BMDATA['ash']['rules'][1024] = _ASH_RULES_HEBREW
BMDATA['ash']['rules'][2048] = _ASH_RULES_HUNGARIAN
BMDATA['ash']['rules'][16384] = _ASH_RULES_POLISH
BMDATA['ash']['rules'][65536] = _ASH_RULES_ROMANIAN
BMDATA['ash']['rules'][131072] = _ASH_RULES_RUSSIAN
BMDATA['ash']['rules'][262144] = _ASH_RULES_SPANISH


if __name__ == '__main__':
    import doctest

    doctest.testmod()
