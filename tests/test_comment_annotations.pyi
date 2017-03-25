from typing import overload, Container


def container_test(arg: Container[int]) -> int:
    pass

def simple_pyi_override(x: str) -> str:
    pass

@overload
def with_args_and_pyi_override(n: str) -> str:
    pass

@overload
def with_args_and_pyi_override(a: int, b: int) -> str:
    pass

