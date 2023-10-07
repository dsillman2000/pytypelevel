import operator

from pytypelevel import Semigroup


def test_semigroup_instances__str_concat():

    str_concat = Semigroup(operator.add)

    assert str_concat.combine('hello', 'world') == 'helloworld'
    assert str_concat.combine_n('ha', 3) == 'hahaha'
    assert str_concat.combine_all_option(['one', 'two', 'three']) == 'onetwothree'
    assert str_concat.combine_all_option([]) is None
    assert Semigroup.first().combine('a', 'b') == 'a'
    assert Semigroup.last().combine('a', 'b') == 'b'
    assert Semigroup.last().reverse().combine('a', 'b') == \
           Semigroup.first().combine('a', 'b') == 'a'

    rev_str_concat = str_concat.reverse()
    rev2_str_concat = rev_str_concat.reverse()

    assert rev_str_concat.combine('hello', 'world') == 'worldhello'
    assert rev2_str_concat.combine('hello', 'world') == 'helloworld'

    interc_spc_str = str_concat.intercalate(' ')

    assert interc_spc_str.combine('hello', 'world') == 'hello world'
    assert interc_spc_str.maybe_combine(None, 'not none') == \
           interc_spc_str.maybe_combine('not none', None) == \
           interc_spc_str.maybe_combine('not', 'none') == 'not none'
    
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
    assert interc_hyp_str_stripconcat.maybe_combine(None, 'not-none') == \
           interc_hyp_str_stripconcat.maybe_combine('not-none', None) == \
           interc_hyp_str_stripconcat.maybe_combine('not', 'none') == 'not-none'

def test_semigroup_instances__int_sum():

    int_sum = Semigroup(operator.add)
    
    assert int_sum.combine(6, 8) == 14
    assert int_sum.combine_n(16, 4) == 64
    assert int_sum.combine_all_option([1, 2, 3, 4]) == 10
    assert int_sum.combine_all_option([]) is None
    assert Semigroup.first().combine(1, 2) == 1
    assert Semigroup.last().combine(2, 3) == 3
    assert Semigroup.last().reverse().combine(3, 4) == \
           Semigroup.first().combine(3, 4) == 3

    rev_int_sum = int_sum.reverse()
    rev2_int_sum = rev_int_sum.reverse()
    
    assert rev_int_sum.combine(6, 8) == 14
    assert rev2_int_sum.combine(8, 8) == 16

    interc_1_int_sum = int_sum.intercalate(1)
    
    assert interc_1_int_sum.combine(1, 7) == 9
    assert interc_1_int_sum.maybe_combine(None, 2) == \
           interc_1_int_sum.maybe_combine(2, None) == \
           interc_1_int_sum.maybe_combine(1, 0) == 2 