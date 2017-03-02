if False:
    from typing import Iterable, List, Container


class ExternalType(object):
    pass


def whatevs(arg):
    """

    Parameters
    ----------
    arg : List[str]

    Returns
    -------
    int
    """
    return 1


def blarg(arg):
    """

    Parameters
    ----------
    arg : Container[str]

    Returns
    -------
    int
    """
    return 1

whatevs('foo')

blarg({'foo'})
blarg(['foo'])
blarg(('foo',))
blarg('foo')
blarg(int)

