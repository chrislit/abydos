             
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
