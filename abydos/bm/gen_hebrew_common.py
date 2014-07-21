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

_gen_hebrew_common = (
                      ("ts","","","C"), # for not confusion Gutes [=guts] and Guts [=guc]
                      ("tS","","","C"), # same reason
                      ("S","","","s"),
                      ("p","","","f"),
                      ("b","^","","b"),
                      ("b","","","(b|v)"),
                      ("B","","","(b|v)"),    # Spanish "b"
                      ("V","","","v"),    # Spanish "v"
                      ("EE","","","(1|)"), # final "e" (english & french)

                      ("ja","","","i"),
                      ("jA","","","i"),
                      ("je","","","i"),
                      ("jE","","","i"),
                      ("aj","","","i"),
                      ("Aj","","","i"),
                      ("I","","","i"),
                      ("j","","","i"),

                      ("a","^","","1"),
                      ("A","^","","1"),
                      ("e","^","","1"),
                      ("E","^","","1"),
                      ("Y","^","","1"),

                      ("a","","$","1"),
                      ("A","","$","1"),
                      ("e","","$","1"),
                      ("E","","$","1"),
                      ("Y","","$","1"),

                      ("a","","",""),
                      ("A","","",""),
                      ("e","","",""),
                      ("E","","",""),
                      ("Y","","",""),

                      ("oj","^","","(u|vi)"),
                      ("Oj","^","","(u|vi)"),
                      ("uj","^","","(u|vi)"),
                      ("Uj","^","","(u|vi)"),

                      ("oj","","","u"),
                      ("Oj","","","u"),
                      ("uj","","","u"),
                      ("Uj","","","u"),

                      ("ou","^","","(u|v|1)"),
                      ("o","^","","(u|v|1)"),
                      ("O","^","","(u|v|1)"),
                      ("P","^","","(u|v|1)"),
                      ("U","^","","(u|v|1)"),
                      ("u","^","","(u|v|1)"),

                      ("o","","$","(u|1)"),
                      ("O","","$","(u|1)"),
                      ("P","","$","(u|1)"),
                      ("u","","$","(u|1)"),
                      ("U","","$","(u|1)"),

                      ("ou","","","u"),
                      ("o","","","u"),
                      ("O","","","u"),
                      ("P","","","u"),
                      ("U","","","u"),

                      ("VV","","","u"), # alef/ayin + vov from ruleshebrew
                      ("V","","","v"), # tsvey-vov from ruleshebrew;; only Ashkenazic
                      ("L","^","","1"), # alef/ayin from  ruleshebrew
                      ("L","","$","1"), # alef/ayin from  ruleshebrew
                      ("L","","",""), # alef/ayin from  ruleshebrew
                      ("WW","^","","(vi|u)"), # vav-yod from  ruleshebrew
                      ("WW","","","u"), # vav-yod from  ruleshebrew
                      ("W","^","","(u|v)"), # vav from  ruleshebrew
                      ("W","","","u"), # vav from  ruleshebrew

                      # ("g","","","(g|Z)"),
                      # ("z","","","(z|Z)"),
                      # ("d","","","(d|dZ)"),

                      ("TB","^","","t"), # tav from ruleshebrew
                      ("TB","","","(t|s)"), # tav from ruleshebrew; s is only Ashkenazic
                      ("T","","","t"),   # tet from  ruleshebrew

                      # ("k","","","(k|x)"),
                      # ("x","","","(k|x)"),
                      ("K","","","k"), # kof and initial kaf from ruleshebrew
                      ("X","","","x"), # khet and final kaf from ruleshebrew

                      ("H","^","","(x|1)"),
                      ("H","","$","(x|1)"),
                      ("H","","","(x|)"),
                      ("h","^","","1"),
                      ("h","","",""),

                      )
