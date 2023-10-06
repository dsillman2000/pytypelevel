import operator
from typing import Optional, Type

import pytest

from pytypelevel import Semigroup


def test_semigroup_instances__str_concat():

    str_concat = Semigroup(operator.add)
    assert str_concat.combine('hello', 'world') == 'helloworld'
    assert str_concat.combine_n('ha', 3) == 'hahaha'
    assert str_concat.combine_all_option(['one', 'two', 'three']) == 'onetwothree'
    assert str_concat.combine_all_option([]) is None

    rev_str_concat = str_concat.reverse()
    rev2_str_concat = rev_str_concat.reverse()
    assert rev_str_concat.combine('hello', 'world') == 'worldhello'
    assert rev2_str_concat.combine('hello', 'world') == 'helloworld'

    interc_spc_str = str_concat.intercalate(' ')
    assert interc_spc_str.combine('hello', 'world') == 'hello world'

def test_semigroup_instances__str_stripconcat():

    str_stripconcat = Semigroup(lambda s1, s2: s1.strip() + s2.strip())
    assert str_stripconcat.combine('  hello  ', '  world') == 'helloworld'
    assert str_stripconcat.combine_n(' ha ', 3) == 'hahaha'
    assert str_stripconcat.combine_all_option(['one_   ', '    two_', ' three']) == 'one_two_three'
    assert str_stripconcat.combine_all_option([]) is None

    rev_str_stripconcat = str_stripconcat.reverse()
    rev2_str_stripconcat = rev_str_stripconcat.reverse()
    assert rev_str_stripconcat.combine('hello ', 'world    ') == 'worldhello'
    assert rev2_str_stripconcat.combine('   hello_ ', ' world  ') == 'hello_world'
    
    interc_hyp_str_stripconcat = str_stripconcat.intercalate('-')
    assert interc_hyp_str_stripconcat.combine('  hello ', 'world   ') == 'hello-world'

def test_semigroup_instances__int_sum():

    int_sum = Semigroup(operator.add)
    assert int_sum.combine(6, 8) == 14
    assert int_sum.combine_n(16, 4) == 64
    assert int_sum.combine_all_option([1, 2, 3, 4]) == 10
    assert int_sum.combine_all_option([]) is None

    rev_int_sum = int_sum.reverse()
    rev2_int_sum = rev_int_sum.reverse()
    assert rev_int_sum.combine(6, 8) == 14
    assert rev2_int_sum.combine(8, 8) == 16

    interc_1_int_sum = int_sum.intercalate(1)
    assert interc_1_int_sum.combine(1, 7) == 9