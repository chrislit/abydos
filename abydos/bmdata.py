# -*- coding: utf-8 -*-
"""abydos.distance

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

This file is derived from PHP code by Alexander Beider and Stephen P. Morse that
is part of the Beider-Morse Phonetic Matching (BMPM) System, available at
http://stevemorse.org/phonetics/bmpm.htm.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

l_any = 2<<0
l_arabic = 2<<1
l_cyrillic = 2<<2
l_czech = 2<<3
l_dutch = 2<<4
l_english = 2<<5
l_french = 2<<6
l_german = 2<<7
l_greek = 2<<8
l_greeklatin = 2<<9
l_hebrew = 2<<10
l_hungarian = 2<<11
l_italian = 2<<12
l_polish = 2<<13
l_portuguese = 2<<14
l_romanian = 2<<15
l_russian = 2<<16
l_spanish = 2<<17
l_turkish = 2<<18

# gen/approxany.php

# GENERIC
# A, E, I, O, P, U should create variants, but a, e, i, o, u should not create any new variant
# Q = ü ; Y = ä = ö
# EE = final "e" (english or french)

_gen_approx_any = (
     # VOWELS
     # "ALL" DIPHTHONGS are interchangeable BETWEEN THEM and with monophthongs of which they are composed ("D" means "diphthong")
     #  {a,o} are totally interchangeable if non-stressed; in German "a/o" can actually be from "ä/ö" (that are equivalent to "e")
     #  {i,e} are interchangeable if non-stressed, while in German "u" can actually be from "ü" (that is equivalent to "i")

     ("mb","","","(mb|b[l_greeklatin])"),
     ("mp","","","(mp|b[l_greeklatin])"),
     ("ng","","","(ng|g[l_greeklatin])"),

     ("B","","[fktSs]","(p|f[l_spanish])"),
     ("B","","p",""),
     ("B","","$","(p|f[l_spanish])"),
     ("V","","[pktSs]","(f|p[l_spanish])"),
     ("V","","f",""),
     ("V","","$","(f|p[l_spanish])"),

     ("B","","","(b|v[l_spanish])"),
     ("V","","","(v|b[l_spanish])"),

     # French word-final and word-part-final letters
     ("t","","$","(t|[l_french])"),
     ("g","n","$","(g|[l_french])"),
     ("k","n","$","(k|[l_french])"),
     ("p","","$","(p|[l_french])"),
     ("r","[Ee]","$","(r|[l_french])"),
     ("s","","$","(s|[l_french])"),
     ("t","[aeiouAEIOU]","[^aeiouAEIOU]","(t|[l_french])"), # Petitjean
     ("s","[aeiouAEIOU]","[^aeiouAEIOU]","(s|[l_french])"), # Groslot, Grosleau
     #("p","[aeiouAEIOU]","[^aeiouAEIOU]","(p|[l_french])"),

     ("I", "[aeiouAEIBFOUQY]", "", "i"),
     ("I","","[^aeiouAEBFIOU]e","(Q[l_german]|i|D[l_english])"),  # "line"
     ("I", "", "$", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk[l_german])"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts[l_german])"),
     ("Its", "", "$", "its"),
     ("I", "", "", "(Q[l_german]|i)"),

     ("lEE","[bdfgkmnprsStvzZ]","","(li|il[l_english])"),  # Apple = Appel
     ("rEE","[bdfgkmnprsStvzZ]","","(ri|ir[l_english])"),
     ("lE","[bdfgkmnprsStvzZ]","","(li|il[l_english]|lY[l_german])"),  # Applebaum < Appelbaum
     ("rE","[bdfgkmnprsStvzZ]","","(ri|ir[l_english]|rY[l_german])"),

     ("EE","","","(i|)"),

     ("ea","","","(D|a|i)"),

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("eu","","","(D|e|u)"),

     ("ai","","","(D|a|i)"),
     ("Ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("Oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),
     ("Ui","","","(D|u|i)"),
     ("ei","","","(D|i)"),
     ("Ei","","","(D|i)"),

     ("iA","","$","(ia|io)"),
     ("iA","","","(ia|io|iY[l_german])"),
     ("A","","[^aeiouAEBFIOU]e","(a|o|Y[l_german]|D[l_english])"), # "plane"

     ("E","i[^aeiouAEIOU]","","(i|Y[l_german]|[l_english])"), # Wineberg (vineberg/vajneberg) --> vajnberg
     ("E","a[^aeiouAEIOU]","","(i|Y[l_german]|[l_english])"), #  Shaneberg (shaneberg/shejneberg) --> shejnberg

     ("E", "", "[fklmnprst]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "", "$", "i"),
     ("E", "[DaoiuAOIUQY]", "", "i"),
     ("E", "", "[aoAOQY]", "i"),
     ("E", "", "", "(i|Y[l_german])"),

     ("P", "", "", "(o|u)"),

     ("O", "", "[fklmnprstv]$", "o"),
     ("O", "", "ts$", "o"),
     ("O", "", "$", "o"),
     ("O", "[oeiuQY]", "", "o"),
     ("O", "", "", "(o|Y[l_german])"),
     ("O", "", "", "o"),

     ("A", "", "[fklmnprst]$", "(a|o)"),
     ("A", "", "ts$", "(a|o)"),
     ("A", "", "$", "(a|o)"),
     ("A", "[oeiuQY]", "", "(a|o)"),
     ("A", "", "", "(a|o|Y[l_german])"),
     ("A", "", "", "(a|o)"),

     ("U", "", "$", "u"),
     ("U", "[DoiuQY]", "", "u"),
     ("U", "", "[^k]$", "u"),
     ("Uk", "[lr]", "$", "(uk|Qk[l_german])"),
     ("Uk", "", "$", "uk"),
     ("sUts", "", "$", "(suts|sQts[l_german])"),
     ("Uts", "", "$", "uts"),
     ("U", "", "", "(u|Q[l_german])"),
     ("U", "", "", "u"),

     ("e", "", "[fklmnprstv]$", "i"),
     ("e", "", "ts$", "i"),
     ("e", "", "$", "i"),
     ("e", "[DaoiuAOIUQY]", "", "i"),
     ("e", "", "[aoAOQY]", "i"),
     ("e", "", "", "(i|Y[l_german])"),

     ("a", "", "", "(a|o)"),

     )

# gen/approxarabic.php
_gen_approx_arabic = (

     ("1a", "", "", "(D|a)"),
     ("1i", "", "", "(D|i|e)"),
     ("1u", "", "", "(D|u|o)"),
     ("j1", "", "", "(ja|je|jo|ju|j)"),
     ("1", "", "", "(a|e|i|o|u|)"),
     ("u", "", "", "(o|u)"),
     ("i", "", "", "(i|e)"),
     ("p", "", "$", "p"),
     ("p", "", "", "(p|b)"),

     )

# gen/approxcommon.php

# GENERIC

_gen_approx_common = (

     # DUTCH
     ("van", "^", "[bp]", "(vam|)"),
     ("van", "^", "", "(van|)"),

     # REGRESSIVE ASSIMILATION OF CONSONANTS
     ("n","","[bp]","m"),

     # PECULIARITY OF "h"
     ("h","","",""),
     ("H","","","(x|)"),

     # "e" and "i" ARE TO BE OMITTED BEFORE (SYLLABIC) n & l: Halperin=Halpern; Frankel = Frankl, Finkelstein = Finklstein
     # but Andersen & Anderson should match
     ("sen", "[rmnl]", "$", "(zn|zon)"),
     ("sen", "", "$", "(sn|son)"),
     ("sEn", "[rmnl]", "$", "(zn|zon)"),
     ("sEn", "", "$", "(sn|son)"),

     ("e", "[BbdfgklmnprsStvzZ]", "[ln]$", ""),
     ("i", "[BbdfgklmnprsStvzZ]", "[ln]$", ""),
     ("E", "[BbdfgklmnprsStvzZ]", "[ln]$", ""),
     ("I", "[BbdfgklmnprsStvzZ]", "[ln]$", ""),
     ("Q", "[BbdfgklmnprsStvzZ]", "[ln]$", ""),
     ("Y", "[BbdfgklmnprsStvzZ]", "[ln]$", ""),

     ("e", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
     ("i", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
     ("E", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
     ("I", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
     ("Q", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),
     ("Y", "[BbdfgklmnprsStvzZ]", "[ln][BbdfgklmnprsStvzZ]", ""),

     ("lEs","","","(lEs|lz)"),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)
     ("lE","[bdfgkmnprStvzZ]","","(lE|l)"),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)

     # SIMPLIFICATION: (TRIPHTHONGS & DIPHTHONGS) -> ONE GENERIC DIPHTHONG "D"
     ("aue","","","D"),
     ("oue","","","D"),

     ("AvE","","","(D|AvE)"),
     ("Ave","","","(D|Ave)"),
     ("avE","","","(D|avE)"),
     ("ave","","","(D|ave)"),

     ("OvE","","","(D|OvE)"),
     ("Ove","","","(D|Ove)"),
     ("ovE","","","(D|ovE)"),
     ("ove","","","(D|ove)"),

     ("ea","","","(D|ea)"),
     ("EA","","","(D|EA)"),
     ("Ea","","","(D|Ea)"),
     ("eA","","","(D|eA)"),

     ("aji","","","D"),
     ("ajI","","","D"),
     ("aje","","","D"),
     ("ajE","","","D"),

     ("Aji","","","D"),
     ("AjI","","","D"),
     ("Aje","","","D"),
     ("AjE","","","D"),

     ("oji","","","D"),
     ("ojI","","","D"),
     ("oje","","","D"),
     ("ojE","","","D"),

     ("Oji","","","D"),
     ("OjI","","","D"),
     ("Oje","","","D"),
     ("OjE","","","D"),

     ("eji","","","D"),
     ("ejI","","","D"),
     ("eje","","","D"),
     ("ejE","","","D"),

     ("Eji","","","D"),
     ("EjI","","","D"),
     ("Eje","","","D"),
     ("EjE","","","D"),

     ("uji","","","D"),
     ("ujI","","","D"),
     ("uje","","","D"),
     ("ujE","","","D"),

     ("Uji","","","D"),
     ("UjI","","","D"),
     ("Uje","","","D"),
     ("UjE","","","D"),

     ("iji","","","D"),
     ("ijI","","","D"),
     ("ije","","","D"),
     ("ijE","","","D"),

     ("Iji","","","D"),
     ("IjI","","","D"),
     ("Ije","","","D"),
     ("IjE","","","D"),

     ("aja","","","D"),
     ("ajA","","","D"),
     ("ajo","","","D"),
     ("ajO","","","D"),
     ("aju","","","D"),
     ("ajU","","","D"),

     ("Aja","","","D"),
     ("AjA","","","D"),
     ("Ajo","","","D"),
     ("AjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("oja","","","D"),
     ("ojA","","","D"),
     ("ojo","","","D"),
     ("ojO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("Oja","","","D"),
     ("OjA","","","D"),
     ("Ojo","","","D"),
     ("OjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("eja","","","D"),
     ("ejA","","","D"),
     ("ejo","","","D"),
     ("ejO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("Eja","","","D"),
     ("EjA","","","D"),
     ("Ejo","","","D"),
     ("EjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("uja","","","D"),
     ("ujA","","","D"),
     ("ujo","","","D"),
     ("ujO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("Uja","","","D"),
     ("UjA","","","D"),
     ("Ujo","","","D"),
     ("UjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("ija","","","D"),
     ("ijA","","","D"),
     ("ijo","","","D"),
     ("ijO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("Ija","","","D"),
     ("IjA","","","D"),
     ("Ijo","","","D"),
     ("IjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("j","","","i"),

     # lander = lender = l채nder
     ("lYndEr","","$","lYnder"),
     ("lander","","$","lYnder"),
     ("lAndEr","","$","lYnder"),
     ("lAnder","","$","lYnder"),
     ("landEr","","$","lYnder"),
     ("lender","","$","lYnder"),
     ("lEndEr","","$","lYnder"),
     ("lendEr","","$","lYnder"),
     ("lEnder","","$","lYnder"),

     # CONSONANTS {z & Z; s & S} are approximately interchangeable
     ("s", "", "[rmnl]", "z"),
     ("S", "", "[rmnl]", "z"),
     ("s", "[rmnl]", "", "z"),
     ("S", "[rmnl]", "", "z"),

     ("dS", "", "$", "S"),
     ("dZ", "", "$", "S"),
     ("Z", "", "$", "S"),
     ("S", "", "$", "(S|s)"),
     ("z", "", "$", "(S|s)"),

     ("S", "", "", "s"),
     ("dZ", "", "", "z"),
     ("Z", "", "", "z"),

     )

# gen/approxcyrillic.php
# this file uses the same rules as approxrussian.php

# gen/approxczech.php

# this file uses the same rules as approxfrench.php

# gen/approxdutch.php
# this file uses the same rules as approxfrench.php

# gen/approxenglish.php
_gen_approx_english = (

     # VOWELS
     ("I","","[^aEIeiou]e","(Q|i|D)"), # like in "five"
     ("I", "", "$", "i"),
     ("I", "[aEIeiou]", "", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "", "", "(i|Q)"),

     ("lE","[bdfgkmnprsStvzZ]","","(il|li|lY)"),  # Applebaum < Appelbaum

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),

     ("E","D[^aeiEIou]","","(i|)"), # Weinberg, Shaneberg (shaneberg/shejneberg) --> shejnberg
     ("e","D[^aeiEIou]","","(i|)"),

     ("e", "", "", "i"),
     ("E", "", "[fklmnprsStv]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "[DaoiEuQY]", "", "i"),
     ("E", "", "[aoQY]", "i"),
     ("E", "", "", "(Y|i)"),

     ("a", "", "", "(a|o)"),

     )

# gen/approxfrench.php
#GENERAL
_gen_approx_french = (
     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),

     ("a", "", "", "(a|o)"),
     ("e", "", "", "i"),

     )

# gen/approxgerman.php

_gen_approx_german = (

     ("I", "", "$", "i"),
     ("I", "[aeiAEIOUouQY]", "", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "", "", "(Q|i)"),

     ("AU","","","(D|a|u)"),
     ("aU","","","(D|a|u)"),
     ("Au","","","(D|a|u)"),
     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("OU","","","(D|o|u)"),
     ("oU","","","(D|o|u)"),
     ("Ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("Ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("Oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),
     ("Ui","","","(D|u|i)"),

     ("e", "", "", "i"),

     ("E", "", "[fklmnprst]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "", "$", "i"),
     ("E", "[DaoAOUiuQY]", "", "i"),
     ("E", "", "[aoAOQY]", "i"),
     ("E", "", "", "(Y|i)"),

     ("O", "", "$", "o"),
     ("O", "", "[fklmnprst]$", "o"),
     ("O", "", "ts$", "o"),
     ("O", "[aoAOUeiuQY]", "", "o"),
     ("O", "", "", "(o|Y)"),

     ("a", "", "", "(a|o)"),

     ("A", "", "$", "(a|o)"),
     ("A", "", "[fklmnprst]$", "(a|o)"),
     ("A", "", "ts$", "(a|o)"),
     ("A", "[aoeOUiuQY]", "", "(a|o)"),
     ("A", "", "", "(a|o|Y)"),

     ("U", "", "$", "u"),
     ("U", "[DaoiuUQY]", "", "u"),
     ("U", "", "[^k]$", "u"),
     ("Uk", "[lr]", "$", "(uk|Qk)"),
     ("Uk", "", "$", "uk"),
     ("sUts", "", "$", "(suts|sQts)"),
     ("Uts", "", "$", "uts"),
     ("U", "", "", "(u|Q)"),

     )

# gen/approxgreek.php

# this file uses the same rules as approxfrench.php

# gen/approxgreeklatin.php
_gen_approx_greeklatin = (
     ("N","","",""),

     )

# gen/approxhebrew.php
_gen_approx_hebrew = (
     )

# gen/approxhungarian.php

# this file uses the same rules as approxfrench.php

# gen/approxitalian.php
# this file uses the same rules as approxfrench.php

# gen/approxpolish.php
_gen_approx_polish = (

     ("aiB","","[bp]","(D|Dm)"),
     ("oiB","","[bp]","(D|Dm)"),
     ("uiB","","[bp]","(D|Dm)"),
     ("eiB","","[bp]","(D|Dm)"),
     ("EiB","","[bp]","(D|Dm)"),
     ("iiB","","[bp]","(D|Dm)"),
     ("IiB","","[bp]","(D|Dm)"),

     ("aiB","","[dgkstvz]","(D|Dn)"),
     ("oiB","","[dgkstvz]","(D|Dn)"),
     ("uiB","","[dgkstvz]","(D|Dn)"),
     ("eiB","","[dgkstvz]","(D|Dn)"),
     ("EiB","","[dgkstvz]","(D|Dn)"),
     ("iiB","","[dgkstvz]","(D|Dn)"),
     ("IiB","","[dgkstvz]","(D|Dn)"),

     ("B","","[bp]","(o|om|im)"),
     ("B","","[dgkstvz]","(o|on|in)"),
     ("B", "", "", "o"),

     ("aiF","","[bp]","(D|Dm)"),
     ("oiF","","[bp]","(D|Dm)"),
     ("uiF","","[bp]","(D|Dm)"),
     ("eiF","","[bp]","(D|Dm)"),
     ("EiF","","[bp]","(D|Dm)"),
     ("iiF","","[bp]","(D|Dm)"),
     ("IiF","","[bp]","(D|Dm)"),

     ("aiF","","[dgkstvz]","(D|Dn)"),
     ("oiF","","[dgkstvz]","(D|Dn)"),
     ("uiF","","[dgkstvz]","(D|Dn)"),
     ("eiF","","[dgkstvz]","(D|Dn)"),
     ("EiF","","[dgkstvz]","(D|Dn)"),
     ("iiF","","[dgkstvz]","(D|Dn)"),
     ("IiF","","[dgkstvz]","(D|Dn)"),

     ("F","","[bp]","(i|im|om)"),
     ("F","","[dgkstvz]","(i|in|on)"),
     ("F", "", "", "i"),

     ("P", "", "", "(o|u)"),

     ("I", "", "$", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "[aeiAEBFIou]", "", "i"),
     ("I", "", "", "(i|Q)"),

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),

     ("a", "", "", "(a|o)"),
     ("e", "", "", "i"),

     ("E", "", "[fklmnprst]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "", "$", "i"),
     ("E", "[DaoiuQ]", "", "i"),
     ("E", "", "[aoQ]", "i"),
     ("E", "", "", "(Y|i)"),

     )

# gen/approxportuguese.php

# this file uses the same rules as approxfrench.php

# gen/approxromanian.php
# this file uses the same rules as approxpolish.php

# gen/approxrussian.php

_gen_approx_russian = (

     # VOWELS
     ("I", "", "$", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "[aeiEIou]", "", "i"),
     ("I", "", "", "(i|Q)"),

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),

     ("om","","[bp]","(om|im)"),
     ("on","","[dgkstvz]","(on|in)"),
     ("em","","[bp]","(im|om)"),
     ("en","","[dgkstvz]","(in|on)"),
     ("Em","","[bp]","(im|Ym|om)"),
     ("En","","[dgkstvz]","(in|Yn|on)"),

     ("a", "", "", "(a|o)"),
     ("e", "", "", "i"),

     ("E", "", "[fklmnprsStv]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "[DaoiuQ]", "", "i"),
     ("E", "", "[aoQ]", "i"),
     ("E", "", "", "(Y|i)"),

     )

# gen/approxspanish.php

_gen_approx_spanish = (
     ("B","","","(b|v)"),
     ("V","","","(b|v)"),

     )

# gen/approxturkish.php
# this file uses the same rules as approxfrench.php

# gen/exactany.php
# GENERAL
# A, E, I, O, P, U should create variants,
# EE = final "e" (english & french)
# V, B from Spanish
# but a, e, i, o, u should not create any new variant
_gen_exact_any = (
     ("EE", "", "$", "e"),

     ("A", "", "", "a"),
     ("E", "", "", "e"),
     ("I", "", "", "i"),
     ("O", "", "", "o"),
     ("P", "", "", "o"),
     ("U", "", "", "u"),

     ("B","","[fktSs]","p"),
     ("B","","p",""),
     ("B","","$","p"),
     ("V","","[pktSs]","f"),
     ("V","","f",""),
     ("V","","$","f"),

     ("B", "", "", "b"),
     ("V", "", "", "v"),

     )

# gen/exactapproxcommon.php
# GENERAL
_gen_exact_approx_common = (
     ("h","","$",""),

     # VOICED - UNVOICED CONSONANTS
     ("b","","[fktSs]","p"),
     ("b","","p",""),
     ("b","","$","p"),
     ("p","","[vgdZz]","b"), # Ashk: "v" excluded (everythere)
     ("p","","b",""),

     ("v","","[pktSs]","f"),
     ("v","","f",""),
     ("v","","$","f"),
     ("f","","[vbgdZz]","v"),
     ("f","","v",""),

     ("g","","[pftSs]","k"),
     ("g","","k",""),
     ("g","","$","k"),
     ("k","","[vbdZz]","g"),
     ("k","","g",""),

     ("d","","[pfkSs]","t"),
     ("d","","t",""),
     ("d","","$","t"),
     ("t","","[vbgZz]","d"),
     ("t","","d",""),

     ("s","","dZ",""),
     ("s","","tS",""),

     ("z","","[pfkSt]","s"),
     ("z","","[sSzZ]",""),
     ("s","","[sSzZ]",""),
     ("Z","","[sSzZ]",""),
     ("S","","[sSzZ]",""),

     # SIMPLIFICATION OF CONSONANT CLUSTERS
     ("jnm","","","jm"),

     # DOUBLE --> SINGLE
     ("ji","^","","i"),
     ("jI","^","","I"),

     ("a","","[aA]",""),
     ("a","A","",""),
     ("A","","A",""),

     ("b","","b",""),
     ("d","","d",""),
     ("f","","f",""),
     ("g","","g",""),
     ("j","","j",""),
     ("k","","k",""),
     ("l","","l",""),
     ("m","","m",""),
     ("n","","n",""),
     ("p","","p",""),
     ("r","","r",""),
     ("t","","t",""),
     ("v","","v",""),
     ("z","","z","")
     # do not put name of file here since it always gets merged into another file
     )

# gen/exactarabic.php
_gen_exact_arabic = (

     ("1", "", "", ""),

     )

# gen/exactcommon.php
# GENERAL

_gen_exact_common = (
     ("H","","",""),

     # VOICED - UNVOICED CONSONANTS
     ("s","[^t]","[bgZd]","z"),
     ("Z","","[pfkst]","S"),
     ("Z","","$","S"),
     ("S","","[bgzd]","Z"),
     ("z","","$","s"),

     ("ji","[aAoOeEiIuU]","","j"),
     ("jI","[aAoOeEiIuU]","","j"),
     ("je","[aAoOeEiIuU]","","j"),
     ("jE","[aAoOeEiIuU]","","j"),

     )

# gen/exactcyrillic.php
# this file uses the same rules as exactrussian.php

# gen/exactczech.php
# this file uses the same rules as exactrussian.php

# gen/exactdutch.php
_gen_exact_dutch = (

     )

# gen/exactenglish.php
# this file uses the same rules as exactrussian.php

# gen/exactfrench.php
# GENERAL
_gen_exact_french = (

     )

# gen/exactgerman.php
# this file uses the same rules as exactany.php

# gen/exactgreek.php
_gen_exact_greek = (

     )

# gen/exactgreeklatin.php
_gen_exact_greeklatin = (

     ("N","","","n"),

     )

# gen/exacthebrew.php
_gen_exact_hebrew = (
     )

# gen/exacthungarian.php
# this file uses the same rules as exactrussian.php

# gen/exactitalian.php
# GENERAL
_gen_exact_italian = (

     )

# gen/exactpolish.php
_gen_exact_polish = (

     ("B", "", "", "a"),
     ("F", "", "", "e"),
     ("P", "", "", "o"),

     ("E", "", "", "e"),
     ("I", "", "", "i"),

     )

# gen/exactportuguese.php
# GENERAL
_gen_exact_portuguese = (

     )

# gen/exactromanian.php
# this file uses the same rules as exactrussian.php

# gen/exactrussian.php
_gen_exact_russian = (

     ("E", "", "", "e"),
     ("I", "", "", "i"),

     )

# gen/exactspanish.php
# GENERAL
_gen_exact_spanish = (

     ("B", "", "", "b"),
     ("V", "", "", "v"),

     )

# gen/exactturkish.php
_gen_exact_turkish = (

     )

# gen/hebrewcommon.php
#GENERAL

_gen_hebrew_common = (
     ("ts","","","C"), # for not confusion Gutes [=guts] and Guts [=guc]
     ("tS","","","C"), # same reason
     ("S","","","s"),
     ("p","","","f"),
     ("b","^","","b"),
     ("b","","","(b|v)"),
     ("B","","","(b|v)"),    # Spanish "b"
     ("V","","","v"),    # Spanish "v"
     ("EE","","","(1|)"), # final "e" (english & french)

     ("ja","","","i"),
     ("jA","","","i"),
     ("je","","","i"),
     ("jE","","","i"),
     ("aj","","","i"),
     ("Aj","","","i"),
     ("I","","","i"),
     ("j","","","i"),

     ("a","^","","1"),
     ("A","^","","1"),
     ("e","^","","1"),
     ("E","^","","1"),
     ("Y","^","","1"),

     ("a","","$","1"),
     ("A","","$","1"),
     ("e","","$","1"),
     ("E","","$","1"),
     ("Y","","$","1"),

     ("a","","",""),
     ("A","","",""),
     ("e","","",""),
     ("E","","",""),
     ("Y","","",""),

     ("oj","^","","(u|vi)"),
     ("Oj","^","","(u|vi)"),
     ("uj","^","","(u|vi)"),
     ("Uj","^","","(u|vi)"),

     ("oj","","","u"),
     ("Oj","","","u"),
     ("uj","","","u"),
     ("Uj","","","u"),

     ("ou","^","","(u|v|1)"),
     ("o","^","","(u|v|1)"),
     ("O","^","","(u|v|1)"),
     ("P","^","","(u|v|1)"),
     ("U","^","","(u|v|1)"),
     ("u","^","","(u|v|1)"),

     ("o","","$","(u|1)"),
     ("O","","$","(u|1)"),
     ("P","","$","(u|1)"),
     ("u","","$","(u|1)"),
     ("U","","$","(u|1)"),

     ("ou","","","u"),
     ("o","","","u"),
     ("O","","","u"),
     ("P","","","u"),
     ("U","","","u"),

     ("VV","","","u"), # alef/ayin + vov from ruleshebrew
     ("V","","","v"), # tsvey-vov from ruleshebrew;; only Ashkenazic
     ("L","^","","1"), # alef/ayin from  ruleshebrew
     ("L","","$","1"), # alef/ayin from  ruleshebrew
     ("L","","",""), # alef/ayin from  ruleshebrew
     ("WW","^","","(vi|u)"), # vav-yod from  ruleshebrew
     ("WW","","","u"), # vav-yod from  ruleshebrew
     ("W","^","","(u|v)"), # vav from  ruleshebrew
     ("W","","","u"), # vav from  ruleshebrew

     # ("g","","","(g|Z)"),
     # ("z","","","(z|Z)"),
     # ("d","","","(d|dZ)"),

     ("TB","^","","t"), # tav from ruleshebrew
     ("TB","","","(t|s)"), # tav from ruleshebrew; s is only Ashkenazic
     ("T","","","t"),   # tet from  ruleshebrew

     # ("k","","","(k|x)"),
     # ("x","","","(k|x)"),
     ("K","","","k"), # kof and initial kaf from ruleshebrew
     ("X","","","x"), # khet and final kaf from ruleshebrew

     ("H","^","","(x|1)"),
     ("H","","$","(x|1)"),
     ("H","","","(x|)"),
     ("h","^","","1"),
     ("h","","",""),

     )

# gen/lang.php
# GENERIC

# format of entries in $languageRules table is
#    (pattern, language, Acceptance)
# where
#    pattern is a regular expression
#      e.g., ^ means start of word, $ Means End Of Word, [^ei] means anything but e or i, etc.
#    language is one or more of the languages defined above separated by + signs
#    acceptance is true or false
# meaning is:
#    if "pattern" matches and acceptance is true, name is in one of the languages indicated and no others
#    if "pattern" matches and acceptance is false, name is not in any of the languages indicated

_gen_language_rules = (

     # 1. following are rules to accept the language
     # 1.1 Special letter combinations
     ('/^o’/', l_english, True),
     ("/^o'/", l_english, True),
     ('/^mc/', l_english, True),
     ('/^fitz/', l_english, True),
     ('/ceau/', l_french+l_romanian, True),
     ('/eau/', l_romanian, True),
     ('/ault$/', l_french, True),
     ('/oult$/', l_french, True),
     ('/eux$/', l_french, True),
     ('/eix$/', l_french, True),
     ('/glou$/', l_greeklatin, True),
     ('/uu/', l_dutch, True),
     ('/tx/', l_spanish, True),
     ('/witz/', l_german, True),
     ('/tz$/', l_german+l_russian+l_english, True),
     ('/^tz/', l_russian+l_english, True),
     ('/poulos$/', l_greeklatin, True),
     ('/pulos$/', l_greeklatin, True),
     ('/iou/', l_greeklatin, True),
     ('/sj$/', l_dutch, True),
     ('/^sj/', l_dutch, True),
     ('/güe/', l_spanish, True),
     ('/güi/', l_spanish, True),
     ('/ghe/', l_romanian + l_greeklatin, True),
     ('/ghi/', l_romanian + l_greeklatin, True),
     ('/escu$/', l_romanian, True),
     ('/esco$/', l_romanian, True),
     ('/vici$/', l_romanian, True),
     ('/schi$/', l_romanian, True),
     ('/ii$/', l_russian, True),
     ('/iy$/', l_russian, True),
     ('/yy$/', l_russian, True),
     ('/yi$/', l_russian, True),
     ('/^rz/', l_polish, True),
     ('/rz$/', l_polish+l_german, True),
     ("/[bcdfgklmnpstwz]rz/", l_polish, True),
     ('/rz[bcdfghklmnpstw]/', l_polish, True),
     ('/cki$/', l_polish, True),
     ('/ska$/', l_polish, True),
     ('/cka$/', l_polish, True),
     ('/ae/', l_german+l_russian+l_english, True),
     ('/oe/', l_german+l_french+l_russian+l_english+l_dutch, True),
     ('/th$/', l_german+l_english, True),
     ('/^th/', l_german+l_english+l_greeklatin, True),
     ('/mann/', l_german, True),
     ('/cz/', l_polish, True),
     ('/cy/', l_polish+l_greeklatin, True),
     ('/niew/', l_polish, True),
     ('/etti$/', l_italian, True),
     ('/eti$/', l_italian, True),
     ('/ati$/', l_italian, True),
     ('/ato$/', l_italian, True),
     ('/[aoei]no$/', l_italian, True),
     ('/[aoei]ni$/', l_italian, True),
     ('/esi$/', l_italian, True),
     ('/oli$/', l_italian, True),
     ('/field$/', l_english, True),
     ('/stein/', l_german, True),
     ('/heim$/', l_german, True),
     ('/heimer$/', l_german, True),
     ('/thal/', l_german, True),
     ('/zweig/', l_german, True),
     ("/[aeou]h/", l_german, True),
     ("/äh/", l_german, True),
     ("/öh/", l_german, True),
     ("/üh/", l_german, True),
     ("/[ln]h[ao]$/", l_portuguese, True),
     ("/[ln]h[aou]/", l_portuguese+l_french+l_german+l_dutch+l_czech+l_spanish+l_turkish, True),
     ('/chsch/', l_german, True),
     ('/tsch/', l_german, True),
     ('/sch$/', l_german+l_russian, True),
     ('/^sch/', l_german+l_russian, True),
     ('/ck$/', l_german + l_english, True),
     ('/c$/', l_polish + l_romanian + l_hungarian + l_czech + l_turkish, True),
     ('/sz/', l_polish + l_hungarian, True),
     ('/cs$/', l_hungarian, True),
     ('/^cs/', l_hungarian, True),
     ('/dzs/', l_hungarian, True),
     ('/zs$/', l_hungarian, True),
     ('/^zs/', l_hungarian, True),
     ("/^wl/", l_polish, True),
     ("/^wr/", l_polish+l_english+l_german+l_dutch, True),

     ("/gy$/", l_hungarian, True),
     ("/gy[aeou]/", l_hungarian, True),
     ("/gy/", l_hungarian + l_russian + l_french+l_greeklatin, True),
     ("/guy/", l_french, True),
     ('/gu[ei]/', l_spanish + l_french + l_portuguese, True),
     ('/gu[ao]/', l_spanish + l_portuguese, True),
     ('/gi[aou]/', l_italian + l_greeklatin, True),

     ("/ly/", l_hungarian + l_russian + l_polish + l_greeklatin, True),
     ("/ny/", l_hungarian + l_russian + l_polish + l_spanish + l_greeklatin, True),
     ("/ty/", l_hungarian + l_russian + l_polish + l_greeklatin, True),

     # 1.2 special characters
     ('/ć/', l_polish, True),
     ('/ç/', l_french + l_spanish + l_portuguese + l_turkish, True),
     ('/č/', l_czech, True),
     ('/ď/', l_czech, True),
     ('/ğ/', l_turkish, True),
     ('/ł/', l_polish, True),
     ('/ń/', l_polish, True),
     ('/ñ/', l_spanish, True),
     ('/ň/', l_czech, True),
     ('/ř/', l_czech, True),
     ('/ś/', l_polish, True),
     ('/ş/', l_romanian + l_turkish, True),
     ('/š/', l_czech, True),
     ('/ţ/', l_romanian, True),
     ('/ť/', l_czech, True),
     ('/ź/', l_polish, True),
     ('/ż/', l_polish, True),

     ('/ß/', l_german, True),

     ('/ä/', l_german, True),
     ('/á/', l_hungarian + l_spanish + l_portuguese + l_czech + l_greeklatin, True),
     ('/â/', l_romanian + l_french +l_portuguese, True),
     ('/ă/', l_romanian, True),
     ('/ą/', l_polish, True),
     ('/à/', l_portuguese, True),
     ('/ã/', l_portuguese, True),
     ('/ę/', l_polish, True),
     ('/é/', l_french + l_hungarian + l_czech + l_greeklatin, True),
     ('/è/', l_french + l_spanish + l_italian, True),
     ('/ê/', l_french, True),
     ('/ě/', l_czech, True),
     ('/ê/', l_french + l_portuguese, True),
     ('/í/', l_hungarian + l_spanish + l_portuguese + l_czech + l_greeklatin, True),
     ('/î/', l_romanian + l_french, True),
     ('/ı/', l_turkish, True),
     ('/ó/', l_polish + l_hungarian + l_spanish + l_italian + l_portuguese +l_czech + l_greeklatin, True),
     ('/ö/', l_german + l_hungarian + l_turkish, True),
     ('/ô/', l_french + l_portuguese, True),
     ('/õ/', l_portuguese + l_hungarian, True),
     ('/ò/', l_italian + l_spanish, True),
     ('/ű/', l_hungarian, True),
     ('/ú/', l_hungarian + l_spanish + l_portuguese + l_czech + l_greeklatin, True),
     ('/ü/', l_german + l_hungarian + l_spanish + l_portuguese + l_turkish, True),
     ('/ù/', l_french, True),
     ('/ů/', l_czech, True),
     ('/ý/', l_czech + l_greeklatin, True),

     # Every Cyrillic word has at least one Cyrillic vowel (аёеоиуыэюя)
     ("/а/", l_cyrillic, True),
     ("/ё/", l_cyrillic, True),
     ("/о/", l_cyrillic, True),
     ("/е/", l_cyrillic, True),
     ("/и/", l_cyrillic, True),
     ("/у/", l_cyrillic, True),
     ("/ы/", l_cyrillic, True),
     ("/э/", l_cyrillic, True),
     ("/ю/", l_cyrillic, True),
     ("/я/", l_cyrillic, True),

     # Every Greek word has at least one Greek vowel
     ("/α/", l_greek, True),
     ("/ε/", l_greek, True),
     ("/η/", l_greek, True),
     ("/ι/", l_greek, True),
     ("/ο/", l_greek, True),
     ("/υ/", l_greek, True),
     ("/ω/", l_greek, True),

     # Arabic (only initial)
     ("/ا/", l_arabic, True), # alif (isol + init)
     ("/ب/", l_arabic, True), # ba'
     ("/ت/", l_arabic, True), # ta'
     ("/ث/", l_arabic, True), # tha'
     ("/ج/", l_arabic, True), # jim
     ("/ح/", l_arabic, True), # h.a'
     ("/خ'/", l_arabic, True), # kha'
     ("/د/", l_arabic, True), # dal (isol + init)
     ("/ذ/", l_arabic, True), # dhal (isol + init)
     ("/ر/", l_arabic, True), # ra' (isol + init)
     ("/ز/", l_arabic, True), # za' (isol + init)
     ("/س/", l_arabic, True), # sin
     ("/ش/", l_arabic, True), # shin
     ("/ص/", l_arabic, True), # s.ad
     ("/ض/", l_arabic, True), # d.ad
     ("/ط/", l_arabic, True), # t.a'
     ("/ظ/", l_arabic, True), # z.a'
     ("/ع/", l_arabic, True), # 'ayn
     ("/غ/", l_arabic, True), # ghayn
     ("/ف/", l_arabic, True), # fa'
     ("/ق/", l_arabic, True), # qaf
     ("/ك/", l_arabic, True), # kaf
     ("/ل/", l_arabic, True), # lam
     ("/م/", l_arabic, True), # mim
     ("/ن/", l_arabic, True), # nun
     ("/ه/", l_arabic, True), # ha'
     ("/و/", l_arabic, True), # waw (isol + init)
     ("/ي/", l_arabic, True), # ya'

     ("/آ/", l_arabic, True), # alif madda
     ("/إ/", l_arabic, True), # alif + diacritic
     ("/أ/", l_arabic, True), # alif + hamza
     ("/ؤ/", l_arabic, True), #  waw + hamza
     ("/ئ/", l_arabic, True), #  ya' + hamza
     #    ("/لا/‎", l_arabic, True), # ligature l+a

     # Hebrew
     ("/א/", l_hebrew, True),
     ("/ב/", l_hebrew, True),
     ("/ג/", l_hebrew, True),
     ("/ד/", l_hebrew, True),
     ("/ה/", l_hebrew, True),
     ("/ו/", l_hebrew, True),
     ("/ז/", l_hebrew, True),
     ("/ח/", l_hebrew, True),
     ("/ט/", l_hebrew, True),
     ("/י/", l_hebrew, True),
     ("/כ/", l_hebrew, True),
     ("/ל/", l_hebrew, True),
     ("/מ/", l_hebrew, True),
     ("/נ/", l_hebrew, True),
     ("/ס/", l_hebrew, True),
     ("/ע/", l_hebrew, True),
     ("/פ/", l_hebrew, True),
     ("/צ/", l_hebrew, True),
     ("/ק/", l_hebrew, True),
     ("/ר/", l_hebrew, True),
     ("/ש/", l_hebrew, True),
     ("/ת/", l_hebrew, True),

     # 2. following are rules to reject the language

     # Every Latin character word has at least one Latin vowel
     ("/a/", l_cyrillic + l_hebrew + l_greek + l_arabic, False),
     ("/o/", l_cyrillic + l_hebrew + l_greek + l_arabic, False),
     ("/e/", l_cyrillic + l_hebrew + l_greek + l_arabic, False),
     ("/i/", l_cyrillic + l_hebrew + l_greek + l_arabic, False),
     ("/y/", l_cyrillic + l_hebrew + l_greek  + l_arabic + l_romanian + l_dutch, False),
     ("/u/", l_cyrillic + l_hebrew + l_greek + l_arabic, False),

     ("/j/", l_italian, False),
     ("/j[^aoeiuy]/", l_french+l_spanish+l_portuguese+l_greeklatin, False),
     ("/g/", l_czech, False),
     ("/k/", l_romanian + l_spanish + l_portuguese + l_french + l_italian, False),
     ("/q/", l_hungarian + l_polish + l_russian + l_romanian + l_czech + l_dutch + l_turkish + l_greeklatin, False),
     ("/v/", l_polish, False),
     ("/w/", l_french + l_romanian + l_spanish + l_hungarian + l_russian + l_czech + l_turkish + l_greeklatin, False),
     ("/x/", l_czech + l_hungarian + l_dutch + l_turkish, False), # polish excluded from the list

     ("/dj/", l_spanish + l_turkish, False),
     ("/v[^aoeiu]/", l_german, False), # in german, "v" can be found before a vowel only
     ("/y[^aoeiu]/", l_german, False),  # in german, "y" usually appears only in the last position; sometimes before a vowel
     ("/c[^aohk]/", l_german, False),
     ("/dzi/", l_german + l_english + l_french + l_turkish, False),
     ("/ou/", l_german, False),
     ("/a[eiou]/", l_turkish, False), # no diphthongs in Turkish
     ("/ö[eaiou]/", l_turkish, False),
     ("/ü[eaiou]/", l_turkish, False),
     ("/e[aiou]/", l_turkish, False),
     ("/i[aeou]/", l_turkish, False),
     ("/o[aieu]/", l_turkish, False),
     ("/u[aieo]/", l_turkish, False),
     ("/aj/", l_german + l_english + l_french + l_dutch, False),
     ("/ej/", l_german + l_english + l_french + l_dutch, False),
     ("/oj/", l_german + l_english + l_french + l_dutch, False),
     ("/uj/", l_german + l_english + l_french + l_dutch, False),
     ("/eu/", l_russian + l_polish, False),
     ("/ky/", l_polish, False),
     ("/kie/", l_french + l_spanish + l_greeklatin, False),
     ("/gie/", l_portuguese + l_romanian + l_spanish + l_greeklatin, False),
     ("/ch[aou]/", l_italian, False),
     ("/ch/", l_turkish, False),
     ("/son$/", l_german, False),
     ('/sc[ei]/', l_french, False),
     ('/sch/', l_hungarian + l_polish + l_french + l_spanish, False),
     ('/^h/', l_russian, False)

     )

# gen/languagenames.php
_gen_languages = ("any", "arabic", "cyrillic", "czech", "dutch", "english", "french", "german", "greek",
     "greeklatin", "hebrew", "hungarian", "italian", "polish", "portuguese","romanian",
     "russian", "spanish", "turkish")

# gen/rulesany.php
# format of each entry rule in the table
#   (pattern, left context, right context, phonetic)
# where
#   pattern is a sequence of characters that might appear in the word to be transliterated
#   left context is the context that precedes the pattern
#   right context is the context that follows the pattern
#   phonetic is the result that this rule generates
#
# note that both left context and right context can be regular expressions
# ex: left context of ^ would mean start of word
#     left context of [aeiouy] means following a vowel
#     right context of [^aeiouy] means preceding a consonant
#     right context of e$ means preceding a final e

#GENERIC
_gen_rules_any = (

     # CONVERTING FEMININE TO MASCULINE
     ("yna","","$","(in[l_russian]|ina)"),
     ("ina","","$","(in[l_russian]|ina)"),
     ("liova","","$","(lova|lof[l_russian]|lef[l_russian])"),
     ("lova","","$","(lova|lof[l_russian]|lef[l_russian]|l[l_czech]|el[l_czech])"),
     ("kova","","$","(kova|kof[l_russian]|k[l_czech]|ek[l_czech])"),
     ("ova","","$","(ova|of[l_russian]|[l_czech])"),
     ("ová","","$","(ova|[l_czech])"),
     ("eva","","$","(eva|ef[l_russian])"),
     ("aia","","$","(aja|i[l_russian])"),
     ("aja","","$","(aja|i[l_russian])"),
     ("aya","","$","(aja|i[l_russian])"),

     ("lowa","","$","(lova|lof[l_polish]|l[l_polish]|el[l_polish])"),
     ("kowa","","$","(kova|kof[l_polish]|k[l_polish]|ek[l_polish])"),
     ("owa","","$","(ova|of[l_polish]|)"),
     ("lowna","","$","(lovna|levna|l[l_polish]|el[l_polish])"),
     ("kowna","","$","(kovna|k[l_polish]|ek[l_polish])"),
     ("owna","","$","(ovna|[l_polish])"),
     ("lówna","","$","(l|el)"),  # polish
     ("kówna","","$","(k|ek)"),  # polish
     ("ówna","","$",""),         # polish
     ("á","","$","(a|i[l_czech])"),
     ("a","","$","(a|i[l_polish+l_czech])"),

     # CONSONANTS
     ("pf","","","(pf|p|f)"),
     ("que","","$","(k[l_french]|ke|kve)"),
     ("qu","","","(kv|k)"),

     ("m","","[bfpv]","(m|n)"),
     ("m","[aeiouy]","[aeiouy]", "m"),
     ("m","[aeiouy]","", "(m|n[l_french+l_portuguese])"),  # nasal

     ("ly","","[au]","l"),
     ("li","","[au]","l"),
     ("lio","","","(lo|le[l_russian])"),
     ("lyo","","","(lo|le[l_russian])"),
     #("ll","","","(l|J[l_spanish])"),  # Disabled Argentinian rule
     ("lt","u","$","(lt|[l_french])"),

     ("v","^","","(v|f[l_german]|b[l_spanish])"),

     ("ex","","[aáuiíoóeéêy]","(ez[l_portuguese]|eS[l_portuguese]|eks|egz)"),
     ("ex","","[cs]","(e[l_portuguese]|ek)"),
     ("x","u","$","(ks|[l_french])"),

     ("ck","","","(k|tsk[l_polish+l_czech])"),
     ("cz","","","(tS|tsz[l_czech])"), # Polish

     #Proceccing of "h" in various combinations
     ("rh","^","","r"),
     ("dh","^","","d"),
     ("bh","^","","b"),

     ("ph","","","(ph|f)"),
     ("kh","","","(x[l_russian+l_english]|kh)"),

     ("lh","","","(lh|l[l_portuguese])"),
     ("nh","","","(nh|nj[l_portuguese])"),

     ("ssch","","","S"),      # german
     ("chsch","","","xS"),    # german
     ("tsch","","","tS"),     # german

     # ("desch","^","","deS"),
     # ("desh","^","","(dES|de[l_french])"),
     # ("des","^","[^aeiouy]","(dEs|de[l_french])"),

     ("sch","[aeiouy]","[ei]","(S|StS[l_russian]|sk[l_romanian+l_italian])"),
     ("sch","[aeiouy]","","(S|StS[l_russian])"),
     ("sch","","[ei]","(sk[l_romanian+l_italian]|S|StS[l_russian])"),
     ("sch","","","(S|StS[l_russian])"),
     ("ssh","","","S"),

     ("sh","","[äöü]","sh"),      # german
     ("sh","","[aeiou]","(S[l_russian+l_english]|sh)"),
     ("sh","","","S"),

     ("zh","","","(Z[l_english+l_russian]|zh|tsh[l_german])"),

     ("chs","","","(ks[l_german]|xs|tSs[l_russian+l_english])"),
     ("ch","","[ei]","(x|tS[l_spanish+l_english+l_russian]|k[l_romanian+l_italian]|S[l_portuguese+l_french])"),
     ("ch","","","(x|tS[l_spanish+l_english+l_russian]|S[l_portuguese+l_french])"),

     ("th","^","","t"),     # english+german+greeklatin
     ("th","","[äöüaeiou]","(t[l_english+l_german+l_greeklatin]|th)"),
     ("th","","","t"),  # english+german+greeklatin

     ("gh","","[ei]","(g[l_romanian+l_italian+l_greeklatin]|gh)"),

     ("ouh","","[aioe]","(v[l_french]|uh)"),
     ("uh","","[aioe]","(v|uh)"),
     ("h","","$",""),
     ("h","[aeiouyäöü]","",""),  # l_german
     ("h","^","","(h|x[l_romanian+l_greeklatin]|H[l_english+l_romanian+l_polish+l_french+l_portuguese+l_italian+l_spanish])"),

     #Processing of "ci", "ce" & "cy"
     ("cia","","","(tSa[l_polish]|tsa)"),  # Polish
     ("cią","","[bp]","(tSom|tsom)"),     # Polish
     ("cią","","","(tSon[l_polish]|tson)"), # Polish
     ("cię","","[bp]","(tSem[l_polish]|tsem)"), # Polish
     ("cię","","","(tSen[l_polish]|tsen)"), # Polish
     ("cie","","","(tSe[l_polish]|tse)"),  # Polish
     ("cio","","","(tSo[l_polish]|tso)"),  # Polish
     ("ciu","","","(tSu[l_polish]|tsu)"), # Polish

     ("sci","","$","(Si[l_italian]|stsi[l_polish+l_czech]|dZi[l_turkish]|tSi[l_polish+l_romanian]|tS[l_romanian]|si)"),
     ("sc","","[ei]","(S[l_italian]|sts[l_polish+l_czech]|dZ[l_turkish]|tS[l_polish+l_romanian]|s)"),
     ("ci","","$","(tsi[l_polish+l_czech]|dZi[l_turkish]|tSi[l_polish+l_romanian]|tS[l_romanian]|si)"),
     ("cy","","","(si|tsi[l_polish])"),
     ("c","","[ei]","(ts[l_polish+l_czech]|dZ[l_turkish]|tS[l_polish+l_romanian]|k[l_greeklatin]|s)"),

     #Processing of "s"
     ("sç","","[aeiou]","(s|stS[l_turkish])"),
     ("ssz","","","S"), # polish
     ("sz","^","","(S|s[l_hungarian])"), # polish
     ("sz","","$","(S|s[l_hungarian])"), # polish
     ("sz","","","(S|s[l_hungarian]|sts[l_german])"), # polish
     ("ssp","","","(Sp[l_german]|sp)"),
     ("sp","","","(Sp[l_german]|sp)"),
     ("sst","","","(St[l_german]|st)"),
     ("st","","","(St[l_german]|st)"),
     ("ss","","","s"),
     ("sj","^","","S"), # dutch
     ("sj","","$","S"), # dutch
     ("sj","","","(sj|S[l_dutch]|sx[l_spanish]|sZ[l_romanian+l_turkish])"),

     ("sia","","","(Sa[l_polish]|sa[l_polish]|sja)"),
     ("sią","","[bp]","(Som[l_polish]|som)"), # polish
     ("sią","","","(Son[l_polish]|son)"), # polish
     ("się","","[bp]","(Sem[l_polish]|sem)"), # polish
     ("się","","","(Sen[l_polish]|sen)"), # polish
     ("sie","","","(se|sje|Se[l_polish]|zi[l_german])"),

     ("sio","","","(So[l_polish]|so)"),
     ("siu","","","(Su[l_polish]|sju)"),

     ("si","[äöëaáuiíoóeéêy]","","(Si[l_polish]|si|zi[l_portuguese+l_french+l_italian+l_german])"),
     ("si","","","(Si[l_polish]|si|zi[l_german])"),
     ("s","[aáuiíoóeéêy]","[aáuíoóeéêy]","(s|z[l_portuguese+l_french+l_italian+l_german])"),
     ("s","","[aeouäöë]","(s|z[l_german])"),
     ("s","[aeiouy]","[dglmnrv]","(s|z|Z[l_portuguese]|[l_french])"), # Groslot
     ("s","","[dglmnrv]","(s|z|Z[l_portuguese])"),

     #Processing of "g"
     ("gue","","$","(k[l_french]|gve)"),  # portuguese+spanish
     ("gu","","[ei]","(g[l_french]|gv[l_portuguese+l_spanish])"), # portuguese+spanish
     ("gu","","[ao]","gv"),     # portuguese+spanish
     ("guy","","","gi"),  # french

     ("gli","","","(glI|l[l_italian])"),
     ("gni","","","(gnI|ni[l_italian+l_french])"),
     ("gn","","[aeou]","(n[l_italian+l_french]|nj[l_italian+l_french]|gn)"),

     ("ggie","","","(je[l_greeklatin]|dZe)"), # dZ is Italian
     ("ggi","","[aou]","(j[l_greeklatin]|dZ)"), # dZ is Italian

     ("ggi","[yaeiou]","[aou]","(gI|dZ[l_italian]|j[l_greeklatin])"),
     ("gge","[yaeiou]","","(gE|xe[l_spanish]|gZe[l_portuguese+l_french]|dZe[l_english+l_romanian+l_italian+l_spanish]|je[l_greeklatin])"),
     ("ggi","[yaeiou]","","(gI|xi[l_spanish]|gZi[l_portuguese+l_french]|dZi[l_english+l_romanian+l_italian+l_spanish]|i[l_greeklatin])"),
     ("ggi","","[aou]","(gI|dZ[l_italian]|j[l_greeklatin])"),

     ("gie","","$","(ge|gi[l_german]|ji[l_french]|dZe[l_italian])"),
     ("gie","","","(ge|gi[l_german]|dZe[l_italian]|je[l_greeklatin])"),
     ("gi","","[aou]","(i[l_greeklatin]|dZ)"), # dZ is Italian

     ("ge","[yaeiou]","","(gE|xe[l_spanish]|Ze[l_portuguese+l_french]|dZe[l_english+l_romanian+l_italian+l_spanish])"),
     ("gi","[yaeiou]","","(gI|xi[l_spanish]|Zi[l_portuguese+l_french]|dZi[l_english+l_romanian+l_italian+l_spanish])"),
     ("ge","","","(gE|xe[l_spanish]|hE[l_russian]|je[l_greeklatin]|Ze[l_portuguese+l_french]|dZe[l_english+l_romanian+l_italian+l_spanish])"),
     ("gi","","","(gI|xi[l_spanish]|hI[l_russian]|i[l_greeklatin]|Zi[l_portuguese+l_french]|dZi[l_english+l_romanian+l_italian+l_spanish])"),
     ("gy","","[aeouáéóúüöőű]","(gi|dj[l_hungarian])"),
     ("gy","","","(gi|d[l_hungarian])"),
     ("g","[yaeiou]","[aouyei]","g"),
     ("g","","[aouei]","(g|h[l_russian])"),

     #Processing of "j"
     ("ij","","","(i|ej[l_dutch]|ix[l_spanish]|iZ[l_french+l_romanian+l_turkish+l_portuguese])"),
     ("j","","[aoeiuy]","(j|dZ[l_english]|x[l_spanish]|Z[l_french+l_romanian+l_turkish+l_portuguese])"),

     #Processing of "z"
     ("rz","t","","(S[l_polish]|r)"), # polish
     ("rz","","","(rz|rts[l_german]|Z[l_polish]|r[l_polish]|rZ[l_polish])"),

     ("tz","","$","(ts|tS[l_english+l_german])"),
     ("tz","^","","(ts[l_english+l_german+l_russian]|tS[l_english+l_german])"),
     ("tz","","","(ts[l_english+l_german+l_russian]|tz)"),

     ("zia","","[bcdgkpstwzż]","(Za[l_polish]|za[l_polish]|zja)"),
     ("zia","","","(Za[l_polish]|zja)"),
     ("zią","","[bp]","(Zom[l_polish]|zom)"),  # polish
     ("zią","","","(Zon[l_polish]|zon)"), # polish
     ("zię","","[bp]","(Zem[l_polish]|zem)"), # polish
     ("zię","","","(Zen[l_polish]|zen)"), # polish
     ("zie","","[bcdgkpstwzż]","(Ze[l_polish]|ze[l_polish]|ze|tsi[l_german])"),
     ("zie","","","(ze|Ze[l_polish]|tsi[l_german])"),
     ("zio","","","(Zo[l_polish]|zo)"),
     ("ziu","","","(Zu[l_polish]|zju)"),
     ("zi","","","(Zi[l_polish]|zi|tsi[l_german]|dzi[l_italian]|tsi[l_italian]|si[l_spanish])"),

     ("z","","$","(s|ts[l_german]|ts[l_italian]|S[l_portuguese])"), # ts It, s/S/Z Port, s in Sp, z Fr
     ("z","","[bdgv]","(z|dz[l_italian]|Z[l_portuguese])"), # dz It, Z/z Port, z Sp & Fr
     ("z","","[ptckf]","(s|ts[l_italian]|S[l_portuguese])"), # ts It, s/S/z Port, z/s Sp

     # VOWELS
     ("aue","","","aue"),
     ("oue","","","(oue|ve[l_french])"),
     ("eau","","","o"), # French

     ("ae","","","(Y[l_german]|aje[l_russian]|ae)"),
     ("ai","","","aj"),
     ("au","","","(au|o[l_french])"),
     ("ay","","","aj"),
     ("ão","","","(au|an)"), # Port
     ("ãe","","","(aj|an)"), # Port
     ("ãi","","","(aj|an)"), # Port
     ("ea","","","(ea|ja[l_romanian])"),
     ("ee","","","(i[l_english]|aje[l_russian]|e)"),
     ("ei","","","(aj|ej)"),
     ("eu","","","(eu|Yj[l_german]|ej[l_german]|oj[l_german]|Y[l_dutch])"),
     ("ey","","","(aj|ej)"),
     ("ia","","","ja"),
     ("ie","","","(i[l_german]|e[l_polish]|ije[l_russian]|Q[l_dutch]|je)"),
     ("ii","","$","i"), # russian
     ("io","","","(jo|e[l_russian])"),
     ("iu","","","ju"),
     ("iy","","$","i"), # russian
     ("oe","","","(Y[l_german]|oje[l_russian]|u[l_dutch]|oe)"),
     ("oi","","","oj"),
     ("oo","","","(u[l_english]|o)"),
     ("ou","","","(ou|u[l_french+l_greeklatin]|au[l_dutch])"),
     ("où","","","u"), # french
     ("oy","","","oj"),
     ("õe","","","(oj|on)"), # Port
     ("ua","","","va"),
     ("ue","","","(Q[l_german]|uje[l_russian]|ve)"),
     ("ui","","","(uj|vi|Y[l_dutch])"),
     ("uu","","","(u|Q[l_dutch])"),
     ("uo","","","(vo|o)"),
     ("uy","","","uj"),
     ("ya","","","ja"),
     ("ye","","","(je|ije[l_russian])"),
     ("yi","^","","i"),
     ("yi","","$","i"), # russian
     ("yo","","","(jo|e[l_russian])"),
     ("yu","","","ju"),
     ("yy","","$","i"), # russian

     ("i","[áóéê]","","j"),
     ("y","[áóéê]","","j"),

     ("e","^","","(e|je[l_russian])"),
     ("e","","$","(e|EE[l_english+l_french])"),

     # LANGUAGE SPECIFIC CHARACTERS
     ("ą","","[bp]","om"), # polish
     ("ą","","","on"),  # polish
     ("ä","","","(Y|e)"),
     ("á","","","a"), # Port & Sp
     ("à","","","a"),
     ("â","","","a"),
     ("ã","","","(a|an)"), # Port
     ("ă","","","(e[l_romanian]|a)"), # romanian
     ("č","","", "tS"), # czech
     ("ć","","","(tS[l_polish]|ts)"),  # polish
     ("ç","","","(s|tS[l_turkish])"),
     ("ď","","","(d|dj[l_czech])"),
     ("ę","","[bp]","em"), # polish
     ("ę","","","en"), # polish
     ("é","","","e"),
     ("è","","","e"),
     ("ê","","","e"),
     ("ě","","","(e|je[l_czech])"),
     ("ğ","","",""), # turkish
     ("í","","","i"),
     ("î","","","i"),
     ("ı","","","(i|e[l_turkish]|[l_turkish])"),
     ("ł","","","l"),
     ("ń","","","(n|nj[l_polish])"), # polish
     ("ñ","","","(n|nj[l_spanish])"),
     ("ó","","","(u[l_polish]|o)"),
     ("ô","","","o"), # Port & Fr
     ("õ","","","(o|on[l_portuguese]|Y[l_hungarian])"),
     ("ò","","","o"),  # Sp & It
     ("ö","","","Y"),
     ("ř","","","(r|rZ[l_czech])"),
     ("ś","","","(S[l_polish]|s)"),
     ("ş","","","S"), # romanian+turkish
     ("š","","", "S"), # czech
     ("ţ","","","ts"),  # romanian
     ("ť","","","(t|tj[l_czech])"),
     ("ű","","","Q"), # hungarian
     ("ü","","","(Q|u[l_portuguese+l_spanish])"),
     ("ú","","","u"),
     ("ů","","","u"), # czech
     ("ù","","","u"), # french
     ("ý","","","i"),  # czech
     ("ż","","","Z"), # polish
     ("ź","","","(Z[l_polish]|z)"),

     ("ß","","","s"), # german
     ("'","","",""), # russian
     ('"',"","",""), # russian

     ("o","","[bcćdgklłmnńrsśtwzźż]","(O|P[l_polish])"),

     # LATIN ALPHABET
     ("a","","","A"),
     ("b","","","B"),
     ("c","","","(k|ts[l_polish+l_czech]|dZ[l_turkish])"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     #("g","","","(g|x[l_dutch])"), # Dutch sound disabled
     ("g","","","g"),
     ("h","","","(h|x[l_romanian]|H[l_french+l_portuguese+l_italian+l_spanish])"),
     ("i","","","I"),
     ("j","","","(j|x[l_spanish]|Z[l_french+l_romanian+l_turkish+l_portuguese])"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","O"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","(s|S[l_portuguese])"),
     ("t","","","t"),
     ("u","","","U"),
     ("v","","","V"),
     ("w","","","(v|w[l_english+l_dutch])"),
     ("x","","","(ks|gz|S[l_portuguese+l_spanish])"),   # S/ks Port & Sp, gz Sp, It only ks
     ("y","","","i"),
     ("z","","","(z|ts[l_german]|dz[l_italian]|ts[l_italian]|s[l_spanish])"), # ts/dz It, z Port & Fr, z/s Sp

     )

# gen/rulesarabic.php

# General
_gen_rules_arabic = (

     ("ا","","","a"), # alif isol & init

     ("ب","","$","b"),
     ("ب","","","b1"), # ba' isol

     ("ت","","$","t"),
     ("ت","","","t1"), # ta' isol

     ("ث","","$","t"),
     ("ث","","","t1"), # tha' isol

     ("ج","","$","(dZ|Z)"),
     ("ج","","","(dZ1|Z1)"), # jim isol

     ("ح","^","","1"),
     ("ح","","$","1"),
     ("ح","","","(h1|1)"), # h.a' isol

     ("خ","","$","x"),
     ("خ","","","x1"), # kha' isol

     ("د","","$","d"),
     ("د","","","d1"), # dal isol & init

     ("ذ","","$","d"),
     ("ذ","","","d1"), # dhal isol & init

     ("ر","","$","r"),
     ("ر","","","r1"), # ra' isol & init

     ("ز","","$","z"),
     ("ز","","","z1"), # za' isol & init

     ("س","","$","s"),
     ("س","","","s1"), # sin isol

     ("ش","","$","S"),
     ("ش","","","S1"), # shin isol

     ("ص","","$","s"),
     ("ص","","","s1"), # s.ad isol

     ("ض","","$","d"),
     ("ض","","","d1"), # d.ad isol

     ("ط","","$","t"),
     ("ط","","","t1"), # t.a' isol

     ("ظ","","$","z"),
     ("ظ","","","z1"), # z.a' isol

     ("ع","^","", "1"),
     ("ع","","$", "1"),
     ("ع","","", "(h1|1)"), # ayin isol

     ("غ","","$","g"),
     ("غ","","","g1"), # ghayin isol

     ("ف","","$","f"),
     ("ف","","","f1"), # fa' isol

     ("ق","","$","k"),
     ("ق","","","k1"), # qaf isol

     ("ك","","$","k"),
     ("ك","","","k1"), # kaf isol

     ("ل","","$","l"),
     ("ل","","","l1"), # lam isol

     ("م","","$","m"),
     ("م","","","m1"), # mim isol

     ("ن","","$","n"),
     ("ن","","","n1"), # nun isol

     ("ه","^","","1"),
     ("ه","","$","1"),
     ("ه","","","(h1|1)"), # h isol

     ("و","","$", "(u|v)"),
     ("و","","", "(u|v1)"), # waw, isol + init

     ("ي‎","","$","(i|j)"),
     ("ي‎","","","(i|j1)"), # ya' isol

     )

# gen/rulescyrillic.php

# GENERAL
_gen_rules_cyrillic = (
     ("ця","","","tsa"),
     ("цю","","","tsu"),
     ("циа","","","tsa"),
     ("цие","","","tse"),
     ("цио","","","tso"),
     ("циу","","","tsu"),
     ("сие","","","se"),
     ("сио","","","so"),
     ("зие","","","ze"),
     ("зио","","","zo"),
     ("с","","с",""),

     ("гауз","","$","haus"),
     ("гаус","","$","haus"),
     ("гольц","","$","holts"),
     ("геймер","","$","(hejmer|hajmer)"),
     ("гейм","","$","(hejm|hajm)"),
     ("гоф","","$","hof"),
     ("гер","","$","ger"),
     ("ген","","$","gen"),
     ("гин","","$","gin"),
     ("г","(й|ё|я|ю|ы|а|е|о|и|у)","(а|е|о|и|у)","g"),
     ("г","","(а|е|о|и|у)","(g|h)"),

     ("ля","","","la"),
     ("лю","","","lu"),
     ("лё","","","(le|lo)"),
     ("лио","","","(le|lo)"),
     ("ле","","","(lE|lo)"),

     ("ийе","","","je"),
     ("ие","","","je"),
     ("ыйе","","","je"),
     ("ые","","","je"),
     ("ий","","(а|о|у)","j"),
     ("ый","","(а|о|у)","j"),
     ("ий","","$","i"),
     ("ый","","$","i"),

     ("ей","^","","(jej|ej)"),
     ("е","(а|е|о|у)","","je"),
     ("е","^","","je"),
     ("эй","","","ej"),
     ("ей","","","ej"),

     ("ауе","","","aue"),
     ("ауэ","","","aue"),

     ("а","","","a"),
     ("б","","","b"),
     ("в","","","v"),
     ("г","","","g"),
     ("д","","","d"),
     ("е","","","E"),
     ("ё","","","(e|jo)"),
     ("ж","","","Z"),
     ("з","","","z"),
     ("и","","","I"),
     ("й","","","j"),
     ("к","","","k"),
     ("л","","","l"),
     ("м","","","m"),
     ("н","","","n"),
     ("о","","","o"),
     ("п","","","p"),
     ("р","","","r"),
     ("с","","","s"),
     ("т","","","t"),
     ("у","","","u"),
     ("ф","","","f"),
     ("х","","","x"),
     ("ц","","","ts"),
     ("ч","","","tS"),
     ("ш","","","S"),
     ("щ","","","StS"),
     ("ъ","","",""),
     ("ы","","","I"),
     ("ь","","",""),
     ("э","","","E"),
     ("ю","","","ju"),
     ("я","","","ja"),

     )

# gen/rulesczech.php

_gen_rules_czech = (
     ("ch","","","x"),
     ("qu","","","(k|kv)"),
     ("aue","","","aue"),
     ("ei","","","(ej|aj)"),
     ("i","[aou]","","j"),
     ("i","","[aeou]","j"),

     ("č","","","tS"),
     ("š","","","S"),
     ("ň","","","n"),
     ("ť","","","(t|tj)"),
     ("ď","","","(d|dj)"),
     ("ř","","","(r|rZ)"),

     ("á","","","a"),
     ("é","","","e"),
     ("í","","","i"),
     ("ó","","","o"),
     ("ú","","","u"),
     ("ý","","","i"),
     ("ě","","","(e|je)"),
     ("ů","","","u"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","ts"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","(h|g)"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","(k|kv)"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","z"),

     )

# gen/rulesdutch.php

_gen_rules_dutch = (

     # CONSONANTS
     ("ssj","","","S"),
     ("sj","","","S"),
     ("ch","","","x"),
     ("c","","[eiy]","ts"),
     ("ck","","","k"),     # German
     ("pf","","","(pf|p|f)"), # German
     ("ph","","","(ph|f)"),
     ("qu","","","kv"),
     ("th","^","","t"), # German
     ("th","","[äöüaeiou]","(t|th)"), # German
     ("th","","","t"), # German
     ("ss","","","s"),
     ("h","[aeiouy]","",""),

     # VOWELS
     ("aue","","","aue"),
     ("ou","","","au"),
     ("ie","","","(Q|i)"),
     ("uu","","","(Q|u)"),
     ("ee","","","e"),
     ("eu","","","(Y|Yj)"), # Dutch Y
     ("aa","","","a"),
     ("oo","","","o"),
     ("oe","","","u"),
     ("ij","","","ej"),
     ("ui","","","(Y|uj)"),
     ("ei","","","(ej|aj)"), # Dutch ej

     ("i","","[aou]","j"),
     ("y","","[aeou]","j"),
     ("i","[aou]","","j"),
     ("y","[aeou]","","j"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","(g|x)"),
     ("h","","","h"),
     ("i","","","(i|Q)"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","(u|Q)"),
     ("v","","","v"),
     ("w","","","(w|v)"),
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","z"),

     )

# gen/rulesenglish.php

# GENERAL
_gen_rules_english = (

     # CONSONANTS
     ("","","",""), # ONeill
     ("'","","",""), # ONeill
     ("mc","^","","mak"), # McDonald
     ("tz","","","ts"), # Fitzgerald
     ("tch","","","tS"),
     ("ch","","","(tS|x)"),
     ("ck","","","k"),
     ("cc","","[iey]","ks"), # success, accent
     ("c","","c",""),
     ("c","","[iey]","s"), # circle

     ("gh","^","","g"), # ghost
     ("gh","","","(g|f|w)"), # burgh | tough | bough
     ("gn","","","(gn|n)"),
     ("g","","[iey]","(g|dZ)"), # get, gem, giant, gigabyte
     # ("th","","","(6|8|t)"),
     ("th","","","t"),
     ("kh","","","x"),
     ("ph","","","f"),
     ("sch","","","(S|sk)"),
     ("sh","","","S"),
     ("who","^","","hu"),
     ("wh","^","","w"),

     ("h","","$",""), # hard to find an example that isn't in a name
     ("h","","[^aeiou]",""), # hard to find an example that isn't in a name
     ("h","^","","H"),

     ("kn","^","","n"), # knight
     ("mb","","$","m"),
     ("ng","","$","(N|ng)"),
     ("pn","^","","(pn|n)"),
     ("ps","^","","(ps|s)"),
     ("qu","","","kw"),
     ("tia","","","(So|Sa)"),
     ("tio","","","So"),
     ("wr","^","","r"),
     ("x","^","","z"),

     # VOWELS
     ("y","^","","j"),
     ("y","^","[aeiouy]","j"),
     ("yi","^","","i"),
     ("aue","","","aue"),
     ("oue","","","(aue|oue)"),
     ("ai","","","(aj|ej|e)"), # rain | said
     ("ay","","","(aj|ej)"),
     ("a","","[^aeiou]e","ej"), # plane
     ("ei","","","(ej|aj|i)"), # weigh | receive
     ("ey","","","(ej|aj|i)"), # hey | barley
     ("ear","","","ia"), # tear
     ("ea","","","(i|e)"), # reason | treasure
     ("ee","","","i"), # between
     ("e","","[^aeiou]e","i"), # meter
     ("e","","$","(|E)"), # blame, badge
     ("ie","","","i"), # believe
     ("i","","[^aeiou]e","aj"), # five
     ("oa","","","ou"), # toad
     ("oi","","","oj"), # join
     ("oo","","","u"), # food
     ("ou","","","(u|ou)"), # through | tough | could
     ("oy","","","oj"), # boy
     ("o","","[^aeiou]e","ou"), # rode
     ("u","","[^aeiou]e","(ju|u)"), # cute | flute
     ("u","","r","(e|u)"), # turn -- Morse disagrees, feels it should go to E

     # LATIN ALPHABET
     ("a","","","(e|o|a)"), # hat | call | part
     ("b","","","b"),
     ("c","","","k"), # candy
     ("d","","","d"),
     ("e","","","E"), # bed
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"),
     ("j","","","dZ"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","(o|a)"), # hot
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","(u|a)"), # put
     ("v","","","v"),
     ("w","","","(w|v)"), # the variant "v" is for spellings coming from German/Polish
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","z"),

     )

# gen/rulesfrench.php

# GENERAL
_gen_rules_french = (

     # CONSONANTS
     ("lt","u","$","(lt|)"), # Renault
     ("c","n","$","(k|)"), # Tronc
     #("f","","","(f|)"), # Clef
     ("d","","$","(t|)"), # Durand
     ("g","n","$","(k|)"), # Gang
     ("p","","$","(p|)"), # Trop, Champ
     ("r","e","$","(r|)"), # Barbier
     ("t","","$","(t|)"), # Murat, Constant
     ("z","","$","(s|)"),

     ("ds","","$","(ds|)"),
     ("ps","","$","(ps|)"), # Champs
     ("rs","e","$","(rs|)"),
     ("ts","","$","(ts|)"),
     ("s","","$","(s|)"), # Denis

     ("x","u","$","(ks|)"), # Arnoux

     ("s","[aeéèêiou]","[^aeéèêiou]","(s|)"), # Deschamps, Malesherbes, Groslot
     ("t","[aeéèêiou]","[^aeéèêiou]","(t|)"), # Petitjean

     ("kh","","","x"), # foreign
     ("ph","","","f"),

     ("ç","","","s"),
     ("x","","","ks"),
     ("ch","","","S"),
     ("c","","[eiyéèê]","s"),

     ("gn","","","(n|gn)"),
     ("g","","[eiy]","Z"),
     ("gue","","$","k"),
     ("gu","","[eiy]","g"),
     ("aill","","e","aj"), # non Jewish
     ("ll","","e","(l|j)"), # non Jewish
     ("que","","$","k"),
     ("qu","","","k"),
     ("s","[aeiouyéèê]","[aeiouyéèê]","z"),
     ("h","[bdgt]","",""), # translit from Arabic

     ("m","[aeiouy]","[aeiouy]", "m"),
     ("m","[aeiouy]","", "(m|n)"),  # nasal

     ("ou","","[aeio]","v"),
     ("u","","[aeio]","v"),

     # VOWELS
     ("aue","","","aue"),
     ("eau","","","o"),
     ("au","","","(o|au)"), # non Jewish
     ("ai","","","(e|aj)"), # [e] is non Jewish
     ("ay","","","(e|aj)"), # [e] is non Jewish
     ("é","","","e"),
     ("ê","","","e"),
     ("è","","","e"),
     ("à","","","a"),
     ("â","","","a"),
     ("où","","","u"),
     ("ou","","","u"),
     ("oi","","","(oj|va)"), # [va] (actually "ua") is non Jewish
     ("ei","","","(aj|ej|e)"), # [e] is non Jewish
     ("ey","","","(aj|ej|e)"), # [e] non Jewish
     ("eu","","","(ej|Y)"), # non Jewish
     ("y","[ou]","","j"),
     ("e","","$","(e|)"),
     ("i","","[aou]","j"),
     ("y","","[aoeu]","j"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("j","","","Z"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","(u|Q)"),
     ("v","","","v"),
     ("w","","","v"),
     ("y","","","i"),
     ("z","","","z"),

     )

# gen/rulesgerman.php

# GENERIC
_gen_rules_german = (

     # CONSONANTS
     ("ewitsch","","$","evitS"),
     ("owitsch","","$","ovitS"),
     ("evitsch","","$","evitS"),
     ("ovitsch","","$","ovitS"),
     ("witsch","","$","vitS"),
     ("vitsch","","$","vitS"),
     ("ssch","","","S"),
     ("chsch","","","xS"),
     ("sch","","","S"),

     ("ziu","","","tsu"),
     ("zia","","","tsa"),
     ("zio","","","tso"),

     ("chs","","","ks"),
     ("ch","","","x"),
     ("ck","","","k"),
     ("c","","[eiy]","ts"),

     ("sp","^","","Sp"),
     ("st","^","","St"),
     ("ssp","","","(Sp|sp)"),
     ("sp","","","(Sp|sp)"),
     ("sst","","","(St|st)"),
     ("st","","","(St|st)"),
     ("pf","","","(pf|p|f)"),
     ("ph","","","(ph|f)"),
     ("qu","","","kv"),

     ("ewitz","","$","(evits|evitS)"),
     ("ewiz","","$","(evits|evitS)"),
     ("evitz","","$","(evits|evitS)"),
     ("eviz","","$","(evits|evitS)"),
     ("owitz","","$","(ovits|ovitS)"),
     ("owiz","","$","(ovits|ovitS)"),
     ("ovitz","","$","(ovits|ovitS)"),
     ("oviz","","$","(ovits|ovitS)"),
     ("witz","","$","(vits|vitS)"),
     ("wiz","","$","(vits|vitS)"),
     ("vitz","","$","(vits|vitS)"),
     ("viz","","$","(vits|vitS)"),
     ("tz","","","ts"),

     ("thal","","$","tal"),
     ("th","^","","t"),
     ("th","","[äöüaeiou]","(t|th)"),
     ("th","","","t"),
     ("rh","^","","r"),
     ("h","[aeiouyäöü]","",""),
     ("h","^","","H"),

     ("ss","","","s"),
     ("s","","[äöüaeiouy]","(z|s)"),
     ("s","[aeiouyäöüj]","[aeiouyäöü]","z"),
     ("ß","","","s"),

     # VOWELS
     ("ij","","$","i"),
     ("aue","","","aue"),
     ("ue","","","Q"),
     ("ae","","","Y"),
     ("oe","","","Y"),
     ("ü","","","Q"),
     ("ä","","","(Y|e)"),
     ("ö","","","Y"),
     ("ei","","","(aj|ej)"),
     ("ey","","","(aj|ej)"),
     ("eu","","","(Yj|ej|aj|oj)"),
     ("i","[aou]","","j"),
     ("y","[aou]","","j"),
     ("ie","","","I"),
     ("i","","[aou]","j"),
     ("y","","[aoeu]","j"),

     # FOREIGN LETTERs
     ("ñ","","","n"),
     ("ã","","","a"),
     ("ő","","","o"),
     ("ű","","","u"),
     ("ç","","","s"),

     # LATIN ALPHABET
     ("a","","","A"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","O"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","U"),
     ("v","","","(f|v)"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","ts"),

     )

# gen/rulesgreek.php

_gen_rules_greek = (

     ("αυ","","$","af"),  # "av" before vowels and voiced consonants, "af" elsewhere
     ("αυ","","(κ|π|σ|τ|φ|θ|χ|ψ)","af"),
     ("αυ","","","av"),
     ("ευ","","$","ef"), # "ev" before vowels and voiced consonants, "ef" elsewhere
     ("ευ","","(κ|π|σ|τ|φ|θ|χ|ψ)","ef"),
     ("ευ","","","ev"),
     ("ηυ","","$","if"), # "iv" before vowels and voiced consonants, "if" elsewhere
     ("ηυ","","(κ|π|σ|τ|φ|θ|χ|ψ)","if"),
     ("ηυ","","","iv"),
     ("ου","","","u"),  # [u:]

     ("αι","","","aj"),  # modern [e]
     ("ει","","","ej"), # modern [i]
     ("οι","","","oj"), # modern [i]
     ("ωι","","","oj"),
     ("ηι","","","ej"),
     ("υι","","","i"), # modern Greek "i"

     ("γγ","(ε|ι|η|α|ο|ω|υ)","(ε|ι|η)","(nj|j)"),
     ("γγ","","(ε|ι|η)","j"),
     ("γγ","(ε|ι|η|α|ο|ω|υ)","","(ng|g)"),
     ("γγ","","","g"),
     ("γκ","^","","g"),
     ("γκ","(ε|ι|η|α|ο|ω|υ)","(ε|ι|η)","(nj|j)"),
     ("γκ","","(ε|ι|η)","j"),
     ("γκ","(ε|ι|η|α|ο|ω|υ)","","(ng|g)"),
     ("γκ","","","g"),
     ("γι","","(α|ο|ω|υ)","j"),
     ("γι","","","(gi|i)"),
     ("γε","","(α|ο|ω|υ)","j"),
     ("γε","","","(ge|je)"),

     ("κζ","","","gz"),
     ("τζ","","","dz"),
     ("σ","","(β|γ|δ|μ|ν|ρ)","z"),

     ("μβ","","","(mb|b)"),
     ("μπ","^","","b"),
     ("μπ","(ε|ι|η|α|ο|ω|υ)","","mb"),
     ("μπ","","","b"), # after any consonant
     ("ντ","^","","d"),
     ("ντ","(ε|ι|η|α|ο|ω|υ)","","(nd|nt)"), # Greek is "nd"
     ("ντ","","","(nt|d)"), # Greek is "d" after any consonant

     ("ά","","","a"),
     ("έ","","","e"),
     ("ή","","","(i|e)"),
     ("ί","","","i"),
     ("ό","","","o"),
     ("ύ","","","(Q|i|u)"),
     ("ώ","","","o"),
     ("ΰ","","","(Q|i|u)"),
     ("ϋ","","","(Q|i|u)"),
     ("ϊ","","","j"),

     ("α","","","a"),
     ("β","","","(v|b)"), # modern "v", old "b"
     ("γ","","","g"),
     ("δ","","","d"),    # modern like "th" in English "them", old "d"
     ("ε","","","e"),
     ("ζ","","","z"),
     ("η","","","(i|e)"), # modern "i", old "e:"
     ("ι","","","i"),
     ("κ","","","k"),
     ("λ","","","l"),
     ("μ","","","m"),
     ("ν","","","n"),
     ("ξ","","","ks"),
     ("ο","","","o"),
     ("π","","","p"),
     ("ρ","","","r"),
     ("σ","","","s"),
     ("ς","","","s"),
     ("τ","","","t"),
     ("υ","","","(Q|i|u)"), # modern "i", old like German "ü"
     ("φ","","","f"),
     ("θ","","","t"), # old greek like "th" in English "theme"
     ("χ","","","x"),
     ("ψ","","","ps"),
     ("ω","","","o"),

     )

# gen/rulesgreeklatin.php

_gen_rules_greeklatin = (

     ("au","","$","af"),
     ("au","","[kpstfh]","af"),
     ("au","","","av"),
     ("eu","","$","ef"),
     ("eu","","[kpstfh]","ef"),
     ("eu","","","ev"),
     ("ou","","","u"),

     ("gge","[aeiouy]","","(nje|je)"), # aggelopoulos
     ("ggi","[aeiouy]","[aou]","(nj|j)"),
     ("ggi","[aeiouy]","","(ni|i)"),
     ("gge","","","je"),
     ("ggi","","","i"),
     ("gg","[aeiouy]","","(ng|g)"),
     ("gg","","","g"),
     ("gk","^","","g"),
     ("gke","[aeiouy]","","(nje|je)"),
     ("gki","[aeiouy]","","(ni|i)"),
     ("gke","","","je"),
     ("gki","","","i"),
     ("gk","[aeiouy]","","(ng|g)"),
     ("gk","","","g"),
     ("nghi","","[aouy]","Nj"),
     ("nghi","","","(Ngi|Ni)"),
     ("nghe","","[aouy]","Nj"),
     ("nghe","","","(Nje|Nge)"),
     ("ghi","","[aouy]","j"),
     ("ghi","","","(gi|i)"),
     ("ghe","","[aouy]","j"),
     ("ghe","","","(je|ge)"),
     ("ngh","","","Ng"),
     ("gh","","","g"),
     ("ngi","","[aouy]","Nj"),
     ("ngi","","","(Ngi|Ni)"),
     ("nge","","[aouy]","Nj"),
     ("nge","","","(Nje|Nge)"),
     ("gi","","[aouy]","j"),
     ("gi","","","(gi|i)"), # what about Pantazis = Pantagis ???
     ("ge","","[aouy]","j"),
     ("ge","","","(je|ge)"),
     ("ng","","","Ng"), # fragakis = fraggakis = frangakis; angel = agel = aggel

     ("i","","[aeou]","j"),
     ("i","[aeou]","","j"),
     ("y","","[aeou]","j"),
     ("y","[aeou]","","j"),
     ("yi","","[aeou]", "j"),
     ("yi","","", "i"),

     ("ch","","","x"),
     ("kh","","","x"),
     ("dh","","","d"),  # actually as "th" in English "that"
     ("dj","","","dZ"), # Turkish words
     ("ph","","","f"),
     ("th","","","t"),
     ("kz","","","gz"),
     ("tz","","","dz"),
     ("s","","[bgdmnr]","z"),

     ("mb","","","(mb|b)"), # Liberis = Limperis = Limberis
     ("mp","^","","b"),
     ("mp","[aeiouy]","","mp"),
     ("mp","","","b"),
     ("nt","^","","d"),
     ("nt","[aeiouy]","","(nd|nt)"), # Greek "nd"
     ("nt","","","(nt|d)"), # Greek "d" after any consonant

     ("á","","","a"),
     ("é","","","e"),
     ("í","","","i"),
     ("ó","","","o"),
     ("óu","","","u"),
     ("ú","","","u"),
     ("ý","","","(i|Q|u)"), # [ü]

     ("a","","","a"),
     ("b","","","(b|v)"), # beta: modern "v", old "b"
     ("c","","","k"),
     ("d","","","d"),    # modern like "th" in English "them", old "d"
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","x"),
     ("i","","","i"),
     ("j","","","(j|Z)"), # Panajotti = Panaiotti; Louijos = Louizos; Pantajis = Pantazis = Pantagis
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("ο","","","o"),
     ("p","","","p"),
     ("q","","","k"), # foreign
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"), # foreign
     ("x","","","ks"),
     ("y","","","(i|Q|u)"), # [ü]
     ("z","","","z"),

     )

# gen/ruleshebrew.php

# General = Ashkenazic
_gen_rules_hebrew = (

     ("אי","","","i"),
     ("עי","","","i"),
     ("עו","","","VV"),
     ("או","","","VV"),

     ("ג׳","","","Z"),
     ("ד׳","","","dZ"),

     ("א","","","L"),
     ("ב","","","b"),
     ("ג","","","g"),
     ("ד","","","d"),

     ("ה","^","","1"),
     ("ה","","$","1"),
     ("ה","","",""),

     ("וו","","","V"),
     ("וי","","","WW"),
     ("ו","","","W"),
     ("ז","","","z"),
     ("ח","","","X"),
     ("ט","","","T"),
     ("יי","","","i"),
     ("י","","","i"),
     ("ך","","","X"),
     ("כ","^","","K"),
     ("כ","","","k"),
     ("ל","","","l"),
     ("ם","","","m"),
     ("מ","","","m"),
     ("ן","","","n"),
     ("נ","","","n"),
     ("ס","","","s"),
     ("ע","","","L"),
     ("ף","","","f"),
     ("פ","","","f"),
     ("ץ","","","C"),
     ("צ","","","C"),
     ("ק","","","K"),
     ("ר","","","r"),
     ("ש","","","s"),
     ("ת","","","TB"), # only Ashkenazic

     )

# gen/ruleshungarian.php

# GENERAL
_gen_rules_hungarian = (

     # CONSONANTS
     ("sz","","","s"),
     ("zs","","","Z"),
     ("cs","","","tS"),

     ("ay","","","(oj|aj)"),
     ("ai","","","(oj|aj)"),
     ("aj","","","(oj|aj)"),

     ("ei","","","(aj|ej)"), # German element
     ("ey","","","(aj|ej)"), # German element

     ("y","[áo]","","j"),
     ("i","[áo]","","j"),
     ("ee","","","(ej|e)"),
     ("ely","","","(ej|eli)"),
     ("ly","","","(j|li)"),
     ("gy","","[aeouáéóúüöőű]","dj"),
     ("gy","","","(d|gi)"),
     ("ny","","[aeouáéóúüöőű]","nj"),
     ("ny","","","(n|ni)"),
     ("ty","","[aeouáéóúüöőű]","tj"),
     ("ty","","","(t|ti)"),
     ("qu","","","(ku|kv)"),
     ("h","","$",""),

     # SPECIAL VOWELS
     ("á","","","a"),
     ("é","","","e"),
     ("í","","","i"),
     ("ó","","","o"),
     ("ú","","","u"),
     ("ö","","","Y"),
     ("ő","","","Y"),
     ("ü","","","Q"),
     ("ű","","","Q"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","ts"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","(S|s)"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","z"),

     )

# gen/rulesitalian.php

_gen_rules_italian = (
     ("kh","","","x"), # foreign

     ("gli","","","(l|gli)"),
     ("gn","","[aeou]","(n|nj|gn)"),
     ("gni","","","(ni|gni)"),

     ("gi","","[aeou]","dZ"),
     ("gg","","[ei]","dZ"),
     ("g","","[ei]","dZ"),
     ("h","[bdgt]","","g"), # gh is It; others from Arabic translit
     ("h","","$",""), # foreign

     ("ci","","[aeou]","tS"),
     ("ch","","[ei]","k"),
     ("sc","","[ei]","S"),
     ("cc","","[ei]","tS"),
     ("c","","[ei]","tS"),
     ("s","[aeiou]","[aeiou]","z"),

     ("i","[aeou]","","j"),
     ("i","","[aeou]","j"),
     ("y","[aeou]","","j"), # foreign
     ("y","","[aeou]","j"), # foreign

     ("qu","","","k"),
     ("uo","","","(vo|o)"),
     ("u","","[aei]","v"),

     ("č","","","e"),
     ("é","","","e"),
     ("ň","","","o"),
     ("ó","","","o"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("j","","","(Z|dZ|j)"), # foreign
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),    # foreign
     ("x","","","ks"),    # foreign
     ("y","","","i"),    # foreign
     ("z","","","(ts|dz)"),

     )

# gen/rulespolish.php

# GENERIC
_gen_rules_polish = (

     # CONVERTING FEMININE TO MASCULINE
     ("ska","","$","ski"),
     ("cka","","$","tski"),
     ("lowa","","$","(lova|lof|l|el)"),
     ("kowa","","$","(kova|kof|k|ek)"),
     ("owa","","$","(ova|of|)"),
     ("lowna","","$","(lovna|levna|l|el)"),
     ("kowna","","$","(kovna|k|ek)"),
     ("owna","","$","(ovna|)"),
     ("lówna","","$","(l|el)"),
     ("kówna","","$","(k|ek)"),
     ("ówna","","$",""),
     ("a","","$","(a|i)"),

     # CONSONANTS
     ("czy","","","tSi"),
     ("cze","","[bcdgkpstwzż]","(tSe|tSF)"),
     ("ciewicz","","","(tsevitS|tSevitS)"),
     ("siewicz","","","(sevitS|SevitS)"),
     ("ziewicz","","","(zevitS|ZevitS)"),
     ("riewicz","","","rjevitS"),
     ("diewicz","","","djevitS"),
     ("tiewicz","","","tjevitS"),
     ("iewicz","","","evitS"),
     ("ewicz","","","evitS"),
     ("owicz","","","ovitS"),
     ("icz","","","itS"),
     ("cz","","","tS"),
     ("ch","","","x"),

     ("cia","","[bcdgkpstwzż]","(tSB|tsB)"),
     ("cia","","","(tSa|tsa)"),
     ("cią","","[bp]","(tSom|tsom)"),
     ("cią","","","(tSon|tson)"),
     ("cię","","[bp]","(tSem|tsem)"),
     ("cię","","","(tSen|tsen)"),
     ("cie","","[bcdgkpstwzż]","(tSF|tsF)"),
     ("cie","","","(tSe|tse)"),
     ("cio","","","(tSo|tso)"),
     ("ciu","","","(tSu|tsu)"),
     ("ci","","","(tSi|tsI)"),
     ("ć","","","(tS|ts)"),

     ("ssz","","","S"),
     ("sz","","","S"),
     ("sia","","[bcdgkpstwzż]","(SB|sB|sja)"),
     ("sia","","","(Sa|sja)"),
     ("sią","","[bp]","(Som|som)"),
     ("sią","","","(Son|son)"),
     ("się","","[bp]","(Sem|sem)"),
     ("się","","","(Sen|sen)"),
     ("sie","","[bcdgkpstwzż]","(SF|sF|se)"),
     ("sie","","","(Se|se)"),
     ("sio","","","(So|so)"),
     ("siu","","","(Su|sju)"),
     ("si","","","(Si|sI)"),
     ("ś","","","(S|s)"),

     ("zia","","[bcdgkpstwzż]","(ZB|zB|zja)"),
     ("zia","","","(Za|zja)"),
     ("zią","","[bp]","(Zom|zom)"),
     ("zią","","","(Zon|zon)"),
     ("zię","","[bp]","(Zem|zem)"),
     ("zię","","","(Zen|zen)"),
     ("zie","","[bcdgkpstwzż]","(ZF|zF)"),
     ("zie","","","(Ze|ze)"),
     ("zio","","","(Zo|zo)"),
     ("ziu","","","(Zu|zju)"),
     ("zi","","","(Zi|zI)"),

     ("że","","[bcdgkpstwzż]","(Ze|ZF)"),
     ("że","","[bcdgkpstwzż]","(Ze|ZF|ze|zF)"),
     ("że","","","Ze"),
     ("źe","","","(Ze|ze)"),
     ("ży","","","Zi"),
     ("źi","","","(Zi|zi)"),
     ("ż","","","Z"),
     ("ź","","","(Z|z)"),

     ("rze","t","","(Se|re)"),
     ("rze","","","(Ze|re|rZe)"),
     ("rzy","t","","(Si|ri)"),
     ("rzy","","","(Zi|ri|rZi)"),
     ("rz","t","","(S|r)"),
     ("rz","","","(Z|r|rZ)"),

     ("lio","","","(lo|le)"),
     ("ł","","","l"),
     ("ń","","","n"),
     ("qu","","","k"),
     ("s","","s",""),

     # VOWELS
     ("ó","","","(u|o)"),
     ("ą","","[bp]","om"),
     ("ę","","[bp]","em"),
     ("ą","","","on"),
     ("ę","","","en"),

     ("ije","","","je"),
     ("yje","","","je"),
     ("iie","","","je"),
     ("yie","","","je"),
     ("iye","","","je"),
     ("yye","","","je"),

     ("ij","","[aou]","j"),
     ("yj","","[aou]","j"),
     ("ii","","[aou]","j"),
     ("yi","","[aou]","j"),
     ("iy","","[aou]","j"),
     ("yy","","[aou]","j"),

     ("rie","","","rje"),
     ("die","","","dje"),
     ("tie","","","tje"),
     ("ie","","[bcdgkpstwzż]","F"),
     ("ie","","","e"),

     ("aue","","","aue"),
     ("au","","","au"),

     ("ei","","","aj"),
     ("ey","","","aj"),
     ("ej","","","aj"),

     ("ai","","","aj"),
     ("ay","","","aj"),
     ("aj","","","aj"),

     ("i","[aeou]","","j"),
     ("y","[aeou]","","j"),
     ("i","","[aou]","j"),
     ("y","","[aeou]","j"),

     ("a","","[bcdgkpstwzż]","B"),
     ("e","","[bcdgkpstwzż]","(E|F)"),
     ("o","","[bcćdgklłmnńrsśtwzźż]","P"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","ts"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","(h|x)"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","I"),
     ("z","","","z"),

     )

# gen/rulesportuguese.php

_gen_rules_portuguese = (
     ("kh","","","x"), # foreign
     ("ch","","","S"),
     ("ss","","","s"),
     ("sc","","[ei]","s"),
     ("sç","","[aou]","s"),
     ("ç","","","s"),
     ("c","","[ei]","s"),
     #  ("c","","[aou]","(k|C)"),

     ("s","^","","s"),
     ("s","[aáuiíoóeéêy]","[aáuiíoóeéêy]","z"),
     ("s","","[dglmnrv]","(Z|S)"), # Z is Brazil

     ("z","","$","(Z|s|S)"), # s and S in Brazil
     ("z","","[bdgv]","(Z|z)"), # Z in Brazil
     ("z","","[ptckf]","(s|S|z)"), # s and S in Brazil

     ("gu","","[eiu]","g"),
     ("gu","","[ao]","gv"),
     ("g","","[ei]","Z"),
     ("qu","","[eiu]","k"),
     ("qu","","[ao]","kv"),

     ("uo","","","(vo|o|u)"),
     ("u","","[aei]","v"),

     ("lh","","","l"),
     ("nh","","","nj"),
     ("h","[bdgt]","",""), # translit. from Arabic
     ("h","","$",""), # foreign

     ("ex","","[aáuiíoóeéêy]","(ez|eS|eks)"), # ez in Brazil
     ("ex","","[cs]","e"),

     ("y","[aáuiíoóeéê]","","j"),
     ("y","","[aeiíou]","j"),
     ("m","","[bcdfglnprstv]","(m|n)"), # maybe to add a rule for m/n before a consonant that disappears [preceeding vowel becomes nasalized]
     ("m","","$","(m|n)"), # maybe to add a rule for final m/n that disappears [preceeding vowel becomes nasalized]

     ("ão","","","(au|an|on)"),
     ("ãe","","","(aj|an)"),
     ("ãi","","","(aj|an)"),
     ("õe","","","(oj|on)"),
     ("i","[aáuoóeéê]","","j"),
     ("i","","[aeou]","j"),

     ("â","","","a"),
     ("à","","","a"),
     ("á","","","a"),
     ("ã","","","(a|an|on)"),
     ("é","","","e"),
     ("ê","","","e"),
     ("í","","","i"),
     ("ô","","","o"),
     ("ó","","","o"),
     ("õ","","","(o|on)"),
     ("ú","","","u"),
     ("ü","","","u"),

     ("aue","","","aue"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","(e|i)"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("j","","","Z"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","(o|u)"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","S"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","(S|ks)"),
     ("y","","","i"),
     ("z","","","z"),

     )

# gen/rulesromanian.php

# GENERAL
_gen_rules_romanian = (
     ("ce","","","tSe"),
     ("ci","","","(tSi|tS)"),
     ("ch","","[ei]","k"),
     ("ch","","","x"), # foreign

     ("gi","","","(dZi|dZ)"),
     ("g","","[ei]","dZ"),
     ("gh","","","g"),

     ("i","[aeou]","","j"),
     ("i","","[aeou]","j"),
     ("ţ","","","ts"),
     ("ş","","","S"),
     ("qu","","","k"),

     ("î","","","i"),
     ("ea","","","ja"),
     ("ă","","","(e|a)"),
     ("aue","","","aue"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","(x|h)"),
     ("i","","","I"),
     ("j","","","Z"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","z"),

     )

# gen/rulesrussian.php

#GENERAL
_gen_rules_russian = (
     # CONVERTING FEMININE TO MASCULINE
     ("yna","","$","(in|ina)"),
     ("ina","","$","(in|ina)"),
     ("liova","","$","(lof|lef)"),
     ("lova","","$","(lof|lef|lova)"),
     ("ova","","$","(of|ova)"),
     ("eva","","$","(ef|ova)"),
     ("aia","","$","(aja|i)"),
     ("aja","","$","(aja|i)"),
     ("aya","","$","(aja|i)"),

     #SPECIAL CONSONANTS
     ("tsya","","","tsa"),
     ("tsyu","","","tsu"),
     ("tsia","","","tsa"),
     ("tsie","","","tse"),
     ("tsio","","","tso"),
     ("tsye","","","tse"),
     ("tsyo","","","tso"),
     ("tsiu","","","tsu"),
     ("sie","","","se"),
     ("sio","","","so"),
     ("zie","","","ze"),
     ("zio","","","zo"),
     ("sye","","","se"),
     ("syo","","","so"),
     ("zye","","","ze"),
     ("zyo","","","zo"),

     ("ger","","$","ger"),
     ("gen","","$","gen"),
     ("gin","","$","gin"),
     ("gg","","","g"),
     ("g","[jaeoiuy]","[aeoiu]","g"),
     ("g","","[aeoiu]","(g|h)"),

     ("kh","","","x"),
     ("ch","","","(tS|x)"),
     ("sch","","","(StS|S)"),
     ("ssh","","","S"),
     ("sh","","","S"),
     ("zh","","","Z"),
     ("tz","","$","ts"),
     ("tz","","","(ts|tz)"),
     ("c","","[iey]","s"),
     ("qu","","","(kv|k)"),
     ("s","","s",""),

     #SPECIAL VOWELS
     ("lya","","","la"),
     ("lyu","","","lu"),
     ("lia","","","la"), # not in DJSRE
     ("liu","","","lu"),  # not in DJSRE
     ("lja","","","la"), # not in DJSRE
     ("lju","","","lu"),  # not in DJSRE
     ("le","","","(lo|lE)"), #not in DJSRE
     ("lyo","","","(lo|le)"), #not in DJSRE
     ("lio","","","(lo|le)"),

     ("ije","","","je"),
     ("ie","","","je"),
     ("iye","","","je"),
     ("iie","","","je"),
     ("yje","","","je"),
     ("ye","","","je"),
     ("yye","","","je"),
     ("yie","","","je"),

     ("ij","","[aou]","j"),
     ("iy","","[aou]","j"),
     ("ii","","[aou]","j"),
     ("yj","","[aou]","j"),
     ("yy","","[aou]","j"),
     ("yi","","[aou]","j"),

     ("io","","","(jo|e)"),
     ("i","","[au]","j"),
     ("i","[aeou]","","j"),
     ("yo","","","(jo|e)"),
     ("y","","[au]","j"),
     ("y","[aeiou]","","j"),

     ("ii","","$","i"),
     ("iy","","$","i"),
     ("yy","","$","i"),
     ("yi","","$","i"),
     ("yj","","$","i"),
     ("ij","","$","i"),

     ("e","^","","(je|E)"),
     ("ee","","","(aje|i)"),
     ("e","[aou]","","je"),
     ("oo","","","(oo|u)"),
     ("'","","",""),
     ('"',"","",""),

     ("aue","","","aue"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","I"),
     ("z","","","z"),

     )

# gen/rulesspanish.php

# GENERAL
_gen_rules_spanish = (

     # Includes both Spanish (Castillian) & Catalan

     # CONSONANTS
     ("ñ","","","(n|nj)"),
     ("ny","","","nj"), # Catalan
     ("ç","","","s"), # Catalan

     ("ig","[aeiou]","","(tS|ig)"), # tS is Catalan
     ("ix","[aeiou]","","S"), # Catalan
     ("tx","","","tS"), # Catalan
     ("tj","","$","tS"), # Catalan
     ("tj","","","dZ"), # Catalan
     ("tg","","","(tg|dZ)"), # dZ is Catalan
     ("ch","","","(tS|dZ)"), # dZ is typical for Argentina
     ("bh","","","b"), # translit. from Arabic
     ("h","[dgt]","",""), # translit. from Arabic
     ("h","","$",""), # foreign
     #("ll","","","(l|Z)"), # Z is typical for Argentina, only Ashkenazic
     ("m","","[bpvf]","(m|n)"),
     ("c","","[ei]","s"),
     #  ("c","","[aou]","(k|C)"),
     ("gu","","[ei]","(g|gv)"), # "gv" because "u" can actually be "ü"
     ("g","","[ei]","(x|g|dZ)"),  # "g" only for foreign words; dZ is Catalan
     ("qu","","","k"),

     ("uo","","","(vo|o)"),
     ("u","","[aei]","v"),

     # SPECIAL VOWELS
     ("ü","","","v"),
     ("á","","","a"),
     ("é","","","e"),
     ("í","","","i"),
     ("ó","","","o"),
     ("ú","","","u"),
     ("à","","","a"),  # Catalan
     ("è","","","e"), # Catalan
     ("ò","","","o"),  # Catalan

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","B"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("j","","","(x|Z)"), # Z is Catalan
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","V"),
     ("w","","","v"), # foreign words
     ("x","","","(ks|gz|S)"), # ks is Spanish, all are Catalan
     ("y","","","(i|j)"),
     ("z","","","(z|s)"), # as "c" befoire "e" or "i", in Spain it is like unvoiced English "th"

     )

# gen/rulesturkish.php

_gen_rules_turkish = (
     ("ç","","","tS"),
     ("ğ","","",""), # to show that previous vowel is long
     ("ş","","","S"),
     ("ü","","","Q"),
     ("ö","","","Y"),
     ("ı","","","(e|i|)"), # as "e" in English "label"

     ("a","","","a"),
     ("b","","","b"),
     ("c","","","dZ"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("j","","","Z"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"), # foreign words
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"), # foreign words
     ("x","","","ks"), # foreign words
     ("y","","","j"),
     ("z","","","z"),

     )

# sep/approxany.php

# SEPHARDIC
_sep_approx_any = (

     ("E","","",""), # Final French "e"

     )

# sep/approxcommon.php
#Sephardic

_sep_approx_common = (
     ("bens", "^", "", "(binz|s)"),
     ("benS", "^", "", "(binz|s)"),
     ("ben", "^", "", "(bin|)"),

     ("abens", "^", "", "(abinz|binz|s)"),
     ("abenS", "^", "", "(abinz|binz|s)"),
     ("aben", "^", "", "(abin|bin|)"),

     ("els", "^", "", "(ilz|alz|s)"),
     ("elS", "^", "", "(ilz|alz|s)"),
     ("el", "^", "", "(il|al|)"),
     ("als", "^", "", "(alz|s)"),
     ("alS", "^", "", "(alz|s)"),
     ("al", "^", "", "(al|)"),

     # ("dels", "^", "", "(dilz|s)"),
     # ("delS", "^", "", "(dilz|s)"),
     ("del", "^", "", "(dil|)"),
     ("dela", "^", "", "(dila|)"),
     # ("delo", "^", "", "(dila|)"),
     ("da", "^", "", "(da|)"),
     ("de", "^", "", "(di|)"),
     # ("des", "^", "", "(dis|dAs|)"),
     # ("di", "^", "", "(di|)"),
     # ("dos", "^", "", "(das|dus|)"),

     ("oa","","","(va|a|D)"),
     ("oe","","","(vi|D)"),
     ("ae","","","D"),

     #  ("s", "", "$", "(s|)"), # Attia(s)
     #  ("C", "", "", "s"),  # "c" could actually be "ç"

     ("n","","[bp]","m"),

     ("h","","","(|h|f)"), # sound "h" (absent) can be expressed via /x/, Cojab in Spanish = Kohab ; Hakim = Fakim
     ("x","","","h"),

     # DIPHTHONGS ARE APPROXIMATELY equivalent
     ("aja","^","","(Da|ia)"),
     ("aje","^","","(Di|Da|i|ia)"),
     ("aji","^","","(Di|i)"),
     ("ajo","^","","(Du|Da|iu|ia)"),
     ("aju","^","","(Du|iu)"),

     ("aj","","","D"),
     ("ej","","","D"),
     ("oj","","","D"),
     ("uj","","","D"),
     ("au","","","D"),
     ("eu","","","D"),
     ("ou","","","D"),

     ("a", "^", "", "(a|)"),  # Arabic

     ("ja","^","","ia"),
     ("je","^","","i"),
     ("jo","^","","(iu|ia)"),
     ("ju","^","","iu"),

     ("ja","","","a"),
     ("je","","","i"),
     ("ji","","","i"),
     ("jo","","","u"),
     ("ju","","","u"),

     ("j","","","i"),

     # CONSONANTS {z & Z & dZ; s & S} are approximately interchangeable
     ("s", "", "[rmnl]", "z"),
     ("S", "", "[rmnl]", "z"),
     ("s", "[rmnl]", "", "z"),
     ("S", "[rmnl]", "", "z"),

     ("dS", "", "$", "S"),
     ("dZ", "", "$", "S"),
     ("Z", "", "$", "S"),
     ("S", "", "$", "(S|s)"),
     ("z", "", "$", "(S|s)"),

     ("S", "", "", "s"),
     ("dZ", "", "", "z"),
     ("Z", "", "", "z"),

     ("i","","$","(i|)"), # often in Arabic
     ("e", "", "", "i"),

     ("o", "", "$", "(a|u)"),
     ("o", "", "", "u"),

     # special character to deal correctly in Hebrew match
     ("B","","","b"),
     ("V","","","v"),

     # Arabic
     ("p", "^", "", "b"),

     )

# sep/approxfrench.php
_sep_approx_french = (

     )

# sep/approxhebrew.php
_sep_approx_hebrew = (

     )

# sep/approxitalian.php

# this file uses the same rules as approxfrench.php

# sep/approxportuguese.php
# this file uses the same rules as approxfrench.php

# sep/approxspanish.php
# this file uses the same rules as approxfrench.php

# sep/exactany.php
_sep_exact_any = (

     ("E","","","e"), # final French "e"

     )

# sep/exactapproxcommon.php
# Sephardic
_sep_exact_approx_common = (
     ("h","","$",""),

     # VOICED - UNVOICED CONSONANTS
     ("b","","[fktSs]","p"),
     ("b","","p",""),
     ("b","","$","p"),
     ("p","","[vgdZz]","b"),
     ("p","","b",""),

     ("v","","[pktSs]","f"),
     ("v","","f",""),
     ("v","","$","f"),
     ("f","","[vbgdZz]","v"),
     ("f","","v",""),

     ("g","","[pftSs]","k"),
     ("g","","k",""),
     ("g","","$","k"),
     ("k","","[vbdZz]","g"),
     ("k","","g",""),

     ("d","","[pfkSs]","t"),
     ("d","","t",""),
     ("d","","$","t"),
     ("t","","[vbgZz]","d"),
     ("t","","d",""),

     ("s","","dZ",""),
     ("s","","tS",""),

     ("z","","[pfkSt]","s"),
     ("z","","[sSzZ]",""),
     ("s","","[sSzZ]",""),
     ("Z","","[sSzZ]",""),
     ("S","","[sSzZ]",""),

     # SIMPLIFICATION OF CONSONANT CLUSTERS
     ("nm","","","m"),

     # DOUBLE --> SINGLE
     ("ji","^","","i"),

     ("a","","a",""),
     ("b","","b",""),
     ("d","","d",""),
     ("e","","e",""),
     ("f","","f",""),
     ("g","","g",""),
     ("i","","i",""),
     ("k","","k",""),
     ("l","","l",""),
     ("m","","m",""),
     ("n","","n",""),
     ("o","","o",""),
     ("p","","p",""),
     ("r","","r",""),
     ("t","","t",""),
     ("u","","u",""),
     ("v","","v",""),
     ("z","","z","")

     # do not put name of file here since it always gets merged into another file
     )

# sep/exactcommon.php
# Sephardic

_sep_exact_common = (
     ("h","","",""),
     #("C","","","k"),  # c that can actually be ç

     # VOICED - UNVOICED CONSONANTS
     ("s","[^t]","[bgZd]","z"),
     ("Z","","[pfkst]","S"),
     ("Z","","$","S"),
     ("S","","[bgzd]","Z"),
     ("z","","$","s"),

     #special character to deal correctly in Hebrew match
     ("B","","","b"),
     ("V","","","v"),

     )

# sep/exactfrench.php
# Sephardic
_sep_exact_french = (

     )

# sep/exacthebrew.php
_sep_exact_hebrew = (

     )

# sep/exactitalian.php
# Sephardic
_sep_exact_italian = (

     )

# sep/exactportuguese.php
# Sephardic
_sep_exact_portuguese = (

     )

# sep/exactspanish.php
# Sephardic
_sep_exact_spanish = (

     )

# sep/hebrewcommon.php
#Sephardic

_sep_hebrew_common = (

     ("E","","",""),  # final French "e": only in Sephardic

     ("ts","","","C"), # for not confusion Gutes [=guts] and Guts [=guc]
     ("tS","","","C"), # same reason
     ("S","","","s"),
     ("p","","","f"),
     ("b","^","","b"),
     ("b","","","(b|v)"),

     ("ja","","","i"),
     ("je","","","i"),
     ("aj","","","i"),
     ("j","","","i"),

     ("a","^","","1"),
     ("e","^","","1"),
     ("a","","$","1"),
     ("e","","$","1"),

     ("a","","",""),
     ("e","","",""),

     ("oj","^","","(u|vi)"),
     ("uj","^","","(u|vi)"),

     ("oj","","","u"),
     ("uj","","","u"),

     ("ou","^","","(u|v|1)"),
     ("o","^","","(u|v|1)"),
     ("u","^","","(u|v|1)"),

     ("o","","$","(u|1)"),
     ("u","","$","(u|1)"),

     ("ou","","","u"),
     ("o","","","u"),

     ("VV","","","u"), # alef/ayin + vov from ruleshebrew
     ("L","^","","1"), # alef/ayin from  ruleshebrew
     ("L","","$","1"), # alef/ayin from  ruleshebrew
     ("L","","",""), # alef/ayin from  ruleshebrew
     ("WW","^","","(vi|u)"), # vav-yod from  ruleshebrew
     ("WW","","","u"), # vav-yod from  ruleshebrew
     ("W","^","","(u|v)"), # vav from  ruleshebrew
     ("W","","","u"), # vav from  ruleshebrew

     # ("g","","","(g|Z)"),
     # ("z","","","(z|Z)"),
     # ("d","","","(d|dZ)"),

     ("T","","","t"),   # tet from  ruleshebrew

     # ("k","","","(k|x)"),
     # ("x","","","(k|x)"),
     ("K","","","k"), # kof and initial kaf from ruleshebrew
     ("X","","","x"), # khet and final kaf from ruleshebrew

     # special for Spanish initial B/V
     ("B","","","v"),
     ("V","","","b"),

     ("H","^","","(x|1)"),
     ("H","","$","(x|1)"),
     ("H","","","(x|)"),
     ("h","^","","1"),
     ("h","","",""),

     )

# sep/lang.php
# SEPHARDIC

_sep_language_rules = (

     # 1. following are rules to accept the language
     # 1.1 Special letter combinations
     ('/eau/', l_french, True),
     ('/ou/', l_french, True),
     ('/gni/', l_italian+l_french, True),
     ('/tx/', l_spanish, True),
     ('/tj/', l_spanish, True),
     ('/gy/', l_french, True),
     ('/guy/', l_french, True),

     ("/sh/", l_spanish+l_portuguese, True), # English, but no sign for /sh/ in these languages

     ('/lh/', l_portuguese, True),
     ('/nh/', l_portuguese, True),
     ('/ny/', l_spanish, True),

     ('/gue/', l_spanish + l_french, True),
     ('/gui/', l_spanish + l_french, True),
     ('/gia/', l_italian, True),
     ('/gie/', l_italian, True),
     ('/gio/', l_italian, True),
     ('/giu/', l_italian, True),

     # 1.2 special characters
     ('/ñ/', l_spanish, True),
     ('/â/', l_portuguese + l_french, True),
     ('/á/', l_portuguese + l_spanish, True),
     ('/à/', l_portuguese, True),
     ('/ã/', l_portuguese, True),
     ('/ê/', l_french + l_portuguese, True),
     ('/í/', l_portuguese + l_spanish, True),
     ('/î/', l_french, True),
     ('/ô/', l_french + l_portuguese, True),
     ('/õ/', l_portuguese, True),
     ('/ò/', l_italian + l_spanish, True),
     ('/ú/', l_portuguese + l_spanish, True),
     ('/ù/', l_french, True),
     ('/ü/', l_portuguese + l_spanish, True),

     # Hebrew
     ("/א/", l_hebrew, True),
     ("/ב/", l_hebrew, True),
     ("/ג/", l_hebrew, True),
     ("/ד/", l_hebrew, True),
     ("/ה/", l_hebrew, True),
     ("/ו/", l_hebrew, True),
     ("/ז/", l_hebrew, True),
     ("/ח/", l_hebrew, True),
     ("/ט/", l_hebrew, True),
     ("/י/", l_hebrew, True),
     ("/כ/", l_hebrew, True),
     ("/ל/", l_hebrew, True),
     ("/מ/", l_hebrew, True),
     ("/נ/", l_hebrew, True),
     ("/ס/", l_hebrew, True),
     ("/ע/", l_hebrew, True),
     ("/פ/", l_hebrew, True),
     ("/צ/", l_hebrew, True),
     ("/ק/", l_hebrew, True),
     ("/ר/", l_hebrew, True),
     ("/ש/", l_hebrew, True),
     ("/ת/", l_hebrew, True),

     # 2. following are rules to reject the language

     # Every Latin character word has at least one Latin vowel
     ("/a/", l_hebrew, False),
     ("/o/", l_hebrew, False),
     ("/e/", l_hebrew, False),
     ("/i/",  l_hebrew, False),
     ("/y/", l_hebrew, False),
     ("/u/", l_hebrew, False),

     ("/kh/", l_spanish, False),
     ("/gua/", l_italian, False),
     ("/guo/", l_italian, False),
     ("/ç/", l_italian, False),
     ("/cha/", l_italian, False),
     ("/cho/", l_italian, False),
     ("/chu/", l_italian, False),
     ("/j/", l_italian, False),
     ("/dj/", l_spanish, False),
     ('/sce/', l_french, False),
     ('/sci/', l_french, False),
     ('/ó/', l_french, False),
     ('/è/', l_portuguese, False)

     )

# sep/languagenames.php
_sep_languages = ("any", "french", "hebrew", "italian", "portuguese", "spanish")

# sep/rulesany.php
# SEPHARDIC: INCORPORATES Portuguese + Italian + Spanish(+Catalan) + French
_sep_rules_any = (
     # CONSONANTS
     ("ph","","","f"), # foreign
     ("sh","","","S"), # foreign
     ("kh","","","x"), # foreign

     ("gli","","","(gli|l[l_italian])"),
     ("gni","","","(gni|ni[l_italian+l_french])"),
     ("gn","","[aeou]","(n[l_italian+l_french]|nj[l_italian+l_french]|gn)"),
     ("gh","","","g"), # It + translit. from Arabic
     ("dh","","","d"), # translit. from Arabic
     ("bh","","","b"), # translit. from Arabic
     ("th","","","t"), # translit. from Arabic
     ("lh","","","l"), # Port
     ("nh","","","nj"), # Port

     ("ig","[aeiou]","","(ig|tS[l_spanish])"),
     ("ix","[aeiou]","","S"), # Sp
     ("tx","","","tS"), # Sp
     ("tj","","$","tS"), # Sp
     ("tj","","","dZ"), # Sp
     ("tg","","","(tg|dZ[l_spanish])"),

     ("gi","","[aeou]","dZ"), # italian
     ("g","","y","Z"), # french
     ("gg","","[ei]","(gZ[l_portuguese+l_french]|dZ[l_italian+l_spanish]|x[l_spanish])"),
     ("g","","[ei]","(Z[l_portuguese+l_french]|dZ[l_italian+l_spanish]|x[l_spanish])"),

     ("guy","","","gi"),
     ("gue","","$","(k[l_french]|ge)"),
     ("gu","","[ei]","(g|gv)"),     # not It
     ("gu","","[ao]","gv"),  # not It

     ("ñ","","","(n|nj)"),
     ("ny","","","nj"),

     ("sc","","[ei]","(s|S[l_italian])"),
     ("sç","","[aeiou]","s"), # not It
     ("ss","","","s"),
     ("ç","","","s"),   # not It

     ("ch","","[ei]","(k[l_italian]|S[l_portuguese+l_french]|tS[l_spanish]|dZ[l_spanish])"),
     ("ch","","","(S|tS[l_spanish]|dZ[l_spanish])"),

     ("ci","","[aeou]","(tS[l_italian]|si)"),
     ("cc","","[eiyéèê]","(tS[l_italian]|ks[l_portuguese+l_french+l_spanish])"),
     ("c","","[eiyéèê]","(tS[l_italian]|s[l_portuguese+l_french+l_spanish])"),
     #("c","","[aou]","(k|C[l_portuguese+l_spanish])"), # "C" means that the actual letter could be "ç" (cedille omitted)

     ("s","^","","s"),
     ("s","[aáuiíoóeéêy]","[aáuiíoóeéêy]","(s[l_spanish]|z[l_portuguese+l_french+l_italian])"),
     ("s","","[dglmnrv]","(z|Z[l_portuguese])"),

     ("z","","$","(s|ts[l_italian]|S[l_portuguese])"), # ts It, s/S/Z Port, s in Sp, z Fr
     ("z","","[bdgv]","(z|dz[l_italian]|Z[l_portuguese])"), # dz It, Z/z Port, z Sp & Fr
     ("z","","[ptckf]","(s|ts[l_italian]|S[l_portuguese])"), # ts It, s/S/z Port, z/s Sp
     ("z","","","(z|dz[l_italian]|ts[l_italian]|s[l_spanish])"), # ts/dz It, z Port & Fr, z/s Sp

     ("que","","$","(k[l_french]|ke)"),
     ("qu","","[eiu]","k"),
     ("qu","","[ao]","(kv|k)"), # k is It

     ("ex","","[aáuiíoóeéêy]","(ez[l_portuguese]|eS[l_portuguese]|eks|egz)"),
     ("ex","","[cs]","(e[l_portuguese]|ek)"),

     ("m","","[cdglnrst]","(m|n[l_portuguese])"),
     ("m","","[bfpv]","(m|n[l_portuguese+l_spanish])"),
     ("m","","$","(m|n[l_portuguese])"),

     ("b","^","","(b|V[l_spanish])"),
     ("v","^","","(v|B[l_spanish])"),

     # VOWELS
     ("eau","","","o"), # Fr

     ("ouh","","[aioe]","(v[l_french]|uh)"),
     ("uh","","[aioe]","(v|uh)"),
     ("ou","","[aioe]","v"), # french
     ("uo","","","(vo|o)"),
     ("u","","[aie]","v"),

     ("i","[aáuoóeéê]","","j"),
     ("i","","[aeou]","j"),
     ("y","[aáuiíoóeéê]","","j"),
     ("y","","[aeiíou]","j"),
     ("e","","$","(e|E[l_french])"),

     ("ão","","","(au|an)"), # Port
     ("ãe","","","(aj|an)"), # Port
     ("ãi","","","(aj|an)"), # Port
     ("õe","","","(oj|on)"), # Port
     ("où","","","u"), # Fr
     ("ou","","","(ou|u[l_french])"),

     ("â","","","a"), # Port & Fr
     ("à","","","a"), # Port
     ("á","","","a"), # Port & Sp
     ("ã","","","(a|an)"), # Port
     ("é","","","e"),
     ("ê","","","e"), # Port & Fr
     ("è","","","e"), # Sp & Fr & It
     ("í","","","i"), # Port & Sp
     ("î","","","i"), # Fr
     ("ô","","","o"), # Port & Fr
     ("ó","","","o"), # Port & Sp & It
     ("õ","","","(o|on)"), # Port
     ("ò","","","o"),  # Sp & It
     ("ú","","","u"), # Port & Sp
     ("ü","","","u"), # Port & Sp

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","(b|v[l_spanish])"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("j","","","(x[l_spanish]|Z)"), # not It
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","(s|S[l_portuguese])"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","(v|b[l_spanish])"),
     ("w","","","v"),    # foreign
     ("x","","","(ks|gz|S[l_portuguese+l_spanish])"),   # S/ks Port & Sp, gz Sp, It only ks
     ("y","","","i"),
     ("z","","","z"),

     )

# sep/rulesfrench.php

# Sephardic
_sep_rules_french = (

     # CONSONANTS
     ("kh","","","x"), # foreign
     ("ph","","","f"),

     ("ç","","","s"),
     ("x","","","ks"),
     ("ch","","","S"),
     ("c","","[eiyéèê]","s"),
     ("c","","","k"),
     ("gn","","","(n|gn)"),
     ("g","","[eiy]","Z"),
     ("gue","","$","k"),
     ("gu","","[eiy]","g"),
     #("aill","","e","aj"), # non Jewish
     #("ll","","e","(l|j)"), # non Jewish
     ("que","","$","k"),
     ("qu","","","k"),
     ("q","","","k"),
     ("s","[aeiouyéèê]","[aeiouyéèê]","z"),
     ("h","[bdgt]","",""), # translit from Arabic
     ("h","","$",""), # foreign
     ("j","","","Z"),
     ("w","","","v"),
     ("ouh","","[aioe]","(v|uh)"),
     ("ou","","[aeio]","v"),
     ("uo","","","(vo|o)"),
     ("u","","[aeio]","v"),

     # VOWELS
     ("aue","","","aue"),
     ("eau","","","o"),
     #("au","","","(o|au)"), # non Jewish
     ("ai","","","aj"), # [e] is non Jewish
     ("ay","","","aj"), # [e] is non Jewish
     ("é","","","e"),
     ("ê","","","e"),
     ("è","","","e"),
     ("à","","","a"),
     ("â","","","a"),
     ("où","","","u"),
     ("ou","","","u"),
     ("oi","","","oj"), # [ua] is non Jewish
     ("ei","","","ej"), # [e] is non Jewish, in Ashk should be aj
     ("ey","","","ej"), # [e] non Jewish, in Ashk should be aj
     #("eu","","","(e|o)"), # non Jewish
     ("y","[ou]","","j"),
     ("e","","$","(e|)"),
     ("i","","[aou]","j"),
     ("y","","[aoeu]","j"),
     ("y","","","i"),

     # TRIVIAL
     ("a","","","a"),
     ("b","","","b"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("z","","","z"),

     )

# sep/ruleshebrew.php

# Sephardic
_sep_rules_hebrew = (

     ("אי","","","i"),
     ("עי","","","i"),
     ("עו","","","VV"),
     ("או","","","VV"),

     ("ג׳","","","Z"),
     ("ד׳","","","dZ"),

     ("א","","","L"),
     ("ב","","","b"),
     ("ג","","","g"),
     ("ד","","","d"),

     ("ה","^","","1"),
     ("ה","","$","1"),
     ("ה","","",""),

     ("וו","","","V"),
     ("וי","","","WW"),
     ("ו","","","W"),
     ("ז","","","z"),
     ("ח","","","X"),
     ("ט","","","T"),
     ("יי","","","i"),
     ("י","","","i"),
     ("ך","","","X"),
     ("כ","^","","K"),
     ("כ","","","k"),
     ("ל","","","l"),
     ("ם","","","m"),
     ("מ","","","m"),
     ("ן","","","n"),
     ("נ","","","n"),
     ("ס","","","s"),
     ("ע","","","L"),
     ("ף","","","f"),
     ("פ","","","f"),
     ("ץ","","","C"),
     ("צ","","","C"),
     ("ק","","","K"),
     ("ר","","","r"),
     ("ש","","","s"),
     ("ת","","","T"),   # Special for Sephardim

     )

# sep/rulesitalian.php

_sep_rules_italian = (
     ("kh","","","x"), # foreign

     ("gli","","","(l|gli)"),
     ("gn","","[aeou]","(n|nj|gn)"),
     ("gni","","","(ni|gni)"),

     ("gi","","[aeou]","dZ"),
     ("gg","","[ei]","dZ"),
     ("g","","[ei]","dZ"),
     ("h","[bdgt]","","g"), # gh is It; others from Arabic translit

     ("ci","","[aeou]","tS"),
     ("ch","","[ei]","k"),
     ("sc","","[ei]","S"),
     ("cc","","[ei]","tS"),
     ("c","","[ei]","tS"),
     ("s","[aeiou]","[aeiou]","z"),

     ("i","[aeou]","","j"),
     ("i","","[aeou]","j"),
     ("y","[aeou]","","j"), # foreign
     ("y","","[aeou]","j"), # foreign

     ("qu","","","k"),
     ("uo","","","(vo|o)"),
     ("u","","[aei]","v"),

     ("č","","","e"),
     ("é","","","e"),
     ("ň","","","o"),
     ("ó","","","o"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("j","","","(Z|dZ|j)"), # foreign
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),    # foreign
     ("x","","","ks"),    # foreign
     ("y","","","i"),    # foreign
     ("z","","","(ts|dz)"),

     )

# sep/rulesportuguese.php

_sep_rules_portuguese = (
     ("kh","","","x"), # foreign
     ("ch","","","S"),
     ("ss","","","s"),
     ("sc","","[ei]","s"),
     ("sç","","[aou]","s"),
     ("ç","","","s"),
     ("c","","[ei]","s"),
     #  ("c","","[aou]","(k|C)"),

     ("s","^","","s"),
     ("s","[aáuiíoóeéêy]","[aáuiíoóeéêy]","z"),
     ("s","","[dglmnrv]","(Z|S)"), # Z is Brazil

     ("z","","$","(Z|s|S)"), # s and S in Brazil
     ("z","","[bdgv]","(Z|z)"), # Z in Brazil
     ("z","","[ptckf]","(s|S|z)"), # s and S in Brazil

     ("gu","","[eiu]","g"),
     ("gu","","[ao]","gv"),
     ("g","","[ei]","Z"),
     ("qu","","[eiu]","k"),
     ("qu","","[ao]","kv"),

     ("uo","","","(vo|o|u)"),
     ("u","","[aei]","v"),

     ("lh","","","l"),
     ("nh","","","nj"),
     ("h","[bdgt]","",""), # translit. from Arabic

     ("ex","","[aáuiíoóeéêy]","(ez|eS|eks)"), # ez in Brazil
     ("ex","","[cs]","e"),

     ("y","[aáuiíoóeéê]","","j"),
     ("y","","[aeiíou]","j"),
     ("m","","[bcdfglnprstv]","(m|n)"), # maybe to add a rule for m/n before a consonant that disappears [preceeding vowel becomes nasalized]
     ("m","","$","(m|n)"), # maybe to add a rule for final m/n that disappears [preceeding vowel becomes nasalized]

     ("ão","","","(au|an|on)"),
     ("ãe","","","(aj|an)"),
     ("ãi","","","(aj|an)"),
     ("õe","","","(oj|on)"),
     ("i","[aáuoóeéê]","","j"),
     ("i","","[aeou]","j"),

     ("â","","","a"),
     ("à","","","a"),
     ("á","","","a"),
     ("ã","","","(a|an|on)"),
     ("é","","","e"),
     ("ê","","","e"),
     ("í","","","i"),
     ("ô","","","o"),
     ("ó","","","o"),
     ("õ","","","(o|on)"),
     ("ú","","","u"),
     ("ü","","","u"),

     ("aue","","","aue"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","(e|i)"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("j","","","Z"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","(o|u)"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","S"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","(S|ks)"),
     ("y","","","i"),
     ("z","","","z"),

     )

# sep/rulesspanish.php

#Sephardic
_sep_rules_spanish = (

     # Includes both Spanish (Castillian) & Catalan

     # CONSONANTS
     ("ñ","","","(n|nj)"),
     ("ny","","","nj"), # Catalan
     ("ç","","","s"), # Catalan

     ("ig","[aeiou]","","(tS|ig)"), # tS is Catalan
     ("ix","[aeiou]","","S"), # Catalan
     ("tx","","","tS"), # Catalan
     ("tj","","$","tS"), # Catalan
     ("tj","","","dZ"), # Catalan
     ("tg","","","(tg|dZ)"), # dZ is Catalan
     ("ch","","","(tS|dZ)"), # dZ is typical for Argentina
     ("bh","","","b"), # translit. from Arabic
     ("h","[dgt]","",""), # translit. from Arabic

     ("j","","","(x|Z)"), # Z is Catalan
     ("x","","","(ks|gz|S)"), # ks is Spanish, all are Catalan

     #("ll","","","(l|Z)"), # Z is typical for Argentina, only Ashkenazic
     ("w","","","v"), # foreign words

     ("v","^","","(B|v)"),
     ("b","^","","(b|V)"),
     ("v","","","(b|v)"),
     ("b","","","(b|v)"),
     ("m","","[bpvf]","(m|n)"),

     ("c","","[ei]","s"),
     #  ("c","","[aou]","(k|C)"),
     ("c","","","k"),

     ("z","","","(z|s)"), # as "c" befoire "e" or "i", in Spain it is like unvoiced English "th"

     ("gu","","[ei]","(g|gv)"), # "gv" because "u" can actually be "ü"
     ("g","","[ei]","(x|g|dZ)"),  # "g" only for foreign words; dZ is Catalan

     ("qu","","","k"),
     ("q","","","k"),

     ("uo","","","(vo|o)"),
     ("u","","[aei]","v"),

     #  ("y","","","(i|j|S|Z)"), # S or Z are peculiar to South America; only Ashkenazic
     ("y","","","(i|j)"),

     # VOWELS
     ("ü","","","v"),
     ("á","","","a"),
     ("é","","","e"),
     ("í","","","i"),
     ("ó","","","o"),
     ("ú","","","u"),
     ("à","","","a"),  # Catalan
     ("è","","","e"), # Catalan
     ("ò","","","o"),  # Catalan

     # TRIVIAL
     ("a","","","a"),
     ("d","","","d"),
     ("e","","","e"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","i"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),

     )

# ash/approxany.php

# ASHKENAZIC

# A, E, I, O, P, U should create variants, but a, e, i, o, u should not create any new variant
# Q = ü ; Y = ä = ö
# H = initial "H" in German/English
_ash_approx_any = (

     # CONSONANTS
     ("b","","","(b|v[l_spanish])"),
     ("J", "", "", "z"), # Argentina Spanish: "ll" = /Z/, but approximately /Z/ = /z/

     # VOWELS
     # "ALL" DIPHTHONGS are interchangeable BETWEEN THEM and with monophthongs of which they are composed ("D" means "diphthong")
     #  {a,o} are totally interchangeable if non-stressed; in German "a/o" can actually be from "ä/ö" (that are equivalent to "e")
     #  {i,e} are interchangeable if non-stressed, while in German "u" can actually be from "ü" (that is equivalent to "i")

     ("aiB","","[bp]","(D|Dm)"),
     ("AiB","","[bp]","(D|Dm)"),
     ("oiB","","[bp]","(D|Dm)"),
     ("OiB","","[bp]","(D|Dm)"),
     ("uiB","","[bp]","(D|Dm)"),
     ("UiB","","[bp]","(D|Dm)"),
     ("eiB","","[bp]","(D|Dm)"),
     ("EiB","","[bp]","(D|Dm)"),
     ("iiB","","[bp]","(D|Dm)"),
     ("IiB","","[bp]","(D|Dm)"),

     ("aiB","","[dgkstvz]","(D|Dn)"),
     ("AiB","","[dgkstvz]","(D|Dn)"),
     ("oiB","","[dgkstvz]","(D|Dn)"),
     ("OiB","","[dgkstvz]","(D|Dn)"),
     ("uiB","","[dgkstvz]","(D|Dn)"),
     ("UiB","","[dgkstvz]","(D|Dn)"),
     ("eiB","","[dgkstvz]","(D|Dn)"),
     ("EiB","","[dgkstvz]","(D|Dn)"),
     ("iiB","","[dgkstvz]","(D|Dn)"),
     ("IiB","","[dgkstvz]","(D|Dn)"),

     ("B","","[bp]","(o|om[l_polish]|im[l_polish])"),
     ("B","","[dgkstvz]","(a|o|on[l_polish]|in[l_polish])"),
     ("B", "", "", "(a|o)"),

     ("aiF","","[bp]","(D|Dm)"),
     ("AiF","","[bp]","(D|Dm)"),
     ("oiF","","[bp]","(D|Dm)"),
     ("OiF","","[bp]","(D|Dm)"),
     ("uiF","","[bp]","(D|Dm)"),
     ("UiF","","[bp]","(D|Dm)"),
     ("eiF","","[bp]","(D|Dm)"),
     ("EiF","","[bp]","(D|Dm)"),
     ("iiF","","[bp]","(D|Dm)"),
     ("IiF","","[bp]","(D|Dm)"),

     ("aiF","","[dgkstvz]","(D|Dn)"),
     ("AiF","","[dgkstvz]","(D|Dn)"),
     ("oiF","","[dgkstvz]","(D|Dn)"),
     ("OiF","","[dgkstvz]","(D|Dn)"),
     ("uiF","","[dgkstvz]","(D|Dn)"),
     ("UiF","","[dgkstvz]","(D|Dn)"),
     ("eiF","","[dgkstvz]","(D|Dn)"),
     ("EiF","","[dgkstvz]","(D|Dn)"),
     ("iiF","","[dgkstvz]","(D|Dn)"),
     ("IiF","","[dgkstvz]","(D|Dn)"),

     ("F","","[bp]","(i|im[l_polish]|om[l_polish])"),
     ("F","","[dgkstvz]","(i|in[l_polish]|on[l_polish])"),
     ("F", "", "", "i"),

     ("P", "", "", "(o|u)"),

     ("I", "[aeiouAEIBFOUQY]", "", "i"),
     ("I","","[^aeiouAEBFIOU]e","(Q[l_german]|i|D[l_english])"),  # "line"
     ("I", "", "$", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk[l_german])"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts[l_german])"),
     ("Its", "", "$", "its"),
     ("I", "", "", "(Q[l_german]|i)"),

     ("lE","[bdfgkmnprsStvzZ]","$","(li|il[l_english])"),  # Apple < Appel
     ("lE","[bdfgkmnprsStvzZ]","","(li|il[l_english]|lY[l_german])"),  # Applebaum < Appelbaum

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),

     ("ai","","","(D|a|i)"),
     ("Ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("Oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),
     ("Ui","","","(D|u|i)"),
     ("ei","","","(D|i)"),
     ("Ei","","","(D|i)"),

     ("iA","","$","(ia|io)"),
     ("iA","","","(ia|io|iY[l_german])"),
     ("A","","[^aeiouAEBFIOU]e","(a|o|Y[l_german]|D[l_english])"), # "plane"

     ("E","i[^aeiouAEIOU]","","(i|Y[l_german]|[l_english])"), # Wineberg (vineberg/vajneberg) --> vajnberg
     ("E","a[^aeiouAEIOU]","","(i|Y[l_german]|[l_english])"), #  Shaneberg (shaneberg/shejneberg) --> shejnberg

     ("e", "", "[fklmnprstv]$", "i"),
     ("e", "", "ts$", "i"),
     ("e", "", "$", "i"),
     ("e", "[DaoiuAOIUQY]", "", "i"),
     ("e", "", "[aoAOQY]", "i"),
     ("e", "", "", "(i|Y[l_german])"),

     ("E", "", "[fklmnprst]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "", "$", "i"),
     ("E", "[DaoiuAOIUQY]", "", "i"),
     ("E", "", "[aoAOQY]", "i"),
     ("E", "", "", "(i|Y[l_german])"),

     ("a", "", "", "(a|o)"),

     ("O", "", "[fklmnprstv]$", "o"),
     ("O", "", "ts$", "o"),
     ("O", "", "$", "o"),
     ("O", "[oeiuQY]", "", "o"),
     ("O", "", "", "(o|Y[l_german])"),

     ("A", "", "[fklmnprst]$", "(a|o)"),
     ("A", "", "ts$", "(a|o)"),
     ("A", "", "$", "(a|o)"),
     ("A", "[oeiuQY]", "", "(a|o)"),
     ("A", "", "", "(a|o|Y[l_german])"),

     ("U", "", "$", "u"),
     ("U", "[DoiuQY]", "", "u"),
     ("U", "", "[^k]$", "u"),
     ("Uk", "[lr]", "$", "(uk|Qk[l_german])"),
     ("Uk", "", "$", "uk"),

     ("sUts", "", "$", "(suts|sQts[l_german])"),
     ("Uts", "", "$", "uts"),
     ("U", "", "", "(u|Q[l_german])"),

     )

# ash/approxcommon.php
# Ashkenazic

_ash_approx_common = (

     # REGRESSIVE ASSIMILATION OF CONSONANTS
     ("n","","[bp]","m"),

     # PECULIARITY OF "h"
     ("h","","",""),
     ("H","","","(x|)"),

     # POLISH OGONEK IMPOSSIBLE
     ("F", "", "[bdgkpstvzZ]h", "e"),
     ("F", "", "[bdgkpstvzZ]x", "e"),
     ("B", "", "[bdgkpstvzZ]h", "a"),
     ("B", "", "[bdgkpstvzZ]x", "a"),

     # "e" and "i" ARE TO BE OMITTED BEFORE (SYLLABIC) n & l: Halperin=Halpern; Frankel = Frankl, Finkelstein = Finklstein
     ("e", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
     ("i", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
     ("E", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
     ("I", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
     ("F", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
     ("Q", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
     ("Y", "[bdfgklmnprsStvzZ]", "[ln]$", ""),

     ("e", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
     ("i", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
     ("E", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
     ("I", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
     ("F", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
     ("Q", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
     ("Y", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),

     ("lEs","","","(lEs|lz)"),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)
     ("lE","[bdfgkmnprStvzZ]","","(lE|l)"),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)

     # SIMPLIFICATION: (TRIPHTHONGS & DIPHTHONGS) -> ONE GENERIC DIPHTHONG "D"
     ("aue","","","D"),
     ("oue","","","D"),

     ("AvE","","","(D|AvE)"),
     ("Ave","","","(D|Ave)"),
     ("avE","","","(D|avE)"),
     ("ave","","","(D|ave)"),

     ("OvE","","","(D|OvE)"),
     ("Ove","","","(D|Ove)"),
     ("ovE","","","(D|ovE)"),
     ("ove","","","(D|ove)"),

     ("ea","","","(D|ea)"),
     ("EA","","","(D|EA)"),
     ("Ea","","","(D|Ea)"),
     ("eA","","","(D|eA)"),

     ("aji","","","D"),
     ("ajI","","","D"),
     ("aje","","","D"),
     ("ajE","","","D"),

     ("Aji","","","D"),
     ("AjI","","","D"),
     ("Aje","","","D"),
     ("AjE","","","D"),

     ("oji","","","D"),
     ("ojI","","","D"),
     ("oje","","","D"),
     ("ojE","","","D"),

     ("Oji","","","D"),
     ("OjI","","","D"),
     ("Oje","","","D"),
     ("OjE","","","D"),

     ("eji","","","D"),
     ("ejI","","","D"),
     ("eje","","","D"),
     ("ejE","","","D"),

     ("Eji","","","D"),
     ("EjI","","","D"),
     ("Eje","","","D"),
     ("EjE","","","D"),

     ("uji","","","D"),
     ("ujI","","","D"),
     ("uje","","","D"),
     ("ujE","","","D"),

     ("Uji","","","D"),
     ("UjI","","","D"),
     ("Uje","","","D"),
     ("UjE","","","D"),

     ("iji","","","D"),
     ("ijI","","","D"),
     ("ije","","","D"),
     ("ijE","","","D"),

     ("Iji","","","D"),
     ("IjI","","","D"),
     ("Ije","","","D"),
     ("IjE","","","D"),

     ("aja","","","D"),
     ("ajA","","","D"),
     ("ajo","","","D"),
     ("ajO","","","D"),
     ("aju","","","D"),
     ("ajU","","","D"),

     ("Aja","","","D"),
     ("AjA","","","D"),
     ("Ajo","","","D"),
     ("AjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("oja","","","D"),
     ("ojA","","","D"),
     ("ojo","","","D"),
     ("ojO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("Oja","","","D"),
     ("OjA","","","D"),
     ("Ojo","","","D"),
     ("OjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("eja","","","D"),
     ("ejA","","","D"),
     ("ejo","","","D"),
     ("ejO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("Eja","","","D"),
     ("EjA","","","D"),
     ("Ejo","","","D"),
     ("EjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("uja","","","D"),
     ("ujA","","","D"),
     ("ujo","","","D"),
     ("ujO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("Uja","","","D"),
     ("UjA","","","D"),
     ("Ujo","","","D"),
     ("UjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("ija","","","D"),
     ("ijA","","","D"),
     ("ijo","","","D"),
     ("ijO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("Ija","","","D"),
     ("IjA","","","D"),
     ("Ijo","","","D"),
     ("IjO","","","D"),
     ("Aju","","","D"),
     ("AjU","","","D"),

     ("j","","","i"),

     # lander = lender = l채nder
     ("lYndEr","","$","lYnder"),
     ("lander","","$","lYnder"),
     ("lAndEr","","$","lYnder"),
     ("lAnder","","$","lYnder"),
     ("landEr","","$","lYnder"),
     ("lender","","$","lYnder"),
     ("lEndEr","","$","lYnder"),
     ("lendEr","","$","lYnder"),
     ("lEnder","","$","lYnder"),

     # CONSONANTS {z & Z; s & S} are approximately interchangeable
     ("s", "", "[rmnl]", "z"),
     ("S", "", "[rmnl]", "z"),
     ("s", "[rmnl]", "", "z"),
     ("S", "[rmnl]", "", "z"),

     ("dS", "", "$", "S"),
     ("dZ", "", "$", "S"),
     ("Z", "", "$", "S"),
     ("S", "", "$", "(S|s)"),
     ("z", "", "$", "(S|s)"),

     ("S", "", "", "s"),
     ("dZ", "", "", "z"),
     ("Z", "", "", "z"),

     )

# ash/approxcyrillic.php
# this file uses the same rules as approxrussian.php

# ash/approxenglish.php

_ash_approx_english = (

     # VOWELS
     ("I","","[^aEIeiou]e","(Q|i|D)"), # like in "five"
     ("I", "", "$", "i"),
     ("I", "[aEIeiou]", "", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "", "", "(i|Q)"),

     ("lE","[bdfgkmnprsStvzZ]","","(il|li|lY)"),  # Applebaum < Appelbaum

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),

     ("E","D[^aeiEIou]","","(i|)"), # Weinberg, Shaneberg (shaneberg/shejneberg) --> shejnberg
     ("e","D[^aeiEIou]","","(i|)"),

     ("e", "", "", "i"),
     ("E", "", "[fklmnprsStv]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "[DaoiEuQY]", "", "i"),
     ("E", "", "[aoQY]", "i"),
     ("E", "", "", "(Y|i)"),

     ("a", "", "", "(a|o)"),

     )

# ash/approxfrench.php
# THE LINES BELOW WERE VALID FOR ASHKENAZIM

_ash_approx_french = (

     ("I", "", "$", "i"),
     ("I", "[aEIeiou]", "", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "", "", "(i|Q)"),

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),

     ("a", "", "", "(a|o)"),
     ("e", "", "", "i"),

     ("E", "", "[fklmnprsStv]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "[aoiuQ]", "", "i"),
     ("E", "", "[aoQ]", "i"),
     ("E", "", "", "(Y|i)"),

     )

# ash/approxgerman.php

_ash_approx_german = (

     ("I", "", "$", "i"),
     ("I", "[aeiAEIOUouQY]", "", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "", "", "(Q|i)"),

     ("AU","","","(D|a|u)"),
     ("aU","","","(D|a|u)"),
     ("Au","","","(D|a|u)"),
     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("OU","","","(D|o|u)"),
     ("oU","","","(D|o|u)"),
     ("Ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("Ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("Oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),
     ("Ui","","","(D|u|i)"),

     ("e", "", "", "i"),

     ("E", "", "[fklmnprst]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "", "$", "i"),
     ("E", "[DaoAOUiuQY]", "", "i"),
     ("E", "", "[aoAOQY]", "i"),
     ("E", "", "", "(Y|i)"),

     ("O", "", "$", "o"),
     ("O", "", "[fklmnprst]$", "o"),
     ("O", "", "ts$", "o"),
     ("O", "[aoAOUeiuQY]", "", "o"),
     ("O", "", "", "(o|Y)"),

     ("a", "", "", "(a|o)"),

     ("A", "", "$", "(a|o)"),
     ("A", "", "[fklmnprst]$", "(a|o)"),
     ("A", "", "ts$", "(a|o)"),
     ("A", "[aoeOUiuQY]", "", "(a|o)"),
     ("A", "", "", "(a|o|Y)"),

     ("U", "", "$", "u"),
     ("U", "[DaoiuUQY]", "", "u"),
     ("U", "", "[^k]$", "u"),
     ("Uk", "[lr]", "$", "(uk|Qk)"),
     ("Uk", "", "$", "uk"),
     ("sUts", "", "$", "(suts|sQts)"),
     ("Uts", "", "$", "uts"),
     ("U", "", "", "(u|Q)"),

     )

# ash/approxhebrew.php

_ash_approx_hebrew = (
     )

# ash/approxhungarian.php

# this file uses the same rules as approxfrench.php

# ash/approxpolish.php
_ash_approx_polish = (

     ("aiB","","[bp]","(D|Dm)"),
     ("oiB","","[bp]","(D|Dm)"),
     ("uiB","","[bp]","(D|Dm)"),
     ("eiB","","[bp]","(D|Dm)"),
     ("EiB","","[bp]","(D|Dm)"),
     ("iiB","","[bp]","(D|Dm)"),
     ("IiB","","[bp]","(D|Dm)"),

     ("aiB","","[dgkstvz]","(D|Dn)"),
     ("oiB","","[dgkstvz]","(D|Dn)"),
     ("uiB","","[dgkstvz]","(D|Dn)"),
     ("eiB","","[dgkstvz]","(D|Dn)"),
     ("EiB","","[dgkstvz]","(D|Dn)"),
     ("iiB","","[dgkstvz]","(D|Dn)"),
     ("IiB","","[dgkstvz]","(D|Dn)"),

     ("B","","[bp]","(o|om|im)"),
     ("B","","[dgkstvz]","(o|on|in)"),
     ("B", "", "", "o"),

     ("aiF","","[bp]","(D|Dm)"),
     ("oiF","","[bp]","(D|Dm)"),
     ("uiF","","[bp]","(D|Dm)"),
     ("eiF","","[bp]","(D|Dm)"),
     ("EiF","","[bp]","(D|Dm)"),
     ("iiF","","[bp]","(D|Dm)"),
     ("IiF","","[bp]","(D|Dm)"),

     ("aiF","","[dgkstvz]","(D|Dn)"),
     ("oiF","","[dgkstvz]","(D|Dn)"),
     ("uiF","","[dgkstvz]","(D|Dn)"),
     ("eiF","","[dgkstvz]","(D|Dn)"),
     ("EiF","","[dgkstvz]","(D|Dn)"),
     ("iiF","","[dgkstvz]","(D|Dn)"),
     ("IiF","","[dgkstvz]","(D|Dn)"),

     ("F","","[bp]","(i|im|om)"),
     ("F","","[dgkstvz]","(i|in|on)"),
     ("F", "", "", "i"),

     ("P", "", "", "(o|u)"),

     ("I", "", "$", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "[aeiAEBFIou]", "", "i"),
     ("I", "", "", "(i|Q)"),

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),

     ("a", "", "", "(a|o)"),
     ("e", "", "", "i"),

     ("E", "", "[fklmnprst]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "", "$", "i"),
     ("E", "[DaoiuQ]", "", "i"),
     ("E", "", "[aoQ]", "i"),
     ("E", "", "", "(Y|i)"),

     )

# ash/approxromanian.php

# this file uses the same rules as approxpolish.php

# ash/approxrussian.php

_ash_approx_russian = (

     # VOWELS
     ("I", "", "$", "i"),
     ("I", "", "[^k]$", "i"),
     ("Ik", "[lr]", "$", "(ik|Qk)"),
     ("Ik", "", "$", "ik"),
     ("sIts", "", "$", "(sits|sQts)"),
     ("Its", "", "$", "its"),
     ("I", "[aeiEIou]", "", "i"),
     ("I", "", "", "(i|Q)"),

     ("au","","","(D|a|u)"),
     ("ou","","","(D|o|u)"),
     ("ai","","","(D|a|i)"),
     ("oi","","","(D|o|i)"),
     ("ui","","","(D|u|i)"),

     ("om","","[bp]","(om|im)"),
     ("on","","[dgkstvz]","(on|in)"),
     ("em","","[bp]","(im|om)"),
     ("en","","[dgkstvz]","(in|on)"),
     ("Em","","[bp]","(im|Ym|om)"),
     ("En","","[dgkstvz]","(in|Yn|on)"),

     ("a", "", "", "(a|o)"),
     ("e", "", "", "i"),

     ("E", "", "[fklmnprsStv]$", "i"),
     ("E", "", "ts$", "i"),
     ("E", "[DaoiuQ]", "", "i"),
     ("E", "", "[aoQ]", "i"),
     ("E", "", "", "(Y|i)"),

     )

# ash/approxspanish.php

# this file uses the same rules as approxfrench.php

# ash/exactany.php
# These rules are applied after the word has been transliterated into the phonetic alphabet
# These rules are substitution rules within the phonetic character space rather than mapping rules

# format of each entry rule in the table
#   (pattern, left context, right context, phonetic)
# where
#   pattern is a sequence of characters that might appear after a word has been transliterated into phonetic alphabet
#   left context is the context that precedes the pattern
#   right context is the context that follows the pattern
#   phonetic is the result that this rule generates
#
# note that both left context and right context can be regular expressions
# ex: left context of ^ would mean start of word
#     right context of $ means end of word
#
# match occurs if all of the following are true:
#   portion of word matches the pattern
#   that portion satisfies the context

# A, E, I, O, P, U should create variants, but a, e, i, o, u should not create any new variant
# Q = ü ; Y = ä = ö

_ash_exact_any = (
     ("A", "", "", "a"),
     ("B", "", "", "a"),

     ("E", "", "", "e"),
     ("F", "", "", "e"),

     ("I", "", "", "i"),
     ("O", "", "", "o"),
     ("P", "", "", "o"),
     ("U", "", "", "u"),

     ("J", "", "", "l"),

     )

# ash/exactapproxcommon.php
# Ashkenazic
_ash_exact_approx_common = (

     ("h","","$",""),
     # VOICED - UNVOICED CONSONANTS
     ("b","","[fktSs]","p"),
     ("b","","p",""),
     ("b","","$","p"),
     ("p","","[gdZz]","b"),
     ("p","","b",""),

     ("v","","[pktSs]","f"),
     ("v","","f",""),
     ("v","","$","f"),
     ("f","","[bgdZz]","v"),
     ("f","","v",""),

     ("g","","[pftSs]","k"),
     ("g","","k",""),
     ("g","","$","k"),
     ("k","","[bdZz]","g"),
     ("k","","g",""),

     ("d","","[pfkSs]","t"),
     ("d","","t",""),
     ("d","","$","t"),
     ("t","","[bgZz]","d"),
     ("t","","d",""),

     ("s","","dZ",""),
     ("s","","tS",""),

     ("z","","[pfkSt]","s"),
     ("z","","[sSzZ]",""),
     ("s","","[sSzZ]",""),
     ("Z","","[sSzZ]",""),
     ("S","","[sSzZ]",""),

     # SIMPLIFICATION OF CONSONANT CLUSTERS

     ("jnm","","","jm"),

     # DOUBLE --> SINGLE

     ("ji","^","","i"),
     ("jI","^","","I"),

     ("a","","[aAB]",""),
     ("a","[AB]","",""),
     ("A","","A",""),
     ("B","","B",""),

     ("b","","b",""),
     ("d","","d",""),
     ("f","","f",""),
     ("g","","g",""),
     ("k","","k",""),
     ("l","","l",""),
     ("m","","m",""),
     ("n","","n",""),
     ("p","","p",""),
     ("r","","r",""),
     ("t","","t",""),
     ("v","","v",""),
     ("z","","z","")

     # do not put name of file here since it always gets merged into another file
     )

# ash/exactcommon.php
# Ashkenazic

_ash_exact_common = (
     ("H","","","h"),

     # VOICED - UNVOICED CONSONANTS

     ("s","[^t]","[bgZd]","z"),
     ("Z","","[pfkst]","S"),
     ("Z","","$","S"),
     ("S","","[bgzd]","Z"),
     ("z","","$","s"),

     ("ji","[aAoOeEiIuU]","","j"),
     ("jI","[aAoOeEiIuU]","","j"),
     ("je","[aAoOeEiIuU]","","j"),
     ("jE","[aAoOeEiIuU]","","j"),

     )

# ash/exactcyrillic.php
# this file uses the same rules as exactrussian.php

# ash/exactenglish.php
# this file uses the same rules as exactrussian.php

# ash/exactfrench.php
#   For Ashkenazic searches:
#this file uses the same rules as exactrussian.php

# ash/exactgerman.php
# this file uses the same rules as exactany.php

# ash/exacthebrew.php
_ash_exact_hebrew = (
     )

# ash/exacthungarian.php
# this file uses the same rules as exactrussian.php

# ash/exactpolish.php
_ash_exact_polish = (

     ("B", "", "", "a"),
     ("F", "", "", "e"),
     ("P", "", "", "o"),

     ("E", "", "", "e"),
     ("I", "", "", "i"),

     )

# ash/exactromanian.php
# this file uses the same rules as exactrussian.php

# ash/exactrussian.php
_ash_exact_russian = (

     ("E", "", "", "e"),
     ("I", "", "", "i"),

     )

# ash/exactspanish.php
#this Ashkenazic file uses the same rules as exactrussian.php

# ash/hebrewcommon.php
#Ashkenazic

_ash_hebrew_common = (

     ("ts","","","C"), # for not confusion Gutes [=guts] and Guts [=guc]
     ("tS","","","C"), # same reason
     ("S","","","s"),
     ("p","","","f"),
     ("b","^","","b"),
     ("b","","","(b|v)"),
     ("J", "", "", "l"),

     ("ja","","","i"),
     ("jA","","","i"),
     ("jB","","","i"),
     ("je","","","i"),
     ("jE","","","i"),
     ("jF","","","i"),
     ("aj","","","i"),
     ("Aj","","","i"),
     ("Bj","","","i"),
     ("Fj","","","i"),
     ("I","","","i"),
     ("Q","","","i"),
     ("j","","","i"),

     ("a","^","","1"),
     ("A","^","","1"),
     ("B","^","","1"),
     ("e","^","","1"),
     ("E","^","","1"),
     ("F","^","","1"),
     ("Y","^","","1"),

     ("a","","$","1"),
     ("A","","$","1"),
     ("B","","$","1"),
     ("e","","$","1"),
     ("E","","$","1"),
     ("F","","$","1"),
     ("Y","","$","1"),

     ("a","","",""),
     ("A","","",""),
     ("B","","",""),
     ("e","","",""),
     ("E","","",""),
     ("F","","",""),
     ("Y","","",""),

     ("oj","^","","(u|vi)"),
     ("Oj","^","","(u|vi)"),
     ("uj","^","","(u|vi)"),
     ("Uj","^","","(u|vi)"),

     ("oj","","","u"),
     ("Oj","","","u"),
     ("uj","","","u"),
     ("Uj","","","u"),

     ("ou","^","","(u|v|1)"),
     ("o","^","","(u|v|1)"),
     ("O","^","","(u|v|1)"),
     ("P","^","","(u|v|1)"),
     ("U","^","","(u|v|1)"),
     ("u","^","","(u|v|1)"),

     ("o","","$","(u|1)"),
     ("O","","$","(u|1)"),
     ("P","","$","(u|1)"),
     ("u","","$","(u|1)"),
     ("U","","$","(u|1)"),

     ("ou","","","u"),
     ("o","","","u"),
     ("O","","","u"),
     ("P","","","u"),
     ("U","","","u"),

     ("VV","","","u"), # alef/ayin + vov from ruleshebrew
     ("V","","","v"), # tsvey-vov from ruleshebrew;; only Ashkenazic
     ("L","^","","1"), # alef/ayin from ruleshebrew
     ("L","","$","1"), # alef/ayin from ruleshebrew
     ("L","","",""), # alef/ayin from ruleshebrew
     ("WW","^","","(vi|u)"), # vav-yod from ruleshebrew
     ("WW","","","u"), # vav-yod from ruleshebrew
     ("W","^","","(u|v)"), # vav from ruleshebrew
     ("W","","","u"), # vav from ruleshebrew

     # ("g","","","(g|Z)"),
     # ("z","","","(z|Z)"),
     # ("d","","","(d|dZ)"),

     ("TB","^","","t"), # tav from ruleshebrew; only Ashkenazic
     ("TB","","$","s"), # tav from ruleshebrew; only Ashkenazic
     ("TB","","","(t|s)"), # tav from ruleshebrew; only Ashkenazic
     ("T","","","t"),   # tet from ruleshebrew

     # ("k","","","(k|x)"),
     # ("x","","","(k|x)"),
     ("K","","","k"), # kof and initial kaf from ruleshebrew
     ("X","","","x"), # khet and final kaf from ruleshebrew

     ("H","^","","(x|1)"),
     ("H","","$","(x|1)"),
     ("H","","","(x|)"),
     ("h","^","","1"),
     ("h","","",""),

     )

# ash/lang.php
# ASHKENAZIC

# format of entries in $languageRules table is
#    (pattern, language, Acceptance)
# where
#    pattern is a regular expression
#      e.g., ^ means start of word, $ Means End Of Word, [^ei] means anything but e or i, etc.
#    language is one or more of the languages defined above separated by + signs
#    acceptance is true or false
# meaning is:
#    if "pattern" matches and acceptance is true, name is in one of the languages indicated and no others
#    if "pattern" matches and acceptance is false, name is not in any of the languages indicated

_ash_language_rules = (

     # 1. following are rules to accept the language
     # 1.1 Special letter combinations
     ('/zh/', l_polish+l_russian+l_german+l_english, True),
     ('/eau/', l_french, True),
     ('/[aoeiuäöü]h/', l_german, True),
     ('/^vogel/', l_german, True),
     ('/vogel$/', l_german, True),
     ('/witz/', l_german, True),
     ('/tz$/', l_german+l_russian+l_english, True),
     ('/^tz/', l_russian+l_english, True),
     ('/güe/', l_spanish, True),
     ('/güi/', l_spanish, True),
     ('/ghe/', l_romanian, True),
     ('/ghi/', l_romanian, True),
     ('/vici$/', l_romanian, True),
     ('/schi$/', l_romanian, True),
     ('/chsch/', l_german, True),
     ('/tsch/', l_german, True),
     ('/ssch/', l_german, True),
     ('/sch$/', l_german+l_russian, True),
     ('/^sch/', l_german+l_russian, True),
     ('/^rz/', l_polish, True),
     ('/rz$/', l_polish+l_german, True),
     ('/[^aoeiuäöü]rz/', l_polish, True),
     ('/rz[^aoeiuäöü]/', l_polish, True),
     ('/cki$/', l_polish, True),
     ('/ska$/', l_polish, True),
     ('/cka$/', l_polish, True),
     ('/ue/', l_german+l_russian, True),
     ('/ae/', l_german+l_russian+l_english, True),
     ('/oe/', l_german+l_french+l_russian+l_english, True),
     ('/th$/', l_german, True),
     ('/^th/', l_german, True),
     ('/th[^aoeiu]/', l_german, True),
     ('/mann/', l_german, True),
     ('/cz/', l_polish, True),
     ('/cy/', l_polish, True),
     ('/niew/', l_polish, True),
     ('/stein/', l_german, True),
     ('/heim$/', l_german, True),
     ('/heimer$/', l_german, True),
     ('/ii$/', l_russian, True),
     ('/iy$/', l_russian, True),
     ('/yy$/', l_russian, True),
     ('/yi$/', l_russian, True),
     ('/yj$/', l_russian, True),
     ('/ij$/', l_russian, True),
     ('/gaus$/', l_russian, True),
     ('/gauz$/', l_russian, True),
     ('/gauz$/', l_russian, True),
     ('/goltz$/', l_russian, True),
     ("/gol'tz$/", l_russian, True),
     ('/golts$/', l_russian, True),
     ("/gol'ts$/", l_russian, True),
     ('/^goltz/', l_russian, True),
     ("/^gol'tz/", l_russian, True),
     ('/^golts/', l_russian, True),
     ("/^gol'ts/", l_russian, True),
     ('/gendler$/', l_russian, True),
     ('/gejmer$/', l_russian, True),
     ('/gejm$/', l_russian, True),
     ('/geimer$/', l_russian, True),
     ('/geim$/', l_russian, True),
     ('/geymer/', l_russian, True),
     ('/geym$/', l_russian, True),
     ('/gof$/', l_russian, True),
     ('/thal/', l_german, True),
     ('/zweig/', l_german, True),
     ('/ck$/', l_german + l_english, True),
     ('/c$/', l_polish + l_romanian + l_hungarian, True),
     ('/sz/', l_polish + l_hungarian, True),
     ('/gue/', l_spanish + l_french, True),
     ('/gui/', l_spanish + l_french, True),
     ('/guy/', l_french, True),
     ('/cs$/', l_hungarian, True),
     ('/^cs/', l_hungarian, True),
     ('/dzs/', l_hungarian, True),
     ('/zs$/', l_hungarian, True),
     ('/^zs/', l_hungarian, True),
     ('/^wl/', l_polish, True),
     ('/^wr/', l_polish+l_english+l_german, True),

     ('/gy$/', l_hungarian, True),
     ("/gy[aeou]/", l_hungarian, True),
     ("/gy/", l_hungarian + l_russian, True),
     ("/ly/", l_hungarian + l_russian + l_polish, True),
     ("/ny/", l_hungarian + l_russian + l_polish, True),
     ("/ty/", l_hungarian + l_russian + l_polish, True),

     # 1.2 special characters
     ('/â/', l_romanian + l_french, True),
     ('/ă/', l_romanian, True),
     ('/à/', l_french, True),
     ('/ä/', l_german, True),
     ('/á/', l_hungarian + l_spanish, True),
     ('/ą/', l_polish, True),
     ('/ć/', l_polish, True),
     ('/ç/', l_french, True),
     ('/ę/', l_polish, True),
     ('/é/', l_french + l_hungarian + l_spanish, True),
     ('/è/', l_french, True),
     ('/ê/', l_french, True),
     ('/í/', l_hungarian + l_spanish, True),
     ('/î/', l_romanian + l_french, True),
     ('/ł/', l_polish, True),
     ('/ń/', l_polish, True),
     ('/ñ/', l_spanish, True),
     ('/ó/', l_polish + l_hungarian + l_spanish, True),
     ('/ö/', l_german + l_hungarian, True),
     ('/õ/', l_hungarian, True),
     ('/ş/', l_romanian, True),
     ('/ś/', l_polish, True),
     ('/ţ/', l_romanian, True),
     ('/ü/', l_german + l_hungarian, True),
     ('/ù/', l_french, True),
     ('/ű/', l_hungarian, True),
     ('/ú/', l_hungarian + l_spanish, True),
     ('/ź/', l_polish, True),
     ('/ż/', l_polish, True),

     ('/ß/', l_german, True),

     # Every Cyrillic word has at least one Cyrillic vowel (аёеоиуыэюя)
     ('/а/', l_cyrillic, True),
     ('/ё/', l_cyrillic, True),
     ('/о/', l_cyrillic, True),
     ('/е/', l_cyrillic, True),
     ('/и/', l_cyrillic, True),
     ('/у/', l_cyrillic, True),
     ('/ы/', l_cyrillic, True),
     ('/э/', l_cyrillic, True),
     ('/ю/', l_cyrillic, True),
     ('/я/', l_cyrillic, True),

     # Hebrew
     ("/א/", l_hebrew, True),
     ("/ב/", l_hebrew, True),
     ("/ג/", l_hebrew, True),
     ("/ד/", l_hebrew, True),
     ("/ה/", l_hebrew, True),
     ("/ו/", l_hebrew, True),
     ("/ז/", l_hebrew, True),
     ("/ח/", l_hebrew, True),
     ("/ט/", l_hebrew, True),
     ("/י/", l_hebrew, True),
     ("/כ/", l_hebrew, True),
     ("/ל/", l_hebrew, True),
     ("/מ/", l_hebrew, True),
     ("/נ/", l_hebrew, True),
     ("/ס/", l_hebrew, True),
     ("/ע/", l_hebrew, True),
     ("/פ/", l_hebrew, True),
     ("/צ/", l_hebrew, True),
     ("/ק/", l_hebrew, True),
     ("/ר/", l_hebrew, True),
     ("/ש/", l_hebrew, True),
     ("/ת/", l_hebrew, True),

     # 2. following are rules to reject the language

     # Every Latin character word has at least one Latin vowel
     ("/a/", l_cyrillic + l_hebrew, False),
     ("/o/", l_cyrillic + l_hebrew, False),
     ("/e/", l_cyrillic + l_hebrew, False),
     ("/i/", l_cyrillic + l_hebrew, False),
     ("/y/", l_cyrillic + l_hebrew + l_romanian, False),
     ("/u/", l_cyrillic + l_hebrew, False),

     ("/v[^aoeiuäüö]/", l_german, False), # in german, "v" can be found before a vowel only
     ("/y[^aoeiu]/", l_german, False),  # in german, "y" usually appears only in the last position; sometimes before a vowel
     ("/c[^aohk]/", l_german, False),
     ("/dzi/", l_german+l_english+l_french, False),
     ("/ou/", l_german, False),
     ("/aj/", l_german + l_english+l_french, False),
     ("/ej/", l_german + l_english+l_french, False),
     ("/oj/", l_german + l_english+l_french, False),
     ("/uj/", l_german + l_english+l_french, False),
     ("/k/", l_romanian, False),
     ("/v/", l_polish, False),
     ("/ky/", l_polish, False),
     ("/eu/", l_russian + l_polish, False),
     ("/w/", l_french + l_romanian + l_spanish + l_hungarian + l_russian, False),
     ("/kie/", l_french + l_spanish, False),
     ("/gie/", l_french + l_romanian + l_spanish, False),
     ("/q/", l_hungarian + l_polish + l_russian + l_romanian, False),
     ('/sch/', l_hungarian + l_polish + l_french + l_spanish, False),
     ('/^h/', l_russian, False)

     )

# ash/languagenames.php
_ash_languages = ("any", "cyrillic", "english", "french", "german", "hebrew",
     "hungarian", "polish", "romanian", "russian", "spanish")

# ash/rulesany.php
#ASHKENAZIC
_ash_rules_any = (

     # CONVERTING FEMININE TO MASCULINE
     ("yna","","$","(in[l_russian]|ina)"),
     ("ina","","$","(in[l_russian]|ina)"),
     ("liova","","$","(lof[l_russian]|lef[l_russian]|lova)"),
     ("lova","","$","(lof[l_russian]|lef[l_russian]|lova)"),
     ("ova","","$","(of[l_russian]|ova)"),
     ("eva","","$","(ef[l_russian]|eva)"),
     ("aia","","$","(aja|i[l_russian])"),
     ("aja","","$","(aja|i[l_russian])"),
     ("aya","","$","(aja|i[l_russian])"),

     ("lowa","","$","(lova|lof[l_polish]|l[l_polish]|el[l_polish])"),
     ("kowa","","$","(kova|kof[l_polish]|k[l_polish]|ek[l_polish])"),
     ("owa","","$","(ova|of[l_polish]|)"),
     ("lowna","","$","(lovna|levna|l[l_polish]|el[l_polish])"),
     ("kowna","","$","(kovna|k[l_polish]|ek[l_polish])"),
     ("owna","","$","(ovna|[l_polish])"),
     ("lówna","","$","(l|el[l_polish])"),  # polish
     ("kówna","","$","(k|ek[l_polish])"),  # polish
     ("ówna","","$",""),   # polish

     ("a","","$","(a|i[l_polish])"),

     # CONSONANTS  (integrated: German, Polish, Russian, Romanian and English)

     ("rh","^","","r"),
     ("ssch","","","S"),
     ("chsch","","","xS"),
     ("tsch","","","tS"),

     ("sch","","[ei]","(sk[l_romanian]|S|StS[l_russian])"), # german
     ("sch","","","(S|StS[l_russian])"), # german

     ("ssh","","","S"),

     ("sh","","[äöü]","sh"), # german
     ("sh","","[aeiou]","(S[l_russian+l_english]|sh)"),
     ("sh","","","S"), # russian+english

     ("kh","","","(x[l_russian+l_english]|kh)"),

     ("chs","","","(ks[l_german]|xs|tSs[l_russian+l_english])"),

     # French "ch" is currently disabled
     #("ch","","[ei]","(x|tS|k[l_romanian]|S[l_french])"),
     #("ch","","","(x|tS[l_russian+l_english]|S[l_french])"),

     ("ch","","[ei]","(x|k[l_romanian]|tS[l_russian+l_english])"),
     ("ch","","","(x|tS[l_russian+l_english])"),

     ("ck","","","(k|tsk[l_polish])"),

     ("czy","","","tSi"),
     ("cze","","[bcdgkpstwzż]","(tSe|tSF)"),
     ("ciewicz","","","(tsevitS|tSevitS)"),
     ("siewicz","","","(sevitS|SevitS)"),
     ("ziewicz","","","(zevitS|ZevitS)"),
     ("riewicz","","","rjevitS"),
     ("diewicz","","","djevitS"),
     ("tiewicz","","","tjevitS"),
     ("iewicz","","","evitS"),
     ("ewicz","","","evitS"),
     ("owicz","","","ovitS"),
     ("icz","","","itS"),
     ("cz","","","tS"), # Polish

     ("cia","","[bcdgkpstwzż]","(tSB[l_polish]|tsB)"),
     ("cia","","","(tSa[l_polish]|tsa)"),
     ("cią","","[bp]","(tSom[l_polish]|tsom)"),
     ("cią","","","(tSon[l_polish]|tson)"),
     ("cię","","[bp]","(tSem[l_polish]|tsem)"),
     ("cię","","","(tSen[l_polish]|tsen)"),
     ("cie","","[bcdgkpstwzż]","(tSF[l_polish]|tsF)"),
     ("cie","","","(tSe[l_polish]|tse)"),
     ("cio","","","(tSo[l_polish]|tso)"),
     ("ciu","","","(tSu[l_polish]|tsu)"),

     ("ci","","$","(tsi[l_polish]|tSi[l_polish+l_romanian]|tS[l_romanian]|si)"),
     ("ci","","","(tsi[l_polish]|tSi[l_polish+l_romanian]|si)"),
     ("ce","","[bcdgkpstwzż]","(tsF[l_polish]|tSe[l_polish+l_romanian]|se)"),
     ("ce","","","(tSe[l_polish+l_romanian]|tse[l_polish]|se)"),
     ("cy","","","(si|tsi[l_polish])"),

     ("ssz","","","S"), # Polish
     ("sz","","","S"), # Polish; actually could also be Hungarian /s/, disabled here

     ("ssp","","","(Sp[l_german]|sp)"),
     ("sp","","","(Sp[l_german]|sp)"),
     ("sst","","","(St[l_german]|st)"),
     ("st","","","(St[l_german]|st)"),
     ("ss","","","s"),

     ("sia","","[bcdgkpstwzż]","(SB[l_polish]|sB[l_polish]|sja)"),
     ("sia","","","(Sa[l_polish]|sja)"),
     ("sią","","[bp]","(Som[l_polish]|som)"),
     ("sią","","","(Son[l_polish]|son)"),
     ("się","","[bp]","(Sem[l_polish]|sem)"),
     ("się","","","(Sen[l_polish]|sen)"),
     ("sie","","[bcdgkpstwzż]","(SF[l_polish]|sF|zi[l_german])"),
     ("sie","","","(se|Se[l_polish]|zi[l_german])"),
     ("sio","","","(So[l_polish]|so)"),
     ("siu","","","(Su[l_polish]|sju)"),
     ("si","","","(Si[l_polish]|si|zi[l_german])"),
     ("s","","[aeiouäöë]","(s|z[l_german])"),

     ("gue","","","ge"),
     ("gui","","","gi"),
     ("guy","","","gi"),
     ("gh","","[ei]","(g[l_romanian]|gh)"),

     ("gauz","","$","haus"),
     ("gaus","","$","haus"),
     ("gol'ts","","$","holts"),
     ("golts","","$","holts"),
     ("gol'tz","","$","holts"),
     ("goltz","","","holts"),
     ("gol'ts","^","","holts"),
     ("golts","^","","holts"),
     ("gol'tz","^","","holts"),
     ("goltz","^","","holts"),
     ("gendler","","$","hendler"),
     ("gejmer","","$","hajmer"),
     ("gejm","","$","hajm"),
     ("geymer","","$","hajmer"),
     ("geym","","$","hajm"),
     ("geimer","","$","hajmer"),
     ("geim","","$","hajm"),
     ("gof","","$","hof"),

     ("ger","","$","ger"),
     ("gen","","$","gen"),
     ("gin","","$","gin"),

     ("gie","","$","(ge|gi[l_german]|ji[l_french])"),
     ("gie","","","ge"),
     ("ge","[yaeiou]","","(gE|xe[l_spanish]|dZe[l_english+l_romanian])"),
     ("gi","[yaeiou]","","(gI|xi[l_spanish]|dZi[l_english+l_romanian])"),
     ("ge","","","(gE|dZe[l_english+l_romanian]|hE[l_russian]|xe[l_spanish])"),
     ("gi","","","(gI|dZi[l_english+l_romanian]|hI[l_russian]|xi[l_spanish])"),
     ("gy","","[aeouáéóúüöőű]","(gi|dj[l_hungarian])"),
     ("gy","","","(gi|d[l_hungarian])"),
     ("g","[jyaeiou]","[aouyei]","g"),
     ("g","","[aouei]","(g|h[l_russian])"),

     ("ej","","","(aj|eZ[l_french+l_romanian]|ex[l_spanish])"),
     ("ej","","","aj"),

     ("ly","","[au]","l"),
     ("li","","[au]","l"),
     ("lj","","[au]","l"),
     ("lio","","","(lo|le[l_russian])"),
     ("lyo","","","(lo|le[l_russian])"),
     ("ll","","","(l|J[l_spanish])"),

     ("j","","[aoeiuy]","(j|dZ[l_english]|x[l_spanish]|Z[l_french+l_romanian])"),
     ("j","","","(j|x[l_spanish])"),

     ("pf","","","(pf|p|f)"),
     ("ph","","","(ph|f)"),

     ("qu","","","(kv[l_german]|k)"),

     ("rze","t","","(Se[l_polish]|re)"), # polish
     ("rze","","","(rze|rtsE[l_german]|Ze[l_polish]|re[l_polish]|rZe[l_polish])"),
     ("rzy","t","","(Si[l_polish]|ri)"), # polish
     ("rzy","","","(Zi[l_polish]|ri[l_polish]|rZi)"),
     ("rz","t","","(S[l_polish]|r)"), # polish
     ("rz","","","(rz|rts[l_german]|Z[l_polish]|r[l_polish]|rZ[l_polish])"), # polish

     ("tz","","$","(ts|tS[l_english+l_german])"),
     ("tz","^","","(ts|tS[l_english+l_german])"),
     ("tz","","","(ts[l_english+l_german+l_russian]|tz)"),

     ("zh","","","(Z|zh[l_polish]|tsh[l_german])"),

     ("zia","","[bcdgkpstwzż]","(ZB[l_polish]|zB[l_polish]|zja)"),
     ("zia","","","(Za[l_polish]|zja)"),
     ("zią","","[bp]","(Zom[l_polish]|zom)"),
     ("zią","","","(Zon[l_polish]|zon)"),
     ("zię","","[bp]","(Zem[l_polish]|zem)"),
     ("zię","","","(Zen[l_polish]|zen)"),
     ("zie","","[bcdgkpstwzż]","(ZF[l_polish]|zF[l_polish]|ze|tsi[l_german])"),
     ("zie","","","(ze|Ze[l_polish]|tsi[l_german])"),
     ("zio","","","(Zo[l_polish]|zo)"),
     ("ziu","","","(Zu[l_polish]|zju)"),
     ("zi","","","(Zi[l_polish]|zi|tsi[l_german])"),

     ("thal","","$","tal"),
     ("th","^","","t"),
     ("th","","[aeiou]","(t[l_german]|th)"),
     ("th","","","t"), # german
     ("vogel","","","(vogel|fogel[l_german])"),
     ("v","^","","(v|f[l_german])"),

     ("h","[aeiouyäöü]","",""), #german
     ("h","","","(h|x[l_romanian+l_polish])"),
     ("h","^","","(h|H[l_english+l_german])"), # H can be exact "h" or approximate "kh"

     # VOWELS
     ("yi","^","","i"),

     # ("e","","$","(e|)"),  # French & English rule disabled except for final -ine
     ("e","in","$","(e|[l_french])"),

     ("ii","","$","i"), # russian
     ("iy","","$","i"), # russian
     ("yy","","$","i"), # russian
     ("yi","","$","i"), # russian
     ("yj","","$","i"), # russian
     ("ij","","$","i"), # russian

     ("aue","","","aue"),
     ("oue","","","oue"),

     ("au","","","(au|o[l_french])"),
     ("ou","","","(ou|u[l_french])"),

     ("ue","","","(Q|uje[l_russian])"),
     ("ae","","","(Y[l_german]|aje[l_russian]|ae)"),
     ("oe","","","(Y[l_german]|oje[l_russian]|oe)"),
     ("ee","","","(i[l_english]|aje[l_russian]|e)"),

     ("ei","","","aj"),
     ("ey","","","aj"),
     ("eu","","","(aj[l_german]|oj[l_german]|eu)"),

     ("i","[aou]","","j"),
     ("y","[aou]","","j"),

     ("ie","","[bcdgkpstwzż]","(i[l_german]|e[l_polish]|ije[l_russian]|je)"),
     ("ie","","","(i[l_german]|e[l_polish]|ije[l_russian]|je)"),
     ("ye","","","(je|ije[l_russian])"),

     ("i","","[au]","j"),
     ("y","","[au]","j"),
     ("io","","","(jo|e[l_russian])"),
     ("yo","","","(jo|e[l_russian])"),

     ("ea","","","(ea|ja[l_romanian])"),
     ("e","^","","(e|je[l_russian])"),
     ("oo","","","(u[l_english]|o)"),
     ("uu","","","u"),

     # LANGUAGE SPECIFIC CHARACTERS
     ("ć","","","(tS[l_polish]|ts)"),  # polish
     ("ł","","","l"),  # polish
     ("ń","","","n"),  # polish
     ("ñ","","","(n|nj[l_spanish])"),
     ("ś","","","(S[l_polish]|s)"), # polish
     ("ş","","","S"),  # romanian
     ("ţ","","","ts"),  # romanian
     ("ż","","","Z"),  # polish
     ("ź","","","(Z[l_polish]|z)"), # polish

     ("où","","","u"), # french

     ("ą","","[bp]","om"),  # polish
     ("ą","","","on"),  # polish
     ("ä","","","(Y|e)"),  # german
     ("á","","","a"), # hungarian
     ("ă","","","(e[l_romanian]|a)"), #romanian
     ("à","","","a"),  # french
     ("â","","","a"), #french+romanian
     ("é","","","e"),
     ("è","","","e"), # french
     ("ê","","","e"), # french
     ("ę","","[bp]","em"),  # polish
     ("ę","","","en"),  # polish
     ("í","","","i"),
     ("î","","","i"),
     ("ö","","","Y"),
     ("ő","","","Y"), # hungarian
     ("ó","","","(u[l_polish]|o)"),
     ("ű","","","Q"),
     ("ü","","","Q"),
     ("ú","","","u"),
     ("ű","","","Q"), # hungarian

     ("ß","","","s"),  # german
     ("'","","",""),
     ('"',"","",""),

     ("a","","[bcdgkpstwzż]","(A|B[l_polish])"),
     ("e","","[bcdgkpstwzż]","(E|F[l_polish])"),
     ("o","","[bcćdgklłmnńrsśtwzźż]","(O|P[l_polish])"),

     # LATIN ALPHABET
     ("a","","","A"),
     ("b","","","b"),
     ("c","","","(k|ts[l_polish])"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","O"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","U"),
     ("v","","","v"),
     ("w","","","v"), # English disabled
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","(ts[l_german]|z)"),

     )

# ash/rulescyrillic.php

_ash_rules_cyrillic = (

     ("ця","","","tsa"),
     ("цю","","","tsu"),
     ("циа","","","tsa"),
     ("цие","","","tse"),
     ("цио","","","tso"),
     ("циу","","","tsu"),
     ("сие","","","se"),
     ("сио","","","so"),
     ("зие","","","ze"),
     ("зио","","","zo"),

     ("гауз","","$","haus"),
     ("гаус","","$","haus"),
     ("гольц","","$","holts"),
     ("геймер","","$","hajmer"),
     ("гейм","","$","hajm"),
     ("гоф","","$","hof"),
     ("гер","","$","ger"),
     ("ген","","$","gen"),
     ("гин","","$","gin"),
     ("г","(й|ё|я|ю|ы|а|е|о|и|у)","(а|е|о|и|у)","g"),
     ("г","","(а|е|о|и|у)","(g|h)"),

     ("ля","","","la"),
     ("лю","","","lu"),
     ("лё","","","(le|lo)"),
     ("лио","","","(le|lo)"),
     ("ле","","","(lE|lo)"),

     ("ийе","","","je"),
     ("ие","","","je"),
     ("ыйе","","","je"),
     ("ые","","","je"),
     ("ий","","(а|о|у)","j"),
     ("ый","","(а|о|у)","j"),

     ("ий","","$","i"),
     ("ый","","$","i"),

     ("ё","","","(e|jo)"),

     ("ей","^","","(jaj|aj)"),
     ("е","(а|е|о|у)","","je"),
     ("е","^","","je"),
     ("эй","","","aj"),
     ("ей","","","aj"),

     ("ауе","","","aue"),
     ("ауэ","","","aue"),

     ("а","","","a"),
     ("б","","","b"),
     ("в","","","v"),
     ("г","","","g"),
     ("д","","","d"),
     ("е","","","E"),
     ("ж","","","Z"),
     ("з","","","z"),
     ("и","","","I"),
     ("й","","","j"),
     ("к","","","k"),
     ("л","","","l"),
     ("м","","","m"),
     ("н","","","n"),
     ("о","","","o"),
     ("п","","","p"),
     ("р","","","r"),
     ("с","","с",""),
     ("с","","","s"),
     ("т","","","t"),
     ("у","","","u"),
     ("ф","","","f"),
     ("х","","","x"),
     ("ц","","","ts"),
     ("ч","","","tS"),
     ("ш","","","S"),
     ("щ","","","StS"),
     ("ъ","","",""),
     ("ы","","","I"),
     ("ь","","",""),
     ("э","","","E"),
     ("ю","","","ju"),
     ("я","","","ja"),

     )

# ash/rulesenglish.php

_ash_rules_english = (

     # CONSONANTS
     ("tch","","","tS"),
     ("ch","","","(tS|x)"),
     ("ck","","","k"),
     ("cc","","[iey]","ks"), # success, accent
     ("c","","c",""),
     ("c","","[iey]","s"), # circle
     ("c","","","k"), # candy
     ("gh","^","","g"), # ghost
     ("gh","","","(g|f|w)"), # burgh | tough | bough
     ("gn","","","(gn|n)"),
     ("g","","[iey]","(g|dZ)"), # get, gem, giant, gigabyte
     # ("th","","","(6|8|t)"),
     ("th","","","t"),
     ("kh","","","x"),
     ("ph","","","f"),
     ("sch","","","(S|sk)"),
     ("sh","","","S"),
     ("who","^","","hu"),
     ("wh","^","","w"),

     ("h","","$",""), # hard to find an example that isn't in a name
     ("h","","[^aeiou]",""), # hard to find an example that isn't in a name
     ("h","^","","H"),
     ("h","","","h"),

     ("j","","","dZ"),
     ("kn","^","","n"), # knight
     ("mb","","$","m"),
     ("ng","","$","(N|ng)"),
     ("pn","^","","(pn|n)"),
     ("ps","^","","(ps|s)"),
     ("qu","","","kw"),
     ("q","","","k"),
     ("tia","","","(So|Sa)"),
     ("tio","","","So"),
     ("wr","^","","r"),
     ("w","","","(w|v)"), # the variant "v" is for spellings coming from German/Polish
     ("x","^","","z"),
     ("x","","","ks"),

     # VOWELS
     ("y","^","","j"),
     ("y","^","[aeiouy]","j"),
     ("yi","^","","i"),
     ("aue","","","aue"),
     ("oue","","","(aue|oue)"),
     ("ai","","","(aj|e)"), # rain | said
     ("ay","","","aj"),
     ("a","","[^aeiou]e","aj"), # plane (actually "ej")
     ("a","","","(e|o|a)"), # hat | call | part
     ("ei","","","(aj|i)"), # weigh | receive
     ("ey","","","(aj|i)"), # hey | barley
     ("ear","","","ia"), # tear
     ("ea","","","(i|e)"), # reason | treasure
     ("ee","","","i"), # between
     ("e","","[^aeiou]e","i"), # meter
     ("e","","$","(|E)"), # blame, badge
     ("e","","","E"), # bed
     ("ie","","","i"), # believe
     ("i","","[^aeiou]e","aj"), # five
     ("i","","","I"), # hit -- Morse disagrees, feels it should go to I
     ("oa","","","ou"), # toad
     ("oi","","","oj"), # join
     ("oo","","","u"), # food
     ("ou","","","(u|ou)"), # through | tough | could
     ("oy","","","oj"), # boy
     ("o","","[^aeiou]e","ou"), # rode
     ("o","","","(o|a)"), # hot -- Morse disagrees, feels it should go to 9
     ("u","","[^aeiou]e","(ju|u)"), # cute | flute
     ("u","","r","(e|u)"), # turn -- Morse disagrees, feels it should go to E
     ("u","","","(u|a)"), # put
     ("y","","","i"),

     # TRIVIAL
     ("b","","","b"),
     ("d","","","d"),
     ("f","","","f"),
     ("g","","","g"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("p","","","p"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("v","","","v"),
     ("z","","","z"),

     )

# ash/rulesfrench.php

# Ashkenazic
_ash_rules_french = (

     # CONSONANTS
     ("kh","","","x"), # foreign
     ("ph","","","f"),

     ("ç","","","s"),
     ("x","","","ks"),
     ("ch","","","S"),
     ("c","","[eiyéèê]","s"),
     ("c","","","k"),
     ("gn","","","(n|gn)"),
     ("g","","[eiy]","Z"),
     ("gue","","$","k"),
     ("gu","","[eiy]","g"),
     #("aill","","e","aj"), # non Jewish
     #("ll","","e","(l|j)"), # non Jewish
     ("que","","$","k"),
     ("qu","","","k"),
     ("q","","","k"),
     ("s","[aeiouyéèê]","[aeiouyéèê]","z"),
     ("h","[bdgt]","",""), # translit from Arabic
     ("h","","$",""), # foreign
     ("j","","","Z"),
     ("w","","","v"),
     ("ouh","","[aioe]","(v|uh)"),
     ("ou","","[aeio]","v"),
     ("uo","","","(vo|o)"),
     ("u","","[aeio]","v"),

     # VOWELS
     ("aue","","","aue"),
     ("eau","","","o"),
     #("au","","","(o|au)"), # non Jewish
     ("ai","","","aj"), # [e] is non Jewish
     ("ay","","","aj"), # [e] is non Jewish
     ("é","","","e"),
     ("ê","","","e"),
     ("è","","","e"),
     ("à","","","a"),
     ("â","","","a"),
     ("où","","","u"),
     ("ou","","","u"),
     ("oi","","","oj"), # [ua] is non Jewish
     ("ei","","","aj"), # [e] is non Jewish
     ("ey","","","aj"), # [e] non Jewish
     #("eu","","","(e|o)"), # non Jewish
     ("y","[ou]","","j"),
     ("e","","$","(e|)"),
     ("i","","[aou]","j"),
     ("y","","[aoeu]","j"),
     ("y","","","i"),

     # TRIVIAL
     ("a","","","a"),
     ("b","","","b"),
     ("d","","","d"),
     ("e","","","E"), # only Ashkenazic
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"), # only Ashkenazic
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("z","","","z"),

     )

# ash/rulesgerman.php

# Ashkenazic
_ash_rules_german = (

     # CONSONANTS
     ("ziu","","","tsu"),
     ("zia","","","tsa"),
     ("zio","","","tso"),

     ("ssch","","","S"),
     ("chsch","","","xS"),
     ("ewitsch","","$","evitS"),
     ("owitsch","","$","ovitS"),
     ("evitsch","","$","evitS"),
     ("ovitsch","","$","ovitS"),
     ("witsch","","$","vitS"),
     ("vitsch","","$","vitS"),
     ("sch","","","S"),

     ("chs","","","ks"),
     ("ch","","","x"),
     ("ck","","","k"),
     ("c","","[eiy]","ts"),

     ("sp","^","","Sp"),
     ("st","^","","St"),
     ("ssp","","","(Sp|sp)"),
     ("sp","","","(Sp|sp)"),
     ("sst","","","(St|st)"),
     ("st","","","(St|st)"),
     ("pf","","","(pf|p|f)"),
     ("ph","","","(ph|f)"),
     ("qu","","","kv"),

     ("ewitz","","$","(evits|evitS)"),
     ("ewiz","","$","(evits|evitS)"),
     ("evitz","","$","(evits|evitS)"),
     ("eviz","","$","(evits|evitS)"),
     ("owitz","","$","(ovits|ovitS)"),
     ("owiz","","$","(ovits|ovitS)"),
     ("ovitz","","$","(ovits|ovitS)"),
     ("oviz","","$","(ovits|ovitS)"),
     ("witz","","$","(vits|vitS)"),
     ("wiz","","$","(vits|vitS)"),
     ("vitz","","$","(vits|vitS)"),
     ("viz","","$","(vits|vitS)"),
     ("tz","","","ts"),

     ("thal","","$","tal"),
     ("th","^","","t"),
     ("th","","[äöüaeiou]","(t|th)"),
     ("th","","","t"),
     ("rh","^","","r"),
     ("h","[aeiouyäöü]","",""),
     ("h","^","","H"),

     ("ss","","","s"),
     ("s","","[äöüaeiouy]","(z|s)"),
     ("s","[aeiouyäöüj]","[aeiouyäöü]","z"),
     ("ß","","","s"),

     # VOWELS
     ("ij","","$","i"),
     ("aue","","","aue"),
     ("ue","","","Q"),
     ("ae","","","Y"),
     ("oe","","","Y"),
     ("ü","","","Q"),
     ("ä","","","(Y|e)"),
     ("ö","","","Y"),
     ("ei","","","aj"),
     ("ey","","","aj"),
     ("eu","","","(aj|oj)"),
     ("i","[aou]","","j"),
     ("y","[aou]","","j"),
     ("ie","","","I"),
     ("i","","[aou]","j"),
     ("y","","[aoeu]","j"),

     # FOREIGN LETTERs
     ("ñ","","","n"),
     ("ã","","","a"),
     ("ő","","","o"),
     ("ű","","","u"),
     ("ç","","","s"),

     # ALPHABET
     ("a","","","A"),
     ("b","","","b"),
     ("c","","","k"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","O"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","U"),
     ("v","","","(f|v)"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","ts"),

     )

# ash/ruleshebrew.php

# Ashkenazic
_ash_rules_hebrew = (

     ("אי","","","i"),
     ("עי","","","i"),
     ("עו","","","VV"),
     ("או","","","VV"),

     ("ג׳","","","Z"),
     ("ד׳","","","dZ"),

     ("א","","","L"),
     ("ב","","","b"),
     ("ג","","","g"),
     ("ד","","","d"),

     ("ה","^","","1"),
     ("ה","","$","1"),
     ("ה","","",""),

     ("וו","","","V"),
     ("וי","","","WW"),
     ("ו","","","W"),
     ("ז","","","z"),
     ("ח","","","X"),
     ("ט","","","T"),
     ("יי","","","i"),
     ("י","","","i"),
     ("ך","","","X"),
     ("כ","^","","K"),
     ("כ","","","k"),
     ("ל","","","l"),
     ("ם","","","m"),
     ("מ","","","m"),
     ("ן","","","n"),
     ("נ","","","n"),
     ("ס","","","s"),
     ("ע","","","L"),
     ("ף","","","f"),
     ("פ","","","f"),
     ("ץ","","","C"),
     ("צ","","","C"),
     ("ק","","","K"),
     ("ר","","","r"),
     ("ש","","","s"),
     ("ת","","","TB"), # only Ashkenazic

     )

# ash/ruleshungarian.php

# ASHKENAZIC
_ash_rules_hungarian = (

     # CONSONANTS
     ("sz","","","s"),
     ("zs","","","Z"),
     ("cs","","","tS"),

     ("ay","","","(oj|aj)"),
     ("ai","","","(oj|aj)"),
     ("aj","","","(oj|aj)"),

     ("ei","","","aj"), # German element
     ("ey","","","aj"), # German element

     ("y","[áo]","","j"),
     ("i","[áo]","","j"),
     ("ee","","","(aj|e)"), # actually ej
     ("ely","","","(aj|eli)"), # actually ej
     ("ly","","","(j|li)"),
     ("gy","","[aeouáéóúüöőű]","dj"),
     ("gy","","","(d|gi)"),
     ("ny","","[aeouáéóúüöőű]","nj"),
     ("ny","","","(n|ni)"),
     ("ty","","[aeouáéóúüöőű]","tj"),
     ("ty","","","(t|ti)"),

     ("qu","","","(ku|kv)"),
     ("h","","$",""),

     # VOWELS
     ("á","","","a"),
     ("é","","","e"),
     ("í","","","i"),
     ("ó","","","o"),
     ("ö","","","Y"),
     ("ő","","","Y"),
     ("ú","","","u"),
     ("ü","","","Q"),
     ("ű","","","Q"),

     # LATIN ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","ts"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","(S|s)"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","i"),
     ("z","","","z"),

     )

# ash/rulespolish.php

# Ashkenazic
_ash_rules_polish = (

     # CONVERTING FEMININE TO MASCULINE
     ("ska","","$","ski"),
     ("cka","","$","tski"),
     ("lowa","","$","(lova|lof|l|el)"),
     ("kowa","","$","(kova|kof|k|ek)"),
     ("owa","","$","(ova|of|)"),
     ("lowna","","$","(lovna|levna|l|el)"),
     ("kowna","","$","(kovna|k|ek)"),
     ("owna","","$","(ovna|)"),
     ("lówna","","$","(l|el)"),
     ("kówna","","$","(k|ek)"),
     ("ówna","","$",""),
     ("a","","$","(a|i)"),

     # CONSONANTS
     ("czy","","","tSi"),
     ("cze","","[bcdgkpstwzż]","(tSe|tSF)"),
     ("ciewicz","","","(tsevitS|tSevitS)"),
     ("siewicz","","","(sevitS|SevitS)"),
     ("ziewicz","","","(zevitS|ZevitS)"),
     ("riewicz","","","rjevitS"),
     ("diewicz","","","djevitS"),
     ("tiewicz","","","tjevitS"),
     ("iewicz","","","evitS"),
     ("ewicz","","","evitS"),
     ("owicz","","","ovitS"),
     ("icz","","","itS"),
     ("cz","","","tS"),
     ("ch","","","x"),

     ("cia","","[bcdgkpstwzż]","(tSB|tsB)"),
     ("cia","","","(tSa|tsa)"),
     ("cią","","[bp]","(tSom|tsom)"),
     ("cią","","","(tSon|tson)"),
     ("cię","","[bp]","(tSem|tsem)"),
     ("cię","","","(tSen|tsen)"),
     ("cie","","[bcdgkpstwzż]","(tSF|tsF)"),
     ("cie","","","(tSe|tse)"),
     ("cio","","","(tSo|tso)"),
     ("ciu","","","(tSu|tsu)"),
     ("ci","","","(tSi|tsI)"),
     ("ć","","","(tS|ts)"),

     ("ssz","","","S"),
     ("sz","","","S"),
     ("sia","","[bcdgkpstwzż]","(SB|sB|sja)"),
     ("sia","","","(Sa|sja)"),
     ("sią","","[bp]","(Som|som)"),
     ("sią","","","(Son|son)"),
     ("się","","[bp]","(Sem|sem)"),
     ("się","","","(Sen|sen)"),
     ("sie","","[bcdgkpstwzż]","(SF|sF|se)"),
     ("sie","","","(Se|se)"),
     ("sio","","","(So|so)"),
     ("siu","","","(Su|sju)"),
     ("si","","","(Si|sI)"),
     ("ś","","","(S|s)"),

     ("zia","","[bcdgkpstwzż]","(ZB|zB|zja)"),
     ("zia","","","(Za|zja)"),
     ("zią","","[bp]","(Zom|zom)"),
     ("zią","","","(Zon|zon)"),
     ("zię","","[bp]","(Zem|zem)"),
     ("zię","","","(Zen|zen)"),
     ("zie","","[bcdgkpstwzż]","(ZF|zF)"),
     ("zie","","","(Ze|ze)"),
     ("zio","","","(Zo|zo)"),
     ("ziu","","","(Zu|zju)"),
     ("zi","","","(Zi|zI)"),

     ("że","","[bcdgkpstwzż]","(Ze|ZF)"),
     ("że","","[bcdgkpstwzż]","(Ze|ZF|ze|zF)"),
     ("że","","","Ze"),
     ("źe","","","(Ze|ze)"),
     ("ży","","","Zi"),
     ("źi","","","(Zi|zi)"),
     ("ż","","","Z"),
     ("ź","","","(Z|z)"),

     ("rze","t","","(Se|re)"),
     ("rze","","","(Ze|re|rZe)"),
     ("rzy","t","","(Si|ri)"),
     ("rzy","","","(Zi|ri|rZi)"),
     ("rz","t","","(S|r)"),
     ("rz","","","(Z|r|rZ)"),

     ("lio","","","(lo|le)"),
     ("ł","","","l"),
     ("ń","","","n"),
     ("qu","","","k"),
     ("s","","s",""),

     # VOWELS
     ("ó","","","(u|o)"),
     ("ą","","[bp]","om"),
     ("ę","","[bp]","em"),
     ("ą","","","on"),
     ("ę","","","en"),

     ("ije","","","je"),
     ("yje","","","je"),
     ("iie","","","je"),
     ("yie","","","je"),
     ("iye","","","je"),
     ("yye","","","je"),

     ("ij","","[aou]","j"),
     ("yj","","[aou]","j"),
     ("ii","","[aou]","j"),
     ("yi","","[aou]","j"),
     ("iy","","[aou]","j"),
     ("yy","","[aou]","j"),

     ("rie","","","rje"),
     ("die","","","dje"),
     ("tie","","","tje"),
     ("ie","","[bcdgkpstwzż]","F"),
     ("ie","","","e"),

     ("aue","","","aue"),
     ("au","","","au"),

     ("ei","","","aj"),
     ("ey","","","aj"),
     ("ej","","","aj"),

     ("ai","","","aj"),
     ("ay","","","aj"),
     ("aj","","","aj"),

     ("i","[ou]","","j"),
     ("y","[ou]","","j"),
     ("i","","[aou]","j"),
     ("y","","[aeou]","j"),

     ("a","","[bcdgkpstwzż]","B"),
     ("e","","[bcdgkpstwzż]","(E|F)"),
     ("o","","[bcćdgklłmnńrsśtwzźż]","P"),

     # ALPHABET
     ("a","","","a"),
     ("b","","","b"),
     ("c","","","ts"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","(h|x)"),
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("q","","","k"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","I"),
     ("z","","","z"),

     )

# ash/rulesromanian.php

_ash_rules_romanian = (

     ("j","","","Z"),

     ("ce","","","tSe"),
     ("ci","","","(tSi|tS)"),
     ("ch","","[ei]","k"),
     ("ch","","","x"), # foreign
     ("c","","","k"),

     ("gi","","","(dZi|dZ)"),
     ("g","","[ei]","dZ"),
     ("gh","","","g"),

     ("ei","","","aj"),
     ("i","[aou]","","j"),
     ("i","","[aeou]","j"),
     ("ţ","","","ts"),
     ("ş","","","S"),
     ("h","","","(x|h)"),

     ("qu","","","k"),
     ("q","","","k"),
     ("w","","","v"),
     ("x","","","ks"),
     ("y","","","i"),

     ("î","","","i"),
     ("ea","","","ja"),
     ("ă","","","(e|a)"),
     ("aue","","","aue"),

     ("a","","","a"),
     ("b","","","b"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("i","","","I"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("z","","","z"),

     )

# ash/rulesrussian.php

_ash_rules_russian = (

     # CONVERTING FEMININE TO MASCULINE
     ("yna","","$","(in|ina)"),
     ("ina","","$","(in|ina)"),
     ("liova","","$","(lof|lef)"),
     ("lova","","$","(lof|lef|lova)"),
     ("ova","","$","(of|ova)"),
     ("eva","","$","(ef|ova)"),
     ("aia","","$","(aja|i)"),
     ("aja","","$","(aja|i)"),
     ("aya","","$","(aja|i)"),

     #SPECIFIC CONSONANTS
     ("tsya","","","tsa"),
     ("tsyu","","","tsu"),
     ("tsia","","","tsa"),
     ("tsie","","","tse"),
     ("tsio","","","tso"),
     ("tsye","","","tse"),
     ("tsyo","","","tso"),
     ("tsiu","","","tsu"),
     ("sie","","","se"),
     ("sio","","","so"),
     ("zie","","","ze"),
     ("zio","","","zo"),
     ("sye","","","se"),
     ("syo","","","so"),
     ("zye","","","ze"),
     ("zyo","","","zo"),

     ("gauz","","$","haus"),
     ("gaus","","$","haus"),
     ("gol'ts","","$","holts"),
     ("golts","","$","holts"),
     ("gol'tz","","$","holts"),
     ("goltz","","$","holts"),
     ("gejmer","","$","hajmer"),
     ("gejm","","$","hajm"),
     ("geimer","","$","hajmer"),
     ("geim","","$","hajm"),
     ("geymer","","$","hajmer"),
     ("geym","","$","hajm"),
     ("gendler","","$","hendler"),
     ("gof","","$","hof"),
     ("gojf","","$","hojf"),
     ("goyf","","$","hojf"),
     ("goif","","$","hojf"),
     ("ger","","$","ger"),
     ("gen","","$","gen"),
     ("gin","","$","gin"),
     ("gg","","","g"),
     ("g","[jaeoiuy]","[aeoiu]","g"),
     ("g","","[aeoiu]","(g|h)"),

     ("kh","","","x"),
     ("ch","","","(tS|x)"), # in DJSRE the rule is simpler: ("ch","","","tS")
     ("sch","","","(StS|S)"),
     ("ssh","","","S"),
     ("sh","","","S"),
     ("zh","","","Z"),
     ("tz","","$","ts"), # not in DJSRE
     ("tz","","","(ts|tz)"), # not in DJSRE
     ("c","","[iey]","s"), # not in DJSRE
     ("c","","","k"), # not in DJSRE
     ("qu","","","(kv|k)"), # not in DJSRE
     ("q","","","k"), # not in DJSRE
     ("s","","s",""),

     ("w","","","v"), # not in DJSRE
     ("x","","","ks"), # not in DJSRE

     #SPECIFIC VOWELS
     ("lya","","","la"),
     ("lyu","","","lu"),
     ("lia","","","la"), # not in DJSRE
     ("liu","","","lu"),  # not in DJSRE
     ("lja","","","la"), # not in DJSRE
     ("lju","","","lu"),  # not in DJSRE
     ("le","","","(lo|lE)"), #not in DJSRE
     ("lyo","","","(lo|le)"), #not in DJSRE
     ("lio","","","(lo|le)"),

     ("ije","","","je"),
     ("ie","","","je"),
     ("iye","","","je"),
     ("iie","","","je"),
     ("yje","","","je"),
     ("ye","","","je"),
     ("yye","","","je"),
     ("yie","","","je"),

     ("ij","","[aou]","j"),
     ("iy","","[aou]","j"),
     ("ii","","[aou]","j"),
     ("yj","","[aou]","j"),
     ("yy","","[aou]","j"),
     ("yi","","[aou]","j"),

     ("io","","","(jo|e)"),
     ("i","","[au]","j"),
     ("i","[aou]","","j"), # not in DJSRE
     ("ei","","","aj"), # not in DJSRE
     ("ey","","","aj"), # not in DJSRE
     ("ej","","","aj"),
     ("yo","","","(jo|e)"), #not in DJSRE
     ("y","","[au]","j"),
     ("y","[aiou]","","j"), # not in DJSRE

     ("ii","","$","i"), # not in DJSRE
     ("iy","","$","i"), # not in DJSRE
     ("yy","","$","i"), # not in DJSRE
     ("yi","","$","i"), # not in DJSRE
     ("yj","","$","i"),
     ("ij","","$","i"),

     ("e","^","","(je|E)"), # in DJSRE the rule is simpler: ("e","^","","je")
     ("ee","","","(aje|i)"), # in DJSRE the rule is simpler: ("ee","","","(eje|aje)")
     ("e","[aou]","","je"),
     ("y","","","I"),
     ("oo","","","(oo|u)"), # not in DJSRE
     ("'","","",""),
     ('"',"","",""),

     ("aue","","","aue"),

     # TRIVIAL
     ("a","","","a"),
     ("b","","","b"),
     ("d","","","d"),
     ("e","","","E"),
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"), # not in DJSRE
     ("i","","","I"),
     ("j","","","j"),
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),
     ("v","","","v"),
     ("z","","","z"),

     )

# ash/rulesspanish.php

# Ashkenazic = Argentina
_ash_rules_spanish = (

     # CONSONANTS
     ("ñ","","","(n|nj)"),

     ("ch","","","(tS|dZ)"), # dZ is typical for Argentina
     ("h","[bdgt]","",""), # translit. from Arabic
     ("h","","$",""), # foreign

     ("j","","","x"),
     ("x","","","ks"),
     ("ll","","","(l|Z)"), # Z is typical for Argentina, only Ashkenazic
     ("w","","","v"), # foreign words

     ("v","","","(b|v)"),
     ("b","","","(b|v)"),
     ("m","","[bpvf]","(m|n)"),

     ("c","","[ei]","s"),
     ("c","","","k"),

     ("z","","","(z|s)"), # as "c" befoire "e" or "i", in Spain it is like unvoiced English "th"

     ("gu","","[ei]","(g|gv)"), # "gv" because "u" can actually be "ü"
     ("g","","[ei]","(x|g)"),  # "g" only for foreign words

     ("qu","","","k"),
     ("q","","","k"),

     ("uo","","","(vo|o)"),
     ("u","","[aei]","v"),

     ("y","","","(i|j|S|Z)"), # S or Z are peculiar to South America; only Ashkenazic

     # VOWELS
     ("ü","","","v"),
     ("á","","","a"),
     ("é","","","e"),
     ("í","","","i"),
     ("ó","","","o"),
     ("ú","","","u"),

     # TRIVIAL
     ("a","","","a"),
     ("d","","","d"),
     ("e","","","E"), # Only Ashkenazic
     ("f","","","f"),
     ("g","","","g"),
     ("h","","","h"),
     ("i","","","I"), # Only Ashkenazic
     ("k","","","k"),
     ("l","","","l"),
     ("m","","","m"),
     ("n","","","n"),
     ("o","","","o"),
     ("p","","","p"),
     ("r","","","r"),
     ("s","","","s"),
     ("t","","","t"),
     ("u","","","u"),

     )

bmdata = dict()

bmdata['gen'] = dict()
bmdata['gen']['approx'] = dict()
bmdata['gen']['exact'] = dict()
bmdata['gen']['rules'] = dict()

bmdata['gen']['approx'][l_any] = _gen_approx_any
bmdata['gen']['approx'][l_arabic] = _gen_approx_arabic
bmdata['gen']['approx']['common'] = _gen_exact_approx_common + _gen_approx_common
bmdata['gen']['approx'][l_cyrillic] = _gen_approx_russian
bmdata['gen']['approx'][l_czech] = _gen_approx_french
bmdata['gen']['approx'][l_dutch] = _gen_approx_french
bmdata['gen']['approx'][l_english] = _gen_approx_english
bmdata['gen']['approx'][l_french] = _gen_approx_french
bmdata['gen']['approx'][l_german] = _gen_approx_german
bmdata['gen']['approx'][l_greek] = _gen_approx_french
bmdata['gen']['approx']['greeklatin'] = _gen_approx_french + _gen_approx_greeklatin
bmdata['gen']['approx'][l_hebrew] = _gen_approx_hebrew
bmdata['gen']['approx'][l_hungarian] = _gen_approx_french
bmdata['gen']['approx'][l_italian] = _gen_approx_french
bmdata['gen']['approx'][l_polish] = _gen_approx_polish
bmdata['gen']['approx'][l_portuguese] = _gen_approx_french
bmdata['gen']['approx'][l_romanian] = _gen_approx_polish
bmdata['gen']['approx'][l_russian] = _gen_approx_russian
bmdata['gen']['approx']['spanish'] = _gen_approx_french + _gen_approx_spanish
bmdata['gen']['approx'][l_turkish] = _gen_approx_french
bmdata['gen']['exact'][l_any] = _gen_exact_any
bmdata['gen']['exact'][l_arabic] = _gen_exact_arabic
bmdata['gen']['exact']['common'] = _gen_exact_approx_common + _gen_exact_common
bmdata['gen']['exact'][l_cyrillic] = _gen_exact_russian
bmdata['gen']['exact'][l_czech] = _gen_exact_russian
bmdata['gen']['exact'][l_dutch] = _gen_exact_dutch
bmdata['gen']['exact'][l_english] = _gen_exact_russian
bmdata['gen']['exact'][l_french] = _gen_exact_french
bmdata['gen']['exact'][l_german] = _gen_exact_any
bmdata['gen']['exact'][l_greek] = _gen_exact_greek
bmdata['gen']['exact'][l_greeklatin] = _gen_exact_greeklatin
bmdata['gen']['exact'][l_hebrew] = _gen_exact_hebrew
bmdata['gen']['exact'][l_hungarian] = _gen_exact_russian
bmdata['gen']['exact'][l_italian] = _gen_exact_italian
bmdata['gen']['exact'][l_polish] = _gen_exact_polish
bmdata['gen']['exact'][l_portuguese] = _gen_exact_portuguese
bmdata['gen']['exact'][l_romanian] = _gen_exact_russian
bmdata['gen']['exact'][l_russian] = _gen_exact_russian
bmdata['gen']['exact'][l_spanish] = _gen_exact_spanish
bmdata['gen']['exact'][l_turkish] = _gen_exact_turkish
bmdata['gen']['hebrew']['common'] = _gen_exact_approx_common + _gen_hebrew_common
bmdata['gen']['rules'][l_any] = _gen_rules_any
bmdata['gen']['rules'][l_arabic] = _gen_rules_arabic
bmdata['gen']['rules'][l_cyrillic] = _gen_rules_cyrillic
bmdata['gen']['rules'][l_czech] = _gen_rules_czech
bmdata['gen']['rules'][l_dutch] = _gen_rules_dutch
bmdata['gen']['rules'][l_english] = _gen_rules_english
bmdata['gen']['rules'][l_french] = _gen_rules_french
bmdata['gen']['rules'][l_german] = _gen_rules_german
bmdata['gen']['rules'][l_greek] = _gen_rules_greek
bmdata['gen']['rules'][l_greeklatin] = _gen_rules_greeklatin
bmdata['gen']['rules'][l_hebrew] = _gen_rules_hebrew
bmdata['gen']['rules'][l_hungarian] = _gen_rules_hungarian
bmdata['gen']['rules'][l_italian] = _gen_rules_italian
bmdata['gen']['rules'][l_polish] = _gen_rules_polish
bmdata['gen']['rules'][l_portuguese] = _gen_rules_portuguese
bmdata['gen']['rules'][l_romanian] = _gen_rules_romanian
bmdata['gen']['rules'][l_russian] = _gen_rules_russian
bmdata['gen']['rules'][l_spanish] = _gen_rules_spanish
bmdata['gen']['rules'][l_turkish] = _gen_rules_turkish

bmdata['sep'] = dict()
bmdata['sep']['approx'] = dict()
bmdata['sep']['exact'] = dict()
bmdata['sep']['rules'] = dict()

bmdata['sep']['approx'][l_any] = _sep_approx_any
bmdata['sep']['approx']['common'] = _sep_exact_approx_common + _sep_approx_common
bmdata['sep']['approx'][l_french] = _sep_approx_french
bmdata['sep']['approx'][l_hebrew] = _sep_approx_hebrew
bmdata['sep']['approx'][l_italian] = _sep_approx_french
bmdata['sep']['approx'][l_portuguese] = _sep_approx_french
bmdata['sep']['approx'][l_spanish] = _sep_approx_french
bmdata['sep']['exact'][l_any] = _sep_exact_any
bmdata['sep']['exact']['common'] = _sep_exact_approx_common + _sep_exact_common
bmdata['sep']['exact'][l_french] = _sep_exact_french
bmdata['sep']['exact'][l_hebrew] = _sep_exact_hebrew
bmdata['sep']['exact'][l_italian] = _sep_exact_italian
bmdata['sep']['exact'][l_portuguese] = _sep_exact_portuguese
bmdata['sep']['exact'][l_spanish] = _sep_exact_spanish
bmdata['sep']['hebrew']['common'] = _sep_exact_approx_common + _sep_hebrew_common
bmdata['sep']['rules'][l_any] = _sep_rules_any
bmdata['sep']['rules'][l_french] = _sep_rules_french
bmdata['sep']['rules'][l_hebrew] = _sep_rules_hebrew
bmdata['sep']['rules'][l_italian] = _sep_rules_italian
bmdata['sep']['rules'][l_portuguese] = _sep_rules_portuguese
bmdata['sep']['rules'][l_spanish] = _sep_rules_spanish

bmdata['ash'] = dict()
bmdata['ash']['approx'] = dict()
bmdata['ash']['exact'] = dict()
bmdata['ash']['rules'] = dict()

bmdata['ash']['approx'][l_any] = _ash_approx_any
bmdata['ash']['approx']['common'] = _ash_exact_approx_common + _ash_approx_common
bmdata['ash']['approx'][l_cyrillic] = _ash_approx_russian
bmdata['ash']['approx'][l_english] = _ash_approx_english
bmdata['ash']['approx'][l_french] = _ash_approx_french
bmdata['ash']['approx'][l_german] = _ash_approx_german
bmdata['ash']['approx'][l_hebrew] = _ash_approx_hebrew
bmdata['ash']['approx'][l_hungarian] = _ash_approx_french
bmdata['ash']['approx'][l_polish] = _ash_approx_polish
bmdata['ash']['approx'][l_romanian] = _ash_approx_polish
bmdata['ash']['approx'][l_russian] = _ash_approx_russian
bmdata['ash']['approx'][l_spanish] = _ash_approx_french
bmdata['ash']['exact'][l_any] = _ash_exact_any
bmdata['ash']['exact']['common'] = _ash_exact_approx_common + _ash_exact_common
bmdata['ash']['exact'][l_cyrillic] = _ash_exact_russian
bmdata['ash']['exact'][l_english] = _ash_exact_russian
bmdata['ash']['exact'][l_french] = _ash_exact_russian
bmdata['ash']['exact'][l_german] = _ash_exact_any
bmdata['ash']['exact'][l_hebrew] = _ash_exact_hebrew
bmdata['ash']['exact'][l_hungarian] = _ash_exact_russian
bmdata['ash']['exact'][l_polish] = _ash_exact_polish
bmdata['ash']['exact'][l_romanian] = _ash_exact_russian
bmdata['ash']['exact'][l_russian] = _ash_exact_russian
bmdata['ash']['exact'][l_spanish] = _ash_exact_russian
bmdata['ash']['hebrew']['common'] = _ash_exact_approx_common + _ash_hebrew_common
bmdata['ash']['rules'][l_any] = _ash_rules_any
bmdata['ash']['rules'][l_cyrillic] = _ash_rules_cyrillic
bmdata['ash']['rules'][l_english] = _ash_rules_english
bmdata['ash']['rules'][l_french] = _ash_rules_french
bmdata['ash']['rules'][l_german] = _ash_rules_german
bmdata['ash']['rules'][l_hebrew] = _ash_rules_hebrew
bmdata['ash']['rules'][l_hungarian] = _ash_rules_hungarian
bmdata['ash']['rules'][l_polish] = _ash_rules_polish
bmdata['ash']['rules'][l_romanian] = _ash_rules_romanian
bmdata['ash']['rules'][l_russian] = _ash_rules_russian
bmdata['ash']['rules'][l_spanish] = _ash_rules_spanish
