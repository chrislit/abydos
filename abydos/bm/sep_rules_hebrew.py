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

_sep_rules_hebrew = (


                     ("אי","","","i"),
                     ("עי","","","i"),
                     ("עו","","","VV"),
                     ("או","","","VV"),

                     ("ג׳","","","Z"),
                     ("ד׳","","","dZ"),

                     ("א","","","L"),
                     ("ב","","","b"),
                     ("ג","","","g"),
                     ("ד","","","d"),

                     ("ה","^","","1"),
                     ("ה","","$","1"),
                     ("ה","","",""),

                     ("וו","","","V"),
                     ("וי","","","WW"),
                     ("ו","","","W"),
                     ("ז","","","z"),
                     ("ח","","","X"),
                     ("ט","","","T"),
                     ("יי","","","i"),
                     ("י","","","i"),
                     ("ך","","","X"),
                     ("כ","^","","K"),
                     ("כ","","","k"),
                     ("ל","","","l"),
                     ("ם","","","m"),
                     ("מ","","","m"),
                     ("ן","","","n"),
                     ("נ","","","n"),
                     ("ס","","","s"),
                     ("ע","","","L"),
                     ("ף","","","f"),
                     ("פ","","","f"),
                     ("ץ","","","C"),
                     ("צ","","","C"),
                     ("ק","","","K"),
                     ("ר","","","r"),
                     ("ש","","","s"),
                     ("ת","","","T"),   # Special for Sephardim


                     )
