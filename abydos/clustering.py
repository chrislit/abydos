# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from ._compat import _unicode
from .phonetic import double_metaphone
import unicodedata
from .util import qgrams

def fingerprint(phrase):
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join(filter(lambda c: (c.isalnum() or c.isspace()), phrase))
    phrase = ' '.join(sorted(list(set(phrase.split()))))
    return phrase

def qgram_fingerprint(phrase, q=2, start_stop=''):
    phrase = unicodedata.normalize('NFKD', _unicode(phrase.strip().lower()))
    phrase = ''.join(filter(lambda c: c.isalnum(), phrase))
    phrase = qgrams(phrase, q, start_stop)
    phrase = ''.join(sorted(list(set(phrase))))
    return phrase

def phonetic_fingerprint(phrase, phonetic_algorithm=double_metaphone, *args):
    phrase = phonetic_algorithm(phrase, *args)
    if not isinstance(phrase, _unicode):
        phrase = phrase[0]
    return fingerprint(phrase)
