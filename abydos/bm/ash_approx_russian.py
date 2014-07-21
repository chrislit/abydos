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

_ash_approx_russian = (


                       # VOWELS
                       ("I", "", "$", "i"),
                       ("I", "", "[^k]$", "i"),
                       ("Ik", "[lr]", "$", "(ik|Qk)"),
                       ("Ik", "", "$", "ik"),
                       ("sIts", "", "$", "(sits|sQts)"),
                       ("Its", "", "$", "its"),
                       ("I", "[aeiEIou]", "", "i"),
                       ("I", "", "", "(i|Q)"),

                       ("au","","","(D|a|u)"),
                       ("ou","","","(D|o|u)"),
                       ("ai","","","(D|a|i)"),
                       ("oi","","","(D|o|i)"),
                       ("ui","","","(D|u|i)"),

                       ("om","","[bp]","(om|im)"),
                       ("on","","[dgkstvz]","(on|in)"),
                       ("em","","[bp]","(im|om)"),
                       ("en","","[dgkstvz]","(in|on)"),
                       ("Em","","[bp]","(im|Ym|om)"),
                       ("En","","[dgkstvz]","(in|Yn|on)"),

                       ("a", "", "", "(a|o)"),
                       ("e", "", "", "i"),

                       ("E", "", "[fklmnprsStv]$", "i"),
                       ("E", "", "ts$", "i"),
                       ("E", "[DaoiuQ]", "", "i"),
                       ("E", "", "[aoQ]", "i"),
                       ("E", "", "", "(Y|i)"),

                       ("approxrussian")

                       )
