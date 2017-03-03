from typing import List, Tuple, Sequence, Type, Pattern, Iterable, Container, Union

import re
from collections import OrderedDict


def container_test(arg):
    """
    :type arg: Container[int]
    :rtype: int
    """
    return arg[0]  # problem detected


container_test({0})
container_test([0])
container_test({'foo'})  # problem detected
container_test(dict(foo=1))  # problem detected in mypy, but not pycharm


def iterable_test(arg):
    """
    :type arg: Iterable[int]
    :rtype: int
    """
    return arg[0]  # problem detected


def sequence_test(arg):
    """
    :type arg: Sequence[int]
    :rtype: int
    """
    return arg[0]


def regex_test(arg):
    """
    :type arg: Pattern
    :rtype: None
    """
    return

regex_test(re.compile(r'foo'))
regex_test(False)  # problem detected in mypy, but not pycharm


def odict_test(arg):
    """
    :type arg: OrderedDict[str, int]
    :rtype: None
    """
    return

odict_test(2)  # problem detected
odict_test(OrderedDict(foo='bar'))  # problem detected in mypy, but not pycharm
odict_test(OrderedDict(foo=2))


def tuple_test(arg1, arg2, ):
    # type: (Tuple[str, int], Tuple[int, ...]) -> None
    return

tuple_test(('foo', 2), (1, 2, 3))
tuple_test((2, 2), ('foo', 'foo'))  # problem detected


# import othermodule
def external_test(arg):
    """
    :type arg: othermodule.ExternalType
    :rtype: None
    """
    return


external_test(2)  # problem detected in pycharm, but not mypy (can't locate othermodule)
# external_test(othermodule.ExternalType())


class Vehicle(object):
    name = ''


class Car(Vehicle):
    wheels = 4


def test_isinstance(x):
    """
    :type x: Vehicle
    :rtype: None
    """
    print(x.name)
    if isinstance(x, Car):
        print(x.wheels)


def test_issubclass(x):
    """
    :type x: Type[Vehicle]
    :rtype: None
    """
    print(x.name)
    if issubclass(x, Car):
        print(x.wheels)


class Foo(object):

    @classmethod
    def bar(cls):
        pass


def get_class_type():
    """
    :rtype: Type[Foo]
    """
    return Foo

get_class_type().bar()  # problem incorrectly detected in pycharm because it misinterpets the result as 'Type'
get_class_type().bad()  # problem detected in pycharm but only because of the issue above


def with_args1(*args):
    """
    :type args: str
    :return: None
    """
    pass

with_args1('foo')
with_args1('foo', 1)


# with the star in the type comment, pycharm interprets this as:
# "each item in args must be Iterable[int]"
# BUT I can't get the same behavior with docstrings, regardless of where I put the *!
# def with_args2(*args):
#     """
#     :type args: Iterable[int]
#     :return: None
#     """
#     pass


def with_args2(*args):
    """
    Parameters
    ----------
    args: Iterable[int]

    """
    pass

with_args2(1, 2, 3)
with_args2(['a', 'b', 'c'])
with_args2([1, 2, 3], [4, 5, 6])


# without the star in the type comment, pycharm interprets this as:
# "each item in args must be int"
def with_args3(*args):
    # type: (Iterable[int]) -> None
    pass


with_args3(1, 2, 3)
with_args3(['a', 'b', 'c'])
with_args3([1, 2, 3], [4, 5, 6])


def with_args4(*args):
    # type: (*Tuple[str, int, float]) -> None
    pass


with_args4(('a', 1, 1.1), ('b', 0, 0.1))
with_args4('a', 1, 1.1)



# def blarg(foo=None, bar=None):
#     """
#     :type bar: str
#     :type foo: str
#     """
#     pass

# def blarg(foo=None, bar=None):
#     """
#     :Parameters:
#         bar : str
#         foo : str
#     """
#     pass

def blarg(foo=None, bar=None):
    """
    Parameters
    ----------
    bar : str
    foo : str
    """
    pass

blarg(foo=3)


