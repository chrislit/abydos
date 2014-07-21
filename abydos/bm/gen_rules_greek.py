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

_gen_rules_greek = (

                    ("αυ","","$","af"),  # "av" before vowels and voiced consonants, "af" elsewhere
                    ("αυ","","(κ|π|σ|τ|φ|θ|χ|ψ)","af"),
                    ("αυ","","","av"),
                    ("ευ","","$","ef"), # "ev" before vowels and voiced consonants, "ef" elsewhere
                    ("ευ","","(κ|π|σ|τ|φ|θ|χ|ψ)","ef"),
                    ("ευ","","","ev"),
                    ("ηυ","","$","if"), # "iv" before vowels and voiced consonants, "if" elsewhere
                    ("ηυ","","(κ|π|σ|τ|φ|θ|χ|ψ)","if"),
                    ("ηυ","","","iv"),
                    ("ου","","","u"),  # [u:]

                    ("αι","","","aj"),  # modern [e]
                    ("ει","","","ej"), # modern [i]
                    ("οι","","","oj"), # modern [i]
                    ("ωι","","","oj"),
                    ("ηι","","","ej"),
                    ("υι","","","i"), # modern Greek "i"

                    ("γγ","(ε|ι|η|α|ο|ω|υ)","(ε|ι|η)","(nj|j)"),
                    ("γγ","","(ε|ι|η)","j"),
                    ("γγ","(ε|ι|η|α|ο|ω|υ)","","(ng|g)"),
                    ("γγ","","","g"),
                    ("γκ","^","","g"),
                    ("γκ","(ε|ι|η|α|ο|ω|υ)","(ε|ι|η)","(nj|j)"),
                    ("γκ","","(ε|ι|η)","j"),
                    ("γκ","(ε|ι|η|α|ο|ω|υ)","","(ng|g)"),
                    ("γκ","","","g"),
                    ("γι","","(α|ο|ω|υ)","j"),
                    ("γι","","","(gi|i)"),
                    ("γε","","(α|ο|ω|υ)","j"),
                    ("γε","","","(ge|je)"),

                    ("κζ","","","gz"),
                    ("τζ","","","dz"),
                    ("σ","","(β|γ|δ|μ|ν|ρ)","z"),

                    ("μβ","","","(mb|b)"),
                    ("μπ","^","","b"),
                    ("μπ","(ε|ι|η|α|ο|ω|υ)","","mb"),
                    ("μπ","","","b"), # after any consonant
                    ("ντ","^","","d"),
                    ("ντ","(ε|ι|η|α|ο|ω|υ)","","(nd|nt)"), # Greek is "nd"
                    ("ντ","","","(nt|d)"), # Greek is "d" after any consonant

                    ("ά","","","a"),
                    ("έ","","","e"),
                    ("ή","","","(i|e)"),
                    ("ί","","","i"),
                    ("ό","","","o"),
                    ("ύ","","","(Q|i|u)"),
                    ("ώ","","","o"),
                    ("ΰ","","","(Q|i|u)"),
                    ("ϋ","","","(Q|i|u)"),
                    ("ϊ","","","j"),

                    ("α","","","a"),
                    ("β","","","(v|b)"), # modern "v", old "b"
                    ("γ","","","g"),
                    ("δ","","","d"),    # modern like "th" in English "them", old "d"
                    ("ε","","","e"),
                    ("ζ","","","z"),
                    ("η","","","(i|e)"), # modern "i", old "e:"
                    ("ι","","","i"),
                    ("κ","","","k"),
                    ("λ","","","l"),
                    ("μ","","","m"),
                    ("ν","","","n"),
                    ("ξ","","","ks"),
                    ("ο","","","o"),
                    ("π","","","p"),
                    ("ρ","","","r"),
                    ("σ","","","s"),
                    ("ς","","","s"),
                    ("τ","","","t"),
                    ("υ","","","(Q|i|u)"), # modern "i", old like German "ü"
                    ("φ","","","f"),
                    ("θ","","","t"), # old greek like "th" in English "theme"
                    ("χ","","","x"),
                    ("ψ","","","ps"),
                    ("ω","","","o"),



                    )
