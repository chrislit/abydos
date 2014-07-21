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

_ash_rules_english = (

                      # CONSONANTS
                      ("tch","","","tS"),
                      ("ch","","","(tS|x)"),
                      ("ck","","","k"),
                      ("cc","","[iey]","ks"), # success, accent
                      ("c","","c",""),
                      ("c","","[iey]","s"), # circle
                      ("c","","","k"), # candy
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
                      ("h","","","h"),

                      ("j","","","dZ"),
                      ("kn","^","","n"), # knight
                      ("mb","","$","m"),
                      ("ng","","$","(N|ng)"),
                      ("pn","^","","(pn|n)"),
                      ("ps","^","","(ps|s)"),
                      ("qu","","","kw"),
                      ("q","","","k"),
                      ("tia","","","(So|Sa)"),
                      ("tio","","","So"),
                      ("wr","^","","r"),
                      ("w","","","(w|v)"), # the variant "v" is for spellings coming from German/Polish
                      ("x","^","","z"),
                      ("x","","","ks"),

                      # VOWELS
                      ("y","^","","j"),
                      ("y","^","[aeiouy]","j"),
                      ("yi","^","","i"),
                      ("aue","","","aue"),
                      ("oue","","","(aue|oue)"),
                      ("ai","","","(aj|e)"), # rain | said
                      ("ay","","","aj"),
                      ("a","","[^aeiou]e","aj"), # plane (actually "ej")
                      ("a","","","(e|o|a)"), # hat | call | part
                      ("ei","","","(aj|i)"), # weigh | receive
                      ("ey","","","(aj|i)"), # hey | barley
                      ("ear","","","ia"), # tear
                      ("ea","","","(i|e)"), # reason | treasure
                      ("ee","","","i"), # between
                      ("e","","[^aeiou]e","i"), # meter
                      ("e","","$","(|E)"), # blame, badge
                      ("e","","","E"), # bed
                      ("ie","","","i"), # believe
                      ("i","","[^aeiou]e","aj"), # five
                      ("i","","","I"), # hit -- Morse disagrees, feels it should go to I
                      ("oa","","","ou"), # toad
                      ("oi","","","oj"), # join
                      ("oo","","","u"), # food
                      ("ou","","","(u|ou)"), # through | tough | could
                      ("oy","","","oj"), # boy
                      ("o","","[^aeiou]e","ou"), # rode
                      ("o","","","(o|a)"), # hot -- Morse disagrees, feels it should go to 9
                      ("u","","[^aeiou]e","(ju|u)"), # cute | flute
                      ("u","","r","(e|u)"), # turn -- Morse disagrees, feels it should go to E
                      ("u","","","(u|a)"), # put
                      ("y","","","i"),

                      # TRIVIAL
                      ("b","","","b"),
                      ("d","","","d"),
                      ("f","","","f"),
                      ("g","","","g"),
                      ("k","","","k"),
                      ("l","","","l"),
                      ("m","","","m"),
                      ("n","","","n"),
                      ("p","","","p"),
                      ("r","","","r"),
                      ("s","","","s"),
                      ("t","","","t"),
                      ("v","","","v"),
                      ("z","","","z"),

                      ("rulesenglish")

                      )
