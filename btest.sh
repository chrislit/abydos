#!/bin/sh

quick_mode=0
clean=0
docs_only=0

while [ "$1" != "" ]; do
    case $1 in
        -q | --quick | -qc) quick_mode=1
    esac
    case $1 in
	-c | --clean | -qc) clean=1
    esac
    case $1 in
	-d | --docs) docs_only=1
    esac
    shift
done

if [ "$clean" = "1" ]; then
    ./cleanup.sh
fi

if [ "docs_only" = "0" ]; then
    python setup.py build

    python setup.py sdist
    python setup.py bdist_wheel

    python setup.py install

    if [ "$quick_mode" = "0" ]; then
	nosetests .

	pylint --rcfile=pylint.rc abydos > pylint.log
	pycodestyle -v --statistics --exclude=.git,__pycache__,build,dist,docs . > pycodestyle.log
	flake8 . > flake8.log

	./badge_update.py
    fi
fi

sphinx-apidoc -e -f -M -o docs ./abydos
cd docs
make html epub xelatexpdf >> /dev/null
