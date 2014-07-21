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

_ash_rules_any = (

                  # CONVERTING FEMININE TO MASCULINE
                  ("yna","","$","(in[$russian]|ina)"),
                  ("ina","","$","(in[$russian]|ina)"),
                  ("liova","","$","(lof[$russian]|lef[$russian]|lova)"),
                  ("lova","","$","(lof[$russian]|lef[$russian]|lova)"),
                  ("ova","","$","(of[$russian]|ova)"),
                  ("eva","","$","(ef[$russian]|eva)"),
                  ("aia","","$","(aja|i[$russian])"),
                  ("aja","","$","(aja|i[$russian])"),
                  ("aya","","$","(aja|i[$russian])"),

                  ("lowa","","$","(lova|lof[$polish]|l[$polish]|el[$polish])"),
                  ("kowa","","$","(kova|kof[$polish]|k[$polish]|ek[$polish])"),
                  ("owa","","$","(ova|of[$polish]|)"),
                  ("lowna","","$","(lovna|levna|l[$polish]|el[$polish])"),
                  ("kowna","","$","(kovna|k[$polish]|ek[$polish])"),
                  ("owna","","$","(ovna|[$polish])"),
                  ("lówna","","$","(l|el[$polish])"),  # polish
                  ("kówna","","$","(k|ek[$polish])"),  # polish
                  ("ówna","","$",""),   # polish

                  ("a","","$","(a|i[$polish])"),

                  # CONSONANTS  (integrated: German, Polish, Russian, Romanian and English)

                  ("rh","^","","r"),
                  ("ssch","","","S"),
                  ("chsch","","","xS"),
                  ("tsch","","","tS"),

                  ("sch","","[ei]","(sk[$romanian]|S|StS[$russian])"), # german
                  ("sch","","","(S|StS[$russian])"), # german

                  ("ssh","","","S"),

                  ("sh","","[äöü]","sh"), # german
                  ("sh","","[aeiou]","(S[$russian+$english]|sh)"),
                  ("sh","","","S"), # russian+english

                  ("kh","","","(x[$russian+$english]|kh)"),

                  ("chs","","","(ks[$german]|xs|tSs[$russian+$english])"),

                  # French "ch" is currently disabled
                  #("ch","","[ei]","(x|tS|k[$romanian]|S[$french])"),
                  #("ch","","","(x|tS[$russian+$english]|S[$french])"),

                  ("ch","","[ei]","(x|k[$romanian]|tS[$russian+$english])"),
                  ("ch","","","(x|tS[$russian+$english])"),

                  ("ck","","","(k|tsk[$polish])"),

                  ("czy","","","tSi"),
                  ("cze","","[bcdgkpstwzż]","(tSe|tSF)"),
                  ("ciewicz","","","(tsevitS|tSevitS)"),
                  ("siewicz","","","(sevitS|SevitS)"),
                  ("ziewicz","","","(zevitS|ZevitS)"),
                  ("riewicz","","","rjevitS"),
                  ("diewicz","","","djevitS"),
                  ("tiewicz","","","tjevitS"),
                  ("iewicz","","","evitS"),
                  ("ewicz","","","evitS"),
                  ("owicz","","","ovitS"),
                  ("icz","","","itS"),
                  ("cz","","","tS"), # Polish

                  ("cia","","[bcdgkpstwzż]","(tSB[$polish]|tsB)"),
                  ("cia","","","(tSa[$polish]|tsa)"),
                  ("cią","","[bp]","(tSom[$polish]|tsom)"),
                  ("cią","","","(tSon[$polish]|tson)"),
                  ("cię","","[bp]","(tSem[$polish]|tsem)"),
                  ("cię","","","(tSen[$polish]|tsen)"),
                  ("cie","","[bcdgkpstwzż]","(tSF[$polish]|tsF)"),
                  ("cie","","","(tSe[$polish]|tse)"),
                  ("cio","","","(tSo[$polish]|tso)"),
                  ("ciu","","","(tSu[$polish]|tsu)"),

                  ("ci","","$","(tsi[$polish]|tSi[$polish+$romanian]|tS[$romanian]|si)"),
                  ("ci","","","(tsi[$polish]|tSi[$polish+$romanian]|si)"),
                  ("ce","","[bcdgkpstwzż]","(tsF[$polish]|tSe[$polish+$romanian]|se)"),
                  ("ce","","","(tSe[$polish+$romanian]|tse[$polish]|se)"),
                  ("cy","","","(si|tsi[$polish])"),

                  ("ssz","","","S"), # Polish
                  ("sz","","","S"), # Polish; actually could also be Hungarian /s/, disabled here

                  ("ssp","","","(Sp[$german]|sp)"),
                  ("sp","","","(Sp[$german]|sp)"),
                  ("sst","","","(St[$german]|st)"),
                  ("st","","","(St[$german]|st)"),
                  ("ss","","","s"),

                  ("sia","","[bcdgkpstwzż]","(SB[$polish]|sB[$polish]|sja)"),
                  ("sia","","","(Sa[$polish]|sja)"),
                  ("sią","","[bp]","(Som[$polish]|som)"),
                  ("sią","","","(Son[$polish]|son)"),
                  ("się","","[bp]","(Sem[$polish]|sem)"),
                  ("się","","","(Sen[$polish]|sen)"),
                  ("sie","","[bcdgkpstwzż]","(SF[$polish]|sF|zi[$german])"),
                  ("sie","","","(se|Se[$polish]|zi[$german])"),
                  ("sio","","","(So[$polish]|so)"),
                  ("siu","","","(Su[$polish]|sju)"),
                  ("si","","","(Si[$polish]|si|zi[$german])"),
                  ("s","","[aeiouäöë]","(s|z[$german])"),

                  ("gue","","","ge"),
                  ("gui","","","gi"),
                  ("guy","","","gi"),
                  ("gh","","[ei]","(g[$romanian]|gh)"),

                  ("gauz","","$","haus"),
                  ("gaus","","$","haus"),
                  ("gol'ts","","$","holts"),
                  ("golts","","$","holts"),
                  ("gol'tz","","$","holts"),
                  ("goltz","","","holts"),
                  ("gol'ts","^","","holts"),
                  ("golts","^","","holts"),
                  ("gol'tz","^","","holts"),
                  ("goltz","^","","holts"),
                  ("gendler","","$","hendler"),
                  ("gejmer","","$","hajmer"),
                  ("gejm","","$","hajm"),
                  ("geymer","","$","hajmer"),
                  ("geym","","$","hajm"),
                  ("geimer","","$","hajmer"),
                  ("geim","","$","hajm"),
                  ("gof","","$","hof"),

                  ("ger","","$","ger"),
                  ("gen","","$","gen"),
                  ("gin","","$","gin"),

                  ("gie","","$","(ge|gi[$german]|ji[$french])"),
                  ("gie","","","ge"),
                  ("ge","[yaeiou]","","(gE|xe[$spanish]|dZe[$english+$romanian])"),
                  ("gi","[yaeiou]","","(gI|xi[$spanish]|dZi[$english+$romanian])"),
                  ("ge","","","(gE|dZe[$english+$romanian]|hE[$russian]|xe[$spanish])"),
                  ("gi","","","(gI|dZi[$english+$romanian]|hI[$russian]|xi[$spanish])"),
                  ("gy","","[aeouáéóúüöőű]","(gi|dj[$hungarian])"),
                  ("gy","","","(gi|d[$hungarian])"),
                  ("g","[jyaeiou]","[aouyei]","g"),
                  ("g","","[aouei]","(g|h[$russian])"),

                  ("ej","","","(aj|eZ[$french+$romanian]|ex[$spanish])"),
                  ("ej","","","aj"),

                  ("ly","","[au]","l"),
                  ("li","","[au]","l"),
                  ("lj","","[au]","l"),
                  ("lio","","","(lo|le[$russian])"),
                  ("lyo","","","(lo|le[$russian])"),
                  ("ll","","","(l|J[$spanish])"),

                  ("j","","[aoeiuy]","(j|dZ[$english]|x[$spanish]|Z[$french+$romanian])"),
                  ("j","","","(j|x[$spanish])"),

                  ("pf","","","(pf|p|f)"),
                  ("ph","","","(ph|f)"),

                  ("qu","","","(kv[$german]|k)"),

                  ("rze","t","","(Se[$polish]|re)"), # polish
                  ("rze","","","(rze|rtsE[$german]|Ze[$polish]|re[$polish]|rZe[$polish])"),
                  ("rzy","t","","(Si[$polish]|ri)"), # polish
                  ("rzy","","","(Zi[$polish]|ri[$polish]|rZi)"),
                  ("rz","t","","(S[$polish]|r)"), # polish
                  ("rz","","","(rz|rts[$german]|Z[$polish]|r[$polish]|rZ[$polish])"), # polish

                  ("tz","","$","(ts|tS[$english+$german])"),
                  ("tz","^","","(ts|tS[$english+$german])"),
                  ("tz","","","(ts[$english+$german+$russian]|tz)"),

                  ("zh","","","(Z|zh[$polish]|tsh[$german])"),

                  ("zia","","[bcdgkpstwzż]","(ZB[$polish]|zB[$polish]|zja)"),
                  ("zia","","","(Za[$polish]|zja)"),
                  ("zią","","[bp]","(Zom[$polish]|zom)"),
                  ("zią","","","(Zon[$polish]|zon)"),
                  ("zię","","[bp]","(Zem[$polish]|zem)"),
                  ("zię","","","(Zen[$polish]|zen)"),
                  ("zie","","[bcdgkpstwzż]","(ZF[$polish]|zF[$polish]|ze|tsi[$german])"),
                  ("zie","","","(ze|Ze[$polish]|tsi[$german])"),
                  ("zio","","","(Zo[$polish]|zo)"),
                  ("ziu","","","(Zu[$polish]|zju)"),
                  ("zi","","","(Zi[$polish]|zi|tsi[$german])"),

                  ("thal","","$","tal"),
                  ("th","^","","t"),
                  ("th","","[aeiou]","(t[$german]|th)"),
                  ("th","","","t"), # german
                  ("vogel","","","(vogel|fogel[$german])"),
                  ("v","^","","(v|f[$german])"),

                  ("h","[aeiouyäöü]","",""), #german
                  ("h","","","(h|x[$romanian+$polish])"),
                  ("h","^","","(h|H[$english+$german])"), # H can be exact "h" or approximate "kh"

                  # VOWELS
                  ("yi","^","","i"),

                  # ("e","","$","(e|)"),  # French & English rule disabled except for final -ine
                  ("e","in","$","(e|[$french])"),

                  ("ii","","$","i"), # russian
                  ("iy","","$","i"), # russian
                  ("yy","","$","i"), # russian
                  ("yi","","$","i"), # russian
                  ("yj","","$","i"), # russian
                  ("ij","","$","i"), # russian

                  ("aue","","","aue"),
                  ("oue","","","oue"),

                  ("au","","","(au|o[$french])"),
                  ("ou","","","(ou|u[$french])"),

                  ("ue","","","(Q|uje[$russian])"),
                  ("ae","","","(Y[$german]|aje[$russian]|ae)"),
                  ("oe","","","(Y[$german]|oje[$russian]|oe)"),
                  ("ee","","","(i[$english]|aje[$russian]|e)"),

                  ("ei","","","aj"),
                  ("ey","","","aj"),
                  ("eu","","","(aj[$german]|oj[$german]|eu)"),

                  ("i","[aou]","","j"),
                  ("y","[aou]","","j"),

                  ("ie","","[bcdgkpstwzż]","(i[$german]|e[$polish]|ije[$russian]|je)"),
                  ("ie","","","(i[$german]|e[$polish]|ije[$russian]|je)"),
                  ("ye","","","(je|ije[$russian])"),

                  ("i","","[au]","j"),
                  ("y","","[au]","j"),
                  ("io","","","(jo|e[$russian])"),
                  ("yo","","","(jo|e[$russian])"),

                  ("ea","","","(ea|ja[$romanian])"),
                  ("e","^","","(e|je[$russian])"),
                  ("oo","","","(u[$english]|o)"),
                  ("uu","","","u"),

                  # LANGUAGE SPECIFIC CHARACTERS
                  ("ć","","","(tS[$polish]|ts)"),  # polish
                  ("ł","","","l"),  # polish
                  ("ń","","","n"),  # polish
                  ("ñ","","","(n|nj[$spanish])"),
                  ("ś","","","(S[$polish]|s)"), # polish
                  ("ş","","","S"),  # romanian
                  ("ţ","","","ts"),  # romanian
                  ("ż","","","Z"),  # polish
                  ("ź","","","(Z[$polish]|z)"), # polish

                  ("où","","","u"), # french

                  ("ą","","[bp]","om"),  # polish
                  ("ą","","","on"),  # polish
                  ("ä","","","(Y|e)"),  # german
                  ("á","","","a"), # hungarian
                  ("ă","","","(e[$romanian]|a)"), #romanian
                  ("à","","","a"),  # french
                  ("â","","","a"), #french+romanian
                  ("é","","","e"),
                  ("è","","","e"), # french
                  ("ê","","","e"), # french
                  ("ę","","[bp]","em"),  # polish
                  ("ę","","","en"),  # polish
                  ("í","","","i"),
                  ("î","","","i"),
                  ("ö","","","Y"),
                  ("ő","","","Y"), # hungarian
                  ("ó","","","(u[$polish]|o)"),
                  ("ű","","","Q"),
                  ("ü","","","Q"),
                  ("ú","","","u"),
                  ("ű","","","Q"), # hungarian

                  ("ß","","","s"),  # german
                  ("'","","",""),
                  ('"',"","",""),

                  ("a","","[bcdgkpstwzż]","(A|B[$polish])"),
                  ("e","","[bcdgkpstwzż]","(E|F[$polish])"),
                  ("o","","[bcćdgklłmnńrsśtwzźż]","(O|P[$polish])"),

                  # LATIN ALPHABET
                  ("a","","","A"),
                  ("b","","","b"),
                  ("c","","","(k|ts[$polish])"),
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
                  ("v","","","v"),
                  ("w","","","v"), # English disabled
                  ("x","","","ks"),
                  ("y","","","i"),
                  ("z","","","(ts[$german]|z)"),


                  )
