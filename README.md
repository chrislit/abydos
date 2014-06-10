abydos
======

Abydos NLP library by Christopher C. Little

This library contains code I'm using for research, in particular dissertation research & experimentation.



To build/install/unittest in Python 2:
sudo python setup.py install; nosetests -v --with-coverage --cover-package=abydos .

To build/install/unittest in Python 3:
sudo python3 setup.py install; nosetests3 -v --with-coverage --cover-package=abydos .


For pylint testing, run:
pylint --rcfile=pylint.rc abydos > pylint.log
