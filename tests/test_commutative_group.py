import operator

from pytypelevel import CommutativeGroup


def test_commutative_group_instances__intsum():

    intsum = CommutativeGroup[int](operator.add, 0, operator.neg)
    
    assert intsum.combine(2, 3) == intsum.combine(3, 2) == 5 and \
           intsum.combine(5, -5) == intsum.combine(-5, 5) == intsum.empty == 0 and \
           intsum.combine_n(3, 5) == intsum.combine_n(5, 3) == 15
    assert intsum.combine_all([5, 7, 8, 9]) == intsum.combine_all_option([5, 7, 8, 9]) == 29