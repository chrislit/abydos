CODING STANDARDS
----------------

- Nosetest will be used for testing.
- Flake8 will be used for best practice conformance.
- Pydocstyle will be used to ensure documentation style conformance to PEP257
  (for the most part) and NumPy documentation style.
- Black will be used to keep code style consistent.
- 3rd party packages may be used, but must be present in both PyPI and conda
  or conda-forge. They must also support all supported Python versions.

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


Notes on architecture
~~~~~~~~~~~~~~~~~~~~~

As of the 0.3.6 release, each major algorithm of the compression, distance,
fingerprint, phonetic, & stemmer subpackages has been moved into a class of its
own. The distance, fingerprint, phonetic, & stemmer classes each inherit from
respectively common classes that define basic methods for these four major
types of classes.

The old functional API for these subpackages has been retained for backwards
compatibility until the release of version 0.6, but its use is deprecated as
of version 0.4. New classes (those not present at the release of version 0.3.6)
will not be given functional API wrappers.

Although, as of the 0.3.6 release, many of the classes that have are pre-0.3.6
functions encapsulated in a class simply consist of a single method that
could be a static method, making these methods static is generally avoided.
As development continues, these classes will take more advantage of object
architecture to store parameters between calls and inherit from base classes.
