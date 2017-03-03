
Type Classes
------------

The first thing to understand is that type annotations are actual python
classes. You must import them from ``typing`` to use them. This is
admittedly a bit of a nuisance, but it makes more sense when you
consider that the syntax integration in python 3.5 means you're
attaching objects to function definitions just as you do when providing
a default value to an argument. In fact, you can use
``typing.get_type_hints()`` function to inspect type hint objects on a
function at runtime, just as you would inspect argument defaults with
``inspect.getargspec()``.

Type classes fall into several categories, which we'll review below.

Foundational Types
~~~~~~~~~~~~~~~~~~

The core set of types is pretty well covered in the `mypy
docs <http://mypy.readthedocs.io/en/latest/kinds_of_types.html>`__, but
I'll give a brief overview below.

Any
^^^

Represents any type.

If a function returns ``None`` you should specify this explicitly,
because if omitted it defaults to ``Any`` which is more permissive.

    Unlike ``Any``, ``object`` is an ordinary static type, and only
    operations valid for all types are accepted for ``object`` values.

``Any`` is thus more permissive.

Callable
^^^^^^^^

Used to denote a function or bound method with a particular signature.

Here's a simple function and how to encode that as a type annotation:

.. code:: python

    def repeat(s, count):
        # type: (str, int) -> str
        return s * count

.. code:: python

    Callable[[str, int], str]

Or, if you only care about the return result:

.. code:: python

    Callable[..., str]

Union
^^^^^

Used when there is more than one valid type.

.. code:: python

    Union[str, List[str]]

Optional
^^^^^^^^

Shorthand for a type which is allowed to be ``None``.

These are equivalent:

.. code:: python

    Optional[int]
    Union[int, None]

In mypy ``None`` is by default a valid value for every type, but due to
popular demand that is going to change, though I'm not sure in what time
frame. It's already possible to change the behavior of the type-checker
using a flag. Thus, if you're getting started now, its best to get in
the habit of adding the ``Optional`` type modifier to denote a type that
includes ``None``.

Type
^^^^

Used to denote that a type should be an uninstantiated class.

.. code:: python

    Type[MyClass]
    Type[Union[MyClass, OtherClass]]

Type Aliases
^^^^^^^^^^^^

This is a technique rather than a type. Remember how we discussed that
type definitions are regular python objects? Well, that means you can
assign them to module-level variables and use these variables in your
annotations. This is handy if you have a lot of functions that take the
same complex recipe.

(broken in pycharm)

.. code:: python

    from typing import Dict, List, Union
    PropertiesType = Dict[str, List[str]]
    PropertiesListType = List[Dict[str, PropertiesType]]

    def process_properties(props):
        # type: (PropertiesListType) -> None
        ...

Generic
^^^^^^^

This is the base class for all the collection classes covered below.
It's what gives them the bracket syntax for type-specialization (e.g.
``Container[int]``). My epiphany with type-hinting came when I realized
that subclasses of ``Generic`` are not just for defining type-hints. By
using ``Generic`` as an alternative base class to ``object`` when
creating your own collection classes, your classes can be used both as a
collection (by instantiating it as you normally would) and as a type
annotation (by using ``[]`` on the class itself). Check out the
`Stack
example <http://mypy.readthedocs.io/en/latest/generics.html#generics>`__
in the mypy docs to see an example.

(broken in pycharm)

TypeVar
^^^^^^^

``TypeVar`` lets you create relationships and restrictions *between* an
argument and other arguments or return values.

For example, let's say that you have a function which takes a value of
any type, and returns a value of the same type.

If we use ``Any`` then we fail to make that relationship:

.. code:: python

    def passthrough(input):
        # type: (Any) -> Any
        return input

Both input and result may be any type, but there's nothing to indicate that
they will always be the same type as each other.

To give the type checker more context, we create a ``TypeVar`` and share it
between annotations.

.. code:: python

    T = TypeVar('T')

    def passthrough(input):
        # type: (T) -> T
        return input

This is called a generic function. Of course, it gets more interesting
than this. A ``TypeVar`` can be restricted in the same way as any other value:

.. code:: python

    TypeVar('T', bound=Callable[[int, str], bool])

