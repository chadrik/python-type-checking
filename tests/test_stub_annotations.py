from test_comment_annotations import with_args_and_pyi_override, tuple_test


with_args_and_pyi_override('foo')
with_args_and_pyi_override(1, 2)              # problem incorrectly detected: pycharm
with_args_and_pyi_override(1, 2, 'foo')


# pycharm is not finding the pyi file, but mypy is.  evidently the .pyi file
# *completely* replaces the .py file in mypy, rather than merging with it.
tuple_test(('foo', 2), (1, 2, 3))
tuple_test((2, 2), ('foo', 'foo'))
