
The Tools
---------

There are a handful of tools for performing pep484-compatible type
checking. Each has its pros and cons. Both perform static code analysis,
which means they are not actually importing and running your modules:
instead they parse and analyze your code. This is safer, but it means
that dynamically generated objects can not be inspected.

mypy
~~~~

`mypy <http://mypy-lang.org/>`__ is a command-line tool much like a
linter that scans your code and prints out errors. The developers of
mypy are leading the charge on type-checking. PEP 484 was originally
inspired by mypy and Guido himself is now currently involved in its
development.

Below are your options support by mypy for adding type annotations to
functions in python 2.7 (more info
`here <http://mypy.readthedocs.io/en/latest/python2.html>`__):

**Single-line:**

.. code:: python

    def doit(inputs, enabled):
        # (Union[str, List[str]],  Dict[str, bool]) -> Iterable[str]
        "Do something with those inputs"
        ...

The bummer with this is it can get very long, and it's hard to visually
associate the argument with the type.

**Multi-line:**

.. code:: python

    def doit(inputs,    # type: Union[str, List[str]]
             enabled    # type: Dict[str, bool]
             ):
        # type: (...) -> Iterable[str]
        "Do something with those inputs"
        ...

A bit more verbose, but more legible.

One aspect of mypy which may make it difficult for you to integrate into your
build/release cycle is that python 3.5+ is required to run it, even if you're
analyzing python 2.7 code.


PyCharm
~~~~~~~

PyCharm is my new favorite IDE. Its code analysis goes deep, and it
saves my ass daily. Now that I've been making it aware of my argument
and return types, it's basically SkyNet (or will be, with just a few
more upgrades...).

As of this writing, PyCharm supports both the single-line and multi-line styles
above, as well as PEP484-compatible types delivered via docstrings. For the
latter you have to be pretty anal about your formatting: If you're too
loosey-goosey the parser will give up. PyCharm can parse four styles of
docstrings.

**reStructureText style**

.. code:: python

    def doit(inputs, enabled):
        """Do something with those inputs

        :param inputs: input names
        :type inputs:  Union[str, List[str]]
        :param enabled: mapping of input names to enabled status
        :type enabled: Dict[str, bool]
        :rtype: Iterable[str]
        """
        ...

Ugly, but gets the job done. Epydoc-style docstrings are the same but
with an ``@`` instead of the leading ``:``.

**google style**

.. code:: python

    def doit(inputs, enabled):
        """Do something with those inputs

        Args:
            inputs (Union[str, List[str]]):  input names
            enabled (Dict[str, bool]):  mapping of input names to
                enabled status

        Returns:
            Iterable[str]: enabled inputs
        """
        ...

Compact, but legible.

**numpy style**

.. code:: python

    def doit(inputs, enabled):
        """Do something with those inputs

        Parameters
        ----------
        inputs : Union[str, List[str]]
            input names
        enabled: Dict[str, bool]
            mapping of input names to enabled status

        Returns
        -------
        Iterable[str]
            enabled inputs
        """
        ...

My personal favorite.

The main downside with PyCharm for PEP484-style type-checking is that it's
still playing catchup with mypy.  Some pretty fundamental features are still
missing:

- `Type <https://youtrack.jetbrains.com/issue/PY-20057>`__
- `Type aliases <https://youtrack.jetbrains.com/issue/PY-19807>`__
- `TypeVar <https://youtrack.jetbrains.com/issue/PY-19915>`__
- `Generics <https://youtrack.jetbrains.com/issue/PY-19939>`__

Plus, I'd love to see more `visual feedback <https://youtrack.jetbrains.com/issue/PY-20530?query=pep484>`__

If nothing else comes from writing this, it will be worth it if a few people
click on the links above and make some noise on those issues.

pytype
~~~~~~

I'm including `pytype <https://github.com/google/pytype>`__ from Google for
the sake of completeness.  It's a command-line tool like mypy.
The main thing it has going for it is that it can
be run using python 2.7, unlike mypy which can only be run using python 3.5+
(both tools can analyze python 3.x code).


Comparison
~~~~~~~~~~

PyCharm gives you near instant feedback about type incompatibilities in
the context of your code, which creates an addictive feedback loop that
encourages ever more type-hinting. Mypy on the other hand is a bit of a
pain. You have to run it manually, then dig through its cryptic output
and look up corresponding line numbers.  It's really meant to be integrated
into your build/release process.

I also really like that PyCharm let's me continue to specify types within
docstrings.  For existing code, basic types are already working within
PyCharm, so I just need to upgrade the more exotic recipes to the new standard.
Also, I prefer to have type info adjacent to the description of the type.

The main downside of PyCharm is that it is not as thorough as mypy and
there are still a number of extremely important features that are not
implemented at this moment, though I have confidence that it will improve in the
short term. mypy is also capable of statically typing individual variables not just
function arguments and returns.

There's nothing stopping you from using both in tandem -- PyCharm as the
immediate first line of defense and mypy as a more thorough check run by
continuous integration.
