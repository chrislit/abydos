#!/bin/sh

quick_mode=0
while [ "$1" != "" ]; do
    case $1 in
        -q | --quick ) quick_mode=1
    esac
    shift
done

./cleanup.sh

python setup.py build
python3 setup.py build

sudo python3 setup.py sdist
sudo python3 setup.py bdist_wheel

sudo python setup.py install
sudo python3 setup.py install

if [ "$quick_mode" = "0" ]; then
    nosetests -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=abydos .
    nosetests3 -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=abydos .

    pylint --rcfile=pylint.rc abydos > pylint.log
    pep8 -v --statistics --exclude=.git,__pycache__,build,_bmdata.py,docs . > pep8.log

    ./badge_update.py
fi

sphinx-apidoc -F -o docs abydos
cd docs
make html epub latexpdf >> /dev/null
