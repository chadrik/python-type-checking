
Background
==========

Why Should I Care?
------------------

You may have heard about type-hints being added to python 3.5, and
wondered "why you should I care?". Well, the answer is much the same as
for documenting your code: type checking saves you time by preventing
mistakes and removing guesswork. Up until now, the best that we had in
terms of type specifications was a handful of conventions which were
ambiguous at best, and now we have a standard to build tools around.

Take the `numpy docstring
convention <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`__
as an example. They kindly give us some basic typing examples, such as
this:

::

    Parameters
    ----------
    filename : str
    copy : bool
    dtype : data-type
    iterable : iterable object
    shape : int or tuple of int
    files : list of str

But there's no guidance on how to combine these into more complex
recipes. As a result, I often see ambiguous type specifications that
look like this:

::

    list of str or int

Is the ``int`` *in* the list or *out* of it?

Moreover, there are no examples of how to handle complex tuples,
dictionary key and value types, callable signatures, or how to specify
types which are classes rather than instances.

The upshot is that with this much ambiguity, programmatic type checking
is pretty unreliable. To improve the situation, some IDEs like PyCharm
have proposed `their own
convention <https://www.jetbrains.com/help/pycharm/2016.1/type-hinting-in-pycharm.html>`__
which is a step forward, but do you really want to make your modules
IDE-specific?

Enter PEP 484
-------------

With `PEP 484 <https://www.python.org/dev/peps/pep-0484/>`__, Guido and
crew have figured all this out for you and created a standard for type
annotations which is now part of python 3.5. If you're using python 3.5
or greater, you can write function definitions like this:

.. code:: python

    def func(inputs: Union[str, List[str]],
             enabled: Dict[str, bool]) -> Iterable[str]:
        ...

Neat. But what about those of us still stuck on 2.x?

This is where we need to stop and clarify the difference between type
annotations and type checking. With the addition of pep484, python 3.5
gained two things:

1. a standard for describing types (e.g. ``Union[str, List[str]]``.)
2. syntax support for annotating function arguments and return values
   with type descriptions

Noticeably lacking here is actual *type checking*, i.e. inspection of
code to enforce that arguments and assignments match their declared
types. The developers of python left that role be filled by third-party
tools.

Back to python 2.x: A standard for describing types in unambiguous terms
is a big deal even without the syntax support added in 3.5, and the good
news is that the means for creating these type definitions, the
`typing module <https://github.com/python/mypy/blob/master/lib-typing/3.2/typing.py>`__,
is available for python 2.7. However, the lack of syntactical support
means that the type-checkers must provide their own conventions for
associating type descriptions with arguments and return values in python
2.7 code.

So, without further ado, let's get to the tools.
