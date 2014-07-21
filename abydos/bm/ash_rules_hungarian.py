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
