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

_ash_rules_russian = (

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

                      #SPECIFIC CONSONANTS
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

                      ("gauz","","$","haus"),
                      ("gaus","","$","haus"),
                      ("gol'ts","","$","holts"),
                      ("golts","","$","holts"),
                      ("gol'tz","","$","holts"),
                      ("goltz","","$","holts"),
                      ("gejmer","","$","hajmer"),
                      ("gejm","","$","hajm"),
                      ("geimer","","$","hajmer"),
                      ("geim","","$","hajm"),
                      ("geymer","","$","hajmer"),
                      ("geym","","$","hajm"),
                      ("gendler","","$","hendler"),
                      ("gof","","$","hof"),
                      ("gojf","","$","hojf"),
                      ("goyf","","$","hojf"),
                      ("goif","","$","hojf"),
                      ("ger","","$","ger"),
                      ("gen","","$","gen"),
                      ("gin","","$","gin"),
                      ("gg","","","g"),
                      ("g","[jaeoiuy]","[aeoiu]","g"),
                      ("g","","[aeoiu]","(g|h)"),

                      ("kh","","","x"),
                      )
