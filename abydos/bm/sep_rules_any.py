             #CONSONANTS
             ('ph','','','f'),#foreign
             ('sh','','','S'),#foreign
             ('kh','','','x'),#foreign
             
             ('gli','','','(gli|l[$italian])'),
             ('gni','','','(gni|ni['.($italian+$french).'])'),
             ('gn','','[aeou]','(n['.($italian+$french).']|nj['.($italian+$french).']|gn)'),
             ('gh','','','g'),#It+translit.fromArabic
             ('dh','','','d'),#translit.fromArabic
             ('bh','','','b'),#translit.fromArabic
             ('th','','','t'),#translit.fromArabic
             ('lh','','','l'),#Port
             ('nh','','','nj'),#Port
             
             ('ig','[aeiou]','','(ig|tS[$spanish])'),
             ('ix','[aeiou]','','S'),#Sp
             ('tx','','','tS'),#Sp
             ('tj','','$','tS'),#Sp
             ('tj','','','dZ'),#Sp
             ('tg','','','(tg|dZ[$spanish])'),
             
             ('gi','','[aeou]','dZ'),#italian
             ('g','','y','Z'),#french
             ('gg','','[ei]','(gZ['.($portuguese+$french).']|dZ['.($italian+$spanish).']|x[$spanish])'),
             ('g','','[ei]','(Z['.($portuguese+$french).']|dZ['.($italian+$spanish).']|x[$spanish])'),
             
             ('guy','','','gi'),
             ('gue','','$','(k[$french]|ge)'),
             ('gu','','[ei]','(g|gv)'),#notIt
             ('gu','','[ao]','gv'),#notIt
             
             ('ñ','','','(n|nj)'),
             ('ny','','','nj'),
             
             ('sc','','[ei]','(s|S[$italian])'),
             ('sç','','[aeiou]','s'),#notIt
             ('ss','','','s'),
             ('ç','','','s'),#notIt
             
             ('ch','','[ei]','(k[$italian]|S['.($portuguese+$french).']|tS[$spanish]|dZ[$spanish])'),
             ('ch','','','(S|tS[$spanish]|dZ[$spanish])'),
             
             ('ci','','[aeou]','(tS[$italian]|si)'),
             ('cc','','[eiyéèê]','(tS[$italian]|ks['.($portuguese+$french+$spanish).'])'),
             ('c','','[eiyéèê]','(tS[$italian]|s['.($portuguese+$french+$spanish).'])'),
             #('c','','[aou]','(k|C['.($portuguese+$spanish).'])'),#'C'meansthattheactuallettercouldbe'ç'(cedilleomitted)
             
             ('s','^','','s'),
             ('s','[aáuiíoóeéêy]','[aáuiíoóeéêy]','(s[$spanish]|z['.($portuguese+$french+$italian).'])'),
             ('s','','[dglmnrv]','(z|Z[$portuguese])'),
             
             ('z','','$','(s|ts[$italian]|S[$portuguese])'),#tsIt,s/S/ZPort,sinSp,zFr
             ('z','','[bdgv]','(z|dz[$italian]|Z[$portuguese])'),#dzIt,Z/zPort,zSp&Fr
             ('z','','[ptckf]','(s|ts[$italian]|S[$portuguese])'),#tsIt,s/S/zPort,z/sSp
             ('z','','','(z|dz[$italian]|ts[$italian]|s[$spanish])'),#ts/dzIt,zPort&Fr,z/sSp
             
             ('que','','$','(k[$french]|ke)'),
             ('qu','','[eiu]','k'),
             ('qu','','[ao]','(kv|k)'),#kisIt
             
             ('ex','','[aáuiíoóeéêy]','(ez[$portuguese]|eS[$portuguese]|eks|egz)'),
             ('ex','','[cs]','(e[$portuguese]|ek)'),
             
             ('m','','[cdglnrst]','(m|n[$portuguese])'),
             ('m','','[bfpv]','(m|n['.($portuguese+$spanish).'])'),
             ('m','','$','(m|n[$portuguese])'),
             
             ('b','^','','(b|V[$spanish])'),
             ('v','^','','(v|B[$spanish])'),
             
             #VOWELS
             ('eau','','','o'),#Fr
             
             ('ouh','','[aioe]','(v[$french]|uh)'),
             ('uh','','[aioe]','(v|uh)'),
             ('ou','','[aioe]','v'),#french
             ('uo','','','(vo|o)'),
             ('u','','[aie]','v'),
             
             ('i','[aáuoóeéê]','','j'),
             ('i','','[aeou]','j'),
             ('y','[aáuiíoóeéê]','','j'),
             ('y','','[aeiíou]','j'),
             ('e','','$','(e|E[$french])'),
             
             ('ão','','','(au|an)'),#Port
             ('ãe','','','(aj|an)'),#Port
             ('ãi','','','(aj|an)'),#Port
             ('õe','','','(oj|on)'),#Port
             ('où','','','u'),#Fr
             ('ou','','','(ou|u[$french])'),
             
             ('â','','','a'),#Port&Fr
             ('à','','','a'),#Port
             ('á','','','a'),#Port&Sp
             ('ã','','','(a|an)'),#Port
             ('é','','','e'),
             ('ê','','','e'),#Port&Fr
             ('è','','','e'),#Sp&Fr&It
             ('í','','','i'),#Port&Sp
             ('î','','','i'),#Fr
             ('ô','','','o'),#Port&Fr
             ('ó','','','o'),#Port&Sp&It
             ('õ','','','(o|on)'),#Port
             ('ò','','','o'),#Sp&It
             ('ú','','','u'),#Port&Sp
             ('ü','','','u'),#Port&Sp
             
             #LATINALPHABET
             ('a','','','a'),
             ('b','','','(b|v[$spanish])'),
             ('c','','','k'),
             ('d','','','d'),
             ('e','','','e'),
             ('f','','','f'),
             ('g','','','g'),
             ('h','','','h'),
             ('i','','','i'),
             ('j','','','(x[$spanish]|Z)'),#notIt
             ('k','','','k'),
             ('l','','','l'),
             ('m','','','m'),
             ('n','','','n'),
             ('o','','','o'),
             ('p','','','p'),
             ('q','','','k'),
             ('r','','','r'),
             ('s','','','(s|S[$portuguese])'),
             ('t','','','t'),
             ('u','','','u'),
             ('v','','','(v|b[$spanish])'),
             ('w','','','v'),#foreign
             ('x','','','(ks|gz|S['.($portuguese+$spanish).'])'),#S/ksPort&Sp,gzSp,Itonlyks
             ('y','','','i'),
             ('z','','','z'),
             
             ('rulesany')
