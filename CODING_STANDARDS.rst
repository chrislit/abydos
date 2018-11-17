CODING STANDARDS
----------------

- nosetest will be used for testing
- flake8 will be used for best practice conformance
- pydocstyle will be used to ensure documentation style conformance to PEP257
  (for the most part) and NumPy documentation style
- black will be used to keep code style consistent

----

git commits
~~~~~~~~~~~

Each commit should be a minimal unit of code or represent minimal changes.
Avoid doing multiple things in a single commit, but describe them in separate
lines of the commit log if this does occur.


git pushes
~~~~~~~~~~

A git push should be performed only under the following conditions:

- library is syntactically correct (compiling correctly) in both Python 2 & 3
- library passes all tests and doctests according to nosetests in both Python 2
  & 3
- test coverage is 100% according to nosetests
- flake8 and pydocstyle should report 0 issues
- black code styling has been applied
