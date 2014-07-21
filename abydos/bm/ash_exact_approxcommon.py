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

_ash_exact_approxcommon = (
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
