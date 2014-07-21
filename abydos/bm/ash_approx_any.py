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

_ash_approx_any = (

                   # CONSONANTS
                   ("b","","","(b|v[$spanish])"),
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

                   ("B","","[bp]","(o|om[$polish]|im[$polish])"),
                   ("B","","[dgkstvz]","(a|o|on[$polish]|in[$polish])"),
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

                   ("F","","[bp]","(i|im[$polish]|om[$polish])"),
                   ("F","","[dgkstvz]","(i|in[$polish]|on[$polish])"),
                   ("F", "", "", "i"),

                   ("P", "", "", "(o|u)"),

                   ("I", "[aeiouAEIBFOUQY]", "", "i"),
                   ("I","","[^aeiouAEBFIOU]e","(Q[$german]|i|D[$english])"),  # "line"
                   ("I", "", "$", "i"),
                   ("I", "", "[^k]$", "i"),
                   ("Ik", "[lr]", "$", "(ik|Qk[$german])"),
                   ("Ik", "", "$", "ik"),
                   ("sIts", "", "$", "(sits|sQts[$german])"),
                   ("Its", "", "$", "its"),
                   ("I", "", "", "(Q[$german]|i)"),

                   ("lE","[bdfgkmnprsStvzZ]","$","(li|il[$english])"),  # Apple < Appel
                   ("lE","[bdfgkmnprsStvzZ]","","(li|il[$english]|lY[$german])"),  # Applebaum < Appelbaum

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
                   ("iA","","","(ia|io|iY[$german])"),
                   ("A","","[^aeiouAEBFIOU]e","(a|o|Y[$german]|D[$english])"), # "plane"

                   ("E","i[^aeiouAEIOU]","","(i|Y[$german]|[$english])"), # Wineberg (vineberg/vajneberg) --> vajnberg
                   ("E","a[^aeiouAEIOU]","","(i|Y[$german]|[$english])"), #  Shaneberg (shaneberg/shejneberg) --> shejnberg

                   ("e", "", "[fklmnprstv]$", "i"),
                   ("e", "", "ts$", "i"),
                   ("e", "", "$", "i"),
                   ("e", "[DaoiuAOIUQY]", "", "i"),
                   ("e", "", "[aoAOQY]", "i"),
                   ("e", "", "", "(i|Y[$german])"),

                   ("E", "", "[fklmnprst]$", "i"),
                   ("E", "", "ts$", "i"),
                   ("E", "", "$", "i"),
                   ("E", "[DaoiuAOIUQY]", "", "i"),
                   ("E", "", "[aoAOQY]", "i"),
                   ("E", "", "", "(i|Y[$german])"),

                   ("a", "", "", "(a|o)"),

                   ("O", "", "[fklmnprstv]$", "o"),
                   ("O", "", "ts$", "o"),
                   ("O", "", "$", "o"),
                   ("O", "[oeiuQY]", "", "o"),
                   ("O", "", "", "(o|Y[$german])"),

                   ("A", "", "[fklmnprst]$", "(a|o)"),
                   ("A", "", "ts$", "(a|o)"),
                   ("A", "", "$", "(a|o)"),
                   ("A", "[oeiuQY]", "", "(a|o)"),
                   ("A", "", "", "(a|o|Y[$german])"),

                   ("U", "", "$", "u"),
                   ("U", "[DoiuQY]", "", "u"),
                   ("U", "", "[^k]$", "u"),
                   ("Uk", "[lr]", "$", "(uk|Qk[$german])"),
                   ("Uk", "", "$", "uk"),

                   ("sUts", "", "$", "(suts|sQts[$german])"),
                   ("Uts", "", "$", "uts"),
                   ("U", "", "", "(u|Q[$german])"),



                   )
