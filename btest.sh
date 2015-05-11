#!/bin/sh

./cleanup.sh

python setup.py build
python3 setup.py build

sudo python3 setup.py sdist
sudo python3 setup.py bdist_wheel

sudo python setup.py install
sudo python3 setup.py install

nosetests -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=abydos .
nosetests3 -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=abydos .

pylint --rcfile=pylint.rc abydos > pylint.log
pep8 -v --statistics > pep8.log

./badge_update.py
