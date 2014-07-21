             ('bens','^','','(binz|s)'),
             ('benS','^','','(binz|s)'),
             ('ben','^','','(bin|)'),
             
             ('abens','^','','(abinz|binz|s)'),
             ('abenS','^','','(abinz|binz|s)'),
             ('aben','^','','(abin|bin|)'),
             
             ('els','^','','(ilz|alz|s)'),
             ('elS','^','','(ilz|alz|s)'),
             ('el','^','','(il|al|)'),
             ('als','^','','(alz|s)'),
             ('alS','^','','(alz|s)'),
             ('al','^','','(al|)'),
             
             #('dels','^','','(dilz|s)'),
             #('delS','^','','(dilz|s)'),
             ('del','^','','(dil|)'),
             ('dela','^','','(dila|)'),
             #('delo','^','','(dila|)'),
             ('da','^','','(da|)'),
             ('de','^','','(di|)'),
             #('des','^','','(dis|dAs|)'),
             #('di','^','','(di|)'),
             #('dos','^','','(das|dus|)'),
             
             ('oa','','','(va|a|D)'),
             ('oe','','','(vi|D)'),
             ('ae','','','D'),
             
             #/('s','','$','(s|)'),#Attia(s)
             #/('C','','','s'),#'c'couldactuallybe'ç'
             
             ('n','','[bp]','m'),
             
             ('h','','','(|h|f)'),#sound'h'(absent)canbeexpressedvia/x/,CojabinSpanish=Kohab;Hakim=Fakim
             ('x','','','h'),
             
             #DIPHTHONGSAREAPPROXIMATELYequivalent
             ('aja','^','','(Da|ia)'),
             ('aje','^','','(Di|Da|i|ia)'),
             ('aji','^','','(Di|i)'),
             ('ajo','^','','(Du|Da|iu|ia)'),
             ('aju','^','','(Du|iu)'),
             
             ('aj','','','D'),
             ('ej','','','D'),
             ('oj','','','D'),
             ('uj','','','D'),
             ('au','','','D'),
             ('eu','','','D'),
             ('ou','','','D'),
             
             ('a','^','','(a|)'),#Arabic
             
             ('ja','^','','ia'),
             ('je','^','','i'),
             ('jo','^','','(iu|ia)'),
             ('ju','^','','iu'),
             
             ('ja','','','a'),
             ('je','','','i'),
             ('ji','','','i'),
             ('jo','','','u'),
             ('ju','','','u'),
             
             ('j','','','i'),
             
             #CONSONANTS{z&Z&dZ;s&S}areapproximatelyinterchangeable
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
             
             ('i','','$','(i|)'),#ofteninArabic
             ('e','','','i'),
             
             ('o','','$','(a|u)'),
             ('o','','','u'),
             
             #specialcharactertodealcorrectlyinHebrewmatch
             ('B','','','b'),
             ('V','','','v'),
             
             #Arabic
             ('p','^','','b'),
             
             ('exactapproxcommonplusapproxcommon')
