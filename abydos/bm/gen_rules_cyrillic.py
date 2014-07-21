# -*- coding: utf-8 -*-
"""abydos.distance

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

This file is derived from PHP code by Alexander Beider and Stephen P. Morse that
is part of the Beider-Morse Phonetic Matching (BMPM) System, available at
http://stevemorse.org/phonetics/bmpm.htm.

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
             ('ця','','','tsa'),
             ('цю','','','tsu'),
             ('циа','','','tsa'),
             ('цие','','','tse'),
             ('цио','','','tso'),
             ('циу','','','tsu'),
             ('сие','','','se'),
             ('сио','','','so'),
             ('зие','','','ze'),
             ('зио','','','zo'),
             ('с','','с',''),
             
             ('гауз','','$','haus'),
             ('гаус','','$','haus'),
             ('гольц','','$','holts'),
             ('геймер','','$','(hejmer|hajmer)'),
             ('гейм','','$','(hejm|hajm)'),
             ('гоф','','$','hof'),
             ('гер','','$','ger'),
             ('ген','','$','gen'),
             ('гин','','$','gin'),
             ('г','(й|ё|я|ю|ы|а|е|о|и|у)','(а|е|о|и|у)','g'),
             ('г','','(а|е|о|и|у)','(g|h)'),
             
             ('ля','','','la'),
             ('лю','','','lu'),
             ('лё','','','(le|lo)'),
             ('лио','','','(le|lo)'),
             ('ле','','','(lE|lo)'),
             
             ('ийе','','','je'),
             ('ие','','','je'),
             ('ыйе','','','je'),
             ('ые','','','je'),
             ('ий','','(а|о|у)','j'),
             ('ый','','(а|о|у)','j'),
             ('ий','','$','i'),
             ('ый','','$','i'),
             
             ('ей','^','','(jej|ej)'),
             ('е','(а|е|о|у)','','je'),
             ('е','^','','je'),
             ('эй','','','ej'),
             ('ей','','','ej'),
             
             ('ауе','','','aue'),
             ('ауэ','','','aue'),
             
             ('а','','','a'),
             ('б','','','b'),
             ('в','','','v'),
             ('г','','','g'),
             ('д','','','d'),
             ('е','','','E'),
             ('ё','','','(e|jo)'),
             ('ж','','','Z'),
             ('з','','','z'),
             ('и','','','I'),
             ('й','','','j'),
             ('к','','','k'),
             ('л','','','l'),
             ('м','','','m'),
             ('н','','','n'),
             ('о','','','o'),
             ('п','','','p'),
             ('р','','','r'),
             ('с','','','s'),
             ('т','','','t'),
             ('у','','','u'),
             ('ф','','','f'),
             ('х','','','x'),
             ('ц','','','ts'),
             ('ч','','','tS'),
             ('ш','','','S'),
             ('щ','','','StS'),
             ('ъ','','',''),
             ('ы','','','I'),
             ('ь','','',''),
             ('э','','','E'),
             ('ю','','','ju'),
             ('я','','','ja'),
             
             ('rulescyrillic')
             
