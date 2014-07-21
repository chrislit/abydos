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

                      ("rulesspanish")
                      )
