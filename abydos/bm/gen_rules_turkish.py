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

                      ("turkish")
                      )
