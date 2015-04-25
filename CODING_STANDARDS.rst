CODING STANDARDS
----------------

git commits
~~~~~~~~~~~

Each commit should be a minimal unit of code or represent minimal changes.
Avoid doing multiple things in a single commit, but describe them in separate
lines of the commit log if this does occur.


git pushes
~~~~~~~~~~

A git push should be performed only under the following conditions:

- library is syntactically correct (compiling correctly) in both Python 2 & 3
- library passes all tests according to nosetests in both Python 2 & 3
- test coverage is 100% according to nosetests
- using the included pylint.rc, pylint reports a 10/10 rating
