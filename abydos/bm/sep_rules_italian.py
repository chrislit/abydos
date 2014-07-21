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

                      ("rulesitalian")
                      )
