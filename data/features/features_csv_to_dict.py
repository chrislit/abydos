#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""features_csv_to_dict.py

This script converts a CSV document of feature values to a Python dict.

The CSV document is of the format
<phonetic symbol(s)>,<variant number>,<segmental>,<feature>+

    Phonetic symbols are IPA (or other system) symbols.
    Variant number refers to one of the following codes:
         0 = IPA
         1 = Americanist
         2 = IPA variant
         3 = Americanist variant
         9 = other
    Segmental must be either 1 (segmental) or 0 (featural). Featural symbols
    replace features on the preceding segmental symbol.
    Features may be 1 (+), -1 (-), or 0 (0) to indicate feature values.

Lines beginning with # are interpreted as comments


Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

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

from __future__ import unicode_literals
import sys, getopt, codecs
import unicodedata

def main(argv):
    """Main conversion script
    """
    first_col = 3
    last_col = -1

    def print_usage():
        """Print usage statement
        """
        print 'features_csv_to_dict.py -i <inputfile> -o <outputfile>'
        sys.exit(2)


    def binarize(num):
        """Replace 0, -1, 1, 2 with 00, 10, 01, 11
        """
        if num == '0':      # 0
            return '00'
        elif num == '-1':   # -
            return '10'
        elif num == '1':    # +
            return '01'
        elif num == '2':    # ± (segmental) or copy from base (non-segmental)
            return '11'


    def init_termdict():
        """Initialize the terms dict
        """
        ifile = codecs.open('features_terms.csv', 'r', 'utf-8')
        termdict = dict()
        keyline = ifile.readline().strip().split(',')[first_col:last_col]
        for line in ifile:
            line = line.strip().rstrip(',')
            if '#' in line:
                line = line[:line.find('#')].strip()
            if line:
                line = line.split(',')
                term = line[last_col]
                #print line[first_col:last_col]
                features = ''.join([binarize(val) for val
                                    in line[first_col:last_col]])
                termdict[term] = int(features, 2)

        return termdict


    def check_terms(sym, features, name, termdict):
        """Check each term of the phone name to confirm that it matches
        the expected features implied by that feature
        """
        if '#' in name:
            name = name[:name.find('#')].strip()
        for term in name.split():
            if term in termdict:
                if termdict[term] & features != termdict[term]:
                    # print termdict[term], features & termdict[term]
                    print('Feature mismatch for term "' + term +
                          '" in   ' + sym)
            else:
                print 'Unknown term "' + term + '" in ' + name + ' : ' + sym


    def check_entailments(sym, features, name, entailments):
        """Check for necessary feature assignments (entailments)
        For example, [+round] necessitates [+labial]
        """
        pass


    checkdict = dict() # a mapping of symbol to feature
    checkset_s = set() # a set of the symbols seen
    checkset_f = set() # a set of the feature values seen

    termdict = init_termdict()

    ifile = ''
    ofile = ''
    try:
        opts = getopt.getopt(argv, "hi:o:", ["ifile=","ofile="])[0]
    except getopt.GetoptError:
        print_usage()
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
        elif opt in ("-i", "--ifile"):
            ifile = codecs.open(arg, 'r', 'utf-8')
        elif opt in ("-o", "--ofile"):
            ofile = codecs.open(arg, 'w', 'utf-8')
    if not ifile:
        print_usage()

    oline = 'PHONETIC_FEATURES = {'
    if not ofile:
        print(oline)
    else:
        ofile.write(oline+'\n')

    keyline = ifile.readline().strip().split(',')[first_col:last_col]
    for line in ifile:
        line = line.strip().rstrip(',')

        if line.startswith('####'):
            break

        line = unicodedata.normalize('NFC', line)

        oline = ''
        if not line or line.startswith('#'):
            oline = '                     '+line

        else:
            line = line.strip().split(',')
            if '#' in line:
                line = line[:line.find('#')]
            symbol = unicode(line[0])
            variant = int(line[1])
            segmental = bool(line[2])
            features = '0b' + ''.join([binarize(val) for val
                                       in line[first_col:last_col]])
            name = line[-1].strip()
            if not segmental:
                features = '-' + features

            featint = int(features, 2)
            check_terms(symbol, featint, name, termdict)
            if symbol in checkset_s:
                print 'Symbol ' + symbol + ' appears twice in CSV.'
            else:
                checkset_s.add(symbol)

            if variant == 0:
                if featint in checkset_f:
                    print ('Feature set ' + unicode(featint) +
                           ' appears in CSV for two primary IPA symbols: ' +
                           symbol + ' and ' + unicode(checkdict[featint]))
                else:
                    checkdict[featint] = symbol
                    checkset_f.add(featint)

            if variant in set([0, 2, 5]):
                oline = '                     \'{}\': {},'.format(symbol,
                                                                  features)
            else:
                oline = ''

        if oline:
            if not ofile:
                print(oline)
            else:
                ofile.write(oline+'\n')

    oline = '                    }'
    if not ofile:
        print(oline)
    else:
        ofile.write(oline+'\n')

    oline = '\nFEATURE_MASK = {'
    if not ofile:
        print(oline)
    else:
        ofile.write(oline+'\n')

    mag = len(keyline)
    for i in range(len(keyline)):
        features = '0b' + ('00' * i) + '11' + ('00' * (mag - i - 1))
        oline = '                \'{}\': {},'.format(keyline[i], features)
        if not ofile:
            print(oline)
        else:
            ofile.write(oline+'\n')

    oline = '               }'
    if not ofile:
        print(oline)
    else:
        ofile.write(oline+'\n')


if __name__ == "__main__":
    main(sys.argv[1:])
