#!/usr/bin/env python

from os import listdir
from os.path import isfile
import codecs
import re
import sys

def pythonize(line, indent=0, fn=''):
    line = line.strip()
    line = line.replace('//', '#')
    #line = re.sub('"(.*?)"', r"'\1'", line)
    line = re.sub('"\.\((\$.+?)\)\."', r'\1', line)
    line = line.replace('array', '')
    line = line.replace('("'+fn+'")', '')
    line = re.sub('^\s*', '', line)
    if line:
        line = ' '*indent + line
    return line + '\n'

bmdir = sys.argv[1]

subdirs = ('gen', 'sep', 'ash')

for s in subdirs:
    phps = [f for f in listdir(bmdir + s + '/') if (isfile(bmdir + s + '/' + f)
                                                    and f.endswith('.php'))]
    for infilename in phps:
            for pfx in ('rules', 'approx', 'exact', 'hebrew'):
                if infilename.startswith(pfx):
                    infile = codecs.open(bmdir + s + '/' + infilename,
                                         'r', 'utf-8')
                    tuplename = pfx + '_' + infilename[len(pfx):-4]
                    indent = len(tuplename) + 9
                    outfilename = '../abydos/bm/' + s + '_' + tuplename + '.py'
                    outfile = codecs.open(outfilename, 'w', 'utf-8')
                    print infilename, outfilename

                    outfile.write('# -*- coding: utf-8 -*-\n\"\"\"abydos.distance\n\nCopyright 2014 by Christopher C. Little.\nThis file is part of Abydos.\n\nThis file is derived from PHP code by Alexander Beider and Stephen P. Morse that\nis part of the Beider-Morse Phonetic Matching (BMPM) System, available at\nhttp://stevemorse.org/phonetics/bmpm.htm.\n\nAbydos is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nAbydos is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with Abydos. If not, see <http://www.gnu.org/licenses/>.\n\"\"\"\n\n')
                    outfile.write('_' + s + '_' + tuplename + ' = (\n')

                    ignore = True
                    for line in infile:
                        if not ignore:
                            if re.search(r'\);', line):
                                ignore = True
                            else:
                                line = pythonize(line, indent, infilename[:-4])
                                outfile.write(line)
                        if re.search('\$.+ = array\(', line):
                            ignore = False

                    outfile.write(indent*' ' + ')\n')
