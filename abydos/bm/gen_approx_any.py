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
             #VOWELS
             #'ALL'DIPHTHONGSareinterchangeableBETWEENTHEMandwithmonophthongsofwhichtheyarecomposed('D'means'diphthong')
             #{a,o}aretotallyinterchangeableifnon-stressed;inGerman'a/o'canactuallybefrom'ä/ö'(thatareequivalentto'e')
             #{i,e}areinterchangeableifnon-stressed,whileinGerman'u'canactuallybefrom'ü'(thatisequivalentto'i')
             
             ('mb','','','(mb|b[$greeklatin])'),
             ('mp','','','(mp|b[$greeklatin])'),
             ('ng','','','(ng|g[$greeklatin])'),
             
             ('B','','[fktSs]','(p|f[$spanish])'),
             ('B','','p',''),
             ('B','','$','(p|f[$spanish])'),
             ('V','','[pktSs]','(f|p[$spanish])'),
             ('V','','f',''),
             ('V','','$','(f|p[$spanish])'),
             
             ('B','','','(b|v[$spanish])'),
             ('V','','','(v|b[$spanish])'),
             
             #Frenchword-finalandword-part-finalletters
             ('t','','$','(t|[$french])'),
             ('g','n','$','(g|[$french])'),
             ('k','n','$','(k|[$french])'),
             ('p','','$','(p|[$french])'),
             ('r','[Ee]','$','(r|[$french])'),
             ('s','','$','(s|[$french])'),
             ('t','[aeiouAEIOU]','[^aeiouAEIOU]','(t|[$french])'),#Petitjean
             ('s','[aeiouAEIOU]','[^aeiouAEIOU]','(s|[$french])'),#Groslot,Grosleau
             #('p','[aeiouAEIOU]','[^aeiouAEIOU]','(p|[$french])'),
             
             ('I','[aeiouAEIBFOUQY]','','i'),
             ('I','','[^aeiouAEBFIOU]e','(Q[$german]|i|D[$english])'),#'line'
             ('I','','$','i'),
             ('I','','[^k]$','i'),
             ('Ik','[lr]','$','(ik|Qk[$german])'),
             ('Ik','','$','ik'),
             ('sIts','','$','(sits|sQts[$german])'),
             ('Its','','$','its'),
             ('I','','','(Q[$german]|i)'),
             
             ('lEE','[bdfgkmnprsStvzZ]','','(li|il[$english])'),#Apple=Appel
             ('rEE','[bdfgkmnprsStvzZ]','','(ri|ir[$english])'),
             ('lE','[bdfgkmnprsStvzZ]','','(li|il[$english]|lY[$german])'),#Applebaum<Appelbaum
             ('rE','[bdfgkmnprsStvzZ]','','(ri|ir[$english]|rY[$german])'),
             
             ('EE','','','(i|)'),
             
             ('ea','','','(D|a|i)'),
             
             ('au','','','(D|a|u)'),
             ('ou','','','(D|o|u)'),
             ('eu','','','(D|e|u)'),
             
             ('ai','','','(D|a|i)'),
             ('Ai','','','(D|a|i)'),
             ('oi','','','(D|o|i)'),
             ('Oi','','','(D|o|i)'),
             ('ui','','','(D|u|i)'),
             ('Ui','','','(D|u|i)'),
             ('ei','','','(D|i)'),
             ('Ei','','','(D|i)'),
             
             ('iA','','$','(ia|io)'),
             ('iA','','','(ia|io|iY[$german])'),
             ('A','','[^aeiouAEBFIOU]e','(a|o|Y[$german]|D[$english])'),#'plane'
             
             
             ('E','i[^aeiouAEIOU]','','(i|Y[$german]|[$english])'),#Wineberg(vineberg/vajneberg)-->vajnberg
             ('E','a[^aeiouAEIOU]','','(i|Y[$german]|[$english])'),#Shaneberg(shaneberg/shejneberg)-->shejnberg
             
             ('E','','[fklmnprst]$','i'),
             ('E','','ts$','i'),
             ('E','','$','i'),
             ('E','[DaoiuAOIUQY]','','i'),
             ('E','','[aoAOQY]','i'),
             ('E','','','(i|Y[$german])'),
             
             ('P','','','(o|u)'),
             
             ('O','','[fklmnprstv]$','o'),
             ('O','','ts$','o'),
             ('O','','$','o'),
             ('O','[oeiuQY]','','o'),
             ('O','','','(o|Y[$german])'),
             ('O','','','o'),
             
             ('A','','[fklmnprst]$','(a|o)'),
             ('A','','ts$','(a|o)'),
             ('A','','$','(a|o)'),
             ('A','[oeiuQY]','','(a|o)'),
             ('A','','','(a|o|Y[$german])'),
             ('A','','','(a|o)'),
             
             ('U','','$','u'),
             ('U','[DoiuQY]','','u'),
             ('U','','[^k]$','u'),
             ('Uk','[lr]','$','(uk|Qk[$german])'),
             ('Uk','','$','uk'),
             ('sUts','','$','(suts|sQts[$german])'),
             ('Uts','','$','uts'),
             ('U','','','(u|Q[$german])'),
             ('U','','','u'),
             
             ('e','','[fklmnprstv]$','i'),
             ('e','','ts$','i'),
             ('e','','$','i'),
             ('e','[DaoiuAOIUQY]','','i'),
             ('e','','[aoAOQY]','i'),
             ('e','','','(i|Y[$german])'),
             
             ('a','','','(a|o)'),
             
             ('approxany')
             
