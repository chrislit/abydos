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

_sep_rules_any = (
                  # CONSONANTS
                  ("ph","","","f"), # foreign
                  ("sh","","","S"), # foreign
                  ("kh","","","x"), # foreign

                  ("gli","","","(gli|l[$italian])"),
                  ("gni","","","(gni|ni[".($italian+$french)."])"),
                  ("gn","","[aeou]","(n[".($italian+$french)."]|nj[".($italian+$french)."]|gn)"),
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
                  ("gg","","[ei]","(gZ[".($portuguese+$french)."]|dZ[".($italian+$spanish)."]|x[$spanish])"),
                  ("g","","[ei]","(Z[".($portuguese+$french)."]|dZ[".($italian+$spanish)."]|x[$spanish])"),

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

                  ("ch","","[ei]","(k[$italian]|S[".($portuguese+$french)."]|tS[$spanish]|dZ[$spanish])"),
                  ("ch","","","(S|tS[$spanish]|dZ[$spanish])"),

                  ("ci","","[aeou]","(tS[$italian]|si)"),
                  ("cc","","[eiyéèê]","(tS[$italian]|ks[".($portuguese+$french+$spanish)."])"),
                  ("c","","[eiyéèê]","(tS[$italian]|s[".($portuguese+$french+$spanish)."])"),
                  #("c","","[aou]","(k|C[".($portuguese+$spanish)."])"), # "C" means that the actual letter could be "ç" (cedille omitted)

                  ("s","^","","s"),
                  ("s","[aáuiíoóeéêy]","[aáuiíoóeéêy]","(s[$spanish]|z[".($portuguese+$french+$italian)."])"),
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
                  ("m","","[bfpv]","(m|n[".($portuguese+$spanish)."])"),
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
                  ("x","","","(ks|gz|S[".($portuguese+$spanish)."])"),   # S/ks Port & Sp, gz Sp, It only ks
                  ("y","","","i"),
                  ("z","","","z"),

                  ("rulesany")
                  )
