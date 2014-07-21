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
             
             ('ts','','','C'),#fornotconfusionGutes[=guts]andGuts[=guc]
             ('tS','','','C'),#samereason
             ('S','','','s'),
             ('p','','','f'),
             ('b','^','','b'),
             ('b','','','(b|v)'),
             ('J','','','l'),
             
             ('ja','','','i'),
             ('jA','','','i'),
             ('jB','','','i'),
             ('je','','','i'),
             ('jE','','','i'),
             ('jF','','','i'),
             ('aj','','','i'),
             ('Aj','','','i'),
             ('Bj','','','i'),
             ('Fj','','','i'),
             ('I','','','i'),
             ('Q','','','i'),
             ('j','','','i'),
             
             ('a','^','','1'),
             ('A','^','','1'),
             ('B','^','','1'),
             ('e','^','','1'),
             ('E','^','','1'),
             ('F','^','','1'),
             ('Y','^','','1'),
             
             ('a','','$','1'),
             ('A','','$','1'),
             ('B','','$','1'),
             ('e','','$','1'),
             ('E','','$','1'),
             ('F','','$','1'),
             ('Y','','$','1'),
             
             ('a','','',''),
             ('A','','',''),
             ('B','','',''),
             ('e','','',''),
             ('E','','',''),
             ('F','','',''),
             ('Y','','',''),
             
             ('oj','^','','(u|vi)'),
             ('Oj','^','','(u|vi)'),
             ('uj','^','','(u|vi)'),
             ('Uj','^','','(u|vi)'),
             
             ('oj','','','u'),
             ('Oj','','','u'),
             ('uj','','','u'),
             ('Uj','','','u'),
             
             ('ou','^','','(u|v|1)'),
             ('o','^','','(u|v|1)'),
             ('O','^','','(u|v|1)'),
             ('P','^','','(u|v|1)'),
             ('U','^','','(u|v|1)'),
             ('u','^','','(u|v|1)'),
             
             ('o','','$','(u|1)'),
             ('O','','$','(u|1)'),
             ('P','','$','(u|1)'),
             ('u','','$','(u|1)'),
             ('U','','$','(u|1)'),
             
             ('ou','','','u'),
             ('o','','','u'),
             ('O','','','u'),
             ('P','','','u'),
             ('U','','','u'),
             
             ('VV','','','u'),#alef/ayin+vovfromruleshebrew
             ('V','','','v'),#tsvey-vovfromruleshebrew;;onlyAshkenazic
             ('L','^','','1'),#alef/ayinfromruleshebrew
             ('L','','$','1'),#alef/ayinfromruleshebrew
             ('L','','',''),#alef/ayinfromruleshebrew
             ('WW','^','','(vi|u)'),#vav-yodfromruleshebrew
             ('WW','','','u'),#vav-yodfromruleshebrew
             ('W','^','','(u|v)'),#vavfromruleshebrew
             ('W','','','u'),#vavfromruleshebrew
             
             #('g','','','(g|Z)'),
             #('z','','','(z|Z)'),
             #('d','','','(d|dZ)'),
             
             ('TB','^','','t'),#tavfromruleshebrew;onlyAshkenazic
             ('TB','','$','s'),#tavfromruleshebrew;onlyAshkenazic
             ('TB','','','(t|s)'),#tavfromruleshebrew;onlyAshkenazic
             ('T','','','t'),#tetfromruleshebrew
             
             #('k','','','(k|x)'),
             #('x','','','(k|x)'),
             ('K','','','k'),#kofandinitialkaffromruleshebrew
             ('X','','','x'),#khetandfinalkaffromruleshebrew
             
             ('H','^','','(x|1)'),
             ('H','','$','(x|1)'),
             ('H','','','(x|)'),
             ('h','^','','1'),
             ('h','','',''),
             
             ('exactapproxcommonplushebrewcommon')
             
