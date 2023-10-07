import operator

from pytypelevel import Monoid


def test_monoid_instances__str_concat():

    str_concat = Monoid[str](operator.add, '')

    assert str_concat.is_empty('')
    assert str_concat.combine_n('v', 3) == 'vvv'
    assert str_concat.combine_n('v', 0) == str_concat.empty == ''
    assert str_concat.combine_all(['u', 'v', 'w']) == 'uvw'
    assert str_concat.reverse().combine_all(['e', 'c', 'a']) == 'ace'

def test_monoid_instances__str_stripconcat():

    str_stripconcat = Monoid[str](lambda a, b: a.strip() + b.strip(), '')

    assert str_stripconcat.is_empty('')
    assert str_stripconcat.combine_n('v   ', 3) == 'vvv'
    assert str_stripconcat.combine_n('v', 0) == str_stripconcat.empty == ''
    assert str_stripconcat.combine_all(['u', ' v ', 'w   ']) == 'uvw'
    assert str_stripconcat.reverse().combine_all(['e   ', 'c', ' a']) == 'ace'

def test_monoid_instances__int_sum():

    int_sum = Monoid[int](operator.add, 0)

    assert int_sum.is_empty(0)
    assert int_sum.combine_n(2, 3) == 6
    assert int_sum.combine_n(4, 0) == int_sum.empty == 0
    assert int_sum.combine_all([1, 2, 3, 6]) == 12
    assert int_sum.reverse().combine_all([7, 7, 8]) == 22