#!/usr/bin/env python3
# Copyright 2014-2020 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.


"""bm_php2py.py.

This helper script converts Beider-Morse Phonetic Matching Algorithm (BMPM)
code from PHP to Python.

It assumes that the BMPM code is located at ../../bmpm (relative to this
directory in the abydos repository).

It reads the BMPM reference implementation and generates the file
../abydos/_beider_morse_data.py.

The file _beider_morse.py may still need manual changes to be made after this
script is run.
"""

import codecs
import re
import sys
from os import listdir
from os.path import isfile

# noinspection PyPackageRequirements
import chardet

# The list of languages from BMPM to support (might need to be updated or
# tuned as BMPM is updated)
lang_tuple = (
    'any',
    'arabic',
    'cyrillic',
    'czech',
    'dutch',
    'english',
    'french',
    'german',
    'greek',
    'greeklatin',
    'hebrew',
    'hungarian',
    'italian',
    'latvian',
    'polish',
    'portuguese',
    'romanian',
    'russian',
    'spanish',
    'turkish',
)

lang_dict = {}
for i, l in enumerate(lang_tuple):
    lang_dict[l] = 2 ** i
lang_dict['common'] = "'common'"

nl = False
array_seen = False

tail_text = ''
sd = ''


def c2u(name):
    """Convert camelCase (used in PHP) to Python-standard snake_case.

    Src:
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case

    Parameters
    ----------
    name: A function or variable name in camelCase

    Returns
    -------
    str: The name in snake_case

    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return s1


def pythonize(line, fn='', subdir='gen'):
    """Convert a line of BMPM code from PHP to Python.

    Parameters
    ----------
    line : str
        A line of code
        fn : str
        A filename
        subdir : str
        The file's subdirectory

    Returns
    -------
    The code in Python

    """
    global array_seen, nl, sd

    if '$all' in line:
        return ''
    if 'make the sum of all languages be visible in the function' in line:
        return ''

    line = line.strip()

    if 'array' in line and not line.startswith('//'):
        array_seen = True

    line = re.sub('//+', '#', line)
    # line = re.sub('"\.\((\$.+?)\)\."', r'\1', line)
    if line and re.search(r'array\("[^"]+?"\)', line):
        # print("### " + line)
        line = ''
    line = line.replace('array', '')
    line = re.sub(r'^\s*', '', line)
    line = re.sub(';$', '', line)
    line = re.sub('^include_.+', '', line)

    line = re.sub(
        r'\$(approx|rules|exact)\[LanguageIndex\("([^"]+)", '
        + r'\$languages\)\] = \$([a-zA-Z]+)',
        lambda m: (
            "BMDATA['"
            + subdir
            + "']['"
            + m.group(1)
            + "'][L_"
            + m.group(2).upper()
            + '] = _'
            + subdir.upper()
            + '_'
            + c2u(m.group(3)).upper()
        ),
        line,
    )

    line = re.sub(
        r'\$(approx|rules|exact|hebrew)([A-Za-z]+) = _merge'
        + r'\(\$([a-zA-Z]+), \$([a-zA-Z]+)\)',
        lambda m: (
            "BMDATA['"
            + subdir
            + "']['"
            + m.group(1)
            + "'][L_"
            + c2u(m.group(2)).upper()
            + '] = _'
            + subdir.upper()
            + '_'
            + c2u(m.group(3)).upper()
            + ' + _'
            + subdir.upper()
            + '_'
            + c2u(m.group(4)).upper()
        ),
        line,
    )

    line = re.sub(
        r'\$(approx|rules|exact)\[LanguageIndex\("([^"]+)", '
        + r'\$languages\)\] = _merge\(\$([a-zA-Z]+), \$([a-zA-Z]+)\)',
        lambda m: (
            "BMDATA['"
            + subdir
            + "']['"
            + m.group(1)
            + "'][L_"
            + c2u(m.group(2)).upper()
            + '] = _'
            + subdir.upper()
            + '_'
            + c2u(m.group(3)).upper()
            + ' + _'
            + subdir.upper()
            + '_'
            + c2u(m.group(4)).upper()
        ),
        line,
    )

    line = re.sub(
        r'^\$([a-zA-Z]+)',
        lambda m: '_' + sd.upper() + '_' + c2u(m.group(1)).upper(),
        line,
    )

    for _ in range(len(lang_tuple)):
        line = re.sub(r'($[a-zA-Z]+) *\+ *($[a-zA-Z]+)', r'\1\+\2', line)

    line = re.sub(
        r'\$([a-zA-Z]+)',
        lambda m: (
            'L_' + m.group(1).upper()
            if m.group(1) in lang_dict
            else '$' + m.group(1)
        ),
        line,
    )
    line = re.sub(r'\[\"\.\((L_[A-Z_+]+)\)\.\"\]', r'[\1]', line)

    line = re.sub(
        'L_([A-Z]+)', lambda m: str(lang_dict[m.group(1).lower()]), line
    )
    for _ in range(4):
        line = re.sub(
            r'([0-9]+) *\+ *([0-9]+)',
            lambda m: str(int(m.group(1)) + int(m.group(2))),
            line,
        )

    if fn == 'lang':
        if len(line.split(',')) >= 3:
            parts = line.split(',')
            parts[0] = re.sub('/(.+?)/', r'\1', parts[0])
            # parts[1] = re.sub('\$', 'L_', parts[1])
            # parts[1] = re.sub(' *\+ *', '|', parts[1])
            parts[2] = parts[2].title()
            line = ','.join(parts)

    if 'languagenames' in fn:
        line = line.replace('"', "'")
        line = line.replace("','", "', '")
        if line and line[0] == "'":
            line = ' ' * 14 + line

    # fix upstream
    # line = line.replace('ë', 'ü')

    comment = ''
    if '#' in line:
        hashsign = line.find('#')
        comment = line[hashsign:]
        code = line[:hashsign]
    else:
        code = line

    code = code.rstrip()
    comment = comment.strip()
    if not re.match(r'^\s*$', code):
        comment = '  ' + comment

    if '(' in code and ')' in code:
        prefix = code[: code.find('(') + 1]
        suffix = code[code.rfind(')') :]
        tuplecontent = code[len(prefix) : len(code) - len(suffix)]

        elts = tuplecontent.split(',')
        for i in range(len(elts)):
            elts[i] = elts[i].strip()
            if elts[i][0] == '"' and elts[i][-1] == '"':
                elts[i] = "'" + elts[i][1:-1].replace("'", "\\'") + "'"
        tuplecontent = ', '.join(elts)

        code = prefix + tuplecontent + suffix

    line = code + comment
    line = re.sub('# *', '# ', line)

    if line:
        nl = False
        if array_seen and not (line[0] == '_' or line.startswith('BMDATA')):
            line = ' ' * 4 + line
        return line + '\n'
    elif not nl:
        nl = True
        return '\n'
    else:
        return ''


def _run_script():
    global array_seen, nl, sd, tail_text

    if len(sys.argv) > 1:
        bmdir = sys.argv[1].rstrip('/') + '/'
    else:
        bmdir = '../../bmpm/'

    outfilename = '../abydos/phonetic/_beider_morse_data.py'
    outfile = codecs.open(outfilename, 'w', 'utf-8')

    outfile.write(
        '# Copyright 2014-2020 by \
Christopher C. Little.\n# This file is part of Abydos.\n#\n# This file is \
based on Alexander Beider and Stephen P. Morse\'s implementation\n# of the \
Beider-Morse Phonetic Matching (BMPM) System, available at\n# \
http://stevemorse.org/phonetics/bmpm.htm.\n#\n# Abydos is free software: \
you can redistribute it and/or modify\n# it under the terms of the GNU \
General Public License as published by\n# the Free Software Foundation, \
either version 3 of the License, or\n# (at your option) any later version.\n\
#\n# Abydos is distributed in the hope that it will be useful,\n# but WITHOUT \
ANY WARRANTY; without even the implied warranty of\n# MERCHANTABILITY or \
FITNESS FOR A PARTICULAR PURPOSE. See the\n# GNU General Public License for \
more details.\n#\n# You should have received a copy of the GNU General Public \
License\n# along with Abydos. If not, see <http://www.gnu.org/licenses/>.\n\n\
"""abydos.phonetic._beider_morse_data.\n\nBehind-the-scenes constants, \
rules, etc. for the Beider-Morse Phonentic\nMatching (BMPM) algorithm\n\nDO \
NOT EDIT - This document is automatically generated from the reference\n\
implementation in PHP.\n"""\n\nfrom \
__future__ import (\n    absolute_import,\n    division,\n    print_function,\
    unicode_literals,\n)\n'
    )

    outfile.write('L_NONE = 0\n')
    for i, l in enumerate(lang_tuple):
        outfile.write('L_' + l.upper() + ' = 2**' + str(i) + '\n')
    outfile.write('\n\n')

    tail_text += '\nBMDATA = {}\n'

    subdirs = ('gen', 'sep', 'ash')

    for s in subdirs:
        sd = s
        tail_text += "\nBMDATA['" + s + "'] = {}\n"
        tail_text += "BMDATA['" + s + "']['approx'] = {}\n"
        tail_text += "BMDATA['" + s + "']['exact'] = {}\n"
        tail_text += "BMDATA['" + s + "']['rules'] = {}\n"
        tail_text += "BMDATA['" + s + "']['hebrew'] = {}\n\n"
        tail_text += (
            "BMDATA['"
            + s
            + "']['language_rules'] = _"
            + s.upper()
            + '_LANGUAGE_RULES\n'
        )
        tail_text += (
            "BMDATA['" + s + "']['languages'] = _" + s.upper() + '_LANGUAGES\n'
        )

        phps = [
            f
            for f in sorted(listdir(bmdir + s + '/'))
            if (isfile(bmdir + s + '/' + f) and f.endswith('.php'))
        ]
        for infilename in phps:
            for pfx in (
                'rules',
                'approx',
                'exact',
                'hebrew',
                'language',
                'lang',
            ):
                if infilename.startswith(pfx):
                    array_seen = False
                    infilepath = bmdir + s + '/' + infilename
                    infileenc = chardet.detect(open(infilepath, 'rb').read())[
                        'encoding'
                    ]
                    print(s + '/' + infilename)  # noqa: T001
                    infile = codecs.open(infilepath, 'r', infileenc)
                    # if infilename.startswith('lang'):
                    #     tuplename = infilename[:-4]
                    # else:
                    #     tuplename = pfx + '_' + infilename[len(pfx) : -4]
                    # indent = len(tuplename) + 21

                    outfile.write('# ' + s + '/' + infilename + '\n')

                    ignore = True
                    for line in infile:
                        if 'function Language' in line:
                            break
                        if not ignore:
                            if re.search(r'\?>', line):
                                ignore = True
                            else:
                                line = pythonize(line, infilename[:-4], s)
                                if line.startswith('BMDATA'):
                                    tail_text += line
                                else:
                                    outfile.write(line)
                        if '*/' in line:
                            ignore = False

                    outfile.write('\n\n')
                    break

    outfile.write(tail_text)

    outfile.close()
    outfilelines = codecs.open(outfilename, 'r', 'utf-8').readlines()
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    nl = False
    fixlanguagesarray = False

    sep_lang = (
        "('any', 'french', 'hebrew', 'italian', 'portuguese', 'spanish')"
    )

    for line in outfilelines:
        line = line.rstrip()
        if line:
            if fixlanguagesarray:
                line = ' ' + line.strip()
                fixlanguagesarray = False
            if len(line) > 79 or sep_lang in line:
                line += '  # noqa: E501'
            outfile.write(line)
            if not line.endswith('='):
                outfile.write('\n')
            else:
                fixlanguagesarray = True
            nl = False
        else:
            if not nl:
                outfile.write('\n')
            nl = True

    outfile.write(
        "\n\nif __name__ == '__main__':\n    import doctest\n\n\
    doctest.testmod()\n"
    )


if __name__ == '__main__':
    _run_script()