``TypeVars`` are often used with ``Generic`` collections (discussed more
below) to form a relationship between the collection and another
argument or return values. Here's a solid example from
`the docs on generics <http://mypy.readthedocs.io/en/latest/generics.html#generic-functions>`__:

.. code:: python

    from typing import TypeVar, Sequence

    T = TypeVar('T')

    def first(seq: Sequence[T]) -> T:
        return seq[0]

..  structural type checking is not yet supported


    Abstract Collection Types
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    The abstract collection classes are alternatives to their counterparts
    in the ``collections`` module that are augmented to support type
    specialization, e.g. ``Container[int]`` (in other words, they inherit
    from ``typing.Generic``).

    Below are some of the most commonly used abstract collection types. Each
    type adds a particular requirement, and subclasses build up requirements
    by (multiply) inheriting from simpler types. For example, in order to be
    a ``Container`` an object must implement ``__contains__``.

    When defining type annotations for your programs, it can be beneficial
    to use these abstract types rather than concrete types such as ``list``
    or ``set`` because it allows greater flexibility. Rather than requiring
    specific types, you specify the abilities that are required by a type,
    and the type-checker ensures that passed objects possess that ability.
    For example, if an argument to a function is only used to test the
    existence of some item within it, adding a ``Container`` type annotation
    will permit ``list``, ``set``, ``tuple``, ``frozenset``, and quite a few
    more. Be aware, however, that this will also permit ``str``, since this
    is conceptually a container of str characters. We can prevent this by
    adding a specialization to the container, such as ``Container[int]``.

    +-----------------------+------------------------+------------------------------------------+
    | Type                  | Added Requirement      | Inherited Requirements                   |
    +=======================+========================+==========================================+
    | ``Container``         | ``foo in obj``         |                                          |
    +-----------------------+------------------------+------------------------------------------+
    | ``Hashable``          | ``hash(obj)``          |                                          |
    +-----------------------+------------------------+------------------------------------------+
    | ``Iterable``          | ``for foo in obj``     |                                          |
    +-----------------------+------------------------+------------------------------------------+
    | ``Iterator``          | ``next(obj)``          | ``Iterable``                             |
    +-----------------------+------------------------+------------------------------------------+
    | ``Sized``             | ``len(obj)``           |                                          |
    +-----------------------+------------------------+------------------------------------------+
    | ``Mapping``           | ``obj['key']``         | ``Sized``, ``Iterable``, ``Container``   |
    +-----------------------+------------------------+------------------------------------------+
    | ``MutableMapping``    | ``obj['key'] = foo``   | ``Mapping``                              |
    +-----------------------+------------------------+------------------------------------------+
    | ``AbstractSet``       |                        | ``Sized``, ``Iterable``, ``Container``   |
    +-----------------------+------------------------+------------------------------------------+
    | ``MutableSet``        |                        | ``AbstractSet``                          |
    +-----------------------+------------------------+------------------------------------------+
    | ``Sequence``          | ``obj[0]``             | ``Sized``, ``Iterable``, ``Container``   |
    +-----------------------+------------------------+------------------------------------------+
    | ``MutableSequence``   | ``obj[0] = foo``       | ``Sequence``                             |
    +-----------------------+------------------------+------------------------------------------+

    For the full list and more details, see the python 3.x documentation for
    `collections.abc <https://docs.python.org/3/library/collections.abc.html>`__
    (The abstract classes from the ``collections`` module were moved to
    ``collections.abc`` in python 3)

    Just as with the abstract collection types, you can use these ``typing``
    classes in ``isinstance`` tests:

    .. code:: python

    from typing import Iterable, Sized
    isinstance('foo', Iterable)
    isinstance('foo', Sized)

    Note that the return type from a generator is ``Generator``:

    .. code:: python

    def fib():
        # type: () -> Generator
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

Concrete Collection Types
~~~~~~~~~~~~~~~~~~~~~~~~~

The concrete collection types are intended to be used as stand-ins for
certain key collections for the purpose of type-hinting. They cannot be
instantiated: For that, you need to continue to use their "real"
counterparts.

In an ideal world, all of the collections in python's standard library
would subclass from ``Generic``, which would allow the same class to
serve as both implementation and type annotation. Perhaps if type
hinting takes off this will be addressed one day, in the meantime we
have this split.

The concrete collection types:

