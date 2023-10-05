import operator
from typing import Optional, Type

import pytest

from pytypelevel import Semigroup, semigroup


def test_semigroup__instances():

    str_concat: Type[Semigroup[str]] = semigroup(operator.add)
    assert str_concat.combine('hello', 'world') == 'helloworld'
    assert str_concat.combine_n('ha', 3) == 'hahaha'
    assert str_concat.combine_all_option(['one', 'two', 'three']) == 'onetwothree'
    assert str_concat.combine_all_option([]) is None
    rev_str_concat: Type[Semigroup[str]] = str_concat.reverse()
    assert rev_str_concat.combine('hello', 'world') == 'worldhello'
    rev2_str_concat: Type[Semigroup[str]] = rev_str_concat.reverse()
    assert rev2_str_concat.combine('hello', 'world') == 'helloworld'

    str_stripconcat: Type[Semigroup[str]] = semigroup(lambda s1, s2: s1.strip() + s2.strip())
    assert str_stripconcat.combine('  hello  ', '  world') == 'helloworld'
    assert str_stripconcat.combine_n(' ha ', 3) == 'hahaha'
    assert str_stripconcat.combine_all_option(['one_   ', '    two_', ' three']) == 'one_two_three'
    assert str_stripconcat.combine_all_option([]) is None
    rev_str_stripconcat: Type[Semigroup[str]] = str_stripconcat.reverse()
    assert rev_str_stripconcat.combine('hello ', 'world    ') == 'worldhello'
    rev2_str_stripconcat: Type[Semigroup[str]] = rev_str_stripconcat.reverse()
    assert rev2_str_stripconcat.combine('   hello_ ', ' world  ') == 'hello_world'
    
    int_sum: Type[Semigroup[int]] = semigroup(operator.add)
    assert int_sum.combine(6, 8) == 14
    assert int_sum.combine_n(16, 4) == 64
    assert int_sum.combine_all_option([1, 2, 3, 4]) == 10
    assert int_sum.combine_all_option([]) is None
    rev_int_sum: Type[Semigroup[int]] = int_sum.reverse()
    assert rev_int_sum.combine(6, 8) == 14
    rev2_int_sum: Type[Semigroup[int]] = rev_int_sum.reverse()
    assert rev2_int_sum.combine(8, 8) == 16