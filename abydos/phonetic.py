# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from itertools import groupby
from string import maketrans
import re
import unicodedata



_russell_translation_table = dict(zip([ord(c) for c in
                                       u'ABCDEFGIKLMNOPQRSTUVXYZ'],
                                      u'12341231356712383412313'))
def russell_index(word):
    """Return the Russell Index of a word as an int

    Arguments:
    word -- the word to translate to a Russell Index value

    Description:
    This follows Robert C. Russell's Index algorithm, as described in
    US Patent 1,261,167 (1917)
    """
    word = unicodedata.normalize('NFKD', unicode(word.upper()))
    word = word.replace('GH', '')  # discard gh (rule 3)
    while word[len(word)-1] in 'SZ':
        word = word[:-1] # discard /[sz]$/ (rule 3)

    # translate according to Russell's mapping
    word = filter(lambda c: c in 'ABCDEFGIKLMNOPQRSTUVXYZ', word)
    sdx = word.translate(_russell_translation_table)

    # remove any 1s after the first occurrence
    one = sdx.find('1')+1
    if one:
        sdx = sdx[:one] + filter(lambda c: c != '1', sdx[one:])

    # remove repeating characters
    sdx = _delete_consecutive_repeats(sdx)

    # return as an int
    return int(sdx)


_russell_num_translation_table = dict(zip([ord(c) for c in u'12345678'],
                                          u'ABCDLMNR'))

def russell_index_num_to_alpha(num):
    """Return the Russell Index alphabetic string of a Index number

    Arguments:
    num -- an integer representing a Russell Index

    Description:
    This follows Robert C. Russell's Index algorithm, as described in
    US Patent 1,261,167 (1917)
    """
    num = filter(lambda c: c in '12345678', unicode(num))
    return num.translate(_russell_num_translation_table)


def russell_index_alpha(word):
    """Return the Russell Index of a word as an alphabetic string

    Arguments:
    word -- the word to translate to a Russell Index value

    Description:
    This follows Robert C. Russell's Index algorithm, as described in
    US Patent 1,261,167 (1917)
    """
    return russell_index_num_to_alpha(russell_index(word))


