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
             
             #CONSONANTS
             ('lt','u','$','(lt|)'),#Renault
             ('c','n','$','(k|)'),#Tronc
             #('f','','','(f|)'),#Clef
             ('d','','$','(t|)'),#Durand
             ('g','n','$','(k|)'),#Gang
             ('p','','$','(p|)'),#Trop,Champ
             ('r','e','$','(r|)'),#Barbier
             ('t','','$','(t|)'),#Murat,Constant
             ('z','','$','(s|)'),
             
             ('ds','','$','(ds|)'),
             ('ps','','$','(ps|)'),#Champs
             ('rs','e','$','(rs|)'),
             ('ts','','$','(ts|)'),
             ('s','','$','(s|)'),#Denis
             
             ('x','u','$','(ks|)'),#Arnoux
             
             ('s','[aeéèêiou]','[^aeéèêiou]','(s|)'),#Deschamps,Malesherbes,Groslot
             ('t','[aeéèêiou]','[^aeéèêiou]','(t|)'),#Petitjean
             
             ('kh','','','x'),#foreign
             ('ph','','','f'),
             
             ('ç','','','s'),
             ('x','','','ks'),
             ('ch','','','S'),
             ('c','','[eiyéèê]','s'),
             
             ('gn','','','(n|gn)'),
             ('g','','[eiy]','Z'),
             ('gue','','$','k'),
             ('gu','','[eiy]','g'),
             ('aill','','e','aj'),#nonJewish
             ('ll','','e','(l|j)'),#nonJewish
             ('que','','$','k'),
             ('qu','','','k'),
             ('s','[aeiouyéèê]','[aeiouyéèê]','z'),
             ('h','[bdgt]','',''),#translitfromArabic
             
             ('m','[aeiouy]','[aeiouy]','m'),
             ('m','[aeiouy]','','(m|n)'),#nasal
             
             ('ou','','[aeio]','v'),
             ('u','','[aeio]','v'),
             
             #VOWELS
             ('aue','','','aue'),
             ('eau','','','o'),
             ('au','','','(o|au)'),#nonJewish
             ('ai','','','(e|aj)'),#[e]isnonJewish
             ('ay','','','(e|aj)'),#[e]isnonJewish
             ('é','','','e'),
             ('ê','','','e'),
             ('è','','','e'),
             ('à','','','a'),
             ('â','','','a'),
             ('où','','','u'),
             ('ou','','','u'),
             ('oi','','','(oj|va)'),#[va](actually'ua')isnonJewish
             ('ei','','','(aj|ej|e)'),#[e]isnonJewish
             ('ey','','','(aj|ej|e)'),#[e]nonJewish
             ('eu','','','(ej|Y)'),#nonJewish
             ('y','[ou]','','j'),
             ('e','','$','(e|)'),
             ('i','','[aou]','j'),
             ('y','','[aoeu]','j'),
             
             #LATINALPHABET
             ('a','','','a'),
             ('b','','','b'),
             ('c','','','k'),
             ('d','','','d'),
             ('e','','','e'),
             ('f','','','f'),
             ('g','','','g'),
             ('h','','','h'),
             ('i','','','i'),
             ('j','','','Z'),
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
             ('u','','','(u|Q)'),
             ('v','','','v'),
             ('w','','','v'),
             ('y','','','i'),
             ('z','','','z'),
             
             ('rulesfrench')
             
