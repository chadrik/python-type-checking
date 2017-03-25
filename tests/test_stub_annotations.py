from test_comment_annotations import simple_pyi_override, with_args_and_pyi_override, tuple_test


simple_pyi_override('foo')
simple_pyi_override(1)


# when using @overload with multiple definitions, pycharm uses only the first
with_args_and_pyi_override('foo')
with_args_and_pyi_override(1, 2)              # problem incorrectly detected: pycharm
with_args_and_pyi_override(1, 2, 'foo')


# the results below suggest that the .pyi file *completely* replaces the .py
# file in mypy, rather than merging with it, as with pycharm
tuple_test(('foo', 2), (1, 2, 3))
tuple_test((2, 2), ('foo', 'foo'))            # problem detected: pycharm
