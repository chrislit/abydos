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

_ash_approx_polish = (
                      ("aiB","","[bp]","(D|Dm)"),
                      ("oiB","","[bp]","(D|Dm)"),
                      ("uiB","","[bp]","(D|Dm)"),
                      ("eiB","","[bp]","(D|Dm)"),
                      ("EiB","","[bp]","(D|Dm)"),
                      ("iiB","","[bp]","(D|Dm)"),
                      ("IiB","","[bp]","(D|Dm)"),

                      ("aiB","","[dgkstvz]","(D|Dn)"),
                      ("oiB","","[dgkstvz]","(D|Dn)"),
                      ("uiB","","[dgkstvz]","(D|Dn)"),
                      ("eiB","","[dgkstvz]","(D|Dn)"),
                      ("EiB","","[dgkstvz]","(D|Dn)"),
                      ("iiB","","[dgkstvz]","(D|Dn)"),
                      ("IiB","","[dgkstvz]","(D|Dn)"),

                      ("B","","[bp]","(o|om|im)"),
                      ("B","","[dgkstvz]","(o|on|in)"),
                      ("B", "", "", "o"),

                      ("aiF","","[bp]","(D|Dm)"),
                      ("oiF","","[bp]","(D|Dm)"),
                      ("uiF","","[bp]","(D|Dm)"),
                      ("eiF","","[bp]","(D|Dm)"),
                      ("EiF","","[bp]","(D|Dm)"),
                      ("iiF","","[bp]","(D|Dm)"),
                      ("IiF","","[bp]","(D|Dm)"),

                      ("aiF","","[dgkstvz]","(D|Dn)"),
                      ("oiF","","[dgkstvz]","(D|Dn)"),
                      ("uiF","","[dgkstvz]","(D|Dn)"),
                      ("eiF","","[dgkstvz]","(D|Dn)"),
                      ("EiF","","[dgkstvz]","(D|Dn)"),
                      ("iiF","","[dgkstvz]","(D|Dn)"),
                      ("IiF","","[dgkstvz]","(D|Dn)"),

                      ("F","","[bp]","(i|im|om)"),
                      ("F","","[dgkstvz]","(i|in|on)"),
                      ("F", "", "", "i"),

                      ("P", "", "", "(o|u)"),

                      ("I", "", "$", "i"),
                      ("I", "", "[^k]$", "i"),
                      ("Ik", "[lr]", "$", "(ik|Qk)"),
                      ("Ik", "", "$", "ik"),
                      ("sIts", "", "$", "(sits|sQts)"),
                      ("Its", "", "$", "its"),
                      ("I", "[aeiAEBFIou]", "", "i"),
                      ("I", "", "", "(i|Q)"),

                      ("au","","","(D|a|u)"),
                      ("ou","","","(D|o|u)"),
                      ("ai","","","(D|a|i)"),
                      ("oi","","","(D|o|i)"),
                      ("ui","","","(D|u|i)"),

                      ("a", "", "", "(a|o)"),
                      ("e", "", "", "i"),

                      ("E", "", "[fklmnprst]$", "i"),
                      ("E", "", "ts$", "i"),
                      ("E", "", "$", "i"),
                      ("E", "[DaoiuQ]", "", "i"),
                      ("E", "", "[aoQ]", "i"),
                      ("E", "", "", "(Y|i)"),

                      )