_soundex_translation_table = dict(zip([ord(c) for c in
                                       u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'],
                                      u'01230129022455012623019202'))
def soundex(word, maxlength=4, var='American'):
    """Return the Soundex value of a word

    Arguments:
    word -- the word to translate to Soundex
    maxlength -- the length of the code returned (defaults to 4)
    var -- the variant of the algorithm to employ (defaults to 'American'):
        'American' follows the American Soundex algorithm, as described at
        http://www.archives.gov/publications/general-info-leaflets/55-census.html
        and in Knuth(1998:394)
        'special' follows the rules from the 1880-1910 US Census, in which
        h & w are not treated as 
    """
    # uppercase, normalize, decompose, and filter non-A-Z
    word = unicodedata.normalize('NFKD', unicode(word.upper()))
    word = filter(lambda c: c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', word)
    
    # apply the Soundex algorithm
    sdx = word.translate(_soundex_translation_table)

    if var == 'special':
        sdx = sdx.replace('9', '0') # special rule for 1880-1910 census
    else:
        sdx = sdx.replace('9', '') # rule 1
    sdx = _delete_consecutive_repeats(sdx) # rule 3

    if word[0] in 'HW':
        sdx = word[0] + sdx
    else:
        sdx = word[0] + sdx[1:]
    sdx = sdx.replace('0', '') # rule 1

    sdx += ('0'*maxlength) # rule 4

    return sdx[:maxlength]


def koelner_phonetik(word):
    """Given a string 'word', returns its Int value according to the
    Kölner Phonetik
    """
    def _before(word, i, letters):
        if i > 0 and word[i-1] in letters:
            return True
        return False

    def _after(word, i, letters):
        if i+1 < len(word) and word[i+1] in letters:
            return True
        return False

    sdx = ''

    word = word.replace('ß', 'SS')
    word = word.upper()

    word = word.replace('Ä', 'AE')
    word = word.replace('Ö', 'OE')
    word = word.replace('Ü', 'UE')


    for i in range(len(word)):
        if word[i] in 'AEIJYOU':
            sdx += '0'
        elif word[i] in 'B':
            sdx += '1'
        elif word[i] in 'P':
            if _before(word, i, 'H'):
                sdx += '3'
            else:
                sdx += '1'
        elif word[i] in 'DT':
            if _before(word, i, 'CSZ'):
                sdx += '8'
            else:
                sdx += '2'
        elif word[i] in 'FVW':
            sdx += '3'
        elif word[i] in 'GKQ':
            sdx += '4'
        elif word[i] in 'C':
            if _after(word, i, 'SZ'):
                sdx += '8'
            elif i == 0:
                if _after(word, i, 'AHKLOQRUX'):
                    sdx += '4'
                else:
                    sdx += '8'
            elif _before(word, i, 'AHKOQUX'):
                sdx += '4'
            else:
                sdx += '8'
        elif word[i] in 'X':
            if _after(word, i, 'CKQ'):
                sdx += '8'
            else:
                sdx += '48'
        elif word[i] in 'L':
            sdx += '5'
        elif word[i] in 'MN':
            sdx += '6'
        elif word[i] in 'R':
            sdx += '7'
        elif word[i] in 'SZ':
            sdx += '8'

    sdx = _delete_consecutive_repeats(sdx)

    sdx = sdx.replace('0', '')

    return int(sdx)


def koelner_phonetik_num_to_alpha(num):
    """Given the numeric form of a Kölner Phonetik value, returns an
    alphabetic form
    """
    num = str(num)
    return num.translate(maketrans('012345678', 'APTFKLNRS'))


def koelner_phonetik_alpha(word):
    """Given a string 'word', returns an alphabetic value representing
    its Kölner Phonetik value
    """
    return koelner_phonetik_num_to_alpha(koelner_phonetik(word))


def nysiis(word, maxlength=6):
    """Return the New York State Identification and Intelligence System
        (NYSIIS) coding of a string

    Arguments:
    word -- the word to apply the match rating approach to
    maxlength -- the maximum length (default 6) of the code to return

    Description:
    A description of the algorithm can be found at
    https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System
    """
    _vowels = 'AEIOU'

    word = filter(lambda i: i.isalpha(), word.upper())

    if word.startswith('MAC'):
        word = 'MCC'+word[3:]
    if word.startswith('KN'):
        word = 'NN'+word[2:]
    if word.startswith('K'):
        word = 'C'+word[1:]
    if word.startswith('PH') or word.startswith('PF'):
        word = 'FF'+word[2:]
    if word.startswith('SCH'):
        word = 'SSS'+word[3:]

    if word.endswith('EE') or word.endswith('IE'):
        word = word[:-2]+'Y'
    if word.endswith('DT') or word.endswith('RT') or word.endswith('RD') or word.endswith('NT') or word.endswith('ND'):
        word = word[:-2]+'D'

    key = word[0]

    skip = 0
    for i in xrange(1,len(word)):
        if i >= len(word):
            continue
        elif skip:
            skip -= 1
            continue
        elif word[i:i+2] == 'EV':
            word = word[:i] + 'AF' + word[i+2:]
            skip = 1
        elif word[i] in _vowels:
            word = word[:i] + 'A' + word[i+1:]
        elif word[i] == 'Q':
            word = word[:i] + 'G' + word[i+1:]
        elif word[i] == 'Z':
            word = word[:i] + 'S' + word[i+1:]
        elif word[i] == 'M':
            word = word[:i] + 'N' + word[i+1:]
        elif word[i:i+2] == 'KN':
            word = word[:i] + 'N' + word[i+2:]
        elif word[i] == 'K':
            word = word[:i] + 'C' + word[i+1:]
        elif word[i:i+3] == 'SCH':
            word = word[:i] + 'SSS' + word[i+3:]
            skip = 2
        elif word[i:i+2] == 'PH':
            word = word[:i] + 'FF' + word[i+2:]
            skip = 1
        elif word[i] == 'H' and (word[i-1] not in _vowels or word[i+1:i+2] not in _vowels):
            word = word[:i] + word[i-1] + word[i+1:]
        elif word[i] == 'W' and word[i-1] in _vowels:
            word = word[:i] + word[i-1] + word[i+1:]

        if word[i] != key[-1]:
            key += word[i]

    if key[-1] == 'S':
        key = key[:-1]
    if key[-2:] == 'AY':
        key = key[:-2] + 'Y'
    if key[-1:] == 'A':
        key = key[:-1]

    return key[:maxlength]


def mra(word):
    """Return the personal numeric identifier (PNI) for a word, derived by
        the Western Airlines Surname Match Rating Algorithm

    Arguments:
    word -- the word to apply the match rating approach to

    Description:
    A description of the algorithm can be found on page 18 of
    https://archive.org/details/accessingindivid00moor
    """
    word = word.upper()
    word = word[0]+filter(lambda c: c not in 'AEIOU', word[1:])
    word = _delete_consecutive_repeats(word)
    if len(word)>6:
        word = word[:3]+word[-3:]
    return word


def metaphone(word, maxlength=float('inf')):
    """Return the Metaphone encoding of a word

    Arguments:
    word -- the word to apply the Metaphone algorithm to
    maxlength -- the maximum length of the returned Metaphone code
        (defaults to unlimited, but in Philips' original implementation
        this was 4)

    Description:
    Based on Lawrence Philips' BASIC code from 1990:
    http://aspell.net/metaphone/metaphone.basic
    This incorporates some corrections to the above code, particularly
    some of those suggested by Michael Kuhn in:
    http://aspell.net/metaphone/metaphone-kuhn.txt
    """
    _vowels = list('AEIOU')
    _frontv = list('EIY')
    _varson = list('CSPTG')

    # As in variable sound--those modified by adding an "h"
    ename = filter(lambda i: i.isalnum(), word.upper())

    # Delete nonalphanumeric characters and make all caps
    if ename == '':
        return ''
    if ename[0:2] in ['PN', 'AE', 'KN', 'GN', 'WR']:
        ename = ename[1:]
    elif ename[0] == 'X':
        ename = 'S' + ename[1:]
    elif ename[0:2] == 'WH':
        ename = 'W' + ename[2:]

    # Convert to metaph
    l = len(ename)-1
    metaph = ''
    for n in xrange(len(ename)):
        if len(metaph) >= maxlength:
            break
        if ename[n] not in 'GT' and n > 0 and ename[n-1] == ename[n]:
            continue

        if ename[n] in _vowels and n == 0:
            metaph = ename[n]

        elif ename[n] == 'B':
            if n != l or ename[n-1] != 'M':
                metaph += ename[n]

        elif ename[n] == 'C':
            if not (n > 0 and ename[n-1] == 'S' and ename[n+1:n+2] in _frontv):
                if ename[n+1:n+3] == 'IA':
                    metaph += 'X'
                elif ename[n+1:n+2] in _frontv:
                    metaph += 'S'
                elif n > 0 and ename[n-1:n+2] == 'SCH':
                    metaph += 'K'
                elif ename[n+1:n+2] == 'H':
                    if n == 0 and n+1 < l and ename[n+2:n+3] not in _vowels:
                        metaph += 'K'
                    else:
                        metaph += 'X'
                else:
                    metaph += 'K'

        elif ename[n] == 'D':
            if ename[n+1:n+2] == 'G' and ename[n+2:n+3] in _frontv:
                metaph += 'J'
            else:
                metaph += 'T'

        elif ename[n] == 'G':
            if ename[n+1:n+2] == 'H' and (n+1 < l and ename[n+2] not in _vowels):
                continue
            elif n > 0 and (n+1 == l or (ename[n+1:n+4] == 'NED' and n+3 == l)):
                continue
            elif n-1 > 0 and n+1 < l and ename[n-1] == 'D' and ename[n+1] in _frontv:
                continue
            elif ename[n+1:n+2] in _frontv:
                if n == 0 or ename[n-1] != 'G':
                    metaph += 'J'
                else:
                    metaph += 'K'
            else:
                metaph += 'K'

        elif ename[n] == 'H':
            if n > 0 and ename[n-1] in _vowels and ename[n+1:n+2] not in _vowels:
                continue
            elif n > 0 and ename[n-1] in _varson:
                continue
            else:
                metaph += 'H'

        elif ename[n] in 'FJLMNR':
            metaph += ename[n]

        elif ename[n] == 'K':
            if n > 0 and ename[n-1] == 'C':
                continue
            else:
                metaph += 'K'

        elif ename[n] == 'P':
            if ename[n+1:n+2] == 'H':
                metaph += 'F'
            else:
                metaph += 'P'

        elif ename[n] == 'Q':
            metaph += 'K'

        elif ename[n] == 'S':
            if n > 0 and n+2 < l and ename[n+1] == 'I' and ename[n+2] in 'OA':
                metaph += 'X'
            elif ename[n+1:n+2] == 'H':
                metaph += 'X'
            else:
                metaph += 'S'

        elif ename[n] == 'T':
            if n > 0 and n+2 < l and ename[n+1] == 'I' and ename[n+2] in 'OA':
                metaph += 'X'
            elif ename[n+1:n+2] == 'H':
                metaph += '0'
            elif ename[n+1:n+3] != 'CH':
                metaph += 'T'

        elif ename[n] == 'V':
            metaph += 'F'

        elif ename[n] in 'WY':
            if ename[n+1:n+2] in _vowels:
                metaph += ename[n]

        elif ename[n] == 'X':
            metaph += 'KS'

        elif ename[n] == 'Z':
            metaph += 'S'

    return metaph


def double_metaphone(word, maxlength=float('inf')):
    """Return the Double Metaphone encodings of a word as a tuple

    Arguments:
    word -- the word to apply the Double Metaphone algorithm to
    maxlength -- the maximum length of the returned Double Metaphone
        codes (defaults to unlimited, but in Philips' original
        implementation this was 4)

    Description:
    Based on Lawrence Philips' (Visual) C++ code from 1999:
    http://aspell.net/metaphone/dmetaph.cpp
    """
    primary = ''
    secondary = ''

    def _slavo_germanic():
        if ('W' in word or 'K' in word or 'CZ' in word):
            return True
        return False

    def _metaph_add(p, s=''):
        newp = primary
        news = secondary
        if p:
            newp += p
        if s:
            if s != ' ':
                news += s
        else:
            if p and (p != ' '):
                news += p
        return (newp, news)

    def _is_vowel(pos):
        if pos < 0:
            return False
        return word[pos] in list('AEIOUY')

    def _get_at(pos):
        if not (pos < 0):
            return word[pos]

    def _string_at(pos, slen, substrings):
        if pos < 0:
            return False
        for s in substrings:
            if word[pos:pos+slen] == s:
                return True
        return False

    current = 0
    length = len(word)
    if length < 0:
        return ''
    last = length - 1

    word = filter(lambda i: True, word.upper())

    # Pad the original string so that we can index beyond the edge of the world
    word += '     '

    # Skip these when at start of word
    if word[0:2] in ['GN', 'KN', 'PN', 'WR', 'PS']:
        current += 1

    # Initial 'X' is pronounced 'Z' e.g. 'Xavier'
    if _get_at(0) == 'X':
        (primary, secondary) = _metaph_add('S') # 'Z' maps to 'S'
        current += 1

    # Main loop
    while(True or len(primary) < maxlength or len(secondary) < maxlength):
        if current >= length:
            break

        if _get_at(current) in list('AEIOUY'):
            if current == 0:
                # All init vowels now map to 'A'
                (primary, secondary) = _metaph_add('A')
            current +=1
            continue

        elif _get_at(current) == 'B':
            # "-mb", e.g", "dumb", already skipped over...
            (primary, secondary) = _metaph_add('P')
            if _get_at(current + 1) == 'B':
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'Ç':
            (primary, secondary) = _metaph_add('S')
            current += 1
            continue

        elif _get_at(current) == 'C':
            # Various Germanic
            if (current > 1 and not _is_vowel(current - 2) and
                _string_at((current - 1), 3, ["ACH"]) and
                ((_get_at(current + 2) != 'I') and
                 ((_get_at(current + 2) != 'E') or
                  _string_at((current - 2), 6, ["BACHER", "MACHER"])))):
                (primary, secondary) = _metaph_add("K")
                current +=2
                continue

            # Special case 'caesar'
            elif current == 0 and _string_at(current, 6, ["CAESAR"]):
                (primary, secondary) = _metaph_add("S")
                current +=2
                continue

            # Italian 'chianti'
            elif _string_at(current, 4, ["CHIA"]):
                (primary, secondary) = _metaph_add("K")
                current +=2
                continue

            elif _string_at(current, 2, ["CH"]):
                # Find 'Michael'
                if  current > 0 and _string_at(current, 4, ["CHAE"]):
                    (primary, secondary) = _metaph_add("K", "X")
                    current +=2
                    continue

                # Greek roots e.g. 'chemistry', 'chorus'
                elif (current == 0 and
                      (_string_at((current + 1), 5, ["HARAC", "HARIS"]) or
                       _string_at((current + 1), 3, ["HOR", "HYM", "HIA", "HEM"]))
                      and not _string_at(0, 5, ["CHORE"])):
                    (primary, secondary) = _metaph_add("K")
                    current +=2
                    continue

                # Germanic, Greek, or otherwise 'ch' for 'kh' sound
                elif ((_string_at(0, 4, ["VAN ", "VON "]) or _string_at(0, 3, ["SCH"]))
                      # 'architect but not 'arch', 'orchestra', 'orchid'
                      or _string_at((current - 2), 6, ["ORCHES", "ARCHIT", "ORCHID"])
                      or _string_at((current + 2), 1, ["T", "S"])
                      or ((_string_at((current - 1), 1, ["A", "O", "U", "E"]) or (current == 0))
                          # e.g., 'wachtler', 'wechsler', but not 'tichner'
                          and _string_at((current + 2), 1, ["L", "R", "N", "M", "B", "H", "F", "V", "W", " "]))):
                    (primary, secondary) = _metaph_add("K")

                else:
                    if current > 0:
                        if _string_at(0, 2, ["MC"]):
                            # e.g., "McHugh"
                            (primary, secondary) = _metaph_add("K")
                        else:
                            (primary, secondary) = _metaph_add("X", "K")
                    else:
                        (primary, secondary) = _metaph_add("X")

                current +=2
                continue

            # e.g, 'czerny'
            elif _string_at(current, 2, ["CZ"]) and not _string_at((current - 2), 4, ["WICZ"]):
                (primary, secondary) = _metaph_add("S", "X")
                current += 2
                continue

            # e.g., 'focaccia'
            elif _string_at((current + 1), 3, ["CIA"]):
                (primary, secondary) = _metaph_add("X")
                current += 3

            # double 'C', but not if e.g. 'McClellan'
            elif _string_at(current, 2, ["CC"]) and not ((current == 1) and (_get_at(0) == 'M')):
                # 'bellocchio' but not 'bacchus'
                if _string_at((current + 2), 1, ["I", "E", "H"]) and not _string_at((current + 2), 2, ["HU"]):
                    # 'accident', 'accede' 'succeed'
                    if (((current == 1) and _get_at(current - 1) == 'A')
                        or _string_at((current - 1), 5, ["UCCEE", "UCCES"])):
                        (primary, secondary) = _metaph_add("KS")
                    # 'bacci', 'bertucci', other italian
                    else:
                        (primary, secondary) = _metaph_add("X")
                    current += 3
                    continue
                else: # Pierce's rule
                    (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

            elif _string_at(current, 2, ["CK", "CG", "CQ"]):
                (primary, secondary) = _metaph_add("K")
                current += 2
                continue

            elif _string_at(current, 2, ["CI", "CE", "CY"]):
                # Italian vs. English
                if _string_at(current, 3, ["CIO", "CIE", "CIA"]):
                    (primary, secondary) = _metaph_add("S", "X")
                else:
                    (primary, secondary) = _metaph_add("S")
                current += 2
                continue

            # else
            else:
                (primary, secondary) = _metaph_add("K")

                # name sent in 'mac caffrey', 'mac gregor
                if _string_at((current + 1), 2, [" C", " Q", " G"]):
                    current += 3
                elif (_string_at((current + 1), 1, ["C", "K", "Q"])
                      and not _string_at((current + 1), 2, ["CE", "CI"])):
                    current += 2
                else:
                    current += 1
                continue

        elif _get_at(current) == 'D':
            if _string_at(current, 2, ["DG"]):
                if _string_at((current + 2), 1, ["I", "E", "Y"]):
                    # e.g. 'edge'
                    (primary, secondary) = _metaph_add("J")
                    current += 3
                    continue
                else:
                    # e.g. 'edgar'
                    (primary, secondary) = _metaph_add("TK")
                    current += 2
                    continue

            elif _string_at(current, 2, ["DT", "DD"]):
                (primary, secondary) = _metaph_add("T")
                current += 2
                continue

            # else
            else:
                (primary, secondary) = _metaph_add("T")
                current += 1
                continue

        elif _get_at(current) == 'F':
            if _get_at(current + 1) == 'F':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("F")
            continue

        elif _get_at(current) == 'G':
            if _get_at(current + 1) == 'H':
                if (current > 0) and not _is_vowel(current - 1):
                    (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

                # 'ghislane', ghiradelli
                elif current == 0:
                    if _get_at(current + 2) == 'I':
                        (primary, secondary) = _metaph_add("J")
                    else:
                        (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

                # Parker's rule (with some further refinements) - e.g., 'hugh'
                elif (((current > 1) and _string_at((current - 2), 1, ["B", "H", "D"]))
                    # e.g., 'bough'
                    or ((current > 2) and _string_at((current - 3), 1, ["B", "H", "D"]))
                    # e.g., 'broughton'
                    or ((current > 3) and _string_at((current - 4), 1, ["B", "H"]))):
                    current += 2
                    continue
                else:
                    # e.g., 'laugh', 'McLaughlin', 'cough', 'gough', 'rough', 'tough'
                    if ((current > 2)
                         and (_get_at(current - 1) == 'U')
                         and _string_at((current - 3), 1, ["C", "G", "L", "R", "T"]) ):
                        (primary, secondary) = _metaph_add("F")
                    elif ((current > 0) and _get_at(current - 1) != 'I'):
                        (primary, secondary) = _metaph_add("K")
                    current += 2
                    continue

            elif _get_at(current + 1) == 'N':
                if (current == 1) and _is_vowel(0) and not _slavo_germanic():
                    (primary, secondary) = _metaph_add("KN", "N")
                # not e.g. 'cagney'
                elif (not _string_at((current + 2), 2, ["EY"])
                      and (_get_at(current + 1) != 'Y') and not _slavo_germanic()):
                    (primary, secondary) = _metaph_add("N", "KN")
                else:
                    (primary, secondary) = _metaph_add("KN")
                current += 2
                continue

            # 'tagliaro'
            elif _string_at((current + 1), 2, ["LI"]) and not _slavo_germanic():
                (primary, secondary) = _metaph_add("KL", "L")
                current += 2
                continue

            # -ges-,-gep-,-gel-, -gie- at beginning
            elif ((current == 0)
                  and ((_get_at(current + 1) == 'Y')
                       or _string_at((current + 1), 2, ["ES", "EP", "EB", "EL", "EY", "IB", "IL", "IN", "IE", "EI", "ER"]))):
                (primary, secondary) = _metaph_add("K", "J")
                current += 2
                continue

            #  -ger-,  -gy-
            elif ((_string_at((current + 1), 2, ["ER"]) or (_get_at(current + 1) == 'Y'))
                  and not _string_at(0, 6, ["DANGER", "RANGER", "MANGER"])
                  and not _string_at((current - 1), 1, ["E", "I"])
                  and not _string_at((current - 1), 3, ["RGY", "OGY"]) ):
                (primary, secondary) = _metaph_add("K", "J")
                current += 2
                continue

            #  italian e.g, 'biaggi'
            elif (_string_at((current + 1), 1, ["E", "I", "Y"])
                  or _string_at((current - 1), 4, ["AGGI", "OGGI"])):
                # obvious germanic
                if ((_string_at(0, 4, ["VAN ", "VON "]) or _string_at(0, 3, ["SCH"]))
                    or _string_at((current + 1), 2, ["ET"])):
                    (primary, secondary) = _metaph_add("K")
                elif (_string_at((current + 1), 4, ["IER "])):
                    (primary, secondary) = _metaph_add("J")
                else:
                    (primary, secondary) = _metaph_add("J", "K")
                current += 2
                continue

            else:
                if _get_at(current + 1) == 'G':
                    current += 2
                else:
                    current += 1
                (primary, secondary) = _metaph_add("K")
                continue

        elif _get_at(current) == 'H':
            # only keep if first & before vowel or btw. 2 vowels
            if (((current == 0) or _is_vowel(current - 1))
                and _is_vowel(current + 1)):
                (primary, secondary) = _metaph_add("H")
                current += 2
            else: # also takes care of 'HH'
                current += 1
            continue

        elif _get_at(current) == 'J':
            # obvious spanish, 'jose', 'san jacinto'
            if _string_at(current, 4, ["JOSE"]) or _string_at(0, 4, ["SAN "]):
                if (((current == 0) and (_get_at(current + 4) == ' ')) or _string_at(0, 4, ["SAN "]) ):
                    (primary, secondary) = _metaph_add("H")
                else:
                    (primary, secondary) = _metaph_add("J", "H")
                current += 1
                continue

            elif (current == 0) and not _string_at(current, 4, ["JOSE"]):
                (primary, secondary) = _metaph_add("J", "A") # Yankelovich/Jankelowicz
            # Spanish pron. of e.g. 'bajador'
            elif (_is_vowel(current - 1)
                  and not _slavo_germanic()
                  and ((_get_at(current + 1) == 'A') or (_get_at(current + 1) == 'O'))):
                (primary, secondary) = _metaph_add("J", "H")
            elif (current == last):
                (primary, secondary) = _metaph_add("J", " ")
            elif (not _string_at((current + 1), 1, ["L", "T", "K", "S", "N", "M", "B", "Z"])
                  and not _string_at((current - 1), 1, ["S", "K", "L"])):
                (primary, secondary) = _metaph_add("J")

            if _get_at(current + 1) == 'J': # it could happen!
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'K':
            if _get_at(current + 1) == 'K':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("K")
            continue

        elif _get_at(current) == 'L':
            if _get_at(current + 1) == 'L':
                # Spanish e.g. 'cabrillo', 'gallegos'
                if (((current == (length - 3))
                     and _string_at((current - 1), 4, ["ILLO", "ILLA", "ALLE"]))
                    or ((_string_at((last - 1), 2, ["AS", "OS"]) or _string_at(last, 1, ["A", "O"]))
                        and _string_at((current - 1), 4, ["ALLE"]))):
                    (primary, secondary) = _metaph_add("L", " ")
                    current += 2
                    continue
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("L")
            continue

        elif _get_at(current) == 'M':
            if((_string_at((current - 1), 3, ["UMB"])
                and (((current + 1) == last) or _string_at((current + 2), 2, ["ER"])))
               # 'dumb','thumb'
               or  (_get_at(current + 1) == 'M') ):
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("M")
            continue

        elif _get_at(current) == 'N':
            if _get_at(current + 1) == 'N':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("N")
            continue

        elif _get_at(current) == 'Ñ':
            current += 1
            (primary, secondary) = _metaph_add("N")
            continue

        elif _get_at(current) == 'P':
            if _get_at(current + 1) == 'H':
                (primary, secondary) = _metaph_add("F")
                current += 2
                continue

            # also account for "campbell", "raspberry"
            elif _string_at((current + 1), 1, ["P", "B"]):
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("P")
            continue

        elif _get_at(current) == 'Q':
            if _get_at(current + 1) == 'Q':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("K")
            continue

        elif _get_at(current) == 'R':
            # french e.g. 'rogier', but exclude 'hochmeier'
            if ((current == last)
                and not _slavo_germanic()
                and _string_at((current - 2), 2, ["IE"])
                and not _string_at((current - 4), 2, ["ME", "MA"])):
                (primary, secondary) = _metaph_add("", "R")
            else:
                (primary, secondary) = _metaph_add("R")

            if _get_at(current + 1) == 'R':
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'S':
            # special cases 'island', 'isle', 'carlisle', 'carlysle'
            if _string_at((current - 1), 3, ["ISL", "YSL"]):
                current += 1
                continue

            # special case 'sugar-'
            elif (current == 0) and _string_at(current, 5, ["SUGAR"]):
                (primary, secondary) = _metaph_add("X", "S")
                current += 1
                continue

            elif _string_at(current, 2, ["SH"]):
                # Germanic
                if _string_at((current + 1), 4, ["HEIM", "HOEK", "HOLM", "HOLZ"]):
                    (primary, secondary) = _metaph_add("S")
                else:
                    (primary, secondary) = _metaph_add("X")
                current += 2
                continue

            # Italian & Armenian
            elif _string_at(current, 3, ["SIO", "SIA"]) or _string_at(current, 4, ["SIAN"]):
                if not _slavo_germanic():
                    (primary, secondary) = _metaph_add("S", "X")
                else:
                    (primary, secondary) = _metaph_add("S")
                current += 3
                continue

            # German & anglicisations, e.g. 'smith' match 'schmidt', 'snider' match 'schneider'
            # also, -sz- in Slavic language although in Hungarian it is pronounced 's'
            elif (((current == 0)
                   and _string_at((current + 1), 1, ["M", "N", "L", "W"]))
                  or _string_at((current + 1), 1, ["Z"])):
                (primary, secondary) = _metaph_add("S", "X")
                if _string_at((current + 1), 1, ["Z"]):
                    current += 2
                else:
                    current += 1
                continue

            elif _string_at(current, 2, ["SC"]):
                # Schlesinger's rule
                if _get_at(current + 2) == 'H':
                    # dutch origin, e.g. 'school', 'schooner'
                    if _string_at((current + 3), 2, ["OO", "ER", "EN", "UY", "ED", "EM"]):
                        # 'schermerhorn', 'schenker'
                        if _string_at((current + 3), 2, ["ER", "EN"]):
                            (primary, secondary) = _metaph_add("X", "SK")
                        else:
                            (primary, secondary) = _metaph_add("SK")
                        current += 3
                        continue
                    else:
                        if (current == 0) and not _is_vowel(3) and (_get_at(3) != 'W'):
                            (primary, secondary) = _metaph_add("X", "S")
                        else:
                            (primary, secondary) = _metaph_add("X")
                        current += 3
                        continue

                elif _string_at((current + 2), 1, ["I", "E", "Y"]):
                    (primary, secondary) = _metaph_add("S")
                    current += 3
                    continue

                # else
                else:
                    (primary, secondary) = _metaph_add("SK")
                    current += 3
                    continue

            else:
                # french e.g. 'resnais', 'artois'
                if (current == last) and _string_at((current - 2), 2, ["AI", "OI"]):
                    (primary, secondary) = _metaph_add("", "S")
                else:
                    (primary, secondary) = _metaph_add("S")

                if _string_at((current + 1), 1, ["S", "Z"]):
                    current += 2
                else:
                    current += 1
                continue

        elif _get_at(current) == 'T':
            if _string_at(current, 4, ["TION"]):
                (primary, secondary) = _metaph_add("X")
                current += 3
                continue

            elif _string_at(current, 3, ["TIA", "TCH"]):
                (primary, secondary) = _metaph_add("X")
                current += 3
                continue

            elif (_string_at(current, 2, ["TH"])
                  or _string_at(current, 3, ["TTH"])):
                # special case 'thomas', 'thames' or germanic
                if (_string_at((current + 2), 2, ["OM", "AM"])
                    or _string_at(0, 4, ["VAN ", "VON "])
                    or _string_at(0, 3, ["SCH"])):
                    (primary, secondary) = _metaph_add("T")
                else:
                    (primary, secondary) = _metaph_add("0", "T")
                current += 2
                continue

            elif _string_at((current + 1), 1, ["T", "D"]):
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("T")
            continue

        elif _get_at(current) == 'V':
            if _get_at(current + 1) == 'V':
                current += 2
            else:
                current += 1
            (primary, secondary) = _metaph_add("F")
            continue

        elif _get_at(current) == 'W':
            # can also be in middle of word
            if _string_at(current, 2, ["WR"]):
                (primary, secondary) = _metaph_add("R")
                current += 2
                continue
            elif ((current == 0)
                  and (_is_vowel(current + 1) or _string_at(current, 2, ["WH"]))):
                # Wasserman should match Vasserman
                if _is_vowel(current + 1):
                    (primary, secondary) = _metaph_add("A", "F")
                else:
                    # need Uomo to match Womo
                    (primary, secondary) = _metaph_add("A")

            # Arnow should match Arnoff
            if (((current == last) and _is_vowel(current - 1))
                or _string_at((current - 1), 5, ["EWSKI", "EWSKY", "OWSKI", "OWSKY"])
                or _string_at(0, 3, ["SCH"])):
                (primary, secondary) = _metaph_add("", "F")
                current += 1
                continue
            # Polish e.g. 'filipowicz'
            elif _string_at(current, 4, ["WICZ", "WITZ"]):
                (primary, secondary) = _metaph_add("TS", "FX")
                current += 4
                continue
            # else skip it
            else:
                current +=1
                continue

        elif _get_at(current) == 'X':
            # French e.g. breaux
            if (not ((current == last)
                     and (_string_at((current - 3), 3, ["IAU", "EAU"])
                          or _string_at((current - 2), 2, ["AU", "OU"])))):
                (primary, secondary) = _metaph_add("KS")

            if _string_at((current + 1), 1, ["C", "X"]):
                current += 2
            else:
                current += 1
            continue

        elif _get_at(current) == 'Z':
            # Chinese Pinyin e.g. 'zhao'
            if _get_at(current + 1) == 'H':
                (primary, secondary) = _metaph_add("J")
                current += 2
                continue
            elif (_string_at((current + 1), 2, ["ZO", "ZI", "ZA"])
                  or (_slavo_germanic() and ((current > 0) and _get_at(current - 1) != 'T'))):
                (primary, secondary) = _metaph_add("S", "TS")
            else:
                (primary, secondary) = _metaph_add("S")

            if _get_at(current + 1) == 'Z':
                current += 2
            else:
                current += 1
            continue

        else:
            current += 1

    if maxlength < float('inf'):
        primary = primary[:maxlength]
        secondary = secondary[:maxlength]
    if primary == secondary:
        secondary = ''

    return (primary, secondary)


def caverphone(word, version=2):
    """Return the Caverphone encoding of a word

    Arguments:
    word -- the word to apply the Caverphone algorithm to
    version -- the version of Caverphone to employ for encoding
                (defaults to 2)

    Description:
    A description of version 1 of the algorithm can be found at:
    http://caversham.otago.ac.nz/files/working/ctp060902.pdf
    A description of version 2 of the algorithm can be found at:
    http://caversham.otago.ac.nz/files/working/ctp150804.pdf
    """
    word = word.lower()
    word = filter(lambda c: c in 'abcdefghijklmnopqrstuvwxyz', word)

    if version!=1 and word.endswith('e'):
        word = word[:-1]
    if word.startswith('cough'):
        word = 'cou2f'+word[5:]
    if word.startswith('rough'):
        word = 'rou2f'+word[5:]
    if word.startswith('tough'):
        word = 'tou2f'+word[5:]
    if word.startswith('enough'):
        word = 'enou2f'+word[6:]
    if version!=1 and word.startswith('trough'):
        word = 'trou2f'+word[6:]
    if word.startswith('gn'):
        word = '2n'+word[2:]
    if word.endswith('mb'):
        word = word[:-1]+'2'
    word = word.replace('cq', '2q')
    word = word.replace('ci', 'si')
    word = word.replace('ce', 'se')
    word = word.replace('cy', 'sy')
    word = word.replace('tch', '2ch')
    word = word.replace('c', 'k')
    word = word.replace('q', 'k')
    word = word.replace('x', 'k')
    word = word.replace('v', 'f')
    word = word.replace('dg', '2g')
    word = word.replace('tio', 'sio')
    word = word.replace('tia', 'sia')
    word = word.replace('d', 't')
    word = word.replace('ph', 'fh')
    word = word.replace('b', 'p')
    word = word.replace('sh', 's2')
    word = word.replace('z', 's')
    if word[0] in 'aeiou':
        word = 'A'+word[1:]
    word = word.replace('a', '3')
    word = word.replace('e', '3')
    word = word.replace('i', '3')
    word = word.replace('o', '3')
    word = word.replace('u', '3')
    if version!=1:
        word = word.replace('j', 'y')
        if word.startswith('y3'):
            word = 'Y3'+word[2:]
        if word.startswith('y'):
            word = 'A'+word[1:]
        word = word.replace('y', '3')
    word = word.replace('3gh3', '3kh3')
    word = word.replace('gh', '22')
    word = word.replace('g', 'k')
    word = re.sub(r's+', r'S', word)
    word = re.sub(r't+', r'T', word)
    word = re.sub(r'p+', r'P', word)
    word = re.sub(r'k+', r'K', word)
    word = re.sub(r'f+', r'F', word)
    word = re.sub(r'm+', r'M', word)
    word = re.sub(r'n+', r'N', word)
    word = word.replace('w3', 'W3')
    if version==1:
        word = word.replace('wy', 'Wy')
    word = word.replace('wh3', 'Wh3')
    if version==1:
        word = word.replace('why', 'Why')
    if version!=1 and word.endswith('w'):
        word = word[:-1]+'3'
    word = word.replace('w', '2')
    if word.startswith('h'):
        word = 'A'+word[1:]
    word = word.replace('h', '2')
    word = word.replace('r3', 'R3')
    if version==1:
        word = word.replace('ry', 'Ry')
    if version!=1 and word.endswith('r'):
        word = word[:-1]+'3'
    word = word.replace('r', '2')
    word = word.replace('l3', 'L3')
    if version==1:
        word = word.replace('ly', 'Ly')
    if version!=1 and word.endswith('l'):
        word = word[:-1]+'3'
    word = word.replace('l', '2')
    if version==1:
        word = word.replace('j', 'y')
        word = word.replace('y3', 'Y3')
        word = word.replace('y', '2')
    word = word.replace('2', '')
    if version!=1 and word.endswith('3'):
        word = word[:-1]+'A'
    word = word.replace('3', '')
    word = word+'1'*10
    if version!=1:
        word = word[:10]
    else:
        word = word[:6]

    return word


"""def phonemicize_graphemes(word):
    phones = word
    #phones = phones.replace(
"""

def _delete_consecutive_repeats(word):
    return ''.join(char for char, _ in groupby(word))


"""def test():
    words = ['ANASTHA','DAVIS-CARTER','ESCARMANT','MCCALL','MCCROREY',
             'MERSEAL','PIEURISSAINT','ROTMAN','SCHEVEL','SCHROM',
             'SEAL','SPARR','STARLEPER','THRASH']

    for w in words:
        print w + '\t\t' + ' '.join(double_metaphone(w))
"""
