# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
import numpy
import sys
import math
from collections import defaultdict
from .util import _qgram_counts, qgrams


def levenshtein(s, t, mode='lev', cost=(1,1,1,1)):
    """Return the Levenshtein distance between two string arguments

    Arguments:
    s, t -- two strings to be compared
    mode -- specifies a mode for computing the Levenshtein distance:
              'lev' (default) computes the ordinary Levenshtein distance,
                in which edits may include inserts, deletes, and substitutions
              'osa' computes the Optimal String Alignment distance, in which
                edits may include inserts, deletes, substitutions, and
                transpositions but substrings may only be edited once
              'dam' computes the Damerau-Levenshtein distance, in which
                edits may include inserts, deletes, substitutions, and
                transpositions and substrings may undergo repeated edits
    cost -- a 4-tuple representing the cost of the four possible edits:
              inserts, deletes, substitutions, and transpositions,
              respectively (by default: (1,1,1,1))
    """
    ins_cost, del_cost, sub_cost, trans_cost = cost

    if len(s) == 0:
        return len(t) * ins_cost
    if len(t) == 0:
        return len(s) * del_cost

    if 'dam' not in mode:
        d = numpy.zeros((len(s)+1,len(t)+1), dtype=numpy.int)
        for i in xrange(len(s)+1):
            d[i,0] = i
        for j in xrange(len(t)+1):
            d[0,j] = j

        for i in xrange(len(s)):
            for j in xrange(len(t)):
                d[i+1,j+1] = min(
                    d[i+1,j] + ins_cost, # ins
                    d[i,j+1] + del_cost, # del
                    d[i,j] + (sub_cost if s[i] != t[j] else 0) # sub (or equal)
                )

                if mode=='osa':
                    if (i+1 > 1 and j+1 > 1 and s[i] == t[j-1] and s[i-1] == t[j]):
                        d[i+1,j+1] = min(
                            d[i+1,j+1],
                            d[i-1,j-1] + trans_cost  # transposition
                        )

        return d[len(s),len(t)]

    else:
        """Damerau-Levenshtein code based on Java code by Kevin L. Stern,
        under the MIT license:
        https://github.com/KevinStern/software-and-algorithms/blob/master/src/main/java/blogspot/software_and_algorithms/stern_library/string/DamerauLevenshteinAlgorithm.java"""
        if 2*trans_cost < ins_cost + del_cost:
            raise ValueError('Unsupported cost assignment; the cost of two transpositions must not be less than the cost of an insert plus a delete.')

        d = numpy.zeros((len(s))*(len(t)), dtype=numpy.int).reshape((len(s), len(t)))

        if s[0] != t[0]:
            d[0,0] = min(sub_cost, ins_cost + del_cost)

        s_index_by_character = {}
        s_index_by_character[s[0]] = 0
        for i in xrange(1, len(s)):
            del_distance = d[i-1,0] + del_cost
            ins_distance = (i+1) * del_cost + ins_cost
            match_distance = i * del_cost + (0 if s[i] == t[0] else sub_cost)
            d[i,0] = min(del_distance, ins_distance, match_distance)

        for j in xrange(1, len(t)):
            del_distance = (j+1) * ins_cost + del_cost
            ins_distance = d[0,j-1] + ins_cost
            match_distance = j * ins_cost + (0 if s[0] == t[j] else sub_cost)
            d[0,j] = min(del_distance, ins_distance, match_distance)

        for i in xrange(1, len(s)):
            max_s_letter_match_index = (0 if s[i] == t[0] else -1)
            for j in xrange(1, len(t)):
                candidate_swap_index = -1 if t[j] not in s_index_by_character else s_index_by_character[t[j]]
                j_swap = max_s_letter_match_index
                del_distance = d[i-1,j] + del_cost
                ins_distance = d[i,j-1] + ins_cost
                match_distance = d[i-1,j-1]
                if s[i] != t[j]:
                    match_distance += sub_cost
                else:
                    max_s_letter_match_index = j

                if candidate_swap_index != -1 and j_swap != -1:
                    i_swap = candidate_swap_index

                    if i_swap == 0 and j_swap == 0:
                        pre_swap_cost = 0
                    else:
                        pre_swap_cost = d[max(0, i_swap-1), max(0, j_swap-1)]
                    swap_distance = pre_swap_cost + (i - i_swap - 1) * del_cost + (j - j_swap - 1) * ins_cost + trans_cost
                else:
                    swap_distance = sys.maxint

                d[i,j] = min(del_distance, ins_distance, match_distance, swap_distance)
            s_index_by_character[s[i]] = i

        return d[len(s)-1, len(t)-1]


