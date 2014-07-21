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

_ash_approx_common = (

                      # REGRESSIVE ASSIMILATION OF CONSONANTS
                      ("n","","[bp]","m"),

                      # PECULIARITY OF "h"
                      ("h","","",""),
                      ("H","","","(x|)"),

                      # POLISH OGONEK IMPOSSIBLE
                      ("F", "", "[bdgkpstvzZ]h", "e"),
                      ("F", "", "[bdgkpstvzZ]x", "e"),
                      ("B", "", "[bdgkpstvzZ]h", "a"),
                      ("B", "", "[bdgkpstvzZ]x", "a"),

                      # "e" and "i" ARE TO BE OMITTED BEFORE (SYLLABIC) n & l: Halperin=Halpern; Frankel = Frankl, Finkelstein = Finklstein
                      ("e", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
                      ("i", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
                      ("E", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
                      ("I", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
                      ("F", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
                      ("Q", "[bdfgklmnprsStvzZ]", "[ln]$", ""),
                      ("Y", "[bdfgklmnprsStvzZ]", "[ln]$", ""),

                      ("e", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
                      ("i", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
                      ("E", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
                      ("I", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
                      ("F", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
                      ("Q", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),
                      ("Y", "[bdfgklmnprsStvzZ]", "[ln][bdfgklmnprsStvzZ]", ""),

                      ("lEs","","","(lEs|lz)"),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)
                      ("lE","[bdfgkmnprStvzZ]","","(lE|l)"),  # Applebaum < Appelbaum (English + blend English-something forms as Finklestein)

                      # SIMPLIFICATION: (TRIPHTHONGS & DIPHTHONGS) -> ONE GENERIC DIPHTHONG "D"
                      ("aue","","","D"),
                      ("oue","","","D"),

                      ("AvE","","","(D|AvE)"),
                      ("Ave","","","(D|Ave)"),
                      ("avE","","","(D|avE)"),
                      ("ave","","","(D|ave)"),

                      ("OvE","","","(D|OvE)"),
                      ("Ove","","","(D|Ove)"),
                      ("ovE","","","(D|ovE)"),
                      ("ove","","","(D|ove)"),

                      ("ea","","","(D|ea)"),
                      ("EA","","","(D|EA)"),
                      ("Ea","","","(D|Ea)"),
                      ("eA","","","(D|eA)"),

                      ("aji","","","D"),
                      ("ajI","","","D"),
                      ("aje","","","D"),
                      ("ajE","","","D"),

                      ("Aji","","","D"),
                      ("AjI","","","D"),
                      ("Aje","","","D"),
                      ("AjE","","","D"),

                      ("oji","","","D"),
                      ("ojI","","","D"),
                      ("oje","","","D"),
                      ("ojE","","","D"),

                      ("Oji","","","D"),
                      ("OjI","","","D"),
                      ("Oje","","","D"),
                      ("OjE","","","D"),

                      ("eji","","","D"),
                      ("ejI","","","D"),
                      ("eje","","","D"),
                      ("ejE","","","D"),

                      ("Eji","","","D"),
                      ("EjI","","","D"),
                      ("Eje","","","D"),
                      ("EjE","","","D"),

                      ("uji","","","D"),
                      ("ujI","","","D"),
                      ("uje","","","D"),
                      ("ujE","","","D"),

                      ("Uji","","","D"),
                      ("UjI","","","D"),
                      ("Uje","","","D"),
                      ("UjE","","","D"),

                      ("iji","","","D"),
                      ("ijI","","","D"),
                      ("ije","","","D"),
                      ("ijE","","","D"),

                      ("Iji","","","D"),
                      ("IjI","","","D"),
                      ("Ije","","","D"),
                      ("IjE","","","D"),

                      ("aja","","","D"),
                      ("ajA","","","D"),
                      ("ajo","","","D"),
                      ("ajO","","","D"),
                      ("aju","","","D"),
                      ("ajU","","","D"),

                      ("Aja","","","D"),
                      ("AjA","","","D"),
                      ("Ajo","","","D"),
                      ("AjO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("oja","","","D"),
                      ("ojA","","","D"),
                      ("ojo","","","D"),
                      ("ojO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("Oja","","","D"),
                      ("OjA","","","D"),
                      ("Ojo","","","D"),
                      ("OjO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("eja","","","D"),
                      ("ejA","","","D"),
                      ("ejo","","","D"),
                      ("ejO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("Eja","","","D"),
                      ("EjA","","","D"),
                      ("Ejo","","","D"),
                      ("EjO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("uja","","","D"),
                      ("ujA","","","D"),
                      ("ujo","","","D"),
                      ("ujO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("Uja","","","D"),
                      ("UjA","","","D"),
                      ("Ujo","","","D"),
                      ("UjO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("ija","","","D"),
                      ("ijA","","","D"),
                      ("ijo","","","D"),
                      ("ijO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("Ija","","","D"),
                      ("IjA","","","D"),
                      ("Ijo","","","D"),
                      ("IjO","","","D"),
                      ("Aju","","","D"),
                      ("AjU","","","D"),

                      ("j","","","i"),

                      # lander = lender = länder
                      ("lYndEr","","$","lYnder"),
                      ("lander","","$","lYnder"),
                      ("lAndEr","","$","lYnder"),
                      ("lAnder","","$","lYnder"),
                      ("landEr","","$","lYnder"),
                      ("lender","","$","lYnder"),
                      ("lEndEr","","$","lYnder"),
                      ("lendEr","","$","lYnder"),
                      ("lEnder","","$","lYnder"),

                      # CONSONANTS {z & Z; s & S} are approximately interchangeable
                      ("s", "", "[rmnl]", "z"),
                      ("S", "", "[rmnl]", "z"),
                      ("s", "[rmnl]", "", "z"),
                      ("S", "[rmnl]", "", "z"),

                      ("dS", "", "$", "S"),
                      ("dZ", "", "$", "S"),
                      ("Z", "", "$", "S"),
                      ("S", "", "$", "(S|s)"),
                      ("z", "", "$", "(S|s)"),

                      ("S", "", "", "s"),
                      ("dZ", "", "", "z"),
                      ("Z", "", "", "z"),

                      ("exactapproxcommon plus approxcommon")

                      )
