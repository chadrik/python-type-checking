from typing import List, Tuple, Type, Pattern, Iterable, Container

import re


from collections import OrderedDict


def container_test(arg):
    # type: (Container[int]) -> int
    return arg[0]  # fail


container_test({0})
container_test({'foo'})  # fail
container_test(dict(foo=1))  # fails in mypy, but not pycharm


def iterable_test(arg):
    # type: (Iterable[int]) -> int
    return arg[0]


# FIXME: this isn't working. how do you type check regular expressions?
def regex_test(arg):
    # type: (re.Pattern) -> None
    return

regex_test(re.compile(r'foo'))
regex_test(False)


def odict_test(arg):
    # type: (OrderedDict[str, int]) -> None
    return

odict_test(2)

# import othermodule
def external_test(arg):
    # type: (othermodule.ExternalType) -> None
    return

external_test(2)
# external_test(othermodule.ExternalType())


class User(object):
    pass

class BasicUser(User):
    def upgrade(self):
        """Upgrade to Pro"""

class ProUser(User):
    def pay(self):
        """Pay bill"""

def new_user(user_class):
    # type: (Type[User]) -> None
    user = user_class()

new_user(ProUser)


class Foo(object):

    @classmethod
    def bar(cls):
        pass

def get_class_type():
    # type: () -> Type[Foo]
    return Foo

get_class_type().bar()
get_class_type().bad()

def get_class_type2():
    """
    :return: Type[Foo]
    """
    return Foo

get_class_type2().bar()
get_class_type2().bad()


def multiline_test(arg1,  # type: str
                   arg2   # type: List[int]
                   ):
    # type: (...) -> str
    return 'xxx'

multiline_test('foo', 'bar').format()