def hamming(s, t, allow_different_lengths=False):
    """Return the hamming distance between two string arguments.

    Arguments:
    s, t -- two strings to be compared
    allow_different_lengths --
      If False, an exception is raised in the case of strings of unequal
      lengths.
      If True, this returns the hamming distance for those characters that
      have a matching character in both strings plus the difference in the
      strings' lengths. This is equivalent to  extending the shorter string
      with obligatoriliy non-matching characters.
    """
    if not allow_different_lengths and len(s) != len(t):
        raise ValueError("Undefined for sequences of unequal length; set allow_different_lengths to True for Hamming distance between strings of unequal lengths.")
    dist = 0
    if allow_different_lengths:
        dist += abs(len(s)-len(t))
    dist += sum(c1 != c2 for c1, c2 in zip(s, t))
    return dist


def tversky_index(s, t, q=2, alpha=1, beta=1, bias=None):
    """Return the Tversky index of two string arguments.

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram
    alpha, beta -- two Tversky index parameters as indicated in the description below

    The Tversky index is defined as:
    For two sets X and Y:
    S(X,Y) = |X∩Y| / (|X∩Y| + α|X-Y| + β|Y-X|)

    α = β = 1 is equivalent to the Jaccard & Tanimoto similarity coefficients
    α = β = 0.5 is equivalent to the Sorensen-Dice similarity coefficient

    Unequal α and β will tend to emphasize one or the other set's contributions (α>β emphasizes the contributions of X over Y; α<β emphasizes the contributions of Y over X.
    α and β > 1 emphsize unique contributions over the intersection.
    α and β < 1 emphsize the intersection over unique contributions.

    The symmetric variant is defined in Jiminez, Sergio, Claudio Becerra, and Alexander Gelbukh. 2013. SOFTCARDINALITY-CORE: Improving Text Overlap with Distributional Measures for Semantic Textual Similarity. This is activated by specifying a bias parameter. http://aclweb.org/anthology/S/S13/S13-1028.pdf
    """
    if alpha < 0 or beta < 0:
        raise ValueError('Unsupported weight assignment; alpha and beta must be greater than or equal to 0.')

    if s == t:
        return 1.0
    elif len(s) == 0 and len(t) == 0:
        return 1.0
    q_s, q_t, q_intersection = _qgram_counts(s, t, q)
    if bias is None:
        return q_intersection / (q_intersection + alpha * (q_s - q_intersection) + beta * (q_t - q_intersection))
    else:
        a = min(q_s - q_intersection, q_t - q_intersection)
        b = max(q_s - q_intersection, q_t - q_intersection)
        c = q_intersection + bias
        return c / (beta * (alpha * a + (1 - alpha) * b) + c)


def sorensen_coeff(s, t, q=2):
    """Return the Sørensen–Dice coefficient of two string arguments.

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram

    Description:
    For two sets X and Y, the Sørensen–Dice coefficient is
    S(X,Y) = 2 * |X∩Y| / (|X| + |Y|)
    This is identical to the Tanimoto similarity coefficient
    and the Tversky index for α = β = 1
    """
    return tversky_index(s, t, q, 0.5, 0.5)


def sorensen(s, t, q=2):
    """Return the Sørensen–Dice distance of two string arguments.

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram

    Description:
    Sørensen–Dice distance is 1 - the Sørensen–Dice coefficient
    """
    return 1 - sorensen_coeff(s, t, q)


def jaccard_coeff(s, t, q=2):
    """Return the Jaccard similarity coefficient of two string arguments.

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram

    Description:
    For two sets X and Y, the Jaccard similarity coefficient is
    S(X,Y) = |X∩Y| / |X∪Y|
    This is identical to the Tanimoto similarity coefficient
    and the Tversky index for α = β = 1
    """
    return tversky_index(s, t, q, 1, 1)


def jaccard(s, t, q=2):
    """Return the Jaccard distance of two string arguments.

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram

    Description:
    Jaccard distance is 1 - the Jaccard coefficient
    """
    return 1 - jaccard_coeff(s, t, q)


def tanimoto_coeff(s, t, q=2):
    """Return the Tanimoto similarity of two string arguments.

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram

    Description:
    For two sets X and Y, the Tanimoto similarity coefficient is
    S(X,Y) = |X∩Y| / |X∪Y|
    This is identical to the Jaccard similarity coefficient
    and the Tversky index for α = β = 1
    """
    return jaccard_coeff(s, t, q)


