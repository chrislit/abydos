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

_gen_approx_arabic = (

                      ("1a", "", "", "(D|a)"),
                      ("1i", "", "", "(D|i|e)"),
                      ("1u", "", "", "(D|u|o)"),
                      ("j1", "", "", "(ja|je|jo|ju|j)"),
                      ("1", "", "", "(a|e|i|o|u|)"),
                      ("u", "", "", "(o|u)"),
                      ("i", "", "", "(i|e)"),
                      ("p", "", "$", "p"),
                      ("p", "", "", "(p|b)"),

                      )
