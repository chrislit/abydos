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

_sep_rules_portuguese = (
                         ("kh","","","x"), # foreign
                         ("ch","","","S"),
                         ("ss","","","s"),
                         ("sc","","[ei]","s"),
                         ("sç","","[aou]","s"),
                         ("ç","","","s"),
                         ("c","","[ei]","s"),
                         #  ("c","","[aou]","(k|C)"),

                         ("s","^","","s"),
                         ("s","[aáuiíoóeéêy]","[aáuiíoóeéêy]","z"),
                         ("s","","[dglmnrv]","(Z|S)"), # Z is Brazil

                         ("z","","$","(Z|s|S)"), # s and S in Brazil
                         ("z","","[bdgv]","(Z|z)"), # Z in Brazil
                         ("z","","[ptckf]","(s|S|z)"), # s and S in Brazil

                         ("gu","","[eiu]","g"),
                         ("gu","","[ao]","gv"),
                         ("g","","[ei]","Z"),
                         ("qu","","[eiu]","k"),
                         ("qu","","[ao]","kv"),

                         ("uo","","","(vo|o|u)"),
                         ("u","","[aei]","v"),

                         ("lh","","","l"),
                         ("nh","","","nj"),
                         ("h","[bdgt]","",""), # translit. from Arabic

                         ("ex","","[aáuiíoóeéêy]","(ez|eS|eks)"), # ez in Brazil
                         ("ex","","[cs]","e"),

                         ("y","[aáuiíoóeéê]","","j"),
                         ("y","","[aeiíou]","j"),
                         ("m","","[bcdfglnprstv]","(m|n)"), # maybe to add a rule for m/n before a consonant that disappears [preceeding vowel becomes nasalized]
                         ("m","","$","(m|n)"), # maybe to add a rule for final m/n that disappears [preceeding vowel becomes nasalized]

                         ("ão","","","(au|an|on)"),
                         ("ãe","","","(aj|an)"),
                         ("ãi","","","(aj|an)"),
                         ("õe","","","(oj|on)"),
                         ("i","[aáuoóeéê]","","j"),
                         ("i","","[aeou]","j"),

                         ("â","","","a"),
                         ("à","","","a"),
                         ("á","","","a"),
                         ("ã","","","(a|an|on)"),
                         ("é","","","e"),
                         ("ê","","","e"),
                         ("í","","","i"),
                         ("ô","","","o"),
                         ("ó","","","o"),
                         ("õ","","","(o|on)"),
                         ("ú","","","u"),
                         ("ü","","","u"),

                         ("aue","","","aue"),

                         # LATIN ALPHABET
                         ("a","","","a"),
                         ("b","","","b"),
                         ("c","","","k"),
                         ("d","","","d"),
                         ("e","","","(e|i)"),
                         ("f","","","f"),
                         ("g","","","g"),
                         ("h","","","h"),
                         ("i","","","i"),
                         ("j","","","Z"),
                         ("k","","","k"),
                         ("l","","","l"),
                         ("m","","","m"),
                         ("n","","","n"),
                         ("o","","","(o|u)"),
                         ("p","","","p"),
                         ("q","","","k"),
                         ("r","","","r"),
                         ("s","","","S"),
                         ("t","","","t"),
                         ("u","","","u"),
                         ("v","","","v"),
                         ("w","","","v"),
                         ("x","","","(S|ks)"),
                         ("y","","","i"),
                         ("z","","","z"),


                         )