def tanimoto(s, t, q=2):
    """Return the Tanimoto distance of two string arguments:

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram

    Description:
    Tanimoto distance is -log2(Tanimoto coefficient)
    """
    return math.log(jaccard_coeff(s, t, q), 2)


def strcmp95(s, t, long_strings=False):
    """Return the strcmp95 distance between two string arguments.

    Arguments:
    s, t -- two strings to be compared
    long_strings -- set to True to "Increase the probability of a match when
        the number of matched characters is large.  This option allows for a
        little more tolerance when the strings are large.  It is not an
        appropriate test when comparing fixed length fields such as phone and
        social security numbers."

    Description:
    This is a Python translation of the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    The above file is a US Government publication and, accordingly,
    in the public domain.

    This is based on the Jaro-Winkler distance, but also attempts to correct
    for some common typos and frequently confused characters. It is also
    limited to uppercase ASCII characters, so it is appropriate to American
    names, but not much else.
    """
    def _INRANGE(c):
        return ord(c)>0 and ord(c)<91

    ying = s.strip().upper()
    yang = t.strip().upper()

    """
    If either string is blank - return - added in Version 2
    """
    if len(ying) == 0 or len(yang) == 0:
        return 0.0

    adjwt = defaultdict(int)
    sp = (
        ('A','E'), ('A','I'), ('A','O'), ('A','U'), ('B','V'), ('E','I'),
        ('E','O'), ('E','U'), ('I','O'), ('I','U'), ('O','U'), ('I','Y'),
        ('E','Y'), ('C','G'), ('E','F'), ('W','U'), ('W','V'), ('X','K'),
        ('S','Z'), ('X','S'), ('Q','C'), ('U','V'), ('M','N'), ('L','I'),
        ('Q','O'), ('P','R'), ('I','J'), ('2','Z'), ('5','S'), ('8','B'),
        ('1','I'), ('1','L'), ('0','O'), ('0','Q'), ('C','K'), ('G','J')
    )

    """
    Initialize the adjwt array on the first call to the function only.
    The adjwt array is used to give partial credit for characters that
    may be errors due to known phonetic or character recognition errors.
    A typical example is to match the letter "O" with the number "0"
    """
    for i in sp:
        x,y = i
        adjwt[(x,y)]=3
        adjwt[(y,x)]=3

    if len(ying) > len(yang):
        search_range = len(ying)
        minv = len(yang)
    else:
        search_range = len(yang)
        minv = len(ying)

    """
    Blank out the flags
    """
    ying_flag = [0 for i in xrange(search_range)]
    yang_flag = [0 for j in xrange(search_range)]
    search_range = search_range//2 - 1
    if search_range < 0:
        search_range = 0

    """
    Looking only within the search range, count and flag the matched pairs.
    """
    Num_com = 0
    yl1 = len(yang) - 1
    for i in xrange(len(ying)):
        lowlim = (i - search_range) if (i >= search_range) else 0
        hilim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in xrange(lowlim, hilim+1):
            if (yang_flag[j] == 0) and (yang[j] == ying[i]):
                yang_flag[j] = 1
                ying_flag[i] = 1
                Num_com += 1
                break

    """
    If no characters in common - return
    """
    if Num_com == 0:
        return 0.0

    """
    Count the number of transpositions
    """
    k = N_trans = 0
    for i in xrange(len(ying)):
        if ying_flag[i] != 0:
            for j in xrange(k, len(yang)):
                if yang_flag[j] != 0:
                    k = j + 1
                    break
            if ying[i] != yang[j]:
                N_trans += 1
    N_trans = N_trans // 2

    """
    Adjust for similarities in nonmatched characters
    """
    N_simi = 0
    if (minv > Num_com):
        for i in xrange(len(ying)):
            if ying_flag[i] == 0 and _INRANGE(ying[i]):
                for j in xrange(len(yang)):
                    if yang_flag[j] == 0 and _INRANGE(yang[j]):
                        if (ying[i],yang[j]) in adjwt:
                            N_simi += adjwt[(ying[i],yang[j])]
                            yang_flag[j] = 2
                            break
    Num_sim = N_simi/10.0 + Num_com

    """
    Main weight computation.
    """
    weight = Num_sim / len(ying) + Num_sim / len(yang) + (Num_com - N_trans) / Num_com
    weight = weight / 3.0

    """
    Continue to boost the weight if the strings are similar
    """
    if (weight > 0.7):

        """
        Adjust for having up to the first 4 characters in common
        """
        j = 4 if (minv >= 4) else minv
        i = 0
        while ((i<j) and (ying[i]==yang[i]) and (not ying[i].isdigit())):
            i += 1
        if i:
            weight += i * 0.1 * (1.0 - weight)

        """
        Optionally adjust for long strings.
        """
        """
        After agreeing beginning chars, at least two more must agree and
        the agreeing characters must be > .5 of remaining characters.
        """
        if ((long_strings) and (minv>4) and (Num_com>i+1) and (2*Num_com>=minv+i)):
            if (not ying[0].isdigit()):
                weight += (1.0-weight) * ((Num_com-i-1) / (len(ying)+len(yang)-i*2+2))

    return weight


