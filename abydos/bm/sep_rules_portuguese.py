             ('kh','','','x'),#foreign
             ('ch','','','S'),
             ('ss','','','s'),
             ('sc','','[ei]','s'),
             ('sç','','[aou]','s'),
             ('ç','','','s'),
             ('c','','[ei]','s'),
             #('c','','[aou]','(k|C)'),
             
             ('s','^','','s'),
             ('s','[aáuiíoóeéêy]','[aáuiíoóeéêy]','z'),
             ('s','','[dglmnrv]','(Z|S)'),#ZisBrazil
             
             ('z','','$','(Z|s|S)'),#sandSinBrazil
             ('z','','[bdgv]','(Z|z)'),#ZinBrazil
             ('z','','[ptckf]','(s|S|z)'),#sandSinBrazil
             
             ('gu','','[eiu]','g'),
             ('gu','','[ao]','gv'),
             ('g','','[ei]','Z'),
             ('qu','','[eiu]','k'),
             ('qu','','[ao]','kv'),
             
             ('uo','','','(vo|o|u)'),
             ('u','','[aei]','v'),
             
             ('lh','','','l'),
             ('nh','','','nj'),
             ('h','[bdgt]','',''),#translit.fromArabic
             
             ('ex','','[aáuiíoóeéêy]','(ez|eS|eks)'),#ezinBrazil
             ('ex','','[cs]','e'),
             
             ('y','[aáuiíoóeéê]','','j'),
             ('y','','[aeiíou]','j'),
             ('m','','[bcdfglnprstv]','(m|n)'),#maybetoaddaruleform/nbeforeaconsonantthatdisappears[preceedingvowelbecomesnasalized]
             ('m','','$','(m|n)'),#maybetoaddaruleforfinalm/nthatdisappears[preceedingvowelbecomesnasalized]
             
             ('ão','','','(au|an|on)'),
             ('ãe','','','(aj|an)'),
             ('ãi','','','(aj|an)'),
             ('õe','','','(oj|on)'),
             ('i','[aáuoóeéê]','','j'),
             ('i','','[aeou]','j'),
             
             ('â','','','a'),
             ('à','','','a'),
             ('á','','','a'),
             ('ã','','','(a|an|on)'),
             ('é','','','e'),
             ('ê','','','e'),
             ('í','','','i'),
             ('ô','','','o'),
             ('ó','','','o'),
             ('õ','','','(o|on)'),
             ('ú','','','u'),
             ('ü','','','u'),
             
             ('aue','','','aue'),
             
             #LATINALPHABET
             ('a','','','a'),
             ('b','','','b'),
             ('c','','','k'),
             ('d','','','d'),
             ('e','','','(e|i)'),
             ('f','','','f'),
             ('g','','','g'),
             ('h','','','h'),
             ('i','','','i'),
             ('j','','','Z'),
             ('k','','','k'),
             ('l','','','l'),
             ('m','','','m'),
             ('n','','','n'),
             ('o','','','(o|u)'),
             ('p','','','p'),
             ('q','','','k'),
             ('r','','','r'),
             ('s','','','S'),
             ('t','','','t'),
             ('u','','','u'),
             ('v','','','v'),
             ('w','','','v'),
             ('x','','','(S|ks)'),
             ('y','','','i'),
             ('z','','','z'),
             
             ('rulesportuguese')
