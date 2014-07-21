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

_gen_rules_russian = (
                      # CONVERTING FEMININE TO MASCULINE
                      ("yna","","$","(in|ina)"),
                      ("ina","","$","(in|ina)"),
                      ("liova","","$","(lof|lef)"),
                      ("lova","","$","(lof|lef|lova)"),
                      ("ova","","$","(of|ova)"),
                      ("eva","","$","(ef|ova)"),
                      ("aia","","$","(aja|i)"),
                      ("aja","","$","(aja|i)"),
                      ("aya","","$","(aja|i)"),

                      #SPECIAL CONSONANTS
                      ("tsya","","","tsa"),
                      ("tsyu","","","tsu"),
                      ("tsia","","","tsa"),
                      ("tsie","","","tse"),
                      ("tsio","","","tso"),
                      ("tsye","","","tse"),
                      ("tsyo","","","tso"),
                      ("tsiu","","","tsu"),
                      ("sie","","","se"),
                      ("sio","","","so"),
                      ("zie","","","ze"),
                      ("zio","","","zo"),
                      ("sye","","","se"),
                      ("syo","","","so"),
                      ("zye","","","ze"),
                      ("zyo","","","zo"),

                      ("ger","","$","ger"),
                      ("gen","","$","gen"),
                      ("gin","","$","gin"),
                      ("gg","","","g"),
                      ("g","[jaeoiuy]","[aeoiu]","g"),
                      ("g","","[aeoiu]","(g|h)"),

                      ("kh","","","x"),
                      ("ch","","","(tS|x)"),
                      ("sch","","","(StS|S)"),
                      ("ssh","","","S"),
                      ("sh","","","S"),
                      ("zh","","","Z"),
                      ("tz","","$","ts"),
                      ("tz","","","(ts|tz)"),
                      ("c","","[iey]","s"),
                      ("qu","","","(kv|k)"),
                      ("s","","s",""),

                      #SPECIAL VOWELS
                      ("lya","","","la"),
                      ("lyu","","","lu"),
                      ("lia","","","la"), # not in DJSRE
                      ("liu","","","lu"),  # not in DJSRE
                      ("lja","","","la"), # not in DJSRE
                      ("lju","","","lu"),  # not in DJSRE
                      ("le","","","(lo|lE)"), #not in DJSRE
                      ("lyo","","","(lo|le)"), #not in DJSRE
                      ("lio","","","(lo|le)"),

                      ("ije","","","je"),
                      ("ie","","","je"),
                      ("iye","","","je"),
                      ("iie","","","je"),
                      ("yje","","","je"),
                      ("ye","","","je"),
                      ("yye","","","je"),
                      ("yie","","","je"),

                      ("ij","","[aou]","j"),
                      ("iy","","[aou]","j"),
                      ("ii","","[aou]","j"),
                      ("yj","","[aou]","j"),
                      ("yy","","[aou]","j"),
                      ("yi","","[aou]","j"),

                      ("io","","","(jo|e)"),
                      ("i","","[au]","j"),
                      ("i","[aeou]","","j"),
                      ("yo","","","(jo|e)"),
                      ("y","","[au]","j"),
                      ("y","[aeiou]","","j"),

                      ("ii","","$","i"),
                      ("iy","","$","i"),
                      ("yy","","$","i"),
                      ("yi","","$","i"),
                      ("yj","","$","i"),
                      ("ij","","$","i"),

                      ("e","^","","(je|E)"),
                      ("ee","","","(aje|i)"),
                      ("e","[aou]","","je"),
                      ("oo","","","(oo|u)"),
                      ("'","","",""),
                      ('"',"","",""),

                      ("aue","","","aue"),

                      # LATIN ALPHABET
                      ("a","","","a"),
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
                      ("y","","","I"),
                      ("z","","","z"),

                      ("rulesrussian")
                      )
