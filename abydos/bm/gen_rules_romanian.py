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
