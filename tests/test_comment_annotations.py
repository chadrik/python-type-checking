from typing import List, Dict, Tuple, Sequence, Type, Pattern, Iterable, Container

import re
from collections import OrderedDict


def container_test(arg):
    # type: (Container[int]) -> int
    return arg[0]                       # problem detected: mypy, pycharm


container_test({0})
container_test([0])
container_test({'foo'})                 # problem detected: mypy, pycharm
container_test(dict(foo=1))             # problem detected: mypy


def iterable_test(arg):
    # type: (Iterable[int]) -> int
    return arg[0]                       # problem detected: mypy, pycharm


def sequence_test(arg):
    # type: (Sequence[int]) -> int
    return arg[0]


def regex_test(arg):
    # type: (Pattern) -> None
    return

regex_test(re.compile(r'foo'))
regex_test(False)                        # problem detected: mypy


def dict_test(arg):
    # type: (Dict[str, int]) -> None
    return

dict_test(2)                             # problem detected: mypy
dict_test(dict(foo='bar'))               # problem detected: mypy
dict_test(dict(foo=2))
dict_test({'foo': 'bar'})                # problem detected: mypy, pycharm
dict_test({'foo': 2})
arg = {'foo': 'bar'}
dict_test(arg)                           # problem detected: mypy, pycharm


def odict_test(arg):
    # type: (OrderedDict[str, int]) -> None
    return

odict_test(2)                            # problem detected: mypy
odict_test(OrderedDict(foo='bar'))       # problem detected: mypy
odict_test(OrderedDict(foo=2))
odict_test(OrderedDict({'foo': 'bar'}))  # problem detected: mypy
odict_test(OrderedDict({'foo': 2}))
arg = OrderedDict({'foo': 'bar'})
odict_test(arg)  # problem detected: mypy


def tuple_test(arg1, arg2):
    # type: (Tuple[str, int], Tuple[int, ...]) -> None
    return

tuple_test(('foo', 2), (1, 2, 3))
tuple_test((2, 2), ('foo', 'foo'))      # problem detected: mypy, pycharm


# import othermodule
def external_test(arg):
    # type: (othermodule.ExternalType) -> None
    return


external_test(2)                       # problem detected: pycharm (mypy can't locate othermodule)
# external_test(othermodule.ExternalType())


class Vehicle(object):
    name = ''


class Car(Vehicle):
    wheels = 4


def test_isinstance(x):
    # type: (Vehicle) -> None
    print(x.name)
    if isinstance(x, Car):
        print(x.wheels)


def test_issubclass(x):
    # type: (Type[Vehicle]) -> None
    print(x.name)
    if issubclass(x, Car):
        print(x.wheels)

#
# def new_user(user_class):
#     # type: (Type[User]) -> None
#     user = user_class()
#
# new_user(ProUser)


class Foo(object):

    @classmethod
    def bar(cls):
        pass


def get_class_type():
    # type: () -> Type[Foo]
    return Foo

get_class_type().bar()
get_class_type().bad()                 # problem detected: mypy


def multiline_test(arg1,  # type: str
                   arg2,  # type: List[int]
                   *args  # type: Iterable[int]
                   ):
    # type: (...) -> str
    return 'xxx'

multiline_test('foo', [1]).format()
multiline_test('foo', 'bar')           # problem detected: mypy, pycharm
multiline_test('foo', [1], [1, 2, 3])  # problem incorrectly detected: pycharm


def with_args1(*args):
    # type: (*str) -> None
    pass

with_args1('foo')
with_args1('foo', 1)                   # problem detected: mypy, pycharm


# with the star in the type comment, pycharm and mypy interprets this as:
# "each item in args must be Iterable[int]"
def with_args2(*args):
    # type: (*Iterable[int]) -> None
    pass


with_args2(1, 2, 3)                   # problem detected: mypy, pycharm
with_args2(['a', 'b', 'c'])           # problem detected: mypy, pycharm
with_args2([1, 2, 3], [4, 5, 6])


# without the star in the type comment, pycharm interprets this as:
# "each item in args must be int"
# mypy interprets this the same as above regardless of the *
def with_args3(*args):
    # type: (Iterable[int]) -> None
    pass


with_args3(1, 2, 3)                   # problem detected: mypy
with_args3(['a', 'b', 'c'])           # problem detected: mypy, pycharm
with_args3([1, 2, 3], [4, 5, 6])      # problem incorrectly detected: pycharm


def with_args4(*args):
    # type: (*Tuple[str, int, float]) -> None
    pass


with_args4(('a', 1, 1.1), ('b', 0, 0.1))
with_args4('a', 1, 1.1)


def with_args_and_pyi_override(*args):
    pass
