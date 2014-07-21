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
