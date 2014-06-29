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

    first_col = 3
    last_col = -1

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
            symbol = line[0]
            variant = int(line[1])
            segmental = bool(line[2])
            features = '0b' + ''.join([binarize(val) for val
                                       in line[first_col:last_col]])
            if not segmental:
                features = '-' + features

            if variant == 0 or variant == 2:
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
