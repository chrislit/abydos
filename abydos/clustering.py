# -*- coding: utf-8 -*-

from .phonetic import double_metaphone
import unicodedata
from .util import qgrams

def fingerprint(phrase):
    phrase = unicodedata.normalize('NFKD', unicode(phrase.strip().lower()))
    phrase = filter(lambda c: (c.isalnum() or c.isspace()), phrase)
    phrase = ' '.join(sorted(list(set(phrase.split()))))
    return phrase

def qgram_fingerprint(phrase, q=2, start_stop=''):
    phrase = unicodedata.normalize('NFKD', unicode(phrase.strip().lower()))
    phrase = filter(lambda c: c.isalnum(), phrase)
    phrase = qgrams(phrase, q, start_stop)
    phrase = ''.join(sorted(list(set(phrase))))
    return phrase

def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone, *args):
    phrase = phonetic_algorithm(phrase, *args)
    if not isinstance(phrase, unicode):
        phrase = phrase[0]
    return fingerprint(phrase)
