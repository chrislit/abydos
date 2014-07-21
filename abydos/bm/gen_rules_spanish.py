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
             
             #IncludesbothSpanish(Castillian)&Catalan
             
             #CONSONANTS
             ('ñ','','','(n|nj)'),
             ('ny','','','nj'),#Catalan
             ('ç','','','s'),#Catalan
             
             ('ig','[aeiou]','','(tS|ig)'),#tSisCatalan
             ('ix','[aeiou]','','S'),#Catalan
             ('tx','','','tS'),#Catalan
             ('tj','','$','tS'),#Catalan
             ('tj','','','dZ'),#Catalan
             ('tg','','','(tg|dZ)'),#dZisCatalan
             ('ch','','','(tS|dZ)'),#dZistypicalforArgentina
             ('bh','','','b'),#translit.fromArabic
             ('h','[dgt]','',''),#translit.fromArabic
             ('h','','$',''),#foreign
             #('ll','','','(l|Z)'),#ZistypicalforArgentina,onlyAshkenazic
             ('m','','[bpvf]','(m|n)'),
             ('c','','[ei]','s'),
             #('c','','[aou]','(k|C)'),
             ('gu','','[ei]','(g|gv)'),#'gv'because'u'canactuallybe'ü'
             ('g','','[ei]','(x|g|dZ)'),#'g'onlyforforeignwords;dZisCatalan
             ('qu','','','k'),
             
             ('uo','','','(vo|o)'),
             ('u','','[aei]','v'),
             
             #SPECIALVOWELS
             ('ü','','','v'),
             ('á','','','a'),
             ('é','','','e'),
             ('í','','','i'),
             ('ó','','','o'),
             ('ú','','','u'),
             ('à','','','a'),#Catalan
             ('è','','','e'),#Catalan
             ('ò','','','o'),#Catalan
             
             #LATINALPHABET
             ('a','','','a'),
             ('b','','','B'),
             ('c','','','k'),
             ('d','','','d'),
             ('e','','','e'),
             ('f','','','f'),
             ('g','','','g'),
             ('h','','','h'),
             ('i','','','i'),
             ('j','','','(x|Z)'),#ZisCatalan
             ('k','','','k'),
             ('l','','','l'),
             ('m','','','m'),
             ('n','','','n'),
             ('o','','','o'),
             ('p','','','p'),
             ('q','','','k'),
             ('r','','','r'),
             ('s','','','s'),
             ('t','','','t'),
             ('u','','','u'),
             ('v','','','V'),
             ('w','','','v'),#foreignwords
             ('x','','','(ks|gz|S)'),#ksisSpanish,allareCatalan
             ('y','','','(i|j)'),
             ('z','','','(z|s)'),#as'c'befoire'e'or'i',inSpainitislikeunvoicedEnglish'th'
             
             ('rulesspanish')
