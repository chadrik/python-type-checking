from typing import AnyStr, Generic, List, Dict, Tuple, Sequence, Set, Type, TypeVar, Pattern, Iterable, Container, Union

import re
from collections import OrderedDict, deque, defaultdict
# created a local copy of collections to test if providing a .pyi would help
# with OrderedDict issues.  it did not.
# from mycollections import OrderedDict

# strings
# =======

def bytestring_test(s):
    # type: (str) -> str
    return s

bytestring_test('x')                   # OK!
bytestring_test(u'x')                  # problem detected: mypy, pycharm
bytestring_test(1)                     # problem detected: mypy, pycharm


def unicodestring_test(s):
    # type: (unicode) -> unicode
    return s

# pycharm allows str for unicode?
unicodestring_test('x')                 # problem detected: mypy
unicodestring_test(u'x')                # OK!
unicodestring_test(1)                   # problem detected: mypy, pycharm


def anystr_test(s):
    # type: (AnyStr) -> AnyStr
    return s

anystr_test('x')                        # OK!
anystr_test(u'x')                       # OK!
anystr_test(1)                          # problem detected: mypy, pycharm


# Builtin Generics
# ================

# List
# ----

l = list()  # type: List[int]
l.append(1)                             # OK!
l.append('x')                           # problem detected: mypy, pycharm

# Set
# ---

l = set()  # type: Set[int]
l.add(1)                                # OK!
l.add('x')                              # problem detected: mypy, pycharm


def container_test(arg):
    # type: (Container[int]) -> int
    return arg[0]                       # problem detected: mypy, pycharm


container_test({0})
container_test([0])
container_test({'foo'})                 # problem detected: mypy, pycharm
container_test({'foo': 1})              # problem detected: mypy, pycharm
# same as above:
container_test(dict(foo=1))             # problem detected: mypy
# same as above:
ddd = dict(foo=1)
container_test(ddd)                     # problem detected: mypy


def iterable_test(arg):
    # type: (Iterable[int]) -> int
    return arg[0]                       # problem detected: mypy, pycharm


def sequence_test(arg):
    # type: (Sequence[int]) -> int
    return arg[0]                       # OK!


def regex_test(arg):
    # type: (Pattern) -> None
    return

regex_test(re.compile(r'foo'))
regex_test(False)                        # problem detected: mypy, pycharm


# Dict
# ----

def dict_test(arg):
    # type: (Dict[str, int]) -> None
    return

dict_test(2)                             # problem detected: mypy, pycharm
dict_test(dict(foo='bar'))               # problem detected: mypy, pycharm
dict_test(dict(foo=2))                   # OK!
dict_test({'foo': 'bar'})                # problem detected: mypy, pycharm
dict_test({'foo': 2})                    # OK!
arg = {'foo': 'bar'}
dict_test(arg)                           # problem detected: mypy, pycharm


# Tuple
# -----

def tuple_test(arg1, arg2):
    # type: (Tuple[str, int], Tuple[int, ...]) -> None
    return

tuple_test(('foo', 2), (1, 2, 3))       # OK! problem incorrectly detected: pycharm
tuple_test((2, 2), ('foo', 'foo'))      # problem detected: mypy, pycharm


# Other Generics
# ==============

# OrderedDict
# -----------

def odict_test(arg):
    # type: (OrderedDict[str, int]) -> None
    return

odict_test(2)                            # problem detected: mypy, pycharm
odict_test(OrderedDict(foo='bar'))       # problem detected: mypy
odict_test(OrderedDict(foo=2))           # OK!
odict_test(OrderedDict({'foo': 'bar'}))  # problem detected: mypy
odict_test(OrderedDict({'foo': 2}))      # OK!
arg = OrderedDict({'foo': 'bar'})
odict_test(arg)                          # problem detected: mypy
arg2 = OrderedDict({'foo': 'bar'})       # type: OrderedDict[str, str]
odict_test(arg2)                         # problem detected: mypy, pycharm
arg2['this'] = 'that'                    # OK!
arg2['this'] = 1                         # problem detected: mypy

# deque
# -----

l = deque()  # type: deque[int]
l.append(1)                             # OK!
l.append('x')                           # problem detected: mypy


# Custom Generic
# --------------

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self):
        # Create an empty list with items of type T
        self.items = []  # type: List[T]

    def push(self, item):
        # type: (T) -> None
        self.items.append(item)

    def pop(self):
        # type: () -> T
        return self.items.pop()

    def empty(self):
        # type: () -> bool
        return not self.items

stack = Stack()  # type: Stack[int]
stack.push(1)
stack.push('x')                          # problem detected: mypy, pycharm


# Class discovery
# ===============

def external_test1(arg):
    # type: (othermodule.ExternalType) -> None
    return

external_test1(2)                       # mypy nor pycharm can locate othermodule


import othermodule2

def external_test2(typ):
    # type: (othermodule2.ExternalType2) -> None
    print(typ)
    return

external_test2(2)                       # problem detected: mypy
ot = othermodule2.ExternalType()
external_test2(ot)                       # OK!

# Type alias
# ==========

# https://youtrack.jetbrains.com/issue/PY-19807
Number = Union[int, float]


def type_alias_test(x):
    # type: (Number) -> Number
    return x + 1

type_alias_test('2')                   # problem detected: mypy, pycharm


# Type
# ====

class Foo(object):

    @classmethod
    def bar(cls):
        pass


def get_class_type():
    # type: () -> Type[Foo]
    return Foo

get_class_type().bar()                 # OK!
get_class_type().bad()                 # problem detected: mypy, pycharm


# Star Args
# =========

def multiline_test(arg1,  # type: str
                   arg2,  # type: List[int]
                   *args  # type: Iterable[int]
                   ):
    # type: (...) -> str
    return 'xxx'

multiline_test('foo', [1]).format()    # OK!
multiline_test('foo', 'bar')           # problem detected: mypy, pycharm
multiline_test('foo', [1], [1, 2, 3])  # OK!


def with_args1(*args):
    # type: (*str) -> None
    pass

with_args1('foo')                      # OK!
with_args1('foo', 1)                   # problem detected: mypy, pycharm


# with the star in the type comment, pycharm and mypy interprets this as:
# "each item in args must be Iterable[int]"
def with_args2(*args):
    # type: (*Iterable[int]) -> None
    pass


with_args2(1, 2, 3)                   # problem detected: mypy, pycharm
with_args2(['a', 'b', 'c'])           # problem detected: mypy, pycharm
with_args2([1, 2, 3], [4, 5, 6])      # OK!


# without the star in the type comment, pycharm interprets this as:
# "each item in args must be int"
# mypy interprets this the same as above regardless of the *
def with_args3(*args):
    # type: (Iterable[int]) -> None
    pass


with_args3(1, 2, 3)                   # problem detected: mypy
with_args3(['a', 'b', 'c'])           # problem detected: mypy, pycharm
with_args3([1, 2, 3], [4, 5, 6])      # OK! problem incorrectly detected: pycharm


def with_args4(*args):
    # type: (*Tuple[str, int, float]) -> None
    pass


with_args4(('a', 1, 1.1), ('b', 0, 0.1))
with_args4('a', 1, 1.1)


def simple_pyi_override(x):
    pass

def with_args_and_pyi_override(*args):
    pass
