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
             
             ('ا','','','a'),#alifisol&init
             
             ('ب','','$','b'),
             ('ب','','','b1'),#ba'isol
             
             ('ت','','$','t'),
             ('ت','','','t1'),#ta'isol
             
             ('ث','','$','t'),
             ('ث','','','t1'),#tha'isol
             
             ('ج','','$','(dZ|Z)'),
             ('ج','','','(dZ1|Z1)'),#jimisol
             
             ('ح','^','','1'),
             ('ح','','$','1'),
             ('ح','','','(h1|1)'),#h.a'isol
             
             ('خ','','$','x'),
             ('خ','','','x1'),#kha'isol
             
             ('د','','$','d'),
             ('د','','','d1'),#dalisol&init
             
             ('ذ','','$','d'),
             ('ذ','','','d1'),#dhalisol&init
             
             ('ر','','$','r'),
             ('ر','','','r1'),#ra'isol&init
             
             ('ز','','$','z'),
             ('ز','','','z1'),#za'isol&init
             
             ('س','','$','s'),
             ('س','','','s1'),#sinisol
             
             ('ش','','$','S'),
             ('ش','','','S1'),#shinisol
             
             ('ص','','$','s'),
             ('ص','','','s1'),#s.adisol
             
             ('ض','','$','d'),
             ('ض','','','d1'),#d.adisol
             
             ('ط','','$','t'),
             ('ط','','','t1'),#t.a'isol
             
             ('ظ','','$','z'),
             ('ظ','','','z1'),#z.a'isol
             
             ('ع','^','','1'),
             ('ع','','$','1'),
             ('ع','','','(h1|1)'),#ayinisol
             
             ('غ','','$','g'),
             ('غ','','','g1'),#ghayinisol
             
             ('ف','','$','f'),
             ('ف','','','f1'),#fa'isol
             
             ('ق','','$','k'),
             ('ق','','','k1'),#qafisol
             
             ('ك','','$','k'),
             ('ك','','','k1'),#kafisol
             
             ('ل','','$','l'),
             ('ل','','','l1'),#lamisol
             
             ('م','','$','m'),
             ('م','','','m1'),#mimisol
             
             ('ن','','$','n'),
             ('ن','','','n1'),#nunisol
             
             ('ه','^','','1'),
             ('ه','','$','1'),
             ('ه','','','(h1|1)'),#hisol
             
             ('و','','$','(u|v)'),
             ('و','','','(u|v1)'),#waw,isol+init
             
             ('ي‎','','$','(i|j)'),
             ('ي‎','','','(i|j1)'),#ya'isol
             
             ('rulesarabic')
