             
             #DUTCH
             ('van','^','[bp]','(vam|)'),
             ('van','^','','(van|)'),
             
             #REGRESSIVEASSIMILATIONOFCONSONANTS
             ('n','','[bp]','m'),
             
             #PECULIARITYOF'h'
             ('h','','',''),
             ('H','','','(x|)'),
             
             #'e'and'i'ARETOBEOMITTEDBEFORE(SYLLABIC)n&l:Halperin=Halpern;Frankel=Frankl,Finkelstein=Finklstein
             #butAndersen&Andersonshouldmatch
             ('sen','[rmnl]','$','(zn|zon)'),
             ('sen','','$','(sn|son)'),
             ('sEn','[rmnl]','$','(zn|zon)'),
             ('sEn','','$','(sn|son)'),
             
             ('e','[BbdfgklmnprsStvzZ]','[ln]$',''),
             ('i','[BbdfgklmnprsStvzZ]','[ln]$',''),
             ('E','[BbdfgklmnprsStvzZ]','[ln]$',''),
             ('I','[BbdfgklmnprsStvzZ]','[ln]$',''),
             ('Q','[BbdfgklmnprsStvzZ]','[ln]$',''),
             ('Y','[BbdfgklmnprsStvzZ]','[ln]$',''),
             
             ('e','[BbdfgklmnprsStvzZ]','[ln][BbdfgklmnprsStvzZ]',''),
             ('i','[BbdfgklmnprsStvzZ]','[ln][BbdfgklmnprsStvzZ]',''),
             ('E','[BbdfgklmnprsStvzZ]','[ln][BbdfgklmnprsStvzZ]',''),
             ('I','[BbdfgklmnprsStvzZ]','[ln][BbdfgklmnprsStvzZ]',''),
             ('Q','[BbdfgklmnprsStvzZ]','[ln][BbdfgklmnprsStvzZ]',''),
             ('Y','[BbdfgklmnprsStvzZ]','[ln][BbdfgklmnprsStvzZ]',''),
             
             ('lEs','','','(lEs|lz)'),#Applebaum<Appelbaum(English+blendEnglish-somethingformsasFinklestein)
             ('lE','[bdfgkmnprStvzZ]','','(lE|l)'),#Applebaum<Appelbaum(English+blendEnglish-somethingformsasFinklestein)
             
             #SIMPLIFICATION:(TRIPHTHONGS&DIPHTHONGS)->ONEGENERICDIPHTHONG'D'
             ('aue','','','D'),
             ('oue','','','D'),
             
             ('AvE','','','(D|AvE)'),
             ('Ave','','','(D|Ave)'),
             ('avE','','','(D|avE)'),
             ('ave','','','(D|ave)'),
             
             ('OvE','','','(D|OvE)'),
             ('Ove','','','(D|Ove)'),
             ('ovE','','','(D|ovE)'),
             ('ove','','','(D|ove)'),
             
             ('ea','','','(D|ea)'),
             ('EA','','','(D|EA)'),
             ('Ea','','','(D|Ea)'),
             ('eA','','','(D|eA)'),
             
             ('aji','','','D'),
             ('ajI','','','D'),
             ('aje','','','D'),
             ('ajE','','','D'),
             
             ('Aji','','','D'),
             ('AjI','','','D'),
             ('Aje','','','D'),
             ('AjE','','','D'),
             
             ('oji','','','D'),
             ('ojI','','','D'),
             ('oje','','','D'),
             ('ojE','','','D'),
             
             ('Oji','','','D'),
             ('OjI','','','D'),
             ('Oje','','','D'),
             ('OjE','','','D'),
             
             ('eji','','','D'),
             ('ejI','','','D'),
             ('eje','','','D'),
             ('ejE','','','D'),
             
             ('Eji','','','D'),
             ('EjI','','','D'),
             ('Eje','','','D'),
             ('EjE','','','D'),
             
             ('uji','','','D'),
             ('ujI','','','D'),
             ('uje','','','D'),
             ('ujE','','','D'),
             
             ('Uji','','','D'),
             ('UjI','','','D'),
             ('Uje','','','D'),
             ('UjE','','','D'),
             
             ('iji','','','D'),
             ('ijI','','','D'),
             ('ije','','','D'),
             ('ijE','','','D'),
             
             ('Iji','','','D'),
             ('IjI','','','D'),
             ('Ije','','','D'),
             ('IjE','','','D'),
             
             ('aja','','','D'),
             ('ajA','','','D'),
             ('ajo','','','D'),
             ('ajO','','','D'),
             ('aju','','','D'),
             ('ajU','','','D'),
             
             ('Aja','','','D'),
             ('AjA','','','D'),
             ('Ajo','','','D'),
             ('AjO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('oja','','','D'),
             ('ojA','','','D'),
             ('ojo','','','D'),
             ('ojO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('Oja','','','D'),
             ('OjA','','','D'),
             ('Ojo','','','D'),
             ('OjO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('eja','','','D'),
             ('ejA','','','D'),
             ('ejo','','','D'),
             ('ejO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('Eja','','','D'),
             ('EjA','','','D'),
             ('Ejo','','','D'),
             ('EjO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('uja','','','D'),
             ('ujA','','','D'),
             ('ujo','','','D'),
             ('ujO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('Uja','','','D'),
             ('UjA','','','D'),
             ('Ujo','','','D'),
             ('UjO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('ija','','','D'),
             ('ijA','','','D'),
             ('ijo','','','D'),
             ('ijO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('Ija','','','D'),
             ('IjA','','','D'),
             ('Ijo','','','D'),
             ('IjO','','','D'),
             ('Aju','','','D'),
             ('AjU','','','D'),
             
             ('j','','','i'),
             
             #lander=lender=länder
             ('lYndEr','','$','lYnder'),
             ('lander','','$','lYnder'),
             ('lAndEr','','$','lYnder'),
             ('lAnder','','$','lYnder'),
             ('landEr','','$','lYnder'),
             ('lender','','$','lYnder'),
             ('lEndEr','','$','lYnder'),
             ('lendEr','','$','lYnder'),
             ('lEnder','','$','lYnder'),
             
             #CONSONANTS{z&Z;s&S}areapproximatelyinterchangeable
             ('s','','[rmnl]','z'),
             ('S','','[rmnl]','z'),
             ('s','[rmnl]','','z'),
             ('S','[rmnl]','','z'),
             
             ('dS','','$','S'),
             ('dZ','','$','S'),
             ('Z','','$','S'),
             ('S','','$','(S|s)'),
             ('z','','$','(S|s)'),
             
             ('S','','','s'),
             ('dZ','','','z'),
             ('Z','','','z'),
             
             ('exactapproxcommonplusapproxcommon')
