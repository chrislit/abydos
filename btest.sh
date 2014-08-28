#!/bin/sh

sudo rm -rf ./build
python setup.py build
sudo python setup.py install

sudo rm -rf ./build
python3 setup.py build
sudo python3 setup.py install

nosetests -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=abydos .
#nosetests3 -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=abydos .

pylint --rcfile=pylint.rc abydos > pylint.log
