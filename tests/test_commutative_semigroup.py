import operator

from pytypelevel import CommutativeSemigroup


def test_commutative_semigroup_instances__intmul():

    intmul = CommutativeSemigroup[int](operator.mul)

    assert intmul.combine(3, 7) == intmul.combine(7, 3) == 21
    assert intmul.reverse() == intmul
    assert intmul.intercalate(2).combine(3, 4) == 24