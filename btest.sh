#!/bin/sh

quick_mode=0
clean=0
while [ "$1" != "" ]; do
    case $1 in
        -q | --quick | -qc) quick_mode=1
    esac
    case $1 in
	-c | --clean | -qc) clean=1
    esac
    shift
done

if [ "$clean" = "1" ]; then
    ./cleanup.sh
fi

python setup.py build

python setup.py sdist
python setup.py bdist_wheel

python setup.py install

if [ "$quick_mode" = "0" ]; then
    nosetests .

    pylint --rcfile=pylint.rc abydos > pylint.log
    pycodestyle -v --statistics --exclude=.git,__pycache__,build,_bmdata.py,docs . > pycodestyle.log

    ./badge_update.py
fi

sphinx-apidoc -F -o docs abydos
cd docs
make html epub latexpdf >> /dev/null
