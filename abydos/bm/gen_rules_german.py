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

_gen_rules_german = (

                     # CONSONANTS
                     ("ewitsch","","$","evitS"),
                     ("owitsch","","$","ovitS"),
                     ("evitsch","","$","evitS"),
                     ("ovitsch","","$","ovitS"),
                     ("witsch","","$","vitS"),
                     ("vitsch","","$","vitS"),
                     ("ssch","","","S"),
                     ("chsch","","","xS"),
                     ("sch","","","S"),

                     ("ziu","","","tsu"),
                     ("zia","","","tsa"),
                     ("zio","","","tso"),

                     ("chs","","","ks"),
                     ("ch","","","x"),
                     ("ck","","","k"),
                     ("c","","[eiy]","ts"),

                     ("sp","^","","Sp"),
                     ("st","^","","St"),
                     ("ssp","","","(Sp|sp)"),
                     ("sp","","","(Sp|sp)"),
                     ("sst","","","(St|st)"),
                     ("st","","","(St|st)"),
                     ("pf","","","(pf|p|f)"),
                     ("ph","","","(ph|f)"),
                     ("qu","","","kv"),

                     ("ewitz","","$","(evits|evitS)"),
                     ("ewiz","","$","(evits|evitS)"),
                     ("evitz","","$","(evits|evitS)"),
                     ("eviz","","$","(evits|evitS)"),
                     ("owitz","","$","(ovits|ovitS)"),
                     ("owiz","","$","(ovits|ovitS)"),
                     ("ovitz","","$","(ovits|ovitS)"),
                     ("oviz","","$","(ovits|ovitS)"),
                     ("witz","","$","(vits|vitS)"),
                     ("wiz","","$","(vits|vitS)"),
                     ("vitz","","$","(vits|vitS)"),
                     ("viz","","$","(vits|vitS)"),
                     ("tz","","","ts"),

                     ("thal","","$","tal"),
                     ("th","^","","t"),
                     ("th","","[äöüaeiou]","(t|th)"),
                     ("th","","","t"),
                     ("rh","^","","r"),
                     ("h","[aeiouyäöü]","",""),
                     ("h","^","","H"),

                     ("ss","","","s"),
                     ("s","","[äöüaeiouy]","(z|s)"),
                     ("s","[aeiouyäöüj]","[aeiouyäöü]","z"),
                     ("ß","","","s"),


                     # VOWELS
                     ("ij","","$","i"),
                     ("aue","","","aue"),
                     ("ue","","","Q"),
                     ("ae","","","Y"),
                     ("oe","","","Y"),
                     ("ü","","","Q"),
                     ("ä","","","(Y|e)"),
                     ("ö","","","Y"),
                     ("ei","","","(aj|ej)"),
                     ("ey","","","(aj|ej)"),
                     ("eu","","","(Yj|ej|aj|oj)"),
                     ("i","[aou]","","j"),
                     ("y","[aou]","","j"),
                     ("ie","","","I"),
                     ("i","","[aou]","j"),
                     ("y","","[aoeu]","j"),

                     # FOREIGN LETTERs
                     ("ñ","","","n"),
                     ("ã","","","a"),
                     ("ő","","","o"),
                     ("ű","","","u"),
                     ("ç","","","s"),

                     # LATIN ALPHABET
                     ("a","","","A"),
                     ("b","","","b"),
                     ("c","","","k"),
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
                     ("o","","","O"),
                     ("p","","","p"),
                     ("q","","","k"),
                     ("r","","","r"),
                     ("s","","","s"),
                     ("t","","","t"),
                     ("u","","","U"),
                     ("v","","","(f|v)"),
                     ("w","","","v"),
                     ("x","","","ks"),
                     ("y","","","i"),
                     ("z","","","ts"),

                     ("rulesgerman")

                     )
