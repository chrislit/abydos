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
