from test_comment_annotations import simple_pyi_override, with_args_and_pyi_override, tuple_test


simple_pyi_override('foo')                    # OK!
simple_pyi_override(1)                        # problem detected: mypy, pycharm


with_args_and_pyi_override('foo')             # OK!
with_args_and_pyi_override(1, 2)              # OK!
with_args_and_pyi_override(1, 2, 'foo')       # problem detected: mypy, pycharm

# the .pyi file *completely* replaces the .py file in mypy and pycharm (note
# above that tuple_test is not imported correctly because it exists only in
# test_comment_annotations.py and not test_comment_annotations.pyi
tuple_test(('foo', 2), (1, 2, 3))
tuple_test((2, 2), ('foo', 'foo'))
