#!/bin/sh

rm -rf ./cover
rm -rf ./flake8
rm -rf ./abydos.egg-info
rm -rf ./dist
rm -rf ./build
rm -rf ./.tox
rm -rf ./.mypy_cache
rm -rf ./.coverage

rm -rf ./docs/_build/*
rm -rf ./docs/abydos.bib.bak

find . -type f -name '*~' -delete
find . -type f -name '.*~' -delete
find . -type f -name '*.pyc' -delete
find . -type f -name '*.log' -delete
find . -type f -name '*.sav' -delete
find . -type f -name '*.bak' -delete
find . -type d -name '__pycache__' -delete
