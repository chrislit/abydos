FAQ
===


Why is the library licensed under GPL3+? Can you change the license?
--------------------------------------------------------------------

GPL3 is the only license compatible with all of the various parts of
Abydos that have been ported to Python from other languages. For example,
the Beider-Morse Phonetic Matching algorithm implementation included in
Abydos was ported from their reference implementation in PHP, which is
itself licensed under GPL3.

Accordingly, it's not possible to change to a different license without
removing parts of the library. However, if you have a need for a specific
part of the library and can't use GPL3+ code, contact us and we may be able
to provide it separately or can give guidance on its underlying licensing
status.

What is the purpose of this library?
------------------------------------

A. Abydos is intended to facilitate any manner of string transformation and
comparison might be useful for string matching or record linkage. The two
most significant parts of the library are string distance/similarity
measures and phonetic algorithms/string fingerprint algorithms, but a large
collection of tokenizers, corpus classes, compression algorithms, &
phonetics functions support these and afford greater customization.

Can you add this new feature?
-----------------------------

Maybe. Open an issue at https://github.com/chrislit/abydos/issues and
propose your new feature.

Additional string distance/similarity measures,
phonetic algorithms, string fingerprint algorithms, and string tokenizers
will certainly be added if possible -- but it's helpful to point them
out since we may not be aware of them.

Can I contribute to the project?
--------------------------------

Absolutely. You can take on an unclaimed issue, report bugs, add new
classes, or whatever piques your interest. You are welcome to open an
issue at https://github.com/chrislit/abydos/issues proposing what you'd
like to work on, or you can submit a pull request if you have something
ready to contribute to the repository.

Will you add Metaphone 3?
-------------------------

No. Although Lawrence Philips (author of Metaphone, Double Metaphone, and
Metaphone 3) released Metaphone 3 version 2.1.3 under the BSD 3-clause
license as part of Google Refine, which became OpenRefine
(https://github.com/OpenRefine/OpenRefine/blob/master/main/src/com/google/refine/clustering/binning/Metaphone3.java),
he doesn't want that code used for ports to other languages or used in any
way outside of OpenRefine. In accordance with his wishes, no one has
released Metaphone 3 ports to other languages or included it other
libraries.

Why have you included algorithm X when it is already a part of NLTK/SciPy/...?
------------------------------------------------------------------------------

Abydos is a collection of algorithms with common class & function
interfaces and options. So, while NLTK has Levenshtein & Jaccard string
similarity measures, they don't allow for tunable edit costs or using
the tokenizer of your choice.

Are there similar projects for languages other than Python?
-----------------------------------------------------------

Yes, there are libraries such as:

    - Talisman_ for JavaScript
    - Phonics_ for R (phonetic algorithms)
    - stringmetric_ for Scala

.. _Talisman: https://github.com/Yomguithereal/talisman
.. _Phonics: https://github.com/howardjp/phonics
.. _stringmetric: https://github.com/rockymadden/stringmetric

What is the process for adding a new class to the library?
----------------------------------------------------------

The process of adding a new class follows roughly the following steps:

    - Discover that a new (unimplemented) measure/algorithm/method exists
    - Locate the original source of the algorithm (a journal article, a
      reference implementation, etc.). And save the reference to it in
      docs/abydos.bib.

        - If the original source cannot be located for reference, use an
          adequate secondary source and add its reference info to
          docs/abydos.bib.

    - Implement the class based on its description/reference implementation.
    - Create a test class and add all examples and test cases from the
      original source. Add other reliable test cases from other sources, if
      they are available.
    - Ensure that the class passes all test cases.
    - Add test cases, as necessary, until test coverage reaches 100%, or as
      close to 100% as possible.

Are these really Frequently Asked Questions?
--------------------------------------------

No. Most of these questions have never been explicitly asked.