-  ``Tuple``
-  ``Dict``
-  ``DefaultDict``
-  ``List``
-  ``Set``

These are pretty straight-forward to use. You can glean all you need
from a few simple examples:

+-----------------------+----------------------------------------------------------------+
| Example               | Explanation                                                    |
+=======================+================================================================+
| ``list``              | list of any type, possibly heterogeneous                       |
+-----------------------+----------------------------------------------------------------+
| ``List[Any]``         | same as above                                                  |
+-----------------------+----------------------------------------------------------------+
| ``List[int]``         | list containing only integers                                  |
+-----------------------+----------------------------------------------------------------+
| ``dict``              | dictionary with any key or value                               |
+-----------------------+----------------------------------------------------------------+
| ``Dict[Any, Any]``    | same as above                                                  |
+-----------------------+----------------------------------------------------------------+
| ``Dict[str, int]``    | dictionary whose keys are strings and values are integers      |
+-----------------------+----------------------------------------------------------------+
| ``tuple``             | tuple with any quantity of any type                            |
+-----------------------+----------------------------------------------------------------+
| ``Tuple[Any, ...]``   | same as above                                                  |
+-----------------------+----------------------------------------------------------------+
| ``Tuple[int]``        | tuple with a single integer. ex: ``(1,)``                      |
+-----------------------+----------------------------------------------------------------+
| ``Tuple[int, ...]``   | tuple with any number of ``int``                               |
+-----------------------+----------------------------------------------------------------+
| ``Tuple[int, str]``   | tuple whose first element is an integer and second is a string |
+-----------------------+----------------------------------------------------------------+

NamedTuple
~~~~~~~~~~

``typing.NamedTuple`` is an alternative to ``collections.namedtuple``
that supports type-checking.

Under the hood it wraps ``collections.namedtuple`` and tags the
resulting class with an attribute to track the field types, but in
reality, that's not even necessary as the static code analysis won't
have access to it.

Here's an example adapted from the docs. The ``Point`` class defined in
the following code is opaque to type-checking:

::

    from collections import namedtuple

    Point = namedtuple('Point', ['x', 'y'])
    p = Point(x=1, y='x')
    p.y / 2.0  # fails at runtime

By swapping it with ``typing.NamedTuple``, the ``Point`` class can now
be used as a type annotation in functions and instantiation of the type
can be properly validated.

::

    from typing import NamedTuple

    Point = NamedTuple('Point', [('x', int), ('y', int)])
    p = Point(x=1, y='x')  # issue detected by mypy
    p.y / 2.0

Ordinary Classes
~~~~~~~~~~~~~~~~

As you might expect, any class can be used as a type identifier. This
restricts objects to instances of this class and its subclasses.

The two tools -- mypy and PyCharm -- differ in how they find objects
specified in type annotations.

With mypy, the name given *must* be a valid identifier for that
object in the current module. For example, this works:

.. code:: python

    import zipfile

    def zipit(arg):
        # type: (zipfile.ZipFile) -> None
        return

But this does not:

.. code:: python

    import zipfile

    def zipit(arg):
        # type: (ZipFile) -> None
        return

This is because ``ZipFile`` does not identify any object at the scope of
the ``zipit`` function (to be honest, I'm actually not entirely sure how
the scoping works in mypy, but it has a module scope for sure). This
behavior makes sense if you think of the type-comments as placeholders
for the python 3.5 syntax additions. Again, it helps to think of type hints
the same way that you would default arguments.  In that light, I think it's
intuitive that it would not work without first importing ``zipfile``:

.. code:: python

    def zipit(arg: zipfile.ZipFile) -> None:
        return

This rule actually applies to any object defined externally to a comment-based
type annotation, such as type aliases, but it comes into play most often
with custom classes.

PyCharm is a bit more forgiving than mypy. If prefix your object with a dotted
module or package name, it will find the object within that module, assuming
your project search paths are setup correctly. Of course, if you plan to use
both tools in conjunction, you'll have to shoot for the lowest common
denominator, which is mypy.

..
    Structural checks, a.k.a. protocols.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    TODO

    ::

        `Reversible`
        `SupportsAbs`
        `SupportsFloat`
        `SupportsInt`

    Gotchas
    -------

    OrderedDict