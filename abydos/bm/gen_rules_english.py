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

_gen_rules_english = (
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
