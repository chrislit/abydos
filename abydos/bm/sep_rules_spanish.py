             
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
             
             ('j','','','(x|Z)'),#ZisCatalan
             ('x','','','(ks|gz|S)'),#ksisSpanish,allareCatalan
             
             #('ll','','','(l|Z)'),#ZistypicalforArgentina,onlyAshkenazic
             ('w','','','v'),#foreignwords
             
             ('v','^','','(B|v)'),
             ('b','^','','(b|V)'),
             ('v','','','(b|v)'),
             ('b','','','(b|v)'),
             ('m','','[bpvf]','(m|n)'),
             
             ('c','','[ei]','s'),
             #('c','','[aou]','(k|C)'),
             ('c','','','k'),
             
             ('z','','','(z|s)'),#as'c'befoire'e'or'i',inSpainitislikeunvoicedEnglish'th'
             
             ('gu','','[ei]','(g|gv)'),#'gv'because'u'canactuallybe'ü'
             ('g','','[ei]','(x|g|dZ)'),#'g'onlyforforeignwords;dZisCatalan
             
             ('qu','','','k'),
             ('q','','','k'),
             
             ('uo','','','(vo|o)'),
             ('u','','[aei]','v'),
             
             #('y','','','(i|j|S|Z)'),#SorZarepeculiartoSouthAmerica;onlyAshkenazic
             ('y','','','(i|j)'),
             
             #VOWELS
             ('ü','','','v'),
             ('á','','','a'),
             ('é','','','e'),
             ('í','','','i'),
             ('ó','','','o'),
             ('ú','','','u'),
             ('à','','','a'),#Catalan
             ('è','','','e'),#Catalan
             ('ò','','','o'),#Catalan
             
             #TRIVIAL
             ('a','','','a'),
             ('d','','','d'),
             ('e','','','e'),
             ('f','','','f'),
             ('g','','','g'),
             ('h','','','h'),
             ('i','','','i'),
             ('k','','','k'),
             ('l','','','l'),
             ('m','','','m'),
             ('n','','','n'),
             ('o','','','o'),
             ('p','','','p'),
             ('r','','','r'),
             ('s','','','s'),
             ('t','','','t'),
             ('u','','','u'),
             
             ('rulesspanish')
