# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
import numpy
import sys
import math
from .util import _qgram_counts


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
        raise ValueError('Unsupported weight assignment; but alpha and beta must be greater than or equal to 0.')

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
        return c / (beta * (alpha * a + (1 - alpha) * beta) + c)


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

def jaro(s, t, mode='jaro'):
    """Return the Jaro distance between two string arguments.

    Arguments:
    s, t -- two strings to be compared
    mode -- specifies which algorithm to employ:
              'jaro' -- the basic Jaro algorithm
              'winkler' -- the Jaro-Winkler algorithm
              'strcmp95' -- the algorithm as implemented in strcmp95.c

    Description:
    This is a Python translation of the c code for strcmp95:
    http://web.archive.org/web/20110629121242/http://www.census.gov/geo/msb/stand/strcmp.c
    The above file is a US Goverment publication and, accordingly,
    in the public domain.
    """
    def _NOTNUM(c):
        return c.isdigit()
    def _INRANGE(c):
        return ord(c)>0 and ord(c)<91

    ying = s
    yang = t

    lenDiff = len(s) - len(t)
    if lenDiff:
        if lenDiff > 0:
            yang += ' '*lenDiff
        else:
            ying += ' '*lenDiff

    y_length = len(ying)

    first_pass = True
    adjwt = numpy.zeros((91,91), dtype=numpy.int)
    sp = (
        ('A','E'), ('A','I'), ('A','O'), ('A','U'), ('B','V'), ('E','I'),
        ('E','O'), ('E','U'), ('I','O'), ('I','U'), ('O','U'), ('I','Y'),
        ('E','Y'), ('C','G'), ('E','F'), ('W','U'), ('W','V'), ('X','K'),
        ('S','Z'), ('X','S'), ('Q','C'), ('U','V'), ('M','N'), ('L','I'),
        ('Q','O'), ('P','R'), ('I','J'), ('2','Z'), ('5','S'), ('8','B'),
        ('1','I'), ('1','L'), ('0','O'), ('0','Q'), ('C','K'), ('G','J')
    )

    ying_hold, yang_hold, ying_flag, yang_flag = '', '', '', ''
    weight = 0.0, 0.0
    minv, search_range, lowlim, ying_length = 0, 0, 0, 0
    hilim, N_trans, Num_com, yang_length = 0, 0, 0, 0
    yl1, yi_st, N_simi = 0, 0, 0

    """
    Initialize the adjwt array on the first call to the function only.
    The adjwt array is used to give partial credit for characters that
    may be errors due to known phonetic or character recognition errors.
    A typical example is to match the letter "O" with the number "0"
    """
    if (first_pass):
        first_pass = False
        for i in xrange(36):
            adjwt[sp[i][0],sp[i][1]] = 3
            adjwt[sp[i][1],sp[i][0]] = 3

    """
    Identify the strings to be compared by stripping off all leading and
    trailing spaces.
    """
    k = y_length - 1

    for(j = 0; ((ying[j]==' ') && (j < k)); j++);
    for(i = k; ((ying[i]==' ') && (i > 0)); i--);
    ying_length = i + 1 - j;
    yi_st = j;

    for(j = 0; ((yang[j]==' ') && (j < k)); j++);
    for(i = k; ((yang[i]==' ') && (i > 0)); i--);
    yang_length = i + 1 - j;

    """ If either string is blank - return - added in Version 2                    """
    if(ying_length <= 0 || yang_length <= 0) return(0.0);

    ying_hold = (char*) malloc(sizeof(char) * (ying_length + 1));
    yang_hold = (char*) malloc(sizeof(char) * (yang_length + 1));

    strncpy(ying_hold,&ying[yi_st],ying_length);
    strncpy(yang_hold,&yang[j],yang_length);

    if (ying_length > yang_length) {
        search_range = ying_length;
        minv = yang_length;
    }
    else {
        search_range = yang_length;
        minv = ying_length;
    }

    """ If either string is blank - return                                         """
    """ if (!minv) return(0.0);                   removed in version 2             """

    """ Blank out the flags							      """
    ying_flag = (char*) malloc(sizeof(char) * search_range);
    yang_flag = (char*) malloc(sizeof(char) * search_range);

    memset(ying_flag, ' ', search_range);
    memset(yang_flag, ' ', search_range);
    search_range = (search_range/2) - 1;
    if (search_range < 0) search_range = 0;   """ added in version 2               """

    """ Convert all lower case characters to upper case.                           """
    if (!ind_c[1]) {
        for (i = 0; i < ying_length; i++) if (islower(ying_hold[i])) ying_hold[i] -= 32;
        for (j = 0; j < yang_length; j++) if (islower(yang_hold[j])) yang_hold[j] -= 32;
    }

    """ Looking only within the search range, count and flag the matched pairs.    """
    Num_com = 0;
    yl1 = yang_length - 1;
    for (i = 0; i < ying_length; i++) {
        lowlim = (i >= search_range) ? i - search_range : 0;
        hilim = ((i + search_range) <= yl1) ? (i + search_range) : yl1;
        for (j = lowlim; j <= hilim; j++)  {
            if ((yang_flag[j] != '1') && (yang_hold[j] == ying_hold[i])) {
                yang_flag[j] = '1';
                ying_flag[i] = '1';
                Num_com++;
                break;
            }
        }
    }

    """ If no characters in common - return                                        """
    if (!Num_com) {
        free(ying_hold);
        free(yang_hold);
        free(ying_flag);
        free(yang_flag);
        return(0.0);
    }

    """ Count the number of transpositions                                         """
    k = N_trans = 0;
    for (i = 0; i < ying_length; i++) {
        if (ying_flag[i] == '1') {
            for (j = k; j < yang_length; j++) {
                if (yang_flag[j] == '1') {
                    k = j + 1;
                    break;
                }
            }
            if (ying_hold[i] != yang_hold[j]) N_trans++;
        }
    }
    N_trans = N_trans / 2;

    """ adjust for similarities in nonmatched characters                           """
    N_simi = 0;
    if (minv > Num_com) {
        for (i = 0; i < ying_length; i++) {
            if (ying_flag[i] == ' ' && INRANGE(ying_hold[i])) {
                for (j = 0; j < yang_length; j++) {
                    if (yang_flag[j] == ' ' && INRANGE(yang_hold[j])) {
                        if (adjwt[ying_hold[i]][yang_hold[j]] > 0) {
                            N_simi += adjwt[ying_hold[i]][yang_hold[j]];
                            yang_flag[j] = '2';
                            break;
                        }
                    }
                }
            }
        }
    }
    Num_sim = ((double) N_simi)/10.0 + Num_com;

    """ Main weight computation.						      """
    weight= Num_sim / ((double) ying_length) + Num_sim / ((double) yang_length)
            + ((double) (Num_com - N_trans)) / ((double) Num_com);
    weight = weight / 3.0;

    """ Continue to boost the weight if the strings are similar                    """
    if (weight > 0.7) {

        """ Adjust for having up to the first 4 characters in common                 """
        j = (minv >= 4) ? 4 : minv;
        for (i=0; ((i<j)&&(ying_hold[i]==yang_hold[i])&&(NOTNUM(ying_hold[i]))); i++);
        if (i) weight += i * 0.1 * (1.0 - weight);

        """ Optionally adjust for long strings.                                      """
        """ After agreeing beginning chars, at least two more must agree and
             the agreeing characters must be > .5 of remaining characters.          """
        if ((!ind_c[0]) && (minv>4) && (Num_com>i+1) && (2*Num_com>=minv+i))
            if (NOTNUM(ying_hold[0]))
                weight += (double) (1.0-weight) *
                          ((double) (Num_com-i-1) / ((double) (ying_length+yang_length-i*2+2)));
    }

    return(weight);

    return 0