def jaro_winkler(s, t, q=1, mode='winkler', long_strings=False, boost_threshold=0.7, scaling_factor=0.1):
    """Return the Jaro(-Winkler) distance between two string arguments.

    Arguments:
    s, t -- two strings to be compared
    q -- the length of each q-gram (defaults to 1: character-wise matching) 
    mode -- indicates which variant of this distance metric to compute:
        'winkler' -- computes the Jaro-Winkler distance (default)
            which increases the score for matches near the start of the word
        'jaro' -- computes the Jaro distance

    The following arguments apply only when mode is 'winkler':
    long_strings -- set to True to "Increase the probability of a match when
        the number of matched characters is large.  This option allows for a
        little more tolerance when the strings are large.  It is not an
        appropriate test when comparing fixed length fields such as phone and
        social security numbers."
    boost_threshold -- a value between 0 and 1, below which the Winkler boost
        is not applied (defaults to 0.7)
    scaling_factor -- a value between 0 and 0.25, indicating by how much to
        boost scores for matching prefixes (defaults to 0.1)

    Description:
    This is a Python based on the C code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    The above file is a US Government publication and, accordingly,
    in the public domain.
    """
    if mode == 'winkler':
        if boost_threshold > 1 or boost_threshold<0:
            raise ValueError('Unsupported boost_threshold assignment; boost_threshold must be between 0 and 1.')
        if scaling_factor > 0.25 or boost_threshold<0:
            raise ValueError('Unsupported scaling_factor assignment; scaling_factor must be between 0 and 0.25.')

    s = qgrams(s.strip(), q)
    t = qgrams(t.strip(), q)

    lens = len(s)
    lent = len(t)

    """
    If either string is blank - return - added in Version 2
    """
    if lens == 0 or lent == 0:
        return 0.0

    if lens > lent:
        search_range = lens
        minv = lent
    else:
        search_range = lent
        minv = lens

    """
    Zero out the flags
    """
    s_flag = [0 for i in xrange(search_range)]
    t_flag = [0 for j in xrange(search_range)]
    search_range = search_range//2 - 1
    if search_range < 0:
        search_range = 0

    """
    Looking only within the search range, count and flag the matched pairs.
    """
    Num_com = 0
    yl1 = lent - 1
    for i in xrange(lens):
        lowlim = (i - search_range) if (i >= search_range) else 0
        hilim = (i + search_range) if ((i + search_range) <= yl1) else yl1
        for j in xrange(lowlim, hilim+1):
            if (t_flag[j] == 0) and (t[j] == s[i]):
                t_flag[j] = 1
                s_flag[i] = 1
                Num_com += 1
                break

    """
    If no characters in common - return
    """
    if Num_com == 0:
        return 0.0

    """
    Count the number of transpositions
    """
    k = N_trans = 0
    for i in xrange(lens):
        if s_flag[i] != 0:
            for j in xrange(k, lent):
                if t_flag[j] != 0:
                    k = j + 1
                    break
            if s[i] != t[j]:
                N_trans += 1
    N_trans = N_trans // 2

    """
    Main weight computation for Jaro distance
    """
    weight = Num_com / lens + Num_com / lent + (Num_com - N_trans) / Num_com
    weight = weight / 3.0

    """
    Continue to boost the weight if the strings are similar
    This is the Winkler portion of Jaro-Winkler distance
    """
    if (mode == 'winkler' and weight > boost_threshold):

        """
        Adjust for having up to the first 4 characters in common
        """
        j = 4 if (minv >= 4) else minv
        i = 0
        while ((i<j) and (s[i]==t[i])):
            i += 1
        if i:
            weight += i * scaling_factor * (1.0 - weight)

        """
        Optionally adjust for long strings.
        """
        """
        After agreeing beginning chars, at least two more must agree and
        the agreeing characters must be > .5 of remaining characters.
        """
        if ((long_strings) and (minv>4) and (Num_com>i+1) and (2*Num_com>=minv+i)):
            weight += (1.0-weight) * ((Num_com-i-1) / (lens+lent-i*2+2))

    return weight
