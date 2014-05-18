# -*- coding: utf-8 -*-

import abydos.phonetic
import unicodedata

def fingerprint(phrase):
    phrase = unicodedata.normalize('NFKD', unicode(phrase.strip().lower()))
    phrase = filter(lambda c: (c.isalnum() or c.isspace()), phrase)
    phrase = " ".join(sorted(list(set(phrase.split()))))
    return phrase

def qgram_fingerprint(phrase, q=2):
    pass

def phonetic_fingerprint(phrase, phonetic_algorithm=abydos.phonetic.double_metaphone, args=None):
    pass
