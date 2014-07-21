#!/usr/bin/env python

from os import listdir
from os.path import isfile
import codecs
import re
import sys

def pythonize(line):
    line = line.strip()
    line = re.sub('\s*', '', line)
    line = line.replace('//', '#')
    line = re.sub('"(.*?)"', r"'\1'", line)
    line = line.replace('array', '')
    return '             '+line+'\n'

bmdir = sys.argv[1]

subdirs = ('gen', 'sep', 'ash')

for s in subdirs:
    phps = [f for f in listdir(bmdir+s+'/') if (isfile(bmdir+s+'/'+f) and f.endswith('.php'))]
    for infilename in phps:
            for pfx in ('rules', 'approx', 'exact', 'hebrew'):
                if infilename.startswith(pfx):
                    infile = codecs.open(bmdir+s+'/'+infilename, 'r', 'utf-8')
                    outfilename = pfx + '_' + infilename[len(pfx):-3]
                    outfilename = '../abydos/bm/' + s + '_' +outfilename + 'py'
                    outfile = codecs.open(outfilename, 'w', 'utf-8')
                    print outfilename

                    ignore = True
                    for line in infile:
                        if not ignore:
                            if re.search(r'\);', line):
                                ignore = True
                            else:
                                line = pythonize(line)
                                outfile.write(line)
                        if re.search('\$.+ = array\(', line):
                            ignore = False
