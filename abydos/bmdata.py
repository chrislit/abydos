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

bmdata = dict()

bmdata['gen'] = dict()

bmdata['gen']['approx_german'] = (

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

bmdata['gen']['approx_common'] = (
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

                      # lander = lender = länder
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

bmdata['gen']['rules_cyrillic'] = (
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

bmdata['gen']['rules_czech'] = (
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

bmdata['gen']['rules_english'] = (
                      # CONSONANTS
                      ("’","","",""), # O’Neill
                      ("'","","",""), # O’Neill
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

bmdata['gen']['exact_hungarian'] = (
                        )

bmdata['gen']['approx_portuguese'] = (
                          )

bmdata['gen']['exact_portuguese'] = (
                         )

bmdata['gen']['exact_turkish'] = (
                      )

bmdata['gen']['exact_cyrillic'] = (
                       )

bmdata['gen']['exact_french'] = (
                     )

bmdata['gen']['approx_english'] = (
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

bmdata['gen']['approx_russian'] = (
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

bmdata['gen']['exact_german'] = (
                     )

bmdata['gen']['exact_russian'] = (
                      ("E", "", "", "e"),
                      ("I", "", "", "i"),

                      )

bmdata['gen']['rules_dutch'] = (
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

bmdata['gen']['rules_italian'] = (
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

                      ("è","","","e"),
                      ("é","","","e"),
                      ("ò","","","o"),
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

bmdata['gen']['exact_common'] = (
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

bmdata['gen']['rules_hebrew'] = (
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

bmdata['gen']['approx_turkish'] = (
                       )

bmdata['gen']['rules_spanish'] = (
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

bmdata['gen']['rules_hungarian'] = (
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

bmdata['gen']['approx_spanish'] = (
                       ("B","","","(b|v)"),
                       ("V","","","(b|v)"),

                       )

bmdata['gen']['exact_english'] = (
                      )

bmdata['gen']['approx_greeklatin'] = (
                          ("N","","",""),

                          )

bmdata['gen']['exact_hebrew'] = (
                     )

bmdata['gen']['approx_hungarian'] = (
                         )

bmdata['gen']['approx_dutch'] = (
                     )

bmdata['gen']['approx_polish'] = (
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

bmdata['gen']['rules_romanian'] = (
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

bmdata['gen']['approx_any'] = (
                   # VOWELS
                   # "ALL" DIPHTHONGS are interchangeable BETWEEN THEM and with monophthongs of which they are composed ("D" means "diphthong")
                   #  {a,o} are totally interchangeable if non-stressed; in German "a/o" can actually be from "ä/ö" (that are equivalent to "e")
                   #  {i,e} are interchangeable if non-stressed, while in German "u" can actually be from "ü" (that is equivalent to "i")

                   ("mb","","","(mb|b[$greeklatin])"),
                   ("mp","","","(mp|b[$greeklatin])"),
                   ("ng","","","(ng|g[$greeklatin])"),

                   ("B","","[fktSs]","(p|f[$spanish])"),
                   ("B","","p",""),
                   ("B","","$","(p|f[$spanish])"),
                   ("V","","[pktSs]","(f|p[$spanish])"),
                   ("V","","f",""),
                   ("V","","$","(f|p[$spanish])"),

                   ("B","","","(b|v[$spanish])"),
                   ("V","","","(v|b[$spanish])"),

                   # French word-final and word-part-final letters
                   ("t","","$","(t|[$french])"),
                   ("g","n","$","(g|[$french])"),
                   ("k","n","$","(k|[$french])"),
                   ("p","","$","(p|[$french])"),
                   ("r","[Ee]","$","(r|[$french])"),
                   ("s","","$","(s|[$french])"),
                   ("t","[aeiouAEIOU]","[^aeiouAEIOU]","(t|[$french])"), # Petitjean
                   ("s","[aeiouAEIOU]","[^aeiouAEIOU]","(s|[$french])"), # Groslot, Grosleau
                   #("p","[aeiouAEIOU]","[^aeiouAEIOU]","(p|[$french])"),

                   ("I", "[aeiouAEIBFOUQY]", "", "i"),
                   ("I","","[^aeiouAEBFIOU]e","(Q[$german]|i|D[$english])"),  # "line"
                   ("I", "", "$", "i"),
                   ("I", "", "[^k]$", "i"),
                   ("Ik", "[lr]", "$", "(ik|Qk[$german])"),
                   ("Ik", "", "$", "ik"),
                   ("sIts", "", "$", "(sits|sQts[$german])"),
                   ("Its", "", "$", "its"),
                   ("I", "", "", "(Q[$german]|i)"),

                   ("lEE","[bdfgkmnprsStvzZ]","","(li|il[$english])"),  # Apple = Appel
                   ("rEE","[bdfgkmnprsStvzZ]","","(ri|ir[$english])"),
                   ("lE","[bdfgkmnprsStvzZ]","","(li|il[$english]|lY[$german])"),  # Applebaum < Appelbaum
                   ("rE","[bdfgkmnprsStvzZ]","","(ri|ir[$english]|rY[$german])"),

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
                   ("iA","","","(ia|io|iY[$german])"),
                   ("A","","[^aeiouAEBFIOU]e","(a|o|Y[$german]|D[$english])"), # "plane"

                   ("E","i[^aeiouAEIOU]","","(i|Y[$german]|[$english])"), # Wineberg (vineberg/vajneberg) --> vajnberg
                   ("E","a[^aeiouAEIOU]","","(i|Y[$german]|[$english])"), #  Shaneberg (shaneberg/shejneberg) --> shejnberg

                   ("E", "", "[fklmnprst]$", "i"),
                   ("E", "", "ts$", "i"),
                   ("E", "", "$", "i"),
                   ("E", "[DaoiuAOIUQY]", "", "i"),
                   ("E", "", "[aoAOQY]", "i"),
                   ("E", "", "", "(i|Y[$german])"),

                   ("P", "", "", "(o|u)"),

                   ("O", "", "[fklmnprstv]$", "o"),
                   ("O", "", "ts$", "o"),
                   ("O", "", "$", "o"),
                   ("O", "[oeiuQY]", "", "o"),
                   ("O", "", "", "(o|Y[$german])"),
                   ("O", "", "", "o"),

                   ("A", "", "[fklmnprst]$", "(a|o)"),
                   ("A", "", "ts$", "(a|o)"),
                   ("A", "", "$", "(a|o)"),
                   ("A", "[oeiuQY]", "", "(a|o)"),
                   ("A", "", "", "(a|o|Y[$german])"),
                   ("A", "", "", "(a|o)"),

                   ("U", "", "$", "u"),
                   ("U", "[DoiuQY]", "", "u"),
                   ("U", "", "[^k]$", "u"),
                   ("Uk", "[lr]", "$", "(uk|Qk[$german])"),
                   ("Uk", "", "$", "uk"),
                   ("sUts", "", "$", "(suts|sQts[$german])"),
                   ("Uts", "", "$", "uts"),
                   ("U", "", "", "(u|Q[$german])"),
                   ("U", "", "", "u"),

                   ("e", "", "[fklmnprstv]$", "i"),
                   ("e", "", "ts$", "i"),
                   ("e", "", "$", "i"),
                   ("e", "[DaoiuAOIUQY]", "", "i"),
                   ("e", "", "[aoAOQY]", "i"),
                   ("e", "", "", "(i|Y[$german])"),

                   ("a", "", "", "(a|o)"),

                   )

bmdata['gen']['exact_spanish'] = (
                      ("B", "", "", "b"),
                      ("V", "", "", "v"),

                      )

bmdata['gen']['rules_french'] = (
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

bmdata['gen']['rules_arabic'] = (
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

bmdata['gen']['rules_greeklatin'] = (
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

bmdata['gen']['rules_portuguese'] = (
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

bmdata['gen']['hebrew_common'] = (
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

bmdata['gen']['rules_russian'] = (
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

bmdata['gen']['rules_german'] = (
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

bmdata['gen']['exact_czech'] = (
                    )

bmdata['gen']['approx_romanian'] = (
                        )

bmdata['gen']['rules_any'] = (
                  # CONVERTING FEMININE TO MASCULINE
                  ("yna","","$","(in[$russian]|ina)"),
                  ("ina","","$","(in[$russian]|ina)"),
                  ("liova","","$","(lova|lof[$russian]|lef[$russian])"),
                  ("lova","","$","(lova|lof[$russian]|lef[$russian]|l[$czech]|el[$czech])"),
                  ("kova","","$","(kova|kof[$russian]|k[$czech]|ek[$czech])"),
                  ("ova","","$","(ova|of[$russian]|[$czech])"),
                  ("ová","","$","(ova|[$czech])"),
                  ("eva","","$","(eva|ef[$russian])"),
                  ("aia","","$","(aja|i[$russian])"),
                  ("aja","","$","(aja|i[$russian])"),
                  ("aya","","$","(aja|i[$russian])"),

                  ("lowa","","$","(lova|lof[$polish]|l[$polish]|el[$polish])"),
                  ("kowa","","$","(kova|kof[$polish]|k[$polish]|ek[$polish])"),
                  ("owa","","$","(ova|of[$polish]|)"),
                  ("lowna","","$","(lovna|levna|l[$polish]|el[$polish])"),
                  ("kowna","","$","(kovna|k[$polish]|ek[$polish])"),
                  ("owna","","$","(ovna|[$polish])"),
                  ("lówna","","$","(l|el)"),  # polish
                  ("kówna","","$","(k|ek)"),  # polish
                  ("ówna","","$",""),         # polish
                  ("á","","$","(a|i[$czech])"),
                  ("a","","$","(a|i[$polish+$czech])"),

                  # CONSONANTS
                  ("pf","","","(pf|p|f)"),
                  ("que","","$","(k[$french]|ke|kve)"),
                  ("qu","","","(kv|k)"),

                  ("m","","[bfpv]","(m|n)"),
                  ("m","[aeiouy]","[aeiouy]", "m"),
                  ("m","[aeiouy]","", "(m|n[$french+$portuguese])"),  # nasal

                  ("ly","","[au]","l"),
                  ("li","","[au]","l"),
                  ("lio","","","(lo|le[$russian])"),
                  ("lyo","","","(lo|le[$russian])"),
                  #("ll","","","(l|J[$spanish])"),  # Disabled Argentinian rule
                  ("lt","u","$","(lt|[$french])"),

                  ("v","^","","(v|f[$german]|b[$spanish])"),

                  ("ex","","[aáuiíoóeéêy]","(ez[$portuguese]|eS[$portuguese]|eks|egz)"),
                  ("ex","","[cs]","(e[$portuguese]|ek)"),
                  ("x","u","$","(ks|[$french])"),

                  ("ck","","","(k|tsk[$polish+$czech])"),
                  ("cz","","","(tS|tsz[$czech])"), # Polish

                  #Proceccing of "h" in various combinations
                  ("rh","^","","r"),
                  ("dh","^","","d"),
                  ("bh","^","","b"),

                  ("ph","","","(ph|f)"),
                  ("kh","","","(x[$russian+$english]|kh)"),

                  ("lh","","","(lh|l[$portuguese])"),
                  ("nh","","","(nh|nj[$portuguese])"),

                  ("ssch","","","S"),      # german
                  ("chsch","","","xS"),    # german
                  ("tsch","","","tS"),     # german

                  #/ ("desch","^","","deS"),
                  #/ ("desh","^","","(dES|de[$french])"),
                  #/ ("des","^","[^aeiouy]","(dEs|de[$french])"),

                  ("sch","[aeiouy]","[ei]","(S|StS[$russian]|sk[$romanian+$italian])"),
                  ("sch","[aeiouy]","","(S|StS[$russian])"),
                  ("sch","","[ei]","(sk[$romanian+$italian]|S|StS[$russian])"),
                  ("sch","","","(S|StS[$russian])"),
                  ("ssh","","","S"),

                  ("sh","","[äöü]","sh"),      # german
                  ("sh","","[aeiou]","(S[$russian+$english]|sh)"),
                  ("sh","","","S"),

                  ("zh","","","(Z[$english+$russian]|zh|tsh[$german])"),

                  ("chs","","","(ks[$german]|xs|tSs[$russian+$english])"),
                  ("ch","","[ei]","(x|tS[$spanish+$english+$russian]|k[$romanian+$italian]|S[$portuguese+$french])"),
                  ("ch","","","(x|tS[$spanish+$english+$russian]|S[$portuguese+$french])"),

                  ("th","^","","t"),     # english+german+greeklatin
                  ("th","","[äöüaeiou]","(t[$english+$german+$greeklatin]|th)"),
                  ("th","","","t"),  # english+german+greeklatin

                  ("gh","","[ei]","(g[$romanian+$italian+$greeklatin]|gh)"),

                  ("ouh","","[aioe]","(v[$french]|uh)"),
                  ("uh","","[aioe]","(v|uh)"),
                  ("h","","$",""),
                  ("h","[aeiouyäöü]","",""),  # $german
                  ("h","^","","(h|x[$romanian+$greeklatin]|H[$english+$romanian+$polish+$french+$portuguese+$italian+$spanish])"),

                  #Processing of "ci", "ce" & "cy"
                  ("cia","","","(tSa[$polish]|tsa)"),  # Polish
                  ("cią","","[bp]","(tSom|tsom)"),     # Polish
                  ("cią","","","(tSon[$polish]|tson)"), # Polish
                  ("cię","","[bp]","(tSem[$polish]|tsem)"), # Polish
                  ("cię","","","(tSen[$polish]|tsen)"), # Polish
                  ("cie","","","(tSe[$polish]|tse)"),  # Polish
                  ("cio","","","(tSo[$polish]|tso)"),  # Polish
                  ("ciu","","","(tSu[$polish]|tsu)"), # Polish

                  ("sci","","$","(Si[$italian]|stsi[$polish+$czech]|dZi[$turkish]|tSi[$polish+$romanian]|tS[$romanian]|si)"),
                  ("sc","","[ei]","(S[$italian]|sts[$polish+$czech]|dZ[$turkish]|tS[$polish+$romanian]|s)"),
                  ("ci","","$","(tsi[$polish+$czech]|dZi[$turkish]|tSi[$polish+$romanian]|tS[$romanian]|si)"),
                  ("cy","","","(si|tsi[$polish])"),
                  ("c","","[ei]","(ts[$polish+$czech]|dZ[$turkish]|tS[$polish+$romanian]|k[$greeklatin]|s)"),

                  #Processing of "s"
                  ("sç","","[aeiou]","(s|stS[$turkish])"),
                  ("ssz","","","S"), # polish
                  ("sz","^","","(S|s[$hungarian])"), # polish
                  ("sz","","$","(S|s[$hungarian])"), # polish
                  ("sz","","","(S|s[$hungarian]|sts[$german])"), # polish
                  ("ssp","","","(Sp[$german]|sp)"),
                  ("sp","","","(Sp[$german]|sp)"),
                  ("sst","","","(St[$german]|st)"),
                  ("st","","","(St[$german]|st)"),
                  ("ss","","","s"),
                  ("sj","^","","S"), # dutch
                  ("sj","","$","S"), # dutch
                  ("sj","","","(sj|S[$dutch]|sx[$spanish]|sZ[$romanian+$turkish])"),

                  ("sia","","","(Sa[$polish]|sa[$polish]|sja)"),
                  ("sią","","[bp]","(Som[$polish]|som)"), # polish
                  ("sią","","","(Son[$polish]|son)"), # polish
                  ("się","","[bp]","(Sem[$polish]|sem)"), # polish
                  ("się","","","(Sen[$polish]|sen)"), # polish
                  ("sie","","","(se|sje|Se[$polish]|zi[$german])"),

                  ("sio","","","(So[$polish]|so)"),
                  ("siu","","","(Su[$polish]|sju)"),

                  ("si","[äöëaáuiíoóeéêy]","","(Si[$polish]|si|zi[$portuguese+$french+$italian+$german])"),
                  ("si","","","(Si[$polish]|si|zi[$german])"),
                  ("s","[aáuiíoóeéêy]","[aáuíoóeéêy]","(s|z[$portuguese+$french+$italian+$german])"),
                  ("s","","[aeouäöë]","(s|z[$german])"),
                  ("s","[aeiouy]","[dglmnrv]","(s|z|Z[$portuguese]|[$french])"), # Groslot
                  ("s","","[dglmnrv]","(s|z|Z[$portuguese])"),

                  #Processing of "g"
                  ("gue","","$","(k[$french]|gve)"),  # portuguese+spanish
                  ("gu","","[ei]","(g[$french]|gv[$portuguese+$spanish])"), # portuguese+spanish
                  ("gu","","[ao]","gv"),     # portuguese+spanish
                  ("guy","","","gi"),  # french

                  ("gli","","","(glI|l[$italian])"),
                  ("gni","","","(gnI|ni[$italian+$french])"),
                  ("gn","","[aeou]","(n[$italian+$french]|nj[$italian+$french]|gn)"),

                  ("ggie","","","(je[$greeklatin]|dZe)"), # dZ is Italian
                  ("ggi","","[aou]","(j[$greeklatin]|dZ)"), # dZ is Italian

                  ("ggi","[yaeiou]","[aou]","(gI|dZ[$italian]|j[$greeklatin])"),
                  ("gge","[yaeiou]","","(gE|xe[$spanish]|gZe[$portuguese+$french]|dZe[$english+$romanian+$italian+$spanish]|je[$greeklatin])"),
                  ("ggi","[yaeiou]","","(gI|xi[$spanish]|gZi[$portuguese+$french]|dZi[$english+$romanian+$italian+$spanish]|i[$greeklatin])"),
                  ("ggi","","[aou]","(gI|dZ[$italian]|j[$greeklatin])"),

                  ("gie","","$","(ge|gi[$german]|ji[$french]|dZe[$italian])"),
                  ("gie","","","(ge|gi[$german]|dZe[$italian]|je[$greeklatin])"),
                  ("gi","","[aou]","(i[$greeklatin]|dZ)"), # dZ is Italian

                  ("ge","[yaeiou]","","(gE|xe[$spanish]|Ze[$portuguese+$french]|dZe[$english+$romanian+$italian+$spanish])"),
                  ("gi","[yaeiou]","","(gI|xi[$spanish]|Zi[$portuguese+$french]|dZi[$english+$romanian+$italian+$spanish])"),
                  ("ge","","","(gE|xe[$spanish]|hE[$russian]|je[$greeklatin]|Ze[$portuguese+$french]|dZe[$english+$romanian+$italian+$spanish])"),
                  ("gi","","","(gI|xi[$spanish]|hI[$russian]|i[$greeklatin]|Zi[$portuguese+$french]|dZi[$english+$romanian+$italian+$spanish])"),
                  ("gy","","[aeouáéóúüöőű]","(gi|dj[$hungarian])"),
                  ("gy","","","(gi|d[$hungarian])"),
                  ("g","[yaeiou]","[aouyei]","g"),
                  ("g","","[aouei]","(g|h[$russian])"),

                  #Processing of "j"
                  ("ij","","","(i|ej[$dutch]|ix[$spanish]|iZ[$french+$romanian+$turkish+$portuguese])"),
                  ("j","","[aoeiuy]","(j|dZ[$english]|x[$spanish]|Z[$french+$romanian+$turkish+$portuguese])"),

                  #Processing of "z"
                  ("rz","t","","(S[$polish]|r)"), # polish
                  ("rz","","","(rz|rts[$german]|Z[$polish]|r[$polish]|rZ[$polish])"),

                  ("tz","","$","(ts|tS[$english+$german])"),
                  ("tz","^","","(ts[$english+$german+$russian]|tS[$english+$german])"),
                  ("tz","","","(ts[$english+$german+$russian]|tz)"),

                  ("zia","","[bcdgkpstwzż]","(Za[$polish]|za[$polish]|zja)"),
                  ("zia","","","(Za[$polish]|zja)"),
                  ("zią","","[bp]","(Zom[$polish]|zom)"),  # polish
                  ("zią","","","(Zon[$polish]|zon)"), # polish
                  ("zię","","[bp]","(Zem[$polish]|zem)"), # polish
                  ("zię","","","(Zen[$polish]|zen)"), # polish
                  ("zie","","[bcdgkpstwzż]","(Ze[$polish]|ze[$polish]|ze|tsi[$german])"),
                  ("zie","","","(ze|Ze[$polish]|tsi[$german])"),
                  ("zio","","","(Zo[$polish]|zo)"),
                  ("ziu","","","(Zu[$polish]|zju)"),
                  ("zi","","","(Zi[$polish]|zi|tsi[$german]|dzi[$italian]|tsi[$italian]|si[$spanish])"),

                  ("z","","$","(s|ts[$german]|ts[$italian]|S[$portuguese])"), # ts It, s/S/Z Port, s in Sp, z Fr
                  ("z","","[bdgv]","(z|dz[$italian]|Z[$portuguese])"), # dz It, Z/z Port, z Sp & Fr
                  ("z","","[ptckf]","(s|ts[$italian]|S[$portuguese])"), # ts It, s/S/z Port, z/s Sp

                  # VOWELS
                  ("aue","","","aue"),
                  ("oue","","","(oue|ve[$french])"),
                  ("eau","","","o"), # French

                  ("ae","","","(Y[$german]|aje[$russian]|ae)"),
                  ("ai","","","aj"),
                  ("au","","","(au|o[$french])"),
                  ("ay","","","aj"),
                  ("ão","","","(au|an)"), # Port
                  ("ãe","","","(aj|an)"), # Port
                  ("ãi","","","(aj|an)"), # Port
                  ("ea","","","(ea|ja[$romanian])"),
                  ("ee","","","(i[$english]|aje[$russian]|e)"),
                  ("ei","","","(aj|ej)"),
                  ("eu","","","(eu|Yj[$german]|ej[$german]|oj[$german]|Y[$dutch])"),
                  ("ey","","","(aj|ej)"),
                  ("ia","","","ja"),
                  ("ie","","","(i[$german]|e[$polish]|ije[$russian]|Q[$dutch]|je)"),
                  ("ii","","$","i"), # russian
                  ("io","","","(jo|e[$russian])"),
                  ("iu","","","ju"),
                  ("iy","","$","i"), # russian
                  ("oe","","","(Y[$german]|oje[$russian]|u[$dutch]|oe)"),
                  ("oi","","","oj"),
                  ("oo","","","(u[$english]|o)"),
                  ("ou","","","(ou|u[$french+$greeklatin]|au[$dutch])"),
                  ("où","","","u"), # french
                  ("oy","","","oj"),
                  ("õe","","","(oj|on)"), # Port
                  ("ua","","","va"),
                  ("ue","","","(Q[$german]|uje[$russian]|ve)"),
                  ("ui","","","(uj|vi|Y[$dutch])"),
                  ("uu","","","(u|Q[$dutch])"),
                  ("uo","","","(vo|o)"),
                  ("uy","","","uj"),
                  ("ya","","","ja"),
                  ("ye","","","(je|ije[$russian])"),
                  ("yi","^","","i"),
                  ("yi","","$","i"), # russian
                  ("yo","","","(jo|e[$russian])"),
                  ("yu","","","ju"),
                  ("yy","","$","i"), # russian

                  ("i","[áóéê]","","j"),
                  ("y","[áóéê]","","j"),

                  ("e","^","","(e|je[$russian])"),
                  ("e","","$","(e|EE[$english+$french])"),

                  # LANGUAGE SPECIFIC CHARACTERS
                  ("ą","","[bp]","om"), # polish
                  ("ą","","","on"),  # polish
                  ("ä","","","(Y|e)"),
                  ("á","","","a"), # Port & Sp
                  ("à","","","a"),
                  ("â","","","a"),
                  ("ã","","","(a|an)"), # Port
                  ("ă","","","(e[$romanian]|a)"), # romanian
                  ("č","","", "tS"), # czech
                  ("ć","","","(tS[$polish]|ts)"),  # polish
                  ("ç","","","(s|tS[$turkish])"),
                  ("ď","","","(d|dj[$czech])"),
                  ("ę","","[bp]","em"), # polish
                  ("ę","","","en"), # polish
                  ("é","","","e"),
                  ("è","","","e"),
                  ("ê","","","e"),
                  ("ě","","","(e|je[$czech])"),
                  ("ğ","","",""), # turkish
                  ("í","","","i"),
                  ("î","","","i"),
                  ("ı","","","(i|e[$turkish]|[$turkish])"),
                  ("ł","","","l"),
                  ("ń","","","(n|nj[$polish])"), # polish
                  ("ñ","","","(n|nj[$spanish])"),
                  ("ó","","","(u[$polish]|o)"),
                  ("ô","","","o"), # Port & Fr
                  ("õ","","","(o|on[$portuguese]|Y[$hungarian])"),
                  ("ò","","","o"),  # Sp & It
                  ("ö","","","Y"),
                  ("ř","","","(r|rZ[$czech])"),
                  ("ś","","","(S[$polish]|s)"),
                  ("ş","","","S"), # romanian+turkish
                  ("š","","", "S"), # czech
                  ("ţ","","","ts"),  # romanian
                  ("ť","","","(t|tj[$czech])"),
                  ("ű","","","Q"), # hungarian
                  ("ü","","","(Q|u[$portuguese+$spanish])"),
                  ("ú","","","u"),
                  ("ů","","","u"), # czech
                  ("ù","","","u"), # french
                  ("ý","","","i"),  # czech
                  ("ż","","","Z"), # polish
                  ("ź","","","(Z[$polish]|z)"),

                  ("ß","","","s"), # german
                  ("'","","",""), # russian
                  ('"',"","",""), # russian

                  ("o","","[bcćdgklłmnńrsśtwzźż]","(O|P[$polish])"),

                  # LATIN ALPHABET
                  ("a","","","A"),
                  ("b","","","B"),
                  ("c","","","(k|ts[$polish+$czech]|dZ[$turkish])"),
                  ("d","","","d"),
                  ("e","","","E"),
                  ("f","","","f"),
                  #("g","","","(g|x[$dutch])"), # Dutch sound disabled
                  ("g","","","g"),
                  ("h","","","(h|x[$romanian]|H[$french+$portuguese+$italian+$spanish])"),
                  ("i","","","I"),
                  ("j","","","(j|x[$spanish]|Z[$french+$romanian+$turkish+$portuguese])"),
                  ("k","","","k"),
                  ("l","","","l"),
                  ("m","","","m"),
                  ("n","","","n"),
                  ("o","","","O"),
                  ("p","","","p"),
                  ("q","","","k"),
                  ("r","","","r"),
                  ("s","","","(s|S[$portuguese])"),
                  ("t","","","t"),
                  ("u","","","U"),
                  ("v","","","V"),
                  ("w","","","(v|w[$english+$dutch])"),
                  ("x","","","(ks|gz|S[$portuguese+$spanish])"),   # S/ks Port & Sp, gz Sp, It only ks
                  ("y","","","i"),
                  ("z","","","(z|ts[$german]|dz[$italian]|ts[$italian]|s[$spanish])"), # ts/dz It, z Port & Fr, z/s Sp

                  )

bmdata['gen']['approx_cyrillic'] = (
                        )

bmdata['gen']['exact_romanian'] = (
                       )

bmdata['gen']['approx_czech'] = (
                     )

bmdata['gen']['approx_greek'] = (
                     )

bmdata['gen']['exact_arabic'] = (
                     ("1", "", "", ""),

                     )

bmdata['gen']['rules_greek'] = (
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

bmdata['gen']['rules_polish'] = (
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

bmdata['gen']['approx_hebrew'] = (
                      )

bmdata['gen']['exact_approxcommon'] = (
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

bmdata['gen']['approx_arabic'] = (

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

bmdata['gen']['exact_any'] = (
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

bmdata['gen']['exact_polish'] = (
                     ("B", "", "", "a"),
                     ("F", "", "", "e"),
                     ("P", "", "", "o"),

                     ("E", "", "", "e"),
                     ("I", "", "", "i"),

                     )

bmdata['gen']['rules_turkish'] = (
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

bmdata['gen']['exact_italian'] = (
                      )

bmdata['gen']['exact_greeklatin'] = (
                         ("N","","","n"),

                         )

bmdata['gen']['approx_italian'] = (
                       )

bmdata['gen']['approx_french'] = (
                      ("au","","","(D|a|u)"),
                      ("ou","","","(D|o|u)"),
                      ("ai","","","(D|a|i)"),
                      ("oi","","","(D|o|i)"),
                      ("ui","","","(D|u|i)"),

                      ("a", "", "", "(a|o)"),
                      ("e", "", "", "i"),

                      )

bmdata['gen']['exact_dutch'] = (
                    )

bmdata['gen']['exact_greek'] = (
                    )

bmdata['sep'] = dict()

bmdata['sep']['approx_common'] = (
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

                      #/  ("s", "", "$", "(s|)"), # Attia(s)
                      #/  ("C", "", "", "s"),  # "c" could actually be "ç"

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

bmdata['sep']['approx_portuguese'] = (
                          )

bmdata['sep']['exact_portuguese'] = (
                         )

bmdata['sep']['exact_french'] = (
                     )

bmdata['sep']['rules_italian'] = (
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

                      ("è","","","e"),
                      ("é","","","e"),
                      ("ò","","","o"),
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

bmdata['sep']['exact_common'] = (
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

bmdata['sep']['rules_hebrew'] = (
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

bmdata['sep']['rules_spanish'] = (
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

bmdata['sep']['approx_spanish'] = (
                       )

bmdata['sep']['exact_hebrew'] = (
                     )

bmdata['sep']['approx_any'] = (
                   ("E","","",""), # Final French "e"

                   )

bmdata['sep']['exact_spanish'] = (
                      )

bmdata['sep']['rules_french'] = (
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

bmdata['sep']['rules_portuguese'] = (
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

bmdata['sep']['hebrew_common'] = (
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

bmdata['sep']['rules_any'] = (
                  # CONSONANTS
                  ("ph","","","f"), # foreign
                  ("sh","","","S"), # foreign
                  ("kh","","","x"), # foreign

                  ("gli","","","(gli|l[$italian])"),
                  ("gni","","","(gni|ni[$italian+$french])"),
                  ("gn","","[aeou]","(n[$italian+$french]|nj[$italian+$french]|gn)"),
                  ("gh","","","g"), # It + translit. from Arabic
                  ("dh","","","d"), # translit. from Arabic
                  ("bh","","","b"), # translit. from Arabic
                  ("th","","","t"), # translit. from Arabic
                  ("lh","","","l"), # Port
                  ("nh","","","nj"), # Port

                  ("ig","[aeiou]","","(ig|tS[$spanish])"),
                  ("ix","[aeiou]","","S"), # Sp
                  ("tx","","","tS"), # Sp
                  ("tj","","$","tS"), # Sp
                  ("tj","","","dZ"), # Sp
                  ("tg","","","(tg|dZ[$spanish])"),

                  ("gi","","[aeou]","dZ"), # italian
                  ("g","","y","Z"), # french
                  ("gg","","[ei]","(gZ[$portuguese+$french]|dZ[$italian+$spanish]|x[$spanish])"),
                  ("g","","[ei]","(Z[$portuguese+$french]|dZ[$italian+$spanish]|x[$spanish])"),

                  ("guy","","","gi"),
                  ("gue","","$","(k[$french]|ge)"),
                  ("gu","","[ei]","(g|gv)"),     # not It
                  ("gu","","[ao]","gv"),  # not It

                  ("ñ","","","(n|nj)"),
                  ("ny","","","nj"),

                  ("sc","","[ei]","(s|S[$italian])"),
                  ("sç","","[aeiou]","s"), # not It
                  ("ss","","","s"),
                  ("ç","","","s"),   # not It

                  ("ch","","[ei]","(k[$italian]|S[$portuguese+$french]|tS[$spanish]|dZ[$spanish])"),
                  ("ch","","","(S|tS[$spanish]|dZ[$spanish])"),

                  ("ci","","[aeou]","(tS[$italian]|si)"),
                  ("cc","","[eiyéèê]","(tS[$italian]|ks[$portuguese+$french+$spanish])"),
                  ("c","","[eiyéèê]","(tS[$italian]|s[$portuguese+$french+$spanish])"),
                  #("c","","[aou]","(k|C[$portuguese+$spanish])"), # "C" means that the actual letter could be "ç" (cedille omitted)

                  ("s","^","","s"),
                  ("s","[aáuiíoóeéêy]","[aáuiíoóeéêy]","(s[$spanish]|z[$portuguese+$french+$italian])"),
                  ("s","","[dglmnrv]","(z|Z[$portuguese])"),

                  ("z","","$","(s|ts[$italian]|S[$portuguese])"), # ts It, s/S/Z Port, s in Sp, z Fr
                  ("z","","[bdgv]","(z|dz[$italian]|Z[$portuguese])"), # dz It, Z/z Port, z Sp & Fr
                  ("z","","[ptckf]","(s|ts[$italian]|S[$portuguese])"), # ts It, s/S/z Port, z/s Sp
                  ("z","","","(z|dz[$italian]|ts[$italian]|s[$spanish])"), # ts/dz It, z Port & Fr, z/s Sp

                  ("que","","$","(k[$french]|ke)"),
                  ("qu","","[eiu]","k"),
                  ("qu","","[ao]","(kv|k)"), # k is It

                  ("ex","","[aáuiíoóeéêy]","(ez[$portuguese]|eS[$portuguese]|eks|egz)"),
                  ("ex","","[cs]","(e[$portuguese]|ek)"),

                  ("m","","[cdglnrst]","(m|n[$portuguese])"),
                  ("m","","[bfpv]","(m|n[$portuguese+$spanish])"),
                  ("m","","$","(m|n[$portuguese])"),

                  ("b","^","","(b|V[$spanish])"),
                  ("v","^","","(v|B[$spanish])"),

                  # VOWELS
                  ("eau","","","o"), # Fr

                  ("ouh","","[aioe]","(v[$french]|uh)"),
                  ("uh","","[aioe]","(v|uh)"),
                  ("ou","","[aioe]","v"), # french
                  ("uo","","","(vo|o)"),
                  ("u","","[aie]","v"),

                  ("i","[aáuoóeéê]","","j"),
                  ("i","","[aeou]","j"),
                  ("y","[aáuiíoóeéê]","","j"),
                  ("y","","[aeiíou]","j"),
                  ("e","","$","(e|E[$french])"),

                  ("ão","","","(au|an)"), # Port
                  ("ãe","","","(aj|an)"), # Port
                  ("ãi","","","(aj|an)"), # Port
                  ("õe","","","(oj|on)"), # Port
                  ("où","","","u"), # Fr
                  ("ou","","","(ou|u[$french])"),

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
                  ("b","","","(b|v[$spanish])"),
                  ("c","","","k"),
                  ("d","","","d"),
                  ("e","","","e"),
                  ("f","","","f"),
                  ("g","","","g"),
                  ("h","","","h"),
                  ("i","","","i"),
                  ("j","","","(x[$spanish]|Z)"), # not It
                  ("k","","","k"),
                  ("l","","","l"),
                  ("m","","","m"),
                  ("n","","","n"),
                  ("o","","","o"),
                  ("p","","","p"),
                  ("q","","","k"),
                  ("r","","","r"),
                  ("s","","","(s|S[$portuguese])"),
                  ("t","","","t"),
                  ("u","","","u"),
                  ("v","","","(v|b[$spanish])"),
                  ("w","","","v"),    # foreign
                  ("x","","","(ks|gz|S[$portuguese+$spanish])"),   # S/ks Port & Sp, gz Sp, It only ks
                  ("y","","","i"),
                  ("z","","","z"),

                  )

bmdata['sep']['approx_hebrew'] = (
                      )

bmdata['sep']['exact_approxcommon'] = (
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

bmdata['sep']['exact_any'] = (

                  ("E","","","e"), # final French "e"

                  )

bmdata['sep']['exact_italian'] = (
                      )

bmdata['sep']['approx_italian'] = (
                       )

bmdata['sep']['approx_french'] = (
                      )

bmdata['ash'] = dict()

bmdata['ash']['approx_german'] = (
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

bmdata['ash']['approx_common'] = (
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

                      # lander = lender = länder
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

bmdata['ash']['rules_cyrillic'] = (
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

bmdata['ash']['rules_english'] = (
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

bmdata['ash']['exact_hungarian'] = (
                        )

bmdata['ash']['exact_cyrillic'] = (
                       )

bmdata['ash']['exact_french'] = (
                     )

bmdata['ash']['approx_english'] = (
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

bmdata['ash']['approx_russian'] = (
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

bmdata['ash']['exact_german'] = (
                     )

bmdata['ash']['exact_russian'] = (
                      ("E", "", "", "e"),
                      ("I", "", "", "i"),

                      )

bmdata['ash']['exact_common'] = (
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

bmdata['ash']['rules_hebrew'] = (
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

bmdata['ash']['rules_spanish'] = (
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

bmdata['ash']['rules_hungarian'] = (
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

bmdata['ash']['approx_spanish'] = (
                       )

bmdata['ash']['exact_english'] = (
                      )

bmdata['ash']['exact_hebrew'] = (
                     )

bmdata['ash']['approx_hungarian'] = (
                         )

bmdata['ash']['approx_polish'] = (
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

bmdata['ash']['rules_romanian'] = (
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

bmdata['ash']['approx_any'] = (
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

bmdata['ash']['exact_spanish'] = (
                      )

bmdata['ash']['rules_french'] = (
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

bmdata['ash']['hebrew_common'] = (
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

bmdata['ash']['rules_russian'] = (
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
                      )

bmdata['ash']['rules_german'] = (

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

bmdata['ash']['approx_romanian'] = (
                        )

bmdata['ash']['rules_any'] = (
                  # CONVERTING FEMININE TO MASCULINE
                  ("yna","","$","(in[$russian]|ina)"),
                  ("ina","","$","(in[$russian]|ina)"),
                  ("liova","","$","(lof[$russian]|lef[$russian]|lova)"),
                  ("lova","","$","(lof[$russian]|lef[$russian]|lova)"),
                  ("ova","","$","(of[$russian]|ova)"),
                  ("eva","","$","(ef[$russian]|eva)"),
                  ("aia","","$","(aja|i[$russian])"),
                  ("aja","","$","(aja|i[$russian])"),
                  ("aya","","$","(aja|i[$russian])"),

                  ("lowa","","$","(lova|lof[$polish]|l[$polish]|el[$polish])"),
                  ("kowa","","$","(kova|kof[$polish]|k[$polish]|ek[$polish])"),
                  ("owa","","$","(ova|of[$polish]|)"),
                  ("lowna","","$","(lovna|levna|l[$polish]|el[$polish])"),
                  ("kowna","","$","(kovna|k[$polish]|ek[$polish])"),
                  ("owna","","$","(ovna|[$polish])"),
                  ("lówna","","$","(l|el[$polish])"),  # polish
                  ("kówna","","$","(k|ek[$polish])"),  # polish
                  ("ówna","","$",""),   # polish

                  ("a","","$","(a|i[$polish])"),

                  # CONSONANTS  (integrated: German, Polish, Russian, Romanian and English)

                  ("rh","^","","r"),
                  ("ssch","","","S"),
                  ("chsch","","","xS"),
                  ("tsch","","","tS"),

                  ("sch","","[ei]","(sk[$romanian]|S|StS[$russian])"), # german
                  ("sch","","","(S|StS[$russian])"), # german

                  ("ssh","","","S"),

                  ("sh","","[äöü]","sh"), # german
                  ("sh","","[aeiou]","(S[$russian+$english]|sh)"),
                  ("sh","","","S"), # russian+english

                  ("kh","","","(x[$russian+$english]|kh)"),

                  ("chs","","","(ks[$german]|xs|tSs[$russian+$english])"),

                  # French "ch" is currently disabled
                  #("ch","","[ei]","(x|tS|k[$romanian]|S[$french])"),
                  #("ch","","","(x|tS[$russian+$english]|S[$french])"),

                  ("ch","","[ei]","(x|k[$romanian]|tS[$russian+$english])"),
                  ("ch","","","(x|tS[$russian+$english])"),

                  ("ck","","","(k|tsk[$polish])"),

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

                  ("cia","","[bcdgkpstwzż]","(tSB[$polish]|tsB)"),
                  ("cia","","","(tSa[$polish]|tsa)"),
                  ("cią","","[bp]","(tSom[$polish]|tsom)"),
                  ("cią","","","(tSon[$polish]|tson)"),
                  ("cię","","[bp]","(tSem[$polish]|tsem)"),
                  ("cię","","","(tSen[$polish]|tsen)"),
                  ("cie","","[bcdgkpstwzż]","(tSF[$polish]|tsF)"),
                  ("cie","","","(tSe[$polish]|tse)"),
                  ("cio","","","(tSo[$polish]|tso)"),
                  ("ciu","","","(tSu[$polish]|tsu)"),

                  ("ci","","$","(tsi[$polish]|tSi[$polish+$romanian]|tS[$romanian]|si)"),
                  ("ci","","","(tsi[$polish]|tSi[$polish+$romanian]|si)"),
                  ("ce","","[bcdgkpstwzż]","(tsF[$polish]|tSe[$polish+$romanian]|se)"),
                  ("ce","","","(tSe[$polish+$romanian]|tse[$polish]|se)"),
                  ("cy","","","(si|tsi[$polish])"),

                  ("ssz","","","S"), # Polish
                  ("sz","","","S"), # Polish; actually could also be Hungarian /s/, disabled here

                  ("ssp","","","(Sp[$german]|sp)"),
                  ("sp","","","(Sp[$german]|sp)"),
                  ("sst","","","(St[$german]|st)"),
                  ("st","","","(St[$german]|st)"),
                  ("ss","","","s"),

                  ("sia","","[bcdgkpstwzż]","(SB[$polish]|sB[$polish]|sja)"),
                  ("sia","","","(Sa[$polish]|sja)"),
                  ("sią","","[bp]","(Som[$polish]|som)"),
                  ("sią","","","(Son[$polish]|son)"),
                  ("się","","[bp]","(Sem[$polish]|sem)"),
                  ("się","","","(Sen[$polish]|sen)"),
                  ("sie","","[bcdgkpstwzż]","(SF[$polish]|sF|zi[$german])"),
                  ("sie","","","(se|Se[$polish]|zi[$german])"),
                  ("sio","","","(So[$polish]|so)"),
                  ("siu","","","(Su[$polish]|sju)"),
                  ("si","","","(Si[$polish]|si|zi[$german])"),
                  ("s","","[aeiouäöë]","(s|z[$german])"),

                  ("gue","","","ge"),
                  ("gui","","","gi"),
                  ("guy","","","gi"),
                  ("gh","","[ei]","(g[$romanian]|gh)"),

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

                  ("gie","","$","(ge|gi[$german]|ji[$french])"),
                  ("gie","","","ge"),
                  ("ge","[yaeiou]","","(gE|xe[$spanish]|dZe[$english+$romanian])"),
                  ("gi","[yaeiou]","","(gI|xi[$spanish]|dZi[$english+$romanian])"),
                  ("ge","","","(gE|dZe[$english+$romanian]|hE[$russian]|xe[$spanish])"),
                  ("gi","","","(gI|dZi[$english+$romanian]|hI[$russian]|xi[$spanish])"),
                  ("gy","","[aeouáéóúüöőű]","(gi|dj[$hungarian])"),
                  ("gy","","","(gi|d[$hungarian])"),
                  ("g","[jyaeiou]","[aouyei]","g"),
                  ("g","","[aouei]","(g|h[$russian])"),

                  ("ej","","","(aj|eZ[$french+$romanian]|ex[$spanish])"),
                  ("ej","","","aj"),

                  ("ly","","[au]","l"),
                  ("li","","[au]","l"),
                  ("lj","","[au]","l"),
                  ("lio","","","(lo|le[$russian])"),
                  ("lyo","","","(lo|le[$russian])"),
                  ("ll","","","(l|J[$spanish])"),

                  ("j","","[aoeiuy]","(j|dZ[$english]|x[$spanish]|Z[$french+$romanian])"),
                  ("j","","","(j|x[$spanish])"),

                  ("pf","","","(pf|p|f)"),
                  ("ph","","","(ph|f)"),

                  ("qu","","","(kv[$german]|k)"),

                  ("rze","t","","(Se[$polish]|re)"), # polish
                  ("rze","","","(rze|rtsE[$german]|Ze[$polish]|re[$polish]|rZe[$polish])"),
                  ("rzy","t","","(Si[$polish]|ri)"), # polish
                  ("rzy","","","(Zi[$polish]|ri[$polish]|rZi)"),
                  ("rz","t","","(S[$polish]|r)"), # polish
                  ("rz","","","(rz|rts[$german]|Z[$polish]|r[$polish]|rZ[$polish])"), # polish

                  ("tz","","$","(ts|tS[$english+$german])"),
                  ("tz","^","","(ts|tS[$english+$german])"),
                  ("tz","","","(ts[$english+$german+$russian]|tz)"),

                  ("zh","","","(Z|zh[$polish]|tsh[$german])"),

                  ("zia","","[bcdgkpstwzż]","(ZB[$polish]|zB[$polish]|zja)"),
                  ("zia","","","(Za[$polish]|zja)"),
                  ("zią","","[bp]","(Zom[$polish]|zom)"),
                  ("zią","","","(Zon[$polish]|zon)"),
                  ("zię","","[bp]","(Zem[$polish]|zem)"),
                  ("zię","","","(Zen[$polish]|zen)"),
                  ("zie","","[bcdgkpstwzż]","(ZF[$polish]|zF[$polish]|ze|tsi[$german])"),
                  ("zie","","","(ze|Ze[$polish]|tsi[$german])"),
                  ("zio","","","(Zo[$polish]|zo)"),
                  ("ziu","","","(Zu[$polish]|zju)"),
                  ("zi","","","(Zi[$polish]|zi|tsi[$german])"),

                  ("thal","","$","tal"),
                  ("th","^","","t"),
                  ("th","","[aeiou]","(t[$german]|th)"),
                  ("th","","","t"), # german
                  ("vogel","","","(vogel|fogel[$german])"),
                  ("v","^","","(v|f[$german])"),

                  ("h","[aeiouyäöü]","",""), #german
                  ("h","","","(h|x[$romanian+$polish])"),
                  ("h","^","","(h|H[$english+$german])"), # H can be exact "h" or approximate "kh"

                  # VOWELS
                  ("yi","^","","i"),

                  # ("e","","$","(e|)"),  # French & English rule disabled except for final -ine
                  ("e","in","$","(e|[$french])"),

                  ("ii","","$","i"), # russian
                  ("iy","","$","i"), # russian
                  ("yy","","$","i"), # russian
                  ("yi","","$","i"), # russian
                  ("yj","","$","i"), # russian
                  ("ij","","$","i"), # russian

                  ("aue","","","aue"),
                  ("oue","","","oue"),

                  ("au","","","(au|o[$french])"),
                  ("ou","","","(ou|u[$french])"),

                  ("ue","","","(Q|uje[$russian])"),
                  ("ae","","","(Y[$german]|aje[$russian]|ae)"),
                  ("oe","","","(Y[$german]|oje[$russian]|oe)"),
                  ("ee","","","(i[$english]|aje[$russian]|e)"),

                  ("ei","","","aj"),
                  ("ey","","","aj"),
                  ("eu","","","(aj[$german]|oj[$german]|eu)"),

                  ("i","[aou]","","j"),
                  ("y","[aou]","","j"),

                  ("ie","","[bcdgkpstwzż]","(i[$german]|e[$polish]|ije[$russian]|je)"),
                  ("ie","","","(i[$german]|e[$polish]|ije[$russian]|je)"),
                  ("ye","","","(je|ije[$russian])"),

                  ("i","","[au]","j"),
                  ("y","","[au]","j"),
                  ("io","","","(jo|e[$russian])"),
                  ("yo","","","(jo|e[$russian])"),

                  ("ea","","","(ea|ja[$romanian])"),
                  ("e","^","","(e|je[$russian])"),
                  ("oo","","","(u[$english]|o)"),
                  ("uu","","","u"),

                  # LANGUAGE SPECIFIC CHARACTERS
                  ("ć","","","(tS[$polish]|ts)"),  # polish
                  ("ł","","","l"),  # polish
                  ("ń","","","n"),  # polish
                  ("ñ","","","(n|nj[$spanish])"),
                  ("ś","","","(S[$polish]|s)"), # polish
                  ("ş","","","S"),  # romanian
                  ("ţ","","","ts"),  # romanian
                  ("ż","","","Z"),  # polish
                  ("ź","","","(Z[$polish]|z)"), # polish

                  ("où","","","u"), # french

                  ("ą","","[bp]","om"),  # polish
                  ("ą","","","on"),  # polish
                  ("ä","","","(Y|e)"),  # german
                  ("á","","","a"), # hungarian
                  ("ă","","","(e[$romanian]|a)"), #romanian
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
                  ("ó","","","(u[$polish]|o)"),
                  ("ű","","","Q"),
                  ("ü","","","Q"),
                  ("ú","","","u"),
                  ("ű","","","Q"), # hungarian

                  ("ß","","","s"),  # german
                  ("'","","",""),
                  ('"',"","",""),

                  ("a","","[bcdgkpstwzż]","(A|B[$polish])"),
                  ("e","","[bcdgkpstwzż]","(E|F[$polish])"),
                  ("o","","[bcćdgklłmnńrsśtwzźż]","(O|P[$polish])"),

                  # LATIN ALPHABET
                  ("a","","","A"),
                  ("b","","","b"),
                  ("c","","","(k|ts[$polish])"),
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
                  ("z","","","(ts[$german]|z)"),

                  )

bmdata['ash']['approx_cyrillic'] = (
                        )

bmdata['ash']['exact_romanian'] = (
                       )

bmdata['ash']['rules_polish'] = (
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

bmdata['ash']['approx_hebrew'] = (
                      )

bmdata['ash']['exact_approxcommon'] = (
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

bmdata['ash']['exact_any'] = (
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

bmdata['ash']['exact_polish'] = (
                     ("B", "", "", "a"),
                     ("F", "", "", "e"),
                     ("P", "", "", "o"),

                     ("E", "", "", "e"),
                     ("I", "", "", "i"),

                     )

bmdata['ash']['approx_french'] = (
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

