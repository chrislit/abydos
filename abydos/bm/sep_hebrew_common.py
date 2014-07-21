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

_sep_hebrew_common = (

                      ("E","","",""),  # final French "e": only in Sephardic

                      ("ts","","","C"), # for not confusion Gutes [=guts] and Guts [=guc]
                      ("tS","","","C"), # same reason
                      ("S","","","s"),
                      ("p","","","f"),
                      ("b","^","","b"),
                      ("b","","","(b|v)"),

                      ("ja","","","i"),
                      ("je","","","i"),
                      ("aj","","","i"),
                      ("j","","","i"),

                      ("a","^","","1"),
                      ("e","^","","1"),
                      ("a","","$","1"),
                      ("e","","$","1"),

                      ("a","","",""),
                      ("e","","",""),

                      ("oj","^","","(u|vi)"),
                      ("uj","^","","(u|vi)"),

                      ("oj","","","u"),
                      ("uj","","","u"),

                      ("ou","^","","(u|v|1)"),
                      ("o","^","","(u|v|1)"),
                      ("u","^","","(u|v|1)"),

                      ("o","","$","(u|1)"),
                      ("u","","$","(u|1)"),

                      ("ou","","","u"),
                      ("o","","","u"),

                      ("VV","","","u"), # alef/ayin + vov from ruleshebrew
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

                      ("T","","","t"),   # tet from  ruleshebrew

                      # ("k","","","(k|x)"),
                      # ("x","","","(k|x)"),
                      ("K","","","k"), # kof and initial kaf from ruleshebrew
                      ("X","","","x"), # khet and final kaf from ruleshebrew

                      # special for Spanish initial B/V
                      ("B","","","v"),
                      ("V","","","b"),

                      ("H","^","","(x|1)"),
                      ("H","","$","(x|1)"),
                      ("H","","","(x|)"),
                      ("h","^","","1"),
                      ("h","","",""),

                      ("exactapproxcommon plus hebrewcommon")
                      )
